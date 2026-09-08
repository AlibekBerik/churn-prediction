WITH reference_date AS (
    SELECT MAX(order_date) AS max_date FROM orders
),

customer_orders AS (
    SELECT
        customer_id,
        order_id,
        order_date,
        quantity * price AS line_total
    FROM orders
),

rfm_raw AS (
    SELECT
        customer_id,
        MAX(order_date) AS last_order_date,
        COUNT(DISTINCT order_id) AS frequency,
        SUM(line_total) AS monetary
    FROM customer_orders
    GROUP BY customer_id
)

SELECT
    customer_id,
    frequency,
    ROUND(monetary, 2) AS monetary,
    CAST(julianday((SELECT max_date FROM reference_date)) - julianday(last_order_date) AS INTEGER) AS recency_days,
    CASE
        WHEN CAST(julianday((SELECT max_date FROM reference_date)) - julianday(last_order_date) AS INTEGER) > 365
        THEN 1 ELSE 0
    END AS churned
FROM rfm_raw;