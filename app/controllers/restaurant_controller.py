from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.db import Restaurant
from app.services.restaurant_service import RestaurantService
from app.dtos.restaurant_dto import RestaurantDTO
from app.factories.restaurant_factory import RestaurantFactory
from flask import current_app
from werkzeug.utils import secure_filename
import os
from app.models.db import Dish


#Crea un Blueprint para la gestión de restaurantes
restaurant_bp = Blueprint('restaurant', __name__)

#Verifica si la extensión del archivo es permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

#Permite a un admin agregar un nuevo restaurante
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

        # Crear DTO y usar factory
        dto = RestaurantDTO(
            id=None,
            name=name,
            address=address,
            phone=phone,
            description=description,
            image_filename=filename
        )

        # Usar servicio para guardar
        success = RestaurantService.create(dto, created_by=current_user.id)

        if success:
            flash('Restaurante registrado con éxito.', 'success')
            return redirect(url_for('restaurant.list_restaurants_admin'))
        else:
            flash('Hubo un error al registrar el restaurante.', 'error')

    return render_template('admin/add_restaurant.html')

#Lista de restaurantes solo para admins
@restaurant_bp.route('/restaurants')
@login_required
def list_restaurants():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    restaurants = RestaurantService.get_all()  # ← usa el service que devuelve DTOs
    return render_template('admin/restaurants_list.html', restaurants=restaurants)

#Lista de restaurantes vista por los clientes
@restaurant_bp.route('/customer/restaurants')
@login_required
def view_restaurants():
    if current_user.role != 'customer':
        flash('Esta sección es solo para clientes.', 'error')
        return redirect(url_for('auth.login'))

    restaurants = RestaurantService.get_all()  # ← también usa el mismo service
    return render_template('customer/restaurants_list.html', restaurants=restaurants)

#Muestra listado de restaurantes para admins (gestión)
@restaurant_bp.route('/restaurants/manage')
@login_required
def list_restaurants_admin():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    restaurants = RestaurantService.get_all()
    return render_template('admin/restaurant_listes.html', restaurants=restaurants)

#Permite a un admin eliminar un restaurante
@restaurant_bp.route('/restaurants/<int:restaurant_id>/delete', methods=['POST'])
@login_required
def delete_restaurant(restaurant_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    if RestaurantService.delete(restaurant_id):
        flash('Restaurante eliminado exitosamente.', 'success')
    else:
        flash('No se pudo eliminar el restaurante.', 'error')

    return redirect(url_for('restaurant.list_restaurants_admin'))

#Permite editar un restaurante
@restaurant_bp.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_restaurant(restaurant_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    restaurant = Restaurant.query.get_or_404(restaurant_id)

    #Actualiza los datos del restaurant
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        description = request.form.get('description')

        dto = RestaurantDTO(
            id=restaurant_id,
            name=name,
            address=address,
            phone=phone,
            description=description,
            image_filename=restaurant.image_filename
        )

        success = RestaurantService.update(restaurant_id, dto)

        if success:
            flash('Restaurante actualizado exitosamente.', 'success')
        else:
            flash('Error al actualizar restaurante.', 'error')

        return redirect(url_for('restaurant.list_restaurants_admin'))


    return render_template('admin/edit_restaurant.html', restaurant=restaurant)

#Muestra todos los restaurantes para seleccionar y luego ver sus mesas
@restaurant_bp.route('/restaurants/tables')
@login_required
def list_restaurants_tables():
    if current_user.role != 'admin':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('auth.login'))

    restaurants = RestaurantService.get_all()  # o como se llame tu método
    return render_template('admin/list_restaurants_tables.html', restaurants=restaurants)

