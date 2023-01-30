from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazwaU = db.Column(db.String, unique=True)
    hasloU = db.Column(db.String)
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, nazwaU, hasloU):
        self.nazwaU = nazwaU
        self.hasloU = hasloU

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)




@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nazwaU = request.form['nazwaU']
        hasloU = request.form['hasloU']
        user = User.query.filter_by(nazwaU=nazwaU, hasloU=hasloU).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


class consq_g(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    data = db.Column(db.Integer)
    rating = db.Column(db.Float)


with app.app_context():
    db.create_all()
    new_user = User(nazwaU='admin', hasloU='admin')
    db.session.add(new_user)
    db.session.commit()


@app.route('/rate_game', methods=['POST'])
@login_required
def rate_game():
    game_id = request.form['game_id']
    consq_x = consq_g.query.get(game_id)
    consq_x.rating = request.form['rating']
    db.session.commit()
    return redirect(url_for('index'))



@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        data = request.form['data']
        rating = request.form['rating']
        new_game = consq_g(name=name, data=data, rating=rating)
        db.session.add(new_game)
        db.session.commit()

    sort_by = request.args.get('sort_by', 'name')
    if sort_by == 'name':
        games = consq_g.query.order_by(consq_g.name).all()
    elif sort_by == 'data':
        games = consq_g.query.order_by(consq_g.data).all()
    elif sort_by == 'rating':
        games = consq_g.query.order_by(consq_g.rating).all()
    else:
        games = consq_g.query.all()

    return render_template('index.html', games=games)


@app.route('/delete_game', methods=['POST'])
@login_required
def delete_game():
    game_id = request.form['game_id']
    game = consq_g.query.get(game_id)
    db.session.delete(game)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = 'ultra_secret_key'
    app.run(debug=False, port=3000, host='0.0.0.0')
