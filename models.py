from database import db
from datetime import datetime

# First, define the association table
trail_feature = db.Table(
    'Trail_Feature',
    db.Column('TrailID', db.Integer, db.ForeignKey('CW2.Trail.TrailID'), primary_key=True),
    db.Column('FeatureID', db.Integer, db.ForeignKey('CW2.Feature.FeatureID'), primary_key=True),
    schema='CW2'
)

class User(db.Model):
    __tablename__ = 'USER'
    __table_args__ = {'schema': 'CW2'}
    
    OwnerUserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(100), nullable=False)
    
    # Relationships
    trails = db.relationship('Trail', backref='owner', lazy=True)

class Trail(db.Model):
    __tablename__ = 'Trail'
    __table_args__ = {'schema': 'CW2'}
    
    TrailID = db.Column(db.Integer, primary_key=True)
    TrailName = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.String(500))
    Difficulty = db.Column(db.String(20), nullable=False)
    Length = db.Column(db.Numeric(5, 2), nullable=False)
    ElevationGain = db.Column(db.Integer, nullable=False)
    OwnerUserID = db.Column(db.Integer, db.ForeignKey('CW2.USER.OwnerUserID'), nullable=False)
    
    # Relationships - use the trail_feature table defined above
    features = db.relationship('Feature', 
                             secondary=trail_feature,
                             backref='trails', 
                             lazy=True)

class Feature(db.Model):
    __tablename__ = 'Feature'
    __table_args__ = {'schema': 'CW2'}
    
    FeatureID = db.Column(db.Integer, primary_key=True)
    FeatureName = db.Column(db.String(50), nullable=False, unique=True)

class TrailAuditLog(db.Model):
    __tablename__ = 'TrailAuditLog'
    __table_args__ = {'schema': 'CW2'}
    
    LogID = db.Column(db.Integer, primary_key=True)
    TrailID = db.Column(db.Integer, nullable=False)
    TrailName = db.Column(db.String(100), nullable=False)
    AddedByUserID = db.Column(db.Integer, nullable=False)
    DateAdded = db.Column(db.DateTime, default=datetime.utcnow)