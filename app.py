
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///names.db'
db=SQLAlchemy(app)

class NameAge(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

# In-memory list to store names temporarily
names_list = []

# Home page with form
@app.route('/')
def home():
    return render_template('home.html')

# Handle form submission
@app.route('/result', methods=['POST'])
def result():
    name_input = request.form['name']
    age_int= request.form['age']

    #names_list.append(name_input)  # Store the name in the list
    new_entry =NameAge(name=name_input, age=int(age_int))
    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for('all_names'))

# Display all names and ages
@app.route('/names')
def all_names():
    entries= NameAge.query.all()
    return render_template('names.html', entries=entries)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)

@app. route('/age')
def all_ages():
    return render_template('ages.html')

names_list1=[]
#Home page with form
def home():
    return
