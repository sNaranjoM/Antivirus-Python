import threading

import PySimpleGUI as sg
import sys
import time
from threading import Thread
from datetime import date
from datetime import datetime

from Dominio.Actualizaciones import MiHilo
from Dominio.ExamenMd5 import analisisHashMd5Individual, analisisHashMd5Grupal,identificacionArchivoContaminado

sg.theme('DarkAmber')

global ListaTema

def login():
    layout = [
        [sg.Text('Nombre')],
        [sg.In(key=('nombre'))],
        [sg.Text('Contraseña')],
        [sg.In(key=('contrasena'),password_char ='*')],
        [sg.Text('                     '), sg.Button('Registrar', key=('registrar')), sg.Button('Ingresar', key=('login'))],
    ]
    window = sg.Window('Antivirus LSJ', layout)
    while True:
        event, values = window.read()
        if event == 'Exit' or event is None:
            sys.exit()
        if event == 'login' or event is None:
            window.close()
            return values['nombre']+"~~LOGIN~~"+values['contrasena']
        if event == 'registrar' or event is None:
            window.close()
            return values['nombre']+"~~REGISTRAR~~"+values['contrasena']



def showGUI(socket):

    # hilo = MiHilo()
    # hilo.start()


    # archivosMalisiosos.append(listaHashMalisiosos)
    column1 = [
               [sg.CalendarButton('  Fecha  ', target='txt_Dia', pad=None, key='_CALENDAR_', format=('%Y-%m-%d'),size=(10, 1))],
               [sg.FolderBrowse(  'Carpeta  ', target='imput2',size=(10, 1)),sg.In('', key=('imput2'),visible=False)],
               [sg.Text('Dia: ')],
               [sg.In('                  ',key='txt_Dia',size=(12, 1))],
               [sg.Button('Aceptar', key=('aceptarExamenProgramado'),size=(10, 1),button_color=('red', 'white'))]
    ]

    column2 = [
        [sg.FileBrowse('Archivo', file_types=(("Text Files", "*.pdf"),), target='imput',size=(20, 1))],
        [sg.Button('Reportar', key=('ExaminarArchivo'),size=(20, 1),button_color=('red', 'white'))],
        [sg.Text('                  '),sg.In('', key=('imput'),visible=False)],
        [sg.FolderBrowse('Carpeta', target='imput',size=(20, 1))],
        [sg.Button('Examinar carpeta', key=('ExaminarCarpeta'),size=(20, 1),button_color=('red', 'white'))]
    ]
    layout = [
        [sg.Text('Antivirus JSL', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
        [sg.Text('       ')],
        # espacio para programar cita
        [sg.Text('Examen programado',font=("Helvetica", 15))],
        [sg.Frame('Hora y minutos', [[
            sg.Slider(range=(1, 24), orientation='v', size=(7, 20), default_value=12, key='sld_hora'),
            sg.Slider(range=(1, 60), orientation='v', size=(7, 20), default_value=30,key='sld_minuto'),
            sg.Column(column1)
        ]]),sg.Listbox(values=('     ~~~~     Analisis programados        ~~~~     ', ''), size=(50, 10),key=('lb_citas'))],
        [sg.Text('_' * 80)],
        # espacio para examinar carpeta
        [sg.Text('Analizar carpeta', font=("Helvetica", 15))],
        [sg.Frame('Analisis', [[
            sg.Column(column2)
        ]]), sg.Listbox(values=("      ~~~~~     Resultado del analisis        ~~~~~     " , "" ), size=(50, 10),key=('lb_Examen'),enable_events=True)]


    ]
    # visible=False

    window = sg.Window('Antivirus LSJ', layout, size=(550,550))

    listaArgs=[window,socket]

    d = threading.Thread(target=hiloValidacionActualizacion, name='Daemon', args=(listaArgs,))
    d.setDaemon(True)
    d.start()

    # event, values = window.read()

    while True:
        event, values = window.read()
        if event == 'Exit' or event is None:
            sys.exit()
        if event == 'ExaminarArchivo' or event is None:
            socket.send("nuevoArchivoContaminado".encode())
            respuesta = socket.recv(1000)
            if(respuesta.decode() == "aceptoPeticion"):
                socket.send(identificacionArchivoContaminado(values['imput']).encode())
                respuesta = socket.recv(1000)
                sg.Popup(respuesta.decode())
            # print(values['imput'])

            # analisisHashMd5Individual(values['imput'], listaHashMalisiosos)
        if event == 'ExaminarCarpeta' or event is None:
            # print("holamundo")
            actualizaListaArchivoInspecionados(analisisHashMd5Grupal(values['imput'],socket), window)
        if event == 'aceptarExamenProgramado' or event is None:
            if(int(values['sld_hora']) < 10):
                hora = "0" + str(int(values['sld_hora'])) + ":" + str(int(values['sld_minuto']))
            else:
                hora = str(int(values['sld_hora'])) + ":" + str(int(values['sld_minuto']))
            actualizaListBoxAnalisisProgramados(values['txt_Dia'],hora ,values['imput2'],window)

            lista.append(values['txt_Dia']+"|"+ hora +"|"+ values['imput2'])



def hiloValidacionActualizacion(args):

    # event, values = args.read()
    while 1:
        # proceso para averiguar la fecha y hora del sistema
        now = str(datetime.now())
        vec = now.split(" ")
        vec2 = vec[1].split(".")
        vec3 = vec2[0].split(":")
        fechaSistema = str(date.today())
        horaSistema = vec3[0] + ":" + vec3[1]
        print("Time sistema: "+fechaSistema + horaSistema)

        for x in lista:
            print(x)
            cita =x.split("|")
            if(cita[0]==fechaSistema and cita[1] == horaSistema):
                print("Se procede a realizar una inspeccion en la carpeta: " + cita[2])
                print()
                actualizaListaArchivoInspecionados(analisisHashMd5Grupal(cita[2],args[1]),args[0])
        time.sleep(30)


def actualizaListaArchivoInspecionados(entrada,window):
    listaArchivos = entrada.split("&")
    choices = ['      ~~~~~     Resultado del analisis        ~~~~~     ', '']
    for x in listaArchivos:
        choices.append(x)
        # print(x)
    window['lb_Examen'].update(choices)
    # window.FindElement('lb_archivos').Update()

def actualizaListBoxAnalisisProgramados(fecha, hora, carpeta,window):

    choices = ['     ~~~~     Analisis programados        ~~~~     ', '']
    choices.append(fecha + " - " + hora + " - "  + carpeta)
    window['lb_citas'].update(choices)


def loginExitos(socket):
    sg.Popup('Exito!')
    showGUI(socket)



def loginDenegado():
    sg.Popup('No existe un usuario registrado con esos credenciales')
    return 0;

def ResgistroExitos(socket):
    sg.Popup('Usuario registrado con exito!')
    showGUI(socket)

def RegistroDenegado():
    sg.Popup('No se puede crear el usario, intente de nuevo con otras credenciales')
    return 0;

lista = []
archivosMalisiosos=[]



