#!/usr/bin/env python3
import cgitb
import cgi
import pymysql

# add this in the new_user form html
#<form id="addUserForm" action="/cgi-bin/students_24/Team_4/add_user_insert.py" method="post">
#    <!-- Form fields as previously defined -->
#    <button type="submit">Submit</button>
#</form>


cgitb.enable()
print("Content-type: text/html\n")

# Connect to the database
connection = pymysql.connect(
    host='bioed.bu.edu',
    user='bsd112',  # Replace with your username
    password='bsd112',  # Replace with your password
    db='Team_4',  # Replace with your database name
    port=4253
)

# Parse form data
form = cgi.FieldStorage()

# Insert data
try:
    with connection.cursor() as cursor:
        f_name = form.getvalue('f_name')
        l_name = form.getvalue('l_name')
        role = form.getvalue('role')

        sql = """
        INSERT INTO lab_members (
            f_name, l_name, lab_role, active
        ) VALUES (
            %s, %s, %s, 'Active'
        );
        """
        cursor.execute(sql, (f_name, l_name, role))
        connection.commit()
        print("Data inserted successfully")
except Exception as e:
    print("Failed to insert data:", e)

# Close database connection
connection.close()