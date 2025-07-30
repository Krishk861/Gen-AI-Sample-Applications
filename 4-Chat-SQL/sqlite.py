import sqlite3

##Connect to sqllite
connection=sqlite3.connect("students.db")

## Create a cursor object ot insert record,create table
cursor=connection.cursor()

## Create the table
table_info="""
create table student(NAME Varchar(25),CLASS varchar(20),SECTION VARCHAR(32),MARKS INT)"""
cursor.execute(table_info)

## Insert some more records
cursor.execute('''insert into students values("Krish","Data Science","A",90)''')
cursor.execute('''insert into students values('John','Data Science','B',100)''')
cursor.execute('''insert into students values('Mukesh','Data Science','A',86)''')
cursor.execute('''insert into students values('Jacob','DEVOPS','A',50)''')
cursor.execute('''insert into students values('Dipesh','DEVOPS','A',35)''')

## Display all the records
print("The inerted records are")
data=cursor.execute('''Select * from Student''')
for row in data:
    print(row)

### Commit the  changes 
connection.commit()
connection.close()