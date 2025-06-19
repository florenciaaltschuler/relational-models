def print_basic_statistics(arr_vals, name):
    q1 = arr_vals.quantile(0.25)
    q3 = arr_vals.quantile(0.75)
    iqr = q3 - q1

    print("-" * 30)
    print(f"Estadísticas de {name.strip()}:")
    print("  Q1:", q1)
    print("  Q3:", q3)
    print("  IQR (rango intercuartil):", iqr)
    print("  Promedio:", arr_vals.mean())
    print("  Mediana:", arr_vals.median())
    print("  Moda:", arr_vals.mode().values[0])
    print("  Desvío estándar:", arr_vals.std())
    print("  Mínimo:", arr_vals.min())
    print("  Máximo:", arr_vals.max())
    print("-" * 30)
