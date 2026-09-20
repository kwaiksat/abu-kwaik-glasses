import os

from flask import Flask, render_template


# =========================================================
# APPLICATION
# =========================================================

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "majd-al-khair-platform-secret-key"
)


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def index():
    return render_template("index.html")


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health():
    return "OK", 200


# =========================================================
# ERROR PAGES
# =========================================================

@app.errorhandler(404)
def page_not_found(error):
    return """
    <!doctype html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="utf-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1">
        <title>الصفحة غير موجودة - منصة مجد الخير</title>
        <style>
            body {
                margin: 0;
                padding: 30px;
                background: #f7f7f5;
                color: #222;
                font-family:
                    "Noto Naskh Arabic",
                    "Noto Sans Arabic",
                    "Segoe UI",
                    Tahoma,
                    Arial,
                    sans-serif;
                text-align: center;
            }

            .box {
                max-width: 600px;
                margin: 80px auto;
                padding: 35px 20px;
                background: #ffffff;
                border-radius: 18px;
                border: 1px solid #e2e2e2;
                box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            }

            h1 {
                color: #111111;
            }

            p {
                color: #666666;
            }

            a {
                display: inline-block;
                margin-top: 15px;
                padding: 12px 24px;
                background: #c9a227;
                color: #111111;
                text-decoration: none;
                border-radius: 10px;
                font-weight: bold;
            }
        </style>
    </head>

    <body>
        <div class="box">
            <h1>الصفحة غير موجودة</h1>
            <p>
                عذرًا، الصفحة التي تبحث عنها غير متوفرة.
            </p>

            <a href="/">
                العودة إلى منصة مجد الخير
            </a>
        </div>
    </body>
    </html>
    """, 404


# =========================================================
# SERVER
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
