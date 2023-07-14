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


def get_owner_id(username):
    query = "SELECT owner_id FROM OwnerINFO WHERE owner_name = %s"
    values = (username,)
    cursor.execute(query, values)
    result = cursor.fetchone()
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
    cursor.execute(query, values)
    db.commit()
    print("Tower record added successfully!")

# Function to update a tower record based on tower ID and username
def update_tower(tower_id, username):
    # Check if the owner_name matches the username
    query = "SELECT operator_name FROM TowerINFO WHERE tower_id = %s"
    values = (tower_id,)
    cursor.execute(query, values)
    result = cursor.fetchone()
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

        cursor.execute(query, values)
        db.commit()
        print("Tower record updated successfully!")
    else:
        print("You do not have permission to update the tower record.")

# Function to delete a tower record based on tower ID
def tower_delete(tower_id):
    query = "SELECT operator_name FROM TowerINFO WHERE tower_id = %s"
    values = (tower_id,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result and result[0] == username:

        print("Select an option:")
        print("1. Delete the whole row")
        print("2. Delete a specific column value")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            query = "DELETE FROM TowerINFO WHERE tower_id = %s"
            values = (tower_id,)
            cursor.execute(query, values)
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
            cursor.execute(query, values)
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
        cursor.execute(query, values)
    elif choice == 2:
        column = input("Enter Column Name: ")
        value = input("Enter Value: ")
        query = "SELECT * FROM TowerINFO WHERE {0} = %s".format(column)
        values = (value,)
        cursor.execute(query, values)
    else:
        print("Invalid choice.")
        return

    result = cursor.fetchall()
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
    cursor.execute(query, values)
    db.commit()
    print("Antenna record added successfully!")


def update_antenna(antenna_id, userid):
    # Check if the owner_name matches the userid
    query = "SELECT owner_id FROM AntennaINFO WHERE antenna_id = %s"
    values = (antenna_id,)
    cursor.execute(query, values)
    result = cursor.fetchone()
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

        cursor.execute(query, values)
        db.commit()
        print("Antenna record updated successfully!")
    else:
        print("You do not have permission to update the antenna record.")



# Function to delete an antenna record based on antenna ID and userid
def delete_antenna(antenna_id, userid):
    # Check if the owner_id matches the userid
    query = "SELECT owner_id FROM AntennaINFO WHERE antenna_id = %s"
    values = (antenna_id,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result and result[0] == userid:
        print("Select an option:")
        print("1. Delete the whole row")
        print("2. Delete a specific column value")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            query = "DELETE FROM AntennaINFO WHERE antenna_id = %s"
            values = (antenna_id,)
            cursor.execute(query, values)
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
            cursor.execute(query, values)
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
        cursor.execute(query, values)
    elif choice == 2:
        column = input("Enter Column Name: ")
        value = input("Enter Value: ")
        query = "SELECT * FROM AntennaINFO WHERE {0} = %s".format(column)
        values = (value,)
        cursor.execute(query, values)
    else:
        print("Invalid choice.")
        return

    result = cursor.fetchall()
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
    cursor.execute(query, values)
    db.commit()
    print("Site record added successfully!")



# Function to update the SiteINFO table based on site ID and userid
def update_site(site_id, userid):
    # Check if the owner_id matches the userid
    query = "SELECT owner_id FROM SiteINFO WHERE site_id = %s"
    values = (site_id,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result and result[0] == userid:
        new_site_name = input("Enter new site name: ")
        query = "UPDATE SiteINFO SET site_name = %s WHERE site_id = %s"
        values = (new_site_name, site_id)
        cursor.execute(query, values)
        db.commit()
        print("Site record updated successfully!")
    else:
        print("You do not have permission to update the site record.")

# Function to delete the owner_id value in a site record based on site ID and userid
def delete_site(site_id, username):
    # Check if the owner_id matches the userid
    query = "SELECT owner_id FROM SiteINFO WHERE site_id = %s"
    values = (site_id,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result and result[0] == userid:
        query = "UPDATE SiteINFO SET owner_id = NULL WHERE site_id = %s"
        values = (site_id,)
        cursor.execute(query, values)
        db.commit()
        print("Owner ID value in Site record deleted successfully!")
    else:
        print("You do not have permission to delete the owner ID value in the site record.")


def search_site():
    print("Select an option:")
    print("1. Search by Site ID")
    print("2. Search by Column Value")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        site_id = input("Enter Site ID: ")
        query = "SELECT * FROM SiteINFO WHERE site_id = %s"
        values = (site_id,)
        cursor.execute(query, values)
    elif choice == 2:
        column = input("Enter Column Name: ")
        value = input("Enter Value: ")
        query = "SELECT * FROM SiteINFO WHERE {0} = %s".format(column)
        values = (value,)
        cursor.execute(query, values)
    else:
        print("Invalid choice.")
        return

    result = cursor.fetchall()
    if len(result) > 0:
        print("Site record(s) found:")
        for row in result:
            print(row)
    else:
        print("Site record(s) not found.")









def owner_add():
    owner_id = input("Enter owner ID: ")
    owner_name = input("Enter owner name: ")
    sites_owned = input("Enter number of sites owned: ")
    towers_owned = input("Enter number of towers owned: ")
    owner_contact = input("Enter owner contact: ")

    query = "INSERT INTO OwnerINFO (owner_id, owner_name, sites_owned, towers_owned, owner_contact) " \
            "VALUES (%s, %s, %s, %s, %s)"
    values = (owner_id, owner_name, sites_owned, towers_owned, owner_contact)
    cursor.execute(query, values)
    db.commit()
    print("Owner record added successfully!")


# Function to update the OwnerINFO table based on owner ID and userid
def update_owner(owner_id, userid):
    # Check if the owner_name matches the userid
    query = "SELECT owner_id FROM OwnerINFO WHERE owner_id = %s"
    values = (owner_id,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result and result[0] == userid:
        new_owner_contact = input("Enter new owner contact number: ")
        query = "UPDATE OwnerINFO SET owner_contact = %s WHERE owner_id = %s"
        values = (new_owner_contact, owner_id)
        cursor.execute(query, values)
        db.commit()
        print("Owner record updated successfully!")
    else:
        print("You do not have permission to update the owner record.")



# Function to delete the contact number in an owner record based on owner ID and userid
def delete_owner(owner_id, userid):
    # Check if the owner_name matches the userid
    query = "SELECT owner_name FROM OwnerINFO WHERE owner_id = %s"
    values = (owner_id,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result and result[0] == userid:
        query = "UPDATE OwnerINFO SET owner_contact = NULL WHERE owner_id = %s"
        values = (owner_id,)
        cursor.execute(query, values)
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
        cursor.execute(query, values)
    elif choice == 2:
        column = input("Enter Column Name: ")
        value = input("Enter Value: ")
        query = "SELECT * FROM OwnerINFO WHERE {0} = %s".format(column)
        values = (value,)
        cursor.execute(query, values)
    else:
        print("Invalid choice.")
        return

    result = cursor.fetchall()
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
    cursor.execute(query, values)
    db.commit()
    print("Maintenance record added successfully!")


# Function to update the MaintainanceINFO table based on tower ID and username
def update_maintainance(tower_id, username):
    # Check if the owner_name matches the username
    query = "SELECT owner_name FROM TowerINFO WHERE tower_id = %s"
    values = (tower_id,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result and result[0] == username:
        print("Select a column to update:")
        print("1. Last Maintained")
        print("2. Next Maintainance")
        print("3. Maintainance Type")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            new_last_maintained = input("Enter new last maintained date (YYYY-MM-DD): ")
            query = "UPDATE MaintainanceINFO SET last_maintained = %s WHERE tower_id = %s"
            values = (new_last_maintained, tower_id)
        elif choice == 2:
            new_next_maintainance = input("Enter new next maintainance date (YYYY-MM-DD): ")
            query = "UPDATE MaintainanceINFO SET next_maintainance = %s WHERE tower_id = %s"
            values = (new_next_maintainance, tower_id)
        elif choice == 3:
            new_maintainance_type = input("Enter new maintainance type: ")
            query = "UPDATE MaintainanceINFO SET maintainance_type = %s WHERE tower_id = %s"
            values = (new_maintainance_type, tower_id)
        else:
            print("Invalid choice. No changes made.")
            return

        cursor.execute(query, values)
        db.commit()
        print("Maintainance record updated successfully!")
    else:
        print("You do not have permission to update the maintainance record.")



# Function to delete a maintenance record based on tower ID
def maintenance_delete(tower_id):
    query = "DELETE FROM MaintainanceINFO WHERE tower_id = %s"
    values = (tower_id,)
    cursor.execute(query, values)
    db.commit()
    print("Maintenance record deleted successfully!")

def search_maintenance():
    print("Select an option:")
    print("1. Search by Tower ID")
    print("2. Search by Column Value")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        tower_id = input("Enter Tower ID: ")
        query = "SELECT * FROM MaintainanceINFO WHERE tower_id = %s"
        values = (tower_id,)
        cursor.execute(query, values)
    elif choice == 2:
        column = input("Enter Column Name: ")
        value = input("Enter Value: ")
        query = "SELECT * FROM MaintainanceINFO WHERE {0} = %s".format(column)
        values = (value,)
        cursor.execute(query, values)
    else:
        print("Invalid choice.")
        return

    result = cursor.fetchall()
    if len(result) > 0:
        print("Maintenance record(s) found:")
        for row in result:
            print(row)
    else:
        print("Maintenance record(s) not found.")





username= input("Enter Username")
password = input("Enter password")
userid = get_owner_id(username)

if userid != 1:
    pass
else: 
    print("INVALID USERNAME")
    exit()






















# Close the database connection
def close_connection():
    cursor.close()
    db.close()


# Example usage
update_tower(1, 50.5)  # Update tower with ID 1 to a new height of 50.5
delete_tower(2)  # Delete tower with ID 2
search_tower(3)  # Search for tower with ID 3

# Close the database connection
close_connection()
