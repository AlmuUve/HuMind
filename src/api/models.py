from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, Date, Time, Float

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250))
    is_active = db.Column(db.Boolean)
    image = db.Column(db.String(250))
    description = db.Column(db.Text)
    is_psychologist = db.Column(db.Boolean)
    user_company = db.relationship('User_company', cascade="all, delete", lazy=True)
    user_psychologist = db.relationship("User_psychologist", cascade="all, delete", lazy=True)
    
    def __repr__(self):
        return f'User {self.email}'

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "description": self.description,
            "is_psychologist": self.is_psychologist
        }

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        user = cls.query.filter_by(id = id).first()
        return user

    @classmethod
    def delete_user(cls, id):
        target = cls.query.filter_by(id = id).first()
        target.is_active=False        
        db.session.commit()
        return target.is_active

class User_company(db.Model):
    __tablename__ = 'user_company'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(250))
    company_number = db.Column(db.String(80), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    search_workshop = db.relationship('Search_workshop', lazy=True)
 
    def __repr__(self):
        return f'User company {self.company_name}'

    def to_dict(self):
        return {
            "id": self.id,
            "company_name": self.company_name,
            "company_number": self.company_number,
            "user_id": self.user_id,
            "is_psychologist": self.is_psychologist
        }

    def add(self):
        db.session.add()
        db.session.commit()
    
class User_psychologist(db.Model):
    __tablename__ = 'user_psychologist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    lastname = db.Column(db.String(250))
    identity_number = db.Column(db.String(250), unique=True)
    association_number = db.Column(db.String(250), unique=True)
    speciality = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    workshop = db.relationship('Workshop', lazy=True)

 
    def __repr__(self):
        return f'User psychologist {self.name}'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "association_number": self.association_number,
            "speciality": self.speciality,
            "user_id": self.user_id
        }

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_user_id(cls, user):
        user_psychologit = cls.query.filter_by(user_id=user)
        return user_psychologit

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(250), unique=True)
    search_workshop = db.relationship('Search_workshop', lazy=True)
    is_active = db.Column(db.Boolean)
     
    def __repr__(self):
        return f'Category {self.category_name}'

    def to_dict(self):
        return {
            "id": self.id,
            "category_name": self.category_name,
            "is_active":False
        }

class Search_workshop(db.Model):
    __tablename__ = 'search_workshop'

    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.String(250))
    max_price = db.Column(db.Float)
    date = db.Column(db.Date)
    max_people = db.Column(db.Integer)
    is_active = db.Column(db.Boolean)
    user_company_id = db.Column(db.Integer, db.ForeignKey("user_company.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
 
    def __repr__(self):
        return f'Search_workshop {self.user_company_id} and {self.id}'

    def to_dict(self):
        return {
            "id": self.id,
            "duration": self.duration,
            "max_price": self.max_price,
            "date": self.date,
            "max_people": self.max_people,
            "is_active": True,
            "user_company_id": self.user_company_id,
            "category_id": self.category_id
        }

workshop_has_category = db.Table('workshop_has_category',
    db.Column('workshop_id', db.Integer, db.ForeignKey("workshop.id"), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey("category.id"), primary_key=True),
)

class Workshop(db.Model):
    __tablename__ = 'workshop'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    duration = db.Column(db.String(250))
    price = db.Column(db.Float)
    date = db.Column(db.Date)
    is_active = db.Column(db.Boolean)
    max_people = db.Column(db.Integer)
    description = db.Column(db.Text)
    user_psychologist_id = db.Column(db.Integer, db.ForeignKey("user_psychologist.id"))
    category_info = db.relationship("Category", secondary= workshop_has_category, lazy='subquery',
        backref=db.backref("workshops", lazy=True))
 
    def __repr__(self):
        return f'Workshop {self.title} and owner {self.user_psychologist_id}'

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "duration": self.duration,
            "price": self.price,
            "date": self.date,
            "is_active": True,
            "max_people": self.max_people,
            "description": self.description,
            "user_psychologist_id": self.user_psychologist_id,
            "category_info": self.category_info
        }

