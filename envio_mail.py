import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders



def enviar_mail(asunto, cuerpo,ruta_archivo,test):
    # Configura los parámetros del correo
    server = 'pop.gmail.com'
    port = 587
    correo_at = 'shurtado@codylsa.com'
    if test:
        correo_rem = ['hurtadosebastian037@gmail.com']
    else:
        correo_rem = ['proveedores@codylsa.com','cmulieri@codylsa.com']
    correo_at_clave = 'ljmhnoglcsndudng'

    msg = MIMEMultipart()
    msg['From'] = correo_at
    msg['To'] = ", ".join(correo_rem)
    msg['Subject'] = asunto
    msg.attach(MIMEText(cuerpo, 'plain'))

    attachment = MIMEBase('application', 'octet-stream')

    with open(ruta_archivo, 'rb') as attachment_file:
        attachment.set_payload(attachment_file.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename={ruta_archivo.split("/")[-1]}')
        msg.attach(attachment)
    try:
    
        server = smtplib.SMTP(server, port)
        server.starttls()  
        server.login(correo_at, correo_at_clave)
        text = msg.as_string()

        server.sendmail(correo_at, correo_rem, text)
        server.quit()

    except Exception as e:
        print(f"Error al enviar correo: {e}")