import pyodbc

con = pyodbc.connect(Trusted_Connection='yes', driver = '{SQL Server}',server = 'PC-EMI-JULI\SQLEXPRESS' , database = 'turnero')
print("exito")

cursor = con.cursor()
data = cursor.execute("Select * from Consultorios")
print(data.fetchall())