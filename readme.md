# IoT Monitoring System Management Dashboard
This application is created based on the client requirements.
Few snapshots of the application <br>

![User Dashboard](https://github.com/princexoleo/iot_monitoring_system_admin_dashboard/blob/main/static/assets/img.png)

<br>

![Search Result](https://github.com/princexoleo/iot_monitoring_system_admin_dashboard/blob/main/static/assets/img_1.png)

<br>

![Add Machine](https://github.com/princexoleo/iot_monitoring_system_admin_dashboard/blob/main/static/assets/img_2.png)

<br>

![Test Post Dashboard](https://github.com/princexoleo/iot_monitoring_system_admin_dashboard/blob/main/static/assets/img_3.png)

<br>
## Key Features:
* Admin Dashboard
* User management system
* Multi vendor onboarding
* Add IoT machine 
* Control IoT MQTT devices

## Installation 
* blinker==1.8.2
* click==8.1.7
* colorama==0.4.6
* Flask==3.0.3
* itsdangerous==2.2.0
* Jinja2==3.1.4
* MarkupSafe==2.1.5
* psycopg2==2.9.9
* python-dotenv==1.0.1
* Werkzeug==3.0.3
* WTForms==3.1.2

## Database Scheme:
* Users
* ROles
* machine_info
* machine_data
* machine_data_test_post

## TODO:
* MQTT Subscriber codebase 
* MQTT Publish codebase
* MQTT to Database insertion features


# Database Schema Documentation

## Table 1: `users`
- **id**: `SERIAL PRIMARY KEY`
  - Unique identifier for each user.
- **username**: `VARCHAR(255) NOT NULL`
  - The username of the user, must be unique and not null.
- **password**: `VARCHAR(255) NULL`
  - The password of the user, can be null (in case of external authentication methods).
- **role_id**: `INTEGER`
  - Foreign key referencing the `id` column in the `roles` table.

## Table 2: `roles`
- **id**: `SERIAL PRIMARY KEY`
  - Unique identifier for each role.
- **role_names**: `VARCHAR(255)`
  - The name of the role, such as 'admin', 'user', etc.

## Table 3: `machine_info`
- **id**: `SERIAL PRIMARY KEY`
  - Unique identifier for each machine.
- **machine_name**: `VARCHAR(255)`
  - The name of the machine.
- **machine_alias**: `VARCHAR(255)`
  - An alias for the machine.
- **machine_location**: `VARCHAR(255)`
  - The location of the machine.
- **role_id**: `INTEGER`
  - Foreign key referencing the `id` column in the `roles` table.

## Table 4: `machine_data`
- **id**: `SERIAL PRIMARY KEY`
  - Unique identifier for each data entry.
- **machine_id**: `INTEGER`
  - Foreign key referencing the `id` column in the `machine_info` table.
- **battery_voltage**: `FLOAT`
  - The battery voltage of the machine.
- **current**: `FLOAT`
  - The current in the machine.
- **psp**: `FLOAT`
  - Pressure sensor parameter.
- **tr_temp**: `FLOAT`
  - Temperature of some component (transformer temperature).
- **ambient_temperature**: `FLOAT`
  - Ambient temperature where the machine is located.
- **created_time**: `TIMESTAMP`
  - The time when the data was recorded.
- **oil_level**: `FLOAT`
  - The oil level of the machine.

## Table 5: `machine_data_test_post`
- **id**: `SERIAL PRIMARY KEY`
  - Unique identifier for each test data entry.
- **machine_id**: `INTEGER`
  - Foreign key referencing the `id` column in the `machine_info` table.
- **battery_voltage**: `FLOAT`
  - The battery voltage of the machine.
- **psp**: `FLOAT`
  - Pressure sensor parameter.
- **ambient_temperature**: `FLOAT`
  - Ambient temperature where the machine is located.
- **created_at**: `TIMESTAMP DEFAULT CURRENT_TIMESTAMP`
  - The time when the test data was recorded, with a default value of the current timestamp.

## SQL Script

```sql
-- Create roles table
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    role_names VARCHAR(255)
);

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255),
    role_id INTEGER,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- Create machine_info table
CREATE TABLE machine_info (
    id SERIAL PRIMARY KEY,
    machine_name VARCHAR(255),
    machine_alias VARCHAR(255),
    machine_location VARCHAR(255),
    role_id INTEGER,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- Create machine_data table
CREATE TABLE machine_data (
    id SERIAL PRIMARY KEY,
    machine_id INTEGER,
    battery_voltage FLOAT,
    current FLOAT,
    psp FLOAT,
    tr_temp FLOAT,
    ambient_temperature FLOAT,
    created_time TIMESTAMP,
    oil_level FLOAT,
    FOREIGN KEY (machine_id) REFERENCES machine_info(id)
);

-- Create machine_data_test_post table
CREATE TABLE machine_data_test_post (
    id SERIAL PRIMARY KEY,
    machine_id INTEGER,
    battery_voltage FLOAT,
    psp FLOAT,
    ambient_temperature FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (machine_id) REFERENCES machine_info(id)
);
