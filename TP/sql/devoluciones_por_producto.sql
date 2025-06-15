SELECT
  p.Name AS Product,
  COUNT(*) AS ReturnCount
FROM Sales.SalesOrderHeaderSalesReason sr
JOIN Sales.SalesOrderHeader h ON sr.SalesOrderID = h.SalesOrderID
JOIN Sales.SalesOrderDetail d ON h.SalesOrderID = d.SalesOrderID
JOIN Production.Product p ON d.ProductID = p.ProductID
GROUP BY p.Name
ORDER BY ReturnCount DESC;