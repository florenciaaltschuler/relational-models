import matplotlib.pyplot as plt
import numpy as np

import utils


sql_conn = utils.SQLConnection()

df = sql_conn.run_query("prueba_sql.sql")

territorios = df["Name"]
x = np.arange(len(territorios))  # Posiciones para las barras

# Ancho de cada barra
width = 0.25

# Crear la figura
fig, ax = plt.subplots(figsize=(12, 6))

# Dibujar cada conjunto de barras
ax.bar(x - width, df["total_sales"], width, label="Total Ventas (2013-2014)")
ax.bar(x, df["SalesYTD"], width, label="Ventas Año Actual")
ax.bar(x + width, df["SalesLastYear"], width, label="Ventas Año Anterior")

# Etiquetas y leyenda
ax.set_xlabel("Territorio")
ax.set_ylabel("Ventas")
ax.set_title("Comparación de Ventas por Territorio")
ax.set_xticks(x)
ax.set_xticklabels(territorios, rotation=45, ha="right")
ax.legend()

plt.tight_layout()
plt.show()
