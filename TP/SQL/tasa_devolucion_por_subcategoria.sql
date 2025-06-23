
SELECT
  ps.Name AS Subcategory,
  COUNT(sr.SalesOrderID) AS ReturnCount,
  COUNT(d_all.SalesOrderID) AS TotalSold,
  CAST(COUNT(sr.SalesOrderID) AS FLOAT) / NULLIF(COUNT(d_all.SalesOrderID), 0) AS ReturnRate
FROM Production.Product p
JOIN Production.ProductSubcategory ps ON p.ProductSubcategoryID = ps.ProductSubcategoryID

-- Ventas totales (detalle)
LEFT JOIN Sales.SalesOrderDetail d_all ON p.ProductID = d_all.ProductID

-- Detalles que fueron devueltos
LEFT JOIN Sales.SalesOrderHeader h_all ON d_all.SalesOrderID = h_all.SalesOrderID
LEFT JOIN Sales.SalesOrderHeaderSalesReason sr ON h_all.SalesOrderID = sr.SalesOrderID

GROUP BY ps.Name
HAVING COUNT(d_all.SalesOrderID) > 0 AND 
COUNT(sr.SalesOrderID) > 0 

ORDER BY ReturnRate DESC;

