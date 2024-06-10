#!/usr/bin/env python3

#Query the miRNA database through the browser using a cgi program

import pymysql
import cgi
import cgitb
#next is for packaging the output into json format
import json

#the next line is useful for debugging
#it causes errors during execution to be sent back to the browser
cgitb.enable()

# Defining the Queries
queries = {
    'master': '''
    SELECT
        ml.yl_id AS 'Line ID',
        ml.short_name AS 'Short Name',
        ml.full_genotype AS 'Full Genotype',
        p.bcib AS Generation,
        DATE_FORMAT(p.passage_date, '%Y-%m-%d') AS 'Passage Date',
        DATE_FORMAT(p.next_passage, '%Y-%m-%d') AS 'Next Passage',
        ml.background AS 'Background Strain',
        ml.phenotype AS Phenotype,
        ml.phenotype_notes AS 'Phenotype Notes',
        ml.maintenance AS Maintenance
    FROM
        m_lines ml
    LEFT JOIN (SELECT t1.l_id, CONCAT('BC', bc, ' ', 'IB', ib) AS bcib, passage_date, next_passage
        FROM passage t1
        INNER JOIN (
            SELECT l_id, MAX(passage_date) AS max_date
            FROM passage
            GROUP BY l_id
        ) t2 ON t1.l_id = t2.l_id AND t1.passage_date = t2.max_date) AS p ON ml.l_id = p.l_id
    WHERE maintenance = 'Active'
    GROUP BY yl_id 
    ORDER BY ml.yl_id;
    ''',

    'retired': '''
    SELECT
        ml.yl_id AS 'Line ID',
        ml.short_name AS 'Short Name',
        ml.full_genotype AS 'Full Genotype',
        p.bcib AS Generation,
        DATE_FORMAT(p.passage_date, '%Y-%m-%d') AS 'Passage Date',
        DATE_FORMAT(p.next_passage, '%Y-%m-%d') AS 'Next Passage',
        ml.background AS 'Background Strain',
        ml.phenotype AS Phenotype,
        ml.phenotype_notes AS 'Phenotype Notes',
        ml.maintenance AS Maintenance
    FROM
        m_lines ml
    LEFT JOIN (SELECT t1.l_id, CONCAT('BC', bc, ' ', 'IB', ib) AS bcib, passage_date, next_passage
        FROM passage t1
        INNER JOIN (
            SELECT l_id, MAX(passage_date) AS max_date
            FROM passage
            GROUP BY l_id
        ) t2 ON t1.l_id = t2.l_id AND t1.passage_date = t2.max_date) AS p ON ml.l_id = p.l_id
    WHERE maintenance = 'Retired'
    GROUP BY yl_id 
    ORDER BY ml.yl_id;
    ''',

    'full_line_info': '''
    SELECT
        ml.yl_id AS 'Line ID',
        ml.short_name AS 'Short Name',
        ml.full_genotype AS 'Full Genotype',
        p.bcib AS Generation,
        DATE_FORMAT(p.passage_date, '%Y-%m-%d') AS 'Passage Date',
        DATE_FORMAT(p.next_passage, '%Y-%m-%d') AS 'Next Passage',
        ml.background AS 'Background Strain',
        ml.published AS 'PubMed ID',
        ml.authors AS Authors,
        ml.creators AS 'Line Creators',
        ml.phenotype AS Phenotype,
        ml.phenotype_notes AS 'Phenotype Notes',
        ml.genotype_notes AS 'Genotype Notes',
        ml.dna_avail AS 'DNA Availability',
        ml.notes AS Notes,
        ml.maintenance AS Maintenance
    FROM
        m_lines ml
    LEFT JOIN (SELECT t1.l_id, CONCAT('BC', bc, ' ', 'IB', ib) AS bcib, passage_date, next_passage
        FROM passage t1
        INNER JOIN (
            SELECT l_id, MAX(passage_date) AS max_date
            FROM passage
            GROUP BY l_id
        ) t2 ON t1.l_id = t2.l_id AND t1.passage_date = t2.max_date) AS p ON ml.l_id = p.l_id
    GROUP BY yl_id 
    ORDER BY ml.yl_id;
    ''',

    'passage': '''
    SELECT 
        ml.yl_id AS ID, 
        ml.full_genotype AS Genotype, 
        DATE_FORMAT(p.passage_date, '%Y-%m-%d') AS 'Passage Date', 
        DATE_FORMAT(s.hatch_date, '%Y-%m-%d') AS 'Hatch Date', 
        DATE_FORMAT(s.sort_date, '%Y-%m-%d') AS 'Sort Date',
        p.bc AS 'Back Cross', 
        p.ib AS Inbreed, 
        s.fl_ratio AS 'Fluorescent Ratio', 
        c1.egg AS 'Egg Paper Score'
    FROM sort s
        LEFT OUTER JOIN passage p ON (s.l_id, s.hatch_date) = (p.l_id, p.hatch_date)
        JOIN m_lines ml ON ml.l_id = s.l_id
        LEFT JOIN (
            SELECT l_id, hatch_date, GROUP_CONCAT(egg_papers ORDER BY clutch_number SEPARATOR ', ') AS egg
            FROM clutch
            GROUP BY l_id, hatch_date
        ) AS c1 ON (c1.l_id, c1.hatch_date) = (s.l_id, s.hatch_date)

    UNION

    SELECT 
        ml.yl_id AS ID, 
        ml.full_genotype AS Genotype, 
        DATE_FORMAT(p.passage_date, '%Y-%m-%d') AS 'Passage Date', 
        DATE_FORMAT(p.hatch_date, '%Y-%m-%d') AS 'Hatch Date', 
        DATE_FORMAT(s.sort_date, '%Y-%m-%d') AS 'Sort Date',
        p.bc AS 'Back Cross', 
        p.ib AS Inbreed, 
        s.fl_ratio AS 'Fluorescent Ratio', 
        c2.egg AS 'Egg Paper Score'
    FROM sort s
        RIGHT OUTER JOIN passage p ON (s.l_id, s.hatch_date) = (p.l_id, p.hatch_date)
        JOIN m_lines ml ON ml.l_id = p.l_id
        LEFT JOIN (
            SELECT l_id, hatch_date, GROUP_CONCAT(egg_papers ORDER BY clutch_number SEPARATOR ', ') AS egg
            FROM clutch
            GROUP BY l_id, hatch_date
        ) AS c2 ON (c2.l_id, c2.hatch_date) = (p.l_id, p.hatch_date)
    WHERE s.l_id IS NULL
    ORDER BY ID, 'Hatch Date' DESC;
    ''',

    'simple_passage': '''
    SELECT 
        pass_id AS 'Passage ID',
        concat(f_name,' ',l_name) AS 'Lab Member',
        yl_id AS ID, 
        full_genotype AS Genotype, 
        DATE_FORMAT(hatch_date, '%Y-%m-%d') AS 'Hatch Date', 
        DATE_FORMAT(passage_date, '%Y-%m-%d') AS 'Passage Date', 
        bc AS 'Back Cross', 
        ib AS Inbreed, 
        mating_line AS 'Mating Line' 
    FROM 
        passage p 
    JOIN lab_members using(m_id)
    JOIN 
        m_lines ml USING (l_id);
    ''',

    'simple_clutch': '''
    SELECT 
        clutch_id AS 'Clutch ID',
        concat(f_name,' ', l_name) AS 'Lab Member',
        yl_id AS ID, 
        full_genotype AS Genotype, 
        DATE_FORMAT(hatch_date, '%Y-%m-%d') AS 'Hatch Date', 
        DATE_FORMAT(collection_date, '%Y-%m-%d') AS 'Collection Date', 
        clutch_number AS 'Clutch Number', 
        egg_papers AS 'Egg Papers' 
    FROM 
        clutch c 
    join 
        lab_members using(m_id)
    JOIN 
        m_lines ml USING (l_id);
    ''',

    'simple_sort': '''
    SELECT 
        sort_id AS 'Sort ID',
        concat(f_name, ' ',l_name) AS 'Lab Member',
        yl_id AS ID, 
        full_genotype AS Genotype, 
        DATE_FORMAT(hatch_date, '%Y-%m-%d') AS 'Hatch Date', 
        DATE_FORMAT(sort_date, '%Y-%m-%d') AS 'Sort Date',
        line_name AS 'Form Line Name', 
        marker_color AS 'Marker Color', 
        marker_location AS 'Marker Location',
        fl_ratio AS 'Fluorescent Ratio', 
        fl_total AS 'Fluorescent Total', 
        s.notes AS Notes
    FROM 
        sort s 
    JOIN 
        lab_members using(m_id)
    JOIN 
        m_lines ml USING (l_id);
    ''',

    'active_members': '''
    SELECT f_name AS 'First Name', l_name AS 'Last Name', lab_role AS 'Lab Role'
    FROM lab_members
    WHERE active = 'Active';
    ''',

    'inactive_members': '''
    SELECT f_name AS 'First Name', l_name AS 'Last Name', lab_role AS 'Lab Role'
    FROM lab_members
    WHERE active = 'Inactive';
    '''
}


#retrieve input data from the web server
form = cgi.FieldStorage() 

#next line is always required as first part of http output
print("Content-type: text/html\n")

if form:
    # Get submitted values
    selector = form.getvalue("selector")

    # Establish database connection
    try:
        connection = pymysql.connect(
            host='bioed.bu.edu',
            user='camv',
            password='camv',
            db='Team_4',
            port=4253
        )
    except pymysql.Error as e:
        print(json.dumps({'error': str(e)}))
        exit()

    cursor = connection.cursor()

    try:
        cursor.execute(queries[selector])
        results = cursor.fetchall()

        # Extract field names from cursor description
        field_names = [desc[0] for desc in cursor.description]

        # Prepare response data with field names and query results
        response_data = {'fields': field_names, 'data': results}
        print(json.dumps(response_data))
        
    except pymysql.Error as e:
        print(json.dumps({'error': str(e)}))

    finally:
        connection.close()

else:
    print(json.dumps({'error': 'No form data received.'}))