from flask import Flask, render_template, request, session, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, User
from flask_session import Session

from tools import generate_random_code

app = Flask(__name__)
app.secret_key = 'r00rur9cm923cnd92y3cn19'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

engine = create_engine('sqlite:///users.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


@app.route("/")
def generate_code():
    return render_template('index.html', code=str(generate_random_code(8)))


@app.route("/authed_generate_code/")
def generate_code_auth():
    user_id = session.get('user_id')
    if user_id is not None:
        session.pop('user_id', None)
        return render_template('authed_code.html', code=str(generate_random_code(8)))
    else:
        return redirect("/auth/")


@app.route("/auth/", methods=['POST', 'GET'])
def auth():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db_session.query(User).filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.id
            return redirect("/authed_generate_code/")

        return "Не успешный вход"
    else:
        return render_template('auth.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0")