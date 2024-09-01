import tkinter
from tkinter import filedialog
import registrar_facturas

#declaracion de variable global
ruta_factura = ""

def abrir_archivo():
    
    global ruta_factura
    ruta_factura = filedialog.askopenfilename(title="Selecciona un archivo",filetypes=[("Archivos PDF", "*.pdf *.PDF")])
    txt_info.delete("1.0",tkinter.END)
    txt_info.insert(tkinter.END,f"Ha seleccionado la factura {ruta_factura.split('/')[-1]}\n")
    
def enviar_factura(ruta_factura,test):
    try:
        registrar_facturas.registrar_factura(ruta_factura,test)
        txt_info.insert(tkinter.END,"Factura enviada!\n")
    except Exception as e:
        txt_info.insert(tkinter.END,f"ERROR!, Posible causa: {e}\n")
        

#config ventana
ventana = tkinter.Tk()
ventana.geometry("450x300")
ventana.title("Registrar Factura | SISTEMAS")

lbl_titulo = tkinter.Label(ventana,text="Registar factura", font=("Arial", 14, "bold"), padx=20, pady=10)
lbl_descripcion = tkinter.Label(ventana,text="Facturas aceptadas: Claro, Movistar, Amecom, iPlan, Convergia, Cotelcam, Skycorp.", font=("Arial", 8))
btn_abrir_archivo = tkinter.Button(ventana,text="Abrir archivo",font=("Arial", 9, "bold"), padx=5,pady=5,command=lambda: abrir_archivo())
txt_info = tkinter.Text(ventana, height = 5,font=("Arial", 10))
btn_registrar_factura = tkinter.Button(ventana,text="Registar factura",font=("Arial", 9, "bold"), padx=5,pady=5,command=lambda: enviar_factura(ruta_factura,False))
btn_registrar_factura_test = tkinter.Button(ventana,text="Registar factura TEST",font=("Arial", 9, "bold"), padx=5,pady=5,command=lambda: enviar_factura(ruta_factura,True))

#posicionamiento de los widgets
lbl_titulo.pack()
lbl_descripcion.pack(pady=5)
btn_abrir_archivo.pack()
txt_info.pack(pady=10)
btn_registrar_factura.pack()
btn_registrar_factura_test.pack()

ventana.mainloop()