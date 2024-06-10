#!/usr/bin/env python3
import cgitb
import cgi
import pymysql
import json


cgitb.enable()
print("Content-type: text/html\n")

# Connect to the database
connection = pymysql.connect(
    host='bioed.bu.edu',
    user='bsd112',  # Use your actual username
    password='bsd112',  # Use your actual password
    db='Team_4',  # Use your actual database name
    port=4253
)

# Parse form data
form = cgi.FieldStorage()

# Insert data
try:
    with connection.cursor() as cursor:
        m_id = form.getvalue('m_id')
        l_id = form.getvalue('l_id')
        hatch_date = form.getvalue('hatch_date')
        sort_date = form.getvalue('sort_date')
        marker_color = form.getvalue('marker_color', 'N/A')  # Default value as 'N/A' if not provided
        marker_location = form.getvalue('marker_location', 'N/A')  # Default value as 'N/A' if not provided
        fl_ratio = form.getvalue('fluorescencePercentage')
        fl_total = form.getvalue('totalFluorescent')
        notes = form.getvalue('notes')
        line_name = form.getvalue('l_id')
        
        sql = """
        INSERT INTO sort (
            m_id, l_id, hatch_date, sort_date, line_name, marker_color, 
            marker_location, fl_ratio, fl_total, notes
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        );
        """
        cursor.execute(sql, (m_id, l_id, hatch_date, sort_date, line_name, marker_color, marker_location, fl_ratio, fl_total, notes,))
        connection.commit()
        print("Data inserted successfully")
except Exception as e:
    print("Failed to insert data:", e)

# Close database connection
connection.close()