
SELECT 
  ps.Name AS Subcategory,
  COUNT(*) AS ReturnCount
FROM Sales.SalesOrderHeaderSalesReason sr
JOIN Sales.SalesOrderHeader h ON sr.SalesOrderID = h.SalesOrderID
JOIN Sales.SalesOrderDetail d ON h.SalesOrderID = d.SalesOrderID
JOIN Production.Product p ON d.ProductID = p.ProductID
JOIN Production.ProductSubcategory ps ON p.ProductSubcategoryID = ps.ProductSubcategoryID
GROUP BY ps.Name
ORDER BY ReturnCount DESC;
