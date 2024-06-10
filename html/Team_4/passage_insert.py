#!/usr/bin/env python3
import cgitb
import cgi
import pymysql

cgitb.enable()
print("Content-type: text/html\n")


# add this in the passage form html
#<form action="/cgi-bin/students_24/Team_4/passage_insert.py" method="post">
 #   <!-- Form fields as previously defined -->
  #  <button type="submit">Submit</button>
#</form>


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
        m_id = form.getvalue('m_id')  # Assuming m_id corresponds to 'name' dropdown
        l_id = form.getvalue('l_id')  # Assuming l_id corresponds to 'genotype' dropdown
        bc_number = form.getvalue('bc-number')
        ib_number = form.getvalue('ib-number')
        hatch_date = form.getvalue('hatch_date')
        passage_date = form.getvalue('collection-date')
        next_passage = form.getvalue('next-passage')
        mating_line = form.getvalue('mating-line')
        
        sql = """
        INSERT INTO passage (
            l_id, m_id, bc, ib, hatch_date, passage_date, next_passage, mating_line
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s
        );
        """
        cursor.execute(sql, (l_id, m_id, bc_number, ib_number, hatch_date, passage_date, next_passage, mating_line))
        connection.commit()
        print("Data inserted successfully")
except Exception as e:
    print("Failed to insert data:", e)

# Close database connection
connection.close()