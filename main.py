import flet as ft
from flet import ThemeMode, Icons
import pandas as pd
import psycopg2
from db import (
    add_patient, get_patients, update_patient, delete_patient, check_id_exists, search_patients_by_id,
    add_doctor, get_doctors, update_doctor, delete_doctor, check_doctor_id_exists, search_doctors_by_id,
    add_insurance_company, get_insurance_companies, update_insurance_company, delete_insurance_company, check_insurance_company_id_exists, search_insurance_companies_by_id,
    add_contract, get_contracts, update_contract, delete_contract, check_contract_id_exists, search_contracts_by_id,
    add_examination, get_examinations, update_examination, delete_examination, search_examinations, check_examination_id_exists, search_examinations_by_id,
    set_db_connection_params
)

def export_vse():
    examinations = get_examinations()
    df_5 = pd.DataFrame(examinations, columns=[
        "ID",
        "ID Пациента",
        "ID Врача",
        "Название",
        "Вид",
        "Дата проведения",
        "Стоимость"
    ])
    contracts = get_contracts()
    df_4 = pd.DataFrame(contracts, columns=[
        "ID",
        "ID Пациента",
        "ID Врача",
        "Отделение",
        "ID Компании"
    ])
    companies = get_insurance_companies()
    df_3 = pd.DataFrame(companies, columns=[
        "ID",
        "Название",
        "Номер лицензии",
        "ФИО руководителя",
        "Контактный телефон"
    ])
    doctors = get_doctors()
    df_2 = pd.DataFrame(doctors, columns=[
        "ID",
        "ФИО",
        "Категория",
        "Специальность",
        "Оклад",
        "Контактный телефон"
    ])
    patients = get_patients()
    df_1 = pd.DataFrame(patients, columns=[
        "ID",
        "ФИО",
        "Категория пациента",
        "Номер паспорта",
        "Номер страхового полиса",
        "Дата поступления",
        "Гражданство"
    ])
    with pd.ExcelWriter("C:\\games\\wtf\\FLET\\excelBAZA\\wtf.xlsx") as writer:
        df_1.to_excel(writer, sheet_name="Пациенты", index=False)
        df_2.to_excel(writer, sheet_name="Врачи", index=False)
        df_3.to_excel(writer, sheet_name="Страховые компании", index=False)
        df_4.to_excel(writer, sheet_name="Договоры", index=False)
        df_5.to_excel(writer, sheet_name="Обследования", index=False)

def toggle_theme(page):
    if page.theme_mode == ThemeMode.LIGHT:
        page.theme_mode = ThemeMode.DARK
    else:
        page.theme_mode = ThemeMode.LIGHT
    page.update()

# Пациенты
def create_patient_ui(page):
    # Создание полей ввода
    search_field = ft.TextField(label="Поиск по ID", width=400)

    # Создание таблицы для отображения пациентов
    # Внутри функции create_patient_ui(page)
    patients_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", width=50)),
            ft.DataColumn(ft.Text("ФИО")),
            ft.DataColumn(ft.Text("Категория пациента")),
            ft.DataColumn(ft.Text("Номер паспорта")),
            ft.DataColumn(ft.Text("Номер страхового полиса")),
            ft.DataColumn(ft.Text("Дата поступления")),
            ft.DataColumn(ft.Text("Гражданство")),
            ft.DataColumn(ft.Text("Редактирование/Удаление"))
        ],
        rows=[]
    )

    def load_patients(patients=None):
        if patients is None:
            patients = get_patients()
        patients_table.rows.clear()
        for patient in patients:
            edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e, pid=patient[0]: start_editing(pid))
            delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, pid=patient[0]: delete_patient_click(pid))
            patients_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(patient[0]))),
                        ft.DataCell(ft.Text(patient[1])),
                        ft.DataCell(ft.Text(patient[2])),
                        ft.DataCell(ft.Text(patient[3])),
                        ft.DataCell(ft.Text(patient[4])),
                        ft.DataCell(ft.Text(str(patient[5]))),
                        ft.DataCell(ft.Text(patient[6])),
                        ft.DataCell(ft.Row([edit_button, delete_button]))
                    ]
                )
            )
        page.update()

    def start_editing(patient_id):
        # Получаем данные пациента по ID
        patient = search_patients_by_id(patient_id)
        if not patient:
            return
    
        # Создаем текстовые поля с текущими значениями
        id_field = ft.TextField(value=str(patient[0]), width=200)
        fio_field = ft.TextField(value=patient[1], width=200)
        category_field = ft.TextField(value=patient[2], width=200)
        passport_number_field = ft.TextField(value=patient[3], width=200)
        insurance_policy_number_field = ft.TextField(value=patient[4], width=200)
        admission_date_field = ft.TextField(value=str(patient[5]), width=200)
        citizenship_field = ft.TextField(value=patient[6], width=200)
    
        # Кнопка сохранения изменений
        save_button = ft.ElevatedButton(text="Сохранить", on_click=lambda e: save_changes(patient[0], id_field.value, fio_field.value, category_field.value, passport_number_field.value, insurance_policy_number_field.value, admission_date_field.value, citizenship_field.value))
    
        # Удаляем старую строку из таблицы и добавляем новую с текстовыми полями
        patients_table.rows = [
            ft.DataRow(cells=[
                ft.DataCell(id_field),
                ft.DataCell(fio_field),
                ft.DataCell(category_field),
                ft.DataCell(passport_number_field),
                ft.DataCell(insurance_policy_number_field),
                ft.DataCell(admission_date_field),
                ft.DataCell(citizenship_field),
                ft.DataCell(ft.Row([save_button]))
            ])
        ] + [row for row in patients_table.rows if int(row.cells[0].content.value) != patient_id]
        page.update()

    def save_changes(old_patient_id, new_id, fio, category, passport_number, insurance_policy_number, admission_date, citizenship):
        try:
            update_patient(old_patient_id, int(new_id), fio, category, passport_number, insurance_policy_number, admission_date, citizenship)
            load_patients()  # Перезагрузка таблицы после обновления
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"))
            page.snack_bar.open = True
            page.update()

    def delete_patient_click(patient_id):
        try:
            delete_patient(patient_id)
            load_patients()
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"))
            page.snack_bar.open = True
            page.update()

    # Функция для добавления нового пациента
    def add_new_patient(e):
        # Создаем текстовые поля для ввода новых данных
        new_id_field = ft.TextField(label="ID", width=400)
        new_fio_field = ft.TextField(label="ФИО", width=200)
        new_category_field = ft.TextField(label="Категория пациента", width=200)
        new_passport_number_field = ft.TextField(label="Номер паспорта", width=200)
        new_insurance_policy_number_field = ft.TextField(label="Номер страхового полиса", width=200)
        new_admission_date_field = ft.TextField(label="Дата поступления (YYYY-MM-DD)", width=200)
        new_citizenship_field = ft.TextField(label="Гражданство", width=200)
    
        # Кнопка сохранения новых данных
        save_new_button = ft.ElevatedButton(text="Добавить", on_click=lambda e: save_new_patient(new_id_field.value, new_fio_field.value, new_category_field.value, new_passport_number_field.value, new_insurance_policy_number_field.value, new_admission_date_field.value, new_citizenship_field.value))
    
        # Добавляем новые текстовые поля и кнопку в таблицу
        patients_table.rows.insert(0, ft.DataRow(cells=[
            ft.DataCell(new_id_field),
            ft.DataCell(new_fio_field),
            ft.DataCell(new_category_field),
            ft.DataCell(new_passport_number_field),
            ft.DataCell(new_insurance_policy_number_field),
            ft.DataCell(new_admission_date_field),
            ft.DataCell(new_citizenship_field),
            ft.DataCell(ft.Row([save_new_button]))
        ]))
        page.update()

    def save_new_patient(id, fio, category, passport_number, insurance_policy_number, admission_date, citizenship):
        try:
            add_patient(int(id), fio, category, passport_number, insurance_policy_number, admission_date, citizenship)
            load_patients()  # Перезагрузка таблицы после добавления
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"))
            page.snack_bar.open = True
            page.update()
    
    def search_patients_click(e):
        query = search_field.value
        if query:
            try:
                patient_id = int(query)
            except ValueError:
                page.snack_bar = ft.SnackBar(content=ft.Text("Поиск должен быть числом!"))
                page.snack_bar.open = True
                page.update()
                return
            patient = search_patients_by_id(patient_id)
            if patient:
                load_patients([patient])
            else:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Пациент с ID {patient_id} не найден!"))
                page.snack_bar.open = True
                page.update()
                load_patients()
        else:
            load_patients()

    # Загрузка пациентов при запуске приложения
    load_patients()

    # Создание кнопок
    add_patient_button = ft.ElevatedButton(text="Добавить пациента", on_click=add_new_patient)
    search_button = ft.ElevatedButton(text="Поиск", on_click=search_patients_click)



    # Оборачиваем таблицу в ListView для скроллинга
    # Увеличиваем размер таблицы
    scrollable_table = ft.ListView(
        width=1920,  # Увеличиваем ширину
        height=1200,  # Увеличиваем высоту
        controls=[patients_table],
        auto_scroll=False
    )

    # Размещение элементов на странице
    patient_ui = ft.Column([
        ft.Row([search_field, search_button, add_patient_button]),
        scrollable_table
    ])

    return patient_ui

# Врачи 
def create_doctor_ui(page):
    # Создание полей ввода
    search_field = ft.TextField(label="Поиск по ID", width=400)
    
    # Создание таблицы для отображения врачей
    doctors_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", width=50)),
            ft.DataColumn(ft.Text("ФИО")),
            ft.DataColumn(ft.Text("Категория")),
            ft.DataColumn(ft.Text("Специальность")),
            ft.DataColumn(ft.Text("Оклад")),
            ft.DataColumn(ft.Text("Контактный телефон")),
            ft.DataColumn(ft.Text("Редактирование/Удаление"))
        ],
        rows=[]
    )
    
    def load_doctors(doctors=None):
        if doctors is None:
            doctors = get_doctors()
        doctors_table.rows.clear()
        for doctor in doctors:
            edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e, did=doctor[0]: start_editing_doctor(did))
            delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, did=doctor[0]: delete_doctor_click(did))
            doctors_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(doctor[0]))),
                        ft.DataCell(ft.Text(doctor[1])),
                        ft.DataCell(ft.Text(doctor[2])),
                        ft.DataCell(ft.Text(doctor[3])),
                        ft.DataCell(ft.Text(str(doctor[4]))),
                        ft.DataCell(ft.Text(doctor[5])),
                        ft.DataCell(ft.Row([edit_button, delete_button]))
                    ]
                )
            )
        page.update()
    
    def start_editing_doctor(doctor_id):
        # Получаем данные врача по ID
        doctor = search_doctors_by_id(doctor_id)
        if not doctor:
            return
    
        # Создаем текстовые поля с текущими значениями
        id_field = ft.TextField(value=str(doctor[0]), width=200)
        fio_field = ft.TextField(value=doctor[1], width=200)
        category_field = ft.TextField(value=doctor[2], width=200)
        specialty_field = ft.TextField(value=doctor[3], width=200)
        salary_field = ft.TextField(value=str(doctor[4]), width=200)
        contact_phone_field = ft.TextField(value=doctor[5], width=200)
    
        # Кнопка сохранения изменений
        save_button = ft.ElevatedButton(text="Сохранить", on_click=lambda e: save_changes_doctor(doctor[0], id_field.value, fio_field.value, category_field.value, specialty_field.value, salary_field.value, contact_phone_field.value))
    
        # Удаляем старую строку из таблицы и добавляем новую с текстовыми полями
        doctors_table.rows = [
            ft.DataRow(cells=[
                ft.DataCell(id_field),
                ft.DataCell(fio_field),
                ft.DataCell(category_field),
                ft.DataCell(specialty_field),
                ft.DataCell(salary_field),
                ft.DataCell(contact_phone_field),
                ft.DataCell(ft.Row([save_button]))
            ])
        ] + [row for row in doctors_table.rows if int(row.cells[0].content.value) != doctor_id]
        page.update()
    
    def save_changes_doctor(old_doctor_id, new_id, fio, category, specialty, salary, contact_phone):
        try:
            update_doctor(old_doctor_id, int(new_id), fio, category, specialty, float(salary), contact_phone)
            load_doctors()  # Перезагрузка таблицы после обновления
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"))
            page.snack_bar.open = True
            page.update()
    
    def delete_doctor_click(doctor_id):
        try:
            delete_doctor(doctor_id)
            load_doctors()
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"))
            page.snack_bar.open = True
            page.update()
    
    # Функция для добавления нового врача
    def add_new_doctor(e):
        # Создаем текстовые поля для ввода новых данных
        new_id_field = ft.TextField(label="ID", width=400)
        new_fio_field = ft.TextField(label="ФИО", width=200)
        new_category_field = ft.TextField(label="Категория", width=200)
        new_specialty_field = ft.TextField(label="Специальность", width=200)
        new_salary_field = ft.TextField(label="Оклад", width=200)
        new_contact_phone_field = ft.TextField(label="Контактный телефон", width=200)
    
        # Кнопка сохранения новых данных
        save_new_button = ft.ElevatedButton(text="Добавить", on_click=lambda e: save_new_doctor(new_id_field.value, new_fio_field.value, new_category_field.value, new_specialty_field.value, new_salary_field.value, new_contact_phone_field.value))
    
        # Добавляем новые текстовые поля и кнопку в таблицу
        doctors_table.rows.insert(0, ft.DataRow(cells=[
            ft.DataCell(new_id_field),
            ft.DataCell(new_fio_field),
            ft.DataCell(new_category_field),
            ft.DataCell(new_specialty_field),
            ft.DataCell(new_salary_field),
            ft.DataCell(new_contact_phone_field),
            ft.DataCell(ft.Row([save_new_button]))
        ]))
        page.update()
    
    def save_new_doctor(id, fio, category, specialty, salary, contact_phone):
        try:
            add_doctor(int(id), fio, category, specialty, float(salary), contact_phone)
            load_doctors()  # Перезагрузка таблицы после добавления
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"))
            page.snack_bar.open = True
            page.update()
    
    def search_doctors_click(e):
        query = search_field.value
        if query:
            try:
                doctor_id = int(query)
            except ValueError:
                page.snack_bar = ft.SnackBar(content=ft.Text("Поиск должен быть числом!"))
                page.snack_bar.open = True
                page.update()
                return
            doctor = search_doctors_by_id(doctor_id)
            if doctor:
                load_doctors([doctor])
            else:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Врач с ID {doctor_id} не найден!"))
                page.snack_bar.open = True
                page.update()
                load_doctors()
        else:
            load_doctors()

    # Загрузка врачей при запуске приложения
    load_doctors()
    # Создание кнопок
    add_doctor_button = ft.ElevatedButton(text="Добавить врача", on_click=add_new_doctor)
    search_button = ft.ElevatedButton(text="Поиск", on_click=search_doctors_click)

    # Оборачиваем таблицу в ListView для скроллинга
    # Увеличиваем размер таблицы
    scrollable_table = ft.ListView(
        width=1920,  # Увеличиваем ширину
        height=1200,  # Увеличиваем высоту
        controls=[doctors_table],
        auto_scroll=False
    )
    # Размещение элементов на странице
    doctor_ui = ft.Column([
        ft.Row([search_field, search_button, add_doctor_button]),
        scrollable_table
    ])
    return doctor_ui

# Страховые компании
def create_insurance_company_ui(page):
    # Создание полей ввода
    search_field = ft.TextField(label="Поиск по ID", width=400)
    
    # Создание таблицы для отображения страховых компаний
    insurance_companies_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", width=50)),
            ft.DataColumn(ft.Text("Название")),
            ft.DataColumn(ft.Text("Номер лицензии")),
            ft.DataColumn(ft.Text("ФИО руководителя")),
            ft.DataColumn(ft.Text("Контактный телефон")),
            ft.DataColumn(ft.Text("Редактирование/Удаление"))
        ],
        rows=[]
    )
    
    def load_insurance_companies(companies=None):
        if companies is None:
            companies = get_insurance_companies()
        insurance_companies_table.rows.clear()
        for company in companies:
            edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e, cid=company[0]: start_editing_company(cid))
            delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, cid=company[0]: delete_company_click(cid))
            insurance_companies_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(company[0]))),
                        ft.DataCell(ft.Text(company[1])),
                        ft.DataCell(ft.Text(company[2])),
                        ft.DataCell(ft.Text(company[3])),
                        ft.DataCell(ft.Text(company[4])),
                        ft.DataCell(ft.Row([edit_button, delete_button]))
                    ]
                )
            )
        page.update()
    
    def start_editing_company(company_id):
        # Получаем данные компании по ID
        company = search_insurance_companies_by_id(company_id)
        if not company:
            return
    
        # Создаем текстовые поля с текущими значениями
        id_field = ft.TextField(value=str(company[0]), width=200)
        name_field = ft.TextField(value=company[1], width=200)
        license_number_field = ft.TextField(value=company[2], width=200)
        director_fio_field = ft.TextField(value=company[3], width=200)
        contact_phone_field = ft.TextField(value=company[4], width=200)
    
        # Кнопка сохранения изменений
        save_button = ft.ElevatedButton(text="Сохранить", on_click=lambda e: save_changes_company(company[0], id_field.value, name_field.value, license_number_field.value, director_fio_field.value, contact_phone_field.value))
    
        # Удаляем старую строку из таблицы и добавляем новую с текстовыми полями
        insurance_companies_table.rows = [
            ft.DataRow(cells=[
                ft.DataCell(id_field),
                ft.DataCell(name_field),
                ft.DataCell(license_number_field),
                ft.DataCell(director_fio_field),
                ft.DataCell(contact_phone_field),
                ft.DataCell(ft.Row([save_button]))
            ])
        ] + [row for row in insurance_companies_table.rows if int(row.cells[0].content.value) != company_id]
        page.update()
    
    def save_changes_company(old_company_id, new_id, name, license_number, director_fio, contact_phone):
        try:
            update_insurance_company(old_company_id, int(new_id), name, license_number, director_fio, contact_phone)
            load_insurance_companies()  # Перезагрузка таблицы после обновления
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"))
            page.snack_bar.open = True
            page.update()
    
    def delete_company_click(company_id):
        try:
            delete_insurance_company(company_id)
            load_insurance_companies()
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"))
            page.snack_bar.open = True
            page.update()
    
    # Функция для добавления новой компании
    def add_new_company(e):
        # Создаем текстовые поля для ввода новых данных
        new_id_field = ft.TextField(label="ID", width=400)
        new_name_field = ft.TextField(label="Название", width=200)
        new_license_number_field = ft.TextField(label="Номер лицензии", width=200)
        new_director_fio_field = ft.TextField(label="ФИО руководителя", width=200)
        new_contact_phone_field = ft.TextField(label="Контактный телефон", width=200)
    
        # Кнопка сохранения новых данных
        save_new_button = ft.ElevatedButton(text="Добавить", on_click=lambda e: save_new_company(new_id_field.value, new_name_field.value, new_license_number_field.value, new_director_fio_field.value, new_contact_phone_field.value))
    
        # Добавляем новые текстовые поля и кнопку в таблицу
        insurance_companies_table.rows.insert(0, ft.DataRow(cells=[
            ft.DataCell(new_id_field),
            ft.DataCell(new_name_field),
            ft.DataCell(new_license_number_field),
            ft.DataCell(new_director_fio_field),
            ft.DataCell(new_contact_phone_field),
            ft.DataCell(ft.Row([save_new_button]))
        ]))
        page.update()
    
    def save_new_company(id, name, license_number, director_fio, contact_phone):
        try:
            add_insurance_company(int(id), name, license_number, director_fio, contact_phone)
            load_insurance_companies()  # Перезагрузка таблицы после добавления
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"))
            page.snack_bar.open = True
            page.update()
    
    def search_insurance_companies_click(e):
        query = search_field.value
        if query:
            try:
                company_id = int(query)
            except ValueError:
                page.snack_bar = ft.SnackBar(content=ft.Text("Поиск должен быть числом!"))
                page.snack_bar.open = True
                page.update()
                return
            company = search_insurance_companies_by_id(company_id)
            if company:
                load_insurance_companies([company])
            else:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Компания с ID {company_id} не найдена!"))
                page.snack_bar.open = True
                page.update()
                load_insurance_companies()
        else:
            load_insurance_companies()

    # Загрузка страховых компаний при запуске приложения
    load_insurance_companies()
    # Создание кнопок
    add_company_button = ft.ElevatedButton(text="Добавить компанию", on_click=add_new_company)
    search_button = ft.ElevatedButton(text="Поиск", on_click=search_insurance_companies_click)

    # Оборачиваем таблицу в ListView для скроллинга
    # Увеличиваем размер таблицы
    scrollable_table = ft.ListView(
        width=1920,  # Увеличиваем ширину
        height=1200,  # Увеличиваем высоту
        controls=[insurance_companies_table],
        auto_scroll=False
    )
    # Размещение элементов на странице
    insurance_company_ui = ft.Column([
        ft.Row([search_field, search_button, add_company_button]),
        scrollable_table
    ])
    return insurance_company_ui

# Договоры
def create_contract_ui(page):
    # Создание полей ввода
    search_field = ft.TextField(label="Поиск по ID", width=400)
    
    # Создание таблицы для отображения договоров
    contracts_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", width=50)),
            ft.DataColumn(ft.Text("ID Пациента")),
            ft.DataColumn(ft.Text("ID Врача")),
            ft.DataColumn(ft.Text("Отделение")),
            ft.DataColumn(ft.Text("ID Компании")),
            ft.DataColumn(ft.Text("Редактирование/Удаление"))
        ],
        rows=[]
    )
    
    def load_contracts(contracts=None):
        if contracts is None:
            contracts = get_contracts()
        contracts_table.rows.clear()
        for contract in contracts:
            edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e, cid=contract[0]: start_editing_contract(cid))
            delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, cid=contract[0]: delete_contract_click(cid))
            contracts_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(contract[0]))),
                        ft.DataCell(ft.Text(str(contract[1]))),
                        ft.DataCell(ft.Text(str(contract[2]))),
                        ft.DataCell(ft.Text(contract[3])),
                        ft.DataCell(ft.Text(str(contract[4]))),
                        ft.DataCell(ft.Row([edit_button, delete_button]))
                    ]
                )
            )
        page.update()
    
    def start_editing_contract(contract_id):
        # Получаем данные договора по ID
        contract = search_contracts_by_id(contract_id)
        if not contract:
            return
    
        # Создаем текстовые поля с текущими значениями
        id_field = ft.TextField(value=str(contract[0]), width=200)
        patient_id_field = ft.TextField(value=str(contract[1]), width=200)
        doctor_id_field = ft.TextField(value=str(contract[2]), width=200)
        department_field = ft.TextField(value=contract[3], width=200)
        company_id_field = ft.TextField(value=str(contract[4]), width=200)
    
        # Кнопка сохранения изменений
        save_button = ft.ElevatedButton(text="Сохранить", on_click=lambda e: save_changes_contract(contract[0], id_field.value, patient_id_field.value, doctor_id_field.value, department_field.value, company_id_field.value))
    
        # Удаляем старую строку из таблицы и добавляем новую с текстовыми полями
        contracts_table.rows = [
            ft.DataRow(cells=[
                ft.DataCell(id_field),
                ft.DataCell(patient_id_field),
                ft.DataCell(doctor_id_field),
                ft.DataCell(department_field),
                ft.DataCell(company_id_field),
                ft.DataCell(ft.Row([save_button]))
            ])
        ] + [row for row in contracts_table.rows if int(row.cells[0].content.value) != contract_id]
        page.update()
    
    def save_changes_contract(old_contract_id, new_id, patient_id, doctor_id, department, company_id):
        try:
            update_contract(old_contract_id, int(new_id), int(patient_id), int(doctor_id), department, int(company_id) if company_id else None)
            load_contracts()  # Перезагрузка таблицы после обновления
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"))
            page.snack_bar.open = True
            page.update()
    
    def delete_contract_click(contract_id):
        try:
            delete_contract(contract_id)
            load_contracts()
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"))
            page.snack_bar.open = True
            page.update()
    
    # Функция для добавления нового договора
    def add_new_contract(e):
        # Создаем текстовые поля для ввода новых данных
        new_id_field = ft.TextField(label="ID", width=400)
        new_patient_id_field = ft.TextField(label="ID Пациента", width=200)
        new_doctor_id_field = ft.TextField(label="ID Врача", width=200)
        new_department_field = ft.TextField(label="Отделение", width=200)
        new_company_id_field = ft.TextField(label="ID Компании", width=200)
    
        # Кнопка сохранения новых данных
        save_new_button = ft.ElevatedButton(text="Добавить", on_click=lambda e: save_new_contract(new_id_field.value, new_patient_id_field.value, new_doctor_id_field.value, new_department_field.value, new_company_id_field.value))
    
        # Добавляем новые текстовые поля и кнопку в таблицу
        contracts_table.rows.insert(0, ft.DataRow(cells=[
            ft.DataCell(new_id_field),
            ft.DataCell(new_patient_id_field),
            ft.DataCell(new_doctor_id_field),
            ft.DataCell(new_department_field),
            ft.DataCell(new_company_id_field),
            ft.DataCell(ft.Row([save_new_button]))
        ]))
        page.update()
    
    def save_new_contract(id, patient_id, doctor_id, department, company_id):
        try:
            add_contract(int(id), int(patient_id), int(doctor_id), department, int(company_id) if company_id else None)
            load_contracts()  # Перезагрузка таблицы после добавления
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"))
            page.snack_bar.open = True
            page.update()
    
    def search_contracts_click(e):
        query = search_field.value
        if query:
            try:
                contract_id = int(query)
            except ValueError:
                page.snack_bar = ft.SnackBar(content=ft.Text("Поиск должен быть числом!"))
                page.snack_bar.open = True
                page.update()
                return
            contract = search_contracts_by_id(contract_id)
            if contract:
                load_contracts([contract])
            else:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Договор с ID {contract_id} не найден!"))
                page.snack_bar.open = True
                page.update()
                load_contracts()
        else:
            load_contracts()

    # Загрузка договоров при запуске приложения
    load_contracts()
    # Создание кнопок
    add_contract_button = ft.ElevatedButton(text="Добавить договор", on_click=add_new_contract)
    search_button = ft.ElevatedButton(text="Поиск", on_click=search_contracts_click)

    # Оборачиваем таблицу в ListView для скроллинга
    # Увеличиваем размер таблицы
    scrollable_table = ft.ListView(
        width=1920,  # Увеличиваем ширину
        height=1200,  # Увеличиваем высоту
        controls=[contracts_table],
        auto_scroll=False
    )
    # Размещение элементов на странице
    contract_ui = ft.Column([
        ft.Row([search_field, search_button, add_contract_button]),
        scrollable_table
    ])
    return contract_ui

# Обследования
def create_examination_ui(page):
    # Создание полей ввода
    search_field = ft.TextField(label="Поиск по ID", width=400)
    
    # Создание таблицы для отображения обследований
    examinations_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", width=50)),
            ft.DataColumn(ft.Text("ID Пациента")),
            ft.DataColumn(ft.Text("ID Врача")),
            ft.DataColumn(ft.Text("Название")),
            ft.DataColumn(ft.Text("Вид")),
            ft.DataColumn(ft.Text("Дата проведения")),
            ft.DataColumn(ft.Text("Стоимость")),
            ft.DataColumn(ft.Text("Редактирование/Удаление"))
        ],
        rows=[]
    )
    
    def load_examinations(examinations=None):
        if examinations is None:
            examinations = get_examinations()
        examinations_table.rows.clear()
        for examination in examinations:
            edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e, eid=examination[0]: start_editing_examination(eid))
            delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, eid=examination[0]: delete_examination_click(eid))
            examinations_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(examination[0]))),
                        ft.DataCell(ft.Text(str(examination[1]))),
                        ft.DataCell(ft.Text(str(examination[2]))),
                        ft.DataCell(ft.Text(examination[3])),
                        ft.DataCell(ft.Text(examination[4])),
                        ft.DataCell(ft.Text(str(examination[5]))),
                        ft.DataCell(ft.Text(str(examination[6]))),
                        ft.DataCell(ft.Row([edit_button, delete_button]))
                    ]
                )
            )
        page.update()
    
    def start_editing_examination(examination_id):
        # Получаем данные обследования по ID
        examination = search_examinations_by_id(examination_id)
        if not examination:
            return
    
        # Создаем текстовые поля с текущими значениями
        id_field = ft.TextField(value=str(examination[0]), width=200)
        patient_id_field = ft.TextField(value=str(examination[1]), width=200)
        doctor_id_field = ft.TextField(value=str(examination[2]), width=200)
        name_field = ft.TextField(value=examination[3], width=200)
        type_field = ft.TextField(value=examination[4], width=200)
        date_field = ft.TextField(value=str(examination[5]), width=200)
        cost_field = ft.TextField(value=str(examination[6]) if examination[6] else "", width=200)
    
        # Кнопка сохранения изменений
        save_button = ft.ElevatedButton(text="Сохранить", on_click=lambda e: save_changes_examination(examination[0], id_field.value, patient_id_field.value, doctor_id_field.value, name_field.value, type_field.value, date_field.value, cost_field.value))
    
        # Удаляем старую строку из таблицы и добавляем новую с текстовыми полями
        examinations_table.rows = [
            ft.DataRow(cells=[
                ft.DataCell(id_field),
                ft.DataCell(patient_id_field),
                ft.DataCell(doctor_id_field),
                ft.DataCell(name_field),
                ft.DataCell(type_field),
                ft.DataCell(date_field),
                ft.DataCell(cost_field),
                ft.DataCell(ft.Row([save_button]))
            ])
        ] + [row for row in examinations_table.rows if int(row.cells[0].content.value) != examination_id]
        page.update()
    
    def save_changes_examination(old_examination_id, new_id, patient_id, doctor_id, name, type, date, cost):
        try:
            update_examination(old_examination_id, int(new_id), int(patient_id), int(doctor_id), name, type, date, float(cost) if cost else None)
            load_examinations()  # Перезагрузка таблицы после обновления
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"))
            page.snack_bar.open = True
            page.update()
    
    def delete_examination_click(examination_id):
        try:
            delete_examination(examination_id)
            load_examinations()
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"))
            page.snack_bar.open = True
            page.update()
    
    # Функция для добавления нового обследования
    def add_new_examination(e):
        # Создаем текстовые поля для ввода новых данных
        new_id_field = ft.TextField(label="ID", width=400)
        new_patient_id_field = ft.TextField(label="ID Пациента", width=200)
        new_doctor_id_field = ft.TextField(label="ID Врача", width=200)
        new_name_field = ft.TextField(label="Название", width=200)
        new_type_field = ft.TextField(label="Вид", width=200)
        new_date_field = ft.TextField(label="Дата проведения (YYYY-MM-DD)", width=200)
        new_cost_field = ft.TextField(label="Стоимость", width=200)
    
        # Кнопка сохранения новых данных
        save_new_button = ft.ElevatedButton(text="Добавить", on_click=lambda e: save_new_examination(new_id_field.value, new_patient_id_field.value, new_doctor_id_field.value, new_name_field.value, new_type_field.value, new_date_field.value, new_cost_field.value))
    
        # Добавляем новые текстовые поля и кнопку в таблицу
        examinations_table.rows.insert(0, ft.DataRow(cells=[
            ft.DataCell(new_id_field),
            ft.DataCell(new_patient_id_field),
            ft.DataCell(new_doctor_id_field),
            ft.DataCell(new_name_field),
            ft.DataCell(new_type_field),
            ft.DataCell(new_date_field),
            ft.DataCell(new_cost_field),
            ft.DataCell(ft.Row([save_new_button]))
        ]))
        page.update()
    
    def save_new_examination(id, patient_id, doctor_id, name, type, date, cost):
        try:
            add_examination(int(id), int(patient_id), int(doctor_id), name, type, date, float(cost) if cost else None)
            load_examinations()  # Перезагрузка таблицы после добавления
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"))
            page.snack_bar.open = True
            page.update()
    
    def search_examinations_click(e):
        query = search_field.value
        if query:
            try:
                examination_id = int(query)
            except ValueError:
                page.snack_bar = ft.SnackBar(content=ft.Text("Поиск должен быть числом!"))
                page.snack_bar.open = True
                page.update()
                return
            examination = search_examinations_by_id(examination_id)
            if examination:
                load_examinations([examination])
            else:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Обследование с ID {examination_id} не найдено!"))
                page.snack_bar.open = True
                page.update()
                load_examinations()
        else:
            load_examinations()

    # Загрузка обследований при запуске приложения
    load_examinations()
    # Создание кнопок
    add_examination_button = ft.ElevatedButton(text="Добавить обследование", on_click=add_new_examination)
    search_button = ft.ElevatedButton(text="Поиск", on_click=search_examinations_click)

    # Оборачиваем таблицу в ListView для скроллинга
    # Увеличиваем размер таблицы
    scrollable_table = ft.ListView(
        width=1920,  # Увеличиваем ширину
        height=1200,  # Увеличиваем высоту
        controls=[examinations_table],
        auto_scroll=False
    )
    # Размещение элементов на странице
    examination_ui = ft.Column([
        ft.Row([search_field, search_button, add_examination_button]),
        scrollable_table
    ])
    return examination_ui

# Функция для проверки подключения к базе данных
def test_db_connection(host, dbname, user, password):
    try:
        conn = psycopg2.connect(
            host=host,
            database=dbname,
            user=user,
            password=password
        )
        conn.close()
        return True
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {str(e)}")
        return False

# Форма авторизации
def create_auth_ui(page):
    # Поля ввода для данных подключения
    host_field = ft.TextField(label="Host", width=400)
    dbname_field = ft.TextField(label="Database Name", width=400)
    user_field = ft.TextField(label="User", width=400)
    password_field = ft.TextField(label="Password", width=400, password=True)

    def on_auth_click(e):
        host = host_field.value
        dbname = dbname_field.value
        user = user_field.value
        password = password_field.value

        if not host or not dbname or not user or not password:
            page.snack_bar = ft.SnackBar(content=ft.Text("Заполните все поля!"))
            page.snack_bar.open = True
            page.update()
            return

        if test_db_connection(host, dbname, user, password):
            page.snack_bar = ft.SnackBar(content=ft.Text("Подключение успешно!"))
            page.snack_bar.open = True
            page.update()

            # Установите параметры подключения
            set_db_connection_params(host, dbname, user, password)

            # Переход к основному интерфейсу
            page.clean()  # Очистите текущую страницу
            main(page)  # Запустите основное приложение
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("Ошибка подключения к базе данных!"))
            page.snack_bar.open = True
            page.update()

    # Кнопка авторизации
    auth_button = ft.ElevatedButton(text="Авторизоваться", on_click=on_auth_click)

    # Размещение элементов на странице
    auth_ui = ft.Column([
        ft.Row([host_field]),
        ft.Row([dbname_field]),
        ft.Row([user_field]),
        ft.Row([password_field]),
        ft.Row([auth_button])
    ])

    return auth_ui



def create_settings_ui(page):
    export_all_button = ft.ElevatedButton(text="Экспорт всей базы в Excel", on_click=lambda _: export_vse())
    theme_button = ft.ElevatedButton(text="Переключить тему", on_click=lambda _: toggle_theme(page))
    return ft.Column([export_all_button, theme_button])

def main(page: ft.Page):
    page.title = "Медицинское приложение"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.theme_mode = ThemeMode.DARK
    
    # Создание навигационного меню
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="Пациенты", content=create_patient_ui(page)),
            ft.Tab(text="Врачи", content=create_doctor_ui(page)),
            ft.Tab(text="Страховые компании", content=create_insurance_company_ui(page)),
            ft.Tab(text="Договоры", content=create_contract_ui(page)),
            ft.Tab(text="Обследования", content=create_examination_ui(page)),
            ft.Tab(text="Настройки", content=create_settings_ui(page))
        ]
    )
    
    # Размещение навигационного меню на странице
    page.add(tabs)

# Запуск приложения с экраном авторизации
def run_app(page: ft.Page):
    page.title = "Авторизация"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.theme_mode = ThemeMode.DARK

    # Отображение формы авторизации
    page.add(create_auth_ui(page))

ft.app(target=main, assets_dir="excelBAZA")