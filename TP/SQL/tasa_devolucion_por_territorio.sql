
SELECT
  CASE 
    WHEN st.Name IN ('Northwest', 'Southwest', 'Southeast', 'Central', 'Northeast') THEN 'United States'
    ELSE st.Name
  END AS Territory,
  COUNT(sr.SalesOrderID) AS ReturnCount,
  COUNT(d_all.SalesOrderID) AS TotalSold,
  CAST(COUNT(sr.SalesOrderID) AS FLOAT) / NULLIF(COUNT(d_all.SalesOrderID), 0) AS ReturnRate
FROM Sales.SalesOrderDetail d_all
JOIN Production.Product p ON d_all.ProductID = p.ProductID
JOIN Sales.SalesOrderHeader h_all ON d_all.SalesOrderID = h_all.SalesOrderID
JOIN Sales.SalesTerritory st ON h_all.TerritoryID = st.TerritoryID
LEFT JOIN Sales.SalesOrderHeaderSalesReason sr ON h_all.SalesOrderID = sr.SalesOrderID

GROUP BY 
  CASE 
    WHEN st.Name IN ('Northwest', 'Southwest', 'Southeast', 'Central', 'Northeast') THEN 'United States'
    ELSE st.Name
  END

HAVING COUNT(d_all.SalesOrderID) > 0 AND COUNT(sr.SalesOrderID) > 0
ORDER BY ReturnRate DESC;

