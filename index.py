import pymysql
miConexion = pymysql.connect(host="localhost",user="root",passwd="",database="bdpython")
print(miConexion)