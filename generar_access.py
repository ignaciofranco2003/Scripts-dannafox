import mysql.connector
import random
import pyodbc
import os
import win32com.client
import string
from dotenv import load_dotenv
import sys  # Importamos sys para leer parámetros de la línea de comandos

load_dotenv()

# Configuración de la base de datos
mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=3306,
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# Crear un archivo de Access vacío con Access
def create_access_file(db_file):
    # print(f"Creando archivo/s Access: {db_file}")
    try:
        # Iniciar Access usando win32com
        access = win32com.client.Dispatch("Access.Application")
        access.NewCurrentDatabase(db_file)  # Crear un archivo vacío de base de datos
        access.Quit()  # Cerrar la base de datos
    except Exception as e:
        print(f"Error al crear el archivo Access: {e}")
        raise

# Conexión a Access
def connect_to_access(db_file):
    try:
        conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + db_file
        conn = pyodbc.connect(conn_str)
        # print(f"Conexión exitosa a: {db_file}")
        return conn
    except Exception as e:
        print(f"Error al conectar a Access: {e}")
        raise

# Crear tabla en Access
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE NumerosTelefonicos (id INT PRIMARY KEY, telefono VARCHAR(15));''')
    conn.commit()

# Generar archivo de Access
def generate_access_file(db_file, phone_numbers):
    if not os.path.exists(db_file):
        create_access_file(db_file)

    conn = connect_to_access(db_file)
    create_table(conn)

    # Insertar datos en la tabla
    cursor = conn.cursor()
    for i, number in enumerate(phone_numbers):
        cursor.execute("INSERT INTO NumerosTelefonicos (id, telefono) VALUES (?, ?)", (i+1, str(number)))
    conn.commit()

# Obtener localidades asociadas a una campaña
def get_localidades_from_campaign(conn, campaign_id):
    cursor = conn.cursor()
    query = 'SELECT id_localidad FROM campanias_localidades WHERE id_campania = %s;'
    cursor.execute(query, (campaign_id,))
    return [row[0] for row in cursor.fetchall()]

# Obtener información de la campaña
def get_campaign_info(conn, campaign_id):
    cursor = conn.cursor()
    query = 'SELECT nombre_campania, cantidad_mensajes FROM campanias WHERE campania_id = %s;'
    cursor.execute(query, (campaign_id,))
    result = cursor.fetchone()
    if result:
        nombre_campania, cantidad_mensajes = result
        return nombre_campania, int(cantidad_mensajes)
    return None

# Función para sanitizar nombres de archivo
def sanitize_filename(filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return "".join(c if c in valid_chars else "_" for c in filename).strip()

# Obtener números telefónicos
def get_phone_numbers(conn, localidades, cantidad):
    cursor = conn.cursor()

    # Asegurarse de que localidades no esté vacío para evitar errores en la consulta
    if not localidades:
        print("No hay localidades para consultar.")
        return []

    phone_numbers = []

    # Realizar la consulta para cada localidad
    for localidad_id in localidades:
        query = f'SELECT numero FROM numeros WHERE localidad_id = {localidad_id} ORDER BY RAND() LIMIT {cantidad};'
        # print(f"Ejecutando consulta para localidad {localidad_id}: {query}")  # Para depurar
        cursor.execute(query)

        # Agregar los números obtenidos de la consulta al listado final
        phone_numbers.extend([row[0] for row in cursor.fetchall()])

    return phone_numbers

# Generar archivos por campaña
def generate_campaign_files(campaign_id):
    conn = mydb

    # Obtener datos de la campaña
    campaign_info = get_campaign_info(conn, campaign_id)
    if not campaign_info:
        print(f"No se encontró la campaña con ID {campaign_id}")
        conn.close()
        return

    nombre_campania, cantidad_mensajes = campaign_info

    # Obtener localidades asociadas a la campaña
    localidades = get_localidades_from_campaign(conn, campaign_id)
    if not localidades:
        print(f"No se encontraron localidades asociadas a la campaña con ID {campaign_id}")
        conn.close()
        return

    # Obtener números telefónicos
    phone_numbers = get_phone_numbers(conn, localidades, cantidad_mensajes)

    # Directorio de salida fijo
    output_dir = "./campañas_output"

    # Crear la carpeta de salida si no existe
    output_dir = os.path.abspath(output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generar los archivos de Access
    max_numbers_per_file = 10 # Limite de números por archivo
    num_files = (cantidad_mensajes // max_numbers_per_file) + (1 if cantidad_mensajes % max_numbers_per_file != 0 else 0)

    # Limitar la cantidad máxima de archivos generados a 10
    max_files = 10
    num_files = min(num_files, max_files)

    # Iniciar el ciclo para crear los archivos
    file_index = 0
    for i in range(0, cantidad_mensajes, max_numbers_per_file):
        # Asegúrate de no exceder el número máximo de archivos
        if file_index >= max_files:
            break
        
        # Tomar un subconjunto de los números de teléfono para el archivo actual
        phone_list = phone_numbers[i:i + max_numbers_per_file]
        
        # Si phone_list está vacío, se salta este archivo
        if not phone_list:
            continue
        
        # Generar el nombre del archivo
        output_file = os.path.join(output_dir, f"{sanitize_filename(nombre_campania)}_parte_{file_index + 1}.accdb")
        
        try:
            # Generar el archivo de Access con los números de teléfono
            generate_access_file(output_file, phone_list)
            # print(f"Archivo generado: {output_file}")
            
            # Incrementar el índice del archivo
            file_index += 1
        except Exception as e:
            print(f"Error al generar el archivo {output_file}: {e}")

    conn.close()


# Llamada al script con campaign_id como parámetro
if len(sys.argv) > 1:
    campaign_id = int(sys.argv[1]) 
    generate_campaign_files(campaign_id)
    print("Proceso completado")
else:
    print("Debe proporcionar un ID de campaña como parámetro.")
