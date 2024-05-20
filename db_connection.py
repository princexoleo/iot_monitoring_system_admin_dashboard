import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')


# Create a postgres database connection using psycopg2
def create_connection(debug=True):
    if debug:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        print("Connection established")
    else:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    return conn


# Create a user table in the postgres database containing username and password(null acceptable), role_id is a foriegn key from roles table
def create_user_table(con):
    try:
        cursor = conn.cursor()
        sql_query = '''
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY_KEY ,
        username VARCHAR(255), 
        password VARCHAR(255), 
        role_id INTEGER, FOREIGN KEY(role_id) REFERENCES roles(role_id))
        '''
        cursor.execute(sql_query)
        conn.commit()  # commit the changes
        print("Table created successfully")
        conn.close()
    except Exception as e:
        print(e)  # _


# Register user into databases
def add_user(conn, username):
    cursor = conn.cursor()
    sql_query = "INSERT INTO users (username) VALUES (%s)"
    cursor.execute(sql_query, (username,))
    conn.commit()

# Get data from users table
def get_users(con):
    cursor = con.cursor()
    sql_query = "SELECT * FROM users"
    cursor.execute(sql_query)
    users_data = cursor.fetchall()
    user_details = {
        'id': [],
        'username': [],
        'password': [],
        'role_id': []
    }
    if users_data:
        for data in users_data:
            user_details['id'].append(data[0])
            user_details['username'].append(data[1])
            user_details['password'].append(data[2])
            user_details['role_id'].append(data[3])

    return user_details


# Update user password and roles_id
def update_user(conn, user_id, password, role_id):
    cursor = conn.cursor()
    sql_query = "UPDATE users SET password = %s, role_id = %s WHERE id = %s"
    cursor.execute(sql_query, (password, role_id, user_id))
    # sql query commit.
    conn.commit()


# Get user by username and password matched:
def get_user_by_credentials(con, username, password):
    cursor = con.cursor()
    sql_query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(sql_query, (username, password))
    rows = cursor.fetchall()
    return rows

def get_user_by_username(conn, username):
    cursor = conn.cursor()
    sql_query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(sql_query, (username,))
    users_data = cursor.fetchall()
    return users_data

# Get data from roles table;
def get_roles(con):
    cursor = con.cursor()
    sql_query = "SELECT * FROM roles"
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    roles_data = {
        'id': [],
        'role_name': []
    }
    if rows:
        for data in rows:
            roles_data['id'].append(data[0])
            roles_data['role_name'].append(data[1])
    return roles_data


# Get roles data by role_id
def get_role_by_id(con, role_id):
    cursor = con.cursor()
    sql_query = "SELECT * FROM roles WHERE id = %s"
    cursor.execute(sql_query, (role_id,))
    rows = cursor.fetchall()
    role_data = {
        'id': [],
        'role_name': []
    }
    if rows:
        for data in rows:
            role_data['id'].append(data[0])
            role_data['role_name'].append(data[1])
    return role_data


def get_machine_data_by_role_id(conn, role_id):
    cursor = conn.cursor()
    sql_query = "SELECT * FROM machine_data WHERE role_id = %s"
    cursor.execute(sql_query, (role_id,))
    rows = cursor.fetchall()
    m_data = {
        'machine_id': [],
        'tr_1': [],
        'tr_2': [],
        'tr_3': [],
        'tr_4': [],
        'tr_5': [],
        'created_at': []
    }
    if rows:
        for data in rows:
            m_data['machine_id'].append(data[0])
            m_data['tr_1'].append(data[2])
            m_data['tr_2'].append(data[3])
            m_data['tr_3'].append(data[4])
            m_data['tr_4'].append(data[5])
            m_data['tr_5'].append(data[6])
            m_data['created_at'].append(data[7])
    return rows


def get_machine_data_by_machine_id_role_id(conn, search_key, role_id):
    cursor = conn.cursor()
    sql_query = '''SELECT m1.machine_id, m1.battery_voltage, m1.current, m1.ambient_temperature, m1.psp, m1.tr_temp, m1.oil_level, m1.created_time, m2.machine_name, m2.machine_alias, m2.machine_location
    FROM machine_data AS m1
    JOIN machine_info AS m2 ON m1.machine_id = m2.id
    WHERE m2.machine_name LIKE %s OR m2.machine_alias LIKE %s OR m2.machine_location LIKE %s
       OR m1.machine_id::text LIKE %s and m2.role_id = %s
       ORDER BY m1.created_time DESC
    '''
    cursor.execute(sql_query, (search_key, search_key, search_key, search_key, role_id))
    rows = cursor.fetchall()
    print(rows)
    fetch_data = {
        'machine_id': [],
        'battery_voltage': [],
        'current': [],
        'ambient_temperature': [],
        'psp': [],
        'tr_temp': [],
        'oil_level': [],
        'machine_name': [],
        'machine_alias': [],
        'machine_location': [],
        'created_time': []
    }
    if rows:
        for data in rows:
            fetch_data['machine_id'].append(data[0])
            fetch_data['battery_voltage'].append(data[1])
            fetch_data['current'].append(data[2])
            fetch_data['ambient_temperature'].append(data[3])
            fetch_data['psp'].append(data[4])
            fetch_data['tr_temp'].append(data[5])
            fetch_data['oil_level'].append(data[6])
            fetch_data['created_time'].append(data[7])
            fetch_data['machine_name'].append(data[8])
            fetch_data['machine_alias'].append(data[9])
            fetch_data['machine_location'].append(data[10])
    return fetch_data


def get_test_machine_data(conn, role_id, table_type="test_post"):
    cursor = conn.cursor()
    if table_type == "test_post":
        sql_query = '''SELECT m1.machine_id, m1.battery_voltage, m1.ambient_temperature, m1.psp, m2.machine_name, m2.machine_alias, m2.machine_location
                        FROM machine_data_test_post AS m1
                        JOIN machine_info AS m2 ON m1.machine_id = m2.id
                        WHERE m2.role_id = %s'''
        cursor.execute(sql_query, (role_id,))
        rows = cursor.fetchall()
        print(rows)
        fetch_data = {
            'machine_id': [],
            'battery_voltage': [],
            'ambient_temperature': [],
            'psp': [],
            'machine_name': [],
            'machine_alias': [],
            'machine_location': []
        }
        if rows:
            for data in rows:
                fetch_data['machine_id'].append(data[0])
                fetch_data['battery_voltage'].append(data[1])
                fetch_data['ambient_temperature'].append(data[2])
                fetch_data['psp'].append(data[3])
                fetch_data['machine_name'].append(data[4])
                fetch_data['machine_alias'].append(data[5])
                fetch_data['machine_location'].append(data[6])
        return fetch_data
    else:
        sql_query = '''SELECT m1.machine_id, m1.battery_voltage, m1.current ,m1.ambient_temperature, m1.psp, m1.tr_temp, m1.oil_level, m1.created_time, m2.machine_name, m2.machine_alias, m2.machine_location
                            FROM machine_data AS m1
                            JOIN machine_info AS m2 ON m1.machine_id = m2.id
                            WHERE m2.role_id = %s
                            ORDER BY m1.created_time DESC'''
        cursor.execute(sql_query, (role_id,))
        rows = cursor.fetchall()
        print(rows)
        fetch_data = {
            'machine_id': [],
            'battery_voltage': [],
            'current': [],
            'ambient_temperature': [],
            'psp': [],
            'tr_temp': [],
            'oil_level': [],
            'machine_name': [],
            'machine_alias': [],
            'machine_location': [],
            'created_time': []
        }
        if rows:
            for data in rows:
                fetch_data['machine_id'].append(data[0])
                fetch_data['battery_voltage'].append(data[1])
                fetch_data['current'].append(data[2])
                fetch_data['ambient_temperature'].append(data[3])
                fetch_data['psp'].append(data[4])
                fetch_data['tr_temp'].append(data[5])
                fetch_data['oil_level'].append(data[6])
                fetch_data['created_time'].append(data[7])
                fetch_data['machine_name'].append(data[8])
                fetch_data['machine_alias'].append(data[9])
                fetch_data['machine_location'].append(data[10])
        return fetch_data


def get_test_machine_data_by_filter(conn, search_word):
    cursor = conn.cursor()
    sql_query = ''' SELECT m1.machine_id, m1.battery_voltage, m1.ambient_temperature, m1.psp, 
       m2.machine_name, m2.machine_alias, m2.machine_location
    FROM machine_data_test_post AS m1
    JOIN machine_info AS m2 ON m1.machine_id = m2.id
    WHERE m2.machine_name LIKE %s OR m2.machine_alias LIKE %s OR m2.machine_location LIKE %s
       OR m1.machine_id::text LIKE %s
    '''
    cursor.execute(sql_query, (search_word, search_word, search_word, search_word))
    rows = cursor.fetchall()
    print(rows)
    fetch_data = {
        'machine_id': [],
        'battery_voltage': [],
        'ambient_temperature': [],
        'psp': [],
        'machine_name': [],
        'machine_alias': [],
        'machine_location': []
    }
    if rows:
        for data in rows:
            fetch_data['machine_id'].append(data[0])
            fetch_data['battery_voltage'].append(data[1])
            fetch_data['ambient_temperature'].append(data[2])
            fetch_data['psp'].append(data[3])
            fetch_data['machine_name'].append(data[4])
            fetch_data['machine_alias'].append(data[5])
            fetch_data['machine_location'].append(data[6])
    return fetch_data


def add_machine(conn, machine_id, location_name, alias_name, role_id):
    cursor = conn.cursor()
    sql_query = "INSERT INTO machine_info (machine_name, machine_location, machine_alias, role_id) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql_query, (machine_id, location_name, alias_name, role_id))
    conn.commit()

if __name__ == "__main__":
    print("For testing the db connection")
    conn = create_connection()
    machine_data = get_machine_data_by_machine_id_role_id(conn, 'mba', 2)
    print(machine_data)
    conn.close()
    print("Connection closed")