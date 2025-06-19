import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import MarkerCluster

import utils
import utils_plot
import utils_print


sql_conn = utils.SQLConnection()


def prueba():
    df1 = sql_conn.run_query("consulta_geo.sql")
    print(df1)
    del df1


def tiempo_entrega_por_pedido():
    # 1. Tiempo de entrega por pedido
    df1 = sql_conn.run_query("tiempo_entrega_por_pedido.sql")

    delivery_days = df1["DeliveryDays"]
    delivery_days_nona = delivery_days.dropna()

    utils_plot.plot_hist(
        arr_vals=delivery_days,
        title="Distribución de Tiempos de Entrega (días)",
        xlabel="Días de Entrega",
        ylabel="Cantidad de Pedidos",
        show=False,
        save_fn="tiempo_entrega_por_pedido.png",
        n_bins=20,
    )

    utils_print.print_basic_statistics(
        delivery_days_nona, "tiempos de entrega por pedido"
    )
    del df1


def motivos_devoluciones():
    # 4. Motivos de devoluciones - Gráfico circular
    df4 = sql_conn.run_query("motivos_devoluciones.sql")
    utils_plot.plot_pie(
        arr_vals=df4["TotalReturns"],
        arr_labels=df4["Reason"],
        title="Motivos de Devolución",
        show=False,
        save_fn="motivos_devoluciones.png",
    )
    del df4


def devoluciones_por_producto():
    # 5. Devoluciones por producto - Barras horizontales
    df5 = sql_conn.run_query("devoluciones_por_producto.sql").head(10)

    utils_plot.plot_barh(
        y_vals=df5["Product"],
        w_vals=df5["ReturnCount"],
        title="Top 10 Productos con Más Devoluciones",
        xlabel="Cantidad de Devoluciones",
        color="salmon",
        show=False,
        save_fn="devoluciones_por_producto.png",
    )
    del df5


# 6. Devoluciones por territorio - Barras horizontales
def devoluciones_por_territorio():
    df6 = sql_conn.run_query("devoluciones_por_territorio.sql")
    df6.sort_values("ReturnCount", ascending=False, inplace=True)
    utils_plot.plot_barh(
        y_vals=df6["Territory"],
        w_vals=df6["ReturnCount"],
        title="Devoluciones por Territorio",
        xlabel="Cantidad de Devoluciones",
        color="mediumpurple",
        show=False,
        save_fn="devoluciones_por_territorio.png",
    )
    del df6


# 7. Devoluciones por subcategoría - Barras horizontales
def devoluciones_por_subcategoria():
    df7 = sql_conn.run_query("devoluciones_por_subcategoria.sql")
    df7.sort_values("ReturnCount", ascending=True, inplace=True)
    utils_plot.plot_barh(
        y_vals=df7["Subcategory"],
        w_vals=df7["ReturnCount"],
        title="Devoluciones por Subcategoría de Producto",
        xlabel="Cantidad de Devoluciones",
        color="darkcyan",
        show=False,
        save_fn="devoluciones_por_subcategoria.png",
    )
    del df7


def devoluciones_por_categoria():
    # 8. Devoluciones por categoría - Barras horizontales
    df8 = sql_conn.run_query("devoluciones_por_categoria.sql")
    df8.sort_values("ReturnCount", ascending=True, inplace=True)
    utils_plot.plot_barh(
        y_vals=df8["Category"],
        w_vals=df8["ReturnCount"],
        title="Devoluciones por Categoría de Producto",
        xlabel="Cantidad de Devoluciones",
        color="steelblue",
        show=False,
        save_fn="devoluciones_por_categoria.png",
    )
    del df8


def tasa_devolucion_por_producto():
    # 9. Tasa de devolución por producto
    df9 = sql_conn.run_query("tasa_devolucion_por_producto.sql").head(10)

    utils_plot.plot_barh(
        y_vals=df9["Product"],
        w_vals=df9["ReturnRate"],
        title="Tasa de Devolución por Producto",
        xlabel="Tasa de Devolución (Proporción)",
        color="firebrick",
        show=False,
        save_fn="tasa_devolucion_por_producto.png",
    )
    del df9


def tasa_devolucion_por_subcategoria():
    # 10. Tasa de devolución por subcategoría
    df10 = sql_conn.run_query("tasa_devolucion_por_subcategoria.sql").head(50)

    utils_plot.plot_barh(
        y_vals=df10["Subcategory"],
        w_vals=df10["ReturnRate"],
        title="Tasa de Devolución por Subcategoría",
        xlabel="Tasa de Devolución (Proporción)",
        color="darkorange",
        show=False,
        save_fn="tasa_devolucion_por_subcategoria.png",
    )
    del df10


def tasa_devolucion_por_categoria():
    # 11. Tasa de devolución por categoría
    df11 = sql_conn.run_query("tasa_devolucion_por_categoria.sql")

    utils_plot.plot_barh(
        y_vals=df11["Category"],
        w_vals=df11["ReturnRate"],
        title="Tasa de Devolución por Categoría",
        xlabel="Tasa de Devolución (Proporción)",
        color="seagreen",
        show=False,
        save_fn="tasa_devolucion_por_categoria.png",
    )
    del df11


def tasa_devolucion_por_territorio():
    # 12. Tasa de devolución por territorio
    df12 = sql_conn.run_query("tasa_devolucion_por_territorio.sql")
    df12.sort_values("ReturnRate", ascending=True, inplace=True)

    utils_plot.plot_barh(
        y_vals=df12["Territory"],
        w_vals=df12["ReturnRate"],
        title="Tasa de Devolución por Territorio",
        xlabel="Tasa de Devolución (Proporción)",
        color="royalblue",
        show=False,
        save_fn="tasa_devolucion_por_territorio.png",
    )
    del df12


def distancia_ventas_por_tienda():
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
    # plt.tight_layout()
    plt.show()
    plt.savefig(os.path.join(utils.PLOTS_DIRPATH_, "distancia_ventas_por_tienda.png"))


def ganancia_por_territorio():
    # 6. Ganancias por territorio - Barras horizontales
    df14 = sql_conn.run_query("ganancia.sql")
    plt.figure(figsize=(10, 6))
    plt.barh(df14["Territorio"], df14["GananciaTotal"], color="lightgreen")
    plt.title("Ganancia Total por Territorio")
    plt.xlabel("Ganancia Total")
    plt.tight_layout()
    plt.show()


def ganancia_por_ano():
    # 1. Ganancia por Año
    df_ano = sql_conn.run_query("ganancia_por_año.sql")
    df_ano.plot(
        kind="bar", x="Territorio", y="VentaTotal", stacked=True, figsize=(12, 6)
    )
    plt.title("Ganancia por Territorio a lo Largo de los Años")
    plt.xlabel("Territorio")
    plt.ylabel("Venta Total")
    plt.tight_layout()
    plt.show()


def ganancia_por_estacion_año():
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


def ganancia_por_mes_año():
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


def mapa_tiendas_envios():
    # 14. Mapa: Ubicación de tiendas y destinos de envío conectados
    df_map = sql_conn.run_query("distancia_ventas_por_tienda.sql")

    df_map = df_map.dropna(
        subset=["StoreLat", "StoreLong", "DeliveryLat", "DeliveryLong"]
    )

    # Crear mapa centrado en un punto medio aproximado
    center_lat = df_map["StoreLat"].mean()
    center_lon = df_map["StoreLong"].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=4)

    # Agrupar marcadores por tienda
    store_group = MarkerCluster(name="Tiendas").add_to(m)
    delivery_group = MarkerCluster(name="Destinos").add_to(m)

    # Agregar marcadores de tiendas
    for store in (
        df_map[["StoreName", "StoreLat", "StoreLong"]]
        .drop_duplicates()
        .itertuples(index=False)
    ):
        folium.Marker(
            location=[store.StoreLat, store.StoreLong],
            popup=f"Tienda: {store.StoreName}",
            icon=folium.Icon(color="blue", icon="shopping-cart", prefix="fa"),
        ).add_to(store_group)

    # Agregar líneas entre tienda y destino de envío
    for row in df_map.itertuples():
        folium.PolyLine(
            locations=[
                (row.StoreLat, row.StoreLong),
                (row.DeliveryLat, row.DeliveryLong),
            ],
            color="red",
            weight=1,
            opacity=0.5,
        ).add_to(m)

        # Opcional: marcar puntos de entrega (agrupados)
        folium.CircleMarker(
            location=(row.DeliveryLat, row.DeliveryLong),
            radius=2,
            color="green",
            fill=True,
            fill_opacity=0.6,
        ).add_to(delivery_group)

    m.save("mapa_tiendas_envios.html")
    print("Mapa guardado como 'mapa_tiendas_envios.html'")


if __name__ == "__main__":
    prueba()
    tiempo_entrega_por_pedido()
    # motivos_devoluciones()
    # devoluciones_por_producto()
    # devoluciones_por_territorio()
    # devoluciones_por_subcategoria()
    # devoluciones_por_categoria()
    # tasa_devolucion_por_producto()
    # tasa_devolucion_por_subcategoria()
    # tasa_devolucion_por_categoria()
    # tasa_devolucion_por_territorio()
    # distancia_ventas_por_tienda()
    # ganancia_por_territorio()
    # ganancia_por_ano()
    # ganancia_por_estacion_año()
    # ganancia_por_mes_año()
    # mapa_tiendas_envios()
