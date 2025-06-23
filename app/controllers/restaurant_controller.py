from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.db import Restaurant
from flask import current_app
from werkzeug.utils import secure_filename
import os
from app.models.db import Dish



restaurant_bp = Blueprint('restaurant', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@restaurant_bp.route('/restaurants/new', methods=['GET', 'POST'])
@login_required
def add_restaurant():
    if current_user.role != 'admin':
        flash('No tienes permiso para acceder aquí.', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        description = request.form.get('description')
        image = request.files.get('image')

        if not name or not image:
            flash('El nombre y la imagen son obligatorios.', 'error')
            return render_template('admin/add_restaurant.html')

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Formato de imagen no válido.', 'error')
            return render_template('admin/add_restaurant.html')

        restaurant = Restaurant(
            name=name,
            address=address,
            phone=phone,
            description=description,
            image_filename=filename,
            created_by=current_user.id
        )
        db.session.add(restaurant)
        db.session.commit()
        flash('Restaurante registrado con éxito.', 'success')
        return redirect(url_for('restaurant.list_restaurants'))

    return render_template('admin/add_restaurant.html')

@restaurant_bp.route('/restaurants')
@login_required
def list_restaurants():
    if current_user.role != 'admin':
        flash('No tienes permiso.', 'error')
        return redirect(url_for('auth.login'))
    restaurants = Restaurant.query.all()
    return render_template('admin/restaurants_list.html', restaurants=restaurants)

@restaurant_bp.route('/customer/restaurants')
@login_required
def view_restaurants():
    if current_user.role != 'customer':
        flash('Esta sección es solo para clientes.', 'error')
        return redirect(url_for('auth.login'))

    restaurants = Restaurant.query.all()
    return render_template('customer/restaurants_list.html', restaurants=restaurants)

@restaurant_bp.route('/admin/restaurants/<int:restaurant_id>/add-dish', methods=['GET', 'POST'])
@login_required
def add_dish(restaurant_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    restaurant = Restaurant.query.get_or_404(restaurant_id)

    if request.method == 'POST':
        name = request.form.get('name')
        ingredients = request.form.get('ingredients')
        description = request.form.get('description')
        price = request.form.get('price')
        image = request.files.get('image')

        if not name or not price or not ingredients:
            flash('Nombre, ingredientes y precio son obligatorios.', 'error')
            return render_template('admin/add_dish.html', restaurant=restaurant)

        filename = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        new_dish = Dish(
            name=name,
            ingredients=ingredients,
            description=description,
            price=price,
            image_filename=filename,
            restaurant_id=restaurant.id
        )
        db.session.add(new_dish)
        db.session.commit()
        flash('Plato agregado exitosamente.', 'success')
        return redirect(url_for('restaurant.view_dishes', restaurant_id=restaurant.id))

    return render_template('admin/add_dish.html', restaurant=restaurant)

@restaurant_bp.route('/restaurants/<int:restaurant_id>/dishes')
@login_required
def view_dishes(restaurant_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    restaurant = Restaurant.query.get_or_404(restaurant_id)
    return render_template('admin/restaurant_dishes.html', restaurant=restaurant, dishes=restaurant.dishes)

@restaurant_bp.route('/dishes/<int:dish_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_dish(dish_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    dish = Dish.query.get_or_404(dish_id)
    restaurant = Restaurant.query.get(dish.restaurant_id)  # Obtener el restaurante asociado

    if request.method == 'POST':
        dish.name = request.form.get('name')
        dish.ingredients = request.form.get('ingredients')
        dish.description = request.form.get('description')
        dish.price = request.form.get('price')

        image = request.files.get('image')
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            dish.image_filename = filename

        db.session.commit()
        flash('Plato actualizado con éxito.', 'success')
        return redirect(url_for('restaurant.view_dishes', restaurant_id=dish.restaurant_id))

    return render_template('admin/edit_dish.html', dish=dish, restaurant=restaurant)

@restaurant_bp.route('/dishes/<int:dish_id>/delete', methods=['POST'])
@login_required
def delete_dish(dish_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    dish = Dish.query.get_or_404(dish_id)
    restaurant_id = dish.restaurant_id
    db.session.delete(dish)
    db.session.commit()
    flash('Plato eliminado.', 'success')
    return redirect(url_for('restaurant.view_dishes', restaurant_id=restaurant_id))

@restaurant_bp.route('/restaurants/manage')
@login_required
def list_restaurants_admin():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    
    restaurants = Restaurant.query.all()
    return render_template('admin/restaurant_listes.html', restaurants=restaurants)


@restaurant_bp.route('/restaurants/<int:restaurant_id>/delete', methods=['POST'])
@login_required
def delete_restaurant(restaurant_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    restaurant = Restaurant.query.get_or_404(restaurant_id)

    try:
        db.session.delete(restaurant)
        db.session.commit()
        flash('Restaurante eliminado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'error')

    return redirect(url_for('restaurant.list_restaurants_admin'))


@restaurant_bp.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_restaurant(restaurant_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    restaurant = Restaurant.query.get_or_404(restaurant_id)

    if request.method == 'POST':
        restaurant.name = request.form.get('name')
        restaurant.address = request.form.get('address')
        restaurant.phone = request.form.get('phone')
        restaurant.description = request.form.get('description')

        image = request.files.get('image')
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            restaurant.image_filename = filename

        db.session.commit()
        flash('Restaurante actualizado con éxito.', 'success')
        return redirect(url_for('restaurant.list_restaurants_admin'))

    return render_template('admin/edit_restaurant.html', restaurant=restaurant)
