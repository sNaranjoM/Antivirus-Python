# https://recursospython.com/guias-y-manuales/hashlib-md5-sha/
import hashlib
from os import listdir
from os.path import isdir, islink

def identificacionArchivoContaminado(archivo):

    try:
        f = open(archivo, "rb")
    except IOError as e:
        print(e)
    else:
        data = f.read()
        f.close()
        print("Nombre del archivo: "+ archivo)
        h = hashlib.new("md5")
        h.update(data)
        print("Hash: " + h.hexdigest())
        vec1 = archivo.split("/")
        cantidad =len(vec1)
        # print(vec1[cantidad-1])
        return h.hexdigest() +"~~CONTAMINADO~~"+vec1[cantidad-1]


def analisisHashMd5Individual(archivo,s):

    s.send("PeticionListaHashMalisiosos".encode())
    datos = s.recv(1000)
    listaHashMalisiosos = stringToList(datos.decode())

    try:
        f = open(archivo, "rb")
    except IOError as e:
        print(e)
    else:
        data = f.read()
        f.close()
        print("Nombre del archivo: "+ archivo)
        h = hashlib.new("md5")
        h.update(data)
        print("Hash: " + h.hexdigest())
        for row in listaHashMalisiosos:
            if (row == h.hexdigest()):
                print("Hash:  " + (h.hexdigest()))
                print(archivo + "  <<CONTAMINADO>>")
            else:
                print(archivo + " (limpio)")

def analisisHashMd5Grupal(RutaCarpeta, s):

    s.send("PeticionListaHashMalisiosos".encode())
    datos = s.recv(1000)
    listaHashMalisiosos = stringToList(datos.decode())

    salida = ""

    for filename in listdir(RutaCarpeta):

        aux=0

        if not isdir(filename) and not islink(filename):
            try:
                f = open(RutaCarpeta + "/" + filename, "rb")
            except IOError as e:
                print(e)
            else:

                data = f.read()
                f.close()
                h = hashlib.new("md5")
                h.update(data)
                for row in listaHashMalisiosos:
                    if row == h.hexdigest():
                        aux = 1
                if aux == 1:
                    print(filename + "  <<CONTAMINADO>>")
                    salida=salida + filename + " <<CONTAMINADO>>"+"&"
                else:
                    print(filename + " (limpio)")
                    salida = salida + filename + " (limpio)"+"&"
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    return salida

def stringToList(hashMalisosos):
    listaHashMalisios = hashMalisosos.split("~~ANTIVIRUS~~")
    for row in listaHashMalisios:
        print("hashDD: "+row)
    return listaHashMalisios
