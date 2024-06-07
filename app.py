import sqlite3
from multiprocessing.reduction import register

from flask import Flask, request, render_template

app = Flask(__name__)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_from_db(table, condition=None, join_table=None, join_condition=None):
    query = f"SELECT * FROM {table}"
    conditions = []

    if join_table is not None:
        join_condition_list = []
        for key, value in join_condition.items():
            join_condition_list.append(f"{key}={value}")
        join_condition_str = ' and '.join(join_condition_list)
        join_str = f' join {join_table} on {join_condition_str}'
        query = query + join_str

    if condition is not None:
        for key, value in condition.items():
            conditions.append(f"{key} = {value}")
        str_conditions = " and ".join(conditions)
        str_conditions = " where " + str_conditions
        query += str_conditions

    con = sqlite3.connect('db.db')
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute(query)
    if table:
        res = cur.fetchall()
    else:
        res = cur.fetchone()
    con.close()
    return res


def insert_into_db(table, data):
    keys = []
    values = []
    for key, value in data.items():
        keys.append(key)
        values.append("'" + str(value) + "'")
        str_keys = ', '.join(keys)
        str_values = ', '.join(values)
        query = f"""insert into {table} ({str_keys}) values ({str_values})"""
        con = sqlite3.connect('db.db')
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        con.close()


@app.get('/register')
def register_form():
    return render_template('register_form.html')


@app.post('/register')
def new_user_register():
    form_data = request.form
    insert_into_db("user", {"login": form_data['login_reg'], "password": form_data['password_reg'],
                            "date": form_data['birth_date_reg'], "phone": form_data['phone_reg']})
    return 'new user created'


@app.get('/login')
def login_form():
    return render_template('login_form.html')


@app.post('/login')
def login_user():
    return 'user logged in'


@app.get('/user/<user_id>')
def user_info(user_id):
    res = get_from_db("user", {"id": user_id})
    return render_template("user_info.html", user_info=res)


@app.put('/user/<user_id>')
def update_user_info():
    return 'updated user info'


@app.post('/user/<user_id>')
def add_user_info():
    return 'added user info'


@app.get('/user/<user_id>/funds')
def funds():
    res = get_from_db('SELECT funds FROM user WHERE id=1')
    return str(res)


@app.post('/user/<user_id>/funds')
def add_funds():
    return 'added funds'


@app.get('/user/<user_id>/reservations')
def reservations():
    res = get_from_db('SELECT * FROM reservation')
    return str(res)


@app.post('/user/<user_id>/reservations')
def add_reservations():
    return 'added reservations'


@app.get('/user/<user_id>/reservations/<reservation_id>')
def chosen_reservations(reservation_id):
    res = get_from_db(f'SELECT * FROM reservation where id={reservation_id}')
    return str(res)


@app.put('/user/<user_id>/reservations/<reservation_id>')
def update_reservations(reservation_id):
    return f'updated reservation: {reservation_id}'


@app.delete('/user/<user_id>/reservations/<reservation_id>')
def delete_reservations(reservation_id):
    return f'deleted reservation: {reservation_id}'


@app.get('/user/<user_id>/checkout')
def user_checkout(user_id):
    res = get_from_db(
        f'SELECT funds FROM user where id = {user_id}')
    return str(res)


@app.post('/user/<user_id>/checkout')
def make_payment():
    return 'user payed'


@app.put('/user/<user_id>/checkout')
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
        f'SELECT name FROM trainer WHERE fitness_center_id = {fitness_center_id} AND id = {trainer_id}', True)
    return str(res)


@app.get('/fitness_center/<fitness_center_id>/trainer/<trainer_id>/rating')
def trainer_rating(fitness_center_id, trainer_id):
    res = get_from_db(
        f'SELECT * FROM review WHERE fitness_center_id = {fitness_center_id} AND trainer_id = {trainer_id}', True)
    return str(res)


@app.post('/fitness_center/<fitness_center_id>/trainer/<trainer_id>/rating')
def create_trainer_rating(fitness_center_id, trainer_id):
    return f'added rating for trainer: {trainer_id} in {fitness_center_id}'


@app.put('/fitness_center/<fitness_center_id>/trainer/<trainer_id>/rating')
def update_trainer_rating(fitness_center_id, trainer_id):
    return f'updated rating for trainer: {trainer_id} in {fitness_center_id}'


@app.get('/fitness_center/<fitness_center_id>/services')
def services(fitness_center_id):
    res = get_from_db("service", {"fitness_center_id": fitness_center_id})
    return str(res)


@app.get('/fitness_center/<fitness_center_id>/services/<service_id>')
def chosen_service(fitness_center_id, service_id):
    res = get_from_db(f'SELECT * FROM service WHERE fitness_center_id = {fitness_center_id} and id = {service_id}',
                      False)


@app.get('/fitness_center/<fitness_center_id>/loyalty_programs')
def loyalty_programs(fitness_center_id):
    return f'available loyalty programs in {fitness_center_id}'  # we can't got loyalty program cause we didn't add table loyality programs


if __name__ == '__main__':
    app.run()
