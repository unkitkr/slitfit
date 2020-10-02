from flask import Flask, render_template, request, redirect
from models import db,Users
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:SudoAdmin123@localhost/slit"
app.config['SECRET_KEY'] = '0817PDNTSPA'

db.app = app
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

db.create_all()

@app.route('/', methods = ['GET'])
def homepage():
    return render_template('index.html')

@app.route('/signup', methods = ['POST','GET'])
def signup():
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        user_password = request.form['user_password']

        is_email_registered = Users.query.filter_by(email = user_email).first()

        if not is_email_registered:
            new_user = Users(name = user_name, password = generate_password_hash(user_password), email = user_email)

            try:
                db.session.add(new_user)
                db.session.commit()
                return render_template('dashboard.html')

            except Exception as e:
                db.session.rollback()
                return str(e)
        else:
            return render_template('index.html', err = "The email alreay exixts")
    else:
        return redirect('/')

@app.route('/signin', methods = ['GET','POST'])
def signin():
    if request.method == 'POST':
        user_email = request.form['user_email']
        user_password = request.form['user_password']
        user_exist = Users.query.filter_by(email = user_email).first()
        if user_exist:
            if check_password_hash(user_exist.password, user_password):
                login_user(user_exist)
                return render_template('dashboard.html')
            else:
                return render_template('index.html', err = "Wrong password")
        else:
            return render_template('index.html', err = "User not registered")




if __name__ == '__main__':
    app.run(debug=True)
