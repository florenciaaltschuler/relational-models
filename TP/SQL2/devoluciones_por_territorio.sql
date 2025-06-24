SELECT
  t.Name AS Territory,
  COUNT(*) AS ReturnCount
FROM Sales.SalesOrderHeaderSalesReason sr
JOIN Sales.SalesOrderHeader h ON sr.SalesOrderID = h.SalesOrderID
JOIN Sales.SalesTerritory t ON h.TerritoryID = t.TerritoryID
GROUP BY t.Name
ORDER BY ReturnCount DESC;