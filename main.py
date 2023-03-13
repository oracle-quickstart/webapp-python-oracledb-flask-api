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

app = Flask(__name__, template_folder='/')
CORS(app)

# List of API User and Auth Token
VALID_USERS = {'user1': 'password1', 'user2': 'password2'}

# Connect to the Oracle database
con = oracledb.connect(user=user, password=password, dsn=dsn)

# HTML Form Method to Create a New Employee
@app.route('/api/add_employee', methods=['GET', 'POST'])
def add_employee_form():
    # Require authentication for all requests
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

    if request.method == 'POST':
        # Extract the employee data from the form
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']

        # Insert the employee into the database
        cur = con.cursor()
        cur.execute("INSERT INTO employees (name, email, department) VALUES (:name, :email, :department)",
                    {'name': name, 'email': email, 'department': department})
        con.commit()

        # Return the ID of the new employee
        return redirect(url_for('get_all'))
    else:
        return render_template('add_employee.html')


# HTML Method to Get a List of All Employees
@app.route('/api/getall')
def get_all():
    # Require authentication for all requests
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

    cur = con.cursor()
    cur.prefetchrows = 100
    cur.arraysize = 100
    cur.execute("SELECT * FROM employees")
    rows = cur.fetchall()
    employees = []
    for row in rows:
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

    cur = con.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        cur.execute('UPDATE employees SET name=:name, email=:email, department=:department WHERE id=:id',
                       {'name': name, 'email': email, 'department': department, 'id': id})
        con.commit()
        cur.close()
        return redirect(url_for('get_all'))
    else:
        cur.execute('SELECT * FROM employees WHERE id=:id', {'id': id})
        employee = cur.fetchone()
        cur.close()
        return render_template('update_employee.html', employee=employee)


# HTML Method to Delete an Employee
@app.route('/api/delete_employee/<int:id>', methods=['GET', 'POST'])
def delete_employee(id):
    # Require authentication for all requests
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

    if request.method == 'POST':
        cur = con.cursor()
        cur.execute('DELETE FROM employees WHERE id=:id', {'id': id})
        con.commit()
        cur.close()
        return redirect(url_for('get_all'))
    else:
        cur = con.cursor()
        cur.execute('SELECT * FROM employees WHERE id=:id', {'id': id})
        employee = cur.fetchone()
        cur.close()
        return render_template('confirm_delete_employee.html', employee=employee)

# Main Page for Listing All Methods
@app.route('/api/main', methods=['GET'])
def crud_options():
    # Require authentication for all requests
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

    return render_template('crud_options.html')

# HTML Method to Search for an Employee by ID
@app.route('/api/search_employee/<int:id>', methods=['GET', 'POST'])
def search_employee(id):
    # Require authentication for all requests
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

    if request.method == 'POST':
        cur = con.cursor()
        cur.execute('SELECT * FROM employees WHERE id=:id', {'id': id})
        employee = cur.fetchone()
        cur.close()

        if employee is None:
            # Display a message if the employee is not found
            return render_template('employee_not_found.html', id=id)
        else:
            # Display the employee details if found
            return render_template('search_employee.html', employee=employee)
    else:
        # Create an empty employee object if a GET request is received
        return render_template('search_employee.html', employee=None)


def check_auth(username, password):
    """Check if a username/password combination is valid."""
    return username in VALID_USERS and password == VALID_USERS[username]

def authenticate():
    """Send a 401 Unauthorized response that prompts the user to authenticate."""
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})

if __name__ == '__main__':
    # Print out all the routes and their associated URLs
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint:50s} {rule.methods} {rule.rule}")

    # Start the HTTPS server
    app.run(host='0.0.0.0', port=4443, ssl_context=('cert.pem', 'key.pem'))
