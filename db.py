import psycopg2
from psycopg2 import sql

# Глобальные переменные для параметров подключения
DB_HOST = "localhost"
DB_NAME = "zovApendiks"
DB_USER = "postgres"
DB_PASSWORD = "1111"

def set_db_connection_params(host, dbname, user, password):
    global DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
    DB_HOST = host
    DB_NAME = dbname
    DB_USER = user
    DB_PASSWORD = password

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Функции для работы с таблицей Пациенты
def add_patient(patient_id, fio, category, passport_number, insurance_policy_number, admission_date, citizenship):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO Пациенты (Пациент_id, ФИО, Категория_пациента, Номер_паспорта, Номер_страхового_полиса, Дата_поступления, Гражданство) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (patient_id, fio, category, passport_number, insurance_policy_number, admission_date, citizenship)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

def get_patients():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Пациенты ORDER BY Пациент_id ASC")
        patients = cur.fetchall()
        return patients
    finally:
        cur.close()
        conn.close()

def update_patient(patient_id, new_id, fio, category, passport_number, insurance_policy_number, admission_date, citizenship):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Проверяем, существует ли новый ID
        cur.execute("SELECT COUNT(*) FROM Пациенты WHERE Пациент_id = %s", (new_id,))
        count = cur.fetchone()[0]
        if count > 0 and new_id != patient_id:
            raise ValueError(f"ID {new_id} уже существует.")
        
        # Формируем SQL-запрос для обновления только измененных полей
        update_fields = []
        params = []
        if new_id != patient_id:
            update_fields.append("Пациент_id = %s")
            params.append(new_id)
        if fio:
            update_fields.append("ФИО = %s")
            params.append(fio)
        if category:
            update_fields.append("Категория_пациента = %s")
            params.append(category)
        if passport_number:
            update_fields.append("Номер_паспорта = %s")
            params.append(passport_number)
        if insurance_policy_number:
            update_fields.append("Номер_страхового_полиса = %s")
            params.append(insurance_policy_number)
        if admission_date:
            update_fields.append("Дата_поступления = %s")
            params.append(admission_date)
        if citizenship:
            update_fields.append("Гражданство = %s")
            params.append(citizenship)
        
        if update_fields:
            params.append(patient_id)
            query = f"UPDATE Пациенты SET {', '.join(update_fields)} WHERE Пациент_id = %s"
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
            "DELETE FROM Пациенты WHERE Пациент_id = %s",
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
        cur.execute("SELECT COUNT(*) FROM Пациенты WHERE Пациент_id = %s", (patient_id,))
        count = cur.fetchone()[0]
        return count > 0
    finally:
        cur.close()
        conn.close()

def search_patients_by_id(patient_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Пациенты WHERE Пациент_id = %s", (patient_id,))
        patient = cur.fetchone()
        return patient
    finally:
        cur.close()
        conn.close()

# Функции для работы с таблицей Врачи
def add_doctor(doctor_id, fio, category, specialty, salary, contact_phone):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO doctors (id, full_name, category, specialty, salary, contact_phone) VALUES (%s, %s, %s, %s, %s, %s)",
            (doctor_id, fio, category, specialty, salary, contact_phone)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

def get_doctors():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Врачи ORDER BY Врач_id ASC")
        doctors = cur.fetchall()
        return doctors
    finally:
        cur.close()
        conn.close()

def update_doctor(doctor_id, new_id, fio, category, specialty, salary, contact_phone):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Проверяем, существует ли новый ID
        cur.execute("SELECT COUNT(*) FROM Врачи WHERE Врач_id = %s", (new_id,))
        count = cur.fetchone()[0]
        if count > 0 and new_id != doctor_id:
            raise ValueError(f"ID {new_id} уже существует.")
        
        # Формируем SQL-запрос для обновления только измененных полей
        update_fields = []
        params = []
        if new_id != doctor_id:
            update_fields.append("Врач_id = %s")
            params.append(new_id)
        if fio:
            update_fields.append("ФИО = %s")
            params.append(fio)
        if category:
            update_fields.append("Категория = %s")
            params.append(category)
        if specialty:
            update_fields.append("Специальность = %s")
            params.append(specialty)
        if salary is not None:
            update_fields.append("Оклад = %s")
            params.append(salary)
        if contact_phone:
            update_fields.append("Контактный_телефон = %s")
            params.append(contact_phone)
        
        if update_fields:
            params.append(doctor_id)
            query = f"UPDATE Врачи SET {', '.join(update_fields)} WHERE Врач_id = %s"
            cur.execute(query, params)
            conn.commit()
    finally:
        cur.close()
        conn.close()

def delete_doctor(doctor_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Врачи WHERE Врач_id = %s", (doctor_id,))
        conn.commit()
    finally:
        cur.close()
        conn.close()

def check_doctor_id_exists(doctor_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM Врачи WHERE Врач_id = %s", (doctor_id,))
        count = cur.fetchone()[0]
        return count > 0
    finally:
        cur.close()
        conn.close()

def search_doctors_by_id(doctor_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Врачи WHERE Врач_id = %s", (doctor_id,))
        doctor = cur.fetchone()
        return doctor
    finally:
        cur.close()
        conn.close()

# Функции для работы с таблицей Страховые компании
def add_insurance_company(company_id, name, license_number, director_fio, contact_phone):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO Страховые_компании (id, name, license_number, director_fio, contact_phone) VALUES (%s, %s, %s, %s, %s)",
            (company_id, name, license_number, director_fio, contact_phone)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

def get_insurance_companies():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Страховые_компании ORDER BY Компания_id ASC")
        companies = cur.fetchall()
        return companies
    finally:
        cur.close()
        conn.close()

def update_insurance_company(company_id, new_id, name, license_number, director_fio, contact_phone):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Проверяем, существует ли новый ID
        cur.execute("SELECT COUNT(*) FROM Страховые_компании WHERE Компания_id = %s", (new_id,))
        count = cur.fetchone()[0]
        if count > 0 and new_id != company_id:
            raise ValueError(f"ID {new_id} уже существует.")
        
        # Формируем SQL-запрос для обновления только измененных полей
        update_fields = []
        params = []
        if new_id != company_id:
            update_fields.append("Компания_id = %s")
            params.append(new_id)
        if name:
            update_fields.append("Название = %s")
            params.append(name)
        if license_number:
            update_fields.append("Номер_лицензии = %s")
            params.append(license_number)
        if director_fio:
            update_fields.append("ФИО_руководителя = %s")
            params.append(director_fio)
        if contact_phone:
            update_fields.append("Контактный_телефон = %s")
            params.append(contact_phone)
        
        if update_fields:
            params.append(company_id)
            query = f"UPDATE Страховые_компании SET {', '.join(update_fields)} WHERE Компания_id = %s"
            cur.execute(query, params)
            conn.commit()
    finally:
        cur.close()
        conn.close()

def delete_insurance_company(company_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Страховые_компании WHERE Компания_id = %s", (company_id,))
        conn.commit()
    finally:
        cur.close()
        conn.close()

def check_insurance_company_id_exists(company_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM Страховые_компании WHERE Компания_id = %s", (company_id,))
        count = cur.fetchone()[0]
        return count > 0
    finally:
        cur.close()
        conn.close()

def search_insurance_companies_by_id(company_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Страховые_компании WHERE Компания_id = %s", (company_id,))
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
            "INSERT INTO договоры (id, patient_id, doctor_id, department, company_id) VALUES (%s, %s, %s, %s, %s)",
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
        cur.execute("SELECT * FROM договоры ORDER BY Договор_id ASC")
        contracts = cur.fetchall()
        return contracts
    finally:
        cur.close()
        conn.close()

def update_contract(contract_id, new_id, patient_id, doctor_id, department, company_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Проверяем, существует ли новый ID
        cur.execute("SELECT COUNT(*) FROM договоры WHERE Договор_id = %s", (new_id,))
        count = cur.fetchone()[0]
        if count > 0 and new_id != contract_id:
            raise ValueError(f"ID {new_id} уже существует.")
        
        # Формируем SQL-запрос для обновления только измененных полей
        update_fields = []
        params = []
        if new_id != contract_id:
            update_fields.append("Договор_id = %s")
            params.append(new_id)
        if patient_id is not None:
            update_fields.append("Пациент_id = %s")
            params.append(patient_id)
        if doctor_id is not None:
            update_fields.append("Врач_id = %s")
            params.append(doctor_id)
        if department:
            update_fields.append("Отделение = %s")
            params.append(department)
        if company_id is not None:
            update_fields.append("Компания_id = %s")
            params.append(company_id)
        
        if update_fields:
            params.append(contract_id)
            query = f"UPDATE договоры SET {', '.join(update_fields)} WHERE Договор_id = %s"
            cur.execute(query, params)
            conn.commit()
    finally:
        cur.close()
        conn.close()

def delete_contract(contract_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM договоры WHERE Договор_id = %s", (contract_id,))
        conn.commit()
    finally:
        cur.close()
        conn.close()

def search_contracts(search_query):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM договоры WHERE Договор_id = %s", (search_query,))
        contracts = cur.fetchall()
        return contracts
    finally:
        cur.close()
        conn.close()

def check_contract_id_exists(contract_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM договоры WHERE Договор_id = %s", (contract_id,))
        count = cur.fetchone()[0]
        return count > 0
    finally:
        cur.close()
        conn.close()

def search_contracts_by_id(contract_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM договоры WHERE Договор_id = %s", (contract_id,))
        contract = cur.fetchone()
        return contract
    finally:
        cur.close()
        conn.close()

# Функции для работы с таблицей Обследования
def add_examination(examination_id, patient_id, doctor_id, name, type, date, cost):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO Обследования (Обследование_id, Пациент_id, Врач_id, Название, Вид, Дата_проведения, Стоимость)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (examination_id, patient_id, doctor_id, name, type, date, cost)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

def get_examinations():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Обследования ORDER BY Обследование_id ASC")
        examinations = cur.fetchall()
        return examinations
    finally:
        cur.close()
        conn.close()

def update_examination(examination_id, new_id, patient_id, doctor_id, name, type, date, cost):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Проверяем, существует ли новый ID
        cur.execute("SELECT COUNT(*) FROM Обследования WHERE Обследование_id = %s", (new_id,))
        count = cur.fetchone()[0]
        if count > 0 and new_id != examination_id:
            raise ValueError(f"ID {new_id} уже существует.")
        
        # Формируем SQL-запрос для обновления только измененных полей
        update_fields = []
        params = []
        if new_id != examination_id:
            update_fields.append("Обследование_id = %s")
            params.append(new_id)
        if patient_id is not None:
            update_fields.append("Пациент_id = %s")
            params.append(patient_id)
        if doctor_id is not None:
            update_fields.append("Врач_id = %s")
            params.append(doctor_id)
        if name:
            update_fields.append("Название = %s")
            params.append(name)
        if type:
            update_fields.append("Вид = %s")
            params.append(type)
        if date:
            update_fields.append("Дата_проведения = %s")
            params.append(date)
        if cost is not None:
            update_fields.append("Стоимость = %s")
            params.append(cost)
        
        if update_fields:
            params.append(examination_id)
            query = f"UPDATE Обследования SET {', '.join(update_fields)} WHERE Обследование_id = %s"
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
            "DELETE FROM Обследования WHERE Обследование_id = %s",
            (examination_id,)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

def search_examinations(search_query):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT * FROM Обследования
            WHERE Обследование_id = %s OR Название ILIKE %s OR Вид ILIKE %s
            """,
            (search_query, f"%{search_query}%", f"%{search_query}%")
        )
        examinations = cur.fetchall()
        return examinations
    finally:
        cur.close()
        conn.close()

def check_examination_id_exists(examination_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM Обследования WHERE Обследование_id = %s", (examination_id,))
        count = cur.fetchone()[0]
        return count > 0
    finally:
        cur.close()
        conn.close()

def search_examinations_by_id(examination_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Обследования WHERE Обследование_id = %s", (examination_id,))
        examination = cur.fetchone()
        return examination
    finally:
        cur.close()
        conn.close()