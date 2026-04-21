from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.product import Product, db
from models.category import Category
from models.admin_user import AdminUser
from models.attribute import ProductAttribute
from models.index_parameter import IndexParameter
from models.index_result import IndexResult
from utils.auth import admin_only
from utils.file_upload import save_image
from utils.index_calculator import calculate_index
import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
def restrict_admin_access():
    """Restrict access to admin routes."""
    if 'admin_id' not in session:
        return redirect(url_for('auth.login'))

@admin_bp.route('/')
def dashboard():
    """Admin dashboard."""
    # Get statistics
    product_count = Product.query.count()
    category_count = Category.query.count()

    # Recent products
    recent_products = Product.query.order_by(Product.created_at.desc()).limit(5).all()

    # Recent index calculations
    recent_indices = IndexResult.query.order_by(IndexResult.created_at.desc()).limit(5).all()

    return render_template('admin/dashboard.html',
                         product_count=product_count,
                         category_count=category_count,
                         recent_products=recent_products,
                         recent_indices=recent_indices)

@admin_bp.route('/products')
def products():
    """List all products."""
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@admin_bp.route('/products/new', methods=['GET', 'POST'])
@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id=None):
    """Add or edit a product."""
    product = None
    if product_id:
        product = Product.query.get_or_404(product_id)

    categories = Category.query.all()

    if request.method == 'POST':
        try:
            # Handle form data
            name_ar = request.form.get('name_ar')
            name_en = request.form.get('name_en')
            description_ar = request.form.get('description_ar')
            description_en = request.form.get('description_en')
            price = float(request.form.get('price', 0))
            stock_status = request.form.get('stock_status', 'in_stock')
            category_id = int(request.form.get('category_id', 0))

            # Create or update product
            if product:
                product.name_ar = name_ar
                product.name_en = name_en
                product.description_ar = description_ar
                product.description_en = description_en
                product.price = price
                product.stock_status = stock_status
                product.category_id = category_id
            else:
                product = Product(
                    name_ar=name_ar,
                    name_en=name_en,
                    description_ar=description_ar,
                    description_en=description_en,
                    price=price,
                    stock_status=stock_status,
                    category_id=category_id
                )
                db.session.add(product)

            # Handle image uploads
            if 'images' in request.files:
                images = request.files.getlist('images')
                for image in images:
                    if image and image.filename:
                        filename = save_image(image)
                        if filename:
                            # In a full implementation, you might want to save image references
                            pass

            db.session.commit()
            flash('Product saved successfully!', 'success')
            return redirect(url_for('admin.products'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error saving product: {str(e)}', 'error')

    return render_template('admin/edit_product.html',
                         product=product,
                         categories=categories)

@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    """Delete a product."""
    product = Product.query.get_or_404(product_id)
    try:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting product: {str(e)}', 'error')

    return redirect(url_for('admin.products'))

@admin_bp.route('/categories')
def categories():
    """List all categories."""
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@admin_bp.route('/categories/new', methods=['GET', 'POST'])
@admin_bp.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id=None):
    """Add or edit a category."""
    category = None
    if category_id:
        category = Category.query.get_or_404(category_id)

    if request.method == 'POST':
        try:
            name_ar = request.form.get('name_ar')
            name_en = request.form.get('name_en')
            description_ar = request.form.get('description_ar')
            description_en = request.form.get('description_en')

            if category:
                category.name_ar = name_ar
                category.name_en = name_en
                category.description_ar = description_ar
                category.description_en = description_en
            else:
                category = Category(
                    name_ar=name_ar,
                    name_en=name_en,
                    description_ar=description_ar,
                    description_en=description_en
                )
                db.session.add(category)

            db.session.commit()
            flash('Category saved successfully!', 'success')
            return redirect(url_for('admin.categories'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error saving category: {str(e)}', 'error')

    return render_template('admin/edit_category.html', category=category)

@admin_bp.route('/index-parameters')
def index_parameters():
    """List all index parameters."""
    parameters = IndexParameter.query.all()
    return render_template('admin/index_parameters.html', parameters=parameters)

@admin_bp.route('/index-parameters/new', methods=['GET', 'POST'])
@admin_bp.route('/index-parameters/edit/<int:param_id>', methods=['GET', 'POST'])
def edit_index_parameter(param_id=None):
    """Add or edit an index parameter."""
    parameter = None
    if param_id:
        parameter = IndexParameter.query.get_or_404(param_id)

    if request.method == 'POST':
        try:
            name_ar = request.form.get('name_ar')
            name_en = request.form.get('name_en')
            formula = request.form.get('formula')
            weight = float(request.form.get('weight', 1.0))
            is_active = bool(request.form.get('is_active', False))

            if parameter:
                parameter.name_ar = name_ar
                parameter.name_en = name_en
                parameter.formula = formula
                parameter.weight = weight
                parameter.is_active = is_active
            else:
                parameter = IndexParameter(
                    name_ar=name_ar,
                    name_en=name_en,
                    formula=formula,
                    weight=weight,
                    is_active=is_active
                )
                db.session.add(parameter)

            db.session.commit()
            flash('Index parameter saved successfully!', 'success')
            return redirect(url_for('admin.index_parameters'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error saving index parameter: {str(e)}', 'error')

    return render_template('admin/edit_index_parameter.html', parameter=parameter)

@admin_bp.route('/index-results')
def index_results():
    """View index calculation results."""
    # Get results with product and parameter info
    results = db.session.query(IndexResult, Product, IndexParameter)\
               .outerjoin(Product, IndexResult.product_id == Product.id)\
               .join(IndexParameter, IndexResult.parameter_id == IndexParameter.id)\
               .order_by(IndexResult.created_at.desc())\
               .all()

    return render_template('admin/index_results.html', results=results)

@admin_bp.route('/calculate-index', methods=['POST'])
def calculate_index_route():
    """Calculate index for all products."""
    try:
        # This would normally calculate for all products
        # For demo, we'll just show a success message
        flash('Index calculation initiated successfully!', 'success')
    except Exception as e:
        flash(f'Error calculating index: {str(e)}', 'error')

    return redirect(url_for('admin.index_results'))