﻿import pandas as pd
import smtplib
from dotenv import load_dotenv
import os
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import mysql.connector
import sys  # Importa sys para trabajar con los argumentos de la línea de comandos

load_dotenv()

# Configuración de la base de datos
mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=3306,
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# Configuración del correo
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'dannafoxldl@gmail.com',
    'password': 'anxm udpk jsmg bhap'
}


def get_campaign_data(campania_id):
    """Obtiene datos de la campaña desde la base de datos"""

    sql_query = """SELECT 
        c.razon_social, 
        c.cuil_cuit, 
        c.apellido, 
        c.nombre,
        c.telefono, 
        c.email,
        cp.texto_SMS AS sms_text, 
        cp.cantidad_mensajes AS message_count, 
        cp.nombre_campania AS campaign_name, 
        cp.estado AS status, 
        cp.fecha_inicio AS start_date
    FROM campanias AS cp
    JOIN clientes AS c ON cp.cliente_id = c.cliente_id
    WHERE cp.campania_id = %s; """

    mycurr = mydb.cursor(dictionary=True)
    mycurr.execute(sql_query, (campania_id,))
    campaign = mycurr.fetchone()

    if campaign is None:
        raise ValueError(f"No se encontró la campaña con ID {campania_id}")

    return campaign

def generate_excel_report(campaign, file_path):
    """Genera un archivo Excel con los datos de la campaña"""
    data = {
        'Razón Social': [campaign['razon_social']],
        'CUIL/CUIT': [campaign['cuil_cuit']],
        'Apellido': [campaign['apellido']],
        'Nombre': [campaign['nombre']],
        'Teléfono': [campaign['telefono']],
        'Email': [campaign['email']],
        'Texto SMS': [campaign['sms_text']],
        'Cantidad de Mensajes': [campaign['message_count']],
        'Nombre de Campaña': [campaign['campaign_name']],
        'Estado': [campaign['status']],
        'Fecha de Inicio': [campaign['start_date']],
    }

    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)

def send_email_with_attachment(receiver_email, file_path):
    """Envía un correo electrónico con un archivo adjunto"""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_CONFIG['sender_email']
    msg['To'] = receiver_email
    msg['Subject'] = 'Reporte de Campaña'
    msg.attach(MIMEText('Adjunto encontrarás el reporte de la campaña.', 'plain'))

    with open(file_path, 'rb') as file:
        attachment = MIMEApplication(file.read(), _subtype='xlsx')
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))
        msg.attach(attachment)

    with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
        server.starttls()
        server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['password'])
        server.sendmail(EMAIL_CONFIG['sender_email'], receiver_email, msg.as_string())
        print(f'Correo enviado a {receiver_email}\n')

def generate_campaign_report(campania_id):
    """Genera el reporte y lo envía por correo"""
    try:
        # Obtener datos de la campaña
        campaign = get_campaign_data(campania_id)

        # Verificar que la campaña esté finalizada antes de proceder
        if campaign['status'].lower() != 'finalizada':
            raise ValueError(f"La campaña con ID {campania_id} no está finalizada. No se puede enviar el reporte.")

        # Generar archivo Excel
        file_path = f'campaña_{campania_id}.xlsx'
        generate_excel_report(campaign, file_path)

        # Enviar el archivo por correo
        send_email_with_attachment(campaign['email'], file_path)

        # Eliminar el archivo después de enviar el correo
        os.remove(file_path)
        print('Proceso completado con exito.')

    except ValueError as e:
        print(e)
    except Exception as e:
        print(f'Error inesperado: {e}')

# Verificar que se pasó la ID de la campaña como argumento
if len(sys.argv) != 2:
    print("Uso: python generate_report.py <ID_Campania>")
    sys.exit(1)

# Obtener la ID de la campaña del argumento
campania_id = sys.argv[1]

# Ejecutar la función de generar reporte
generate_campaign_report(campania_id)
