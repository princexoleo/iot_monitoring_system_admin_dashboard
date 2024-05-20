from flask import Flask, jsonify, flash, render_template, request, redirect, url_for, session
import bcrypt  # For password hashing
import re
import os
from pathlib import Path
from dotenv import load_dotenv
from db_connection import *

load_dotenv()

RUN_PORT = int(os.environ.get('PORT', 5000))
DEBUG = bool(os.environ.get('DEBUG_MODE'))

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def user_dashboard():
    if 'username' in session:
        role_id = session['role_id']
        conn = create_connection()
        machine_data = get_machine_data_by_role_id(conn, role_id)
        roles_data = get_role_by_id(conn, session['role_id'])
        return render_template('user/dashboard.html', current_user=session['username'], m_data=machine_data,
                               roles_data=roles_data)
    return render_template("frontend/login.html")


# Add machine data to machine_data table
@app.route('/add_machine', methods=['GET', 'POST'])
def add_machine_data():
    if 'username' in session:
        current_user = session['username']
        role_id = session['role_id']
        if request.method == 'POST':
            machine_id = request.form['machine_id']
            location_name = request.form['location']
            alias_name = request.form['alias']
            print(f"AddMachineData: Input data: {machine_id}, {location_name}, {alias_name}")
            conn = create_connection()
            add_machine(conn, machine_id, location_name, alias_name, role_id)
            conn.close()
            print("Added Machine Data")
            return redirect(url_for('user_dashboard'))
        return render_template('frontend/add_machine_modal.html', current_user=current_user, role_id=role_id)
    return redirect(url_for('login'))


# admin user method
@app.route('/admin/dashboard')
def admin_dashboard():
    data = {
        "user_data": None,
        'roles_data': None
    }
    if 'username' in session:
        # Get all user  & role data from database and ppass through template
        conn = create_connection()
        user_data = get_users(conn)
        role_data = get_roles(conn)
        conn.close()
        data['user_data'] = user_data
        data['roles_data'] = role_data
        print(data)
        return render_template("admin/dashboard.html", data=data, current_user=data['user_data']['username'][0])
    return redirect(url_for('login'))


# Update method : update the  role and password when click on update button
@app.route('/admin/update/<int:id>', methods=['GET', 'POST'])
def update_user_role_password(id):
    if 'username' in session:
        if request.method == 'POST':
            role_id = request.form['role_id']
            password = request.form['password']
            print("UpdateUser: ", id, password, role_id)
            conn = create_connection()
            update_user(conn, id, password, role_id)
            session['role_id'] = role_id
            conn.close()
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('admin_dashboard'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    current_user = None;
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # print("LoginInfo: ", username, password)
        # Connect to database
        conn = create_connection()
        user = get_user_by_credentials(conn, username, password)
        conn.close()
        # print((user)) user: [(1, 'username', 'password', role_id)]
        if user:
            session['username'] = user[0][1]  # Store username in session
            session['role_id'] = user[0][3]  # Store role_id in session
            if session['role_id'] == 1:
                flash('You were successfully logged in')
                return redirect(url_for('admin_dashboard'))
            else:
                print(f"Username: {session['username']} and Role_ID: {session['role_id']} ")
                return redirect(url_for('user_dashboard'))  # No need to pass data in redirect
        else:
            flash('Invalid username or password! Please try again...')
            error = "Invalid username or password"  # More informative error message
    else:
        if 'username' in session:
            return redirect(url_for('index'))

    return render_template('frontend/login.html', current_user=None)


# Admin login method:
# Machine ID search from machine_data table by using machine_id and role_id
@app.route('/search', methods=['GET', 'POST'])
def search_machine():
    if request.method == 'POST':
        machine_id = request.form['machine_id']
        role_id = session['role_id']
        print("Input Machine ID: ", machine_id, role_id)
        conn = create_connection()
        search_data = get_machine_data_by_machine_id_role_id(conn, machine_id, role_id)
        print("ResultDB:", search_data)
        conn.close()
        if search_data['machine_id']:
            return render_template('user/search_results.html', machine_data=search_data,
                                   current_user=session['username'])
        else:
            return render_template('user/search_results.html', machine_data=None, current_user=session['username'])
    return render_template('user/searchbox.html')


@app.route('/custom_post', methods=['GET', 'POST'])
def custom_post():
    if 'username' in session:
        role_id = session['role_id']
        conn = create_connection()
        machine_data = get_test_machine_data(conn, role_id)
        return render_template('user/test_post_dashboard.html', current_user=session['username'],
                               roles_data=session['role_id'], m_data=machine_data)
    return redirect(url_for('login'))


@app.route('/test_post_search', methods=['POST'])
def test_post_search():
    if 'username' in session:
        role_id = session['role_id']
        search_key = request.form.get('machine_id')
        print("Input Machine ID: ", search_key, role_id)
        conn = create_connection()
        machine_data = get_test_machine_data_by_filter(conn, f"{search_key}")
        return render_template('user/test_search_results.html', current_user=session['username'],
                               roles_data=session['role_id'], machine_data=machine_data)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role_id', None)
    flash('You were successfully logged out')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.secret_key = '123456'
    app.run(port=RUN_PORT, debug=DEBUG)
