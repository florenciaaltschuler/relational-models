
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import seaborn as sns

# Conexión a SQL Server
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=157.92.26.17,1443;'
    'DATABASE=AdventureWorks2019;'
    'UID=Alumno;'
    'PWD=mrcd2025;'
)

# Ruta a las consultas SQL
sql_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'SQL'))

def ejecutar_query(nombre_archivo_sql):
    ruta = os.path.join(sql_dir, nombre_archivo_sql)
    with open(ruta, 'r', encoding='utf-8') as f:
        query = f.read()
    return pd.read_sql_query(query, conn)


import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns


# Estilo general
sns.set(style="whitegrid")

df4 = ejecutar_query('motivos_devoluciones.sql').sort_values('TotalReturns', ascending=False)

# Crear figura independiente para lollipop
plt.figure(figsize=(6, 4))
plt.hlines(y=df4['Reason'], xmin=0, xmax=df4['TotalReturns'], color='gray', linewidth=2)
plt.plot(df4['TotalReturns'], df4['Reason'], "o", color='black')
plt.title('Motivos de Devolución')
plt.xlabel('Cantidad de Devoluciones')
plt.xlim(left=0)
plt.tight_layout()
plt.show()