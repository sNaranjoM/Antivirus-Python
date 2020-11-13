from threading import Thread
import time


class MiHilo(Thread):


    def run(self):

        while 1:
            print("Soy un hilo "  )
            time.sleep(1)



cadena = "ttt"

# def __init__(self, parametros):
#     # Thread.__init__(self)
#     while 1:
#         print("Soy un hilo " + parametros)
#         time.sleep(1)
