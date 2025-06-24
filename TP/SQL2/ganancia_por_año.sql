WITH
    PeriodoOperacional
    AS
    (
        SELECT
            MIN(OrderDate) AS StartDate,
            MAX(OrderDate) AS EndDate
        FROM Sales.SalesOrderHeader
    ),

    Calendario
    AS
    (
                    SELECT
                po.StartDate AS fecha_cal,
                po.EndDate AS fechaFinal
            FROM PeriodoOperacional po
        UNION ALL
            SELECT
                DATEADD(DAY, 1, fecha_cal) AS fecha_cal,
                fechaFinal
            FROM Calendario
            WHERE fecha_cal < fechaFinal
    ),

    DiasPorAño
    AS
    (
        SELECT
            YEAR(fecha_cal) AS Año,
            COUNT(DISTINCT fecha_cal) AS CantDias
        FROM Calendario
        GROUP BY YEAR(fecha_cal)
    ),

    VentasAño
    AS
    (
        SELECT
            YEAR(soh.OrderDate) AS Año,
            st.Name AS Territorio,
            SUM(sod.LineTotal) AS VentaTotal
        FROM
            Sales.SalesOrderHeader soh
            JOIN Sales.SalesOrderDetail sod
            ON soh.SalesOrderID = sod.SalesOrderID
            JOIN Sales.SalesTerritory st
            ON soh.TerritoryID = st.TerritoryID
        GROUP BY 
            YEAR(soh.OrderDate), st.Name
    ),

    VentasAñoNormalizadas
    AS
    (
        SELECT
            va.Territorio,
            va.Año,
            CAST(va.VentaTotal / da.CantDias AS FLOAT) AS VentasNormalizadas
        FROM
            VentasAño va
            JOIN DiasPorAño da
            ON va.Año = da.Año
    )

SELECT
    Territorio,
    ISNULL([2011], 0) AS [2011],
    ISNULL([2012], 0) AS [2012],
    ISNULL([2013], 0) AS [2013],
    ISNULL([2014], 0) AS [2014]
FROM
    (    
    SELECT
        Territorio,
        Año,
        VentasNormalizadas
    FROM VentasAñoNormalizadas
) AS fuente
PIVOT (
    SUM(VentasNormalizadas)
    FOR Año IN ([2011], [2012], [2013], [2014])
) AS pvt
ORDER BY 
    Territorio

OPTION
(MAXRECURSION
0); 