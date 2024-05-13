from flask import Flask

app = Flask(__name__)


@app.get('/register')
def register_form():
    return 'please input your info'


@app.post('/register')
def new_user_register():
    return 'new user created'


@app.get('/login')
def login_form():
    return 'input login and password'


@app.post('/login')
def login_user():
    return 'user logged in'


@app.get('/user')
def user_info():
    return 'user info'


@app.put('/user')
def update_user_info():
    return 'updated user info'


@app.post('/user')
def add_user_info():
    return 'added user info'


@app.get('/funds')
def funds():
    return 'users\'s balance'


@app.post('/funds')
def add_funds():
    return 'added funds'


@app.get('/user/reservations')
def reservations():
    return 'users\'s reservations'


@app.post('/user/reservations')
def add_reservations():
    return 'added reservations'


@app.get('/user/reservations/<reservation_id>')
def chosen_reservations(reservation_id):
    return f'chosen reservation {reservation_id}'


@app.put('/user/reservations/<reservation_id>')
def update_reservations(reservation_id):
    return f'updated reservation: {reservation_id}'


@app.delete('/user/reservations/<reservation_id>')
def delete_reservations(reservation_id):
    return f'deleted reservation: {reservation_id}'


@app.get('/user/checkout')
def user_checkout():
    return 'user checkout info'


@app.post('/user/checkout')
def make_payment():
    return 'user payed'


@app.put('/user/checkout')
def change_payment_method():
    return 'payment method changed'


@app.get('/fitness_center')
def fitness_center():
    return 'fitness center info'


@app.get('/fitness_center/<fitness_center_id>')
def chosen_fitness_center(fitness_center_id):
    return f'chosen fitness center {fitness_center_id}'


@app.get('/fitness_center/<fitness_center_id>/trainer')
def trainers(fitness_center_id):
    return f'available trainers in {fitness_center_id}'


@app.get('/fitness_center/<fitness_center_id>/trainer/<trainer_id>')
def chosen_trainer(trainer_id, fitness_center_id):
    return f'chosen trainer {trainer_id} in {fitness_center_id}'


@app.get('/fitness_center/<fitness_center_id>/trainer/<trainer_id>/rating')
def trainer_rating(fitness_center_id, trainer_id):
    return f'rating for trainer {trainer_id} in {fitness_center_id}'


@app.post('/fitness_center/<fitness_center_id>/trainer/<trainer_id>/rating')
def create_trainer_rating(fitness_center_id, trainer_id):
    return f'added rating for trainer: {trainer_id} in {fitness_center_id}'


@app.put('/fitness_center/<fitness_center_id>/trainer/<trainer_id>/rating')
def update_trainer_rating(fitness_center_id, trainer_id):
    return f'updated rating for trainer: {trainer_id} in {fitness_center_id}'


@app.get('/fitness_center/<fitness_center_id>/services')
def services(fitness_center_id):
    return f'available services in {fitness_center_id}'


@app.get('/fitness_center/<fitness_center_id>/services/<service_id>')
def chosen_service(fitness_center_id, service_id):
    return f'chosen service {service_id} in {fitness_center_id}'


@app.get('/fitness_center/<fitness_center_id>/loyalty_programs')
def loyalty_programs(fitness_center_id):
    return f'available loyalty programs in {fitness_center_id}'


if __name__ == '__main__':
    app.run()
