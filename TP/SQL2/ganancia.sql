SELECT 
    st.Name AS Territorio,  -- Nombre del territorio
    SUM(sod.LineTotal) AS GananciaTotal  -- Suma total de la venta (LineTotal)
FROM 
    Sales.SalesOrderHeader soh  -- Cabeceras de las órdenes de venta
JOIN 
    Sales.SalesOrderDetail sod ON soh.SalesOrderID = sod.SalesOrderID  -- Detalles de las órdenes de venta
JOIN 
    Sales.SalesTerritory st ON soh.TerritoryID = st.TerritoryID  -- Territorios
GROUP BY 
    st.Name  -- Agrupar por territorio
ORDER BY 
    GananciaTotal DESC;  -- Ordenar de mayor a menor ganancia
