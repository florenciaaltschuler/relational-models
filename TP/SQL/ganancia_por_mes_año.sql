SELECT 
    YEAR(soh.OrderDate) AS Año,
    MONTH(soh.OrderDate) AS Mes,
    st.Name AS Territorio,
    SUM(sod.LineTotal) AS VentaTotal
FROM 
    Sales.SalesOrderHeader soh
JOIN 
    Sales.SalesOrderDetail sod ON soh.SalesOrderID = sod.SalesOrderID
JOIN 
    Sales.SalesTerritory st ON soh.TerritoryID = st.TerritoryID
GROUP BY 
    YEAR(soh.OrderDate), MONTH(soh.OrderDate), st.Name
ORDER BY 
    Año DESC, Mes DESC, VentaTotal DESC;
