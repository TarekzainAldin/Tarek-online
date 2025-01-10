from flask_wtf.file import FileAllowed, FileField, FileRequest,FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators

class Addproducts(Form):
    name =StringField('Name',[validators.DateRequired()])
    price=IntegerField('price',[validators.data_required()])
    discount=IntegerField('Discount',default=0)
    stock=IntegerField('Stock',[validators.data_required()])
    discription=TextAreaField('Discription',validators.data_required())
    color=TextAreaField('Colors',[validators.data_required()])

    image_1=FileField('image1',validators=[FileRequired(),FileAllowed(['jpg','png','gif','jpeg']),'images only please '])
    image_2=FileField('image1',validators=[FileRequired(),FileAllowed(['jpg','png','gif','jpeg']),'images only please '])
    image_3=FileField('image1',validators=[FileRequired(),FileAllowed(['jpg','png','gif','jpeg']),'images only please '])