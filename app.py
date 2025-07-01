from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///firstapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'this-is-not-a-secret'
db = SQLAlchemy(app)

class User(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'{self.sno} - {self.first_name} - {self.email}'

@app.route('/login', methods=['GET', 'POST'])
def login():
    # No validation or authentication, just logs in any input
    if request.method == 'POST':
        email = request.form.get('email')
        session['user'] = email
        return redirect(url_for('index'))
    return render_template('login.html', error=None)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        first_name = request.form['first_name']
        email = request.form['email']
        password = request.form['password']
        new_user = User(first_name=first_name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/delete/<int:sno>')
def delete(sno):
    if 'user' not in session:
        return redirect(url_for('login'))
    user = User.query.get_or_404(sno)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if 'user' not in session:
        return redirect(url_for('login'))
    user = User.query.get_or_404(sno)
    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.email = request.form['email']
        user.password = request.form['password']
        db.session.commit()
        return redirect('/')
    return render_template('update.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)