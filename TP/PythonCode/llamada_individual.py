
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
# Ejecutar el archivo SQL y cargar los datos
df = ejecutar_query('productos_vendidos_por_estacion.sql')
import matplotlib.pyplot as plt
import seaborn as sns

# Asegurar orden correcto de estaciones
orden_estaciones = ['Primavera', 'Verano', 'Otoño', 'Invierno']
df['Estacion'] = pd.Categorical(df['Estacion'], categories=orden_estaciones, ordered=True)

# Configurar figura con subplots (2 filas, 2 columnas)
fig, axs = plt.subplots(2, 2, figsize=(18, 12), sharex=True)
fig.suptitle('Tendencias Estacionales por Territorio (Variaciones Porcentuales)', fontsize=20)

# Variables y títulos
variaciones = [
    ('VariacionVentas', 'Variación Porcentual de Ventas'),
    ('VariacionGananciaTotal', 'Variación Porcentual de Ganancia Total'),
    ('VariacionGananciaBruta', 'Variación Porcentual de Ganancia Bruta'),
    ('VariacionProductosVendidos', 'Variación Porcentual de Productos Vendidos')
]

# Paleta de colores por territorio
territorios = df['Territorio'].unique()
paleta_colores = sns.color_palette("tab10", n_colors=len(territorios))

# Crear gráficos
for ax, (var, titulo) in zip(axs.flat, variaciones):
    for i, (territorio, grupo) in enumerate(df.groupby('Territorio')):
        sns.lineplot(data=grupo, x='Estacion', y=var,
                     label=territorio if ax == axs[1, 1] else "",  # Solo incluir etiquetas en el último para la leyenda
                     color=paleta_colores[i], marker='o', ci=None, ax=ax)

    # Línea de promedio por estación
    media_global = df.groupby('Estacion')[var].mean().reset_index()
    sns.lineplot(data=media_global, x='Estacion', y=var,
                 color='black', linewidth=2, linestyle='--',
                 label='Promedio Global' if ax == axs[1, 1] else "", ax=ax)

    ax.set_title(titulo, fontsize=20)
    ax.set_xlabel('', fontsize=14)
    ax.set_ylabel('% Variación', fontsize=18)
    ax.tick_params(axis='both', labelsize=16)
    ax.tick_params(axis='x')
    # ❌ Eliminar leyenda local del subplot (si existe)
    if ax.get_legend() is not None:
        ax.get_legend().remove()

# Leyenda abajo (fuera de la grilla)
handles, labels = axs[1, 1].get_legend_handles_labels()
fig.legend(handles, labels, title='Territorio', fontsize=16, title_fontsize=18,
           loc='lower center', bbox_to_anchor=(0.5, -0.03), ncol=4)

plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.show()
