WITH CTE AS (
    SELECT 
        YEAR(soh.OrderDate) AS Año,
        CASE 
            WHEN MONTH(soh.OrderDate) IN (12, 1, 2) AND st.Name <> 'Australia' THEN 'Invierno'
            WHEN MONTH(soh.OrderDate) IN (3, 4, 5) AND st.Name <> 'Australia' THEN 'Primavera'
            WHEN MONTH(soh.OrderDate) IN (6, 7, 8) AND st.Name <> 'Australia' THEN 'Verano'
            WHEN MONTH(soh.OrderDate) IN (9, 10, 11) AND st.Name <> 'Australia' THEN 'Otoño'
            WHEN MONTH(soh.OrderDate) IN (12, 1, 2) AND st.Name = 'Australia' THEN 'Verano'
            WHEN MONTH(soh.OrderDate) IN (3, 4, 5) AND st.Name = 'Australia' THEN 'Otoño'
            WHEN MONTH(soh.OrderDate) IN (6, 7, 8) AND st.Name = 'Australia' THEN 'Invierno'
            WHEN MONTH(soh.OrderDate) IN (9, 10, 11) AND st.Name = 'Australia' THEN 'Primavera'
        END AS Estacion,
        CASE 
            WHEN st.Name IN ('Northwest', 'Southwest', 'Southeast', 'Central', 'Northeast') THEN 'United States'
            ELSE st.Name
        END AS Territorio,
        COUNT(DISTINCT soh.SalesOrderID) AS CantidadVentas,
        SUM(sod.LineTotal) AS GananciaTotal,
        SUM(sod.LineTotal - (sod.UnitPrice * sod.OrderQty)) AS GananciaBruta,
        SUM(sod.OrderQty) AS ProductosVendidos
    FROM 
        Sales.SalesOrderHeader soh
    JOIN 
        Sales.SalesOrderDetail sod ON soh.SalesOrderID = sod.SalesOrderID
    JOIN 
        Sales.SalesTerritory st ON soh.TerritoryID = st.TerritoryID
    GROUP BY 
        YEAR(soh.OrderDate), 
        CASE 
            WHEN MONTH(soh.OrderDate) IN (12, 1, 2) AND st.Name <> 'Australia' THEN 'Invierno'
            WHEN MONTH(soh.OrderDate) IN (3, 4, 5) AND st.Name <> 'Australia' THEN 'Primavera'
            WHEN MONTH(soh.OrderDate) IN (6, 7, 8) AND st.Name <> 'Australia' THEN 'Verano'
            WHEN MONTH(soh.OrderDate) IN (9, 10, 11) AND st.Name <> 'Australia' THEN 'Otoño'
            WHEN MONTH(soh.OrderDate) IN (12, 1, 2) AND st.Name = 'Australia' THEN 'Verano'
            WHEN MONTH(soh.OrderDate) IN (3, 4, 5) AND st.Name = 'Australia' THEN 'Otoño'
            WHEN MONTH(soh.OrderDate) IN (6, 7, 8) AND st.Name = 'Australia' THEN 'Invierno'
            WHEN MONTH(soh.OrderDate) IN (9, 10, 11) AND st.Name = 'Australia' THEN 'Primavera'
        END,
        CASE 
            WHEN st.Name IN ('Northwest', 'Southwest', 'Southeast', 'Central', 'Northeast') THEN 'United States'
            ELSE st.Name
        END
),
CTE2 AS (
    SELECT 
        Estacion,
        Territorio,
        Año,
        CantidadVentas,
        GananciaTotal,
        GananciaBruta,
        ProductosVendidos,
        AVG(CantidadVentas) OVER (PARTITION BY Territorio) AS PromedioVentas,
        AVG(GananciaTotal) OVER (PARTITION BY Territorio) AS PromedioGananciaTotal,
        AVG(GananciaBruta) OVER (PARTITION BY Territorio) AS PromedioGananciaBruta,
        AVG(ProductosVendidos) OVER (PARTITION BY Territorio) AS PromedioProductosVendidos
    FROM CTE
)
SELECT 
    Estacion,
    Territorio,
    Año,
    CantidadVentas,
    GananciaTotal,
    GananciaBruta,
    ProductosVendidos,
    -- Cambios porcentuales respecto al promedio histórico del territorio
    CASE 
        WHEN PromedioVentas IS NOT NULL THEN (CantidadVentas - PromedioVentas) / PromedioVentas * 100
        ELSE NULL
    END AS VariacionVentas,
    CASE 
        WHEN PromedioGananciaTotal IS NOT NULL THEN (GananciaTotal - PromedioGananciaTotal) / PromedioGananciaTotal * 100
        ELSE NULL
    END AS VariacionGananciaTotal,
    CASE 
        WHEN PromedioGananciaBruta IS NOT NULL THEN (GananciaBruta - PromedioGananciaBruta) / PromedioGananciaBruta * 100
        ELSE NULL
    END AS VariacionGananciaBruta,
    CASE 
        WHEN PromedioProductosVendidos IS NOT NULL THEN (ProductosVendidos - PromedioProductosVendidos) / PromedioProductosVendidos * 100
        ELSE NULL
    END AS VariacionProductosVendidos
FROM 
    CTE2
ORDER BY 
    Estacion DESC, Año DESC, Territorio;
