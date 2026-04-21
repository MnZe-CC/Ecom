from flask import Blueprint, render_template, request, session
from models.product import Product, db
from models.category import Category

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
@public_bp.route('/<lang>/')
def home(lang='en'):
    """
    Home page showing all products.
    """
    # Get all products
    products = Product.query.all()

    # Get language preference
    language = lang if lang in ['ar', 'en'] else 'en'
    session['language'] = language

    return render_template(f'{language}/home.html',
                         products=products,
                         language=language,
                         dir='rtl' if language == 'ar' else 'ltr')

@public_bp.route('/<lang>/product/<int:product_id>')
@public_bp.route('/product/<int:product_id>')
def product_detail(product_id, lang=None):
    """
    Product detail page.
    """
    # Get language preference
    if lang is None:
        language = session.get('language', 'en')
    else:
        language = lang if lang in ['ar', 'en'] else 'en'
        session['language'] = language

    # Get product by ID
    product = Product.query.get_or_404(product_id)

    # Get product attributes
    attributes = product.attributes

    return render_template(f'{language}/product.html',
                         product=product,
                         attributes=attributes,
                         language=language,
                         dir='rtl' if language == 'ar' else 'ltr')

@public_bp.route('/switch-language/<lang>')
def switch_language(lang):
    """
    Switch between languages.
    """
    if lang in ['ar', 'en']:
        session['language'] = lang

    # Redirect to referrer or home
    referrer = request.referrer
    if referrer:
        return redirect(referrer)
    else:
        return redirect(url_for('public.home', lang=lang))