import functools
import psycopg2
from flask import(
        Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth') 
con = psycopg2.connect(
        database='stockinfo',
        user='Ryan',
        password='',
        host='127.0.0.1', 
        port='5432'
        )
cur = con.cursor()

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        get_user = cur.execute(
                'SELECT * FROM users WHERE id = %s;', (user_id,)
                )
        g.user = cur.fetchone()
    


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        error = None
        cur.execute("SELECT id FROM users WHERE username = %s;", (username,)
                )
        rows = cur.fetchall()

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'
        elif rows is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            cur.execute(
                    "INSERT INTO users(username, email, password) VALUES(%s, %s, %s)",
                    (username, email, generate_password_hash(password))
                    )
            con.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')



@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = cur.execute(
                "SELECT * FROM users WHERE username=%s", (username,)
                )
        
        rows = cur.fetchall()
        for i in rows:
            if i[1] is None:
                error = 'Incorrect username.'
            elif not check_password_hash(i[3], password):
                error = 'Incorrect username or password.'
                
            if error is None:
                session.clear()
                session['user_id'] = i[0]
                return redirect(url_for('index'))
            flash(error)

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
