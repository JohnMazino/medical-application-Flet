import psycopg2
from psycopg2 import sql

# Глобальные переменные для параметров подключения
DB_HOST = None
DB_NAME = None
DB_USER = None
DB_PASSWORD = None

def set_db_credentials(host, name, user, password):
    global DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
    DB_HOST = host
    DB_NAME = name
    DB_USER = user
    DB_PASSWORD = password

def get_connection():
    if not all([DB_HOST, DB_NAME, DB_USER, DB_PASSWORD]):
        raise ValueError("Database credentials are not set.")
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Функции для работы с таблицей Пациенты
def add_patient(patient_id, full_name, patient_category, passport_number, insurance_policy_number, admission_date, citizenship):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO Patients (Patient_id, Full_Name, Patient_Category, Passport_Number, Insurance_Policy_Number, Admission_Date, Citizenship) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (patient_id, full_name, patient_category, passport_number, insurance_policy_number, admission_date, citizenship)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

def get_patients():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Patients ORDER BY Patient_id ASC")
        patients = cur.fetchall()
        return patients
    finally:
        cur.close()
        conn.close()

def update_patient(patient_id, new_id, full_name, patient_category, passport_number, insurance_policy_number, admission_date, citizenship):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM Patients WHERE Patient_id = %s", (new_id,))
        count = cur.fetchone()[0]
        if count > 0 and new_id != patient_id:
            raise ValueError(f"ID {new_id} already exists.")
        update_fields = []
        params = []
        if new_id != patient_id:
            update_fields.append("Patient_id = %s")
            params.append(new_id)
        if full_name:
            update_fields.append("Full_Name = %s")
            params.append(full_name)
        if patient_category:
            update_fields.append("Patient_Category = %s")
            params.append(patient_category)
        if passport_number:
            update_fields.append("Passport_Number = %s")
            params.append(passport_number)
        if insurance_policy_number:
            update_fields.append("Insurance_Policy_Number = %s")
            params.append(insurance_policy_number)
        if admission_date:
            update_fields.append("Admission_Date = %s")
            params.append(admission_date)
        if citizenship:
            update_fields.append("Citizenship = %s")
            params.append(citizenship)
        if update_fields:
            params.append(patient_id)
            query = f"UPDATE Patients SET {', '.join(update_fields)} WHERE Patient_id = %s"
            cur.execute(query, params)
        conn.commit()
    finally:
        cur.close()
        conn.close()

def delete_patient(patient_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM Patients WHERE Patient_id = %s",
            (patient_id,)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

def check_id_exists(patient_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM Patients WHERE Patient_id = %s", (patient_id,))
        count = cur.fetchone()[0]
        return count > 0
    finally:
        cur.close()
        conn.close()

def search_patients_by_id(patient_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Patients WHERE Patient_id = %s", (patient_id,))
        patient = cur.fetchone()
        return patient
    finally:
        cur.close()
        conn.close()

#врачи
def add_doctor(doctor_id, full_name, category, specialty, salary, contact_phone):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO Doctors (Doctor_id, Full_Name, Category, Specialty, Salary, Contact_Phone)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (doctor_id, full_name, category, specialty, salary, contact_phone)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

def get_doctors():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Doctors ORDER BY Doctor_id ASC")
        doctors = cur.fetchall()
        return doctors
    finally:
        cur.close()
        conn.close()

def update_doctor(doctor_id, new_id, full_name, category, specialty, salary, contact_phone):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM Doctors WHERE Doctor_id = %s", (new_id,))
        count = cur.fetchone()[0]
        if count > 0 and new_id != doctor_id:
            raise ValueError(f"ID {new_id} already exists.")
        update_fields = []
        params = []
        if new_id != doctor_id:
            update_fields.append("Doctor_id = %s")
            params.append(new_id)
        if full_name:
            update_fields.append("Full_Name = %s")
            params.append(full_name)
        if category:
            update_fields.append("Category = %s")
            params.append(category)
        if specialty:
            update_fields.append("Specialty = %s")
            params.append(specialty)
        if salary is not None:
            update_fields.append("Salary = %s")
            params.append(salary)
        if contact_phone:
            update_fields.append("Contact_Phone = %s")
            params.append(contact_phone)
        
        if update_fields:
            params.append(doctor_id)
            query = f"UPDATE Doctors SET {', '.join(update_fields)} WHERE Doctor_id = %s"
            cur.execute(query, params)
        
        conn.commit()
    finally:
        cur.close()
        conn.close()

def delete_doctor(doctor_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM Doctors WHERE Doctor_id = %s",
            (doctor_id,)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

def check_doctor_id_exists(doctor_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM Doctors WHERE Doctor_id = %s", (doctor_id,))
        count = cur.fetchone()[0]
        return count > 0
    finally:
        cur.close()
        conn.close()

def search_doctors_by_id(doctor_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Doctors WHERE Doctor_id = %s", (doctor_id,))
        doctor = cur.fetchone()
        return doctor
    finally:
        cur.close()
        conn.close()

# Функции для работы с таблицей Страховые компании
def add_insurance_company(company_id, name, license_number, director_full_name, contact_phone):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO Insurance_Companies (Company_id, Name, License_Number, Director_Full_Name, Contact_Phone)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (company_id, name, license_number, director_full_name, contact_phone)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

def get_insurance_companies():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Insurance_Companies ORDER BY Company_id ASC")
        companies = cur.fetchall()
        return companies
    finally:
        cur.close()
        conn.close()

def update_insurance_company(company_id, new_id, name, license_number, director_full_name, contact_phone):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM Insurance_Companies WHERE Company_id = %s", (new_id,))
        count = cur.fetchone()[0]
        if count > 0 and new_id != company_id:
            raise ValueError(f"ID {new_id} already exists.")
        update_fields = []
        params = []
        if new_id != company_id:
            update_fields.append("Company_id = %s")
            params.append(new_id)
        if name:
            update_fields.append("Name = %s")
            params.append(name)
        if license_number:
            update_fields.append("License_Number = %s")
            params.append(license_number)
        if director_full_name:
            update_fields.append("Director_Full_Name = %s")
            params.append(director_full_name)
        if contact_phone:
            update_fields.append("Contact_Phone = %s")
            params.append(contact_phone)
        
        if update_fields:
            params.append(company_id)
            query = f"UPDATE Insurance_Companies SET {', '.join(update_fields)} WHERE Company_id = %s"
            cur.execute(query, params)
        
        conn.commit()
    finally:
        cur.close()
        conn.close()

def delete_insurance_company(company_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM Insurance_Companies WHERE Company_id = %s",
            (company_id,)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

def check_insurance_company_id_exists(company_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM Insurance_Companies WHERE Company_id = %s", (company_id,))
        count = cur.fetchone()[0]
        return count > 0
    finally:
        cur.close()
        conn.close()

def search_insurance_companies_by_id(company_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Insurance_Companies WHERE Company_id = %s", (company_id,))
        company = cur.fetchone()
        return company
    finally:
        cur.close()
        conn.close()

# Функции для работы с таблицей Договоры
def add_contract(contract_id, patient_id, doctor_id, department, company_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO Contracts (Contract_id, Patient_id, Doctor_id, Department, Company_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (contract_id, patient_id, doctor_id, department, company_id)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

def get_contracts():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Contracts ORDER BY Contract_id ASC")
        contracts = cur.fetchall()
        return contracts
    finally:
        cur.close()
        conn.close()

def update_contract(contract_id, new_id, patient_id, doctor_id, department, company_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM Contracts WHERE Contract_id = %s", (new_id,))
        count = cur.fetchone()[0]
        if count > 0 and new_id != contract_id:
            raise ValueError(f"ID {new_id} already exists.")
        update_fields = []
        params = []
        if new_id != contract_id:
            update_fields.append("Contract_id = %s")
            params.append(new_id)
        if patient_id is not None:
            update_fields.append("Patient_id = %s")
            params.append(patient_id)
        if doctor_id is not None:
            update_fields.append("Doctor_id = %s")
            params.append(doctor_id)
        if department:
            update_fields.append("Department = %s")
            params.append(department)
        if company_id is not None:
            update_fields.append("Company_id = %s")
            params.append(company_id)
        
        if update_fields:
            params.append(contract_id)
            query = f"UPDATE Contracts SET {', '.join(update_fields)} WHERE Contract_id = %s"
            cur.execute(query, params)
        
        conn.commit()
    finally:
        cur.close()
        conn.close()

def delete_contract(contract_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM Contracts WHERE Contract_id = %s",
            (contract_id,)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

def check_contract_id_exists(contract_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM Contracts WHERE Contract_id = %s", (contract_id,))
        count = cur.fetchone()[0]
        return count > 0
    finally:
        cur.close()
        conn.close()

def search_contracts_by_id(contract_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Contracts WHERE Contract_id = %s", (contract_id,))
        contract = cur.fetchone()
        return contract
    finally:
        cur.close()
        conn.close()

# Функции для работы с таблицей Обследования
def add_examination(examination_id, patient_id, doctor_id, name, type, examination_date, cost):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO Examinations (Examination_id, Patient_id, Doctor_id, Name, Type, Examination_Date, Cost)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (examination_id, patient_id, doctor_id, name, type, examination_date, cost)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

def get_examinations():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Examinations ORDER BY Examination_id ASC")
        examinations = cur.fetchall()
        return examinations
    finally:
        cur.close()
        conn.close()

def update_examination(examination_id, new_id, patient_id, doctor_id, name, type, examination_date, cost):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM Examinations WHERE Examination_id = %s", (new_id,))
        count = cur.fetchone()[0]
        if count > 0 and new_id != examination_id:
            raise ValueError(f"ID {new_id} already exists.")
        update_fields = []
        params = []
        if new_id != examination_id:
            update_fields.append("Examination_id = %s")
            params.append(new_id)
        if patient_id is not None:
            update_fields.append("Patient_id = %s")
            params.append(patient_id)
        if doctor_id is not None:
            update_fields.append("Doctor_id = %s")
            params.append(doctor_id)
        if name:
            update_fields.append("Name = %s")
            params.append(name)
        if type:
            update_fields.append("Type = %s")
            params.append(type)
        if examination_date:
            update_fields.append("Examination_Date = %s")
            params.append(examination_date)
        if cost is not None:
            update_fields.append("Cost = %s")
            params.append(cost)
        
        if update_fields:
            params.append(examination_id)
            query = f"UPDATE Examinations SET {', '.join(update_fields)} WHERE Examination_id = %s"
            cur.execute(query, params)
        
        conn.commit()
    finally:
        cur.close()
        conn.close()

def delete_examination(examination_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM Examinations WHERE Examination_id = %s",
            (examination_id,)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

def check_examination_id_exists(examination_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM Examinations WHERE Examination_id = %s", (examination_id,))
        count = cur.fetchone()[0]
        return count > 0
    finally:
        cur.close()
        conn.close()

def search_examinations(search_query):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT * FROM Examinations
            WHERE Examination_id = %s OR Name ILIKE %s OR Type ILIKE %s
            """,
            (search_query, f"%{search_query}%", f"%{search_query}%")
        )
        examinations = cur.fetchall()
        return examinations
    finally:
        cur.close()
        conn.close()

def search_examinations_by_id(examination_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Examinations WHERE Examination_id = %s", (examination_id,))
        examination = cur.fetchone()
        return examination
    finally:
        cur.close()
        conn.close()


