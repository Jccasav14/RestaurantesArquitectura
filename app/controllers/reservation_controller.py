from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.reservation_service import ReservationService
from app.services.restaurant_service import RestaurantService
from app.services.table_service import TableService
from app.services.dish_service import DishService
from app.services.user_service import UserService
from app.dtos.reservation_dto import ReservationDTO
from datetime import datetime, time

# Blueprint para todas las rutas relacionadas con reservas
reservation_bp = Blueprint('reservation', __name__, url_prefix='/reservations')

# Muestra todas las reservas (solo admin)
@reservation_bp.route('/')
@login_required
def list_reservations():
    if current_user.role != 'admin':
        flash('Acceso restringido a administradores.', 'error')
        return redirect(url_for('auth.login'))

    reservations = ReservationService.get_all()
    return render_template('admin/list_reservations.html', reservations=reservations)

# Permite a un admin crear una nueva reserva
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

    if selected_restaurant_id:
        tables = TableService.get_by_restaurant_id(selected_restaurant_id)
        dishes = DishService.get_by_restaurant_id(selected_restaurant_id)

    if request.method == 'POST':
        required_fields = ['restaurant_id', 'table_id', 'customer_id', 'reservation_date', 'reservation_time']
        form_filled = all(request.form.get(field) for field in required_fields)

        if not form_filled:
            if selected_restaurant_id:
                return render_template(
                    'admin/add_reservation.html',
                    restaurants=restaurants,
                    customers=customers,
                    tables=tables,
                    dishes=dishes,
                    selected_restaurant_id=selected_restaurant_id,
                    datetime=datetime
                )
            else:
                flash('Todos los campos obligatorios deben estar llenos.', 'error')
                return render_template(
                    'admin/add_reservation.html',
                    restaurants=restaurants,
                    customers=customers,
                    datetime=datetime
                )

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
        selected_restaurant_id=selected_restaurant_id,
        datetime=datetime
    )

# Permite a un cliente crear su propia reserva
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
                    selected_restaurant_id=selected_restaurant_id,
                    datetime=datetime
                )
            else:
                flash('Todos los campos obligatorios deben estar llenos.', 'error')
                return render_template(
                    'customer/add_reservation.html',
                    restaurants=restaurants,
                    datetime=datetime
                )

        restaurant_id = request.form.get('restaurant_id', type=int)
        table_id = request.form.get('table_id', type=int)
        reservation_date = request.form.get('reservation_date')
        reservation_time = request.form.get('reservation_time')
        special_requests = request.form.get('special_requests')
        menu = request.form.get('menu')

        try:
            selected_datetime = datetime.strptime(f"{reservation_date} {reservation_time}", "%Y-%m-%d %H:%M")
            now = datetime.now()

            if selected_datetime.date() < now.date():
                flash('La fecha de la reservación no puede ser anterior a hoy.', 'error')
                raise ValueError("Fecha inválida")

            hora = selected_datetime.time()
            if not (time(10, 0) <= hora <= time(22, 0)):
                flash('La hora debe estar entre las 10:00 y las 22:00.', 'error')
                raise ValueError("Hora fuera de rango")

        except ValueError:
            return render_template(
                'customer/add_reservation.html',
                restaurants=restaurants,
                tables=tables,
                dishes=dishes,
                selected_restaurant_id=selected_restaurant_id,
                datetime=datetime
            )

        dto = ReservationDTO(
            id=None,
            restaurant_id=restaurant_id,
            customer_id=current_user.id,
            table_id=table_id,
            reservation_date=reservation_date,
            reservation_time=reservation_time,
            special_requests=special_requests,
            menu=menu
        )

        success = ReservationService.create(dto)
        if success:
            flash('Reservación creada exitosamente.', 'success')
            return redirect(url_for('customer.frequent_restaurants'))
        else:
            flash('Error al crear reservación.', 'error')

    return render_template(
        'customer/add_reservation.html',
        restaurants=restaurants,
        tables=tables,
        dishes=dishes,
        selected_restaurant_id=selected_restaurant_id,
        datetime=datetime
    )

# Muestra todas las reservas hechas por el cliente actual
@reservation_bp.route('/my_reservations')
@login_required
def my_reservations():
    if current_user.role != 'customer':
        flash('Acceso restringido a clientes.', 'error')
        return redirect(url_for('auth.login'))

    reservations = ReservationService.get_by_customer_id(current_user.id)
    return render_template('customer/my_reservations.html', reservations=reservations)


# Permite eliminar una reservación (solo admin por ahora)
@reservation_bp.route('/delete/<int:reservation_id>', methods=['POST'])
@login_required
def delete_reservation(reservation_id):
    # Solo los administradores pueden eliminar desde esta ruta
    if current_user.role != 'admin':
        flash('Acceso restringido a administradores.', 'error')
        return redirect(url_for('auth.login'))

    success = ReservationService.delete(reservation_id)
    if success:
        flash('Reservación eliminada exitosamente.', 'success')
    else:
        flash('No se pudo eliminar la reservación (puede que no exista).', 'error')

    return redirect(url_for('reservation.list_reservations'))
