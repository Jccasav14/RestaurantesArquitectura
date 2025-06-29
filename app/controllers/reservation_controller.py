from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.reservation_service import ReservationService
from app.services.restaurant_service import RestaurantService
from app.services.table_service import TableService
from app.services.dish_service import DishService
from app.services.user_service import UserService
from app.dtos.reservation_dto import ReservationDTO
from datetime import datetime

#Blueprint para todas las rutas relacionadas con reservas
reservation_bp = Blueprint('reservation', __name__, url_prefix='/reservations')

#Muestra todas las reservas (solo admin)
@reservation_bp.route('/')
@login_required
def list_reservations():
    if current_user.role != 'admin':
        flash('Acceso restringido a administradores.', 'error')
        return redirect(url_for('auth.login'))
    
    reservations = ReservationService.get_all()  # Aquí deberías implementar este método para traer todas las reservaciones
    return render_template('admin/list_reservations.html', reservations=reservations)

#Permite a un admin crear una nueva reserva
@reservation_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create_reservation():
    if current_user.role != 'admin':
        flash('Acceso restringido a administradores.', 'error')
        return redirect(url_for('auth.login'))

    restaurants = RestaurantService.get_all()
    customers = UserService.get_all_customers()
    selected_restaurant_id = request.form.get('restaurant_id', type=int)
    tables = []
    dishes = []

    # Si ya eligieron restaurante, cargamos mesas y platos de ese restaurante
    if selected_restaurant_id:
        tables = TableService.get_by_restaurant_id(selected_restaurant_id)
        dishes = DishService.get_by_restaurant_id(selected_restaurant_id)

    if request.method == 'POST':
        # Validamos si el formulario es submit final o solo cambio de restaurante
        # Para eso verificamos si todos los campos obligatorios están en request.form

        # Campos obligatorios
        required_fields = ['restaurant_id', 'table_id', 'customer_id', 'reservation_date', 'reservation_time']

        # ¿Están todos los campos obligatorios presentes y no vacíos?
        form_filled = all(request.form.get(field) for field in required_fields)

        if not form_filled:
            # Si NO están llenos pero el usuario solo cambió el restaurante (porque ya cargamos mesas/platos)
            # No mostramos error todavía, solo renderizamos para que siga llenando
            if selected_restaurant_id:
                return render_template(
                    'admin/add_reservation.html',
                    restaurants=restaurants,
                    customers=customers,
                    tables=tables,
                    dishes=dishes,
                    selected_restaurant_id=selected_restaurant_id
                )
            else:
                flash('Todos los campos obligatorios deben estar llenos.', 'error')
                return render_template(
                    'admin/add_reservation.html',
                    restaurants=restaurants,
                    customers=customers
                )

        # Si está todo completo, procesamos para crear la reservación
        restaurant_id = request.form.get('restaurant_id', type=int)
        table_id = request.form.get('table_id', type=int)
        customer_id = request.form.get('customer_id', type=int)
        reservation_date = request.form.get('reservation_date')
        reservation_time = request.form.get('reservation_time')
        special_requests = request.form.get('special_requests')
        menu = request.form.get('menu')

        dto = ReservationDTO(
            id=None,
            restaurant_id=restaurant_id,
            customer_id=customer_id,
            table_id=table_id,
            reservation_date=reservation_date,
            reservation_time=reservation_time,
            special_requests=special_requests,
            menu=menu
        )

        success = ReservationService.create(dto)
        if success:
            flash('Reservación creada exitosamente', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Error al crear reservación', 'error')

    return render_template(
        'admin/add_reservation.html',
        restaurants=restaurants,
        customers=customers,
        tables=tables,
        dishes=dishes,
        selected_restaurant_id=selected_restaurant_id
    )

#Permite a un cliente crear su propia reserva
@reservation_bp.route('/new-client', methods=['GET', 'POST'])
@login_required
def create_reservation_client():
    if current_user.role != 'customer':
        flash('Acceso restringido a clientes.', 'error')
        return redirect(url_for('auth.login'))

    restaurants = RestaurantService.get_all()
    selected_restaurant_id = request.form.get('restaurant_id', type=int)
    tables = []
    dishes = []

    if selected_restaurant_id:
        tables = TableService.get_by_restaurant_id(selected_restaurant_id)
        dishes = DishService.get_by_restaurant_id(selected_restaurant_id)

    if request.method == 'POST':
        required_fields = ['restaurant_id', 'table_id', 'reservation_date', 'reservation_time']
        form_filled = all(request.form.get(field) for field in required_fields)

        if not form_filled:
            if selected_restaurant_id:
                return render_template(
                    'customer/add_reservation.html',
                    restaurants=restaurants,
                    tables=tables,
                    dishes=dishes,
                    selected_restaurant_id=selected_restaurant_id
                )
            else:
                flash('Todos los campos obligatorios deben estar llenos.', 'error')
                return render_template('customer/add_reservation.html', restaurants=restaurants)

        restaurant_id = request.form.get('restaurant_id', type=int)
        table_id = request.form.get('table_id', type=int)
        reservation_date = request.form.get('reservation_date')
        reservation_time = request.form.get('reservation_time')
        special_requests = request.form.get('special_requests')
        menu = request.form.get('menu')

        dto = ReservationDTO(
            id=None,
            restaurant_id=restaurant_id,
            customer_id=current_user.id,  # cliente fijo
            table_id=table_id,
            reservation_date=reservation_date,
            reservation_time=reservation_time,
            special_requests=special_requests,
            menu=menu
        )

        success = ReservationService.create(dto)
        if success:
            flash('Reservación creada exitosamente.', 'success')
            return redirect(url_for('customer.frequent_restaurants'))  # asumiendo tienes dashboard cliente
        else:
            flash('Error al crear reservación.', 'error')

    return render_template(
        'customer/add_reservation.html',
        restaurants=restaurants,
        tables=tables,
        dishes=dishes,
        selected_restaurant_id=selected_restaurant_id
    )

#Muestra todas las reservas hechas por el cliente actual
@reservation_bp.route('/my_reservations')
@login_required
def my_reservations():
    if current_user.role != 'customer':
        flash('Acceso restringido a clientes.', 'error')
        return redirect(url_for('auth.login'))
    
    # Traer todas las reservaciones del usuario actual
    reservations = ReservationService.get_by_customer_id(current_user.id)
    return render_template('customer/my_reservations.html', reservations=reservations)

