from sqlite3.dbapi2 import Row
from tkinter import ttk
from tkinter import *
import sqlite3



class Venta:

    db_name = 'database.db'   


    def __init__(self,window):
        self.wind = window
        self.wind.title('Stock Forever Glam')

        #creating a frame
        frame = LabelFrame(self.wind, text = 'Agrega una venta')
        frame.grid(row= 1, column= 0, columnspan= 3, pady= 20 )

        #name imput
        Label(frame, text = 'Nombre: ').grid(row= 1, column= 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        #price imput
        Label(frame, text= 'Precio').grid(row= 2, column= 0)
        self.price = Entry(frame)
        self.price.grid(row= 2, column= 1)

        #button Add product
        ttk.Button(frame, text= 'Guardar Producto', command = self.add_product).grid(row= 3, columnspan= 2, sticky= W + E )

        #Output messages
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 3, columnspan = 2, sticky = W + E)
        #Table
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row= 4, column= 0, columnspan = 2)
        self.tree.heading('#0', text= 'Nombre', anchor= CENTER)
        self.tree.heading('#1', text= 'Precio', anchor= CENTER)
        self.get_products()

        #Botones eliminar y editar
        ttk.Button(text = 'Eliminar', command = self.delete_product).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'Editar', command = self.edit_product).grid(row = 5, column = 1, sticky = W + E)


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
        query = 'SELECT * FROM ventas ORDER BY name DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text= row[1], values = row[2])

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0
    #Agregar Productos a la base de datos
    def add_product(self):
        if self.validation():
           query = 'INSERT INTO ventas VALUES(NULL, ?, ?)'
           parameters = (self.name.get(), self.price.get())
           self.run_query(query, parameters)
           self.message['text'] = 'Venta {} agregada con exito'.format(self.name.get())
           self.name.delete(0, END)
           self.price.delete(0, END)

        else: 
            self.message['text'] = 'name or price can\'t be empty'
        self.get_products()
    #Eliminar Productos de la base de datos
    def delete_product(self):
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
    def comprobacion(self,answer,name_d):
        if answer : 
            query = 'DELETE FROM ventas WHERE name = ?'
            self.run_query(query,(name_d, ))
            self.message['text'] = 'Venta {} elminada con exito'.format(name_d)
            self.get_products()
        self.comprobacion_wind.destroy()
    #Editar producto
    def edit_product(self):
        self.message['text'] = ''
        try : 
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e: 
            self.message['text'] = 'Debes seleccionar un elemento'
            return
        name_d = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar Venta'

        #Old name
        Label(self.edit_wind,  text= 'Nombre Anterior').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name_d), state = 'readonly').grid(row = 0, column = 2)
        #New name
        Label(self.edit_wind,  text= 'Nombre Nuevo').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)
        

        #Old price
        Label(self.edit_wind,  text= 'Precio Anterior').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row = 2, column = 2)
        #New price
        Label(self.edit_wind,  text= 'Precio Nuevo').grid(row =3, column = 1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2)
        
        #Update Button
        Button(self.edit_wind, text = 'Editar', command = lambda: self.edit_records(new_name.get(), name_d, new_price.get(), old_price)).grid(row = 4, column = 2 , sticky = W + E)
        
    def edit_records(self, new_name, name_d, new_price, old_price):
        query = 'UPDATE ventas SET name =?, price = ? WHERE name = ? AND price = ? '
        parameters = (new_name, new_price, name_d, old_price)
        self.run_query(query,parameters)
        self.message['text'] = 'Venta {} editada con exito'.format(name_d)
        self.get_products()
        self.edit_wind.destroy()

''''
if __name__ == '__main__' :
    window = Tk()
    application = Venta(window)
    
    window.mainloop()

'''