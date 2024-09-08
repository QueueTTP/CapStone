from flask_sqlalchemy import SQLAlchemy
from . import db



class UserDefaultSettings(db.Model):
    __tablename__ = 'user_default_settings'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    E1 = db.Column(db.Float)
    E2 = db.Column(db.Float)
    E3 = db.Column(db.Float)
    E4 = db.Column(db.Float)
    E5 = db.Column(db.Float)
    E6 = db.Column(db.Float)
    E7 = db.Column(db.Float)
    E8 = db.Column(db.Float)
    E9 = db.Column(db.Float)
    E10 = db.Column(db.Float)
    E11 = db.Column(db.Float)
    E12 = db.Column(db.Float)
    E13 = db.Column(db.Float)
    E14 = db.Column(db.Float)
    E15 = db.Column(db.Float)
    E16 = db.Column(db.Float)
    E17 = db.Column(db.Float)
    E18 = db.Column(db.Float)
    E19 = db.Column(db.Float)
    E20 = db.Column(db.Float)
    E21 = db.Column(db.Float)
    E22 = db.Column(db.Float)
    E23 = db.Column(db.Float)
    E24 = db.Column(db.Float)
    E25 = db.Column(db.Float)
    E26 = db.Column(db.Float)
    E27 = db.Column(db.Float)
    E28 = db.Column(db.Float)
    E29 = db.Column(db.Float)
    SC1 = db.Column(db.Float)
    SC2 = db.Column(db.Float)
    SC3 = db.Column(db.Float)
    SC4 = db.Column(db.Float)
    SC5 = db.Column(db.Float)
    SD1 = db.Column(db.Float)
    SD2 = db.Column(db.Float)
    SD3 = db.Column(db.Float)
    SD4 = db.Column(db.Float)
    SD5 = db.Column(db.Float)
    T1 = db.Column(db.Float)
    T2 = db.Column(db.Float)
    T3 = db.Column(db.Float)
    T4 = db.Column(db.Float)
    L1 = db.Column(db.Float)
    L2 = db.Column(db.Float)
    L3 = db.Column(db.Float)
    L4 = db.Column(db.Float)
    L5 = db.Column(db.Float)
    L6 = db.Column(db.Float)

class UserDynamicPreferences(db.Model):
    __tablename__ = 'user_dynamic_preferences'

    user_id = db.Column(db.Integer, db.ForeignKey('user_default_settings.user_id'), primary_key=True)
    current_favorite = db.Column(db.String(50), nullable=False)
    E1 = db.Column(db.Float)
    E2 = db.Column(db.Float)
    E3 = db.Column(db.Float)
    E4 = db.Column(db.Float)
    E5 = db.Column(db.Float)
    E6 = db.Column(db.Float)
    E7 = db.Column(db.Float)
    E8 = db.Column(db.Float)
    E9 = db.Column(db.Float)
    E10 = db.Column(db.Float)
    E11 = db.Column(db.Float)
    E12 = db.Column(db.Float)
    E13 = db.Column(db.Float)
    E14 = db.Column(db.Float)
    E15 = db.Column(db.Float)
    E16 = db.Column(db.Float)
    E17 = db.Column(db.Float)
    E18 = db.Column(db.Float)
    E19 = db.Column(db.Float)
    E20 = db.Column(db.Float)
    E21 = db.Column(db.Float)
    E22 = db.Column(db.Float)
    E23 = db.Column(db.Float)
    E24 = db.Column(db.Float)
    E25 = db.Column(db.Float)
    E26 = db.Column(db.Float)
    E27 = db.Column(db.Float)
    E28 = db.Column(db.Float)
    E29 = db.Column(db.Float)
    SC1 = db.Column(db.Float)
    SC2 = db.Column(db.Float)
    SC3 = db.Column(db.Float)
    SC4 = db.Column(db.Float)
    SC5 = db.Column(db.Float)
    SD1 = db.Column(db.Float)
    SD2 = db.Column(db.Float)
    SD3 = db.Column(db.Float)
    SD4 = db.Column(db.Float)
    SD5 = db.Column(db.Float)
    T1 = db.Column(db.Float)
    T2 = db.Column(db.Float)
    T3 = db.Column(db.Float)
    T4 = db.Column(db.Float)
    L1 = db.Column(db.Float)
    L2 = db.Column(db.Float)
    L3 = db.Column(db.Float)
    L4 = db.Column(db.Float)
    L5 = db.Column(db.Float)
    L6 = db.Column(db.Float)

    user_default = db.relationship('UserDefaultSettings', backref=db.backref('dynamic_preferences', lazy=True))
    
    
