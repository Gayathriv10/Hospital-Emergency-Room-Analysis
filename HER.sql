USE hospital_system;
--select * from Admins;
--select * from Departments order by DepartmentID asc;
--select * from Doctors;
select * from Patients;
--select * from PatientUsers;
--select * from Specializations;
--select * from VisitHistory;

/*
CREATE TABLE Admins (
    admin_id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) UNIQUE NOT NULL,
    email NVARCHAR(100) UNIQUE NOT NULL,
    password NVARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);*/
/*
INSERT INTO Admins (username, email, password)
VALUES 
('superadmin', 'superadmin@hospital.com', 'admin123'),
('er_admin', 'eradmin@hospital.com', 'er@123'),
('system_admin', 'sysadmin@hospital.com', 'sys@123'),
('operations_admin', 'operations@hospital.com', 'ops@123');*/

/*
CREATE TABLE PatientUsers (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) UNIQUE NOT NULL,
    email NVARCHAR(100) UNIQUE NOT NULL,
    password NVARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);*/

/*
CREATE TABLE Doctors (
    doctor_id INT IDENTITY(1,1) PRIMARY KEY,
    doctor_name NVARCHAR(100) NOT NULL,
    department NVARCHAR(100) NOT NULL,
    specialization NVARCHAR(150),
    availability_status NVARCHAR(20) DEFAULT 'Available',
    patients_assigned_today INT DEFAULT 0,
    contact_email NVARCHAR(100),
    created_at DATETIME DEFAULT GETDATE()
);*/

/*
INSERT INTO Doctors (doctor_name, department, specialization, availability_status, patients_assigned_today, contact_email)
VALUES
-- General Medicine (4)
('Dr. Arun Kumar', 'General Medicine', 'Cold & Cough Treatment', 'Available', 2, 'arun.gm@hospital.com'),
('Dr. Meena Ravi', 'General Medicine', 'Fever Management', 'Available', 1, 'meena.gm@hospital.com'),
('Dr. Suresh Babu', 'General Medicine', 'Diabetes & Hypertension Care', 'Available', 3, 'suresh.gm@hospital.com'),
('Dr. Kavitha R', 'General Medicine', 'Stomach Pain & Gastritis', 'Available', 0, 'kavitha.gm@hospital.com'),

-- Emergency Medicine (4)
('Dr. Rajesh N', 'Emergency Medicine', 'Trauma Care', 'Available', 5, 'rajesh.em@hospital.com'),
('Dr. Priya S', 'Emergency Medicine', 'Accident & Injury Management', 'Available', 4, 'priya.em@hospital.com'),
('Dr. Karthik V', 'Emergency Medicine', 'Cardiac Emergency', 'Available', 6, 'karthik.em@hospital.com'),
('Dr. Divya M', 'Emergency Medicine', 'Critical Resuscitation', 'Available', 3, 'divya.em@hospital.com'),

-- Cardiology (4)
('Dr. Harish P', 'Cardiology', 'Interventional Cardiology', 'Available', 2, 'harish.cardio@hospital.com'),
('Dr. Anitha L', 'Cardiology', 'Heart Failure Management', 'Available', 1, 'anitha.cardio@hospital.com'),
('Dr. Manoj K', 'Cardiology', 'ECG & Stress Testing', 'Available', 3, 'manoj.cardio@hospital.com'),
('Dr. Rekha D', 'Cardiology', 'Cardiac Monitoring', 'Available', 2, 'rekha.cardio@hospital.com'),

-- Orthopedics (4)
('Dr. Vignesh T', 'Orthopedics', 'Fracture Treatment', 'Available', 2, 'vignesh.ortho@hospital.com'),
('Dr. Lakshmi P', 'Orthopedics', 'Joint Replacement', 'Available', 1, 'lakshmi.ortho@hospital.com'),
('Dr. Pradeep R', 'Orthopedics', 'Spine Disorders', 'Available', 3, 'pradeep.ortho@hospital.com'),
('Dr. Shalini S', 'Orthopedics', 'Sports Injuries', 'Available', 0, 'shalini.ortho@hospital.com'),

-- Neurology (4)
('Dr. Ajay M', 'Neurology', 'Stroke Management', 'Available', 1, 'ajay.neuro@hospital.com'),
('Dr. Nisha K', 'Neurology', 'Epilepsy Treatment', 'Available', 2, 'nisha.neuro@hospital.com'),
('Dr. Deepak V', 'Neurology', 'Migraine Care', 'Available', 1, 'deepak.neuro@hospital.com'),
('Dr. Swathi R', 'Neurology', 'Neuro Monitoring', 'Available', 0, 'swathi.neuro@hospital.com'),

-- Gynecology (4)
('Dr. Bhavani S', 'Gynecology', 'Pregnancy Care', 'Available', 3, 'bhavani.gyn@hospital.com'),
('Dr. Aishwarya P', 'Gynecology', 'High-Risk Pregnancy', 'Available', 2, 'aishwarya.gyn@hospital.com'),
('Dr. Keerthana R', 'Gynecology', 'Menstrual Disorders', 'Available', 1, 'keerthana.gyn@hospital.com'),
('Dr. Latha M', 'Gynecology', 'PCOS Treatment', 'Available', 2, 'latha.gyn@hospital.com'),

-- Pediatrics (4)
('Dr. Sanjay K', 'Pediatrics', 'Child Fever & Infection', 'Available', 2, 'sanjay.ped@hospital.com'),
('Dr. Renu T', 'Pediatrics', 'Vaccination & Immunization', 'Available', 1, 'renu.ped@hospital.com'),
('Dr. Aravind S', 'Pediatrics', 'Newborn Care', 'Available', 3, 'aravind.ped@hospital.com'),
('Dr. Megha N', 'Pediatrics', 'Child Nutrition', 'Available', 1, 'megha.ped@hospital.com'),

-- Oncology (3)
('Dr. Vikram J', 'Oncology', 'Medical Oncology', 'Available', 2, 'vikram.onco@hospital.com'),
('Dr. Sneha L', 'Oncology', 'Radiation Oncology', 'Available', 1, 'sneha.onco@hospital.com'),
('Dr. Rahul M', 'Oncology', 'Chemotherapy Services', 'Available', 2, 'rahul.onco@hospital.com'),

-- Nephrology (3)
('Dr. Mahesh P', 'Nephrology', 'Kidney Disorders', 'Available', 1, 'mahesh.nephro@hospital.com'),
('Dr. Gayathri R', 'Nephrology', 'Dialysis Treatment', 'Available', 2, 'gayathri.nephro@hospital.com'),
('Dr. Sandeep K', 'Nephrology', 'Renal Care', 'Available', 1, 'sandeep.nephro@hospital.com'),

-- Urology (3)
('Dr. Kiran S', 'Urology', 'Kidney Stone Treatment', 'Available', 1, 'kiran.uro@hospital.com'),
('Dr. Raghav M', 'Urology', 'Urinary Tract Surgery', 'Available', 2, 'raghav.uro@hospital.com'),
('Dr. Preethi L', 'Urology', 'Prostate Care', 'Available', 1, 'preethi.uro@hospital.com'),

-- Critical Care Unit (3)
('Dr. Naveen T', 'Critical Care Unit', 'ICU Monitoring', 'Available', 4, 'naveen.ccu@hospital.com'),
('Dr. Monika S', 'Critical Care Unit', 'Ventilator Support', 'Available', 3, 'monika.ccu@hospital.com'),
('Dr. Ajith R', 'Critical Care Unit', 'Critical Emergency Care', 'Available', 5, 'ajith.ccu@hospital.com');*/

/*
ALTER TABLE Patients
ADD assigned_doctor_id INT NULL;
ALTER TABLE Patients
ADD CONSTRAINT FK_Patient_Doctor
FOREIGN KEY (assigned_doctor_id)
REFERENCES Doctors(doctor_id);*/

/*
CREATE TABLE Departments (
    DepartmentID INT PRIMARY KEY IDENTITY(1,1),
    DepartmentName VARCHAR(100) UNIQUE
);*/
/*
INSERT INTO Departments (DepartmentName) VALUES
('General Medicine'),
('Emergency Medicine'),
('Cardiology'),
('Orthopedics'),
('Neurology'),
('Gynecology'),
('Pediatrics'),
('Oncology'),
('Nephrology'),
('Urology'),
('Gastroenterology'),
('Pulmonology'),
('Endocrinology'),
('Psychiatry'),
('Ophthalmology'),
('Hematology'),
('Dermatology'),
('ENT'),
('Radiology'),
('Anesthesiology'),
('Rheumatology'),
('Infectious Diseases'),
('Geriatrics'),
('Immunology'),
('Vascular Surgery'),
('Neonatology'),
('Critical Care Unit'),
('Pain Management'),
('Sports Medicine'),
('Pathology'),
('Rehabilitation Medicine');*/


/*
CREATE TABLE Specializations (
    SpecializationID INT IDENTITY(1,1) PRIMARY KEY,
    DepartmentID INT NOT NULL,
    SpecializationName NVARCHAR(150) NOT NULL,

    CONSTRAINT FK_Specialization_Department
    FOREIGN KEY (DepartmentID)
    REFERENCES Departments(DepartmentID)
);*/

/*
INSERT INTO Specializations (DepartmentID, SpecializationName)

-- General Medicine
SELECT DepartmentID, 'Cold & Cough Treatment' FROM Departments WHERE DepartmentName='General Medicine'
UNION ALL
SELECT DepartmentID, 'Fever Management' FROM Departments WHERE DepartmentName='General Medicine'
UNION ALL
SELECT DepartmentID, 'Diabetes & Hypertension Care' FROM Departments WHERE DepartmentName='General Medicine'
UNION ALL
SELECT DepartmentID, 'Stomach Pain & Gastritis' FROM Departments WHERE DepartmentName='General Medicine'

-- Emergency Medicine
UNION ALL
SELECT DepartmentID, 'Trauma Care' FROM Departments WHERE DepartmentName='Emergency Medicine'
UNION ALL
SELECT DepartmentID, 'Accident & Injury Management' FROM Departments WHERE DepartmentName='Emergency Medicine'
UNION ALL
SELECT DepartmentID, 'Cardiac Emergency' FROM Departments WHERE DepartmentName='Emergency Medicine'
UNION ALL
SELECT DepartmentID, 'Critical Resuscitation' FROM Departments WHERE DepartmentName='Emergency Medicine'

-- Cardiology
UNION ALL
SELECT DepartmentID, 'Interventional Cardiology' FROM Departments WHERE DepartmentName='Cardiology'
UNION ALL
SELECT DepartmentID, 'Heart Failure Management' FROM Departments WHERE DepartmentName='Cardiology'
UNION ALL
SELECT DepartmentID, 'ECG & Stress Testing' FROM Departments WHERE DepartmentName='Cardiology'

-- Orthopedics
UNION ALL
SELECT DepartmentID, 'Fracture Treatment' FROM Departments WHERE DepartmentName='Orthopedics'
UNION ALL
SELECT DepartmentID, 'Joint Replacement' FROM Departments WHERE DepartmentName='Orthopedics'
UNION ALL
SELECT DepartmentID, 'Spine Disorders' FROM Departments WHERE DepartmentName='Orthopedics'

-- Neurology
UNION ALL
SELECT DepartmentID, 'Stroke Management' FROM Departments WHERE DepartmentName='Neurology'
UNION ALL
SELECT DepartmentID, 'Epilepsy Treatment' FROM Departments WHERE DepartmentName='Neurology'
UNION ALL
SELECT DepartmentID, 'Migraine & Headache Care' FROM Departments WHERE DepartmentName='Neurology'

-- Gynecology
UNION ALL
SELECT DepartmentID, 'Pregnancy Care' FROM Departments WHERE DepartmentName='Gynecology'
UNION ALL
SELECT DepartmentID, 'High-Risk Pregnancy' FROM Departments WHERE DepartmentName='Gynecology'
UNION ALL
SELECT DepartmentID, 'Menstrual Disorders' FROM Departments WHERE DepartmentName='Gynecology'
UNION ALL
SELECT DepartmentID, 'PCOS Treatment' FROM Departments WHERE DepartmentName='Gynecology'

-- Pediatrics
UNION ALL
SELECT DepartmentID, 'Child Fever & Infection' FROM Departments WHERE DepartmentName='Pediatrics'
UNION ALL
SELECT DepartmentID, 'Vaccination & Immunization' FROM Departments WHERE DepartmentName='Pediatrics'
UNION ALL
SELECT DepartmentID, 'Newborn Care' FROM Departments WHERE DepartmentName='Pediatrics'

-- Oncology
UNION ALL
SELECT DepartmentID, 'Medical Oncology' FROM Departments WHERE DepartmentName='Oncology'
UNION ALL
SELECT DepartmentID, 'Radiation Oncology' FROM Departments WHERE DepartmentName='Oncology'
UNION ALL
SELECT DepartmentID, 'Chemotherapy Services' FROM Departments WHERE DepartmentName='Oncology'

-- Nephrology
UNION ALL
SELECT DepartmentID, 'Kidney Disorders' FROM Departments WHERE DepartmentName='Nephrology'
UNION ALL
SELECT DepartmentID, 'Dialysis Treatment' FROM Departments WHERE DepartmentName='Nephrology'

-- Urology
UNION ALL
SELECT DepartmentID, 'Urinary Tract Surgery' FROM Departments WHERE DepartmentName='Urology'
UNION ALL
SELECT DepartmentID, 'Kidney Stone Treatment' FROM Departments WHERE DepartmentName='Urology'

-- Gastroenterology
UNION ALL
SELECT DepartmentID, 'Digestive System Disorders' FROM Departments WHERE DepartmentName='Gastroenterology'
UNION ALL
SELECT DepartmentID, 'Endoscopy Services' FROM Departments WHERE DepartmentName='Gastroenterology'

-- Pulmonology
UNION ALL
SELECT DepartmentID, 'Asthma & COPD Care' FROM Departments WHERE DepartmentName='Pulmonology'
UNION ALL
SELECT DepartmentID, 'Respiratory Infection Treatment' FROM Departments WHERE DepartmentName='Pulmonology'

-- Endocrinology
UNION ALL
SELECT DepartmentID, 'Thyroid Disorders' FROM Departments WHERE DepartmentName='Endocrinology'
UNION ALL
SELECT DepartmentID, 'Hormonal Imbalance Treatment' FROM Departments WHERE DepartmentName='Endocrinology'

-- Psychiatry
UNION ALL
SELECT DepartmentID, 'Depression Treatment' FROM Departments WHERE DepartmentName='Psychiatry'
UNION ALL
SELECT DepartmentID, 'Anxiety & Stress Management' FROM Departments WHERE DepartmentName='Psychiatry'

-- Ophthalmology
UNION ALL
SELECT DepartmentID, 'Cataract Surgery' FROM Departments WHERE DepartmentName='Ophthalmology'
UNION ALL
SELECT DepartmentID, 'Vision Correction' FROM Departments WHERE DepartmentName='Ophthalmology'

-- Hematology
UNION ALL
SELECT DepartmentID, 'Blood Disorders' FROM Departments WHERE DepartmentName='Hematology'
UNION ALL
SELECT DepartmentID, 'Anemia Treatment' FROM Departments WHERE DepartmentName='Hematology'

-- Dermatology
UNION ALL
SELECT DepartmentID, 'Skin Allergy Treatment' FROM Departments WHERE DepartmentName='Dermatology'
UNION ALL
SELECT DepartmentID, 'Acne & Cosmetic Dermatology' FROM Departments WHERE DepartmentName='Dermatology'

-- ENT
UNION ALL
SELECT DepartmentID, 'Ear Infection Treatment' FROM Departments WHERE DepartmentName='ENT'
UNION ALL
SELECT DepartmentID, 'Sinus & Throat Care' FROM Departments WHERE DepartmentName='ENT'

-- Radiology
UNION ALL
SELECT DepartmentID, 'X-Ray Services' FROM Departments WHERE DepartmentName='Radiology'
UNION ALL
SELECT DepartmentID, 'MRI & CT Scan' FROM Departments WHERE DepartmentName='Radiology'

-- Critical Care Unit
UNION ALL
SELECT DepartmentID, 'ICU Monitoring' FROM Departments WHERE DepartmentName='Critical Care Unit'
UNION ALL
SELECT DepartmentID, 'Ventilator Support' FROM Departments WHERE DepartmentName='Critical Care Unit'

-- Pain Management
UNION ALL
SELECT DepartmentID, 'Chronic Pain Therapy' FROM Departments WHERE DepartmentName='Pain Management'

-- Sports Medicine
UNION ALL
SELECT DepartmentID, 'Sports Injury Treatment' FROM Departments WHERE DepartmentName='Sports Medicine'

-- Pathology
UNION ALL
SELECT DepartmentID, 'Lab Diagnostics' FROM Departments WHERE DepartmentName='Pathology'

-- Rehabilitation Medicine
UNION ALL
SELECT DepartmentID, 'Physiotherapy & Recovery' FROM Departments WHERE DepartmentName='Rehabilitation Medicine';*/

/*
CREATE TABLE VisitHistory (
    visit_id INT IDENTITY(1,1) PRIMARY KEY,
    Patient_ID INT NOT NULL,
    visit_type NVARCHAR(50),   -- New Treatment / Regular Checkup
    symptoms NVARCHAR(300),
    diagnosis NVARCHAR(300),
    emergency_flag BIT DEFAULT 0,
    assigned_doctor_id INT NULL,
    wait_time FLOAT,
    visit_datetime DATETIME DEFAULT GETDATE(),

    CONSTRAINT FK_Visit_Patient
    FOREIGN KEY (patient_id)
    REFERENCES Patients(Patient_ID),

    CONSTRAINT FK_Visit_Doctor
    FOREIGN KEY (assigned_doctor_id)
    REFERENCES Doctors(doctor_id)
);*/
