from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Import db from product module to avoid circular imports
from models.product import db

class Category(db.Model):
    """Category model."""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    description_ar = db.Column(db.Text)
    description_en = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    products = db.relationship('Product', back_populates='category')

    def __repr__(self):
        return f'<Category {self.name_en}>'

    def to_dict(self):
        """Convert category to dictionary."""
        return {
            'id': self.id,
            'name_ar': self.name_ar,
            'name_en': self.name_en,
            'description_ar': self.description_ar,
            'description_en': self.description_en,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }