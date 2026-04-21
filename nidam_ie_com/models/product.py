from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    """Product model."""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(200), nullable=False)
    name_en = db.Column(db.String(200), nullable=False)
    description_ar = db.Column(db.Text)
    description_en = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock_status = db.Column(db.String(50), default='in_stock')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    category = db.relationship('Category', back_populates='products')
    attributes = db.relationship('ProductAttribute', back_populates='product', cascade='all, delete-orphan')
    index_results = db.relationship('IndexResult', back_populates='product', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Product {self.name_en}>'

    def to_dict(self):
        """Convert product to dictionary."""
        return {
            'id': self.id,
            'name_ar': self.name_ar,
            'name_en': self.name_en,
            'description_ar': self.description_ar,
            'description_en': self.description_en,
            'price': self.price,
            'stock_status': self.stock_status,
            'category_id': self.category_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }