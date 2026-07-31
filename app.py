# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-this-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Hotel(db.Model):
    __tablename__ = 'hotel'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    rooms_available = db.Column(db.Integer, nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Hotel {self.name}>'


# CREATE + READ (list all hotels)
@app.route('/')
def index():
    hotels = Hotel.query.all()
    return render_template('index.html', hotels=hotels)


@app.route('/add', methods=['POST'])
def add_hotel():
    name = request.form.get('name')
    location = request.form.get('location')
    rooms_available = request.form.get('rooms_available')
    price_per_night = request.form.get('price_per_night')
    rating = request.form.get('rating')

    if not name or not location or not rooms_available or not price_per_night or not rating:
        flash('All fields are required!', 'error')
        return redirect(url_for('index'))

    new_hotel = Hotel(
        name=name,
        location=location,
        rooms_available=rooms_available,
        price_per_night=price_per_night,
        rating=rating
    )
    db.session.add(new_hotel)
    db.session.commit()
    flash('Hotel registered successfully!', 'success')
    return redirect(url_for('index'))


# UPDATE
@app.route('/update/<int:id>', methods=['POST'])
def update_hotel(id):
    hotel = Hotel.query.get_or_404(id)
    hotel.name = request.form.get('name')
    hotel.location = request.form.get('location')
    hotel.rooms_available = request.form.get('rooms_available')
    hotel.price_per_night = request.form.get('price_per_night')
    hotel.rating = request.form.get('rating')
    db.session.commit()
    flash('Hotel updated successfully!', 'success')
    return redirect(url_for('index'))


# DELETE
@app.route('/delete/<int:id>')
def delete_hotel(id):
    hotel = Hotel.query.get_or_404(id)
    db.session.delete(hotel)
    db.session.commit()
    flash('Hotel deleted successfully!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        # db.create_all() only creates tables that do not already exist.
        # If instance/example.db already exists (e.g. from another app/model),
        # this will simply add the 'hotel' table into it without affecting
        # any existing tables/data.
        db.create_all()
    app.run(debug=True)