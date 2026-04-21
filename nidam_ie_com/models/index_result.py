from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Import db from product module to avoid circular imports
from models.product import db

class IndexResult(db.Model):
    """Index result model for storing calculated Ecommerce Development Index results."""
    __tablename__ = 'ecommerce_index_results'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)  # NULL for global index
    parameter_id = db.Column(db.Integer, db.ForeignKey('ecommerce_index_parameters.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)  # Raw value for this parameter
    calculated_score = db.Column(db.Float, nullable=False)  # Weighted score
    date = db.Column(db.Date, default=datetime.utcnow().date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    product = db.relationship('Product', back_populates='index_results')
    parameter = db.relationship('IndexParameter', back_populates='index_results')

    def __repr__(self):
        return f'<IndexResult Product:{self.product_id} Parameter:{self.parameter_id} Score:{self.calculated_score}>'

    def to_dict(self):
        """Convert index result to dictionary."""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'parameter_id': self.parameter_id,
            'value': self.value,
            'calculated_score': self.calculated_score,
            'date': self.date.isoformat() if self.date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }