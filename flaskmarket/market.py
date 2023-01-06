from flask import Flask, render_template, flash, url_for, redirect, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column
from forms import RegistrationForm
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=30), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    def __repr__(self):
        return {self.username}

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'

app.config['SECRET_KEY'] = '382fb94ef01b76641762deeda78cf5cb'

@app.route('/')
def home_page():

    return render_template('home.html')

@app.route('/about')
def about():

    items = Item.query.all()
    return render_template('home.html', items=items)

@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                            email_address = form.email_address.data,
                            password_hash = form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('home_page'))
    
    if form.errors!= {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating the user: {err_msg}')

    return render_template('register.html', form=form)


