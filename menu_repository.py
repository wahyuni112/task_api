from flask import Flask, jsonify, request, render_template
import psycopg2.extras
import psycopg2


class NoResourceFoundException(Exception):
    pass


class MenuRepository:
    def __init__(self, conn):
        self.conn = conn

    def get(self):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM my_food_category"
        cur.execute(query)

        data = cur.fetchall()

        for index, food in enumerate(data):
            query_toppings = 'select ingredients.id as id,name,price from ingredients join toppings ON ingredients.id = toppings.ingredients_id where toppings.food_id =' + \
                str(food['id'])
            cur.execute(query_toppings)
            data_toppings = cur.fetchall()
            print(data_toppings)
            data[index]["topping"] = data_toppings
            query_fillings = 'select ingredients.id as id,name,price from ingredients join fillings ON ingredients.id = fillings.ingredients_id where fillings.food_id =' + \
                str(food['id'])
            cur.execute(query_fillings)
            data_fillings = cur.fetchall()
            print(data_fillings)
            data[index]["filling"] = data_fillings
        self.conn.commit()

        return {'Menu': data}

    def create_order(self, order_data):
        cur = self.conn.cursor()
        order_data = request.get_json()
        order_list = []
        total_price = 0
        for item in order_data['items']:
            base_price_query = 'SELECT base_price FROM my_food_category WHERE id = %s'
            cur.execute(base_price_query, (item['food_id'],))
            food = cur.fetchone()
            if food is None:
                raise NoResourceFoundException(
                    f"Food not found for id: {item['food_id']}")
            base_price = food[-1]

            # Get the price of the filling
            if item['fillings_id']:
                filling_price_query = 'SELECT * FROM fillings LEFT JOIN ingredients ON ingredients.id = fillings.ingredients_id WHERE fillings.ingredients_id = %s'
                cur.execute(filling_price_query, (item['fillings_id'],))
                # filling_price = cur.fetchone()

                filling = cur.fetchone()
                if filling is None:
                    raise NoResourceFoundException(
                        f"Filling id is not found for id: {item['fillings_id']}")
                filling_price = filling[-1]
                # filling_name = filling
                # filling_price = filling['price']

            else:
                # filling_name = ''
                filling_price = 0

            # Get the price of the topping
            if item['toppings_id']:
                topping_price_query = 'SELECT ingredients.price FROM toppings LEFT JOIN ingredients ON ingredients.id = toppings.ingredients_id WHERE toppings.ingredients_id = %s'
                cur.execute(topping_price_query, (item['toppings_id'],))
                # topping_price = cur.fetchone()[0]

                topping = cur.fetchone()
                if topping is None:
                    raise NoResourceFoundException(
                        f"Topping id is not found for id: {item['toppings_id']}")
                topping_price = topping[-1]

            else:
                topping_price = 0
            # Calculate the total price for the item
            item_price = base_price + filling_price + topping_price
            total_price += item_price

            # Get the name of the food
            name_food_query = 'SELECT name FROM my_food_category WHERE id = %s'
            cur.execute(name_food_query, (item['food_id'],))
            food_name = cur.fetchone()[0]

            # Get the name of the topping
            if item['toppings_id']:
                topping_name_query = 'SELECT name FROM ingredients WHERE id = %s'
                cur.execute(topping_name_query, (item['toppings_id'],))
                topping_name = cur.fetchone()[0]
            else:
                topping_name = ''

            # Get the name of the filling
            if item['fillings_id']:
                filling_name_query = 'SELECT name FROM ingredients WHERE id = %s'
                cur.execute(filling_name_query, (item['fillings_id'],))
                filling_name = cur.fetchone()[0]
            else:
                filling_name = ''

            order_item = {
                # 'customer_name': customer_name,
                # 'order_date': order_date,
                'food': food_name,
                'filling': filling_name,
                'topping': topping_name,
                'price': item_price

            }
            order_list.append(order_item)

        # do command insert to database
        # cur = self.conn.cursor()
        customer_name = order_data['customer_name']
        order_name = order_data['order_name']
        order_date = order_data['order_date']

        cur.execute('INSERT INTO customer_order (customer_name, order_name, food_id, topping_name, filling_name, order_date, total_price) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (customer_name, order_name, item['food_id'], item['toppings_id'], item['fillings_id'], order_date, total_price))

        # order_item = {
        #     # 'customer_name': customer_name,
        #     # 'order_date': order_date,
        #     'food': food_name,
        #     'filling': filling_name,
        #     'topping': topping_name,
        #     'price': item_price

        # }
        # order_list.append(order_item)

        self.conn.commit()
        cur.close()

        # return
        response = {
            'customer_name': customer_name,
            'order_date': order_date,
            'items': order_list,
            'total_price': total_price
        }
        return (response)
