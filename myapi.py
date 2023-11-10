from flask import Flask, jsonify, request, render_template, g
import psycopg2.extras
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="menu_food",
                        user="postgres",
                        password="1234",
                        host="localhost", port="5432")


@app.teardown_appcontext
def close_db_connection(exception):
    conn.close()

# cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)


@app.route('/menu')
def menu():
    # create a cursor
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Select all products from the table
    cur.execute(
        'select * from my_food_category')

    data = cur.fetchall()

    for index, food in enumerate(data):
        cur.execute(
            'select name,price from ingredients join toppings ON ingredients.id = toppings.ingredients_id where toppings.food_id =' + str(food['id']))
        data_toppings = cur.fetchall()
        data[index]["topping"] = data_toppings
        cur.execute(
            'select name,price from ingredients join fillings ON ingredients.id = fillings.ingredients_id where fillings.food_id =' + str(food['id']))
        data_fillings = cur.fetchall()
        data[index]["filling"] = data_fillings
    # Close the cursor and connection
    cur.close()
    return (data)


@app.route('/order', methods=['POST'])
def order():
    # Connect to the database
    cur = conn.cursor()

    # Get the order data from the request
    order_data = request.get_json()

    # Calculate the total price for the order
    total_price = 0
    for item in order_data:
        # Get the base price of the item
        cur.execute(
            'SELECT base_price FROM my_food_category WHERE id = %s', (item['food_id'],))
        base_price = cur.fetchone()[0]

        # Get the price of the filling
        if item['fillings_id']:
            cur.execute('SELECT price FROM ingredients WHERE id = %s',
                        (item['fillings_id'],))
            filling_price = cur.fetchone()[0]
        else:
            filling_price = 0

        # Get the price of the topping
        if item['toppings_id']:
            cur.execute('SELECT price FROM ingredients WHERE id = %s',
                        (item['toppings_id'],))
            topping_price = cur.fetchone()[0]
        else:
            topping_price = 0

        # Calculate the total price for the item
        item_price = base_price + filling_price + topping_price
        total_price += item_price

        # Get the customer_name
        # customer_name = order_data[customer_name]
        # order_date = order_data['order_date']

    # Insert the order data
    # cur.execute('INSERT INTO customer_order (customer_name, order_date, total_price) VALUES (%s, %s, %s)',
     #           (order_data['customer_name'], order_data['order_date'], total_price))
    cur.execute('INSERT INTO customer_order (customer_name, order_date, total_price) VALUES (%s, %s, %s)',
                (order_data(item['food_id']), total_price))
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

# @app.route('/customer_order', methods=['POST'])
# def customer_order():
#     # customer_name = order_data['customer_name']
#     if request.method == 'POST':
#         customer_name = request.form['customer_name']
#         order_date = request.form['order_date']

#         conn = get_db_connection()
#         cur = conn.cursor()
#         cur.execute('INSERT INTO customer_order (customer_name, order_date, order_name, total_price)''VALUES (%s, %s, %s, %s)',
#                     (customer_name, order_date, order_name, total_price))
#         conn.commit()

    # Close the cursor and connection
    cur.close()

    # Return the total price as a JSON response
    return jsonify({'total_price': total_price})


if __name__ == '__main__':
    app.run(port=9000, debug=True, host='0.0.0.0')
