import os
import folium
from folium.plugins import MarkerCluster
import matplotlib.pyplot as plt
import seaborn as sns

import utils
import utils_plot
import utils_print

sns.set_context("talk")

sql_conn = utils.SQLConnection()


def prueba():
    df1 = sql_conn.run_sql_file("consulta_geo.sql")
    print(df1)
    del df1


def tiempo_entrega_por_pedido():
    # 1. Tiempo de entrega por pedido
    df1 = sql_conn.run_sql_file("tiempo_entrega_por_pedido.sql")

    utils_plot.plot_hist(
        arr_vals=df1["DeliveryDays"],
        title="Distribución de Tiempos de Entrega (días)",
        xlabel="Días de Entrega",
        ylabel="Cantidad de Pedidos",
        show=False,
        save_fn="tiempo_entrega_por_pedido.png",
        n_bins=20,
    )

    utils_print.print_basic_statistics(
        df1["DeliveryDays"].dropna(), "tiempos de entrega por pedido"
    )
    del df1


def motivos_devoluciones():
    # 4. Motivos de devoluciones - Gráfico circular
    df4 = sql_conn.run_sql_file("motivos_devoluciones.sql")
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
    df5 = sql_conn.run_sql_file("devoluciones_por_producto.sql").head(10)

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
    df6 = sql_conn.run_sql_file("devoluciones_por_territorio.sql")
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
    df7 = sql_conn.run_sql_file("devoluciones_por_subcategoria.sql")
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
    df8 = sql_conn.run_sql_file("devoluciones_por_categoria.sql")
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
    df9 = sql_conn.run_sql_file("tasa_devolucion_por_producto.sql").head(10)

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
    df10 = sql_conn.run_sql_file("tasa_devolucion_por_subcategoria.sql").head(50)

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
    df11 = sql_conn.run_sql_file("tasa_devolucion_por_categoria.sql")

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
    df12 = sql_conn.run_sql_file("tasa_devolucion_por_territorio.sql")
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
    df13 = sql_conn.run_sql_file("distancia_ventas_por_tienda_2.sql")

    df13.boxplot(column="DistanceKm", by="StoreName", grid=False, rot=60, figsize=(15, 10))
   
    plt.title("Distribución de Distancias entre Tienda y Entrega")
    plt.suptitle("")
    plt.xlabel("Tienda")
    plt.ylabel("Distancia (km)")

    plt.tight_layout()
    save_fp = os.path.join(utils.PLOTS_DIRPATH_, "distancia_ventas_por_tienda_2.png")
    print(f'Figura guardada en "{save_fp}".')
    plt.savefig(save_fp)
    # plt.show()
    plt.close()


def ganancia_por_territorio():
    # 6. Ganancias por territorio - Barras horizontales
    df14 = sql_conn.run_sql_file("ganancia.sql")
    utils_plot.plot_barh(
        y_vals=df14["Territorio"],
        w_vals=df14["GananciaTotal"],
        title="Ganancia Total por Territorio",
        xlabel="Ganancia Total",
        color="lightgreen",
        show=False,
        save_fn="ganancia_por_territorio.png",
    )
    del df14


def ganancia_por_año():
    # 1. Ganancia por Año
    df_ano = sql_conn.run_sql_file("ganancia_por_año.sql")

    df_ano = df_ano.set_index('Territorio')

    ax = df_ano.plot(
        kind="bar", rot=60, stacked=True, figsize=(12, 6)
    )
    ax.legend(title="Año", loc="best")

    ax.set_title("Ganancia por territorio por año (normalizada por cant. de días)")
    ax.set_xlabel("Territorio")
    ax.set_ylabel("Ganancia total (normalizada)")

    plt.tight_layout()
    save_fp = os.path.join(utils.PLOTS_DIRPATH_, "ganancia_por_año.png")
    print(f'Figura guardada en "{save_fp}".')
    plt.savefig(save_fp)
    # plt.show()
    plt.close()


def ganancia_por_estacion_año():
    df = sql_conn.run_sql_file("ganancia_por_estacion_año.sql")
 
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(14, 8))

    paleta_colores = sns.color_palette("tab10", n_colors=len(df["Territorio"].unique()))

    # Graficar tendencia para cada año y territorio
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
    # x_numeric = pd.Categorical(df['Estacion']).codes
    # categories = pd.Categorical(df['Estacion']).categories
    # ax = sns.regplot(
    #     x=x_numeric,
    #     y=df["CambioPorcentual"],
    #     scatter=False,
    #     line_kws={"color": "black", "linewidth": 2, "ls": "--"},
    #     ci=95,
    #     label="Línea de tendencia global",
    # )
    # ax.set_xticks(range(len(categories)))
    # ax.set_xticklabels(categories)

    plt.title(
        "Cambio porcentual de ganancia por estación y territorio"
    )
    plt.xlabel("Estación")
    plt.ylabel("Cambio porcentual de ganancia")
    plt.legend(title="Territorio", bbox_to_anchor=(1.05, 1), loc="best")
    plt.xticks(rotation=60)

    plt.tight_layout()
    save_fp = os.path.join(utils.PLOTS_DIRPATH_, "ganancia_por_estacion_año.png")
    print(f'Figura guardada en"{save_fp}".')
    plt.savefig(save_fp)
    # plt.show()
    plt.close()


def ganancia_por_mes_año():
    # 2. Ganancia agrupada por mes y año por territorio
    df_mes_ano = sql_conn.run_sql_file("ganancia_por_mes_año.sql")
    
    g = sns.FacetGrid(df_mes_ano, col="TerritoryName", col_wrap=3, height=4, aspect=1.5, sharex=False)
    g.map(sns.lineplot, "MonthStart", "TotalSales", marker="o", color="coral")

    g.set_axis_labels("Fecha", "Total ventas")
    g.set_titles("{col_name}")
    g.set_xticklabels(rotation=60)
    g.figure.suptitle("Ganancia a lo largo del tiempo para cada territorio", fontsize=22)
    # plt.subplots_adjust(top=0.9)  # Ajustar el título para no sobreponerse

    plt.tight_layout()
    save_fp = os.path.join(utils.PLOTS_DIRPATH_, "ganancia_por_mes_año.png")
    print(f'Figura guardada en "{save_fp}".')
    plt.savefig(save_fp)
    # plt.show()
    plt.close()


def mapa_tiendas_envios():
    # 14. Mapa: Ubicación de tiendas y destinos de envío conectados
    df_map = sql_conn.run_sql_file("distancia_ventas_por_tienda.sql")

    df_stores = df_map[['StoreName', 'StoreLat', 'StoreLong']].drop_duplicates()
    store_coords = set(zip(
        df_stores['StoreLat'].round(4),
        df_stores['StoreLong'].round(4) ))

    coord_to_store = {}
    for _, row in df_stores.iterrows():
        key = (round(row['StoreLat'], 4), round(row['StoreLong'], 4))
        coord_to_store[key] = row['StoreName']

    df_deliveries = df_map[df_map["DistanceKm"] > 0.01]
    df_deliveries = df_deliveries[['StoreName', 'StoreLat', 'StoreLong', 'DeliveryLat', 'DeliveryLong']].drop_duplicates()

    df_deliveries['IsStoreDelivery'] = df_deliveries.apply(
        lambda row: (round(row['DeliveryLat'], 4), round(row['DeliveryLong'], 4)) in store_coords,
        axis=1
    )

    df_deliveries['DeliveryStoreName'] = df_deliveries.apply(
    lambda row: coord_to_store.get(
        (round(row['DeliveryLat'], 4), 
         round(row['DeliveryLong'], 4)))
    if row['IsStoreDelivery'] else None,
    axis=1
    )

    center_lat = df_stores["StoreLat"].mean()
    center_lon = df_stores["StoreLong"].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=5)

    store_layer = folium.FeatureGroup(name='Tiendas')
    transfer_layer = folium.FeatureGroup(name='Transferencias')
    delivery_layer = folium.FeatureGroup(name='Entregas')

    # Agregar marcadores de tiendas
    for _, store in df_stores.iterrows():
        tooltip = f"{store['StoreName']}"
        folium.Marker(
            location=[store['StoreLat'], store['StoreLong']],
            tooltip=tooltip,
            icon=folium.Icon(color='green', icon='shopping-cart', prefix='fa')
        ).add_to(store_layer)

    n_deliveries = 0
    n_transfers = 0
    n_tot_deliveries = 0
    n_transfers_same_name = 0

    for _, row in df_deliveries.iterrows():
        locations = [
            [row['StoreLat'], row['StoreLong']],
            [row['DeliveryLat'], row['DeliveryLong']]
        ]
        n_tot_deliveries += 1
        if row.IsStoreDelivery:
            n_transfers += 1
            if row['StoreName'] == row['DeliveryStoreName']:
                n_transfers_same_name += 1

            folium.PolyLine(
                locations=locations,
                color='purple',
                weight=2.5
            ).add_to(transfer_layer)
        else:
            n_deliveries += 1
            folium.PolyLine(
                locations=locations,
                color='red',
                weight=1.5
            ).add_to(delivery_layer)

    print("-"*30)
    print(f"Total deliveries: {n_tot_deliveries}")
    print(f"Total deliveries to stores: {n_transfers}")
    print(f"Total deliveries to stores (same name): {n_transfers_same_name}")
    print(f"Total deliveries to other destinations: {n_deliveries}")
    print("-"*30)

    store_layer.add_to(m)
    transfer_layer.add_to(m)
    delivery_layer.add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)

    fp = os.path.join(utils.PLOTS_DIRPATH_, "mapa_tiendas_envios.html")
    m.save(fp)
    print(f'Mapa guardado en "{fp}".')

def cohortes():
    df = sql_conn.run_sql_file("cohortes.sql")

    print(df.head())


if __name__ == "__main__":
    # prueba()
    # tiempo_entrega_por_pedido()
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
    # ganancia_por_año()
    # ganancia_por_estacion_año()
    # ganancia_por_mes_año()
    # mapa_tiendas_envios()
    cohortes()

    sql_conn.close()
