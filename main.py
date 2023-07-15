import mysql.connector

# Establish the database connection
db = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
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
    
# Function to clear the query cache
def clear_query_cache():
    query_cache.clear()
    print("Query cache cleared.")



# Function to get the owner ID for a given username
def get_owner_id(username):
    query = "SELECT owner_id FROM OwnerINFO WHERE owner_name = %s"
    values = (username,)
    result = execute_query(query, values)
    if result:
        return result[0]
    else:
        return 1


# Function to add a new tower record
def tower_add():
    tower_id = input("Enter tower ID: ")
    tower_height = input("Enter tower height: ")
    date_of_installation = input("Enter date of installation (YYYY-MM-DD): ")
    operator_name = input("Enter operator name: ")
    antenna_band = input("Enter antenna band: ")

    query = "INSERT INTO TowerINFO (tower_id, tower_height, date_of_installation, operator_name, antenna_band) " \
            "VALUES (%s, %s, %s, %s, %s)"
    values = (tower_id, tower_height, date_of_installation, operator_name, antenna_band)
    execute_query(query, values)
    db.commit()
    print("Tower record added successfully!")

# Function to update a tower record based on tower ID and username
def update_tower(tower_id, username):
    query = "SELECT operator_name FROM TowerINFO WHERE tower_id = %s"
    values = (tower_id,)
    result = execute_query(query, values)
    if result and result[0] == username:
        print("Select a column to update:")
        print("1. Tower Height")
        print("2. Date of Installation")
        print("3. Operator Name")
        print("4. Antenna Band")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            new_height = input("Enter new tower height: ")
            query = "UPDATE TowerINFO SET tower_height = %s WHERE tower_id = %s"
            values = (new_height, tower_id)
        elif choice == 2:
            new_installation_date = input("Enter new date of installation (YYYY-MM-DD): ")
            query = "UPDATE TowerINFO SET date_of_installation = %s WHERE tower_id = %s"
            values = (new_installation_date, tower_id)
        elif choice == 3:
            new_operator_name = input("Enter new operator name: ")
            query = "UPDATE TowerINFO SET operator_name = %s WHERE tower_id = %s"
            values = (new_operator_name, tower_id)
        elif choice == 4:
            new_antenna_band = input("Enter new antenna band: ")
            query = "UPDATE TowerINFO SET antenna_band = %s WHERE tower_id = %s"
            values = (new_antenna_band, tower_id)
        else:
            print("Invalid choice. No changes made.")
            return

        execute_query(query, values)
        db.commit()
        print("Tower record updated successfully!")
    else:
        print("You do not have permission to update the tower record.")

# Function to delete a tower record based on tower ID
def tower_delete(tower_id, username):
    query = "SELECT operator_name FROM TowerINFO WHERE tower_id = %s"
    values = (tower_id,)
    result = execute_query(query, values)  # Use the execute_query function to execute the query
    if result and result[0] == username:
        print("Select an option:")
        print("1. Delete the whole row")
        print("2. Delete a specific column value")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            query = "DELETE FROM TowerINFO WHERE tower_id = %s"
            values = (tower_id,)
            execute_query(query, values)  # Use the execute_query function to execute the query
            db.commit()
            print("Tower record deleted successfully!")
        elif choice == 2:
            print("Select a column to delete:")
            print("1. Tower Height")
            print("2. Date of Installation")
            print("3. Operator Name")
            print("4. Antenna Band")
            column_choice = int(input("Enter your choice: "))

            if column_choice == 1:
                query = "UPDATE TowerINFO SET tower_height = NULL WHERE tower_id = %s"
            elif column_choice == 2:
                query = "UPDATE TowerINFO SET date_of_installation = NULL WHERE tower_id = %s"
            elif column_choice == 3:
                query = "DELETE FROM TowerINFO WHERE tower_id = %s"
            elif column_choice == 4:
                query = "UPDATE TowerINFO SET antenna_band = NULL WHERE tower_id = %s"
            else:
                print("Invalid choice. No changes made.")
                return

            values = (tower_id,)
            execute_query(query, values)  # Use the execute_query function to execute the query
            db.commit()
            print("Tower record updated successfully!")
        else:
            print("Invalid choice. No changes made.")
    else:
        print("You do not have permission to update the tower record.")
def search_tower():
    print("Select an option:")
    print("1. Search by Tower ID")
    print("2. Search by Column Value")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        tower_id = input("Enter Tower ID: ")
        query = "SELECT * FROM TowerINFO WHERE tower_id = %s"
        values = (tower_id,)
        result = execute_query(query, values)  # Use the execute_query function to execute the query
    elif choice == 2:
        column = input("Enter Column Name: ")
        value = input("Enter Value: ")
        query = "SELECT * FROM TowerINFO WHERE {0} = %s".format(column)
        values = (value,)
        result = execute_query(query, values)  # Use the execute_query function to execute the query
    else:
        print("Invalid choice.")
        return

    if len(result) > 0:
        print("Tower record(s) found:")
        for row in result:
            print(row)
    else:
        print("Tower record(s) not found.")










# Function to add a new antenna record
def antenna_add():
    antenna_id = input("Enter antenna ID: ")
    antenna_size = input("Enter antenna size: ")
    bandwidth = input("Enter bandwidth: ")
    network_generation = input("Enter network generation: ")
    antenna_height = input("Enter antenna height: ")
    antenna_azimuth = input("Enter antenna azimuth: ")

    query = "INSERT INTO AntennaINFO (antenna_id, antenna_size, bandwidth, network_generation, antenna_height, antenna_azimuth) " \
            "VALUES (%s, %s, %s, %s, %s, %s)"
    values = (antenna_id, antenna_size, bandwidth, network_generation, antenna_height, antenna_azimuth)
    result = execute_query(query, values)  # Use the execute_query function to execute the query
    db.commit()
    print("Antenna record added successfully!")


# Function to update an antenna record based on antenna ID and userid
def update_antenna(antenna_id, userid):
    # Check if the owner_id matches the userid
    query = "SELECT owner_id FROM AntennaINFO WHERE antenna_id = %s"
    values = (antenna_id,)
    result = execute_query(query, values)  # Use the execute_query function to execute the query
    if result and result[0] == userid:
        print("Select a column to update:")
        print("1. Antenna Size")
        print("2. Bandwidth")
        print("3. Network Generation")
        print("4. Antenna Height")
        print("5. Antenna Azimuth")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            new_size = input("Enter new antenna size: ")
            query = "UPDATE AntennaINFO SET antenna_size = %s WHERE antenna_id = %s"
            values = (new_size, antenna_id)
        elif choice == 2:
            new_bandwidth = input("Enter new bandwidth: ")
            query = "UPDATE AntennaINFO SET bandwidth = %s WHERE antenna_id = %s"
            values = (new_bandwidth, antenna_id)
        elif choice == 3:
            new_network_generation = input("Enter new network generation: ")
            query = "UPDATE AntennaINFO SET network_generation = %s WHERE antenna_id = %s"
            values = (new_network_generation, antenna_id)
        elif choice == 4:
            new_height = input("Enter new antenna height: ")
            query = "UPDATE AntennaINFO SET antenna_height = %s WHERE antenna_id = %s"
            values = (new_height, antenna_id)
        elif choice == 5:
            new_azimuth = input("Enter new antenna azimuth: ")
            query = "UPDATE AntennaINFO SET antenna_azimuth = %s WHERE antenna_id = %s"
            values = (new_azimuth, antenna_id)
        else:
            print("Invalid choice. No changes made.")
            return

        result = execute_query(query, values)  # Use the execute_query function to execute the query
        db.commit()
        print("Antenna record updated successfully!")
    else:
        print("You do not have permission to update the antenna record.")


# Function to delete an antenna record based on antenna ID and userid
def delete_antenna(antenna_id, userid):
    # Check if the owner_id matches the userid
    query = "SELECT owner_id FROM AntennaINFO WHERE antenna_id = %s"
    values = (antenna_id,)
    result = execute_query(query, values)  # Use the execute_query function to execute the query
    if result and result[0] == userid:
        print("Select an option:")
        print("1. Delete the whole row")
        print("2. Delete a specific column value")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            query = "DELETE FROM AntennaINFO WHERE antenna_id = %s"
            values = (antenna_id,)
            result = execute_query(query, values)  # Use the execute_query function to execute the query
            db.commit()
            print("Antenna record deleted successfully!")
        elif choice == 2:
            print("Select a column to delete:")
            print("1. Antenna Size")
            print("2. Bandwidth")
            print("3. Network Generation")
            print("4. Antenna Height")
            print("5. Antenna Azimuth")
            column_choice = int(input("Enter your choice: "))

            if column_choice == 1:
                query = "UPDATE AntennaINFO SET antenna_size = NULL WHERE antenna_id = %s"
            elif column_choice == 2:
                query = "UPDATE AntennaINFO SET bandwidth = NULL WHERE antenna_id = %s"
            elif column_choice == 3:
                query = "UPDATE AntennaINFO SET network_generation = NULL WHERE antenna_id = %s"
            elif column_choice == 4:
                query = "UPDATE AntennaINFO SET antenna_height = NULL WHERE antenna_id = %s"
            elif column_choice == 5:
                query = "UPDATE AntennaINFO SET antenna_azimuth = NULL WHERE antenna_id = %s"
            else:
                print("Invalid choice. No changes made.")
                return

            values = (antenna_id,)
            result = execute_query(query, values)  # Use the execute_query function to execute the query
            db.commit()
            print("Antenna record updated successfully!")
        else:
            print("Invalid choice. No changes made.")
    else:
        print("You do not have permission to delete the antenna record.")


# Function to search for a record in AntennaINFO table
def search_antenna():
    print("Select an option:")
    print("1. Search by Antenna ID")
    print("2. Search by Column Value")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        antenna_id = input("Enter Antenna ID: ")
        query = "SELECT * FROM AntennaINFO WHERE antenna_id = %s"
        values = (antenna_id,)
        result = execute_query(query, values)  # Use the execute_query function to execute the query
    elif choice == 2:
        column = input("Enter Column Name: ")
        value = input("Enter Value: ")
        query = "SELECT * FROM AntennaINFO WHERE {0} = %s".format(column)
        values = (value,)
        result = execute_query(query, values)  # Use the execute_query function to execute the query
    else:
        print("Invalid choice.")
        return

    if len(result) > 0:
        print("Antenna record(s) found:")
        for row in result:
            print(row)
    else:
        print("Antenna record(s) not found.")





# Function to add a new site record
def site_add():
    site_id = input("Enter site ID: ")
    site_name = input("Enter site name: ")
    site_coordinates = input("Enter site coordinates: ")
    site_address = input("Enter site address: ")
    site_zip_code = input("Enter site zip code: ")
    site_type = input("Enter site type: ")

    query = "INSERT INTO SiteINFO (site_id, site_name, site_coordinates, site_address, site_zip_code, site_type) " \
            "VALUES (%s, %s, %s, %s, %s, %s)"
    values = (site_id, site_name, site_coordinates, site_address, site_zip_code, site_type)
    result = execute_query(query, values)  # Use the execute_query function to execute the query
    db.commit()
    print("Site record added successfully!")


# Function to update the SiteINFO table based on site ID and userid
def update_site(site_id, userid):
    # Check if the owner_id matches the userid
    query = "SELECT owner_id FROM SiteINFO WHERE site_id = %s"
    values = (site_id,)
    result = execute_query(query, values)  # Use the execute_query function to execute the query
    if result and result[0] == userid:
        new_site_name = input("Enter new site name: ")
        query = "UPDATE SiteINFO SET site_name = %s WHERE site_id = %s"
        values = (new_site_name, site_id)
        result = execute_query(query, values)  # Use the execute_query function to execute the query
        db.commit()
        print("Site record updated successfully!")
    else:
        print("You do not have permission to update the site record.")


# Function to delete the owner_id value in a site record based on site ID and userid
def delete_site(site_id, userid):
    # Check if the owner_id matches the userid
    query = "SELECT owner_id FROM SiteINFO WHERE site_id = %s"
    values = (site_id,)
    result = execute_query(query, values)  # Use the execute_query function to execute the query
    if result and result[0] == userid:
        query = "UPDATE SiteINFO SET owner_id = NULL WHERE site_id = %s"
        values = (site_id,)
        result = execute_query(query, values)  # Use the execute_query function to execute the query
        db.commit()
        print("Owner ID value in Site record deleted successfully!")
    else:
        print("You do not have permission to delete the owner ID value in the site record.")


# Function to search for a record in SiteINFO table
def search_site():
    print("Select an option:")
    print("1. Search by Site ID")
    print("2. Search by Column Value")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        site_id = input("Enter Site ID: ")
        query = "SELECT * FROM SiteINFO WHERE site_id = %s"
        values = (site_id,)
        result = execute_query(query, values)  # Use the execute_query function to execute the query
    elif choice == 2:
        column = input("Enter Column Name: ")
        value = input("Enter Value: ")
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




# Function to add a new owner record
def owner_add():
    owner_id = input("Enter owner ID: ")
    owner_name = input("Enter owner name: ")
    sites_owned = input("Enter number of sites owned: ")
    towers_owned = input("Enter number of towers owned: ")
    owner_contact = input("Enter owner contact: ")

    query = "INSERT INTO OwnerINFO (owner_id, owner_name, sites_owned, towers_owned, owner_contact) " \
            "VALUES (%s, %s, %s, %s, %s)"
    values = (owner_id, owner_name, sites_owned, towers_owned, owner_contact)
    result = execute_query(query, values)  # Use the execute_query function to execute the query
    db.commit()
    print("Owner record added successfully!")


# Function to update the OwnerINFO table based on owner ID and userid
def update_owner(owner_id, userid):
    # Check if the owner_id matches the userid
    query = "SELECT owner_id FROM OwnerINFO WHERE owner_id = %s"
    values = (owner_id,)
    result = execute_query(query, values)  # Use the execute_query function to execute the query
    if result and result[0] == userid:
        new_owner_contact = input("Enter new owner contact number: ")
        query = "UPDATE OwnerINFO SET owner_contact = %s WHERE owner_id = %s"
        values = (new_owner_contact, owner_id)
        result = execute_query(query, values)  # Use the execute_query function to execute the query
        db.commit()
        print("Owner record updated successfully!")
    else:
        print("You do not have permission to update the owner record.")


# Function to delete the contact number in an owner record based on owner ID and userid
def delete_owner(owner_id, username):
    # Check if the owner_name matches the username
    query = "SELECT owner_name FROM OwnerINFO WHERE owner_id = %s"
    values = (owner_id,)
    result = execute_query(query, values)  # Use the execute_query function to execute the query
    if result and result[0] == username:
        query = "UPDATE OwnerINFO SET owner_contact = NULL WHERE owner_id = %s"
        values = (owner_id,)
        result = execute_query(query, values)  # Use the execute_query function to execute the query
        db.commit()
        print("Contact number in Owner record deleted successfully!")
    else:
        print("You do not have permission to delete the contact number in the owner record.")


# Function to search for a record in OwnerINFO table
def search_owner():
    print("Select an option:")
    print("1. Search by Owner ID")
    print("2. Search by Column Value")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        owner_id = input("Enter Owner ID: ")
        query = "SELECT * FROM OwnerINFO WHERE owner_id = %s"
        values = (owner_id,)
        result = execute_query(query, values)  # Use the execute_query function to execute the query
    elif choice == 2:
        column = input("Enter Column Name: ")
        value = input("Enter Value: ")
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


# Function to add a new maintenance record
def maintenance_add():
    tower_id = input("Enter tower ID: ")
    last_maintained = input("Enter last maintenance date (YYYY-MM-DD): ")
    next_maintenance = input("Enter next maintenance date (YYYY-MM-DD): ")
    maintenance_type = input("Enter maintenance type: ")

    query = "INSERT INTO MaintainanceINFO (tower_id, last_maintained, next_maintenance, maintainance_type) " \
            "VALUES (%s, %s, %s, %s)"
    values = (tower_id, last_maintained, next_maintenance, maintenance_type)
    result = execute_query(query, values)  # Use the execute_query function to execute the query
    db.commit()
    print("Maintenance record added successfully!")


# Function to update the MaintainanceINFO table based on tower ID and username
def update_maintenance(tower_id, username):
    # Check if the owner_name matches the username
    query = "SELECT owner_name FROM TowerINFO WHERE tower_id = %s"
    values = (tower_id,)
    result = execute_query(query, values)  # Use the execute_query function to execute the query
    if result and result[0] == username:
        print("Select a column to update:")
        print("1. Last Maintained")
        print("2. Next Maintenance")
        print("3. Maintenance Type")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            new_last_maintained = input("Enter new last maintained date (YYYY-MM-DD): ")
            query = "UPDATE MaintainanceINFO SET last_maintained = %s WHERE tower_id = %s"
            values = (new_last_maintained, tower_id)
        elif choice == 2:
            new_next_maintenance = input("Enter new next maintenance date (YYYY-MM-DD): ")
            query = "UPDATE MaintainanceINFO SET next_maintenance = %s WHERE tower_id = %s"
            values = (new_next_maintenance, tower_id)
        elif choice == 3:
            new_maintenance_type = input("Enter new maintenance type: ")
            query = "UPDATE MaintainanceINFO SET maintenance_type = %s WHERE tower_id = %s"
            values = (new_maintenance_type, tower_id)
        else:
            print("Invalid choice. No changes made.")
            return

        result = execute_query(query, values)  # Use the execute_query function to execute the query
        db.commit()
        print("Maintenance record updated successfully!")
    else:
        print("You do not have permission to update the maintenance record.")


# Function to delete a maintenance record based on tower ID
def maintenance_delete(tower_id):
    query = "DELETE FROM MaintainanceINFO WHERE tower_id = %s"
    values = (tower_id,)
    result = execute_query(query, values)  # Use the execute_query function to execute the query
    db.commit()
    print("Maintenance record deleted successfully!")


# Function to search for a record in MaintainanceINFO table
def search_maintenance():
    print("Select an option:")
    print("1. Search by Tower ID")
    print("2. Search by Column Value")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        tower_id = input("Enter Tower ID: ")
        query = "SELECT * FROM MaintainanceINFO WHERE tower_id = %s"
        values = (tower_id,)
        result = execute_query(query, values)  # Use the execute_query function to execute the query
    elif choice == 2:
        column = input("Enter Column Name: ")
        value = input("Enter Value: ")
        query = "SELECT * FROM MaintainanceINFO WHERE {0} = %s".format(column)
        values = (value,)
        result = execute_query(query, values)  # Use the execute_query function to execute the query
    else:
        print("Invalid choice.")
        return

    if len(result) > 0:
        print("Maintenance record(s) found:")
        for row in result:
            print(row)
    else:
        print("Maintenance record(s) not found.")


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
