from flask import Flask, jsonify, request, render_template
import psycopg2.extras
import psycopg2

app = Flask(__name__)

# conn = psycopg2.connect(database="food_menu",
#                         user="postgres",
#                         password="1234",
#                         host="localhost", port="5432")

# cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)


@app.route('/menu')
def menu():
    conn = psycopg2.connect(database="menu_food",
                            user="postgres",
                            password="1234",
                            host="localhost", port="5432")


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
    conn.close()
    return (data)

    

@app.route('/order', methods=['POST'])
def order():
    #Connect to the database
    conn = psycopg2.connect(database="menu_food",
                            user="postgres",
                            password="1234",
                            host="localhost", port="5432")
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

    # Close the cursor and connection
    cur.close()
    conn.close()

    # Return the total price as a JSON response
    return jsonify({'total_price': total_price})


if __name__ == '__main__':
    app.run(port=9000, debug=True, host='0.0.0.0')
