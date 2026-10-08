import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "ghayth-al-majd-secret-key"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ads.txt")
def ads_txt():
    return send_from_directory(
        os.path.dirname(os.path.abspath(__file__)),
        "ads.txt",
        mimetype="text/plain"
    )


@app.route("/robots.txt")
def robots_txt():
    return """User-agent: *
Allow: /
""", 200, {"Content-Type": "text/plain"}


@app.route("/about")
def about():
    return """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>عن غيث المجد</title>
    <meta name="description"
          content="تعرف على موقع غيث المجد وأهدافه وطبيعة الخدمات والروابط التي يقدمها.">
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: #f4f9fd;
            color: #111;
            line-height: 1.9;
        }

        main {
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
        }

        .box {
            background: #fff;
            border-radius: 18px;
            padding: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        }

        h1, h2 {
            color: #111;
        }

        h1 {
            text-align: center;
            margin-bottom: 30px;
        }

        a {
            color: #155fa0;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        .back {
            display: inline-block;
            margin-top: 25px;
            font-weight: bold;
        }
    </style>
</head>

<body>

<main>
    <div class="box">

        <h1>عن غيث المجد</h1>

        <h2>ما هو غيث المجد؟</h2>

        <p>
            غيث المجد هو موقع مستقل يهدف إلى تنظيم وتجميع الروابط
            والمعلومات المفيدة المتعلقة بالمساعدات الإنسانية والخدمات
            التعليمية والخدمات العامة في فلسطين، مع التركيز على توفير
            وصول أسهل للمستخدم إلى المصادر والجهات الرسمية.
        </p>

        <h2>هدف الموقع</h2>

        <p>
            يهدف الموقع إلى مساعدة الزائر في الوصول إلى الروابط الرسمية
            والنماذج والخدمات الإلكترونية بشكل منظم وواضح، بدلًا من البحث
            بين عدد كبير من الصفحات والمصادر المختلفة.
        </p>

        <h2>الالتزام والوصف</h2>

        <p>
            غيث المجد موقع مستقل وليس جهة حكومية أو منظمة إنسانية أو
            جهة مانحة، ولا يمثل أي مؤسسة أو منظمة مدرجة ضمن الروابط.
        </p>

        <p>
            نحاول تنظيم الروابط وتحديثها قدر الإمكان، لكن طبيعة الخدمات
            والبرامج والروابط الخارجية قد تتغير من وقت إلى آخر.
        </p>

        <p>
            وجود رابط لأي جهة على الموقع لا يعني وجود شراكة أو اعتماد
            أو علاقة رسمية بين غيث المجد وتلك الجهة.
        </p>

        <h2>تنبيه مهم</h2>

        <p>
            غيث المجد لا يضمن حصول أي شخص على مساعدة أو خدمة من الجهات
            الخارجية، ولا يتحكم في قرارات تلك الجهات أو شروطها أو
            مواعيد التسجيل والاستفادة.
        </p>

        <h2>الخصوصية والأمان</h2>

        <p>
            لا يطلب الموقع من الزائر تقديم معلومات حساسة من خلال الصفحة
            الرئيسية، ويُفضّل دائمًا التأكد من أن أي معلومات شخصية يتم
            إدخالها تكون داخل الموقع الرسمي للجهة المعنية.
        </p>

        <h2>التواصل</h2>

        <p>
            للاستفسارات والملاحظات المتعلقة بالموقع:
        </p>

        <p>
            <a href="mailto:n299964@hotmail.com">
                n299964@hotmail.com
            </a>
        </p>

        <a class="back" href="/">
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
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>سياسة الخصوصية | غيث المجد</title>
    <meta name="description"
          content="سياسة الخصوصية لموقع غيث المجد.">
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: #f4f9fd;
            color: #111;
            line-height: 1.9;
        }

        main {
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
        }

        .box {
            background: #fff;
            border-radius: 18px;
            padding: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        }

        h1, h2 {
            color: #111;
        }

        h1 {
            text-align: center;
            margin-bottom: 30px;
        }

        a {
            color: #155fa0;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        .back {
            display: inline-block;
            margin-top: 25px;
            font-weight: bold;
        }
    </style>
</head>

<body>

<main>
    <div class="box">

        <h1>سياسة الخصوصية</h1>

        <p>
            يحترم غيث المجد خصوصية زواره، ونسعى إلى توضيح طريقة التعامل
            مع المعلومات أثناء استخدام الموقع.
        </p>

        <h2>المعلومات الشخصية</h2>

        <p>
            لا يطلب الموقع من الزائر تقديم معلومات شخصية من أجل تصفح
            صفحات الموقع والوصول إلى الروابط المتاحة فيه.
        </p>

        <h2>الروابط الخارجية</h2>

        <p>
            يحتوي الموقع على روابط لمواقع وجهات خارجية. عند الانتقال
            إلى أي موقع خارجي، يصبح المستخدم خاضعًا لسياسة الخصوصية
            وشروط الاستخدام الخاصة بذلك الموقع.
        </p>

        <h2>ملفات تعريف الارتباط والإعلانات</h2>

        <p>
            قد يستخدم الموقع في المستقبل خدمات إعلانية أو تقنيات مثل
            ملفات تعريف الارتباط لتحسين تجربة المستخدم أو عرض الإعلانات
            ذات الصلة، وفقًا للسياسات المعمول بها لدى مزودي هذه الخدمات.
        </p>

        <h2>الأمان</h2>

        <p>
            نسعى إلى الحفاظ على الموقع بصورة آمنة، ولكن لا يمكن ضمان
            الحماية المطلقة لأي خدمة متاحة عبر الإنترنت.
        </p>

        <h2>التحديثات</h2>

        <p>
            قد يتم تحديث سياسة الخصوصية عند الحاجة لمواكبة أي تغييرات
            في الموقع أو الخدمات المستخدمة فيه.
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

        <a class="back" href="/">
            العودة إلى الصفحة الرئيسية
        </a>

    </div>
</main>

</body>
</html>
"""


@app.route("/terms")
def terms():
    return """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>شروط الاستخدام | غيث المجد</title>

    <meta name="description"
          content="شروط استخدام موقع غيث المجد.">

    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: #f4f9fd;
            color: #111;
            line-height: 1.9;
        }

        main {
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
        }

        .box {
            background: #fff;
            border-radius: 18px;
            padding: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        }

        h1, h2 {
            color: #111;
        }

        h1 {
            text-align: center;
            margin-bottom: 30px;
        }

        a {
            color: #155fa0;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        .back {
            display: inline-block;
            margin-top: 25px;
            font-weight: bold;
        }
    </style>
</head>

<body>

<main>
    <div class="box">

        <h1>شروط الاستخدام</h1>

        <p>
            باستخدامك موقع غيث المجد، فإنك توافق على الالتزام بشروط
            الاستخدام الموضحة في هذه الصفحة. إذا كنت لا توافق على هذه
            الشروط، يرجى عدم استخدام الموقع.
        </p>

        <h2>طبيعة الموقع</h2>

        <p>
            غيث المجد موقع مستقل يهدف إلى تنظيم وتقديم روابط ومعلومات
            مفيدة حول المساعدات والخدمات التعليمية والخدمات العامة
            في فلسطين.
        </p>

        <p>
            الموقع ليس جهة حكومية أو منظمة إنسانية أو جهة مانحة،
            ولا يمثل أي جهة خارجية تظهر روابطها أو خدماتها في الموقع.
        </p>

        <h2>الروابط الخارجية</h2>

        <p>
            قد يحتوي الموقع على روابط لمواقع إلكترونية تابعة لجهات
            ومؤسسات خارجية. هذه المواقع تخضع لشروط وسياسات الجهات
            المالكة لها، ولا يتحمل غيث المجد مسؤولية محتواها أو خدماتها.
        </p>

        <h2>دقة المعلومات</h2>

        <p>
            نسعى إلى تقديم معلومات وروابط مفيدة قدر الإمكان، لكن قد
            تتغير بعض الروابط أو الخدمات أو شروط الجهات الخارجية
            بمرور الوقت. لذلك يجب على المستخدم التأكد من المعلومات
            من المصدر الرسمي قبل اتخاذ أي إجراء.
        </p>

        <h2>مسؤولية المستخدم</h2>

        <p>
            يستخدم الزائر المعلومات والروابط الموجودة في الموقع
            على مسؤوليته الخاصة، ولا يتحمل غيث المجد مسؤولية
            القرارات أو الإجراءات التي يتخذها المستخدم بناءً
            على محتوى المواقع الخارجية.
        </p>

        <h2>الرسوم والمدفوعات</h2>

        <p>
            غيث المجد لا يفرض رسومًا على المستخدم مقابل الوصول إلى
            المعلومات والروابط المنشورة في الموقع.
        </p>

        <p>
            إذا كانت إحدى الجهات الخارجية تفرض رسومًا أو شروطًا
            معينة مقابل خدمة تقدمها، فإن تلك الرسوم والشروط تخص
            الجهة الخارجية وحدها.
        </p>

        <h2>التعديلات</h2>

        <p>
            قد يتم تحديث أو تعديل محتوى الموقع أو هذه الشروط عند الحاجة،
            ويُعد استمرار استخدام الموقع بعد التحديث موافقة على النسخة
            المحدثة.
        </p>

        <h2>التواصل</h2>

        <p>
            للاستفسارات المتعلقة بشروط الاستخدام:
        </p>

        <p>
            <a href="mailto:n299964@hotmail.com">
                n299964@hotmail.com
            </a>
        </p>

        <a class="back" href="/">
            العودة إلى الصفحة الرئيسية
        </a>

    </div>
</main>

</body>
</html>
"""


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
