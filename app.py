from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///class_list.db'
db = SQLAlchemy(app)
app.secret_key = '22ea5dbb877a0f2e798907e7ed86bf28'

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    registration_number = db.Column(db.String(100), unique=True, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    registration_number = request.form['registration_number']
    new_student = Student(name=name, registration_number=registration_number)
    try: 
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))
    except IntegrityError:
        flash('registration number already exixts', 'error')
        return redirect(url_for('index'))



@app.route('/list', methods=['GET'])
def list():
    students = Student.query.all()
    return render_template('list.html', students=students)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
