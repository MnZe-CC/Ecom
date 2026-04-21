from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Import db from product module to avoid circular imports
from models.product import db

class IndexParameter(db.Model):
    """Index parameter model for Ecommerce Development Index."""
    __tablename__ = 'ecommerce_index_parameters'

    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    formula = db.Column(db.Text, nullable=False)  # Formula to calculate this parameter
    weight = db.Column(db.Float, default=1.0)  # Weight factor for this parameter
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    index_results = db.relationship('IndexResult', back_populates='parameter', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<IndexParameter {self.name_en}>'

    def to_dict(self):
        """Convert index parameter to dictionary."""
        return {
            'id': self.id,
            'name_ar': self.name_ar,
            'name_en': self.name_en,
            'formula': self.formula,
            'weight': self.weight,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }