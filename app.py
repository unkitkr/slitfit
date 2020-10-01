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
    return "yaay i'm working"









if __name__ == '__main__':
    app.run(debug=True)
