from os import name, stat
from sqlite3.dbapi2 import Row
from tkinter import ttk
from tkinter import *
import sqlite3
from typing import Collection





class Venta:


    db_name = 'database.db'   


    def __init__(self,window):
        self.wind = window
        self.wind.title('Stock Forever Glam')
        self.wind.geometry('900x750')
        self.get_products_data()

        #creating a frame
        frame = LabelFrame(self.wind, text = 'Registra una nueva venta')
        frame.grid(row= 1, column= 0, columnspan= 3, pady= 20, padx= 40 )

        #name imput
        Label(frame, text = 'Nombre: ').grid(row= 1, column= 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        #product imput
        Label(frame, text= 'Producto').grid(row= 2, column= 0)
        #self.stock = Entry(frame)
        #self.stock.grid(row= 2, column= 1)
        self.combo = ttk.Combobox(frame, width= 16)
        self.combo.grid(row=2, column= 1)
        self.combo['values'] = self.names_added
        self.combo.set('Seleccionar')
        self.combo.bind("<<ComboboxSelected>>", self.selected)

        #price
        Label(frame, text= 'Precio').grid(row= 3, column= 0)
        self.price = Entry(frame, textvariable= '0')
        self.price.grid(row= 3, column= 1)
        
        #quantity
        Label(frame, text= 'Cantidad').grid(row= 4, column= 0)
        self.quantity = Entry(frame)
        self.quantity.grid(row= 4, column= 1)

        
        #button Add product
        ttk.Button(frame, text= 'Cargar Venta', command = self.add_sell).grid(row= 6, columnspan= 2, sticky= W + E )

        #Output messages
        self.message = Label(text = '', fg = 'red')
        #control names
        #self.names_added = []
        

        self.message.grid(row = 3, columnspan = 2, sticky = W + E)
        columns = ('product', 'quantity','price','total')

        #Table
        self.tree = ttk.Treeview(height = 30, columns = columns)
        self.tree.grid(row= 1, column= 9, columnspan = 1, rowspan= 10)
        self.tree.heading('#0', text= 'Comprador', anchor= CENTER)
        self.tree.heading('product', text= 'Articulo', anchor= CENTER)
        self.tree.heading('quantity', text= 'Cantidad', anchor= CENTER)
        self.tree.heading('price', text= 'Precio', anchor= CENTER)
        self.tree.heading('total', text= 'Total', anchor= CENTER)

        self.tree.column('#0', width= 90, anchor= CENTER)
        self.tree.column('product', width= 200, anchor= CENTER)
        self.tree.column('quantity', width= 40, anchor= CENTER)
        self.tree.column('price', width= 50, anchor= CENTER)
        self.tree.column('total', width= 50, anchor= CENTER)
        
        self.get_products()
        

        #Botones eliminar y editar
        frame_ed = LabelFrame(self.wind, text= '')
        frame_ed.grid(row=2, column=0, padx= 40)
        ttk.Button(frame_ed, text = 'Eliminar', command = self.delete_sell).grid(row = 2, column = 0)
        ttk.Button(frame_ed, text = 'Editar  ', command = self.edit_sell).grid(row = 2, column = 1)


    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn : 
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()            
        return result

    #Cargar productos de la base de datos
    def get_products(self):
        #cleanning Table
        records = self.tree.get_children()
        for element in records :
            self.tree.delete(element)
        #quering data
        query = 'SELECT * FROM sell ORDER BY buyer_name DESC'
        db_rows = self.run_query(query)
        #self.names_added=[]
        for row in db_rows:
            #self.names_added.append(row[1].upper())
            self.tree.insert('', 0, text= row[1], values = row[2:])

    def validation(self, name, product, quantity, price):
             
        return len(name) != 0 and len(product) and len(quantity) != 0 and len(price) != 0  

    #Agregar Productos a la base de datos
    def add_sell(self):
        
        if self.validation(self.name.get(),self.product,self.quantity.get(),self.price.get()) :
           self.total = float(self.price.get())*float(self.quantity.get())
           query = 'INSERT INTO sell VALUES(NULL, ?, ?, ?, ?, ?)'
           parameters = (self.name.get(), self.product, self.quantity.get(), self.price.get(), self.total)
           self.run_query(query, parameters)
           self.message['text'] = 'Venta agregada satisfactoriamente '
           self.name.delete(0, END)
           self.price.delete(0, END)
           self.quantity.delete(0, END)
           self.combo.set('Seleccionar')
        self.get_products()

    #Eliminar Productos de la base de datos
    def delete_sell(self):
        self.message['text'] = ''
        try : 
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e: 
            self.message['text'] = 'Debes seleccionar un elemento'
            return
        name_d = self.tree.item(self.tree.selection())['text']
        self.comprobacion_wind = Toplevel()
        self.comprobacion_wind.geometry("300x100")
        question = 'Esta seguro que desea eliminar {}'.format(name_d)
        #Label(self.comprobacion_wind, text = ' ').grid(row = 0, column = 0, padx = 20)
        Label(self.comprobacion_wind, text = question).grid(row = 0, column = 1)
        answer = False
        #Button Yes
        Button(self.comprobacion_wind, text = 'Eliminar', command = lambda: self.comprobacion(True, name_d)).grid(row = 3, column = 1, pady= 20)
        #Button NO
        Button(self.comprobacion_wind, text = 'Cancelar', command = lambda: self.comprobacion(False, name_d)).grid(row = 3, column = 2, pady= 20)

    #Pregunta antes de eliminar
    def comprobation(self,answer,name_d):
        if answer : 
            query = 'DELETE FROM sell WHERE buyer_name = ?'
            self.run_query(query,(name_d, ))
            self.message['text'] = 'El producto {} elminado satisfactoriamente'.format(name_d)
            self.get_products()
        self.comprobacion_wind.destroy()
    
    #Editar producto
    def edit_sell(self):
        self.message['text'] = ''
        try : 
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e: 
            self.message['text'] = 'Debes seleccionar un elemento'
            return
        name_d = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][1]
        old_stock = self.tree.item(self.tree.selection())['values'][0]
        old_sell_price = self.tree.item(self.tree.selection())['values'][2]
        
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar Producto'

        #name
        Label(self.edit_wind,  text= 'Nombre').grid(row = 0, column = 1)
        self.new_name= Entry(self.edit_wind)
        self.new_name.grid(row = 0, column = 2)
        self.new_name.insert(0,name_d)
        
        #stock
        Label(self.edit_wind,  text= 'Stock ').grid(row = 1, column = 1)
        self.new_stock = Entry(self.edit_wind)
        self.new_stock.grid(row = 1, column = 2)
        self.new_stock.insert(0, str(old_stock))
        #price
        Label(self.edit_wind,  text= 'Precio ').grid(row = 2, column = 1)
        self.new_price = Entry(self.edit_wind)
        self.new_price.grid(row = 2, column = 2)
        self.new_price.insert(0, str(old_price))
        #sell_price
        Label(self.edit_wind,  text= 'Pr. Venta ').grid(row = 3, column = 1)
        self.new_sell_price = Entry(self.edit_wind)
        self.new_sell_price.grid(row = 3, column = 2)
        self.new_sell_price.insert(0, str(old_sell_price))
        #Update Button
        Button(self.edit_wind, text = 'Editar', command = lambda: self.edit_records(self.new_name.get(), name_d, self.new_price.get(), self.new_stock.get(), self.new_sell_price.get())).grid(row = 4, column = 2 , sticky = W + E)
        
    def edit_records(self, new_name, name_d, new_price, new_stock, new_sell_price):
        
        ###REVISAR QUERY
      
        query = 'UPDATE sell SET name =?, stock = ?, price = ?, sell_price = ?, sug_price = ? WHERE name = ?'    
        new_sug_price = str(float(new_price) *2)
        parameters = (new_name, new_stock, new_price, new_sell_price, new_sug_price, name_d)
        self.run_query(query,parameters)    
        self.message['text'] = 'El producto editado satisfactoriamente'
        self.get_products()
        self.edit_wind.destroy()


    def get_products_data(self):
        #quering data
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        self.names_added=[]
        self.price_data = []
        for row in db_rows:
            self.names_added.append(row[1].upper())
            self.price_data.append(row[4])
        
        

    def selected(self, event):
        ##Actualizar automaticamente el precio cada vez que se seleccione una opcion del combobox
        option = self.combo.current()
        price = str(self.price_data[option])
        self.price.delete(0, END)
        self.price.insert(0, price)
        
        
        self.product = self.names_added[option]
