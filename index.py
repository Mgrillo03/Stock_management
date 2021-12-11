import sqlite3
from sqlite3.dbapi2 import Row
from tkinter import ttk
from tkinter import *

from ventas import Venta
from product import Product



def iniciar_product(window):
    frame_w = LabelFrame(window, text = '')
    frame_w.grid(row= 0, column= 0, columnspan= 20, pady= 20, padx= 1 )
    ttk.Button(frame_w, text = 'Producto', command = lambda : start_product(window)).grid(row= 10, column= 0, padx= 5)
    ttk.Button(frame_w, text = 'Venta', command = lambda : start_sells(window)).grid(row= 10, column= 1, padx= 10)
    ttk.Button(frame_w, text = 'Compra', command = lambda : start_sells(window)).grid(row= 10, column= 2, padx= 10)
    ttk.Button(frame_w, text = 'Cliente', command = lambda : start_sells(window)).grid(row= 10, column= 3, padx= 10)
    ttk.Button(frame_w, text = 'Proveedor', command = lambda : start_sells(window)).grid(row= 10, column= 4, padx= 10)
    ttk.Button(frame_w, text = 'Estadisticas', command = lambda : start_sells(window)).grid(row= 10, column= 5, padx= 10)
    application = Product(window)

    
def start_product(window):
    application = Product(window)

def start_sells(window):
    application = Venta(window)

def start_purchases(window):
    pass

def start_clients(window):
    pass

def start_providers(window):
    pass
    



if __name__ == '__main__' :
    window = Tk()
    #application = Product(window)
    iniciar_product(window)
    window.mainloop()