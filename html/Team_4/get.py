#!/usr/bin/env python3
import cgi
import json
import pymysql

# Connect to the database
connection = pymysql.connect(
    host='bioed.bu.edu',
    user='astoicad',
    password='astoicad',
    db='Team_4',
    port=4253
)

# Defining the Queries
queries = {
    'line': '''
    SELECT yl_id, short_name, full_genotype, background, published,
        authors, creators, phenotype, phenotype_notes, genotype_notes,
        dna_avail, notes, maintenance
    FROM m_lines
    WHERE l_id = %s;    
    ''',

    'member': '''
    SELECT f_name, l_name, lab_role, active
    FROM lab_members
    WHERE m_id = %s;
    ''',

    'sort': '''
    SELECT hatch_date, sort_date, line_name, marker_color,
        marker_location, fl_ratio, fl_total, notes, l_id, m_id
    FROM sort
    WHERE sort_id = %s;
    ''',

    'pass': '''
    SELECT l_id, m_id, bc, ib, hatch_date, passage_date, next_passage,
        mating_line
    FROM passage
    WHERE pass_id = %s;
    ''',
    
    'clutch': '''
    SELECT l_id, m_id, hatch_date, collection_date, clutch_number,
        egg_papers
    FROM clutch
    WHERE clutch_id = %s;
    '''
    }

# Function to get sort data for a given sort_id from the database
def get_data(selector, id):
    # Parse id as integer
    id = int(id)
    try:
        with connection.cursor() as cursor:
            cursor.execute(queries[selector], (id,))
            result = cursor.fetchone()
            if result:
                if selector == 'line':
                   return {
                        "yl_id": result[0],
                        "short_name": result[1],
                        "full_genotype": result[2],
                        "background": result[3],
                        "published": result[4],
                        "authors": result[5],
                        "creators": result[6],
                        "phenotype": result[7],
                        "phenotype_notes": result[8],
                        "genotype_notes": result[9],
                        "dna_avail": result[10],
                        "notes": result[11],
                        "maintenance": result[12],
                    } 
                
                if selector == 'member':
                   return {
                        "f_name": result[0],
                        "l_name": result[1],
                        "lab_role": result[2],
                        "active": result[3]
                    } 
                
                if selector == "sort":
                    return {
                        "sort_hatch": result[0].isoformat(),
                        "sort_date": result[1].isoformat(),
                        "line_name": result[2],
                        "marker_color": result[3],
                        "marker_location": result[4],
                        "fl_ratio": float(result[5]),
                        "fl_total": int(result[6]),
                        "notes": result[7],
                        "sort_l_id": result[8],
                        "sort_m_id": result[9]
                    }
                
                if selector == "pass":
                    # Convert date fields to isoformat if they are not None
                    hatch_date = result[4].isoformat() if result[4] else None
                    passage_date = result[5].isoformat() if result[5] else None
                    next_passage = result[6].isoformat() if result[6] else None
                    
                    return {
                        "bc": result[2],
                        "ib": result[3],
                        "passage_hatch": hatch_date,
                        "passage_date": passage_date,
                        "next_passage": next_passage,
                        "mating_line": result[7],
                        "pass_l_id": result[0],
                        "pass_m_id": result[1]
                    }
                
                if selector == 'clutch':
                    hatch_date = result[2].isoformat() if result[2] else None
                    collection_date = result[3].isoformat() if result[3] else None
                    
                    return {
                        "clutch_l_id": result[0],
                        "clutch_m_id": result[1],
                        "clutch_hatch": hatch_date,
                        "collection_date": collection_date,
                        "clutch_number": result[4],
                        "egg_papers": result[5]
                    }
            else:
                return None
            
    except Exception as e:
        # Handle database errors
        print("Failed to fetch data:", e)
        return None


try:
    # connection = pymysql.connect(
    #     host='bioed.bu.edu',
    #     user='camv',
    #     password='camv',
    #     db='Team_4',
    #     port=4253
    # )
    # Set content type to JSON
    print("Content-type: application/json\n")
    
    # Get sort_id parameter from the query string
    form = cgi.FieldStorage()
    selector = form.getvalue('selector')
    id = form.getvalue('id')
    
    # Check if sort_id is not None and can be parsed as an integer
    if id is not None and id.isdigit():
        # Fetch the data for the given sort_id
        data = get_data(selector, id)
        
        # Prepare JSON response
        if data:
            print(json.dumps(data))
        else:
            print(json.dumps({"error": "Data not found for id {}".format(id)}))
    else:
        print(json.dumps({"error": "Invalid id: {}".format(id)}))

except pymysql.Error as e:
    print(json.dumps({'error': str(e)}))
    exit()

finally:
    # Close the database connection
    if 'connection' in locals() and connection.open:
        connection.close()



