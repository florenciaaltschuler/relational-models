SELECT
  r.Name AS Reason,
  COUNT(*) AS TotalReturns
FROM Sales.SalesOrderHeaderSalesReason sr
JOIN Sales.SalesReason r ON sr.SalesReasonID = r.SalesReasonID
GROUP BY r.Name
ORDER BY TotalReturns DESC;