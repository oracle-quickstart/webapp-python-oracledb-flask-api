#------------------------------------------------------------------------------
# Copyright (c) 2023, Oracle and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#------------------------------------------------------------------------------

import os

import flask
from flask import Flask, jsonify, request
from flask import render_template
from flask_cors import CORS
from flask import session, redirect, url_for, request, Response

import oracledb

# Environment Variables for Oracle Database Connectivity
user = os.environ['ORACLE_USER']
password = os.environ['ORACLE_PASSWORD']
dsn = os.environ['ORACLE_DSN']
# wallet_location = os.environ['TNS_ADMIN']
# wallet_password = os.environ['ORACLE_PASSWORD']

# start_pool(): starts the connection pool
def start_pool():

    # Generally a fixed-size pool is recommended, i.e. pool_min=pool_max.
    # Here the pool contains 4 connections, which is fine for 4 concurrent
    # users.

    pool_min = 4
    pool_max = 4
    pool_inc = 0

    pool = oracledb.create_pool(user=user,
                                   password=password,
                                   dsn=dsn,
#                                  wallet_location=wallet_location,
#                                  wallet_password=wallet_password,
                                   min=pool_min,
                                   max=pool_max,
                                   increment=pool_inc)

    return pool

app = Flask(__name__, template_folder='/myapp')
CORS(app)

# List of API User and Auth Token
VALID_USERS = {'user1': 'password1', 'user2': 'password2'}

# HTML Form Method to Create a New Employee
@app.route('/api/add_employee', methods=['GET', 'POST'])
def add_employee_form():
    # Require authentication for all requests
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

    if request.method != 'POST':
        return render_template('add_employee.html')
    else:
        # Extract the employee data from the form
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']

        # Insert the employee into the database
        with pool.acquire() as con:
            with con.cursor() as cur:
                cur.execute("""INSERT INTO employees (name, email, department)
                               VALUES (:bvname, :bvemail, :bvdepartment)""",
                            {'bvname': name, 'bvemail': email, 'bvdepartment': department})
                con.commit()

                # Return the ID of the new employee
                return redirect(url_for('get_all'))


# HTML Method to Get a List of All Employees
@app.route('/api/getall')
def get_all():
    # Require authentication for all requests
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

    with pool.acquire() as con:
        with con.cursor() as cur:
            cur.arraysize = 1000
            employees = []
            for row in cur.execute("SELECT * FROM employees"):
                employee = {'id': row[0], 'name': row[1], 'email': row[2], 'department': row[3]}
                employees.append(employee)
            return render_template('get_employees.html', employees=employees)


# HTML Method to Update en Employee
@app.route('/api/update_employee/<int:id>', methods=['GET','POST'])
def update_employee(id):

    # Require authentication for all requests
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

    with pool.acquire() as con:
        with con.cursor() as cur:
            if request.method == 'POST':
                name = request.form['name']
                email = request.form['email']
                department = request.form['department']
                cur.execute("""UPDATE employees
                               SET name = :bvname, email = :bvemail, department = :bvdepartment
                               WHERE id = :idbv""",
                            {'bvname': name, 'bvemail': email, 'bvdepartment': department, 'idbv': id})
                con.commit()
                return redirect(url_for('get_all'))
            else:
                cur.execute("""SELECT *
                               FROM employees
                               WHERE id = :bvid""", {'bvid': id})
                employee = cur.fetchone()
                return render_template('update_employee.html', employee=employee)


# HTML Method to Delete an Employee
@app.route('/api/delete_employee/<int:id>', methods=['GET', 'POST'])
def delete_employee(id):
    # Require authentication for all requests
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

    with pool.acquire() as con:
        with con.cursor() as cur:
            if request.method == 'POST':
                cur.execute("DELETE FROM employees WHERE id = :bvid", {'bvid': id})
                con.commit()
                return redirect(url_for('get_all'))
            else:
                cur.execute("SELECT * FROM employees WHERE id = :bvid", {'bvid': id})
                employee = cur.fetchone()
                return render_template('confirm_delete_employee.html', employee=employee)

# Main Page for Listing All Methods
@app.route('/api/main', methods=['GET'])
def crud_options():
    # Require authentication for all requests
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

    return render_template('crud_options.html')

@app.route('/api/search_employee', methods=['GET', 'POST'])
def search_employee():
    # Require authentication for all requests
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

    search_query = request.args.get('search_query') or request.form.get('search_query')

    if not search_query:
        return render_template('search_employee.html', employee=None)

    query = f"""SELECT * FROM employees WHERE
                LOWER(name) LIKE LOWER(:search_query) OR
                LOWER(email) LIKE LOWER(:search_query) OR
                LOWER(department) LIKE LOWER(:search_query) OR
                TO_CHAR(id) LIKE :search_query"""
    with pool.acquire() as con:
        with con.cursor() as cur:
            cur.execute(query, {'search_query': f'%{search_query}%'})
            employee = cur.fetchone()

            if employee is None:
                # Display a message if the employee is not found
                return render_template('employee_not_found.html', search_query=search_query)
            else:
                # Display the employee details if found
                return render_template('search_employee.html', employee=employee)


def check_auth(username, password):
    """Check if a username/password combination is valid."""
    return username in VALID_USERS and password == VALID_USERS[username]

def authenticate():
    """Send a 401 Unauthorized response that prompts the user to authenticate."""
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})

if __name__ == '__main__':

    # Start a pool of connections
    pool = start_pool()

    # Print out all the routes and their associated URLs
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint:50s} {rule.methods} {rule.rule}")

    # Start the HTTPS server
    app.run(host='0.0.0.0', port=4443, ssl_context=('cert.pem', 'key.pem'))

