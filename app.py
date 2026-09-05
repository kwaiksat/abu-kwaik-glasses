import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, send_file

from docx import Document
from reportlab.pdfgen import canvas


# =========================
# إعداد التطبيق
# =========================

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "abu-kwaik-glasses-secret-key")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "families.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================
# الاتصال بقاعدة البيانات
# =========================

def conn():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


# =========================
# إنشاء قاعدة البيانات
# =========================

def init_db():

    c = conn()

    c.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_no TEXT,
            applicant_name TEXT,
            applicant_id TEXT,
            phone TEXT,
            address TEXT,
            beneficiary_name TEXT,
            beneficiary_id TEXT,
            birth_date TEXT,
            age TEXT,
            gender TEXT,
            beneficiary_phone TEXT,
            father_name TEXT,
            mother_name TEXT,
            blood_pressure TEXT,
            diabetes TEXT,
            current_glasses TEXT,
            prescription TEXT,
            last_eye_exam TEXT,
            glasses_type TEXT,
            vision_problem TEXT,
            medical_report TEXT,
            family_data TEXT,
            attachment TEXT,
            created_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    c.commit()
    c.close()


init_db()


# =========================
# الصفحة الرئيسية
# =========================

@app.route("/")
def index():
    return render_template("index.html")


# =========================
# التسجيل
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")

    try:

        # ---------------------------------
        # بيانات النموذج
        # ---------------------------------

        fields = [
            "applicant_name",
            "applicant_id",
            "phone",
            "address",
            "beneficiary_name",
            "beneficiary_id",
            "birth_date",
            "age",
            "gender",
            "beneficiary_phone",
            "father_name",
            "mother_name",
            "blood_pressure",
            "diabetes",
            "current_glasses",
            "prescription",
            "last_eye_exam",
            "glasses_type",
            "vision_problem",
            "medical_report",
            "family_data"
        ]

        data = {}

        for field in fields:
            data[field] = request.form.get(field, "").strip()


        # ---------------------------------
        # رفع المرفق
        # ---------------------------------

        filename = ""

        attachment = request.files.get("attachment")

        if attachment and attachment.filename:

            original_name = attachment.filename

            # اسم آمن للملف
            safe_name = os.path.basename(original_name)

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")

            filename = f"{timestamp}_{safe_name}"

            attachment.save(
                os.path.join(UPLOAD_FOLDER, filename)
            )


        # ---------------------------------
        # حفظ البيانات
        # ---------------------------------

        c = conn()

        cursor = c.cursor()

        cursor.execute("""
            INSERT INTO applications (
                application_no,
                applicant_name,
                applicant_id,
                phone,
                address,
                beneficiary_name,
                beneficiary_id,
                birth_date,
                age,
                gender,
                beneficiary_phone,
                father_name,
                mother_name,
                blood_pressure,
                diabetes,
                current_glasses,
                prescription,
                last_eye_exam,
                glasses_type,
                vision_problem,
                medical_report,
                family_data,
                attachment,
                created_at
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?
            )
        """, (
            "TEMP",
            data["applicant_name"],
            data["applicant_id"],
            data["phone"],
            data["address"],
            data["beneficiary_name"],
            data["beneficiary_id"],
            data["birth_date"],
            data["age"],
            data["gender"],
            data["beneficiary_phone"],
            data["father_name"],
            data["mother_name"],
            data["blood_pressure"],
            data["diabetes"],
            data["current_glasses"],
            data["prescription"],
            data["last_eye_exam"],
            data["glasses_type"],
            data["vision_problem"],
            data["medical_report"],
            data["family_data"],
            filename,
            datetime.now().isoformat(timespec="seconds")
        ))

        # ---------------------------------
        # التصحيح المهم
        # ---------------------------------

        # نأخذ رقم السجل من Cursor وليس Connection
        application_id = cursor.lastrowid

        application_no = (
            f"AK-{datetime.now():%Y%m%d}-{application_id:04d}"
        )

        cursor.execute("""
            UPDATE applications
            SET application_no = ?
            WHERE id = ?
        """, (
            application_no,
            application_id
        ))

        c.commit()
        c.close()


        # ---------------------------------
        # صفحة النجاح
        # ---------------------------------

        return render_template(
            "success.html",
            no=application_no
        )


    except Exception as e:

        print("===================================")
        print("REGISTRATION ERROR:")
        print(str(e))
        print("===================================")

        return """
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>حدث خطأ</title>

            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: #f8f7fb;
                    padding: 30px;
                    text-align: center;
                }

                .box {
                    max-width: 600px;
                    margin: 50px auto;
                    background: white;
                    padding: 30px;
                    border-radius: 18px;
                    box-shadow: 0 5px 25px rgba(0,0,0,0.08);
                }

                h1 {
                    color: #7b4ab8;
                }

                p {
                    color: #555;
                    line-height: 1.8;
                }

                a {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 12px 25px;
                    background: #7b4ab8;
                    color: white;
                    text-decoration: none;
                    border-radius: 10px;
                }
            </style>
        </head>

        <body>

            <div class="box">

                <h1>حدث خطأ أثناء التسجيل</h1>

                <p>
                    نعتذر، حدث خطأ أثناء حفظ البيانات.
                    يرجى المحاولة مرة أخرى.
                </p>

                <a href="/register">
                    العودة إلى نموذج التسجيل
                </a>

            </div>

        </body>
        </html>
        """, 500


# =========================
# لوحة الإدارة
# =========================

@app.route("/admin")
def admin():

    c = conn()

    applications = c.execute("""
        SELECT *
        FROM applications
        ORDER BY id DESC
    """).fetchall()

    c.close()

    return render_template(
        "admin.html",
        applications=applications
    )


# =========================
# تصدير Word
# =========================

@app.route("/export/<int:i>/docx")
def export_docx(i):

    c = conn()

    row = c.execute(
        "SELECT * FROM applications WHERE id = ?",
        (i,)
    ).fetchone()

    c.close()

    if not row:
        return "الطلب غير موجود", 404

    document = Document()

    document.add_heading(
        "مبادرة العطاء لدعم النظارات الطبية",
        level=1
    )

    document.add_paragraph(
        f"رقم الطلب: {row['application_no']}"
    )

    document.add_paragraph(
        f"تاريخ التسجيل: {row['created_at']}"
    )

    document.add_heading("بيانات مقدم الطلب", level=2)

    document.add_paragraph(
        f"الاسم: {row['applicant_name']}"
    )

    document.add_paragraph(
        f"رقم الهوية: {row['applicant_id']}"
    )

    document.add_paragraph(
        f"رقم الهاتف: {row['phone']}"
    )

    document.add_paragraph(
        f"العنوان: {row['address']}"
    )

    document.add_heading("بيانات المستفيد", level=2)

    document.add_paragraph(
        f"الاسم: {row['beneficiary_name']}"
    )

    document.add_paragraph(
        f"رقم الهوية: {row['beneficiary_id']}"
    )

    document.add_paragraph(
        f"تاريخ الميلاد: {row['birth_date']}"
    )

    document.add_paragraph(
        f"العمر: {row['age']}"
    )

    document.add_paragraph(
        f"الجنس: {row['gender']}"
    )

    document.add_paragraph(
        f"هاتف المستفيد: {row['beneficiary_phone']}"
    )

    document.add_heading("الحالة الصحية والبصرية", level=2)

    document.add_paragraph(
        f"ضغط الدم: {row['blood_pressure']}"
    )

    document.add_paragraph(
        f"السكري: {row['diabetes']}"
    )

    document.add_paragraph(
        f"النظارات الحالية: {row['current_glasses']}"
    )

    document.add_paragraph(
        f"الوصفة الطبية: {row['prescription']}"
    )

    document.add_paragraph(
        f"آخر فحص للعين: {row['last_eye_exam']}"
    )

    document.add_paragraph(
        f"نوع النظارة: {row['glasses_type']}"
    )

    document.add_paragraph(
        f"مشكلة النظر: {row['vision_problem']}"
    )

    document.add_paragraph(
        f"التقرير الطبي: {row['medical_report']}"
    )

    document.add_paragraph(
        f"بيانات الأسرة: {row['family_data']}"
    )

    path = os.path.join(
        BASE_DIR,
        f"{row['application_no']}.docx"
    )

    document.save(path)

    return send_file(
        path,
        as_attachment=True
    )


# =========================
# تصدير PDF
# =========================

@app.route("/export/<int:i>/pdf")
def export_pdf(i):

    c = conn()

    row = c.execute(
        "SELECT * FROM applications WHERE id = ?",
        (i,)
    ).fetchone()

    c.close()

    if not row:
        return "الطلب غير موجود", 404

    path = os.path.join(
        BASE_DIR,
        f"{row['application_no']}.pdf"
    )

    pdf = canvas.Canvas(path)

    pdf.setFont("Helvetica", 11)

    y = 800

    lines = [
        "Abu Kwaik Medical Glasses Initiative",
        "",
        f"Application No: {row['application_no']}",
        f"Created: {row['created_at']}",
        "",
        f"Applicant Name: {row['applicant_name']}",
        f"Applicant ID: {row['applicant_id']}",
        f"Phone: {row['phone']}",
        f"Address: {row['address']}",
        "",
        f"Beneficiary Name: {row['beneficiary_name']}",
        f"Beneficiary ID: {row['beneficiary_id']}",
        f"Birth Date: {row['birth_date']}",
        f"Age: {row['age']}",
        f"Gender: {row['gender']}",
        "",
        f"Blood Pressure: {row['blood_pressure']}",
        f"Diabetes: {row['diabetes']}",
        f"Current Glasses: {row['current_glasses']}",
        f"Prescription: {row['prescription']}",
        f"Last Eye Exam: {row['last_eye_exam']}",
        f"Glasses Type: {row['glasses_type']}",
        f"Vision Problem: {row['vision_problem']}",
        "",
        f"Medical Report: {row['medical_report']}",
        f"Family Data: {row['family_data']}"
    ]

    for line in lines:

        pdf.drawString(40, y, str(line))

        y -= 20

        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 11)
            y = 800

    pdf.save()

    return send_file(
        path,
        as_attachment=True
    )


# =========================
# تشغيل التطبيق
# =========================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
