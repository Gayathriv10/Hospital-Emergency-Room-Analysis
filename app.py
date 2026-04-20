import os
from flask import Flask, render_template, request, redirect, session, jsonify, url_for
import pandas as pd
import pyodbc
import joblib
from datetime import datetime

app = Flask(__name__)
app.secret_key = "hospital_super_secret_key"

# Try to load ML model
MODEL_PATH = "waittime_model2.pkl"
model = None
try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("Model loaded successfully")
    else:
        print(f"Warning: Model file {MODEL_PATH} not found.")
except Exception as e:
    print(f"Error loading model: {e}")

# Database Connection Helper
def get_db_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=.\\SQLEXPRESS;'
            'DATABASE=hospital_system;'
            'Trusted_Connection=yes;'
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# ================= ROUTES ================= 

@app.route("/")
def index():
    return render_template("index.html")

# --------- ADMIN PORTAL ---------
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        conn = get_db_connection()
        if not conn:
            return render_template("admin_login.html", error="Database connection failed")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Admins WHERE username=? AND password=?", (username, password))
        admin = cursor.fetchone()
        conn.close()
        
        if admin:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template("admin_login.html", error="Invalid Credentials")
            
    return render_template("admin_login.html")

@app.route("/admin_dashboard")
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM Doctors")
    total_doctors = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM Patients")
    total_patients = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM Doctors WHERE availability_status='Available'")
    available_doctors = cursor.fetchone()[0]
    
    conn.close()
    
    return render_template("admin_dashboard.html", 
                           total_doctors=total_doctors, 
                           total_patients=total_patients, 
                           available_doctors=available_doctors)

@app.route("/doctor_status")
def doctor_status():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT doctor_name, specialization, department, availability_status, doctor_id FROM Doctors")
    doctors = cursor.fetchall()
    conn.close()
    
    return render_template("doctor_status.html", doctors=doctors)

@app.route("/toggle_doctor_status/<int:doctor_id>", methods=["POST"])
def toggle_doctor_status(doctor_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Doctors SET availability_status='Available' WHERE doctor_id=?", (doctor_id,))
    conn.commit()
    conn.close()
        
    return redirect(url_for('doctor_status'))

@app.route("/recent_patients")
def recent_patients():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    # Join with Patients to get details, using VisitHistory as base
    cursor.execute("""
        SELECT TOP 20 
            v.Patient_ID, 
            p.Patient_First_Initial, 
            p.Patient_Last_Name, 
            p.Department_Referral, 
            CONVERT(VARCHAR(19), v.visit_datetime, 120) AS visit_datetime, 
            d.doctor_name, 
            v.wait_time 
        FROM VisitHistory v
        LEFT JOIN Patients p ON v.Patient_ID = p.Patient_ID
        LEFT JOIN Doctors d ON v.assigned_doctor_id = d.doctor_id
        ORDER BY v.visit_datetime DESC
    """)
    recent = cursor.fetchall()
    conn.close()
    
    return render_template("recent_patients.html", recent=recent)

@app.route("/all_patients")
def all_patients():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    # Join with Patients to get all patient details
    cursor.execute("""
        SELECT 
            p.Patient_ID, 
            p.Patient_First_Initial, 
            p.Patient_Last_Name, 
            p.Patient_Age,
            p.Department_Referral, 
            CONVERT(VARCHAR(19), p.Patient_Admission_Date, 120) AS Patient_Admission_Date,
            d.doctor_name, 
            p.Patient_Waittime 
        FROM Patients p
        LEFT JOIN Doctors d ON p.assigned_doctor_id = d.doctor_id
        ORDER BY p.Patient_Admission_Date DESC
    """)
    patients = cursor.fetchall()
    conn.close()
    
    return render_template("all_patients.html", patients=patients)

@app.route("/doctor_assigned")
def doctor_assigned():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            p.Patient_ID, 
            p.Patient_First_Initial, 
            p.Patient_Last_Name, 
            d.doctor_name, 
            d.specialization
        FROM Patients p
        JOIN Doctors d ON p.assigned_doctor_id = d.doctor_id
        ORDER BY p.Patient_Admission_Date DESC
    """)
    assigned = cursor.fetchall()
    conn.close()
    
    return render_template("doctor_assigned.html", assigned=assigned)

@app.route("/waitlist")
def waitlist():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            Patient_ID, 
            Patient_First_Initial, 
            Patient_Last_Name, 
            Patient_Admission_Flag,
            Department_Referral,
            CONVERT(VARCHAR(19), Patient_Admission_Date, 120) AS Patient_Admission_Date
        FROM Patients 
        WHERE assigned_doctor_id IS NULL
        ORDER BY Patient_Admission_Date ASC
    """)
    waitlist_data = cursor.fetchall()
    
    cursor.execute("SELECT doctor_id, doctor_name, department, specialization FROM Doctors WHERE availability_status='Available' ORDER BY department")
    available_doctors = cursor.fetchall()
    
    conn.close()
    
    return render_template("waitlist.html", waitlist=waitlist_data, available_doctors=available_doctors)

@app.route("/assign_doctor_manual", methods=["POST"])
def assign_doctor_manual():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
        
    patient_id = request.form.get("patient_id")
    doctor_id = request.form.get("doctor_id")
    
    if not patient_id or not doctor_id:
        return redirect(url_for('waitlist'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT Patient_Admission_Flag, Department_Referral FROM Patients WHERE Patient_ID=?", (patient_id,))
    patient = cursor.fetchone()
    is_emergency = 1 if patient and patient[0] else 0
    
    cursor.execute("UPDATE Patients SET assigned_doctor_id=? WHERE Patient_ID=?", (doctor_id, patient_id))
    cursor.execute("UPDATE Doctors SET availability_status='Busy', patients_assigned_today = patients_assigned_today + 1 WHERE doctor_id=?", (doctor_id,))
    
    cursor.execute("""
        INSERT INTO VisitHistory (Patient_ID, visit_type, emergency_flag, assigned_doctor_id, wait_time, visit_datetime)
        VALUES (?, 'Manual Assignment', ?, ?, 15.0, GETDATE())
    """, (patient_id, is_emergency, doctor_id))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('waitlist'))

@app.route("/emergency_patients")
def emergency_patients():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            CONVERT(VARCHAR(19), v.visit_datetime, 120) AS visit_datetime,
            v.Patient_ID, 
            p.Patient_First_Initial, 
            p.Patient_Last_Name, 
            p.Department_Referral,
            d.doctor_name,
            d.specialization
        FROM VisitHistory v
        JOIN Patients p ON v.Patient_ID = p.Patient_ID
        LEFT JOIN Doctors d ON v.assigned_doctor_id = d.doctor_id
        WHERE v.emergency_flag = 1
        ORDER BY v.visit_datetime DESC
    """)
    patients = cursor.fetchall()
    conn.close()
    
    return render_template("emergency_patients.html", patients=patients)

@app.route("/admin_logout")
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

# --------- PATIENT PORTAL ---------
@app.route("/patient_portal")
def patient_portal():
    return render_template("patient_portal.html")

@app.route("/doctor_waitime")
def doctor_waitime():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get wait time averages per department
    cursor.execute("""
        SELECT p.Department_Referral, AVG(v.wait_time) 
        FROM VisitHistory v
        JOIN Patients p ON v.Patient_ID = p.Patient_ID
        WHERE v.wait_time > 0
        GROUP BY p.Department_Referral
    """)
    wait_data = cursor.fetchall()
    wait_map = {row[0]: row[1] for row in wait_data if row[0]}
    
    # Get all doctors and attach the predicted wait time per department
    cursor.execute("SELECT doctor_id, doctor_name, specialization, department, patients_assigned_today FROM Doctors")
    doctors_db = cursor.fetchall()
    
    doctors = []
    for doc in doctors_db:
        base_predicted = wait_map.get(doc[3], 35.0) # 35 minutes default if no data
        doctor_id = doc[0]
        assigned_today = doc[4] if doc[4] is not None else 0
        
        # Calculate doctor-specific wait time based on assignments
        personal_wait = base_predicted + (assigned_today * 6.5) + (doctor_id % 4 * 1.5) - 3.0
        personal_wait = max(5.0, personal_wait) # Ensure it doesn't go below realistic minimum
        
        doctors.append({
            'doctor_name': doc[1],
            'specialization': doc[2],
            'department': doc[3],
            'predicted_wait': round(personal_wait, 1)
        })
        
    conn.close()
    return render_template("doctor_waitime.html", doctors=doctors)

@app.route("/new_patient")
def new_patient():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ISNULL(MAX(Patient_ID), 0) + 1 FROM Patients")
    next_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT DepartmentName FROM Departments")
    departments = [row[0] for row in cursor.fetchall()]
    conn.close()
    return render_template("new_patient.html", next_id=next_id, departments=departments)

@app.route("/returning_patient_choice")
def returning_patient_choice():
    return render_template("returning_patient_choice.html")

@app.route("/returning_patient", methods=["GET", "POST"])
def returning_patient():
    if request.method == "POST":
        patient_id = request.form.get("patient_id")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Patients WHERE Patient_ID=?", (patient_id,))
        patient = cursor.fetchone()
        
        if patient:
            # Re-allocate a doctor for the checkup and insert to VisitHistory
            department = patient[7] # Department Referral
            age = patient[5]
            admission_status = patient[8] # Admission Flag
            satisfaction = patient[9]
            is_emergency = (admission_status == "Emergency")
            
            gender = patient[4]
            doctor_id, doctor_name, doctor_specialization, alert_message, doctor_status_msg, wait_time = allocate_doctor(cursor, department, age, gender, admission_status, satisfaction, is_emergency)
            
            # Record the visit
            cursor.execute("""
                INSERT INTO VisitHistory (Patient_ID, visit_type, emergency_flag, assigned_doctor_id, wait_time, visit_datetime)
                VALUES (?, ?, ?, ?, ?, GETDATE())
            """, (patient_id, 'Regular Checkup', 1 if is_emergency else 0, doctor_id, wait_time))
            
            if doctor_id:
                cursor.execute("""
                    UPDATE Patients 
                    SET assigned_doctor_id=?, Patient_Waittime=?
                    WHERE Patient_ID=?
                """, (doctor_id, wait_time, patient_id))
            
            conn.commit()
            
            # Fetch assigned doc name cleanly
            assigned_doc_display = doctor_name if doctor_name else "None Available"
            
            conn.close()
            return render_template("returning_patient_details.html", 
                                   patient=patient, 
                                   assigned_doctor=assigned_doc_display,
                                   doctor_specialization=doctor_specialization,
                                   wait_time=round(wait_time, 2),
                                   alert_message=alert_message)
        else:
            conn.close()
            return render_template("returning_patient.html", error="Patient ID not found.")
            
    return render_template("returning_patient.html")

def allocate_doctor(cursor, department, age, gender, admission_status, satisfaction, is_emergency):
    assigned_doctor_id = None
    assigned_doctor_name = None
    assigned_specialization = None
    wait_time = 0.0
    alert_message = ""
    doctor_status_msg = ""
    
    if is_emergency:
        # Emergency: allocate first doctor in department regardless of status, or any available
        cursor.execute("SELECT TOP 1 doctor_id, doctor_name, contact_email, specialization FROM Doctors WHERE department=? AND availability_status='Available'", (department,))
        doc = cursor.fetchone()
        if not doc:
            cursor.execute("SELECT TOP 1 doctor_id, doctor_name, contact_email, specialization FROM Doctors WHERE department=?", (department,))
            doc = cursor.fetchone()
            
        if doc:
            assigned_doctor_id = doc[0]
            assigned_doctor_name = doc[1]
            doc_email = doc[2]
            assigned_specialization = doc[3]
            cursor.execute("UPDATE Doctors SET availability_status='Busy', patients_assigned_today = patients_assigned_today + 1 WHERE doctor_id=?", (assigned_doctor_id,))
            alert_message = f"EMERGENCY ALERT: Dr. {assigned_doctor_name} has been urgently allocated. Alert sent to {doc_email}."
        else:
            assigned_doctor_name = "None Available"
            alert_message = "EMERGENCY: No doctors available in this department!"
    else:
        # Normal allocation
        cursor.execute("SELECT TOP 1 doctor_id, doctor_name, specialization FROM Doctors WHERE department=? AND availability_status='Available'", (department,))
        doc = cursor.fetchone()
        
        if doc:
            assigned_doctor_id = doc[0]
            assigned_doctor_name = doc[1]
            assigned_specialization = doc[2]
            cursor.execute("UPDATE Doctors SET availability_status='Busy', patients_assigned_today = patients_assigned_today + 1 WHERE doctor_id=?", (assigned_doctor_id,))
            doctor_status_msg = "Allocated successfully."
        else:
            assigned_doctor_name = "None (Added to Waitlist)"
            doctor_status_msg = "Not Available"
            
            # Do not delete waitlisted patients, just proceed with wait time prediction
            
            # Predict Wait Time
            if model is not None:
                dept_map = {"Cardiology":1, "Orthopedics":2, "Neurology":3, "Emergency":4, "General Medicine": 5, "Gynecology": 6, "Pediatrics": 7, "Oncology": 8}
                dept_encoded = dept_map.get(department, 0)
                try:
                    is_admitted = 1 if admission_status and admission_status.lower()=='admitted' else 0
                    gender_encoded = 1 if gender and str(gender).lower() == 'female' else 0
                    input_data = pd.DataFrame(
                        [[int(age), gender_encoded, dept_encoded, is_admitted]],
                        columns=["Patient_Age", "Gender_encoded", "Dept_encoded", "Patient_Admission_Flag"]
                    )
                    wait_time = float(model.predict(input_data)[0])
                except Exception as e:
                    print(f"Prediction error: {e}")
                    wait_time = 30.0 # fallback
            else:
                wait_time = 45.0 # fallback
                
    return assigned_doctor_id, assigned_doctor_name, assigned_specialization, alert_message, doctor_status_msg, wait_time


@app.route("/process_patient", methods=["POST"])
def process_patient():
    # Gather form data
    data = request.form
    patient_id = data.get("patient_id") # Generated one
    first_initial = data.get("first_initial")
    last_name = data.get("last_name")
    age = data.get("age", 0)
    gender = data.get("gender")
    department = data.get("department")
    race = data.get("race")
    admission_status = data.get("admission_status")
    satisfaction = data.get("satisfaction", 0)
    treatment_type = data.get("treatment_type", "New Treatment")
    is_emergency = (admission_status == "Emergency")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    doctor_id, doctor_name, doctor_specialization, alert_message, doctor_status_msg, wait_time = allocate_doctor(cursor, department, age, gender, admission_status, satisfaction, is_emergency)
                
    # Map admission status to BIT for the database
    admission_status_db = 1 if admission_status in ["Admitted", "Emergency", "1", "2"] else 0
    
    # Insert patient
    cursor.execute("""
        INSERT INTO Patients (
            Patient_ID, Patient_Admission_Date, Patient_First_Initial, Patient_Last_Name, 
            Patient_Gender, Patient_Age, Patient_Race, Department_Referral, 
            Patient_Admission_Flag, Patient_Satisfaction_Score, Patient_Waittime, assigned_doctor_id
        )
        VALUES (?, GETDATE(), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (patient_id, first_initial, last_name, gender, int(age), race, department, admission_status_db, int(satisfaction), wait_time, doctor_id))
    
    # Insert into VisitHistory
    cursor.execute("""
        INSERT INTO VisitHistory (Patient_ID, visit_type, emergency_flag, assigned_doctor_id, wait_time, visit_datetime)
        VALUES (?, ?, ?, ?, ?, GETDATE())
    """, (patient_id, treatment_type, 1 if is_emergency else 0, doctor_id, wait_time))
    
    conn.commit()
    conn.close()
    
    return render_template("allocation_result.html", 
                           assigned_doctor=doctor_name, 
                           doctor_specialization=doctor_specialization,
                           wait_time=round(wait_time, 2),
                           alert_message=alert_message,
                           doctor_status_msg=doctor_status_msg,
                           is_emergency=is_emergency)

# --------- SMART DASHBOARD ---------
@app.route("/smart_dashboard")
def smart_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get department distribution for graph
    cursor.execute("SELECT Department_Referral, COUNT(*) FROM Patients GROUP BY Department_Referral")
    dept_data = cursor.fetchall()
    departments = [row[0] for row in dept_data if row[0]]
    dept_counts = [row[1] for row in dept_data if row[0]]
    
    # Get wait time averages per department for graph
    cursor.execute("""
        SELECT p.Department_Referral, AVG(v.wait_time) 
        FROM VisitHistory v
        JOIN Patients p ON v.Patient_ID = p.Patient_ID
        WHERE v.wait_time > 0
        GROUP BY p.Department_Referral
    """)
    wait_data = cursor.fetchall()
    wait_departments = [row[0] for row in wait_data if row[0]]
    wait_avgs = [round(row[1], 1) for row in wait_data if row[0]]
    
    # Get emergency vs standard admittance distribution
    cursor.execute("SELECT Patient_Admission_Flag, COUNT(*) FROM Patients GROUP BY Patient_Admission_Flag")
    admit_data = cursor.fetchall()
    admit_labels = [row[0] if row[0] else 'Unknown' for row in admit_data]
    admit_counts = [row[1] for row in admit_data]
    
    
    # Weekly Arrivals
    cursor.execute("""
        SELECT DATENAME(dw, visit_datetime) AS DayOfWeek, COUNT(*)
        FROM VisitHistory
        GROUP BY DATENAME(dw, visit_datetime), DATEPART(dw, visit_datetime)
        ORDER BY DATEPART(dw, visit_datetime)
    """)
    weekly_data = cursor.fetchall()
    weekly_labels = [row[0] if row[0] is not None else "Unknown" for row in weekly_data]
    weekly_counts = [row[1] for row in weekly_data]
    
    conn.close()
    
    return render_template("smart_dashboard.html", 
                           departments=departments, 
                           dept_counts=dept_counts,
                           wait_departments=wait_departments,
                           wait_avgs=wait_avgs,
                           admit_labels=admit_labels,
                           admit_counts=admit_counts,
                           weekly_labels=weekly_labels,
                           weekly_counts=weekly_counts)

# --------- CHATBOT API ---------
@app.route("/chatbot_api", methods=["POST"])
def chatbot_api():
    user_msg = request.json.get("message", "").lower()
    reply = "I'm sorry, I don't understand that. How can I help you regarding the hospital system?"
    
    if "wait" in user_msg or "time" in user_msg:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT AVG(wait_time) FROM VisitHistory WHERE wait_time > 0")
        avg = cursor.fetchone()[0]
        conn.close()
        avg_wait = round(avg, 2) if avg else 25
        reply = f"The average wait time currently is approximately {avg_wait} minutes."
    elif "doctor" in user_msg or "available" in user_msg:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Doctors WHERE availability_status='Available'")
        count = cursor.fetchone()[0]
        conn.close()
        reply = f"We currently have {count} doctors dynamically available across all departments."
    elif "emergency" in user_msg:
        reply = "If this is a medical emergency, please call 911 immediately or proceed to the nearest Emergency Room. Our ER is open 24/7."
    elif "hello" in user_msg or "hi" in user_msg:
        reply = "Hello! I am the Hospital Assistant Chatbot. How can I help you today?"
        
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
