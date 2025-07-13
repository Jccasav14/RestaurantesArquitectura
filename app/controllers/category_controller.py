from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.dtos.category_dto import CategoryDTO
from app.services.category_service import CategoryService

category_bp = Blueprint('category', __name__, url_prefix='/admin/categories')

@category_bp.route('/')
@login_required
def list_categories():
    if current_user.role != 'admin':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('auth.login'))

    categories = CategoryService.get_all()
    return render_template('admin/category_list.html', categories=categories)

@category_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_category():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        name = request.form.get('name')
        dto = CategoryDTO(name=name)
        if CategoryService.create(dto):
            flash('Categoría agregada con éxito.', 'success')
            return redirect(url_for('category.list_categories'))
        flash('Error al agregar categoría.', 'error')
    
    return render_template('admin/category_add.html')

@category_bp.route('/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    dto = CategoryService.get_by_id(category_id)
    if not dto:
        flash('Categoría no encontrada.', 'error')
        return redirect(url_for('category.list_categories'))

    if request.method == 'POST':
        dto.name = request.form.get('name')
        if CategoryService.update(category_id, dto):
            flash('Categoría actualizada.', 'success')
            return redirect(url_for('category.list_categories'))
        flash('Error al actualizar.', 'error')

    return render_template('admin/category_edit.html', category=dto)

@category_bp.route('/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    if CategoryService.delete(category_id):
        flash('Categoría eliminada.', 'success')
    else:
        flash('Error al eliminar.', 'error')

    return redirect(url_for('category.list_categories'))
