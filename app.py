import os, sqlite3, uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

BASE=os.path.dirname(os.path.abspath(__file__)); DB=os.path.join(BASE,'families.db'); UP=os.path.join(BASE,'uploads')
os.makedirs(UP,exist_ok=True)
app=Flask(__name__); app.secret_key=os.environ.get('SECRET_KEY','change-me')

def conn():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c

def init():
 c=conn(); c.execute('''CREATE TABLE IF NOT EXISTS applications(id INTEGER PRIMARY KEY AUTOINCREMENT, application_no TEXT, applicant_name TEXT, applicant_id TEXT, phone TEXT, address TEXT, beneficiary_name TEXT, beneficiary_id TEXT, birth_date TEXT, age INTEGER, gender TEXT, beneficiary_phone TEXT, father_name TEXT, mother_name TEXT, blood_pressure TEXT, diabetes TEXT, current_glasses TEXT, prescription TEXT, last_eye_exam TEXT, glasses_type TEXT, vision_problem TEXT, medical_report TEXT, family_data TEXT, attachment TEXT, created_at TEXT)'''); c.execute('''CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value TEXT)''');
 for k,v in [('enabled','1'),('open_at',''),('close_at','')]: c.execute('INSERT OR IGNORE INTO settings VALUES(?,?)',(k,v))
 c.commit(); c.close()

def getset(k):
 c=conn(); r=c.execute('SELECT value FROM settings WHERE key=?',(k,)).fetchone(); c.close(); return r['value'] if r else ''
def is_open():
 if getset('enabled')!='1': return False
 now=datetime.now()
 try:
  if getset('open_at') and now < datetime.fromisoformat(getset('open_at')): return False
  if getset('close_at') and now > datetime.fromisoformat(getset('close_at')): return False
 except ValueError: pass
 return True
@app.context_processor
def ctx(): return {'registration_open':is_open()}

@app.route('/')
def home(): return render_template('index.html')
@app.route('/register',methods=['GET','POST'])
def register():
 if not is_open(): return render_template('closed.html')
 if request.method=='POST':
  f=request.files.get('attachment'); fn=''
  if f and f.filename:
   fn=uuid.uuid4().hex+'_'+secure_filename(f.filename); f.save(os.path.join(UP,fn))
  c=conn(); c.execute('''INSERT INTO applications(application_no,applicant_name,applicant_id,phone,address,beneficiary_name,beneficiary_id,birth_date,age,gender,beneficiary_phone,father_name,mother_name,blood_pressure,diabetes,current_glasses,prescription,last_eye_exam,glasses_type,vision_problem,medical_report,family_data,attachment,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',('TEMP',*(request.form.get(k,'') for k in ['applicant_name','applicant_id','phone','address','beneficiary_name','beneficiary_id','birth_date','age','gender','beneficiary_phone','father_name','mother_name','blood_pressure','diabetes','current_glasses','prescription','last_eye_exam','glasses_type','vision_problem','medical_report','family_data']),fn,datetime.now().isoformat(timespec='seconds'))); i=c.lastrowid; no=f'AK-{datetime.now():%Y%m%d}-{i:04d}'; c.execute('UPDATE applications SET application_no=? WHERE id=?',(no,i)); c.commit(); c.close(); return render_template('success.html',no=no)
 return render_template('register.html')

@app.route('/admin',methods=['GET','POST'])
def admin():
 if request.method=='POST':
  c=conn();
  for k in ['enabled','open_at','close_at']: c.execute('INSERT OR REPLACE INTO settings VALUES(?,?)',(k,request.form.get(k,'')))
  c.commit(); c.close(); return redirect('/admin')
 c=conn(); rows=c.execute('SELECT * FROM applications ORDER BY id DESC').fetchall(); c.close(); return render_template('admin.html',rows=rows,enabled=getset('enabled'),open_at=getset('open_at'),close_at=getset('close_at'))

def row(i):
 c=conn(); r=c.execute('SELECT * FROM applications WHERE id=?',(i,)).fetchone(); c.close(); return r
@app.route('/export/<int:i>/docx')
def docx(i):
 r=row(i)
 if not r:return 'Not found',404
 d=Document(); d.add_heading('مبادرة العطاء لدعم النظارات الطبية',0); d.add_heading('لكبار السن من عائلة أبوكويك المحترمين',1); d.add_paragraph('رقم الطلب: '+r['application_no'])
 fields=[('بيانات مقدم الطلب',['applicant_name','applicant_id','phone','address']),('بيانات المستفيد',['beneficiary_name','beneficiary_id','birth_date','age','gender','beneficiary_phone','father_name','mother_name']),('الحالة الصحية',['blood_pressure','diabetes']),('حالة النظر',['current_glasses','prescription','last_eye_exam','glasses_type','vision_problem','medical_report']),('بيانات الأسرة',['family_data']),('تاريخ التسجيل',['created_at'])]
 labels={'applicant_name':'الاسم الكامل','applicant_id':'رقم الهوية','phone':'رقم الهاتف / واتساب','address':'مكان السكن','beneficiary_name':'اسم المستفيد','beneficiary_id':'رقم الهوية','birth_date':'تاريخ الميلاد','age':'العمر','gender':'الجنس','beneficiary_phone':'الهاتف','father_name':'اسم الأب','mother_name':'اسم الأم','blood_pressure':'ارتفاع ضغط الدم','diabetes':'مرض السكري','current_glasses':'يستخدم نظارة حاليًا','prescription':'لديه وصفة طبية','last_eye_exam':'تاريخ آخر فحص للعيون','glasses_type':'نوع النظارة المطلوبة','vision_problem':'وصف مشكلة النظر','medical_report':'لديه تقرير طبي','family_data':'أفراد الأسرة','created_at':'تاريخ التسجيل'}
 for title,ks in fields:
  d.add_heading(title,2)
  for k in ks:d.add_paragraph(f"{labels[k]}: {r[k] or ''}")
 p=os.path.join(BASE,r['application_no']+'.docx'); d.save(p); return send_file(p,as_attachment=True)
@app.route('/export/<int:i>/pdf')
def pdf(i):
 r=row(i)
 if not r:return 'Not found',404
 p=os.path.join(BASE,r['application_no']+'.pdf'); c=canvas.Canvas(p,pagesize=A4); y=800; c.setFont('Helvetica-Bold',16); c.drawString(50,y,'Abu Kwaik Family - Medical Glasses Support'); y-=30; c.setFont('Helvetica',10)
 for k,v in [('Application No.',r['application_no']),('Applicant',r['applicant_name']),('Phone',r['phone']),('Beneficiary',r['beneficiary_name']),('Age',r['age']),('Gender',r['gender']),('Blood pressure',r['blood_pressure']),('Diabetes',r['diabetes']),('Glasses need',r['glasses_type']),('Vision problem',r['vision_problem']),('Family',r['family_data']),('Created',r['created_at'])]:
  c.drawString(50,y,f'{k}: {v or ""}'); y-=18
  if y<50:c.showPage(); y=800; c.setFont('Helvetica',10)
 c.save(); return send_file(p,as_attachment=True)

init()
if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
