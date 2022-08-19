from flask import Flask
from flask import request
import sqlite3


app = Flask(__name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
        return d

def get_data(querry: str):
    conn = sqlite3.connect('db1.db')
    conn.row_factory = dict_factory
    cursor = conn.execute(querry)
    result = cursor.fetchall()
    conn.close()
    return result


@app.get('/currency/<currency_UPS>')
def currency_list(currency_UPS):
    res = get_data(f"select * from Currency where Name='{currency_UPS}'")
    return res

@app.get('/currency/<currency_UPS>/rating')
def currency_rating(currency_UPS):
    res = get_data(f"select avg(rating) from Rating where cur_name='{currency_UPS}'")
    return res

@app.get('/currency')
def all_currency_rating():
    res = get_data(f"SELECT round(avg(rating), 1), cur_name from rating GROUP by cur_name")
    return res


@app.get('/currency/trade/main:<currency_UPS1>/second:<currency_UPS2>')
def course_ups1_to_ups2(currency_UPS1, currency_UPS2):
    res = get_data(f""" SELECT round(
(SELECT The_cost_is_relative_to_USD from Currency WHERE Data = '11-08-22' and Name = 'EUR')/
(SELECT The_cost_is_relative_to_USD from Currency WHERE Data = '11-08-22' and Name = 'UAH'), 2))""")
    return res



@app.get('/user/<user_id>')
def login_get(user_id):
    res = get_data(f"select * from User WHERE user_id={user_id};")
    return res


@app.post('/currency/trade/<name1>/<name2>')
def currency_trade_post(name1, name2):
    return f'Currency exchange {name1} to {name2}. Post method'


@app.post('/currency/<name>/review')
def currency_review_post(name):
    return f'Review currency {name}, POST method'


@app.put('/currency/<name>/review')
def currency_review_put(name):
    return f'Review currency {name}, PUT method'


@app.delete('/currency/<name>/review')
def currency_review_gelete(name):
    return f'Review currency {name}, DELETE method'

@app.get('/currencies')
def amount_of_currency_available():
    res = get_data("SELECT currency_name, available_quantity FROM Currency WHERE date = '11-08-22'")
    return res

@app.get('/user')
def user_balance():
    res = get_data(f"SELECT balance, currency_name FROM Account WHERE user_id = 2")
    return res

@app.post('/user/transfer')
def transfer():
   pass


@app.get('/user/history')
def user_history():
    res = get_data("""SELECT user_id, type_of_transaction, amount_of_currency, currency_with_which_the_transaction, 
    currency_in_which_the_transaction, data_time,amount_of_currency_received, commission, 
    account_from_which_the_transaction, account_on_which_the_transaction FROM Transaction_history WHERE user_id=1""")
    return res


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
