import pandas

datos_facturas_ruta = "datos/datos_facturas.csv"
#CREAR OBJETO!!
def obtener_datos_csv(nro_cliente) -> dict:

    data = pandas.read_csv(datos_facturas_ruta)
    fila = data[data['nro_cliente']==nro_cliente]
    
    centros_costos = []
    porcentajes = []
    for c_costos in fila['centro_costos']:
        centros_costos = c_costos.split('|')

    for porc in fila['porc']:
        porcentajes = porc.split('|')    

    cuenta_contable = []
    for c_contable in fila['cuenta_contable']:
        cuenta_contable = c_contable
    
    servicio = []
    for serv in fila['servicio']:
        servicio = serv

    empresa = []
    for emp in fila['empresa']:
        empresa = emp

    ruta_factura_drive = []
    for path in fila['ruta_factura_drive']:
        ruta_factura_drive = path

    ccostos_porc = {}
    for i in range(len(centros_costos)):
        ccostos_porc[centros_costos[i]] = porcentajes[i]
    
    return ccostos_porc,cuenta_contable,servicio,empresa,ruta_factura_drive

