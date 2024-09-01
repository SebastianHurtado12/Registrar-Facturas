import pdfplumber
import re
import datos_facturas
import envio_mail
import sys
import shutil
from datetime import datetime

def mostrar_ccostos_porc(ccostos_porc):
    str = ""
    for c_costos, porc in ccostos_porc.items():
        str += f"{c_costos} -- {porc}%\n"
    return str

def guardar_factura(ruta_archivo,ruta_factura_drive,anio,mes,nro_factura):
    ruta_factura = "G:/.shortcut-targets-by-id/16t7eZVOe_BtdD74bMZyGCUvM_0RS7BuE/Facturas"
    
    try:
        shutil.copy(ruta_archivo,f"{ruta_factura}/{ruta_factura_drive}/{anio}/{anio}{mes}_{nro_factura}.pdf")
        print(f"Factura guardada en {ruta_factura}/{ruta_factura_drive}/{anio}")
    except Exception as e: 
        print(f"Error al guardar archivo: {e}")

def registrar_factura(ruta_archivo,test):

    with pdfplumber.open(ruta_archivo) as pdf:
        #creo las expresiones regulares a utilizar
        patron_factura = r'Nº\s+\d{5}[-−]\d+|Factura\sNro.\s(\d+)\-(\d+)|Factura\s*(\d+)\-(\d+)|Factura\s+(.*?)\s+[A-Za-z0-9]+|N[uú]mero:\s*(\d+)-(\d+)|N(.*?)\s+(\d+)[/-](\d+)|A\d{4}-\d'
        patron_cliente = r'Cuenta:\s[0-9]+/[0-9]+|N(.*?)\s+Cuenta(.*?)\s[0-9]+/[0-9]+|Cliente\s+(\d+)|Cliente\s+(.*?)\s+(.*?)\s+(\d+)|Usuario:\s(\d+)|cliente:\s+(.*?)+(\d+)[-−](\d+)|Cliente:\s\((\d+)\)|CLIENTE\s+N(.*?)\s(\d+)|Cuenta:\s(\d+)|Pago\s(\d+)'
        patron_fecha = r'Fecha\sde\sEmisi[oó]n:\s\d{2}/\d{2}/\d{4}|\b(?<!Actividades\s)\d{2}[/.-]\d{2}[/.-−]\d{4}\b'
        patron_delimitador = r'[/.-]'
        #tomo primera pagina del .pdf, en general en dicha pagina se encuentra la totalidad de los datos requeridos para el proceso
        page = pdf.pages[0]
        contenido_pdf = page.extract_text()
        
        match_factura = re.search(patron_factura,contenido_pdf)
        match_cliente = re.search(patron_cliente,contenido_pdf)
        match_fecha = re.search(patron_fecha, contenido_pdf)
        informacion_factura = {
            'nro_factura': match_factura.group().split('\n')[0].split(" ")[-1],
            'nro_cliente': match_cliente.group().split('\n')[0].split(" ")[-1],
            'fecha_emision': re.split(patron_delimitador,str(match_fecha.group()))
        }
        
        anio = informacion_factura['fecha_emision'][2]
        mes = informacion_factura['fecha_emision'][1]
        
        ccostos_porc,cuenta_contable,servicio,empresa,ruta_factura_drive = datos_facturas.obtener_datos_csv(informacion_factura['nro_cliente'])
        guardar_factura(ruta_archivo,ruta_factura_drive,anio,mes,informacion_factura['nro_factura'])
        asunto = f"{servicio} {empresa} | {mes}/{anio}"
        cuerpo = f"Se adjunta factura.\nPeriodo:{mes}/{anio}\nCentro de costos y porc:\n{mostrar_ccostos_porc(ccostos_porc)}\nCuenta contable: {cuenta_contable}\nEnvio automatico."
        
        envio_mail.enviar_mail(asunto,cuerpo,ruta_archivo,test)