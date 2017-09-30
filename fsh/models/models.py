from . import db


# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False, unique=True)
#
#     products = db.relationship('Product', back_populates='category')


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(240))
    weight = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(80))

    taken = db.Column(db.Boolean, default=False)

    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # category = db.relationship('Category', back_populates='products')
