from flask import Flask, redirect, render_template, request, url_for, flash
from flask_login import LoginManager, login_user, logout_user, UserMixin, current_user
from flask_sqlalchemy import SQLAlchemy
import os, datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('PASS')


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('dbpath')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

FYBCOM = ["Accountancy & Financial Management I", "Mathematical & Statistical I", "Environmental Studies I", "Commerce I", "Business Economics I", "Foundation Course I",
        "Accountancy & Financial Management II", "Mathematical & Statistical II", "Environmental Studies II", "Commerce II", "Business Economics II", "Foundation Course II"]
SYBCOM = ["Accountancy & Financial Management III", "Financial Accounting and Auditing Introduction to Management Accounting", "Business Law I", "Commerce III", "Business Economics III", "Advertising I",
        "Accountancy & Financial Management IV", "Financial Accounting and Auditing Auditing", "Business Law II", "Commerce IV", "Business Economics IV", "Advertising II"]
TYBCOM = ["Financial Accounting V", "Cost Accounting V", "Direct Tax V", "Commerce V (Marketing)", "Business Economics V", "Export Marketing V", "Financial Management V",
        "Financial Accounting VI", "Cost Accounting VI", "Indirect Tax GST Act VI", "Commerce VI (Human Resource Management)", "Business Economics VI", "Export Marketing VI", "Financial Management VI"]
FYBAF = ["Financial Accounting (Elements of Financial Accounting) I", "Cost Accounting (Introduction and Element of cost) I", "Financial Management (Introduction to Financial Management) I", "Business Communication I", "Foundation Course I", "Commerce (Business Environment) I", "Business Economics I",
        "Financial Accounting (Special Accounting Areas) II", "Auditing (Introduction and Planning) I", "Taxation I (Indirect Taxes I)", "Business Communication II", "Foundation Course II", "Business Law (Business Regulatory Framework) I", "Business Mathematics"]
SYBAF = ["Financial Accounting (Special Accounting Areas) III", "Cost Accounting (Methods of Costing) II", "Auditing (Techniques of Auditing and Audit Procedures) II", "Taxation II (Indirect Taxes Paper- II)", "Operation Research", "Information Technology in Accountancy I", "Commerce (Financial Market Operations) II", "Business Law (Business Regulatory Framework) II", "Business Economics II",
        "Financial Accounting (Special Accounting Areas) IV", "Wealth Management", "Auditing III", "Taxation III (Indirect Taxes Paper- III)", "Management Accounting (Introduction to Management Accounting) I", "Information Technology in Accountancy II", "Management (Introduction to Management) I", "Business Law (Company Law) II", "Research Methodology in Accounting and Finance"]
TYBAF = ["Financial Accounting V", "Cost Accounting IV", "Financial Management II", "Taxation IV (Direct Taxes- I)", "International Finance I", "Financial Analysis and Business Valuation", "Management (Management Applications) II", "Project Work I",
        "Financial Accounting VI", "Cost Accounting V", "Financial Management III", "Taxation V (Direct Taxes- II)", "Financial Accounting VII", "Security Analysis and Portfolio Management", "Economics (Indian Economy) III", "Project Work II"]
FYBMS = ["Introduction to Financial Accounts", "Business Law", "Business Statistics", "Business Communication I", "Foundation Course I", "Foundation of Human Skills", "Business Economics I",
        "Principles of Marketing", "Business Law", "Business Mathematics", "Business Communication II", "Foundation Course II", "Business Environment", "Principles of Management"]
SYBMS = ["Basics of Financial Services", "Introduction to Cost Accounting", "Equity & Debt Market", "Corporate Finance", "Consumer Behaviour", "Product Innovations Management", "Advertising", "Social Marketing", "Recruitment & Selection", "Motivation and Leadership", "Employees Relations & Welfare", "Organisation Behaviour & HRM", "Information Technology in Business Management I", "Environmental Management", "Business Planning & Entrepreneurial Management", "Accounting for Managerial Decisions", "Strategic Management",
        "Financial Institutions & Markets", "Auditing", "Strategic Cost Management", "Behavioural Finance", "Integrated Marketing Communication", "Rural Marketing", "Event Marketing", "Tourism Marketing", "Human Resource Planning & Information System", "Training & Development in HRM","Change Management", "Conflict & Negotiation", "Information Technology in Business Management II", "Business Economics II", "Business Research Methods", "Ethics & Governance", "Production & Total Quality Management"]
TYBMS = ["Investment Analysis & Portfolio Management", "Commodity & Derivatives Market", "Wealth Management", "Strategic Financial Management", "Risk Management", "Financing Rural Development", "Services Marketing", "E-Commerce & Digital Marketing", "Sales & Distribution Management", "Customer Relationship Management", "Industrial Marketing", "Strategic Marketing Management", "Finance for HR Professionals & Compensation Management", "Strategic Human Resource Management & HR Policies", "Performance Management & Career Planning", "Industrial Relations", "Talent & Competency Management", "Stress Management", "Logistics & Supply Chain", "Project Work I",
        "International Finance", "Innovative Financial Services", "Project Management", "Risk Management in Banking Sector", "Direct Taxes", "Indirect Taxes", "Brand Management", "Retail Management", "International Marketing", "Media Planning & Management", "Corporate Communication & Public Relations", "Marketing of Non-Profit Organisation", "HRM in Global Perspective", "Organizational Development", "HRM in Service Sector Management", "Workforce Diversity", "Human Resource Accounting & Audit", "Indian Ethos in Management", "Operation Research", "Project Work II"]
FYBSCIT = ["Imperative Programming", "Digital Electronics", "Operating Systems", "Discrete Mathematics", "Communication Skills", "Imperative Programming Practical", "Digital Electronics Practical", "Operating Systems Practical", "Discrete Mathematics Practical", "Communication Skills Practical",
        "Object oriented Programming", "Microprocessor Architecture", "Web Programming", "Numerical and Statistical Methods", "Green Computing", "Object Oriented Programming Practical", "Microprocessor Architecture Practical", "Web Programming Practical", "Numerical and Statistical Methods Practical", "Green Computing Practical"]
SYBSCIT = ["Python Programming", "Data Structures", "Computer Networks", "Database Management Systems", "Applied Mathematics", "Python Programming Practical", "Data Structures Practical", "Computer Networks Practical", "Database Management Systems Practical", "Mobile Programming Practical",
        "Core Java", "Introduction to Embedded Systems", "Computer Oriented Statistical Techniques", "Software Engineering", "Computer Graphics and Animation", "Core Java Practical", "Introduction to Embedded Systems Practical", "Computer Oriented Statistical Techniques Practical", "Software Engineering Practical", "Computer Graphics and Animation Practical"]
TYBSCIT = ["Software Project Management", "Internet of Things", "Advanced Web Programming", "Artificial Intelligence", "Linux System Administration", "Enterprise Java", "Next Generation Technologies", "Project Dissertation", "Internet of Things Practical", "Advanced Web Programming Practical", "Artificial Intelligence Practical", "Linux Administration Practical", "	Enterprise Java Practical", "Next Generation Technologies Practical",
        "Software Quality Assurance", "Security in Computing", "Business Intelligence", "Principles of Geographic Information Systems", "Enterprise Networking", "IT Service Management", "Cyber Laws", "Project Implementation", "Security in Computing Practical", "Business Intelligence Practical", "Principles of Geographic Information Systems Practical", "	Enterprise Networking Practical", "Advanced Mobile Programming"]

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)

class Student_details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batch = db.Column(db.String(15), nullable=False)
    course = db.Column(db.String(15), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    parent_first_name = db.Column(db.String(100), nullable=False)
    parent_middle_name = db.Column(db.String(100), nullable=False)
    parent_last_name = db.Column(db.String(100), nullable=False)
    parents_occupation = db.Column(db.String(200), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    street_address = db.Column(db.String(1000), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    phone_no = db.Column(db.String(10), nullable=False)
    parents_phone_no = db.Column(db.String(10), nullable=False)
    fees = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(15), nullable=False)
    admission_date = db.Column(db.Date, default=datetime.date.today())
    entry_by = db.Column(db.String(45), nullable=False)
    roll_no = db.Column(db.String(3), nullable=True)

class Attendence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.date.today())
    time = db.Column(db.String(100), default=datetime.datetime.now().strftime("%H:%M:%S"))
    course = db.Column(db.String(10), nullable=True)
    subject = db.Column(db.String(200), nullable=True)
    roll_no = db.Column(db.String(3), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    entry_by = db.Column(db.String(45), nullable=False)
    student_id = db.Column(db.String(100), nullable=False)

class Fees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.date.today())
    time = db.Column(db.String(100), default=datetime.datetime.now().strftime("%H:%M:%S"))
    course = db.Column(db.String(10), nullable=True)
    roll_no = db.Column(db.String(3), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    entry_by = db.Column(db.String(45), nullable=False)
    batch = db.Column(db.String(100), nullable=False)

class Deleted_records(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batch = db.Column(db.String(15), nullable=False)
    course = db.Column(db.String(15), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    parent_first_name = db.Column(db.String(100), nullable=False)
    parent_middle_name = db.Column(db.String(100), nullable=False)
    parent_last_name = db.Column(db.String(100), nullable=False)
    parents_occupation = db.Column(db.String(200), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    street_address = db.Column(db.String(1000), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    phone_no = db.Column(db.String(10), nullable=False)
    parents_phone_no = db.Column(db.String(10), nullable=False)
    fees = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(15), nullable=False)
    admission_date = db.Column(db.String(15), nullable=False)
    deletion_date = db.Column(db.Date, default=datetime.date.today())
    entry_by = db.Column(db.String(45), nullable=False)
    roll_no = db.Column(db.String(3), nullable=True)


@app.route("/")
def index():
    return render_template("login.html")


def add_attendence(present, subject, course):
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    if current_month<=3:
        current_year = f"{current_year-1}-{current_year}"
    else:
        current_year = f"{current_year}-{current_year+1}"
    students = db.session.query(Student_details).filter(Student_details.batch==current_year).filter(Student_details.course==course)
    print(course)
    students_list = list(students)
    for m in students_list:
        if m.roll_no in present:
            new_record = Attendence(
            course = course,
            subject = subject,
            roll_no = m.roll_no,
            name = f"{m.first_name} {m.middle_name} {m.last_name}",
            status = "Present",
            entry_by = current_user.name,
            student_id = m.id
            )
        else:
            new_record = Attendence(
            course = course,
            subject = subject,
            roll_no = m.roll_no,
            name = f"{m.first_name} {m.middle_name} {m.last_name}",
            status = "Absent",
            entry_by = current_user.name,
            student_id = m.id
            )
        db.session.add(new_record)
        db.session.commit()
    flash("Attendence submitted Successfully :)")


@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":

        username = request.form.get('username')
        password = request.form.get('password')

        user = Users.query.filter_by(email=username).first()

        if not user:
            flash("please, enter correct username.")
            return redirect(url_for("home"))

        elif not user.password==password:
            flash("please, enter correct password.")
            return redirect(url_for("home"))

        else:
            login_user(user)
            return render_template("index.html")

    elif current_user.is_authenticated:
        return render_template("index.html")


    return render_template("login.html")


@app.route("/home/students")
def students():
    return render_template("student.html")

@app.route("/home/students/add_student", methods=["GET", "POST"])
def add_student():
    
    if request.method == "POST":
        batch = request.form.get("batch")
        course = request.form.get("course")
        gender = request.form.get("gender")
        first_name = request.form.get("stfirst")
        middle_name = request.form.get("stmiddle")
        last_name = request.form.get("stlast")
        prfirst_name = request.form.get("prfirst")
        prmiddle_name = request.form.get("prmiddle")
        prlast_name = request.form.get("prlast")
        dob = request.form.get("dob")
        pr_occupation = request.form.get("proccupation")
        street_address = request.form.get("street")
        city = request.form.get("city")
        state = request.form.get("state")
        postal_code = request.form.get("postalcode")
        phone = request.form.get("number")
        parents_phone = request.form.get("prnumber")
        email = request.form.get("email")
        fees = request.form.getlist("fees")[0]


        students = db.session.query(Student_details).filter(Student_details.batch==batch, Student_details.course==course.upper())
        students_list = list(students)
        if len(students_list) == 0:
            roll_no = 1
        else:
            rl_det = int(students_list[-1].roll_no)
            roll_no = rl_det+1

        if fees == "Done":
            new_fees = Fees(
                course = course,
                roll_no = roll_no,
                name = f"{first_name} {middle_name} {last_name}",
                entry_by = current_user.name,
                batch = batch
            )

            db.session.add(new_fees)
            db.session.commit()

        

        new_student = Student_details(
            batch = batch,
            course = course,
            first_name = first_name.capitalize(),
            middle_name = middle_name.capitalize(),
            last_name = last_name.capitalize(),
            parent_first_name = prfirst_name.capitalize(),
            parent_middle_name = prmiddle_name.capitalize(),
            parent_last_name = prlast_name.capitalize(),
            parents_occupation = pr_occupation.capitalize(),
            dob = dob,
            street_address = street_address.capitalize(),
            city = city.capitalize(),
            state = state.capitalize(),
            postal_code = postal_code,
            phone_no = phone,
            parents_phone_no = parents_phone,
            fees = fees,
            email = email,
            gender = gender.capitalize(),
            entry_by = current_user.name,
            roll_no = roll_no
        )

        db.session.add(new_student)
        db.session.commit()

        flash("Student Added Successfully :)")



    current_year = datetime.datetime.now().year
    a = []
    for i in range(1950, current_year+1):
        a.append(f"{i}-{i+1}")

    
    return render_template("add_student.html", years=a)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/home/students/student_records", methods=["GET", "POST"])
def all_students():
    if request.method == "POST":
        students = Student_details.query.all()
        searched_students = []
        name = request.form.get('student_name')
        for i in students:
            a = i.first_name.lower()
            b = name.lower()
            if a == b:
                searched_students.append(i)
        return render_template("all_students.html", students=searched_students)
    students = Student_details.query.all()
    return render_template("all_students.html", students=students)

@app.route("/home/students/student_records/<id>")
def specific_student(id):
    the_student = None
    students = Student_details.query.all()
    att = Attendence.query.all()
    att_available = False
    present = 0
    total = 0
    for k in att:
        if int(k.student_id) == int(id):
            att_available = True
            total += 1
            if k.status == "Present":
                present += 1
    the_att = f"{present}/{total}"
    for i in students:
        if i.id == int(id):
            the_student = i
    return render_template('specific_student.html', student=the_student, len_of_email=len(the_student.email), old=att_available, att_rec=the_att)


@app.route("/home/students/update_records", methods=["GET", "POST"])
def update_student():
    if request.method == "POST":
        students = Student_details.query.all()
        searched_students = []
        name = request.form.get('student_name')
        for i in students:
            a = i.first_name.lower()
            b = name.lower()
            if a == b:
                searched_students.append(i)
        return render_template("update_student.html", students=searched_students)
    students = Student_details.query.all()
    return render_template("update_student.html", students=students)

@app.route("/home/students/update_records/update_student/<id>")
def edit_student(id):
    current_year = datetime.datetime.now().year
    y = []
    for i in range(1950, current_year+1):
        y.append(f"{i}-{i+1}")
    a = id
    the_student = None
    students = Student_details.query.all()
    for i in students:
        if i.id == int(id):
            the_student = i
    return render_template('edit_data.html', student=the_student, years=y)


@app.route("/home/students/update_records/update_student/<id>/student_updated", methods=["GET", "POST"])
def student_updated(id):
    if request.method == "POST":
        batch = request.form.get("batch")
        course = request.form.get("course")
        gender = request.form.get("gender")
        first_name = request.form.get("stfirst")
        middle_name = request.form.get("stmiddle")
        last_name = request.form.get("stlast")
        prfirst_name = request.form.get("prfirst")
        prmiddle_name = request.form.get("prmiddle")
        prlast_name = request.form.get("prlast")
        dob = request.form.get("dob")
        pr_occupation = request.form.get("proccupation")
        street_address = request.form.get("street")
        city = request.form.get("city")
        state = request.form.get("state")
        postal_code = request.form.get("postalcode")
        phone = request.form.get("number")
        parents_phone = request.form.get("prnumber")
        email = request.form.get("email")
        fees = request.form.getlist("fees")[0]
        
        students = Student_details.query.all()
        for i in students:
            if i.id == int(id):
                batch = batch,
                i.course = course,
                i.first_name = first_name.capitalize(),
                i.middle_name = middle_name.capitalize(),
                i.last_name = last_name.capitalize(),
                i.parent_first_name = prfirst_name.capitalize(),
                i.parent_middle_name = prmiddle_name.capitalize(),
                i.parent_last_name = prlast_name.capitalize(),
                i.parents_occupation = pr_occupation.capitalize(),
                i.dob = dob,
                i.street_address = street_address.capitalize(),
                i.city = city.capitalize(),
                i.state = state.capitalize(),
                i.postal_code = postal_code,
                i.phone_no = phone,
                i.parents_phone_no = parents_phone,
                i.fees = fees,
                i.email = email,
                i.gender = gender.capitalize()
                i.entry_by = current_user.name
                db.session.commit()
    
    return redirect(url_for('update_student'))


@app.route("/home/fees", methods=["GET", "POST"])
def fees():
    if request.method == "POST":
        students = Student_details.query.all()
        searched_students = []
        name = request.form.get('student_name')
        for i in students:
            a = i.first_name.lower()
            b = name.lower()
            if a == b:
                searched_students.append(i)
        return render_template("fees.html", students=searched_students)
    students = Student_details.query.all()
    return render_template("fees.html", students=students)


@app.route("/payment_done/<id>", methods=["GET", "POST"])
def payment_done(id):
    students = Student_details.query.all()
    for i in students:
        if i.id == int(id):
            i.fees = "Done"
            db.session.commit()
            new_fees = Fees(
                course = i.course,
                roll_no = i.roll_no,
                name = f"{i.first_name} {i.middle_name} {i.last_name}",
                entry_by = current_user.name,
                batch = i.batch
            )
            db.session.add(new_fees)
            db.session.commit()
            flash('Record Updated :)')
    return redirect(url_for("fees"))


@app.route('/home/attendence', methods=["GET", "POST"])
def attendence():
    if request.method == "POST":
        a = request.form.get('course')
        subject = None
        if a=="FYBCOM":
            subject=FYBCOM
        elif a=="SYBCOM":
            subject=SYBCOM
        elif a=="TYBCOM":
            subject=TYBCOM
        elif a=="FYBAF":
            subject=FYBAF
        elif a=="SYBAF":
            subject=SYBAF
        elif a=="TYBAF":
            subject=TYBAF
        elif a=="FYBMS":
            subject=FYBMS
        elif a=="SYBMS":
            subject=SYBMS
        elif a=="TYBMS":
            subject=TYBMS
        elif a=="FYBSCIT":
            subject=FYBSCIT
        elif a=="SYBSCIT":
            subject=SYBSCIT
        elif a=="TYBSCIT":
            subject=TYBSCIT
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        if current_month<=3:
            current_year = f"{current_year-1}-{current_year}"
        else:
            current_year = f"{current_year}-{current_year+1}"
        students = db.session.query(Student_details).filter(Student_details.batch==current_year).filter(Student_details.course==a)
        students_list = list(students)
        print(students_list)
        return render_template("submit_attendence.html", course=a, subject=subject, course_students=students_list, date = datetime.date.today())
    
    return render_template("submit_attendence.html", date = datetime.date.today())


@app.route("/submit_attendence", methods=["GET", "POST"])
def submit_att():
    course = request.form.get('selected_course')
    print(course)
    a = request.form.getlist('attendence')
    b = request.form.get('subject')
    add_attendence(present=a, subject=b, course=course)
    return redirect(url_for('attendence'))


@app.route("/delete_record/<id>", methods=["GET", "POST"])
def del_record(id):
    students = Student_details.query.all()
    for i in students:
        if i.id == int(id):
            del_record = Deleted_records(
            batch = i.batch,
            course = i.course,
            first_name = i.first_name.capitalize(),
            middle_name = i.middle_name.capitalize(),
            last_name = i.last_name.capitalize(),
            parent_first_name = i.parent_first_name.capitalize(),
            parent_middle_name = i.parent_middle_name.capitalize(),
            parent_last_name = i.parent_last_name.capitalize(),
            parents_occupation = i.parents_occupation.capitalize(),
            dob = i.dob,
            street_address = i.street_address.capitalize(),
            city = i.city.capitalize(),
            state = i.state.capitalize(),
            postal_code = i.postal_code,
            phone_no = i.phone_no,
            parents_phone_no = i.parents_phone_no,
            fees = i.fees,
            email = i.email,
            gender = i.gender.capitalize(),
            entry_by = current_user.name,
            roll_no = i.roll_no,
            admission_date = i.admission_date
            )
            db.session.add(del_record)
            db.session.commit()
            db.session.delete(i)
            db.session.commit()
            
    return redirect(url_for('all_students'))


if __name__ == "__main__":
    app.run(debug=True, port=3307)