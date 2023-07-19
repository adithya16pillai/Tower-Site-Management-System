from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'towermanagement'

# Establish the database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="tower_management"
)

# Create a cursor object to execute SQL queries
cursor = db.cursor()

# Create a dictionary to serve as the query cache
query_cache = {}

# Function to authenticate the username and password
def authenticate_user(username, password):
    # Retrieve owner_id from OwnerINFO table for the given username
    query = "SELECT owner_id FROM OwnerINFO WHERE owner_name = %s"
    values = (username,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result:
        owner_id = result[0]
        # Retrieve password from Credentials table for the retrieved owner_id
        query = "SELECT password FROM Credentials WHERE owner_id = %s"
        values = (owner_id,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result and result[0] == password:
            return owner_id
    return None
#

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        owner_id = authenticate_user(username, password)
        if owner_id:
            # Authentication successful, redirect to the homepage
            return redirect(url_for('index'))
        else:
            # Authentication failed, display error message
            flash('Invalid username or password', 'error')
    # Render the login form
    return render_template('login.html')
#

# Function to execute a query and store the result in the cache
def execute_query(query, values=None):
    cache_key = hash(query + str(values))
    if cache_key in query_cache:
        result = query_cache[cache_key]
        print("Query result retrieved from cache.")
    else:
        cursor.execute(query, values)
        result = cursor.fetchone()
        query_cache[cache_key] = result
        print("Query executed and result stored in cache.")
    return result
#

# Route to execute a query
@app.route('/execute_query', methods=['GET', 'POST'])
def execute_query_route():
    if request.method == 'POST':
        query = request.form.get('query')
        result = execute_query(query)
        return render_template('query.html', result=result)
    return render_template('query.html')
#
    
# Function to execute a query and store the result in the cache
def execute_query(query, values=None):
    cache_key = hash(query + str(values))
    if cache_key in query_cache:
        result = query_cache[cache_key]
        print("Query result retrieved from cache.")
    else:
        cursor.execute(query, values)
        result = cursor.fetchone()
        query_cache[cache_key] = result
        print("Query executed and result stored in cache.")
    return result
#

# Function to clear the query cache
def clear_query_cache():
    query_cache.clear()
    print("Query cache cleared.")
#

# Route to execute a query
@app.route('/execute_query', methods=['GET', 'POST'])
def execute_query_route():
    if request.method == 'POST':
        query = request.form.get('query')
        result = execute_query(query)
        return render_template('query.html', result=result)
    return render_template('query.html')
#

# Route to clear the query cache
@app.route('/clear_query_cache', methods=['POST'])
def clear_query_cache_route():
    clear_query_cache()
    message = "Query cache cleared successfully."
    return render_template('clear_cache.html', message=message)
#

# Function to execute a query and store the result in the cache
def execute_query(query, values=None):
    cache_key = hash(query + str(values))
    if cache_key in query_cache:
        result = query_cache[cache_key]
        print("Query result retrieved from cache.")
    else:
        cursor.execute(query, values)
        result = cursor.fetchone()
        query_cache[cache_key] = result
        print("Query executed and result stored in cache.")
    return result
#

# Function to get the owner ID for a given username
def get_owner_id(username):
    query = "SELECT owner_id FROM OwnerINFO WHERE owner_name = %s"
    values = (username,)
    result = execute_query(query, values)
    if result:
        return result[0]
    else:
        return 1
#

# Route to get the owner ID
@app.route('/get_owner_id', methods=['GET', 'POST'])
def get_owner_id_route():
    if request.method == 'POST':
        username = request.form.get('username')
        owner_id = get_owner_id(username)
        return render_template('get_owner_id.html', owner_id=owner_id)
    return render_template('get_owner_id.html')
#

# Function to execute a query and store the result in the cache
def execute_query(query, values=None):
    cursor.execute(query, values)
    result = cursor.fetchone()
    return result
#

# Function to add a new tower record
def tower_add():
    tower_id = request.form.get('tower_id')
    tower_height = request.form.get('tower_height')
    date_of_installation = request.form.get('date_of_installation')
    operator_name = request.form.get('operator_name')
    antenna_band = request.form.get('antenna_band')

    query = "INSERT INTO TowerINFO (tower_id, tower_height, date_of_installation, operator_name, antenna_band) " \
            "VALUES (%s, %s, %s, %s, %s)"
    values = (tower_id, tower_height, date_of_installation, operator_name, antenna_band)
    execute_query(query, values)
    db.commit()
    return "Tower record added successfully!"
#

# Route to render the tower_add.html template
@app.route('/tower_add', methods=['GET'])
def render_tower_add():
    return render_template('tower_add.html')
#

# Route to handle the tower_add form submission
@app.route('/tower_add', methods=['POST'])
def handle_tower_add():
    return tower_add()
#

# Function to execute a query and store the result in the cache
def execute_query(query, values=None):
    cursor.execute(query, values)
    result = cursor.fetchone()
    return result
#

# Function to update a tower record based on tower ID and username
def update_tower(tower_id, username, column_choice, new_value):
    query = "SELECT operator_name FROM TowerINFO WHERE tower_id = %s"
    values = (tower_id,)
    result = execute_query(query, values)
    if result and result[0] == username:
        query = f"UPDATE TowerINFO SET {column_choice} = %s WHERE tower_id = %s"
        values = (new_value, tower_id)
        execute_query(query, values)
        db.commit()
        return "Tower record updated successfully!"
    else:
        return "You do not have permission to update the tower record."
#

# Route to render the update_tower.html template
@app.route('/update_tower', methods=['GET'])
def render_update_tower():
    return render_template('update_tower.html')
#

# Route to handle the update_tower form submission
@app.route('/update_tower', methods=['POST'])
def handle_update_tower():
    tower_id = request.form.get('tower_id')
    username = request.form.get('username')
    column_choice = request.form.get('column_choice')
    new_value = request.form.get('new_value')
    result = update_tower(tower_id, username, column_choice, new_value)
    return result
#

# Function to execute a query and store the result in the cache
def execute_query(query, values=None):
    cursor.execute(query, values)
    result = cursor.fetchone()
    return result
#

# Function to delete a tower record based on tower ID
def tower_delete(tower_id, username):
    query = "SELECT operator_name FROM TowerINFO WHERE tower_id = %s"
    values = (tower_id,)
    result = execute_query(query, values)
    if result and result[0] == username:
        query = "DELETE FROM TowerINFO WHERE tower_id = %s"
        values = (tower_id,)
        execute_query(query, values)
        db.commit()
        return "Tower record deleted successfully!"
    else:
        return "You do not have permission to delete the tower record."
#

# Route to render the tower_delete.html template
@app.route('/tower_delete', methods=['GET'])
def render_tower_delete():
    return render_template('tower_delete.html')
#

# Route to handle the tower_delete form submission
@app.route('/tower_delete', methods=['POST'])
def handle_tower_delete():
    tower_id = request.form.get('tower_id')
    username = request.form.get('username')
    result = tower_delete(tower_id, username)
    return result
#

# Function to execute a query and store the result in the cache
def execute_query(query, values=None):
    cursor.execute(query, values)
    result = cursor.fetchall()
    return result
#

# Function to search for a tower record
def search_tower_by_id(tower_id):
    query = "SELECT * FROM TowerINFO WHERE tower_id = %s"
    values = (tower_id,)
    result = execute_query(query, values)
    return result
#

def search_tower_by_column(column_name, column_value):
    query = "SELECT * FROM TowerINFO WHERE {0} = %s".format(column_name)
    values = (column_value,)
    result = execute_query(query, values)
    return result
#

# Route to render the search_tower.html template
@app.route('/search_tower', methods=['GET'])
def render_search_tower():
    return render_template('search_tower.html')
#

# Route to handle the search_tower form submission
@app.route('/search_tower', methods=['POST'])
def handle_search_tower():
    search_type = request.form.get('search_type')
    
    if search_type == 'tower_id':
        tower_id = request.form.get('tower_id')
        result = search_tower_by_id(tower_id)
    elif search_type == 'column_value':
        column_name = request.form.get('column_name')
        column_value = request.form.get('column_value')
        result = search_tower_by_column(column_name, column_value)
    else:
        result = []
    
    if len(result) > 0:
        return "Tower record(s) found: {}".format(result)
    else:
        return "Tower record(s) not found."
#

# Function to execute a query and store the result in the cache
def execute_query(query, values=None):
    cursor.execute(query, values)
    result = cursor.fetchall()
    return result
#

# Route to render the antenna_add.html template
@app.route('/antenna_add', methods=['GET'])
def render_antenna_add():
    return render_template('antenna_add.html')
#

# Route to handle the antenna_add form submission
@app.route('/antenna_add', methods=['POST'])
def handle_antenna_add():
    antenna_id = request.form.get('antenna_id')
    antenna_size = request.form.get('antenna_size')
    bandwidth = request.form.get('bandwidth')
    network_generation = request.form.get('network_generation')
    antenna_height = request.form.get('antenna_height')
    antenna_azimuth = request.form.get('antenna_azimuth')

    query = "INSERT INTO AntennaINFO (antenna_id, antenna_size, bandwidth, network_generation, antenna_height, antenna_azimuth) " \
            "VALUES (%s, %s, %s, %s, %s, %s)"
    values = (antenna_id, antenna_size, bandwidth, network_generation, antenna_height, antenna_azimuth)
    execute_query(query, values)
    db.commit()
    print("Antenna record added successfully!")

    # Redirect to a success page or perform any other necessary action
    return "Antenna record added successfully!"
#

# Function to execute a query and store the result in the cache
def execute_query(query, values=None):
    cursor.execute(query, values)
    result = cursor.fetchall()
    return result
#

# Route to render the update_antenna.html template
@app.route('/update_antenna', methods=['GET'])
def render_update_antenna():
    return render_template('update_antenna.html')
#

# Route to handle the update_antenna form submission
@app.route('/update_antenna', methods=['POST'])
def handle_update_antenna():
    antenna_id = request.form.get('antenna_id')
    userid = request.form.get('userid')
    column_choice = request.form.get('column_choice')
    new_value = request.form.get('new_value')

    # Check if the owner_id matches the userid
    query = "SELECT owner_id FROM AntennaINFO WHERE antenna_id = %s"
    values = (antenna_id,)
    result = execute_query(query, values)  # Use the execute_query function to execute the query
    if result and result[0] == userid:
        query = "UPDATE AntennaINFO SET {0} = %s WHERE antenna_id = %s".format(column_choice)
        values = (new_value, antenna_id)
        result = execute_query(query, values)  # Use the execute_query function to execute the query
        db.commit()
        print("Antenna record updated successfully!")
    else:
        print("You do not have permission to update the antenna record.")

    # Redirect to a success page or perform any other necessary action
    return "Antenna record updated successfully!"
#

# Function to execute a query and store the result in the cache
def execute_query(query, values=None):
    cursor.execute(query, values)
    result = cursor.fetchall()
    return result
#

# Route to render the delete_antenna.html template
@app.route('/delete_antenna', methods=['GET'])
def render_delete_antenna():
    return render_template('delete_antenna.html')
#

# Route to handle the delete_antenna form submission
@app.route('/delete_antenna', methods=['POST'])
def handle_delete_antenna():
    antenna_id = request.form.get('antenna_id')
    userid = request.form.get('userid')
    option = request.form.get('option')

    if option == 'delete_row':
        query = "DELETE FROM AntennaINFO WHERE antenna_id = %s"
        values = (antenna_id,)
    elif option == 'delete_column':
        column_choice = request.form.get('column_choice')
        query = "UPDATE AntennaINFO SET {0} = NULL WHERE antenna_id = %s".format(column_choice)
        values = (antenna_id,)
    else:
        print("Invalid option. No changes made.")
        return

    result = execute_query(query, values)  # Use the execute_query function to execute the query
    db.commit()
    print("Antenna record deleted successfully!")

    # Redirect to a success page or perform any other necessary action
    return "Antenna record deleted successfully!"
#

# Function to execute a query and store the result in the cache
def execute_query(query, values=None):
    cursor.execute(query, values)
    result = cursor.fetchall()
    return result
#

# Route to render the search_antenna.html template
@app.route('/search_antenna', methods=['GET'])
def render_search_antenna():
    return render_template('search_antenna.html')
#

# Route to handle the search_antenna form submission
@app.route('/search_antenna', methods=['POST'])
def handle_search_antenna():
    search_option = request.form.get('search_option')

    if search_option == 'by_antenna_id':
        antenna_id = request.form.get('antenna_id')
        query = "SELECT * FROM AntennaINFO WHERE antenna_id = %s"
        values = (antenna_id,)
    elif search_option == 'by_column_value':
        column = request.form.get('column')
        value = request.form.get('value')
        query = "SELECT * FROM AntennaINFO WHERE {0} = %s".format(column)
        values = (value,)
    else:
        print("Invalid search option.")
        return

    result = execute_query(query, values)  # Use the execute_query function to execute the query

    if len(result) > 0:
        print("Antenna record(s) found:")
        for row in result:
            print(row)
    else:
        print("Antenna record(s) not found.")

    # Redirect to a success page or perform any other necessary action
    return "Antenna record(s) found!"
#

# Function to execute a query and store the result in the cache
def execute_query(query, values=None):
    cursor.execute(query, values)
    result = cursor.fetchall()
    return result
#

# Route to render the site_add.html template
@app.route('/site_add', methods=['GET'])
def render_site_add():
    return render_template('site_add.html')
#

# Route to handle the site_add form submission
@app.route('/site_add', methods=['POST'])
def handle_site_add():
    site_id = request.form.get('site_id')
    site_name = request.form.get('site_name')
    site_coordinates = request.form.get('site_coordinates')
    site_address = request.form.get('site_address')
    site_zip_code = request.form.get('site_zip_code')
    site_type = request.form.get('site_type')

    query = "INSERT INTO SiteINFO (site_id, site_name, site_coordinates, site_address, site_zip_code, site_type) " \
            "VALUES (%s, %s, %s, %s, %s, %s)"
    values = (site_id, site_name, site_coordinates, site_address, site_zip_code, site_type)
    result = execute_query(query, values)  # Use the execute_query function to execute the query
    db.commit()
    print("Site record added successfully!")

    # Redirect to a success page or perform any other necessary action
    return "Site record added successfully!"
#

# Function to execute a query and store the result in the cache
def execute_query(query, values=None):
    cursor.execute(query, values)
    result = cursor.fetchall()
    return result
#

# Route to render the update_site.html template
@app.route('/update_site', methods=['GET'])
def render_update_site():
    return render_template('update_site.html')
#

# Route to handle the update_site form submission
@app.route('/update_site', methods=['POST'])
def handle_update_site():
    site_id = request.form.get('site_id')
    user_id = request.form.get('user_id')
    new_site_name = request.form.get('new_site_name')

    # Check if the owner_id matches the userid
    query = "SELECT owner_id FROM SiteINFO WHERE site_id = %s"
    values = (site_id,)
    result = execute_query(query, values)  # Use the execute_query function to execute the query
    if result and result[0] == user_id:
        query = "UPDATE SiteINFO SET site_name = %s WHERE site_id = %s"
        values = (new_site_name, site_id)
        result = execute_query(query, values)  # Use the execute_query function to execute the query
        db.commit()
        print("Site record updated successfully!")
        return "Site record updated successfully!"
    else:
        print("You do not have permission to update the site record.")
        return "You do not have permission to update the site record."
#


# Route to render the delete_site.html template
@app.route('/delete_site', methods=['GET'])
def render_delete_site():
    return render_template('delete_site.html')
#

# Route to handle the delete_site form submission
@app.route('/delete_site', methods=['POST'])
def handle_delete_site():
    site_id = request.form.get('site_id')
    user_id = request.form.get('user_id')

    # Check if the owner_id matches the userid
    query = "SELECT owner_id FROM SiteINFO WHERE site_id = %s"
    values = (site_id,)
    result = execute_query(query, values)  # Use the execute_query function to execute the query
    if result and result[0] == user_id:
        query = "UPDATE SiteINFO SET owner_id = NULL WHERE site_id = %s"
        values = (site_id,)
        result = execute_query(query, values)  # Use the execute_query function to execute the query
        db.commit()
        print("Owner ID value in Site record deleted successfully!")
        return "Owner ID value in Site record deleted successfully!"
    else:
        print("You do not have permission to delete the owner ID value in the site record.")
        return "You do not have permission to delete the owner ID value in the site record."
#

# Function to execute a query and store the result in the cache
def execute_query(query, values=None):
    cursor.execute(query, values)
    result = cursor.fetchall()
    return result
#

# Route to render the search_site.html template
@app.route('/search_site', methods=['GET'])
def render_search_site():
    return render_template('search_site.html')
#

# Route to handle the search_site form submission
@app.route('/search_site', methods=['POST'])
def handle_search_site():
    choice = int(request.form.get('choice'))

    if choice == 1:
        site_id = request.form.get('site_id')
        query = "SELECT * FROM SiteINFO WHERE site_id = %s"
        values = (site_id,)
        result = execute_query(query, values)  # Use the execute_query function to execute the query
    elif choice == 2:
        column = request.form.get('column')
        value = request.form.get('value')
        query = "SELECT * FROM SiteINFO WHERE {0} = %s".format(column)
        values = (value,)
        result = execute_query(query, values)  # Use the execute_query function to execute the query
    else:
        print("Invalid choice.")
        return

    if len(result) > 0:
        print("Site record(s) found:")
        for row in result:
            print(row)
    else:
        print("Site record(s) not found.")

    return "Site record(s) found."
#

# Function to execute a query and store the result in the cache
def execute_query(query, values=None):
    cursor.execute(query, values)
    result = cursor.fetchall()
    return result
#

# Route to render the owner_add.html template
@app.route('/owner_add', methods=['GET'])
def render_owner_add():
    return render_template('owner_add.html')
#

# Route to handle the owner_add form submission
@app.route('/owner_add', methods=['POST'])
def handle_owner_add():
    owner_id = request.form.get('owner_id')
    owner_name = request.form.get('owner_name')
    sites_owned = request.form.get('sites_owned')
    towers_owned = request.form.get('towers_owned')
    owner_contact = request.form.get('owner_contact')

    query = "INSERT INTO OwnerINFO (owner_id, owner_name, sites_owned, towers_owned, owner_contact) " \
            "VALUES (%s, %s, %s, %s, %s)"
    values = (owner_id, owner_name, sites_owned, towers_owned, owner_contact)
    execute_query(query, values)  # Use the execute_query function to execute the query
    db.commit()
    print("Owner record added successfully!")

    return "Owner record added successfully!"
#

# Function to execute a query and store the result in the cache
def execute_query(query, values=None):
    cursor.execute(query, values)
    result = cursor.fetchall()
    return result
#

# Route to render the update_owner.html template
@app.route('/update_owner', methods=['GET'])
def render_update_owner():
    return render_template('update_owner.html')
#

# Route to handle the update_owner form submission
@app.route('/update_owner', methods=['POST'])
def handle_update_owner():
    owner_id = request.form.get('owner_id')
    userid = request.form.get('userid')
    new_owner_contact = request.form.get('new_owner_contact')

    # Check if the owner_id matches the userid
    query = "SELECT owner_id FROM OwnerINFO WHERE owner_id = %s"
    values = (owner_id,)
    result = execute_query(query, values)  # Use the execute_query function to execute the query
    if result and result[0] == userid:
        query = "UPDATE OwnerINFO SET owner_contact = %s WHERE owner_id = %s"
        values = (new_owner_contact, owner_id)
        execute_query(query, values)  # Use the execute_query function to execute the query
        db.commit()
        print("Owner record updated successfully!")
    else:
        print("You do not have permission to update the owner record.")

    return "Owner record updated successfully!"
#

# Function to execute a query and store the result in the cache
def execute_query(query, values=None):
    cursor.execute(query, values)
    result = cursor.fetchall()
    return result
#

# Route to render the delete_owner.html template
@app.route('/delete_owner', methods=['GET'])
def render_delete_owner():
    return render_template('delete_owner.html')
#

# Route to handle the delete_owner form submission
@app.route('/delete_owner', methods=['POST'])
def handle_delete_owner():
    owner_id = request.form.get('owner_id')
    username = request.form.get('username')

    # Check if the owner_name matches the username
    query = "SELECT owner_name FROM OwnerINFO WHERE owner_id = %s"
    values = (owner_id,)
    result = execute_query(query, values)  # Use the execute_query function to execute the query
    if result and result[0] == username:
        query = "UPDATE OwnerINFO SET owner_contact = NULL WHERE owner_id = %s"
        values = (owner_id,)
        execute_query(query, values)  # Use the execute_query function to execute the query
        db.commit()
        print("Contact number in Owner record deleted successfully!")
    else:
        print("You do not have permission to delete the contact number in the owner record.")

    return "Contact number in Owner record deleted successfully!"
#

# Function to execute a query and store the result in the cache
def execute_query(query, values=None):
    cursor.execute(query, values)
    result = cursor.fetchall()
    return result
#

# Route to render the search_owner.html template
@app.route('/search_owner', methods=['GET'])
def render_search_owner():
    return render_template('search_owner.html')
#

# Route to handle the search_owner form submission
@app.route('/search_owner', methods=['POST'])
def handle_search_owner():
    choice = request.form.get('choice')

    if choice == '1':
        owner_id = request.form.get('owner_id')
        query = "SELECT * FROM OwnerINFO WHERE owner_id = %s"
        values = (owner_id,)
        result = execute_query(query, values)  # Use the execute_query function to execute the query
    elif choice == '2':
        column = request.form.get('column')
        value = request.form.get('value')
        query = "SELECT * FROM OwnerINFO WHERE {0} = %s".format(column)
        values = (value,)
        result = execute_query(query, values)  # Use the execute_query function to execute the query
    else:
        print("Invalid choice.")
        return

    if len(result) > 0:
        print("Owner record(s) found:")
        for row in result:
            print(row)
    else:
        print("Owner record(s) not found.")

    return "Owner record(s) found."
#

# Function to execute a query and store the result in the cache
def execute_query(query, values=None):
    cursor.execute(query, values)
    result = cursor.fetchall()
    return result
#

# Route to render the maintenance_add.html template
@app.route('/maintenance_add', methods=['GET'])
def render_maintenance_add():
    return render_template('maintenance_add.html')
#

# Route to handle the maintenance_add form submission
@app.route('/maintenance_add', methods=['POST'])
def handle_maintenance_add():
    tower_id = request.form.get('tower_id')
    last_maintained = request.form.get('last_maintained')
    next_maintenance = request.form.get('next_maintenance')
    maintenance_type = request.form.get('maintenance_type')

    query = "INSERT INTO MaintainanceINFO (tower_id, last_maintained, next_maintenance, maintainance_type) " \
            "VALUES (%s, %s, %s, %s)"
    values = (tower_id, last_maintained, next_maintenance, maintenance_type)
    result = execute_query(query, values)  # Use the execute_query function to execute the query
    db.commit()
    print("Maintenance record added successfully!")

    return "Maintenance record added successfully!"
#

# Function to execute a query and store the result in the cache
def execute_query(query, values=None):
    cursor.execute(query, values)
    result = cursor.fetchall()
    return result
#

# Route to render the update_maintenance.html template
@app.route('/update_maintenance', methods=['GET'])
def render_update_maintenance():
    return render_template('update_maintenance.html')
#

# Route to handle the update_maintenance form submission
@app.route('/update_maintenance', methods=['POST'])
def handle_update_maintenance():
    tower_id = request.form.get('tower_id')
    username = request.form.get('username')
    choice = request.form.get('choice')
    new_value = request.form.get('new_value')

    # Check if the owner_name matches the username
    query = "SELECT owner_name FROM TowerINFO WHERE tower_id = %s"
    values = (tower_id,)
    result = execute_query(query, values)  # Use the execute_query function to execute the query
    if result and result[0] == username:
        if choice == "1":
            query = "UPDATE MaintainanceINFO SET last_maintained = %s WHERE tower_id = %s"
        elif choice == "2":
            query = "UPDATE MaintainanceINFO SET next_maintenance = %s WHERE tower_id = %s"
        elif choice == "3":
            query = "UPDATE MaintainanceINFO SET maintenance_type = %s WHERE tower_id = %s"
        else:
            print("Invalid choice. No changes made.")
            return

        values = (new_value, tower_id)
        result = execute_query(query, values)  # Use the execute_query function to execute the query
        db.commit()
        print("Maintenance record updated successfully!")
    else:
        print("You do not have permission to update the maintenance record.")

    return "Maintenance record updated successfully!"
#

# Function to execute a query and store the result in the cache
def execute_query(query, values=None):
    cursor.execute(query, values)
    result = cursor.fetchall()
    return result
#

# Route to render the maintenance_delete.html template
@app.route('/maintenance_delete', methods=['GET'])
def render_maintenance_delete():
    return render_template('maintenance_delete.html')
#

# Route to handle the maintenance_delete form submission
@app.route('/maintenance_delete', methods=['POST'])
def handle_maintenance_delete():
    tower_id = request.form.get('tower_id')

    query = "DELETE FROM MaintainanceINFO WHERE tower_id = %s"
    values = (tower_id,)
    result = execute_query(query, values)  # Use the execute_query function to execute the query
    db.commit()
    print("Maintenance record deleted successfully!")

    return "Maintenance record deleted successfully!"
#

# Function to execute a query and store the result in the cache
def execute_query(query, values=None):
    cursor.execute(query, values)
    result = cursor.fetchall()
    return result
#

# Route to render the search_maintenance.html template
@app.route('/search_maintenance', methods=['GET'])
def render_search_maintenance():
    return render_template('search_maintenance.html')
#

# Route to handle the search_maintenance form submission
@app.route('/search_maintenance', methods=['POST'])
def handle_search_maintenance():
    choice = int(request.form.get('choice'))

    if choice == 1:
        tower_id = request.form.get('tower_id')
        query = "SELECT * FROM MaintainanceINFO WHERE tower_id = %s"
        values = (tower_id,)
    elif choice == 2:
        column_name = request.form.get('column_name')
        column_value = request.form.get('column_value')
        query = "SELECT * FROM MaintainanceINFO WHERE {0} = %s".format(column_name)
        values = (column_value,)
    else:
        print("Invalid choice.")
        return

    result = execute_query(query, values)  # Use the execute_query function to execute the query

    if len(result) > 0:
        print("Maintenance record(s) found:")
        for row in result:
            print(row)
    else:
        print("Maintenance record(s) not found.")

    return "Maintenance record(s) found."
#

# Function to display the main menu
def display_menu():
    print("Welcome to the Database Management System!")
    print("Select a function to execute:")
    print("1. Add Record")
    print("2. Update Record")
    print("3. Delete Record")
    print("4. Search Record")
    print("0. Exit")

# Function to get the user's choice
def get_choice():
    while True:
        choice = input("Enter your choice: ")
        if choice.isdigit():
            choice = int(choice)
            if choice in range(5):
                return choice
        print("Invalid choice. Please try again.")

# Function to execute the selected function
def execute_function(choice):
    if choice == 1:
        add_record()
    elif choice == 2:
        update_record()
    elif choice == 3:
        delete_record()
    elif choice == 4:
        search_record()
    elif choice == 0:
        exit_program()
    else:
        print("Invalid choice.")

# Function to handle adding a record
def add_record():
    print("Select where to add the record")
    print("1. Tower INFO")
    print("2. Antenna INFO")
    print("3. Site INFO")
    print("4. Owner INFO")
    print("5. Maintaince INFO")
    table_choice = get_choice()
    
    if table_choice == 1:
        tower_add()
    elif table_choice == 2:
        antenna_add()
    elif table_choice == 3:
        site_add()
    elif table_choice == 4:
        owner_add()
    elif table_choice == 5:
        maintainance_add()
    else:
        print("Invalid choice.")


# Function to handle updating a record
def update_record():
    print("Select a table to update a record in:")
    print("1. TowerINFO")
    print("2. AntennaINFO")
    print("3. SiteINFO")
    print("4. OwnerINFO")
    print("5. MaintenanceINFO")
    table_choice = get_choice()
    
    if table_choice == 1:
        tower_id = input("Enter Tower ID: ")
        update_tower(tower_id, username)
    elif table_choice == 2:
        antenna_id = input("Enter Antenna ID: ")
        update_antenna(antenna_id, userid)
    elif table_choice == 3:
        print("Only site name can be updated")
        site_id = input("Enter Site ID: ")
        update_site(site_id, userid)
    elif table_choice == 4:
        owner_id = input("Enter Owner ID: ")
        update_owner(owner_id, userid)
    elif table_choice == 5:
        tower_id = input("Enter Tower ID: ")
        update_maintainance(tower_id, username)
    else:
        print("Invalid choice.")

# Function to handle deleting a record
def delete_record():
    print("Select a table to delete a record from:")
    print("1. TowerINFO")
    print("2. AntennaINFO")
    print("3. SiteINFO")
    print("4. OwnerINFO")
    print("5. MaintenanceINFO")
    table_choice = get_choice()
    
    if table_choice == 1:
        tower_id = input("Enter Tower ID: ")
        tower_delete(tower_id,username)
    elif table_choice == 2:
        antenna_id = input("Enter Antenna ID: ")
        delete_antenna(antenna_id, userid)
    elif table_choice == 3:
        site_id = input("Enter Site ID: ")
        delete_site(site_id, userid)
    elif table_choice == 4:
        print("Can only delete owner contact")
        owner_id = input("Enter Owner ID: ")
        delete_owner(owner_id, username)
    elif table_choice == 5:
        tower_id = input("Enter Tower ID: ")
        maintenance_delete(tower_id)
    else:
        print("Invalid choice.")

# Function to handle searching for a record
def search_record():
    print("Select a table to search for a record in:")
    print("1. TowerINFO")
    print("2. AntennaINFO")
    print("3. SiteINFO")
    print("4. OwnerINFO")
    print("5. MaintenanceINFO")
    table_choice = get_choice()
    
    if table_choice == 1:
        search_tower()
    elif table_choice == 2:
        search_antenna()
    elif table_choice == 3:
        search_site()
    elif table_choice == 4:
        search_owner()
    elif table_choice == 5:
        search_maintenance()
    else:
        print("Invalid choice.")

# Function to exit the program
def exit_program():
    print("Exiting the program...")
    db.close()
    sys.exit()

username= input("Enter Username")
max_attempts=3
attempts = 0
authenticated = False
while attempts < max_attempts:
    password = input("Enter Password")
    userid = authenticate_user(username, password)
    if userid is not None:
        authenticated = True
        print("Authentication successful!")
        break
    else: 
        attempts +=1
        print("Wrong password. Please try again.")

if not authenticated:
    print("Maximum login attempts exceeded. Exiting...")
    exit_program()


while True: 
    display_menu()
    choice = get_choice()
    execute_function(choice)

    cursor.close()
    db.close()

close_connection()

if __name__ == '__main__':
    app.run()
