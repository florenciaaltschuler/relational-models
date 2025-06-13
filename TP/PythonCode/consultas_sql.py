import os

# Crear estructura de carpetas simulada
sql_path = os.path.join(os.path.dirname(__file__), '../SQL')



# Consultas SQL para análisis de logística y devoluciones
sql_queries = {
    "tiempo_entrega_por_pedido.sql": """
SELECT 
  SalesOrderID,
  DATEDIFF(DAY, OrderDate, ShipDate) AS DeliveryDays,
  TerritoryID,
  SalesPersonID
FROM Sales.SalesOrderHeader
WHERE ShipDate IS NOT NULL;
""",
    "motivos_devoluciones.sql": """
SELECT 
  r.Name AS Reason,
  COUNT(*) AS TotalReturns
FROM Sales.SalesOrderHeaderSalesReason sr
JOIN Sales.SalesReason r ON sr.SalesReasonID = r.SalesReasonID
GROUP BY r.Name
ORDER BY TotalReturns DESC;
""",
    "devoluciones_por_producto.sql": """
SELECT 
  p.Name AS Product,
  COUNT(*) AS ReturnCount
FROM Sales.SalesOrderHeaderSalesReason sr
JOIN Sales.SalesOrderHeader h ON sr.SalesOrderID = h.SalesOrderID
JOIN Sales.SalesOrderDetail d ON h.SalesOrderID = d.SalesOrderID
JOIN Production.Product p ON d.ProductID = p.ProductID
GROUP BY p.Name
ORDER BY ReturnCount DESC;
""",
    "devoluciones_por_territorio.sql": """
SELECT 
  t.Name AS Territory,
  COUNT(*) AS ReturnCount
FROM Sales.SalesOrderHeaderSalesReason sr
JOIN Sales.SalesOrderHeader h ON sr.SalesOrderID = h.SalesOrderID
JOIN Sales.SalesTerritory t ON h.TerritoryID = t.TerritoryID
GROUP BY t.Name
ORDER BY ReturnCount DESC;
""",
    "devoluciones_por_subcategoria.sql": """
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
""",
    "devoluciones_por_categoria.sql": """
SELECT 
  pc.Name AS Category,
  COUNT(*) AS ReturnCount
FROM Sales.SalesOrderHeaderSalesReason sr
JOIN Sales.SalesOrderHeader h ON sr.SalesOrderID = h.SalesOrderID
JOIN Sales.SalesOrderDetail d ON h.SalesOrderID = d.SalesOrderID
JOIN Production.Product p ON d.ProductID = p.ProductID
JOIN Production.ProductSubcategory ps ON p.ProductSubcategoryID = ps.ProductSubcategoryID
JOIN Production.ProductCategory pc ON ps.ProductCategoryID = pc.ProductCategoryID
GROUP BY pc.Name
ORDER BY ReturnCount DESC;
""",
    "tasa_devolucion_por_producto.sql": """
SELECT 
  p.Name AS Product,
  COUNT(DISTINCT sr.SalesOrderID) AS ReturnCount,
  COUNT(DISTINCT d_all.SalesOrderID) AS TotalSales,
  CAST(COUNT(DISTINCT sr.SalesOrderID) AS FLOAT) / NULLIF(COUNT(DISTINCT d_all.SalesOrderID), 0) AS ReturnRate
FROM Production.Product p
LEFT JOIN Sales.SalesOrderDetail d_all ON p.ProductID = d_all.ProductID
LEFT JOIN Sales.SalesOrderHeader h_all ON d_all.SalesOrderID = h_all.SalesOrderID
LEFT JOIN Sales.SalesOrderHeaderSalesReason sr ON h_all.SalesOrderID = sr.SalesOrderID
GROUP BY p.Name
HAVING COUNT(DISTINCT d_all.SalesOrderID) > 0
ORDER BY ReturnRate DESC;
""",
    "tasa_devolucion_por_subcategoria.sql": """
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
""",
    "tasa_devolucion_por_categoria.sql": """
SELECT 
  pc.Name AS Category,
  COUNT(DISTINCT sr.SalesOrderID) AS ReturnCount,
  COUNT(DISTINCT d_all.SalesOrderID) AS TotalSales,
  CAST(COUNT(DISTINCT sr.SalesOrderID) AS FLOAT) / NULLIF(COUNT(DISTINCT d_all.SalesOrderID), 0) AS ReturnRate
FROM Production.Product p
JOIN Production.ProductSubcategory ps ON p.ProductSubcategoryID = ps.ProductSubcategoryID
JOIN Production.ProductCategory pc ON ps.ProductCategoryID = pc.ProductCategoryID
LEFT JOIN Sales.SalesOrderDetail d_all ON p.ProductID = d_all.ProductID
LEFT JOIN Sales.SalesOrderHeader h_all ON d_all.SalesOrderID = h_all.SalesOrderID
LEFT JOIN Sales.SalesOrderHeaderSalesReason sr ON h_all.SalesOrderID = sr.SalesOrderID
GROUP BY pc.Name
HAVING COUNT(DISTINCT d_all.SalesOrderID) > 0
ORDER BY ReturnRate DESC;
""",
   "tasa_devolucion_por_territorio.sql": """
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
""",
"consulta_geo.sql": """SELECT 
    t.name AS TableName,
    c.name AS ColumnName,
    ty.name AS DataType
FROM sys.columns c
JOIN sys.tables t ON c.object_id = t.object_id
JOIN sys.types ty ON c.user_type_id = ty.user_type_id
WHERE ty.name IN ('geography', 'geometry');
""",
    "distancia_ventas_por_tienda.sql": """
-- Coordenadas de cada tienda
WITH Tiendas AS (
    SELECT 
        s.BusinessEntityID,
        s.Name AS StoreName,
        a.SpatialLocation AS StoreLocation,
        a.City AS StoreCity,
        sp.Name AS StoreState
    FROM Sales.Store s
    JOIN Person.BusinessEntityAddress bea ON s.BusinessEntityID = bea.BusinessEntityID
    JOIN Person.Address a ON bea.AddressID = a.AddressID
    JOIN Person.StateProvince sp ON a.StateProvinceID = sp.StateProvinceID
    WHERE a.SpatialLocation IS NOT NULL
),

-- Ventas con dirección de envío
Ventas AS (
    SELECT 
        h.SalesOrderID,
        c.StoreID,
        a.SpatialLocation AS DeliveryLocation,
        a.City AS DeliveryCity,
        sp.Name AS DeliveryState
    FROM Sales.SalesOrderHeader h
    JOIN Sales.Customer c ON h.CustomerID = c.CustomerID
    JOIN Person.Address a ON h.ShipToAddressID = a.AddressID
    JOIN Person.StateProvince sp ON a.StateProvinceID = sp.StateProvinceID
    WHERE c.StoreID IS NOT NULL AND a.SpatialLocation IS NOT NULL
)

-- Calcular distancia entre tienda y dirección de envío
SELECT 
    t.StoreName,
    t.StoreCity,
    t.StoreState,
    v.SalesOrderID,
    v.DeliveryCity,
    v.DeliveryState,
    t.StoreLocation.Lat AS StoreLat,
    t.StoreLocation.Long AS StoreLong,
    v.DeliveryLocation.Lat AS DeliveryLat,
    v.DeliveryLocation.Long AS DeliveryLong,
    t.StoreLocation.STDistance(v.DeliveryLocation) / 1000.0 AS DistanceKm
FROM Ventas v
JOIN Tiendas t ON v.StoreID = t.BusinessEntityID;
"""
}

# Guardar archivos SQL
for filename, content in sql_queries.items():
    with open(os.path.join(sql_path, filename), 'w', encoding='utf-8') as file:
        file.write(content)

# Mostrar rutas
sql_queries_files = list(sql_queries.keys())
sql_queries_files


SELECT 
  CAST(SUM(CASE WHEN sr.SalesOrderID IS NOT NULL THEN d.OrderQty ELSE 0 END) AS FLOAT) /
  NULLIF(SUM(d.OrderQty), 0) AS ReturnedRate
FROM Sales.SalesOrderDetail d
JOIN Sales.SalesOrderHeader h ON d.SalesOrderID = h.SalesOrderID
LEFT JOIN Sales.SalesOrderHeaderSalesReason sr ON h.SalesOrderID = sr.SalesOrderID;
