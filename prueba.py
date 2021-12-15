import sqlite3
from sqlite3.dbapi2 import Row
from tkinter import ttk
from tkinter import *

from ventas_3 import Venta
from product import Product

def imprimir():
    c = combo.get()
    print(c)
    print('hola')

def hide():
    combo.grid_forget()

def selected(event):
    c = combo.get()
    print(c)
    print('paso algo')

window = Tk()
window.geometry('600x400')
#application = Product(window)
combo = ttk.Combobox(values = ['Yaritmar', 'Manuel', 'Steffany'])

combo.grid(row=0)

#def new_func(selected, combo):
    #ombo.bind("<<ComboboxSelected>>", selected)

#new_func(selected, combo)


button1 = ttk.Button(text= 'si', command= imprimir)
button1.grid(row=1)
ttk.Button(text='Esconder', command= hide).grid(row=2)

window.mainloop()