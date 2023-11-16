import os
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="menu_food",
    user="postgres",
    password="1234")

cur = conn.cursor()

# creates a new table
cur.execute('DROP TABLE IF EXISTS my_food_category CASCADE;')
cur.execute('CREATE TABLE my_food_category (id serial PRIMARY KEY,'
            'name varchar (30) NOT NULL,'
            'base_price integer  NOT NULL);'
            )
cur.execute('DROP TABLE IF EXISTS ingredients CASCADE;')
cur.execute('CREATE TABLE ingredients (id serial PRIMARY KEY,'
            'name varchar (30) NOT NULL,'
            'price integer NOT NULL);'
            )

cur.execute('DROP TABLE IF EXISTS fillings CASCADE;')
cur.execute('CREATE TABLE fillings (id serial PRIMARY KEY,'
            'ingredients_id integer NOT NULL REFERENCES ingredients(id),'
            'food_id integer NOT NULL REFERENCES my_food_category(id));'
            )
cur.execute('DROP TABLE IF EXISTS toppings CASCADE;')
cur.execute('CREATE TABLE toppings (id serial PRIMARY KEY,'
            'ingredients_id integer NOT NULL REFERENCES ingredients(id),'
            'food_id integer NOT NULL REFERENCES my_food_category(id));'
            )
cur.execute('DROP TABLE IF EXISTS my_food_order CASCADE;')
cur.execute('CREATE TABLE my_food_order (id serial PRIMARY KEY,'
            'order_date TIMESTAMP NOT NULL,'
            'toppings_id integer NOT NULL REFERENCES toppings(id),'
            'food_id integer NOT NULL REFERENCES my_food_category(id),'
            'fillings_id integer NOT NULL REFERENCES fillings(id),'
            'total_price integer );'
            )

cur.execute('DROP TABLE IF EXISTS customer_order')
cur.execute('CREATE TABLE customer_order(id serial PRIMARY KEY,'
            'customer_name VARCHAR(100) NOT NULL,'
            'order_name VARCHAR (100) NOT NULL,'
            'topping_name integer NOT NULL REFERENCES toppings(id),'
            'filling_name integer NOT NULL REFERENCES fillings(id),'
            'order_date TIMESTAMP NOT NULL,'
            'total_price INTEGER NOT NULL);'
            )


# Insert table for customer_order
# cur.execute('CREATE TABLE customer_order (id serial PRIMARY KEY,'
#             'customer_name varchar(100) NOT NULL,'
#             'order_name integer NOT NULL REFERENCES my_food_order(id),'
#             'order_date TIMESTAMP NOT NULL'
#             'total_price integer );'
#             )

# Insert data into the table

cur.execute(
    "INSERT INTO my_food_category (name, base_price) VALUES ('Pizza', 50000)")
cur.execute(
    "INSERT INTO my_food_category (name, base_price) VALUES ('Doughnut', 20000)")
cur.execute(
    "INSERT INTO my_food_category (name, base_price) VALUES ('Pie',45000)")
cur.execute("INSERT INTO ingredients (name, price)VALUES ('Cheese',12000)")
cur.execute("INSERT INTO ingredients (name, price)VALUES ('Chicken',18000)")

cur.execute("INSERT INTO ingredients (name, price) VALUES ('Pepper',8000)")
cur.execute("INSERT INTO ingredients (name, price)VALUES ('Tomato',9000)")
cur.execute("INSERT INTO ingredients (name, price)VALUES ('Tuna',20000)")
cur.execute("INSERT INTO ingredients (name, price)VALUES ('Blueberry',12000)")
cur.execute("INSERT INTO ingredients (name, price)VALUES ('Sugar Glaze',10000)")
cur.execute("INSERT INTO ingredients (name, price) VALUES ('Apple Slices',14000)")
cur.execute("INSERT INTO ingredients (name, price)VALUES ('Milk Cream',10000)")


# cur.execute("INSERT INTO my_food_order (customer_name, order_date, food_id, toppings_id, fillings_id, total_price) VALUES (%s, %s, %s, %s, %s, %s)",
#             (customer_name, order_date, food_id, toppings_id, fillings_id, total_price))

conn.commit()

cur.close()
conn.close()
