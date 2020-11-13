import pymysql

#CONNECTION TO MySQL
_Mysql_server = "163.178.107.10"
_Mysql_database = "Antivirus_Proyecto_Redes2_LSJ"
_Mysql_server_port = 1433
_Mysql_user = "laboratorios"
_Mysql_password = "KmZpo.2796"


#MySQL  CONNECTION FUNCTION
def mysql_connection():
    try:
        cnx = pymysql.connect(_Mysql_server,_Mysql_user,_Mysql_password,_Mysql_database)
        return cnx
    except:
        print('ERROR: MSSQL_CONNECTION')

def registrarUsuario(nombre, contrasena):
    try:
        con = mysql_connection()
        cur = con.cursor()
        #AQUI HAY QUE HACER EL PROCEDURE PARA INSERTAR
        #cur.execute("EXECUTE {} ".format(sp))
        con.commit()
    except IOError as e:
        print("ERROR: [0] Register data from MYSQL[1]".format(e.errno, e .strerror))


def get_hash_Malisiosos_sql():
    try:
        con = mysql_connection()
        cur = con.cursor()
        query = " select * from  tb_ArchivosMalisiosos;".format(0)
        cur.execute(query)
        data_return = cur.fetchall()
        print("~~~~~~~~~~~~~~~~~~~~ Lista hash malisisos ~~~~~~~~~~~~~~~~~~")
        salida=""
        for row in data_return:
            print("ID: " + str(row[0]) + " - Hash: " + row[1]);
            salida=salida+row[1]+"~~ANTIVIRUS~~"
        con.close()
        return salida
    except IOError as e:
        print("ERROR: [0] Getting data from MYSQL: [1]".format(
            e.errno, e.strerror))

def validarLogin(cadena):
    credenciales = cadena.split("~~LOGIN~~")

    try:
        con = mysql_connection()
        cur = con.cursor()
        query = " select * from  tb_Usuarios;".format(0)
        cur.execute(query)
        data_return = cur.fetchall()
        print("~~~~~~~~~~~~~~~~~~~~ Lista usuarios  ~~~~~~~~~~~~~~~~~~")
        for row in data_return:
            print("Nombre: " + str(row[1]) + " - Contrasena: " + row[2]);
            if (str(row[1]) == credenciales[0] and str(row[2]) == credenciales[1] ):
                print("Si existe este usuario")
                return 1
        con.close()
        return 0
    except IOError as e:
        print("ERROR: [0] Getting data from MYSQL: [1]".format(
            e.errno, e.strerror))

def validarRegistro(cadena):

    # Valida que el usuario no exista anteriormente
    credenciales = cadena.split("~~REGISTRAR~~")
    validaciones =credenciales[0]+"~~LOGIN~~"+credenciales[1]

    if (validarLogin(validaciones)):
        return 0;
    try:
        con = mysql_connection()
        cur = con.cursor()
        query = "insert into tb_Usuarios (nombre,contrasena )values('"+ credenciales[0] + "','"+credenciales[1]+"');".format(0)
        cur.execute(query)
        con.commit()
        con.close()
        return validarLogin(validaciones)
    except IOError as e:
        print("ERROR: [0] Getting data from MYSQL: [1]".format(
            e.errno, e.strerror))

def ingresarArchivoContamindo(cadena):

    # Valida que el usuario no exista anteriormente
    aux = cadena.split("~~CONTAMINADO~~")

    try:
        con = mysql_connection()
        cur = con.cursor()
        query = "insert into tb_ArchivosMalisiosos (hashMalisioso,nombre)values('"+ aux[0] + "','"+aux[1]+"');".format(0)
        cur.execute(query)
        con.commit()
        con.close()
        return 1
    except IOError as e:
        print("ERROR: [0] Getting data from MYSQL: [1]".format(
            e.errno, e.strerror))
        return 0

def getArchivos():
    try:

        con = mysql_connection()
        cur = con.cursor()
        query = " select * from  tb_ArchivosMalisiosos;".format(0)
        cur.execute(query)
        data_return = cur.fetchall()
        print("~~~~~~~~~~~~~~~~~~~~ Lista hash malisisos ~~~~~~~~~~~~~~~~~~")
        salida=""
        for row in data_return:
            print("Hash: " + str(row[1]) + " - Archivo: " + row[2])
            salida=salida+"Hash: " + str(row[1]) + " - Archivo: " + row[2] + "|"
        con.close()
        return salida
    except IOError as e:
        print("ERROR: [0] Getting data from MYSQL: [1]".format(
            e.errno, e.strerror))

def getUsuarios():
    try:

        con = mysql_connection()
        cur = con.cursor()
        query = " select * from  tb_Usuarios;".format(0)
        cur.execute(query)
        data_return = cur.fetchall()
        print("~~~~~~~~~~~~~~~~~~~~ Lista hash malisisos ~~~~~~~~~~~~~~~~~~")
        salida=""
        for row in data_return:
            print("Usuario: " + str(row[1]) + " - Contrasena: " + row[2])
            salida=salida+"Usuario: " + str(row[1]) + " - Contrasena: " + row[2] + "|"
        con.close()
        return salida
    except IOError as e:
        print("ERROR: [0] Getting data from MYSQL: [1]".format(
            e.errno, e.strerror))














