import socket
import time

from GUI.GUI import showGUI,login,loginExitos,loginDenegado,RegistroDenegado,ResgistroExitos
from Dominio.ExamenMd5 import stringToList


def gestorConexionConServidor():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 8000))

    # s.send("PeticionListaHashMalisiosos".encode())
    # datos = s.recv(1000)
    # listaHashMalisiosos = stringToList(datos.decode())
    # showGUI(listaHashMalisiosos)

    Bit_login = 0
    while Bit_login !=1:
        usuario=login()
        credenciales = usuario.split("~~REGISTRAR~~")
        if(len(credenciales)==2):
            s.send("registrar".encode())
        else:
            s.send("login".encode())
        datos = s.recv(1000)
        if ("aceptoPeticionLogin" == datos.decode()):
            s.send(usuario.encode())
            Bit_login=siwtchOperaciones(s.recv(1000).decode(),s)
        if ("aceptoPeticionRegistrar" == datos.decode()):
            s.send(usuario.encode())
            Bit_login=siwtchOperaciones(s.recv(1000).decode(),s)

    s.close()

def siwtchOperaciones(accion,socket):
    if ("aceptoLogin" == accion):
        loginExitos(socket)
        return 1
    if ("DeniegoLogin" == accion):
        loginDenegado()
        return 0
    if ("aceptoRegistro" == accion):
        ResgistroExitos(socket)
        return 1
    if ("DeniegoRegistro" == accion):
        RegistroDenegado()
        return 0










