from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://task_manager_myy1_user:DA1Yo4VQBOxB7CXa1Ecs0FULf0K3kUG2@dpg-cvsi74re5dus7394o1bg-a.oregon-postgres.render.com/task_manager_myy1'
db = SQLAlchemy(app)

class NameAge(db.Model):
    __tablename__ = 'name_age'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    hobbies = db.relationship('Hobby', backref='person', lazy=True)


class Hobby(db.Model):
    __tablename__ = 'hobby'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('name_age.id'), nullable=False)

# Home page with form
@app.route('/')
def home():
    return render_template('home.html')

# Handle form submission
@app.route('/result', methods=['POST'])
def result():
    name_input = request.form['name']
    age_int = request.form['age']
    hobby_input = request.form['hobby']

    new_entry = NameAge(name=name_input, age=int(age_int))
    db.session.add(new_entry)
    db.session.commit()

    # Use the new_person.id as FK
    new_hobby = Hobby(description=hobby_input, person_id=new_entry.id)
    db.session.add(new_hobby)
    db.session.commit()

    return redirect(url_for('all_names'))

# Display all names and ages
@app.route('/names')
def all_names():
    entries = NameAge.query.all()
    return render_template('names.html', entries=entries)

# This ensures that the app uses the correct port when running on Glitch
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

@app.route('/age')
def all_ages():
    return render_template('ages.html')
