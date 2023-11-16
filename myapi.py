from flask import Flask, jsonify, request, render_template
import psycopg2.extras
import psycopg2
from menu_repository import MenuRepository, NoResourceFoundException


app = Flask(__name__)

conn = psycopg2.connect(database="menu_food",
                        user="postgres",
                        password="1234",
                        host="localhost", port="5432")


menu_repository = MenuRepository(conn)
# @app.teardown_appcontext
# def close_db_connection(exception):
#     conn.close()
#     print("halooo")


class ClientException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(ClientException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response = jsonify({'error': str(error)})
    response.status_code = error.status_code
    return response


@app.route('/menu')
def menu():
    return menu_repository.get()


@app.route('/order', methods=['POST'])
def order():
    # Get the order data from the request
    order_data = request.get_json()
    try:
        order = menu_repository.create_order(order_data)
        return jsonify({'order': order})
    except NoResourceFoundException as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(port=9000, debug=True, host='0.0.0.0')
    input("Press Enter to continue...")
    conn.close()

# {
#     items: [
#         {
#             food: pizza,
#             topping: tomato,
#             filling: tuna,
#             price: 1000
#         },
#         {
#             food: pizza,
#             topping: tomato,
#             filling: tuna,
#             price: 1000
#         },
#     ],
#     total_price: 1000
# }
