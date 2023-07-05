# importing required libraries
import mysql.connector
  
def check(n,p):
    dataBase = mysql.connector.connect(host ="localhost",user ="root",passwd ="",database = "elms")
    # preparing a cursor object
    cursorObject = dataBase.cursor()
    # sql query
    sql = f'select * from StudentDetails where name=  "{n}" and password = {p}";'
    # executing the sql query
    cursorObject.execute(sql)
    # fetching the data
    myresult = cursorObject.fetchall()
    print(myresult)
    if len(myresult) == 0:
        dataBase.close()
        return False
    else:
        dataBase.close()
        return True


