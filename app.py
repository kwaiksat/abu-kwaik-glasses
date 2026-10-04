import os

from flask import Flask, render_template

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "ghayth-al-majd-secret-key"
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return """
    <!doctype html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <meta name="description"
              content="عن غيث المجد وأهداف الموقع وطريقة استخدامه">

        <title>عن غيث المجد</title>

        <style>
            body {
                margin: 0;
                background: #f5f5f5;
                color: #111;
                font-family: Arial, Tahoma, sans-serif;
                line-height: 2;
            }

            .page {
                width: min(100% - 30px, 900px);
                margin: 30px auto;
            }

            .box {
                background: #fff;
                padding: 25px;
                margin-bottom: 18px;
                border-radius: 18px;
                border: 1px solid #e5e5e5;
                box-shadow: 0 8px 25px rgba(0, 0, 0, .07);
            }

            h1, h2 {
                color: #111;
            }

            h1 {
                text-align: center;
                font-size: 32px;
            }

            h2 {
                font-size: 22px;
            }

            p {
                color: #444;
            }

            a {
                display: inline-block;
                margin-top: 10px;
                padding: 11px 20px;
                background: #111;
                color: #fff;
                text-decoration: none;
                border-radius: 10px;
                font-weight: bold;
            }
        </style>
    </head>

    <body>
        <main class="page">

            <div class="box">
                <h1>عن غيث المجد</h1>

                <p>
                    دليل مستقل للمساعدات والخدمات الإنسانية
                    والتعليمية.
                </p>
            </div>

            <div class="box">
                <h2>ما هو غيث المجد؟</h2>

                <p>
                    غيث المجد هو دليل مستقل يهدف إلى تنظيم
                    وتجميع روابط المساعدات والخدمات الإنسانية
                    والتعليمية المتاحة للعائلات والأفراد
                    في قطاع غزة وفلسطين.
                </p>

                <p>
                    يساعد الموقع المستخدم على الوصول إلى
                    الروابط والنماذج الرسمية بصورة أوضح،
                    مع التنبيه إلى ضرورة التأكد من مصدر
                    أي رابط قبل إدخال البيانات الشخصية.
                </p>
            </div>

            <div class="box">
                <h2>هدف الموقع</h2>

                <p>
                    يهدف غيث المجد إلى تسهيل الوصول إلى
                    المعلومات والروابط الرسمية المتعلقة
                    بالمساعدات والخدمات وتقليل صعوبة البحث
                    بين الروابط المتعددة.
                </p>
            </div>

            <div class="box">
                <h2>تنبيه مهم</h2>

                <p>
                    غيث المجد ليس جهة مانحة ولا يستلم أموالًا
                    من المستفيدين، ولا يطلب رسومًا مقابل
                    الوصول إلى روابط المساعدات.
                </p>

                <p>
                    يجب دائمًا مراجعة الجهة الرسمية قبل
                    مشاركة أي بيانات شخصية.
                </p>
            </div>

            <div class="box">
                <h2>الخصوصية والأمان</h2>

                <p>
                    لا ينبغي إدخال كلمات المرور أو البيانات
                    البنكية أو أي معلومات حساسة في أي رابط
                    قبل التأكد من أن الرابط تابع للجهة
                    الرسمية المعنية.
                </p>
            </div>

            <div class="box">
                <h2>التواصل</h2>

                <p>
                    واتساب / هاتف:
                    <strong>0592480001</strong>
                </p>

                <p>
                    البريد الإلكتروني:
                    <a href="mailto:n299964@hotmail.com">
                        n299964@hotmail.com
                    </a>
                </p>

                <p>
                    البريد الإلكتروني:
                    <a href="mailto:zaeemkwaik@gmail.com">
                        zaeemkwaik@gmail.com
                    </a>
                </p>

                <a href="/">
                    العودة إلى الصفحة الرئيسية
                </a>
            </div>

        </main>
    </body>
    </html>
    """


@app.route("/privacy")
def privacy():
    return """
    <!doctype html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <meta name="description"
              content="سياسة الخصوصية لموقع غيث المجد">

        <title>سياسة الخصوصية - غيث المجد</title>

        <style>
            body {
                margin: 0;
                background: #f5f5f5;
                color: #111;
                font-family: Arial, Tahoma, sans-serif;
                line-height: 2;
            }

            .page {
                width: min(100% - 30px, 900px);
                margin: 30px auto;
            }

            .box {
                background: #fff;
                padding: 25px;
                border-radius: 18px;
                border: 1px solid #e5e5e5;
                box-shadow: 0 8px 25px rgba(0, 0, 0, .07);
            }

            h1, h2 {
                color: #111;
            }

            h1 {
                text-align: center;
            }

            p {
                color: #444;
            }

            a {
                display: inline-block;
                margin-top: 15px;
                padding: 11px 20px;
                background: #111;
                color: #fff;
                text-decoration: none;
                border-radius: 10px;
                font-weight: bold;
            }
        </style>
    </head>

    <body>
        <main class="page">

            <div class="box">

                <h1>سياسة الخصوصية</h1>

                <h2>مقدمة</h2>

                <p>
                    نحترم خصوصية زوار موقع غيث المجد،
                    ونسعى إلى توضيح كيفية التعامل مع المعلومات
                    أثناء استخدام الموقع.
                </p>

                <h2>المعلومات الشخصية</h2>

                <p>
                    غيث المجد لا يطلب من الزوار إدخال كلمات
                    المرور أو البيانات البنكية أو المعلومات
                    الحساسة داخل الموقع.
                </p>

                <h2>الروابط الخارجية</h2>

                <p>
                    يحتوي الموقع على روابط لجهات ومؤسسات
                    خارجية. عند الانتقال إلى أي رابط خارجي،
                    يصبح المستخدم خاضعًا لسياسة الخصوصية
                    وشروط استخدام الجهة الخارجية.
                </p>

                <h2>ملفات تعريف الارتباط والإعلانات</h2>

                <p>
                    قد يستخدم الموقع خدمات خارجية، بما في ذلك
                    خدمات الإعلانات والتحليلات، وقد تستخدم هذه
                    الخدمات ملفات تعريف الارتباط وفقًا لسياساتها
                    الخاصة.
                </p>

                <h2>أمان المستخدم</h2>

                <p>
                    ننصح دائمًا بالتأكد من عنوان الموقع والجهة
                    الرسمية قبل مشاركة أي معلومات شخصية.
                </p>

                <h2>التواصل</h2>

                <p>
                    للاستفسارات المتعلقة بالخصوصية:
                </p>

                <p>
                    <a href="mailto:n299964@hotmail.com">
                        n299964@hotmail.com
                    </a>
                </p>

                <a href="/">
                    العودة إلى الصفحة الرئيسية
                </a>

            </div>

        </main>
    </body>
    </html>
    """


@app.route("/health")
def health():
    return "OK", 200


@app.errorhandler(404)
def page_not_found(error):
    return """
    <!doctype html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="utf-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1">

        <title>الصفحة غير موجودة - غيث المجد</title>

        <style>
            body {
                margin: 0;
                padding: 30px;
                background: #f5f5f5;
                color: #222;
                font-family: Arial, Tahoma, sans-serif;
                text-align: center;
            }

            .box {
                max-width: 600px;
                margin: 80px auto;
                padding: 35px 20px;
                background: #ffffff;
                border-radius: 18px;
                border: 1px solid #e2e2e2;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
            }

            h1 {
                color: #111111;
            }

            p {
                color: #666666;
                line-height: 1.8;
            }

            a {
                display: inline-block;
                margin-top: 15px;
                padding: 12px 24px;
                background: #111111;
                color: #ffffff;
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
                العودة إلى غيث المجد
            </a>

        </div>

    </body>
    </html>
    """, 404


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
