import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import utils


sql_conn = utils.SQLConnection()

df1 = sql_conn.run_query("consulta_geo.sql")
print(df1)

# 1. Tiempo de entrega por pedido - Histograma
df1 = sql_conn.run_query("tiempo_entrega_por_pedido.sql")
plt.figure(figsize=(10, 6))
plt.hist(df1["DeliveryDays"], bins=20, color="skyblue", edgecolor="black")
plt.title("Distribución de Tiempos de Entrega (días)")
plt.xlabel("Días de Entrega")
plt.ylabel("Cantidad de Pedidos")
plt.tight_layout()
plt.show()


delivery_days = df1["DeliveryDays"].dropna()

# Cuartiles e IQR
q1 = delivery_days.quantile(0.25)
q3 = delivery_days.quantile(0.75)
iqr = q3 - q1

print("Q1:", q1)
print("Q3:", q3)
print("IQR (rango intercuartil):", iqr)

# Estadísticas básicas
print("Promedio:", delivery_days.mean())
print("Mediana:", delivery_days.median())
print("Moda:", delivery_days.mode().values[0])
print("Desvío estándar:", delivery_days.std())
print("Mínimo:", delivery_days.min())
print("Máximo:", delivery_days.max())


# 4. Motivos de devoluciones - Gráfico circular
df4 = sql_conn.run_query("motivos_devoluciones.sql")
plt.figure(figsize=(8, 6))
plt.pie(df4["TotalReturns"], labels=df4["Reason"], autopct="%1.1f%%", startangle=140)
plt.title("Motivos de Devolución")
plt.tight_layout()
plt.show()

# 5. Devoluciones por producto - Barras horizontales
df5 = sql_conn.run_query("devoluciones_por_producto.sql").head(10)
plt.figure(figsize=(10, 6))
plt.barh(df5["Product"], df5["ReturnCount"], color="salmon")
plt.title("Top 10 Productos con Más Devoluciones")
plt.xlabel("Cantidad de Devoluciones")
plt.tight_layout()
plt.show()

# 6. Devoluciones por territorio - Barras horizontales
df6 = sql_conn.run_query("devoluciones_por_territorio.sql")
df6.sort_values("ReturnCount", ascending=False, inplace=True)
plt.figure(figsize=(10, 6))
plt.barh(df6["Territory"], df6["ReturnCount"], color="mediumpurple")
plt.title("Devoluciones por Territorio")
plt.xlabel("Cantidad de Devoluciones")
plt.tight_layout()
plt.show()

# 7. Devoluciones por subcategoría - Barras horizontales
df7 = sql_conn.run_query("devoluciones_por_subcategoria.sql")
df7.sort_values("ReturnCount", ascending=True, inplace=True)
plt.figure(figsize=(10, 6))
plt.barh(df7["Subcategory"], df7["ReturnCount"], color="darkcyan")
plt.title("Devoluciones por Subcategoría de Producto")
plt.xlabel("Cantidad de Devoluciones")
plt.tight_layout()
plt.show()

# 8. Devoluciones por categoría - Barras horizontales
df8 = sql_conn.run_query("devoluciones_por_categoria.sql")
df8.sort_values("ReturnCount", ascending=True, inplace=True)
plt.figure(figsize=(8, 5))
plt.barh(df8["Category"], df8["ReturnCount"], color="steelblue")
plt.title("Devoluciones por Categoría de Producto")
plt.xlabel("Cantidad de Devoluciones")
plt.tight_layout()
plt.show()

# 9. Tasa de devolución por producto
df9 = sql_conn.run_query("tasa_devolucion_por_producto.sql").head(10)
plt.figure(figsize=(10, 6))
plt.barh(df9["Product"], df9["ReturnRate"], color="firebrick")
plt.title("Tasa de Devolución por Producto")
plt.xlabel("Tasa de Devolución (Proporción)")
plt.tight_layout()
plt.show()

# 10. Tasa de devolución por subcategoría
df10 = sql_conn.run_query("tasa_devolucion_por_subcategoria.sql").head(50)
plt.figure(figsize=(10, 6))
plt.barh(df10["Subcategory"], df10["ReturnRate"], color="darkorange")
plt.title("Tasa de Devolución por Subcategoría")
plt.xlabel("Tasa de Devolución (Proporción)")
plt.tight_layout()
plt.show()

# 11. Tasa de devolución por categoría
df11 = sql_conn.run_query("tasa_devolucion_por_categoria.sql")
plt.figure(figsize=(8, 5))
plt.barh(df11["Category"], df11["ReturnRate"], color="seagreen")
plt.title("Tasa de Devolución por Categoría")
plt.xlabel("Tasa de Devolución (Proporción)")
plt.tight_layout()
plt.show()

# 12. Tasa de devolución por territorio
df12 = sql_conn.run_query("tasa_devolucion_por_territorio.sql")
df12.sort_values("ReturnRate", ascending=True, inplace=True)
plt.figure(figsize=(10, 6))
plt.barh(df12["Territory"], df12["ReturnRate"], color="royalblue")
plt.title("Tasa de Devolución por Territorio")
plt.xlabel("Tasa de Devolución (Proporción)")
plt.tight_layout()
plt.show()

# 13. Distancia entre tienda y destino de envío
df13 = sql_conn.run_query("distancia_ventas_por_tienda.sql")

# Boxplot de distancias por tienda (top 10 por cantidad de registros)
top_tiendas = df13["StoreName"].value_counts().head(10).index
df_top = df13[df13["StoreName"].isin(top_tiendas)]


# Calcular el promedio de distancia por tienda
store_avg_distance = (
    df_top.groupby("StoreName")["DistanceKm"].mean().sort_values(ascending=False)
)

# Ordenar df_top por el promedio de distancia de mayor a menor
df_top["StoreName"] = pd.Categorical(
    df_top["StoreName"], categories=store_avg_distance.index, ordered=True
)
df_top = df_top.sort_values("StoreName")

# Crear figura y tamaño del gráfico
plt.figure(figsize=(12, 6))

# Crear el boxplot de distancias por tienda (ordenado)
ax = df_top.boxplot(column="DistanceKm", by="StoreName", grid=False, rot=45)

# Agregar los puntos individuales (scatter plot) sobre el boxplot
for i, store_name in enumerate(store_avg_distance.index, start=1):
    store_data = df_top[df_top["StoreName"] == store_name]
    plt.scatter(
        [i] * len(store_data), store_data["DistanceKm"], alpha=0.5, color="blue"
    )

# Personalizar el gráfico
plt.title("Distribución de Distancias entre Tienda y Entrega")
plt.suptitle("")  # Eliminar el título por defecto
plt.xlabel("Tienda")
plt.ylabel("Distancia (km)")

# Ajustar el diseño y mostrar el gráfico
plt.tight_layout()
plt.show()


# 6. Ganancias por territorio - Barras horizontales
df14 = sql_conn.run_query("ganancia.sql")
plt.figure(figsize=(10, 6))
plt.barh(df14["Territorio"], df14["GananciaTotal"], color="lightgreen")
plt.title("Ganancia Total por Territorio")
plt.xlabel("Ganancia Total")
plt.tight_layout()
plt.show()

# 1. Ganancia por Año
df_ano = sql_conn.run_query("ganancia_por_año.sql")
df_ano.plot(kind="bar", x="Territorio", y="VentaTotal", stacked=True, figsize=(12, 6))
plt.title("Ganancia por Territorio a lo Largo de los Años")
plt.xlabel("Territorio")
plt.ylabel("Venta Total")
plt.tight_layout()
plt.show()


# Ejecutar la consulta para obtener los datos pivotados
df = sql_conn.run_query("ganancia_por_estacion_año.sql")

# Verificar las primeras filas del DataFrame para asegurarse de que la columna 'CambioPorcentual' existe
print(df.head())

sns.set(style="whitegrid")

# Crear una figura para el gráfico
plt.figure(figsize=(14, 8))

# Asignar una paleta de colores para los territorios
paleta_colores = sns.color_palette("tab10", n_colors=len(df["Territorio"].unique()))

# Graficar una línea para cada año y territorio
for i, (territorio, grupo) in enumerate(df.groupby("Territorio")):
    sns.lineplot(
        data=grupo,
        x="Estacion",
        y="CambioPorcentual",
        label=territorio,
        color=paleta_colores[i],
        marker="o",
    )

# Graficar la línea de tendencia global
sns.regplot(
    data=df,
    x="Estacion",
    y="CambioPorcentual",
    scatter=False,
    line_kws={"color": "black", "linewidth": 2, "ls": "--"},
    ci=95,
    label="Línea de tendencia global",
)

# Personalizar el gráfico
plt.title(
    "Líneas de Tendencia del Cambio Porcentual de Ganancia por Estación y Territorio"
)
plt.xlabel("Estación")
plt.ylabel("Cambio Porcentual de la Ganancia")
plt.legend(title="Territorio", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.xticks(rotation=45)
plt.tight_layout()

# Mostrar el gráfico
plt.show()
# 2. Ganancia por Mes y Año (Ejemplo: Agrupado por mes y año por territorio)
df_mes_ano = sql_conn.run_query("ganancia_por_mes_año.sql")

# Crear un FacetGrid para tener un gráfico por territorio
g = sns.FacetGrid(
    df_mes_ano, col="Territorio", col_wrap=4, height=4
)  # 4 gráficos por fila
g.map(sns.lineplot, "Mes", "VentaTotal", marker="o", color="coral")

# Personalizar los gráficos
g.set_axis_labels("Mes", "Venta Total")
g.set_titles("{col_name}")
g.set_xticklabels(rotation=45)
g.fig.suptitle("Ganancia por Mes y Año para cada Territorio", fontsize=16)
plt.tight_layout()
plt.subplots_adjust(top=0.9)  # Ajustar el título para no sobreponerse
plt.show()
"""''
# 14. Mapa: Ubicación de tiendas y destinos de envío conectados

import folium
from folium.plugins import MarkerCluster

df_map = df13.copy()
df_map = df_map.dropna(subset=['StoreLat', 'StoreLong', 'DeliveryLat', 'DeliveryLong'])

# Crear mapa centrado en un punto medio aproximado
center_lat = df_map['StoreLat'].mean()
center_lon = df_map['StoreLong'].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=4)

# Agrupar marcadores por tienda
store_group = MarkerCluster(name="Tiendas").add_to(m)
delivery_group = MarkerCluster(name="Destinos").add_to(m)

# Agregar marcadores de tiendas
for store in df_map[['StoreName', 'StoreLat', 'StoreLong']].drop_duplicates().itertuples(index=False):
    folium.Marker(
        location=[store.StoreLat, store.StoreLong],
        popup=f"Tienda: {store.StoreName}",
        icon=folium.Icon(color='blue', icon='shopping-cart', prefix='fa')
    ).add_to(store_group)

# Agregar líneas entre tienda y destino de envío
for row in df_map.itertuples():
    folium.PolyLine(
        locations=[(row.StoreLat, row.StoreLong), (row.DeliveryLat, row.DeliveryLong)],
        color='red',
        weight=1,
        opacity=0.5
    ).add_to(m)

    # Opcional: marcar puntos de entrega (agrupados)
    folium.CircleMarker(
        location=(row.DeliveryLat, row.DeliveryLong),
        radius=2,
        color='green',
        fill=True,
        fill_opacity=0.6
    ).add_to(delivery_group)

m.save('mapa_tiendas_envios.html')
print("🌍 Mapa guardado como 'mapa_tiendas_envios.html'")
""" """"""
