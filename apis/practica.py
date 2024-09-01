import requests
import datos_facturas
url = "https://codylsa.sd.cloud.invgate.net/api/v1/"

user = "Humand"
token = "7kenuqdYSoVRMpaJyEDOqxlM"

response = requests.get(url+"users", auth = (user, token))

if response.ok:
    data = response.json()
    for persona in data:
        nombre = persona.get('name')
        apellido = persona.get('lastname')
        posicion = persona.get('position')
        if nombre == "Sebastian":
            print(f"{nombre} {apellido} es {posicion}")    
       
else:
    print(f"La conexion ha fracasado. {response.status_code}")