import os
import sqlite3
import uuid
from datetime import datetime
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "families.db")
UP = os.path.join(BASE, "uploads")

os.makedirs(UP, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "abu-kwaik-secret-key")


def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c


def init():
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

    for k, v in [
        ("enabled", "1"),
        ("open_at", ""),
        ("close_at", "")
    ]:
        c.execute(
            "INSERT OR IGNORE INTO settings VALUES (?, ?)",
            (k, v)
        )

    c.commit()
    c.close()


def getset(key):
    c = conn()
    r = c.execute(
        "SELECT value FROM settings WHERE key=?",
        (key,)
    ).fetchone()
    c.close()

    return r["value"] if r else ""


def is_open():
    if getset("enabled") != "1":
        return False

    now = datetime.now()

    try:
        if getset("open_at"):
            if now < datetime.fromisoformat(getset("open_at")):
                return False

        if getset("close_at"):
            if now > datetime.fromisoformat(getset("close_at")):
                return False

    except ValueError:
        pass

    return True


@app.context_processor
def ctx():
    return {
        "registration_open": is_open()
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if not is_open():
        return render_template("closed.html")

    if request.method == "POST":

        try:
            # -------------------------
            # رفع المرفق
            # -------------------------
            f = request.files.get("attachment")
            filename = ""

            if f and f.filename:
                original_name = secure_filename(f.filename)

                if original_name:
                    filename = (
                        uuid.uuid4().hex
                        + "_"
                        + original_name
                    )

                    f.save(
                        os.path.join(UP, filename)
                    )

            # -------------------------
            # قراءة جميع البيانات
            # -------------------------
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

            data = {
                field: request.form.get(field, "").strip()
                for field in fields
            }

            # -------------------------
            # حفظ التسجيل
            # -------------------------
            c = conn()

            c.execute("""
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
                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?
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

            application_id = c.lastrowid

            application_no = (
                f"AK-{datetime.now():%Y%m%d}-{application_id:04d}"
            )

            c.execute(
                """
                UPDATE applications
                SET application_no=?
                WHERE id=?
                """,
                (application_no, application_id)
            )

            c.commit()
            c.close()

            # -------------------------
            # صفحة نجاح التسجيل
            # -------------------------
            return render_template(
                "success.html",
                no=application_no
            )

        except Exception as e:

            print("REGISTRATION ERROR:", e)

            return """
            <div style="
                direction:rtl;
                text-align:center;
                font-family:Arial;
                padding:50px;
            ">
                <h2>حدث خطأ أثناء حفظ التسجيل</h2>
                <p>يرجى المحاولة مرة أخرى.</p>
                <a href="/register">العودة إلى نموذج التسجيل</a>
            </div>
            """, 500

    return render_template("register.html")


# ==========================================
# لوحة الإدارة
# ==========================================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        c = conn()

        for key in [
            "enabled",
            "open_at",
            "close_at"
        ]:
            c.execute(
                """
                INSERT OR REPLACE INTO settings
                VALUES (?, ?)
                """,
                (
                    key,
                    request.form.get(key, "")
                )
            )

        c.commit()
        c.close()

        return render_template(
            "admin.html",
            rows=[],
            enabled=getset("enabled"),
            open_at=getset("open_at"),
            close_at=getset("close_at")
        )

    c = conn()

    rows = c.execute(
        """
        SELECT *
        FROM applications
        ORDER BY id DESC
        """
    ).fetchall()

    c.close()

    return render_template(
        "admin.html",
        rows=rows,
        enabled=getset("enabled"),
        open_at=getset("open_at"),
        close_at=getset("close_at")
    )


# ==========================================
# جلب طلب
# ==========================================

def get_application(application_id):

    c = conn()

    row = c.execute(
        """
        SELECT *
        FROM applications
        WHERE id=?
        """,
        (application_id,)
    ).fetchone()

    c.close()

    return row


# ==========================================
# تحميل Word
# ==========================================

@app.route("/export/<int:i>/docx")
def docx(i):

    r = get_application(i)

    if not r:
        return "Not found", 404

    document = Document()

    document.add_heading(
        "مبادرة العطاء لدعم النظارات الطبية",
        0
    )

    document.add_heading(
        "لكبار السن من عائلة أبوكويك المحترمين",
        1
    )

    document.add_paragraph(
        "رقم الطلب: " + str(r["application_no"])
    )

    sections = [
        (
            "بيانات مقدم الطلب",
            [
                ("الاسم الكامل", "applicant_name"),
                ("رقم الهوية", "applicant_id"),
                ("رقم الهاتف", "phone"),
                ("مكان السكن", "address")
            ]
        ),
        (
            "بيانات المستفيد",
            [
                ("اسم المستفيد", "beneficiary_name"),
                ("رقم الهوية", "beneficiary_id"),
                ("تاريخ الميلاد", "birth_date"),
                ("العمر", "age"),
                ("الجنس", "gender"),
                ("الهاتف", "beneficiary_phone"),
                ("اسم الأب", "father_name"),
                ("اسم الأم", "mother_name")
            ]
        ),
        (
            "الحالة الصحية",
            [
                ("ضغط الدم", "blood_pressure"),
                ("مرض السكري", "diabetes")
            ]
        ),
        (
            "حالة النظر",
            [
                ("يستخدم نظارة حاليًا", "current_glasses"),
                ("لديه وصفة طبية", "prescription"),
                ("تاريخ آخر فحص للعيون", "last_eye_exam"),
                ("نوع النظارة المطلوبة", "glasses_type"),
                ("وصف مشكلة النظر", "vision_problem"),
                ("لديه تقرير طبي", "medical_report")
            ]
        ),
        (
            "بيانات الأسرة",
            [
                ("أفراد الأسرة", "family_data")
            ]
        ),
        (
            "بيانات التسجيل",
            [
                ("تاريخ التسجيل", "created_at")
            ]
        )
    ]

    for title, fields in sections:

        document.add_heading(title, 2)

        for label, key in fields:

            value = r[key] or ""

            document.add_paragraph(
                f"{label}: {value}"
            )

    path = os.path.join(
        BASE,
        r["application_no"] + ".docx"
    )

    document.save(path)

    return send_file(
        path,
        as_attachment=True
    )


# ==========================================
# تحميل PDF
# ==========================================

@app.route("/export/<int:i>/pdf")
def pdf(i):

    r = get_application(i)

    if not r:
        return "Not found", 404

    path = os.path.join(
        BASE,
        r["application_no"] + ".pdf"
    )

    pdf_file = canvas.Canvas(
        path,
        pagesize=A4
    )

    y = 800

    pdf_file.setFont(
        "Helvetica-Bold",
        16
    )

    pdf_file.drawString(
        50,
        y,
        "Abu Kwaik Family - Medical Glasses Support"
    )

    y -= 35

    pdf_file.setFont(
        "Helvetica",
        10
    )

    fields = [
        ("Application No.", "application_no"),
        ("Applicant", "applicant_name"),
        ("Applicant ID", "applicant_id"),
        ("Phone", "phone"),
        ("Address", "address"),
        ("Beneficiary", "beneficiary_name"),
        ("Beneficiary ID", "beneficiary_id"),
        ("Age", "age"),
        ("Gender", "gender"),
        ("Blood pressure", "blood_pressure"),
        ("Diabetes", "diabetes"),
        ("Current glasses", "current_glasses"),
        ("Prescription", "prescription"),
        ("Glasses type", "glasses_type"),
        ("Vision problem", "vision_problem"),
        ("Medical report", "medical_report"),
        ("Family", "family_data"),
        ("Created", "created_at")
    ]

    for label, key in fields:

        value = r[key] or ""

        pdf_file.drawString(
            50,
            y,
            f"{label}: {value}"
        )

        y -= 18

        if y < 50:
            pdf_file.showPage()
            y = 800
            pdf_file.setFont(
                "Helvetica",
                10
            )

    pdf_file.save()

    return send_file(
        path,
        as_attachment=True
    )


# ==========================================
# تشغيل التطبيق
# ==========================================

init()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        )
    )
