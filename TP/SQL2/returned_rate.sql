SELECT
  CAST(SUM(CASE WHEN sr.SalesOrderID IS NOT NULL THEN d.OrderQty ELSE 0 END) AS FLOAT) /
  NULLIF(SUM(d.OrderQty), 0) AS ReturnedRate
FROM Sales.SalesOrderDetail d
JOIN Sales.SalesOrderHeader h ON d.SalesOrderID = h.SalesOrderID
LEFT JOIN Sales.SalesOrderHeaderSalesReason sr ON h.SalesOrderID = sr.SalesOrderID;