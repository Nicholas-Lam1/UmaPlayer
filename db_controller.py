import mariadb

# connection parameters
conn_params= {
    "user" : "root",
    "password" : "LilBunny<3",
    "host" : "NLPi.local",
    "database" : "NL_App"
}

# Establish a connection
connection= mariadb.connect(**conn_params)

cursor= connection.cursor()

# Populate countries table  with some data
cursor.execute("INSERT INTO Testing(ID, Last_Name, First_Name, Age) VALUES (?,?,?,?)", ("1", "Smith", "John", 30))
connection.commit()

# retrieve data
cursor.execute("SELECT ID, Last_Name, First_Name, Age FROM Testing")

# print content
row= cursor.fetchone()
print(*row, sep=' ')

# free resources
cursor.close()
connection.close()