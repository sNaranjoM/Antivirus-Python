import PySimpleGUI as sg
import sys

from Data.Data import registrarUsuario
#from Dominio.ExamenMd5 import analisisHashMd5Individual,analisisHashMd5Grupal

sg.theme('DarkAmber')
def showGUIServer(archivos, usuarios):

    vecArchivos=archivos.split("|")
    vecUsuarios = usuarios.split("|")
    layout = [
        [sg.Text('Servidor JSL', size=(30, 1), justification='center', font=("Helvetica", 25),
                 relief=sg.RELIEF_RIDGE)],
        [sg.Listbox(vecArchivos, size=(100, 10),key=('lb_citas'))],
        [sg.Listbox(vecUsuarios, size=(100, 10), key=('lb_citas'))],
    ]


    window = sg.Window('Servidor LSJ', layout,size=(500,450))

    while True:
        event, values = window.read()
        if event == 'Exit' or event is None:
            sys.exit()



def OperacionExitosa():
    sg.Popup('La operacion se realizó con exito')
def OperacionFallida():
    sg.Popup('Las contraseñas no son iguales')
def EspaciosEnBlanco():
    sg.Popup('faltan campos por llenar')

def eliminarExitoso(validar):
    if validar ==True:
        sg.Popup('Se elimino con exito')
    else:
        sg.Popup('Se produjo un error')

def acutalizaListBoxArchivos():
    print('d')



archivos=[]
