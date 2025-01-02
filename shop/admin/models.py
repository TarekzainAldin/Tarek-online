from shop import  db

class User(db.Model):
   id = db.Column(db.Integer, Primary_Key=True)
   name=db.Column(db.stering(30), unique=False,nullable=False)
   username=db.Column(db.string(80),unique=False,nullable=False)
   email=db.Column(db.string(120),unique=True,nullable=False)
   password=db.Column(db.string(150),unique=False,nullable=False)
   default='profail.jpg'

   def __repet__(self):
    return '<User %r>' % self.User.username
   

   db.create_all()