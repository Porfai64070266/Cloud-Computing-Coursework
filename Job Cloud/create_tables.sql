-- Create comm034_retail dataset tables with synthetic e-commerce data

-- Products table
CREATE OR REPLACE TABLE comm034_retail.products (
  id INT64,
  cost FLOAT64,
  category STRING,
  name STRING,
  brand STRING,
  retail_price FLOAT64,
  department STRING,
  sku STRING,
  distribution_center_id INT64
);

INSERT INTO comm034_retail.products (id, cost, category, name, brand, retail_price, department, sku, distribution_center_id)
VALUES
  (1, 5.50, 'Jeans', 'Classic Blue Jeans', 'Levi''s', 49.99, 'Men', 'LV-JN-001', 1),
  (2, 12.00, 'Tops & Tees', 'Cotton T-Shirt', 'H&M', 19.99, 'Women', 'HM-TS-002', 1),
  (3, 25.00, 'Sweaters', 'Wool Sweater', 'Zara', 79.99, 'Men', 'ZR-SW-003', 2),
  (4, 8.00, 'Pants', 'Casual Chinos', 'Gap', 39.99, 'Men', 'GP-PT-004', 1),
  (5, 15.00, 'Dresses', 'Summer Dress', 'Forever 21', 59.99, 'Women', 'F21-DR-005', 2),
  (6, 7.50, 'Tops & Tees', 'Graphic Tee', 'Uniqlo', 24.99, 'Women', 'UQ-TS-006', 1),
  (7, 30.00, 'Outerwear & Coats', 'Winter Jacket', 'North Face', 149.99, 'Men', 'NF-JK-007', 3),
  (8, 6.00, 'Socks', 'Cotton Socks 3-Pack', 'Nike', 14.99, 'Men', 'NK-SK-008', 1),
  (9, 20.00, 'Shoes', 'Running Shoes', 'Adidas', 89.99, 'Women', 'AD-SH-009', 2),
  (10, 10.00, 'Accessories', 'Leather Belt', 'Calvin Klein', 45.99, 'Men', 'CK-BL-010', 1);

-- Orders table
CREATE OR REPLACE TABLE comm034_retail.orders (
  order_id INT64,
  user_id INT64,
  status STRING,
  gender STRING,
  created_at TIMESTAMP,
  returned_at TIMESTAMP,
  shipped_at TIMESTAMP,
  delivered_at TIMESTAMP,
  num_of_item INT64
);

INSERT INTO comm034_retail.orders (order_id, user_id, status, gender, created_at, returned_at, shipped_at, delivered_at, num_of_item)
VALUES
  (1001, 501, 'Complete', 'M', TIMESTAMP('2024-01-15 10:30:00'), NULL, TIMESTAMP('2024-01-16 08:00:00'), TIMESTAMP('2024-01-18 14:30:00'), 2),
  (1002, 502, 'Complete', 'F', TIMESTAMP('2024-01-20 14:15:00'), NULL, TIMESTAMP('2024-01-21 09:00:00'), TIMESTAMP('2024-01-23 16:45:00'), 1),
  (1003, 503, 'Shipped', 'M', TIMESTAMP('2024-02-05 11:00:00'), NULL, TIMESTAMP('2024-02-06 07:30:00'), NULL, 3),
  (1004, 504, 'Complete', 'F', TIMESTAMP('2024-02-10 16:45:00'), NULL, TIMESTAMP('2024-02-11 10:00:00'), TIMESTAMP('2024-02-14 12:00:00'), 2),
  (1005, 505, 'Returned', 'M', TIMESTAMP('2024-03-01 09:20:00'), TIMESTAMP('2024-03-10 15:00:00'), TIMESTAMP('2024-03-02 08:00:00'), TIMESTAMP('2024-03-04 11:30:00'), 1),
  (1006, 506, 'Complete', 'F', TIMESTAMP('2024-03-15 13:30:00'), NULL, TIMESTAMP('2024-03-16 09:15:00'), TIMESTAMP('2024-03-19 17:00:00'), 4),
  (1007, 507, 'Processing', 'M', TIMESTAMP('2024-04-02 10:00:00'), NULL, NULL, NULL, 2),
  (1008, 508, 'Complete', 'F', TIMESTAMP('2024-04-10 15:45:00'), NULL, TIMESTAMP('2024-04-11 08:30:00'), TIMESTAMP('2024-04-13 14:15:00'), 1),
  (1009, 509, 'Cancelled', 'M', TIMESTAMP('2024-04-20 12:00:00'), NULL, NULL, NULL, 1),
  (1010, 510, 'Complete', 'F', TIMESTAMP('2024-05-05 11:30:00'), NULL, TIMESTAMP('2024-05-06 09:00:00'), TIMESTAMP('2024-05-08 16:30:00'), 3);

-- Order items table
CREATE OR REPLACE TABLE comm034_retail.order_items (
  id INT64,
  order_id INT64,
  user_id INT64,
  product_id INT64,
  inventory_item_id INT64,
  status STRING,
  created_at TIMESTAMP,
  shipped_at TIMESTAMP,
  delivered_at TIMESTAMP,
  returned_at TIMESTAMP,
  sale_price FLOAT64
);

INSERT INTO comm034_retail.order_items (id, order_id, user_id, product_id, inventory_item_id, status, created_at, shipped_at, delivered_at, returned_at, sale_price)
VALUES
  (2001, 1001, 501, 1, 3001, 'Complete', TIMESTAMP('2024-01-15 10:30:00'), TIMESTAMP('2024-01-16 08:00:00'), TIMESTAMP('2024-01-18 14:30:00'), NULL, 49.99),
  (2002, 1001, 501, 8, 3002, 'Complete', TIMESTAMP('2024-01-15 10:30:00'), TIMESTAMP('2024-01-16 08:00:00'), TIMESTAMP('2024-01-18 14:30:00'), NULL, 14.99),
  (2003, 1002, 502, 2, 3003, 'Complete', TIMESTAMP('2024-01-20 14:15:00'), TIMESTAMP('2024-01-21 09:00:00'), TIMESTAMP('2024-01-23 16:45:00'), NULL, 19.99),
  (2004, 1003, 503, 3, 3004, 'Shipped', TIMESTAMP('2024-02-05 11:00:00'), TIMESTAMP('2024-02-06 07:30:00'), NULL, NULL, 79.99),
  (2005, 1003, 503, 4, 3005, 'Shipped', TIMESTAMP('2024-02-05 11:00:00'), TIMESTAMP('2024-02-06 07:30:00'), NULL, NULL, 39.99),
  (2006, 1003, 503, 10, 3006, 'Shipped', TIMESTAMP('2024-02-05 11:00:00'), TIMESTAMP('2024-02-06 07:30:00'), NULL, NULL, 45.99),
  (2007, 1004, 504, 5, 3007, 'Complete', TIMESTAMP('2024-02-10 16:45:00'), TIMESTAMP('2024-02-11 10:00:00'), TIMESTAMP('2024-02-14 12:00:00'), NULL, 59.99),
  (2008, 1004, 504, 6, 3008, 'Complete', TIMESTAMP('2024-02-10 16:45:00'), TIMESTAMP('2024-02-11 10:00:00'), TIMESTAMP('2024-02-14 12:00:00'), NULL, 24.99),
  (2009, 1005, 505, 7, 3009, 'Returned', TIMESTAMP('2024-03-01 09:20:00'), TIMESTAMP('2024-03-02 08:00:00'), TIMESTAMP('2024-03-04 11:30:00'), TIMESTAMP('2024-03-10 15:00:00'), 149.99),
  (2010, 1006, 506, 1, 3010, 'Complete', TIMESTAMP('2024-03-15 13:30:00'), TIMESTAMP('2024-03-16 09:15:00'), TIMESTAMP('2024-03-19 17:00:00'), NULL, 49.99),
  (2011, 1006, 506, 2, 3011, 'Complete', TIMESTAMP('2024-03-15 13:30:00'), TIMESTAMP('2024-03-16 09:15:00'), TIMESTAMP('2024-03-19 17:00:00'), NULL, 19.99),
  (2012, 1006, 506, 9, 3012, 'Complete', TIMESTAMP('2024-03-15 13:30:00'), TIMESTAMP('2024-03-16 09:15:00'), TIMESTAMP('2024-03-19 17:00:00'), NULL, 89.99),
  (2013, 1006, 506, 10, 3013, 'Complete', TIMESTAMP('2024-03-15 13:30:00'), TIMESTAMP('2024-03-16 09:15:00'), TIMESTAMP('2024-03-19 17:00:00'), NULL, 45.99),
  (2014, 1007, 507, 3, 3014, 'Processing', TIMESTAMP('2024-04-02 10:00:00'), NULL, NULL, NULL, 79.99),
  (2015, 1007, 507, 4, 3015, 'Processing', TIMESTAMP('2024-04-02 10:00:00'), NULL, NULL, NULL, 39.99),
  (2016, 1008, 508, 5, 3016, 'Complete', TIMESTAMP('2024-04-10 15:45:00'), TIMESTAMP('2024-04-11 08:30:00'), TIMESTAMP('2024-04-13 14:15:00'), NULL, 59.99),
  (2017, 1009, 509, 6, 3017, 'Cancelled', TIMESTAMP('2024-04-20 12:00:00'), NULL, NULL, NULL, 24.99),
  (2018, 1010, 510, 1, 3018, 'Complete', TIMESTAMP('2024-05-05 11:30:00'), TIMESTAMP('2024-05-06 09:00:00'), TIMESTAMP('2024-05-08 16:30:00'), NULL, 49.99),
  (2019, 1010, 510, 7, 3019, 'Complete', TIMESTAMP('2024-05-05 11:30:00'), TIMESTAMP('2024-05-06 09:00:00'), TIMESTAMP('2024-05-08 16:30:00'), NULL, 149.99),
  (2020, 1010, 510, 9, 3020, 'Complete', TIMESTAMP('2024-05-05 11:30:00'), TIMESTAMP('2024-05-06 09:00:00'), TIMESTAMP('2024-05-08 16:30:00'), NULL, 89.99);

-- Events table
CREATE OR REPLACE TABLE comm034_retail.events (
  id INT64,
  user_id INT64,
  sequence_number INT64,
  session_id STRING,
  created_at TIMESTAMP,
  ip_address STRING,
  city STRING,
  state STRING,
  postal_code STRING,
  browser STRING,
  traffic_source STRING,
  uri STRING,
  event_type STRING,
  event_time TIMESTAMP
);

INSERT INTO comm034_retail.events (id, user_id, sequence_number, session_id, created_at, ip_address, city, state, postal_code, browser, traffic_source, uri, event_type, event_time)
VALUES
  (5001, 501, 1, 'sess-501-1', TIMESTAMP('2024-01-15 10:25:00'), '203.0.113.45', 'Bangkok', 'Bangkok', '10110', 'Chrome', 'Search', '/products/1', 'view', TIMESTAMP('2024-01-15 10:25:00')),
  (5002, 501, 2, 'sess-501-1', TIMESTAMP('2024-01-15 10:28:00'), '203.0.113.45', 'Bangkok', 'Bangkok', '10110', 'Chrome', 'Search', '/products/8', 'view', TIMESTAMP('2024-01-15 10:28:00')),
  (5003, 501, 3, 'sess-501-1', TIMESTAMP('2024-01-15 10:30:00'), '203.0.113.45', 'Bangkok', 'Bangkok', '10110', 'Chrome', 'Search', '/cart', 'purchase', TIMESTAMP('2024-01-15 10:30:00')),
  (5004, 502, 1, 'sess-502-1', TIMESTAMP('2024-01-20 14:10:00'), '198.51.100.22', 'Chiang Mai', 'Chiang Mai', '50000', 'Firefox', 'Email', '/products/2', 'view', TIMESTAMP('2024-01-20 14:10:00')),
  (5005, 502, 2, 'sess-502-1', TIMESTAMP('2024-01-20 14:15:00'), '198.51.100.22', 'Chiang Mai', 'Chiang Mai', '50000', 'Firefox', 'Email', '/cart', 'purchase', TIMESTAMP('2024-01-20 14:15:00')),
  (5006, 503, 1, 'sess-503-1', TIMESTAMP('2024-02-05 10:55:00'), '192.0.2.101', 'Phuket', 'Phuket', '83000', 'Safari', 'Organic', '/products/3', 'view', TIMESTAMP('2024-02-05 10:55:00')),
  (5007, 503, 2, 'sess-503-1', TIMESTAMP('2024-02-05 10:58:00'), '192.0.2.101', 'Phuket', 'Phuket', '83000', 'Safari', 'Organic', '/products/4', 'view', TIMESTAMP('2024-02-05 10:58:00')),
  (5008, 503, 3, 'sess-503-1', TIMESTAMP('2024-02-05 11:00:00'), '192.0.2.101', 'Phuket', 'Phuket', '83000', 'Safari', 'Organic', '/cart', 'purchase', TIMESTAMP('2024-02-05 11:00:00')),
  (5009, 504, 1, 'sess-504-1', TIMESTAMP('2024-02-10 16:40:00'), '203.0.113.78', 'Bangkok', 'Bangkok', '10110', 'Chrome', 'Social', '/products/5', 'view', TIMESTAMP('2024-02-10 16:40:00')),
  (5010, 504, 2, 'sess-504-1', TIMESTAMP('2024-02-10 16:45:00'), '203.0.113.78', 'Bangkok', 'Bangkok', '10110', 'Chrome', 'Social', '/cart', 'purchase', TIMESTAMP('2024-02-10 16:45:00')),
  (5011, 505, 1, 'sess-505-1', TIMESTAMP('2024-03-01 09:15:00'), '198.51.100.55', 'Pattaya', 'Chonburi', '20150', 'Edge', 'Display', '/products/7', 'view', TIMESTAMP('2024-03-01 09:15:00')),
  (5012, 505, 2, 'sess-505-1', TIMESTAMP('2024-03-01 09:20:00'), '198.51.100.55', 'Pattaya', 'Chonburi', '20150', 'Edge', 'Display', '/cart', 'purchase', TIMESTAMP('2024-03-01 09:20:00')),
  (5013, 506, 1, 'sess-506-1', TIMESTAMP('2024-03-15 13:20:00'), '192.0.2.133', 'Chiang Rai', 'Chiang Rai', '57000', 'Chrome', 'Search', '/products/1', 'view', TIMESTAMP('2024-03-15 13:20:00')),
  (5014, 506, 2, 'sess-506-1', TIMESTAMP('2024-03-15 13:25:00'), '192.0.2.133', 'Chiang Rai', 'Chiang Rai', '57000', 'Chrome', 'Search', '/products/9', 'view', TIMESTAMP('2024-03-15 13:25:00')),
  (5015, 506, 3, 'sess-506-1', TIMESTAMP('2024-03-15 13:30:00'), '192.0.2.133', 'Chiang Rai', 'Chiang Rai', '57000', 'Chrome', 'Search', '/cart', 'purchase', TIMESTAMP('2024-03-15 13:30:00')),
  (5016, 507, 1, 'sess-507-1', TIMESTAMP('2024-04-02 09:55:00'), '203.0.113.99', 'Bangkok', 'Bangkok', '10110', 'Firefox', 'Organic', '/products/3', 'view', TIMESTAMP('2024-04-02 09:55:00')),
  (5017, 507, 2, 'sess-507-1', TIMESTAMP('2024-04-02 10:00:00'), '203.0.113.99', 'Bangkok', 'Bangkok', '10110', 'Firefox', 'Organic', '/cart', 'purchase', TIMESTAMP('2024-04-02 10:00:00')),
  (5018, 508, 1, 'sess-508-1', TIMESTAMP('2024-04-10 15:40:00'), '198.51.100.144', 'Krabi', 'Krabi', '81000', 'Safari', 'Email', '/products/5', 'view', TIMESTAMP('2024-04-10 15:40:00')),
  (5019, 508, 2, 'sess-508-1', TIMESTAMP('2024-04-10 15:45:00'), '198.51.100.144', 'Krabi', 'Krabi', '81000', 'Safari', 'Email', '/cart', 'purchase', TIMESTAMP('2024-04-10 15:45:00')),
  (5020, 509, 1, 'sess-509-1', TIMESTAMP('2024-04-20 11:55:00'), '192.0.2.167', 'Surat Thani', 'Surat Thani', '84000', 'Chrome', 'Social', '/products/6', 'view', TIMESTAMP('2024-04-20 11:55:00')),
  (5021, 509, 2, 'sess-509-1', TIMESTAMP('2024-04-20 12:00:00'), '192.0.2.167', 'Surat Thani', 'Surat Thani', '84000', 'Chrome', 'Social', '/cart', 'cancel', TIMESTAMP('2024-04-20 12:00:00')),
  (5022, 510, 1, 'sess-510-1', TIMESTAMP('2024-05-05 11:20:00'), '203.0.113.211', 'Bangkok', 'Bangkok', '10110', 'Edge', 'Search', '/products/1', 'view', TIMESTAMP('2024-05-05 11:20:00')),
  (5023, 510, 2, 'sess-510-1', TIMESTAMP('2024-05-05 11:25:00'), '203.0.113.211', 'Bangkok', 'Bangkok', '10110', 'Edge', 'Search', '/products/7', 'view', TIMESTAMP('2024-05-05 11:25:00')),
  (5024, 510, 3, 'sess-510-1', TIMESTAMP('2024-05-05 11:30:00'), '203.0.113.211', 'Bangkok', 'Bangkok', '10110', 'Edge', 'Search', '/cart', 'purchase', TIMESTAMP('2024-05-05 11:30:00'));
