from flask import Blueprint, render_template, redirect, url_for, flash
from app.models import Product, ProductImage
from flask_login import login_required, current_user
from flask import request,abort
from datetime import datetime
from app import db
from app.products.forms import CreateForm, UpdateProductForm,EditMainPhotoForm, EditOtherPhotoForm
from PIL import Image
from functools import wraps
from urllib.parse import urlparse, urljoin
import os
import secrets

products = Blueprint('products', __name__, template_folder="templates", static_folder="static")


def admin_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin():
            return abort(403)
        return func(*args, **kwargs)
    return decorated_view


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(products.root_path, 'static/profile_pics', picture_fn)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@products.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@products.route('/create', methods=['GET', 'POST'])
@admin_login_required
@login_required
def create():
    if current_user.is_admin:
        form = CreateForm()
        if form.validate_on_submit():
            product = Product(name=form.name.data, description=form.description.data,
                              price=form.price.data, count=form.count.data, category=form.category.data,
                              color=form.color.data)
            if form.avatar.data:
                picture_file = save_picture(form.avatar.data)
                product.avatar = picture_file
            db.session.add(product)
            db.session.commit()

            if form.picture.data:
                for file in form.picture.data:
                    picture_file = save_picture(file)
                    image_files = ProductImage(image_file=picture_file, product_id=product.id)
                    db.session.add(image_files)
                    db.session.commit()

            flash('Congratulations, you add new product!', 'success')
            page = request.args.get('page', 1, type=int)
            return render_template('/products/all_products.html',
                    products = Product.query.order_by(Product.timestamp.desc()).paginate(page=page, per_page=6))

    return render_template('/products/create.html', form=form)


@products.route('/all_products', methods=['GET', 'POST'])
def all_products():
    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)

    if q:
        products = Product.query.filter(Product.title.contains(q) | Product.body.contains(q)).order_by(
            Product.timestamp.desc()).paginate(page=page, per_page=3)
    else:
        products = Product.query.order_by(Product.timestamp.desc()).paginate(page=page, per_page=6)
    return render_template('/products/all_products.html', products=products)


@products.route('/<id>')
def product(id):
    form = UpdateProductForm()
    product = Product.query.get(id)
    if form.validate_on_submit():

        if form.avatar.data:
            picture_file = save_picture(form.avatar.data)
            product.avatar = picture_file
        db.session.add(product)
        db.session.commit()
    images = ProductImage.query.filter_by(product_id = id).all()
    product = Product.query.filter_by(id=id)
    return render_template('/products/product.html',images=images, product=product,form=form)



@products.route('/<int:id>/delete', methods=['GET', 'POST'])
@admin_login_required
@login_required
def delete(id):
    if current_user.is_admin:
        Product.query.filter_by(id=id).delete()
        ProductImage.query.filter_by(product_id=id).delete()
        db.session.commit()
        flash('Post was deleted', 'success')
        return redirect(url_for('products.all_products'))

    else:
        flash('You don`t have the permission to access', 'danger')
    return redirect(url_for('products.product', id=id))


@products.route('/<int:id>/edit', methods=['GET', 'POST'])
@admin_login_required
@login_required
def edit(id):
    form = UpdateProductForm()
    product = Product.query.get(id)
    if current_user.is_admin:
        if form.validate_on_submit():

            Product.query.filter_by(id=id).update({'name': form.name.data, 'description': form.description.data,
                                                   'price': form.price.data, 'count': form.count.data,
                                                   'color': form.color.data, 'category': form.category.data})
            db.session.commit()

            flash('Your post has been updated!', 'success')
            return redirect(url_for('products.product', id = id))
        elif request.method == 'GET':
            product = Product.query.get(id)
            form.name.data = product.name
            form.description.data = product.description
            form.price.data = product.price
            form.count.data = product.count
            form.color.data = product.color
            form.category.data = product.category

    else:
        flash('You don`t have the permission to access', 'danger')
        return redirect(url_for('products.product', id = id))
    return render_template('/products/edit.html', title='Edit', form=form)



@products.route('/<int:id>/edit_main', methods=['GET', 'POST'])
@admin_login_required
@login_required
def edit_main(id):
    if current_user.is_admin:
        form = EditMainPhotoForm()
        product=Product.query.filter_by(id=id)
        if form.validate_on_submit():
            if form.avatar.data:
                picture_file = save_picture(form.avatar.data)
                product.avatar = picture_file
            Product.query.filter_by(id=id).update({'avatar': product.avatar})

            db.session.commit()

            flash('Congratulations, you edit main photo!', 'success')
            return redirect(url_for('products.product', id = id))

    return render_template('/products/edit_main.html', form=form)


@products.route('/<int:id>/edit_other', methods=['GET', 'POST'])
@admin_login_required
@login_required
def edit_other(id):
    if current_user.is_admin:
        form = EditOtherPhotoForm()
        product=Product.query.filter_by(id=id)
        if form.validate_on_submit():
            if form.picture.data:
                ProductImage.query.filter_by(product_id=id).delete()
                for file in form.picture.data:
                    picture_file = save_picture(file)
                    image_files = ProductImage(image_file=picture_file, product_id=id)
                    db.session.add(image_files)
                    db.session.commit()
            db.session.commit()

            flash('Congratulations, you edit main photo!', 'success')
            return redirect(url_for('products.product', id = id))

    return render_template('/products/edit_other.html', form=form)