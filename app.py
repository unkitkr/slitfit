from flask import Flask, render_template, request, redirect
from models import db, Users, UserLinks
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
import uuid
import shortuuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:SudoAdmin123@localhost/slit"
app.config['SECRET_KEY'] = '0817PDNTSPA'

db.app = app
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Algorithm for creating random IDs


def generate_random_uid(url):
    modulus = 6
    url_length = len(url)
    length_required = url_length % modulus
    if length_required < 3:
        length_required += 3
    random_sequence = uuid.uuid4()
    best_sequence = shortuuid.random(length=length_required)
    return (best_sequence)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


db.create_all()


@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        user_password = request.form['user_password']

        is_email_registered = Users.query.filter_by(email=user_email).first()

        if not is_email_registered:
            new_user = Users(name=user_name, password=generate_password_hash(
                user_password), email=user_email)

            try:
                db.session.add(new_user)
                db.session.commit()
                return render_template('dashboard.html')

            except Exception as e:
                db.session.rollback()
                return str(e)
        else:
            return render_template('index.html', err="The email alreay exixts")
    else:
        return redirect('/')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        user_email = request.form['user_email']
        user_password = request.form['user_password']
        user_exist = Users.query.filter_by(email=user_email).first()
        if user_exist:
            if check_password_hash(user_exist.password, user_password):
                login_user(user_exist)
                return redirect('/dashboard')
            else:
                return render_template('index.html', err="Wrong password")
        else:
            return render_template('index.html', err="User not registered")


@login_required
@app.route('/dashboard', methods=['GET'])
def dashboard():
    if request.method == 'GET':
        all_done_links = UserLinks.query.filter_by(
            owner=current_user.uid).all()
        total_visits = UserLinks.query.filter_by(
            owner=current_user.uid).filter(UserLinks.visited_times > 0).all()
        active_links = UserLinks.query.filter_by(
            owner=current_user.uid).filter_by(is_active=True).all()
        higest_visits = UserLinks.query.filter_by(owner=current_user.uid).all()
        higest_visited = max([x.visited_times for x in higest_visits])
        payload = {
            'name': current_user.name,
            'joined': current_user.date_of_joining.date(),
            'email': current_user.email,
            'links_created': len(all_done_links),
            'total_visits': len(total_visits),
            'active_links': len(active_links),
            'higest_visit': higest_visited,
            'all_links': all_done_links,
        }
        print(payload)
        return render_template('dashboard.html', payload=payload)


@login_required
@app.route('/createnewurl', methods=['POST'])
def create_new_url():
    if request.method == 'POST':
        link_name = request.form['link_name']
        long_link = request.form['long_link']
        hashed_url = generate_random_uid(long_link)

        if not UserLinks.query.filter_by(short_key=hashed_url).first():
            new_short_url = UserLinks(
                owner=current_user.uid, name=link_name, original_link=long_link, short_key=hashed_url)
            try:
                db.session.add(new_short_url)
                db.session.commit()
                redirect_url = "www.slit.fit/"+hashed_url
                return render_template('dashboard.html', err = "The URL is added succesfully:"+" ", url_msg = redirect_url)

            except Exception as e:
                db.session.rollback()
                return render_template('dashboard.html', err ='OOPs we ran into some problem. Please try again.')
        else:
            return render_template('dashboard.html', err = 'OOPs we ran into some problem. Please try again.')


if __name__ == '__main__':
    app.run(debug=True)
