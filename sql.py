import sqlite3

# connect to sqlite
connection = sqlite3.connect("student.db")

# create a cursor object to insert record, create table, retrieve
cursor = connection.cursor()

# create the table
table_info = """
Create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT);
"""

cursor.execute(table_info)

# Insert some more records

cursor.execute('''Insert Into STUDENT values('Krish','Data science','A',90)''')
cursor.execute('''Insert Into STUDENT values('Sudhanshu','Data science','B',100)''')
cursor.execute('''Insert Into STUDENT values('Darius','Data science','A',86)''')
cursor.execute('''Insert Into STUDENT values('Viksah','DEVOPS','A',50)''')
cursor.execute('''Insert Into STUDENT values('Dipesh','DEVOPS','A',35)''')

# Display all the records
print("the inserted records")

data = cursor.execute('''select * From STUDENT''')

for row in data:
    print(row)

# close the connection
connection.commit()
connection.close()