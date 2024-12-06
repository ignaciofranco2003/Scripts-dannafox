Este repositorio sirve para los puntos 3, 4 y 5.

1. Un sitio web para gestionar las campañas publicitarias. Deberá permitir altas, bajas,
modificaciones y listados de campañas publicitarias. Mínimamente, la información
que se desea almacenar para cada campaña publicitaria es la siguiente: razón social,
CUIL/CUIT, apellido y nombre del cliente, teléfono, email, texto a enviar por SMS (160
caracteres como máximo), localidad o localidades de destino, cantidad de mensajes a
enviar (7.000, 14.000, 21.000, 28.000, 35.000, 42.000, 49.000, 56.000, 63.000 o
70.000), nombre de la campaña publicitaria (no se admiten duplicados), estado
(creada, en ejecución, finalizada) y la fecha de inicio de la campaña. Definir las tablas
a utilizar para la base de datos que almacenará todo este conjunto de información.

2. Una base de datos de numeración telefónica. Definir las tablas a utilizar.

3. Un script Python que se encargará de crear y suministrar de números telefónicos a la
base de datos creada en el punto anterior. Para esto, se deberá procesar un archivo
Excel que contiene todos los rangos de numeración telefónica del país.

4. Un script Python, que permita generar hasta 10 archivos de tipo “Microsoft Access”
donde cada uno cuente con 7.000 números telefónicos distintos (según las localidades
seleccionadas para una campaña publicitaria) cada una. Estos archivos se generan
tomando información de la base de datos creada en el punto 2.

5. Un script Python que sea capaz de crear una planilla de cálculo a modo de reporte con
los datos de una campaña publicitaria finalizada. Este script, además debe enviar por
mail el reporte creado al cliente en cuestión.

# scripts-python

### Para crear un entorno virtual
```python
py -m venv .venv
```
### Para activar el entorno virtual
```python
.venv\Scripts\activate
```
### Para instalar las librerias requeridas para este Script
```python
pip install -r req.txt
```
### Si se agrega otra libreria 

```python
pip freeze > req.txt
```

#### .env
```
DB_HOST=
DB_NAME=
DB_USER=
DB_PASSWORD=
```
