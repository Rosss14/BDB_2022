import pymysql.cursors
import xml.etree.ElementTree as ET

# Establish a connection with MySQL databaseA
connection = pymysql.connect(host='localhost',
      user = 'root', password = '12345', db = 'isoforms',
      cursorclass = pymysql.cursors.DictCursor)

print('Connection succesful')

cursor = connection.cursor()

# Retrieve all the table names from the database
query = 'show tables from isoforms'

cursor.execute(query)

tables = cursor.fetchall()

# Generate XML
root = ET.Element('isoforms')

for table in tables:

    # Obtain the data from each table one per an iteration of the loop
    query = 'select * from '+ str(table['Tables_in_isoforms'])

    cursor.execute(query)

    results = cursor.fetchall()

    for row in results:  # Iterate through rows of the table
        entry = ET.Element(str(table['Tables_in_isoforms']))
        root.append(entry)
        for i in row:  # Iterate through columns and insert a label per column
            field = ET.SubElement(entry, str(i))
            field.text = str(row[i])

tree = ET.ElementTree(root)
with open('isoforms.xml', 'wb') as files:
    tree.write(files)

connection.close()
