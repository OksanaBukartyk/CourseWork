from functools import wraps

from flask import Blueprint, render_template, redirect, url_for, flash
from app.models import Order, Address, Product
from flask_login import login_required, current_user
from flask import request, abort
from datetime import datetime
from app import db
from app.orders.forms import CreateOrderForm, UpdateOrderForm, AddressForm

orders = Blueprint('orders', __name__, template_folder="templates", static_folder="static")


def admin_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin():
            return abort(403)
        return func(*args, **kwargs)

    return decorated_view


@orders.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@orders.route('/create/<id>', methods=['GET', 'POST'])
@login_required
def create(id):
    form = CreateOrderForm()
    product = Product.query.get(id)
    order_first = Order.query.filter_by(product_id=id, user_id=current_user.id, status='ordered').first()
    if order_first is None:
        if form.validate_on_submit():
            order = Order(product_id=product.id, color=form.color.data, count=form.count.data, user_id=current_user.id)
            db.session.add(order)
            db.session.commit()

            flash('Congratulations! You can continue to buy!', 'success')
            return redirect(url_for('products.products'))
    else:
        flash('In card allready!', 'success')
        return redirect(url_for('orders.order', id=order_first.id))

    return render_template('/orders/create.html', form=form, product=product)


@orders.route('/my_orders', methods=['GET', 'POST'])
@login_required
def my_orders():
    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)

    if q:
        orders = Order.query.filter(Order.user_id == current_user.id, Order.status == 'ordered').filter(
            Order.color.contains(q) | Order.count.contains(q)).paginate(page=page, per_page=4)
    else:
        orders = Order.query.filter(Order.user_id == current_user.id, Order.status == 'ordered').order_by(
            Order.timestamp.desc()).paginate(page=page, per_page=6)

    return render_template('/orders/my_orders.html', orders=orders)


'''
        !!!!!!!!!!!!!!Треба спробувати реалізувати
        
    https://stackoverflow.com/questions/53176976/how-to-insert-many-to-many-relationship-data-using-sqlalchemy
    
    https://question-it.com/questions/77309/flask-sqlalchemy-otnoshenie-mnogie-ko-mnogim-kak-vstavit-dannye
    '''


@orders.route('/<id>')
@login_required
def order(id):
    return render_template('/orders/order.html', order=Order.query.filter_by(id=id))


@orders.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    Order.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Order was deleted', 'success')
    return redirect(url_for('orders.my_orders'))


@orders.route('/done', methods=['GET', 'POST'])
@login_required
def done():
    form = AddressForm()
    if form.validate_on_submit():
        address_first = Address.query.filter_by(first_name=form.first_name.data, last_name=form.last_name.data,
                                                phone=form.phone.data,
                                                district=form.district.data, region=form.region.data,
                                                city=form.city.data,
                                                mail=form.mail.data, number=form.number.data).first()

        if address_first is None:
            address = Address(first_name=form.first_name.data, last_name=form.last_name.data, phone=form.phone.data,
                              district=form.district.data, region=form.region.data,
                              city=form.city.data,
                              mail=form.mail.data, number=form.number.data)
            db.session.add(address)
            db.session.commit()
            order = Order.query.filter_by(user_id=current_user.id, status='ordered').update(dict(address_id=address.id))

        else:
            order = Order.query.filter_by(user_id=current_user.id, status='ordered').update(
                dict(address_id=address_first.id))
        db.session.commit()

        Order.query.filter_by(user_id=current_user.id, status='ordered').update(dict(status='bought'))
        db.session.commit()

        flash('Congratulations!', 'success')
        return redirect(url_for('products.all_products'))

    return render_template('/orders/done.html', form=form)


@orders.route('/archive', methods=['GET', 'POST'])
@login_required
def archive():
    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)

    if q:
        orders = Order.query.filter(Order.user_id == current_user.id, Order.status == 'bought').filter(
            Order.color.contains(q) | Order.count.contains(q)).paginate(page=page, per_page=4)
    else:
        orders = Order.query.filter(Order.user_id == current_user.id, Order.status == 'bought').order_by(
            Order.timestamp.desc()).paginate(page=page, per_page=6)

    return render_template('/orders/archive.html', orders=orders)


@orders.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    form = UpdateOrderForm()
    order = Order.query.get(id)

    if form.validate_on_submit():

        Order.query.filter_by(id=id).update({ 'count': form.count.data, 'color': form.color.data,})
        db.session.commit()

        flash('Your order has been updated!', 'success')
        return redirect(url_for('orders.order', id = order.id ))
    elif request.method == 'GET':
        order = Order.query.get(id)

        form.count.data = order.count
        form.color.data = order.color

    return render_template('/orders/edit.html', title='Edit', form=form)
