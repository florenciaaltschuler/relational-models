import pyodbc 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


# Datos de conexión
server = '157.92.26.17,1443'  # IP y puerto
database = 'AdventureWorks2019'  # Reemplaza esto con el nombre real de la base
username = 'Alumno'
password = 'mrcd2025'

# Cadena de conexión
conn_str = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
)

# Crear la conexión con pyodbc
conn = pyodbc.connect(conn_str)

# Leer el archivo SQL
sql_path = os.path.join(os.path.dirname(__file__), '../sql/prueba_sql.sql')
query = open(sql_path, encoding='utf-8').read()

# Ejecutar el query con una conexión válida
df = pd.read_sql_query(query, conn)


# Supongamos que ya tenés tu DataFrame como df
territorios = df['Name']
x = np.arange(len(territorios))  # Posiciones para las barras

# Ancho de cada barra
width = 0.25

# Crear la figura
fig, ax = plt.subplots(figsize=(12, 6))

# Dibujar cada conjunto de barras
ax.bar(x - width, df['total_sales'], width, label='Total Ventas (2013-2014)')
ax.bar(x, df['SalesYTD'], width, label='Ventas Año Actual')
ax.bar(x + width, df['SalesLastYear'], width, label='Ventas Año Anterior')

# Etiquetas y leyenda
ax.set_xlabel('Territorio')
ax.set_ylabel('Ventas')
ax.set_title('Comparación de Ventas por Territorio')
ax.set_xticks(x)
ax.set_xticklabels(territorios, rotation=45, ha='right')
ax.legend()

plt.tight_layout()
plt.show()
