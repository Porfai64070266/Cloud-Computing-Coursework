from flask import Flask, render_template, request, jsonify
from google.cloud import bigquery
import os

app = Flask(__name__)
client = bigquery.Client()

def _table_ref(default: str, env_key: str) -> str:
        # Returns a fully qualified table name from env var if provided, else default
        override = os.getenv(env_key)
        return override if override else default

# Allow overriding dataset/tables via env vars from Jump Start deployment
TBL_ORDER_ITEMS = _table_ref("bigquery-public-data.thelook_ecommerce.order_items", "BQ_TABLE_ORDER_ITEMS")
TBL_ORDERS = _table_ref("bigquery-public-data.thelook_ecommerce.orders", "BQ_TABLE_ORDERS")
TBL_EVENTS = _table_ref("bigquery-public-data.thelook_ecommerce.events", "BQ_TABLE_EVENTS")
TBL_PRODUCTS = _table_ref("bigquery-public-data.thelook_ecommerce.products", "BQ_TABLE_PRODUCTS")

def build_queries():
        return {
                                "monthly_revenue": {
                                                "label": "Monthly revenue by category",
                                                "sql": f"""
                                                SELECT
                                                        FORMAT_TIMESTAMP('%Y-%m', oi.created_at) AS month,
                                                        p.category AS category,
                                                        ROUND(SUM(oi.sale_price), 2) AS revenue
                                                FROM `{TBL_ORDER_ITEMS}` oi
                                                LEFT JOIN `{TBL_PRODUCTS}` p
                                                    ON oi.product_id = p.id
                                                GROUP BY month, category
                                                ORDER BY month DESC, revenue DESC
                                                LIMIT 200
                                                """
                                },
                "top_customers": {
                        "label": "Top 10 customers by lifetime spend",
                        "sql": f"""
                        SELECT
                            oi.user_id,
                            ROUND(SUM(oi.sale_price), 2) AS lifetime_spend
                        FROM `{TBL_ORDER_ITEMS}` oi
                        GROUP BY user_id
                        ORDER BY lifetime_spend DESC
                        LIMIT 10
                        """
                },
                "funnel_month": {
                        "label": "Monthly views vs orders (funnel)",
                        "sql": f"""
                        WITH views AS (
                            SELECT FORMAT_TIMESTAMP('%Y-%m', event_time) AS month, COUNT(*) AS view_events
                            FROM `{TBL_EVENTS}`
                            WHERE event_type = 'view'
                            GROUP BY month
                        ), orders AS (
                            SELECT FORMAT_TIMESTAMP('%Y-%m', created_at) AS month, COUNT(*) AS order_count
                            FROM `{TBL_ORDERS}`
                            GROUP BY month
                        )
                        SELECT v.month,
                                     v.view_events,
                                     o.order_count,
                                     SAFE_DIVIDE(o.order_count, v.view_events) AS order_rate
                        FROM views v
                        LEFT JOIN orders o USING (month)
                        ORDER BY v.month DESC
                        """
                }
        }

@app.route('/', methods=['GET', 'POST'])
def index():
    queries = build_queries()
    result_rows = []
    selected_key = None
    if request.method == 'POST':
        selected_key = request.form.get('query_key')
        if selected_key in queries:
            query = queries[selected_key]['sql']
            job = client.query(query)
            result_rows = [dict(row) for row in job.result()]
    return render_template('index.html', queries=queries, selected_key=selected_key, rows=result_rows)

@app.route('/health', methods=['GET'])
def health():
    # Simple health check
    try:
        client.query("SELECT 1").result()
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
