import sqlite3
from flask import Flask, request

app = Flask(__name__)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_from_db(query, many=True):
    con = sqlite3.connect('db.db')
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute(query)
    if many:
        res = cur.fetchall()
    else:
        res = cur.fetchone()
    con.close()
    return res


def insert_into_db(query):
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    con.close()


@app.get('/register')
def register_form():
    return f"""<form action="/register" method="post">
  <label for="login">Login:</label><br>
  <input type="text" id="login_reg" name="login"><br>
  <label for="password">Password:</label><br>
  <input type="password" id="password_reg" name="password_reg"><br>
  <label for="birth_date">Birth date:</label><br>
  <input type="date" id="birth_date_reg" name="birth_date_reg"><br>
  <label for="phone">Phone:</label><br>
  <input type="text" id="phone_reg" name="phone_reg"><br>
  <input type="submit" value="Submit">
</form>"""


@app.post('/register')
def new_user_register():
    form_data = request.form
    insert_into_db(
        f'INSERT INTO user(login, password, birth_date, phone) VALUES (\'{form_data["login_reg"]}\', \'{form_data["password_reg"]}\', \'{form_data["birth_date_reg"]}\', \'{form_data["phone_reg"]}\')')
    return 'new user created'


@app.get('/login')
def login_form():
    return f"""<form action="/login" method="post">
  <label for="login">Login:</label><br>
  <input type="text" id="login_log" name="login_log"><br>
  <label for="password">Password:</label><br>
  <input type="password_log" id="password" name="password_log"><br>
  <input type="submit" value="Submit">
</form>"""


@app.post('/login')
def login_user():
    return 'user logged in'


@app.get('/user')
def user_info():
    res = get_from_db('SELECT login, phone, birth_date FROM user WHERE id=1')
    return {res}


@app.put('/user')
def update_user_info():
    return 'updated user info'


@app.post('/user')
def add_user_info():
    return 'added user info'


@app.get('/funds')
def funds():
    res = get_from_db('SELECT funds FROM user WHERE id=1')
    return str(res)


@app.post('/funds')
def add_funds():
    return 'added funds'


@app.get('/user/reservations')
def reservations():
    res = get_from_db('SELECT * FROM reservation')
    return str(res)


@app.post('/user/reservations')
def add_reservations():
    return 'added reservations'


@app.get('/user/reservations/<reservation_id>')
def chosen_reservations(reservation_id):
    res = get_from_db('SELECT * FROM reservation where id=1')
    return str(res)


@app.put('/user/reservations/<reservation_id>')
def update_reservations(reservation_id):
    return f'updated reservation: {reservation_id}'


@app.delete('/user/reservations/<reservation_id>')
def delete_reservations(reservation_id):
    return f'deleted reservation: {reservation_id}'


@app.get('/user/checkout')
def user_checkout():
    res = get_from_db(
        'SELECT funds FROM user where id=1')  # not sure what here should be, maybe better price form service? did not get idea
    return str(res)


@app.post('/user/checkout')
def make_payment():
    return 'user payed'


@app.put('/user/checkout')
def change_payment_method():
    return 'payment method changed'


@app.get('/fitness_center')
def fitness_center():
    res = get_from_db('select name, address from fitness_center')
    return str(res)


@app.get('/fitness_center/<fitness_center_id>')
def chosen_fitness_center(fitness_center_id):
    res = get_from_db(f'select name, address from fitness_center where id = {fitness_center_id}', False)
    return str(res)


@app.get('/fitness_center/<fitness_center_id>/trainer/<trainer_id>')
def chosen_trainer(trainer_id, fitness_center_id):
    res = get_from_db(
        f'SELECT name FROM trainer WHERE fitness_center_id = 1 AND id = 1', True)
    return str(res)


@app.get('/fitness_center/<fitness_center_id>/trainer/<trainer_id>/rating')
def trainer_rating(fitness_center_id, trainer_id):
    # res = get_from_db(
    #     f'SELECT * FROM review WHERE fitness_center_id = 1 AND trainer_id = 1', True)
    # return str(res)
    return 'review'


@app.post('/fitness_center/<fitness_center_id>/trainer/<trainer_id>/rating')
def create_trainer_rating(fitness_center_id, trainer_id):
    return f'added rating for trainer: {trainer_id} in {fitness_center_id}'


@app.put('/fitness_center/<fitness_center_id>/trainer/<trainer_id>/rating')
def update_trainer_rating(fitness_center_id, trainer_id):
    return f'updated rating for trainer: {trainer_id} in {fitness_center_id}'


@app.get('/fitness_center/<fitness_center_id>/services')
def services(fitness_center_id):
    res = get_from_db(f'SELECT * FROM service WHERE fitness_center_id = 1') # don't understand how to make thru {fitness_center_id}
    return str(res)


@app.get('/fitness_center/<fitness_center_id>/services/<service_id>')
def chosen_service(fitness_center_id, service_id):
    res = get_from_db(f'SELECT * FROM service WHERE fitness_center_id = 1 and id = 1', False)  # don't understand how to make thru {fitness_center_id}
    return str(res)


@app.get('/fitness_center/<fitness_center_id>/loyalty_programs')
def loyalty_programs(fitness_center_id):
    return f'available loyalty programs in {fitness_center_id}' # we can't got loyalty program cause we didn't add table loyality programs


if __name__ == '__main__':
    app.run()
