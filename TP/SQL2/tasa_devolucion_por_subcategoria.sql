SELECT
  ps.Name AS Subcategory,
  COUNT(DISTINCT sr.SalesOrderID) AS ReturnCount,
  COUNT(DISTINCT d_all.SalesOrderID) AS TotalSales,
  CAST(COUNT(DISTINCT sr.SalesOrderID) AS FLOAT) / NULLIF(COUNT(DISTINCT d_all.SalesOrderID), 0) AS ReturnRate
FROM Production.Product p
JOIN Production.ProductSubcategory ps ON p.ProductSubcategoryID = ps.ProductSubcategoryID
LEFT JOIN Sales.SalesOrderDetail d_all ON p.ProductID = d_all.ProductID
LEFT JOIN Sales.SalesOrderHeader h_all ON d_all.SalesOrderID = h_all.SalesOrderID
LEFT JOIN Sales.SalesOrderHeaderSalesReason sr ON h_all.SalesOrderID = sr.SalesOrderID
GROUP BY ps.Name
HAVING COUNT(DISTINCT d_all.SalesOrderID) > 0
ORDER BY ReturnRate DESC;