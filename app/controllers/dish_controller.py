from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

from app.models.db import Restaurant
from app.services.dish_service import DishService
from app.dtos.dish_dto import DishDTO
from app.services.restaurant_visit_service import RestaurantVisitService


dish_bp = Blueprint('dish', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@dish_bp.route('/admin/restaurants/<int:restaurant_id>/add-dish', methods=['GET', 'POST'])
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

        dto = DishDTO(
            id=None,
            name=name,
            ingredients=ingredients,
            description=description,
            price=price,
            image_filename=filename,
            restaurant_id=restaurant.id
        )

        if DishService.create(dto):
            flash('Plato agregado exitosamente.', 'success')
            return redirect(url_for('dish.view_dishes', restaurant_id=restaurant.id))
        else:
            flash('Error al agregar el plato.', 'error')

    return render_template('admin/add_dish.html', restaurant=restaurant)


@dish_bp.route('/restaurants/<int:restaurant_id>/dishes')
@login_required
def view_dishes(restaurant_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    restaurant = Restaurant.query.get_or_404(restaurant_id)
    dishes = DishService.get_by_restaurant(restaurant)
    return render_template('admin/restaurant_dishes.html', restaurant=restaurant, dishes=dishes)


@dish_bp.route('/dishes/<int:dish_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_dish(dish_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    dto = DishService.get_by_id(dish_id)
    if not dto:
        flash('Plato no encontrado.', 'error')
        return redirect(url_for('restaurant.list_restaurants'))

    restaurant = Restaurant.query.get(dto.restaurant_id)

    if request.method == 'POST':
        name = request.form.get('name')
        ingredients = request.form.get('ingredients')
        description = request.form.get('description')
        price = request.form.get('price')
        image = request.files.get('image')

        image_filename = dto.image_filename
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            image_filename = filename

        updated_dto = DishDTO(
            id=dish_id,
            name=name,
            ingredients=ingredients,
            description=description,
            price=price,
            image_filename=image_filename,
            restaurant_id=dto.restaurant_id
        )

        DishService.update(dish_id, updated_dto)
        flash('Plato actualizado con éxito.', 'success')
        return redirect(url_for('dish.view_dishes', restaurant_id=dto.restaurant_id))

    return render_template('admin/edit_dish.html', dish=dto, restaurant=restaurant)


@dish_bp.route('/dishes/<int:dish_id>/delete', methods=['POST'])
@login_required
def delete_dish(dish_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    dto = DishService.get_by_id(dish_id)
    if not dto:
        flash('Plato no encontrado.', 'error')
        return redirect(url_for('restaurant.list_restaurants'))

    if DishService.delete(dish_id):
        flash('Plato eliminado.', 'success')
    else:
        flash('Error al eliminar el plato.', 'error')

    return redirect(url_for('dish.view_dishes', restaurant_id=dto.restaurant_id))

@dish_bp.route('/customer/restaurants/<int:restaurant_id>/dishes')
@login_required
def view_dishes_by_restaurant(restaurant_id):
    if current_user.role != 'customer':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('auth.login'))

    restaurant = Restaurant.query.get_or_404(restaurant_id)
    dishes = DishService.get_by_restaurant(restaurant)

    # Registrar visita del cliente al restaurante
    from app.services.restaurant_visit_service import RestaurantVisitService
    RestaurantVisitService.register_visit(current_user.id, restaurant.id)

    return render_template('customer/restaurant_dishes.html', restaurant=restaurant, dishes=dishes)
