
SELECT 
  t.Name AS Territory,
  COUNT(DISTINCT sr.SalesOrderID) AS ReturnCount,
  COUNT(DISTINCT h_all.SalesOrderID) AS TotalSales,
  CAST(COUNT(DISTINCT sr.SalesOrderID) AS FLOAT) / NULLIF(COUNT(DISTINCT h_all.SalesOrderID), 0) AS ReturnRate
FROM Sales.SalesTerritory t
LEFT JOIN Sales.SalesOrderHeader h_all ON t.TerritoryID = h_all.TerritoryID
LEFT JOIN Sales.SalesOrderHeaderSalesReason sr ON h_all.SalesOrderID = sr.SalesOrderID
GROUP BY t.Name
HAVING COUNT(DISTINCT h_all.SalesOrderID) > 0
ORDER BY ReturnRate DESC;
