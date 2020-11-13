import socket
import threading
import time


from Data.Data import get_hash_Malisiosos_sql,validarLogin,validarRegistro,ingresarArchivoContamindo,getArchivos,getUsuarios
from GUI.GUI import showGUIServer



def gestor_Clientes():

    get_hash_Malisiosos_sql()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", 8000))
    server.listen(1)




    #hilo que atiende acepta a lo nuevo clientes
    while 1:

        d = threading.Thread(target=hiloValidacionActualizacion, name='Daemon')
        d.setDaemon(True)
        d.start()

        # Se espera a un cliente
        socket_cliente, datos_cliente = server.accept()
        print("conectado " + str(datos_cliente))
        seguir = True



        # hilo que atiende peticiones del cliente
        while seguir:
            # Espera por datos
            peticion = socket_cliente.recv(1000)

            # redistribuccion segun la peticion del cliente
            if ("" != peticion.decode()):
                print("Peticion del cliente: [" + peticion.decode() + "]");
            if ("PeticionListaHashMalisiosos" == peticion.decode()):
                socket_cliente.send(get_hash_Malisiosos_sql().encode())
            if ("login" == peticion.decode()):
                socket_cliente.send("aceptoPeticionLogin".encode())
                peticion = socket_cliente.recv(1000)
                if (validarLogin(peticion.decode())):
                    socket_cliente.send("aceptoLogin".encode())
                    # showGUIServer()
                else:
                    socket_cliente.send("DeniegoLogin".encode())
            if ("registrar" == peticion.decode()):
                socket_cliente.send("aceptoPeticionRegistrar".encode())
                peticion = socket_cliente.recv(1000)

                if (validarRegistro(peticion.decode())):
                    socket_cliente.send("aceptoRegistro".encode())

                else:
                    socket_cliente.send("DeniegoRegistro".encode())
            if ("nuevoArchivoContaminado" == peticion.decode()):
                socket_cliente.send("aceptoPeticion".encode())
                peticion = socket_cliente.recv(1000)

                if (ingresarArchivoContamindo(peticion.decode())):
                    socket_cliente.send("Exito!".encode())
                else:
                    socket_cliente.send("Error!".encode())

            time.sleep(1)

def hiloValidacionActualizacion():
    showGUIServer(getArchivos(),getUsuarios())




