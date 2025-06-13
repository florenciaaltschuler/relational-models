
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


# Ejecutar la consulta para obtener los datos pivotados
df = ejecutar_query('ganancia_por_estacion_año.sql')

# Verificar las primeras filas del DataFrame para asegurarse de que la columna 'CambioPorcentual' existe
print(df.head())


sns.set(style="whitegrid")

# Crear una figura para el gráfico
plt.figure(figsize=(14, 8))

# Asignar una paleta de colores para los territorios
paleta_colores = sns.color_palette("tab10", n_colors=len(df['Territorio'].unique()))

# Graficar una línea para cada año y territorio
for i, (territorio, grupo) in enumerate(df.groupby('Territorio')):
    sns.lineplot(data=grupo, x='Estacion', y='CambioPorcentual', label=territorio, color=paleta_colores[i], marker='o')

# Graficar la línea de tendencia global
sns.regplot(data=df, x="Estacion", y="CambioPorcentual", scatter=False, 
            line_kws={'color': 'black', 'linewidth': 2, 'ls': '--'}, 
            ci=95, label='Línea de tendencia global')

# Personalizar el gráfico
plt.title('Líneas de Tendencia del Cambio Porcentual de Ganancia por Estación y Territorio')
plt.xlabel('Estación')
plt.ylabel('Cambio Porcentual de la Ganancia')
plt.legend(title='Territorio', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()

# Mostrar el gráfico
plt.show()
