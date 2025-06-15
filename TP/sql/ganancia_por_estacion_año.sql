WITH CTE AS (
    SELECT 
        YEAR(soh.OrderDate) AS Año,
        CASE 
            WHEN MONTH(soh.OrderDate) IN (12, 1, 2) AND st.Name <> 'Australia' THEN 'Invierno'
            WHEN MONTH(soh.OrderDate) IN (3, 4, 5) AND st.Name <> 'Australia' THEN 'Primavera'
            WHEN MONTH(soh.OrderDate) IN (6, 7, 8) AND st.Name <> 'Australia' THEN 'Verano'
            WHEN MONTH(soh.OrderDate) IN (9, 10, 11) AND st.Name <> 'Australia' THEN 'Otoño'
            
            -- Para Australia, invertir las estaciones
            WHEN MONTH(soh.OrderDate) IN (12, 1, 2) AND st.Name = 'Australia' THEN 'Verano'
            WHEN MONTH(soh.OrderDate) IN (3, 4, 5) AND st.Name = 'Australia' THEN 'Otoño'
            WHEN MONTH(soh.OrderDate) IN (6, 7, 8) AND st.Name = 'Australia' THEN 'Invierno'
            WHEN MONTH(soh.OrderDate) IN (9, 10, 11) AND st.Name = 'Australia' THEN 'Primavera'
        END AS Estacion,
        -- Agrupamos todos los territorios de EE. UU. como 'United States'
        CASE 
            WHEN st.Name IN ('Northwest', 'Southwest', 'Southeast', 'Central', 'Northeast') THEN 'United States'
            ELSE st.Name
        END AS Territorio,
        SUM(sod.LineTotal) AS VentaTotal
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
        VentaTotal,
        -- Calcular la venta promedio de cada territorio (base)
        AVG(VentaTotal) OVER (PARTITION BY Territorio) AS VentaPromedio
    FROM CTE
)
-- Ahora calculamos el cambio porcentual respecto a la venta promedio de cada territorio
SELECT 
    Estacion,
    Territorio,
    Año,
    VentaTotal,
    -- Calcular el cambio porcentual respecto a la venta promedio
    CASE 
        WHEN VentaPromedio IS NOT NULL THEN (VentaTotal - VentaPromedio) / VentaPromedio * 100
        ELSE NULL
    END AS CambioPorcentual
FROM 
    CTE2
ORDER BY 
    Estacion DESC, Año DESC, Territorio;