#!/usr/bin/env python3
import cgitb
import cgi
import pymysql


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
        m_id = form.getvalue('name')  # Assuming m_id corresponds to 'name' dropdown
        l_id = form.getvalue('genotype')  # Assuming l_id corresponds to 'genotype' dropdown
        hatch_date = form.getvalue('hatch_date')
        collection_date = form.getvalue('collection-date')
        clutch_number = form.getvalue('clutch-number')
        egg_papers = form.getvalue('egg-papers')
        
        sql = """
        INSERT INTO clutch (
            m_id, l_id, hatch_date, collection_date, clutch_number, egg_papers
        ) VALUES (
            %s, %s, %s, %s, %s, %s
        );
        """
        cursor.execute(sql, (m_id, l_id, hatch_date, collection_date, clutch_number, egg_papers))
        connection.commit()
        print("Data inserted successfully")
except Exception as e:
    print("Failed to insert data:", e)

# Close database connection
connection.close()