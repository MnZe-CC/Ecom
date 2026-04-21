from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Import db from product module to avoid circular imports
from models.product import db

class ProductAttribute(db.Model):
    """Product attribute model."""
    __tablename__ = 'product_attributes'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    name_ar = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    value_ar = db.Column(db.String(200), nullable=False)
    value_en = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    product = db.relationship('Product', back_populates='attributes')

    def __repr__(self):
        return f'<ProductAttribute {self.name_en}: {self.value_en}>'

    def to_dict(self):
        """Convert attribute to dictionary."""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'name_ar': self.name_ar,
            'name_en': self.name_en,
            'value_ar': self.value_ar,
            'value_en': self.value_en,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }