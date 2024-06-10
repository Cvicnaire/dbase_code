#!/usr/bin/env python3fff
import json
import pymysql
import cgi
import cgitb; cgitb.enable()

print("Content-type: application/json\n")

def db_connect():
    return pymysql.connect(host='bioed.bu.edu', user='bsd112', password='bsd112', db='bsd112', port=4253)

def fetch_lines():
    lines = []
    try:
        connection = db_connect()
        with connection.cursor() as cursor:
            cursor.execute("SELECT l_id, short_name FROM m_lines WHERE active = TRUE ORDER BY short_name")
            lines = [{'l_id': row[0], 'short_name': row[1]} for row in cursor.fetchall()]
    except pymysql.MySQLError as e:
        print(json.dumps({'error': str(e)}))
    finally:
        if connection:
            connection.close()
    return lines

if __name__ == '__main__':
    print(json.dumps(fetch_lines()))