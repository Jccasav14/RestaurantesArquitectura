from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services.user_service import UserService
from app.dtos.user_dto import UserDTO
from app.models.db import User




admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    return render_template('admin/dashboard.html', user=current_user)


@admin_bp.route('/usuarios')
@login_required
def list_users():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    
    users = UserService.get_all_customers()
    return render_template('admin/user_list.html', users=users)

@admin_bp.route('/usuarios/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        # Como no viene 'role' en el form (porque solo admin puede cambiarlo)
        # entonces mantenemos el valor actual del usuario:
        role = user.role

        # Si quieres que admin pueda cambiar el rol, podrías hacer:
        # role = request.form.get('role') or user.role

        dto = UserDTO(
            id=user.id,
            username=request.form.get('username'),
            email=request.form.get('email'),
            role=role,  # siempre debe tener un valor no nulo
        )

        success = UserService.update(user.id, dto)
        if success:
            flash('Usuario actualizado con éxito.', 'success')
            return redirect(url_for('admin.list_users'))
        else:
            flash('No se pudo actualizar el usuario.', 'error')

    return render_template('admin/edit_user.html', user=user)




@admin_bp.route('/usuarios/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    success = UserService.delete(user_id)
    if success:
        flash('Usuario eliminado con éxito.', 'success')
    else:
        flash('No se pudo eliminar el usuario.', 'error')

    return redirect(url_for('admin.list_users'))