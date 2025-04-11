from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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
    names_list.append(name_input)  # Store the name in the list
    return redirect(url_for('all_names'))

# Display all names
@app.route('/names')
def all_names():
    return render_template('names.html', names=names_list)

if __name__ == '__main__':
    app.run(debug=True)
