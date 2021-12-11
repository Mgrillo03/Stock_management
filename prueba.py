import sqlite3
from sqlite3.dbapi2 import Row
from tkinter import ttk
from tkinter import *

from ventas import Venta
from product import Product

def imprimir():
    c = combo.get()
    print(c)
    print('hola')

window = Tk()
window.geometry('600x400')
#application = Product(window)
combo = ttk.Combobox()
combo['values'] = ['Yaritmar', 'Manuel', 'Steffany']
combo.grid(row=0)


ttk.Button(text= 'si', command= imprimir).grid(row=1)

window.mainloop()