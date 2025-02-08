import flet as ft
from flet import ThemeMode, Icons
from flet import *
import os
import tempfile
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from db import (
    add_patient, get_patients, update_patient, delete_patient, check_id_exists, search_patients_by_id,
    add_doctor, get_doctors, update_doctor, delete_doctor, check_doctor_id_exists, search_doctors_by_id,
    add_insurance_company, get_insurance_companies, update_insurance_company, delete_insurance_company, check_insurance_company_id_exists, search_insurance_companies_by_id,
    add_contract, get_contracts, update_contract, delete_contract, check_contract_id_exists, search_contracts_by_id,
    add_examination, get_examinations, update_examination, delete_examination, search_examinations, check_examination_id_exists, search_examinations_by_id,
    set_db_credentials, get_connection
)

def export_vse():
    # Получаем данные из базы данных
    examinations = get_examinations()
    contracts = get_contracts()
    companies = get_insurance_companies()
    doctors = get_doctors()
    patients = get_patients()

    # Создаем DataFrame для каждой таблицы
    df_1 = pd.DataFrame(patients, columns=[
        "ID", "ФИО", "Категория пациента", "Номер паспорта", "Номер страхового полиса", "Дата поступления", "Гражданство"
    ])
    df_2 = pd.DataFrame(doctors, columns=[
        "ID", "ФИО", "Категория", "Специальность", "Оклад", "Контактный телефон"
    ])
    df_3 = pd.DataFrame(companies, columns=[
        "ID", "Название", "Номер лицензии", "ФИО руководителя", "Контактный телефон"
    ])
    df_4 = pd.DataFrame(contracts, columns=[
        "ID", "ID Пациента", "ID Врача", "Отделение", "ID Компании"
    ])
    df_5 = pd.DataFrame(examinations, columns=[
        "ID", "ID Пациента", "ID Врача", "Название", "Вид", "Дата проведения", "Стоимость"
    ])

    # Создаем временный файл
    temp_file = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
    temp_file_path = temp_file.name
    temp_file.close()

    # Создаем Excel-файл с использованием openpyxl
    wb = Workbook()
    wb.remove(wb.active)  # Удаляем пустой лист по умолчанию

    # Добавляем данные в каждый лист
    for sheet_name, df in [
        ("Пациенты", df_1),
        ("Врачи", df_2),
        ("Страховые компании", df_3),
        ("Договоры", df_4),
        ("Обследования", df_5)
    ]:
        ws = wb.create_sheet(title=sheet_name)
        for row in dataframe_to_rows(df, index=False, header=True):
            ws.append(row)

    # Сохраняем файл во временную директорию
    wb.save(temp_file_path)

    # Открываем файл в Excel
    try:
        if os.name == 'nt':  # Windows
            os.startfile(temp_file_path)
        elif os.name == 'posix':  # Unix или Linux
            subprocess.run(['open', temp_file_path], check=True)
    except Exception as e:
        print(f"Ошибка при открытии файла: {e}")

def toggle_theme(page):
    if page.theme_mode == ThemeMode.LIGHT:
        page.theme_mode = ThemeMode.DARK
    else:
        page.theme_mode = ThemeMode.LIGHT
    page.update()

# Пациенты
def create_patient_ui(page):
    # Стилизованное поле поиска
    search_field = ft.TextField(
        label="Поиск пациента...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=15,
        filled=True,
        bgcolor=ft.Colors.WHITE10,
        focused_bgcolor=ft.Colors.WHITE24,
        width=400,
        height=50,
        text_size=14,
        cursor_color="#2A9D8F",
    )
    # Анимированная кнопка добавления
    add_button = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINED, color="#2A9D8F"),
            ft.Text("Добавить пациента", color="#2A9D8F")
        ]),
        padding=15,
        border_radius=15,
        bgcolor=ft.Colors.WHITE24,
        on_click=lambda e: add_new_patient(e),
        animate=ft.Animation(200, "easeOut"),
    )
    # Сетка для карточек пациентов
    patients_grid = ft.GridView(
        expand=True,
        runs_count=3,
        max_extent=350,
        child_aspect_ratio=0.75,  # высота карточек
        spacing=20,
        run_spacing=20,
        padding=20
    )

    # Карточка пациента с информацией
    def create_patient_card(patient):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PERSON_OUTLINE, color="#2A9D8F"),
                    ft.Text(patient[1], size=16, weight="bold", expand=True)
                ]),
                ft.Divider(height=10, color="transparent"),
                ft.Row([
                    ft.Column([
                        ft.Text("ID:", color=ft.Colors.GREY_400),
                        ft.Text(str(patient[0]), color="#2A9D8F")
                    ], expand=True),
                    ft.VerticalDivider(width=20),
                    ft.Column([
                        ft.Text("Категория:", color=ft.Colors.GREY_400),
                        ft.Text(patient[2], color="#2A9D8F")
                    ], expand=True)
                ]),
                ft.Divider(height=10, color="transparent"),
                ft.Row([
                    ft.Column([
                        ft.Text("Паспорт:", color=ft.Colors.GREY_400),
                        ft.Text(patient[3], color="#2A9D8F")
                    ], expand=True),
                    ft.VerticalDivider(width=20),
                    ft.Column([
                        ft.Text("Полис:", color=ft.Colors.GREY_400),
                        ft.Text(patient[4], color="#2A9D8F")
                    ], expand=True)
                ]),
                ft.Divider(height=10, color="transparent"),
                ft.Row([
                    ft.Column([
                        ft.Text("Дата поступления:", color=ft.Colors.GREY_400),
                        ft.Text(str(patient[5]), color="#2A9D8F")
                    ], expand=True),
                    ft.VerticalDivider(width=20),
                    ft.Column([
                        ft.Text("Гражданство:", color=ft.Colors.GREY_400),
                        ft.Text(patient[6], color="#2A9D8F")
                    ], expand=True)
                ]),
                ft.Divider(height=20),
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        icon_color="#E9C46A",
                        tooltip="Редактировать",
                        bgcolor=ft.Colors.WHITE24,
                        on_click=lambda e, pid=patient[0]: start_editing(pid)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color="#E76F51",
                        tooltip="Удалить",
                        bgcolor=ft.Colors.WHITE24,
                        on_click=lambda e, pid=patient[0]: delete_patient_click(pid)
                    )
                ], alignment=ft.MainAxisAlignment.END)
            ]),
            padding=20,
            border_radius=15,
            bgcolor=ft.Colors.WHITE24,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.Colors.BLACK54),
        )

    # Загрузка данных
    def load_patients(patients=None):
        patients_grid.controls.clear()
        patients = get_patients() if patients is None else patients
        for patient in patients:
            patients_grid.controls.append(create_patient_card(patient))
        page.update()

    # Функция редактирования
    def start_editing(patient_id):
        patient = search_patients_by_id(patient_id)
        if not patient:
            return

        edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Редактирование пациента", color="#2A9D8F"),
            content=ft.Column([
                ft.TextField(label="ID", value=str(patient[0]), read_only=True),
                ft.TextField(label="ФИО", value=patient[1]),
                ft.TextField(label="Категория", value=patient[2]),
                ft.TextField(label="Номер паспорта", value=patient[3]),
                ft.TextField(label="Страховой полис", value=patient[4]),
                ft.TextField(label="Дата поступления", value=str(patient[5])),
                ft.TextField(label="Гражданство", value=patient[6])
            ], spacing=10),
            actions=[
                ft.TextButton(
                    "Сохранить",
                    style=ft.ButtonStyle(color="#2A9D8F"),
                    on_click=lambda e: save_changes(
                        patient[0],
                        e.control.page.dialog.content.controls[1].value,
                        e.control.page.dialog.content.controls[2].value,
                        e.control.page.dialog.content.controls[3].value,
                        e.control.page.dialog.content.controls[4].value,
                        e.control.page.dialog.content.controls[5].value,
                        e.control.page.dialog.content.controls[6].value
                    )
                ),
                ft.TextButton("Отмена", on_click=lambda e: page.close_dialog())
            ],
        )
        page.dialog = edit_dialog
        edit_dialog.open = True
        page.update()

    def save_changes(old_id, fio, category, passport, policy, date, citizenship):
        try:
            update_patient(old_id, old_id, fio, category, passport, policy, date, citizenship)
            load_patients()
            page.close_dialog()
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"), bgcolor="#E76F51")
            page.snack_bar.open = True
            page.update()

    # Функция удаления
    def delete_patient_click(patient_id):
        def confirm_delete(e):  # параметр e
            try:
                delete_patient(patient_id)
                load_patients()
                page.close_dialog()
            except Exception as e:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"), bgcolor="#E76F51")
                page.snack_bar.open = True
                page.update()
    
        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Подтверждение удаления", color="#E76F51"),
            content=ft.Text(f"Вы уверены, что хотите удалить пациента #{patient_id}?"),
            actions=[
                ft.TextButton("Удалить", style=ft.ButtonStyle(color="#E76F51"), on_click=confirm_delete),
                ft.TextButton("Отмена", on_click=lambda e: page.close_dialog())
            ]
        )
        page.dialog = confirm_dialog
        confirm_dialog.open = True
        page.update()

    # Для автоматической генерации ID
    def get_next_patient_id():
        patients = get_patients()
        if patients:
            return max(p[0] for p in patients) + 1
        return 1
    
    # Функция добавления нового пациента
    def add_new_patient(e):
        new_id = get_next_patient_id()
        new_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Новый пациент", color="#2A9D8F"),
            content=ft.Column([
                ft.Text(f"ID: {new_id}", size=16, weight="bold"), # Автоматический ID
                ft.TextField(label="ФИО"),
                ft.TextField(label="Категория"),
                ft.TextField(label="Номер паспорта"),
                ft.TextField(label="Страховой полис"),
                ft.TextField(label="Дата поступления (ГГГГ-ММ-ДД)"),
                ft.TextField(label="Гражданство")
            ], spacing=10),
            actions=[
                ft.TextButton(
                    "Сохранить",
                    style=ft.ButtonStyle(color="#2A9D8F"),
                    on_click=lambda e: save_new_patient(
                        new_id,
                        e.control.page.dialog.content.controls[1].value,
                        e.control.page.dialog.content.controls[2].value,
                        e.control.page.dialog.content.controls[3].value,
                        e.control.page.dialog.content.controls[4].value,
                        e.control.page.dialog.content.controls[5].value,
                        e.control.page.dialog.content.controls[6].value
                    )
                ),
                ft.TextButton("Отмена", on_click=lambda e: page.close_dialog())
            ]
        )
        page.dialog = new_dialog
        new_dialog.open = True
        page.update()

    def save_new_patient(id, fio, category, passport, policy, date, citizenship):
        try:
            add_patient(int(id), fio, category, passport, policy, date, citizenship)
            load_patients()
            page.close_dialog()
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"), bgcolor="#E76F51")
            page.snack_bar.open = True
            page.update()

    # Поиск пациентов
    def search_patients_click(e):
        query = search_field.value.lower()
        if query:
            results = []
            for patient in get_patients():
                # Проверяем совпадения по всем полям
                if (query in str(patient[0]).lower() or
                    query in patient[1].lower() or
                    query in patient[2].lower() or
                    query in patient[3].lower() or
                    query in patient[4].lower() or
                    query in str(patient[5]).lower() or
                    query in patient[6].lower()):
                    results.append(patient)
            load_patients(results)  # Загружаем только найденные результаты
        else:
            load_patients()  # Если запрос пустой, показываем всех пациентов
    
    search_field.on_submit = search_patients_click
    # Первоначальная загрузка данных
    load_patients()

    return ft.Column(
        spacing=20,
        controls=[
            ft.Row([search_field, add_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(height=1, color=ft.Colors.WHITE24),
            patients_grid
        ]
    )

# Врачи 
def create_doctor_ui(page):
    # Стилизованное поле поиска
    search_field = ft.TextField(
        label="Поиск врача...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=15,
        filled=True,
        bgcolor=ft.Colors.WHITE10,
        focused_bgcolor=ft.Colors.WHITE24,
        width=400,
        height=50,
        text_size=14,
        cursor_color="#2A9D8F",
    )
    # Анимированная кнопка добавления
    add_button = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINED, color="#2A9D8F"),
            ft.Text("Добавить врача", color="#2A9D8F")
        ]),
        padding=15,
        border_radius=15,
        bgcolor=ft.Colors.WHITE24,
        on_click=lambda e: add_new_doctor(e),
        animate=ft.Animation(200, "easeOut"),
    )
    # Сетка для карточек врачей
    doctors_grid = ft.GridView(
        expand=True,
        runs_count=3,
        max_extent=350,
        child_aspect_ratio=0.75,  # высота карточек
        spacing=20,
        run_spacing=20,
        padding=20
    )

    # Карточка врача с расширенной информацией
    def create_doctor_card(doctor):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.MEDICAL_SERVICES_OUTLINED, color="#2A9D8F"),
                    ft.Text(doctor[1], size=16, weight="bold", expand=True)
                ]),
                ft.Divider(height=10, color="transparent"),
                ft.Row([
                    ft.Column([
                        ft.Text("ID:", color=ft.Colors.GREY_400),
                        ft.Text(str(doctor[0]), color="#2A9D8F")
                    ], expand=True),
                    ft.VerticalDivider(width=20),
                    ft.Column([
                        ft.Text("Категория:", color=ft.Colors.GREY_400),
                        ft.Text(doctor[2], color="#2A9D8F")
                    ], expand=True)
                ]),
                ft.Divider(height=10, color="transparent"),
                ft.Row([
                    ft.Column([
                        ft.Text("Специальность:", color=ft.Colors.GREY_400),
                        ft.Text(doctor[3], color="#2A9D8F")
                    ], expand=True),
                    ft.VerticalDivider(width=20),
                    ft.Column([
                        ft.Text("Оклад:", color=ft.Colors.GREY_400),
                        ft.Text(str(doctor[4]), color="#2A9D8F")
                    ], expand=True)
                ]),
                ft.Divider(height=10, color="transparent"),
                ft.Row([
                    ft.Column([
                        ft.Text("Контактный телефон:", color=ft.Colors.GREY_400),
                        ft.Text(doctor[5], color="#2A9D8F")
                    ], expand=True)
                ]),
                ft.Divider(height=20),
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        icon_color="#E9C46A",
                        tooltip="Редактировать",
                        bgcolor=ft.Colors.WHITE24,
                        on_click=lambda e, did=doctor[0]: start_editing(did)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color="#E76F51",
                        tooltip="Удалить",
                        bgcolor=ft.Colors.WHITE24,
                        on_click=lambda e, did=doctor[0]: delete_doctor_click(did)
                    )
                ], alignment=ft.MainAxisAlignment.END)
            ]),
            padding=20,
            border_radius=15,
            bgcolor=ft.Colors.WHITE24,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.Colors.BLACK54),
        )

    # Загрузка данных
    def load_doctors(doctors=None):
        doctors_grid.controls.clear()
        doctors = get_doctors() if doctors is None else doctors
        for doctor in doctors:
            doctors_grid.controls.append(create_doctor_card(doctor))
        page.update()

    # Функция редактирования
    def start_editing(doctor_id):
        doctor = search_doctors_by_id(doctor_id)
        if not doctor:
            return
        edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Редактирование врача", color="#2A9D8F"),
            content=ft.Column([
                ft.TextField(label="ID", value=str(doctor[0]), read_only=True),
                ft.TextField(label="ФИО", value=doctor[1]),
                ft.TextField(label="Категория", value=doctor[2]),
                ft.TextField(label="Специальность", value=doctor[3]),
                ft.TextField(label="Оклад", value=str(doctor[4])),
                ft.TextField(label="Контактный телефон", value=doctor[5])
            ], spacing=10),
            actions=[
                ft.TextButton(
                    "Сохранить",
                    style=ft.ButtonStyle(color="#2A9D8F"),
                    on_click=lambda e: save_changes(
                        doctor[0],
                        e.control.page.dialog.content.controls[1].value,
                        e.control.page.dialog.content.controls[2].value,
                        e.control.page.dialog.content.controls[3].value,
                        e.control.page.dialog.content.controls[4].value,
                        e.control.page.dialog.content.controls[5].value
                    )
                ),
                ft.TextButton("Отмена", on_click=lambda e: page.close_dialog())
            ],
        )
        page.dialog = edit_dialog
        edit_dialog.open = True
        page.update()

    def save_changes(old_id, fio, category, specialty, salary, contact_phone):
        try:
            update_doctor(old_id, old_id, fio, category, specialty, float(salary), contact_phone)
            load_doctors()
            page.close_dialog()
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"), bgcolor="#E76F51")
            page.snack_bar.open = True
            page.update()

    # Функция удаления
    def delete_doctor_click(doctor_id):
        def confirm_delete(e):
            try:
                delete_doctor(doctor_id)
                load_doctors()
                page.close_dialog()
            except Exception as e:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"), bgcolor="#E76F51")
                page.snack_bar.open = True
                page.update()

        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Подтверждение удаления", color="#E76F51"),
            content=ft.Text(f"Вы уверены, что хотите удалить врача #{doctor_id}?"),
            actions=[
                ft.TextButton("Удалить", style=ft.ButtonStyle(color="#E76F51"), on_click=confirm_delete),
                ft.TextButton("Отмена", on_click=lambda e: page.close_dialog())
            ]
        )
        page.dialog = confirm_dialog
        confirm_dialog.open = True
        page.update()

    # Автоматическая генерация ID
    def get_next_doctor_id():
        doctors = get_doctors()
        if doctors:
            return max(d[0] for d in doctors) + 1
        return 1

    # Функция добавления нового врача
    def add_new_doctor(e):
        new_id = get_next_doctor_id()
        new_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Новый врач", color="#2A9D8F"),
            content=ft.Column([
                ft.Text(f"ID: {new_id}", size=16, weight="bold"),
                ft.TextField(label="ФИО"),
                ft.TextField(label="Категория"),
                ft.TextField(label="Специальность"),
                ft.TextField(label="Оклад"),
                ft.TextField(label="Контактный телефон")
            ], spacing=10),
            actions=[
                ft.TextButton(
                    "Сохранить",
                    style=ft.ButtonStyle(color="#2A9D8F"),
                    on_click=lambda e: save_new_doctor(
                        new_id,
                        e.control.page.dialog.content.controls[1].value,
                        e.control.page.dialog.content.controls[2].value,
                        e.control.page.dialog.content.controls[3].value,
                        e.control.page.dialog.content.controls[4].value,
                        e.control.page.dialog.content.controls[5].value
                    )
                ),
                ft.TextButton("Отмена", on_click=lambda e: page.close_dialog())
            ]
        )
        page.dialog = new_dialog
        new_dialog.open = True
        page.update()

    def save_new_doctor(id, fio, category, specialty, salary, contact_phone):
        try:
            add_doctor(int(id), fio, category, specialty, float(salary), contact_phone)
            load_doctors()
            page.close_dialog()
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"), bgcolor="#E76F51")
            page.snack_bar.open = True
            page.update()

    # Поиск врачей
    def search_doctors_click(e):
        query = search_field.value.lower()
        if query:
            results = []
            for doctor in get_doctors():
                if (query in str(doctor[0]).lower() or
                    query in doctor[1].lower() or
                    query in doctor[2].lower() or
                    query in doctor[3].lower() or
                    query in str(doctor[4]).lower() or
                    query in doctor[5].lower()):
                    results.append(doctor)
            load_doctors(results)
        else:
            load_doctors()

    search_field.on_submit = search_doctors_click

    # Первоначальная загрузка данных
    load_doctors()

    return ft.Column(
        spacing=20,
        controls=[
            ft.Row([search_field, add_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(height=1, color=ft.Colors.WHITE24),
            doctors_grid
        ]
    )

# Страховые компании
def create_insurance_company_ui(page):
    # Поле поиска
    search_field = ft.TextField(
        label="Поиск страховой компании...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=15,
        filled=True,
        bgcolor=ft.Colors.WHITE10,
        focused_bgcolor=ft.Colors.WHITE24,
        width=400,
        height=50,
        text_size=14,
        cursor_color="#2A9D8F",
    )
    # Кнопка добавления
    add_button = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINED, color="#2A9D8F"),
            ft.Text("Добавить компанию", color="#2A9D8F")
        ]),
        padding=15,
        border_radius=15,
        bgcolor=ft.Colors.WHITE24,
        on_click=lambda e: add_new_company(e),
        animate=ft.Animation(200, "easeOut"),
    )
    # Сетка для карточек компаний
    companies_grid = ft.GridView(
        expand=True,
        runs_count=3,
        max_extent=350,
        child_aspect_ratio=0.75,  # высота карточек
        spacing=20,
        run_spacing=20,
        padding=20
    )

    # Карточка страховой компании
    def create_company_card(company):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.BUSINESS_OUTLINED, color="#2A9D8F"),
                    ft.Text(company[1], size=16, weight="bold", expand=True)
                ]),
                ft.Divider(height=10, color="transparent"),
                ft.Row([
                    ft.Column([
                        ft.Text("ID:", color=ft.Colors.GREY_400),
                        ft.Text(str(company[0]), color="#2A9D8F")
                    ], expand=True),
                    ft.VerticalDivider(width=20),
                    ft.Column([
                        ft.Text("Номер лицензии:", color=ft.Colors.GREY_400),
                        ft.Text(company[2], color="#2A9D8F")
                    ], expand=True)
                ]),
                ft.Divider(height=10, color="transparent"),
                ft.Row([
                    ft.Column([
                        ft.Text("ФИО руководителя:", color=ft.Colors.GREY_400),
                        ft.Text(company[3], color="#2A9D8F")
                    ], expand=True),
                    ft.VerticalDivider(width=20),
                    ft.Column([
                        ft.Text("Контактный телефон:", color=ft.Colors.GREY_400),
                        ft.Text(company[4], color="#2A9D8F")
                    ], expand=True)
                ]),
                ft.Divider(height=20),
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        icon_color="#E9C46A",
                        tooltip="Редактировать",
                        bgcolor=ft.Colors.WHITE24,
                        on_click=lambda e, cid=company[0]: start_editing(cid)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color="#E76F51",
                        tooltip="Удалить",
                        bgcolor=ft.Colors.WHITE24,
                        on_click=lambda e, cid=company[0]: delete_company_click(cid)
                    )
                ], alignment=ft.MainAxisAlignment.END)
            ]),
            padding=20,
            border_radius=15,
            bgcolor=ft.Colors.WHITE24,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.Colors.BLACK54),
        )

    # Загрузка данных
    def load_companies(companies=None):
        companies_grid.controls.clear()
        companies = get_insurance_companies() if companies is None else companies
        for company in companies:
            companies_grid.controls.append(create_company_card(company))
        page.update()

    # Функция редактирования
    def start_editing(company_id):
        company = search_insurance_companies_by_id(company_id)
        if not company:
            return
        edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Редактирование компании", color="#2A9D8F"),
            content=ft.Column([
                ft.TextField(label="ID", value=str(company[0]), read_only=True),
                ft.TextField(label="Название", value=company[1]),
                ft.TextField(label="Номер лицензии", value=company[2]),
                ft.TextField(label="ФИО руководителя", value=company[3]),
                ft.TextField(label="Контактный телефон", value=company[4])
            ], spacing=10),
            actions=[
                ft.TextButton(
                    "Сохранить",
                    style=ft.ButtonStyle(color="#2A9D8F"),
                    on_click=lambda e: save_changes(
                        company[0],
                        e.control.page.dialog.content.controls[1].value,
                        e.control.page.dialog.content.controls[2].value,
                        e.control.page.dialog.content.controls[3].value,
                        e.control.page.dialog.content.controls[4].value
                    )
                ),
                ft.TextButton("Отмена", on_click=lambda e: page.close_dialog())
            ],
        )
        page.dialog = edit_dialog
        edit_dialog.open = True
        page.update()

    def save_changes(old_id, name, license_number, director_fio, contact_phone):
        try:
            update_insurance_company(old_id, old_id, name, license_number, director_fio, contact_phone)
            load_companies()
            page.close_dialog()
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"), bgcolor="#E76F51")
            page.snack_bar.open = True
            page.update()

    # Функция удаления
    def delete_company_click(company_id):
        def confirm_delete(e):
            try:
                delete_insurance_company(company_id)
                load_companies()
                page.close_dialog()
            except Exception as e:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"), bgcolor="#E76F51")
                page.snack_bar.open = True
                page.update()

        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Подтверждение удаления", color="#E76F51"),
            content=ft.Text(f"Вы уверены, что хотите удалить компанию #{company_id}?"),
            actions=[
                ft.TextButton("Удалить", style=ft.ButtonStyle(color="#E76F51"), on_click=confirm_delete),
                ft.TextButton("Отмена", on_click=lambda e: page.close_dialog())
            ]
        )
        page.dialog = confirm_dialog
        confirm_dialog.open = True
        page.update()

    # Автоматическая генерация ID
    def get_next_company_id():
        companies = get_insurance_companies()
        if companies:
            return max(c[0] for c in companies) + 1
        return 1

    # Функция добавления новой компании
    def add_new_company(e):
        new_id = get_next_company_id()
        new_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Новая страховая компания", color="#2A9D8F"),
            content=ft.Column([
                ft.Text(f"ID: {new_id}", size=16, weight="bold"),
                ft.TextField(label="Название"),
                ft.TextField(label="Номер лицензии"),
                ft.TextField(label="ФИО руководителя"),
                ft.TextField(label="Контактный телефон")
            ], spacing=10),
            actions=[
                ft.TextButton(
                    "Сохранить",
                    style=ft.ButtonStyle(color="#2A9D8F"),
                    on_click=lambda e: save_new_company(
                        new_id,
                        e.control.page.dialog.content.controls[1].value,
                        e.control.page.dialog.content.controls[2].value,
                        e.control.page.dialog.content.controls[3].value,
                        e.control.page.dialog.content.controls[4].value
                    )
                ),
                ft.TextButton("Отмена", on_click=lambda e: page.close_dialog())
            ]
        )
        page.dialog = new_dialog
        new_dialog.open = True
        page.update()

    def save_new_company(id, name, license_number, director_fio, contact_phone):
        try:
            add_insurance_company(int(id), name, license_number, director_fio, contact_phone)
            load_companies()
            page.close_dialog()
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"), bgcolor="#E76F51")
            page.snack_bar.open = True
            page.update()

    # Поиск компаний
    def search_companies_click(e):
        query = search_field.value.lower()
        if query:
            results = []
            for company in get_insurance_companies():
                if (query in str(company[0]).lower() or
                    query in company[1].lower() or
                    query in company[2].lower() or
                    query in company[3].lower() or
                    query in company[4].lower()):
                    results.append(company)
            load_companies(results)
        else:
            load_companies()

    search_field.on_submit = search_companies_click

    # Первоначальная загрузка данных
    load_companies()

    return ft.Column(
        spacing=20,
        controls=[
            ft.Row([search_field, add_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(height=1, color=ft.Colors.WHITE24),
            companies_grid
        ]
    )

# Договоры
def create_contract_ui(page):
    # Поле поиска
    search_field = ft.TextField(
        label="Поиск договора...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=15,
        filled=True,
        bgcolor=ft.Colors.WHITE10,
        focused_bgcolor=ft.Colors.WHITE24,
        width=400,
        height=50,
        text_size=14,
        cursor_color="#2A9D8F",
    )
    # Кнопка добавления
    add_button = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINED, color="#2A9D8F"),
            ft.Text("Добавить договор", color="#2A9D8F")
        ]),
        padding=15,
        border_radius=15,
        bgcolor=ft.Colors.WHITE24,
        on_click=lambda e: add_new_contract(e),
        animate=ft.Animation(200, "easeOut"),
    )
    # Сетка для карточек договоров
    contracts_grid = ft.GridView(
        expand=True,
        runs_count=3,
        max_extent=350,
        child_aspect_ratio=0.75,  # высота карточек
        spacing=20,
        run_spacing=20,
        padding=20
    )

    # Карточка договора
    def create_contract_card(contract):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.ASSIGNMENT_OUTLINED, color="#2A9D8F"),
                    ft.Text(f"Договор #{contract[0]}", size=16, weight="bold", expand=True)
                ]),
                ft.Divider(height=10, color="transparent"),
                ft.Row([
                    ft.Column([
                        ft.Text("ID Пациента:", color=ft.Colors.GREY_400),
                        ft.Text(str(contract[1]), color="#2A9D8F")
                    ], expand=True),
                    ft.VerticalDivider(width=20),
                    ft.Column([
                        ft.Text("ID Врача:", color=ft.Colors.GREY_400),
                        ft.Text(str(contract[2]), color="#2A9D8F")
                    ], expand=True)
                ]),
                ft.Divider(height=10, color="transparent"),
                ft.Row([
                    ft.Column([
                        ft.Text("Отделение:", color=ft.Colors.GREY_400),
                        ft.Text(contract[3], color="#2A9D8F")
                    ], expand=True),
                    ft.VerticalDivider(width=20),
                    ft.Column([
                        ft.Text("ID Компании:", color=ft.Colors.GREY_400),
                        ft.Text(str(contract[4]) if contract[4] else "Нет", color="#2A9D8F")
                    ], expand=True)
                ]),
                ft.Divider(height=20),
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        icon_color="#E9C46A",
                        tooltip="Редактировать",
                        bgcolor=ft.Colors.WHITE24,
                        on_click=lambda e, cid=contract[0]: start_editing(cid)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color="#E76F51",
                        tooltip="Удалить",
                        bgcolor=ft.Colors.WHITE24,
                        on_click=lambda e, cid=contract[0]: delete_contract_click(cid)
                    )
                ], alignment=ft.MainAxisAlignment.END)
            ]),
            padding=20,
            border_radius=15,
            bgcolor=ft.Colors.WHITE24,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.Colors.BLACK54),
        )

    # Загрузка данных
    def load_contracts(contracts=None):
        contracts_grid.controls.clear()
        contracts = get_contracts() if contracts is None else contracts
        for contract in contracts:
            contracts_grid.controls.append(create_contract_card(contract))
        page.update()

    # Функция редактирования
    def start_editing(contract_id):
        contract = search_contracts_by_id(contract_id)
        if not contract:
            return
        edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Редактирование договора", color="#2A9D8F"),
            content=ft.Column([
                ft.TextField(label="ID", value=str(contract[0]), read_only=True),
                ft.TextField(label="ID Пациента", value=str(contract[1])),
                ft.TextField(label="ID Врача", value=str(contract[2])),
                ft.TextField(label="Отделение", value=contract[3]),
                ft.TextField(label="ID Компании", value=str(contract[4]) if contract[4] else ""),
            ], spacing=10),
            actions=[
                ft.TextButton(
                    "Сохранить",
                    style=ft.ButtonStyle(color="#2A9D8F"),
                    on_click=lambda e: save_changes(
                        contract[0],
                        e.control.page.dialog.content.controls[1].value,
                        e.control.page.dialog.content.controls[2].value,
                        e.control.page.dialog.content.controls[3].value,
                        e.control.page.dialog.content.controls[4].value
                    )
                ),
                ft.TextButton("Отмена", on_click=lambda e: page.close_dialog())
            ],
        )
        page.dialog = edit_dialog
        edit_dialog.open = True
        page.update()

    def save_changes(old_id, patient_id, doctor_id, department, company_id):
        try:
            update_contract(
                old_id,
                int(patient_id),
                int(doctor_id),
                department,
                int(company_id) if company_id else None
            )
            load_contracts()
            page.close_dialog()
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"), bgcolor="#E76F51")
            page.snack_bar.open = True
            page.update()

    # Функция удаления
    def delete_contract_click(contract_id):
        def confirm_delete(e):
            try:
                delete_contract(contract_id)
                load_contracts()
                page.close_dialog()
            except Exception as e:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"), bgcolor="#E76F51")
                page.snack_bar.open = True
                page.update()

        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Подтверждение удаления", color="#E76F51"),
            content=ft.Text(f"Вы уверены, что хотите удалить договор #{contract_id}?"),
            actions=[
                ft.TextButton("Удалить", style=ft.ButtonStyle(color="#E76F51"), on_click=confirm_delete),
                ft.TextButton("Отмена", on_click=lambda e: page.close_dialog())
            ]
        )
        page.dialog = confirm_dialog
        confirm_dialog.open = True
        page.update()

    # Автоматическая генерация ID
    def get_next_contract_id():
        contracts = get_contracts()
        if contracts:
            return max(c[0] for c in contracts) + 1
        return 1

    # Функция добавления нового договора
    def add_new_contract(e):
        new_id = get_next_contract_id()
        new_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Новый договор", color="#2A9D8F"),
            content=ft.Column([
                ft.Text(f"ID: {new_id}", size=16, weight="bold"),
                ft.TextField(label="ID Пациента"),
                ft.TextField(label="ID Врача"),
                ft.TextField(label="Отделение"),
                ft.TextField(label="ID Компании (опционально)")
            ], spacing=10),
            actions=[
                ft.TextButton(
                    "Сохранить",
                    style=ft.ButtonStyle(color="#2A9D8F"),
                    on_click=lambda e: save_new_contract(
                        new_id,
                        e.control.page.dialog.content.controls[1].value,
                        e.control.page.dialog.content.controls[2].value,
                        e.control.page.dialog.content.controls[3].value,
                        e.control.page.dialog.content.controls[4].value
                    )
                ),
                ft.TextButton("Отмена", on_click=lambda e: page.close_dialog())
            ]
        )
        page.dialog = new_dialog
        new_dialog.open = True
        page.update()

    def save_new_contract(id, patient_id, doctor_id, department, company_id):
        try:
            add_contract(
                int(id),
                int(patient_id),
                int(doctor_id),
                department,
                int(company_id) if company_id else None
            )
            load_contracts()
            page.close_dialog()
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"), bgcolor="#E76F51")
            page.snack_bar.open = True
            page.update()

    # Поиск договоров
    def search_contracts_click(e):
        query = search_field.value.lower()
        if query:
            results = []
            for contract in get_contracts():
                if (query in str(contract[0]).lower() or
                    query in str(contract[1]).lower() or
                    query in str(contract[2]).lower() or
                    query in contract[3].lower() or
                    query in str(contract[4]).lower()):
                    results.append(contract)
            load_contracts(results)
        else:
            load_contracts()

    search_field.on_submit = search_contracts_click

    # Первоначальная загрузка данных
    load_contracts()

    return ft.Column(
        spacing=20,
        controls=[
            ft.Row([search_field, add_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(height=1, color=ft.Colors.WHITE24),
            contracts_grid
        ]
    )

# Обследования
def create_examination_ui(page):
    # Поле поиска
    search_field = ft.TextField(
        label="Поиск обследования...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=15,
        filled=True,
        bgcolor=ft.Colors.WHITE10,
        focused_bgcolor=ft.Colors.WHITE24,
        width=400,
        height=50,
        text_size=14,
        cursor_color="#2A9D8F",
    )
    # Кнопка добавления
    add_button = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINED, color="#2A9D8F"),
            ft.Text("Добавить обследование", color="#2A9D8F")
        ]),
        padding=15,
        border_radius=15,
        bgcolor=ft.Colors.WHITE24,
        on_click=lambda e: add_new_examination(e),
        animate=ft.Animation(200, "easeOut"),
    )
    # Сетка для карточек обследований
    examinations_grid = ft.GridView(
        expand=True,
        runs_count=3,
        max_extent=350,
        child_aspect_ratio=0.75,  # высота карточек
        spacing=20,
        run_spacing=20,
        padding=20
    )

    # Карточка обследования
    def create_examination_card(examination):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.HEALTH_AND_SAFETY_OUTLINED, color="#2A9D8F"),
                    ft.Text(f"Обследование #{examination[0]}", size=16, weight="bold", expand=True)
                ]),
                ft.Divider(height=10, color="transparent"),
                ft.Row([
                    ft.Column([
                        ft.Text("ID Пациента:", color=ft.Colors.GREY_400),
                        ft.Text(str(examination[1]), color="#2A9D8F")
                    ], expand=True),
                    ft.VerticalDivider(width=20),
                    ft.Column([
                        ft.Text("ID Врача:", color=ft.Colors.GREY_400),
                        ft.Text(str(examination[2]), color="#2A9D8F")
                    ], expand=True)
                ]),
                ft.Divider(height=10, color="transparent"),
                ft.Row([
                    ft.Column([
                        ft.Text("Название:", color=ft.Colors.GREY_400),
                        ft.Text(examination[3], color="#2A9D8F")
                    ], expand=True),
                    ft.VerticalDivider(width=20),
                    ft.Column([
                        ft.Text("Вид:", color=ft.Colors.GREY_400),
                        ft.Text(examination[4], color="#2A9D8F")
                    ], expand=True)
                ]),
                ft.Divider(height=10, color="transparent"),
                ft.Row([
                    ft.Column([
                        ft.Text("Дата проведения:", color=ft.Colors.GREY_400),
                        ft.Text(str(examination[5]), color="#2A9D8F")
                    ], expand=True),
                    ft.VerticalDivider(width=20),
                    ft.Column([
                        ft.Text("Стоимость:", color=ft.Colors.GREY_400),
                        ft.Text(str(examination[6]) if examination[6] else "Не указана", color="#2A9D8F")
                    ], expand=True)
                ]),
                ft.Divider(height=20),
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        icon_color="#E9C46A",
                        tooltip="Редактировать",
                        bgcolor=ft.Colors.WHITE24,
                        on_click=lambda e, eid=examination[0]: start_editing(eid)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color="#E76F51",
                        tooltip="Удалить",
                        bgcolor=ft.Colors.WHITE24,
                        on_click=lambda e, eid=examination[0]: delete_examination_click(eid)
                    )
                ], alignment=ft.MainAxisAlignment.END)
            ]),
            padding=20,
            border_radius=15,
            bgcolor=ft.Colors.WHITE24,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.Colors.BLACK54),
        )

    # Загрузка данных
    def load_examinations(examinations=None):
        examinations_grid.controls.clear()
        examinations = get_examinations() if examinations is None else examinations
        for examination in examinations:
            examinations_grid.controls.append(create_examination_card(examination))
        page.update()

    # Функция редактирования
    def start_editing(examination_id):
        examination = search_examinations_by_id(examination_id)
        if not examination:
            return
        edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Редактирование обследования", color="#2A9D8F"),
            content=ft.Column([
                ft.TextField(label="ID", value=str(examination[0]), read_only=True),
                ft.TextField(label="ID Пациента", value=str(examination[1])),
                ft.TextField(label="ID Врача", value=str(examination[2])),
                ft.TextField(label="Название", value=examination[3]),
                ft.TextField(label="Вид", value=examination[4]),
                ft.TextField(label="Дата проведения (ГГГГ-ММ-ДД)", value=str(examination[5])),
                ft.TextField(label="Стоимость", value=str(examination[6]) if examination[6] else "")
            ], spacing=10),
            actions=[
                ft.TextButton(
                    "Сохранить",
                    style=ft.ButtonStyle(color="#2A9D8F"),
                    on_click=lambda e: save_changes(
                        examination[0],
                        e.control.page.dialog.content.controls[1].value,
                        e.control.page.dialog.content.controls[2].value,
                        e.control.page.dialog.content.controls[3].value,
                        e.control.page.dialog.content.controls[4].value,
                        e.control.page.dialog.content.controls[5].value,
                        e.control.page.dialog.content.controls[6].value
                    )
                ),
                ft.TextButton("Отмена", on_click=lambda e: page.close_dialog())
            ],
        )
        page.dialog = edit_dialog
        edit_dialog.open = True
        page.update()

    def save_changes(old_id, patient_id, doctor_id, name, type, date, cost):
        try:
            update_examination(
                old_id,
                int(patient_id),
                int(doctor_id),
                name,
                type,
                date,
                float(cost) if cost else None
            )
            load_examinations()
            page.close_dialog()
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"), bgcolor="#E76F51")
            page.snack_bar.open = True
            page.update()

    # Функция удаления
    def delete_examination_click(examination_id):
        def confirm_delete(e):
            try:
                delete_examination(examination_id)
                load_examinations()
                page.close_dialog()
            except Exception as e:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"), bgcolor="#E76F51")
                page.snack_bar.open = True
                page.update()

        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Подтверждение удаления", color="#E76F51"),
            content=ft.Text(f"Вы уверены, что хотите удалить обследование #{examination_id}?"),
            actions=[
                ft.TextButton("Удалить", style=ft.ButtonStyle(color="#E76F51"), on_click=confirm_delete),
                ft.TextButton("Отмена", on_click=lambda e: page.close_dialog())
            ]
        )
        page.dialog = confirm_dialog
        confirm_dialog.open = True
        page.update()

    # Автоматическая генерация ID
    def get_next_examination_id():
        examinations = get_examinations()
        if examinations:
            return max(e[0] for e in examinations) + 1
        return 1

    # Функция добавления нового обследования
    def add_new_examination(e):
        new_id = get_next_examination_id()
        new_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Новое обследование", color="#2A9D8F"),
            content=ft.Column([
                ft.Text(f"ID: {new_id}", size=16, weight="bold"),
                ft.TextField(label="ID Пациента"),
                ft.TextField(label="ID Врача"),
                ft.TextField(label="Название"),
                ft.TextField(label="Вид"),
                ft.TextField(label="Дата проведения (ГГГГ-ММ-ДД)"),
                ft.TextField(label="Стоимость")
            ], spacing=10),
            actions=[
                ft.TextButton(
                    "Сохранить",
                    style=ft.ButtonStyle(color="#2A9D8F"),
                    on_click=lambda e: save_new_examination(
                        new_id,
                        e.control.page.dialog.content.controls[1].value,
                        e.control.page.dialog.content.controls[2].value,
                        e.control.page.dialog.content.controls[3].value,
                        e.control.page.dialog.content.controls[4].value,
                        e.control.page.dialog.content.controls[5].value,
                        e.control.page.dialog.content.controls[6].value
                    )
                ),
                ft.TextButton("Отмена", on_click=lambda e: page.close_dialog())
            ]
        )
        page.dialog = new_dialog
        new_dialog.open = True
        page.update()

    def save_new_examination(id, patient_id, doctor_id, name, type, date, cost):
        try:
            add_examination(
                int(id),
                int(patient_id),
                int(doctor_id),
                name,
                type,
                date,
                float(cost) if cost else None
            )
            load_examinations()
            page.close_dialog()
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"), bgcolor="#E76F51")
            page.snack_bar.open = True
            page.update()

    # Поиск обследований
    def search_examinations_click(e):
        query = search_field.value.lower()
        if query:
            results = []
            for examination in get_examinations():
                if (query in str(examination[0]).lower() or
                    query in str(examination[1]).lower() or
                    query in str(examination[2]).lower() or
                    query in examination[3].lower() or
                    query in examination[4].lower() or
                    query in str(examination[5]).lower() or
                    query in str(examination[6]).lower()):
                    results.append(examination)
            load_examinations(results)
        else:
            load_examinations()

    search_field.on_submit = search_examinations_click

    # Первоначальная загрузка данных
    load_examinations()

    return ft.Column(
        spacing=20,
        controls=[
            ft.Row([search_field, add_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(height=1, color=ft.Colors.WHITE24),
            examinations_grid
        ]
    )


#отчеты ?
def create_reports_ui(page):
    # Выбор типа отчета
    report_type_dropdown = ft.Dropdown(
        label="Выберите тип отчета",
        options=[
            ft.dropdown.Option("1", "Отчет о посещениях пациентов за период"),
            ft.dropdown.Option("2", "Отчет о количестве пациентов по категориям"),
            ft.dropdown.Option("3", "Отчет о врачах и количестве обследований"),
            ft.dropdown.Option("4", "Отчет о страховых компаниях и пациентах"),
            ft.dropdown.Option("5", "Отчет о пациентах и их последних обследованиях"),
        ],
        width=400,
        value="1"
    )

    # Поля для ввода данных
    start_date_field = ft.TextField(label="Дата начала", visible=False)
    end_date_field = ft.TextField(label="Дата окончания", visible=False)
    category_field = ft.TextField(label="Категория", visible=False)

    # Функция для показа/скрытия полей ввода
    def update_input_fields(e):
        if report_type_dropdown.value == "1":
            start_date_field.visible = True
            end_date_field.visible = True
            category_field.visible = False
        elif report_type_dropdown.value == "2":
            start_date_field.visible = False
            end_date_field.visible = False
            category_field.visible = True
        else:
            start_date_field.visible = False
            end_date_field.visible = False
            category_field.visible = False
        page.update()

    report_type_dropdown.on_change = update_input_fields

    # Кнопка генерации отчета
    generate_button = ft.ElevatedButton(
        text="Сформировать отчет",
        on_click=lambda e: generate_report(
            report_type_dropdown.value,
            start_date_field.value,
            end_date_field.value,
            category_field.value,
            page
        )
    )

    return ft.Column(
        spacing=20,
        controls=[
            report_type_dropdown,
            start_date_field,
            end_date_field,
            category_field,
            generate_button
        ]
    )

def display_report(data, columns, page):
    report_table = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(col)) for col in columns],
        rows=[
            ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in row])
            for row in data
        ]
    )
    page.dialog = ft.AlertDialog(
        title=ft.Text("Результаты отчета"),
        content=report_table,
        actions=[ft.TextButton("Закрыть", on_click=lambda e: page.close_dialog())]
    )
    page.dialog.open = True
    page.update()

def generate_report(report_type, start_date, end_date, category, page):
    if report_type == "1":  # Отчет о посещениях пациентов за период
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                SELECT Patient_id, Full_Name, Admission_Date 
                FROM Patients 
                WHERE Admission_Date BETWEEN %s AND %s
                """,
                (start_date, end_date)
            )
            results = cur.fetchall()
            display_report(results, ["ID Пациента", "ФИО", "Дата поступления"], page)
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"), bgcolor="#E76F51")
            page.snack_bar.open = True
            page.update()

    elif report_type == "2":  # Отчет о количестве пациентов по категориям
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                SELECT Patient_Category, COUNT(*) 
                FROM Patients 
                WHERE Patient_Category = %s
                GROUP BY Patient_Category
                """,
                (category,)
            )
            results = cur.fetchall()
            display_report(results, ["Категория", "Количество пациентов"], page)
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"), bgcolor="#E76F51")
            page.snack_bar.open = True
            page.update()

    elif report_type == "3":  # Отчет о врачах и количестве обследований
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                SELECT d.Doctor_id, d.Full_Name, COUNT(e.Examination_id) AS Examination_Count
                FROM Doctors d
                LEFT JOIN Examinations e ON d.Doctor_id = e.Doctor_id
                GROUP BY d.Doctor_id, d.Full_Name
                ORDER BY Examination_Count DESC
                """
            )
            results = cur.fetchall()
            display_report(results, ["ID Врача", "ФИО Врача", "Количество обследований"], page)
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"), bgcolor="#E76F51")
            page.snack_bar.open = True
            page.update()

    elif report_type == "4":  # Отчет о страховых компаниях и пациентах
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                SELECT ic.Company_id, ic.Name, COUNT(p.Patient_id) AS Patient_Count
                FROM Insurance_Companies ic
                LEFT JOIN Patients p ON ic.Company_id::TEXT = p.Insurance_Policy_Number
                GROUP BY ic.Company_id, ic.Name
                ORDER BY Patient_Count DESC
                """
            )
            results = cur.fetchall()
            display_report(results, ["ID Компании", "Название компании", "Количество пациентов"], page)
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"), bgcolor="#E76F51")
            page.snack_bar.open = True
            page.update()

    elif report_type == "5":  # Отчет о пациентах и их последних обследованиях
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                SELECT p.Patient_id, p.Full_Name, e.Name AS Last_Examination, e.Examination_Date
                FROM Patients p
                LEFT JOIN (
                    SELECT Patient_id, Name, Examination_Date,
                           ROW_NUMBER() OVER (PARTITION BY Patient_id ORDER BY Examination_Date DESC) AS rn
                    FROM Examinations
                ) e ON p.Patient_id = e.Patient_id AND e.rn = 1
                ORDER BY p.Patient_id
                """
            )
            results = cur.fetchall()
            display_report(results, ["ID Пациента", "ФИО Пациента", "Последнее обследование", "Дата обследования"], page)
        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(e)}"), bgcolor="#E76F51")
            page.snack_bar.open = True
            page.update()

# функция для создания главного интерфейса
def main_ui(page):
    # Навигационная панель
    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.PEOPLE_OUTLINED,
                selected_icon=ft.Icons.PEOPLE,
                label="Пациенты"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.MEDICAL_SERVICES_OUTLINED,
                selected_icon=ft.Icons.MEDICAL_SERVICES,
                label="Врачи"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.BUSINESS_OUTLINED,
                selected_icon=ft.Icons.BUSINESS,
                label="Компании"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.ASSIGNMENT_OUTLINED,
                selected_icon=ft.Icons.ASSIGNMENT,
                label="Договоры"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.HEALTH_AND_SAFETY_OUTLINED,
                selected_icon=ft.Icons.HEALTH_AND_SAFETY,
                label="Обследования"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.REPORT_OUTLINED,
                selected_icon=ft.Icons.REPORT,
                label="Отчеты"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
                label="Настройки"
            )
        ],
        bgcolor=ft.Colors.with_opacity(0.95, "#264653"),
        indicator_color="#2A9D8F",
    )
    
    # Контейнер для контента
    content_container = ft.Container(expand=True)
    
    # Обработчик навигации
    def navigate(e):
        index = e.control.selected_index
        content_container.content = [
            create_patient_ui(page),
            create_doctor_ui(page),
            create_insurance_company_ui(page),
            create_contract_ui(page),
            create_examination_ui(page),
            create_reports_ui(page),
            create_settings_ui(page)
        ][index]
        page.update()
    
    nav_rail.on_change = navigate
    
    # Основной макет
    page.add(
        ft.Row(
            [
                nav_rail,
                ft.VerticalDivider(width=1),
                ft.Column([content_container], expand=True, scroll=ft.ScrollMode.ALWAYS)
            ],
            expand=True
        )
    )
    
    # Инициализация первого экрана
    content_container.content = create_patient_ui(page)
    page.update()

# настройки, но почему они тут?
def create_settings_ui(page):
    return ft.Column(
        spacing=20,
        controls=[
            ft.Container(
                content=ft.ElevatedButton(
                    text="Экспорт всей базы",
                    icon=ft.Icons.DOWNLOAD,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    on_click=lambda e: export_vse()
                ),
                animate=ft.Animation(300, "easeOut")
            ),
            ft.Container(
                content=ft.ElevatedButton(
                    text="Переключить тему",
                    icon=ft.Icons.PALETTE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    on_click=lambda _: toggle_theme(page)
                ),
                animate=ft.Animation(300, "easeOut")
            )
        ]
    )

# логин меню
def create_login_ui(page):
    # Фоновое изображение с пиксельной сакурой
    background_image = ft.Image(
        src=f"pixel_sakura.gif", 
        fit=ft.ImageFit.COVER,
        #width=page.window_width, #чертово разрешение 
        #height=page.window_height,
        opacity=0.8,  # Полупрозрачность для лучшего восприятия
    )
    # Заголовок приложения
    app_logo = ft.Text(
        "MedVision",
        size=32,
        weight="bold",
        color="#2A9D8F",
        text_align=ft.TextAlign.CENTER,
    )
    # Поле для ввода имени пользователя
    username_field = ft.TextField(
        label="Имя пользователя",
        border_radius=15,
        filled=True,
        bgcolor=ft.Colors.WHITE10,
        focused_bgcolor=ft.Colors.WHITE24,
        width=300,
        height=50,
        text_size=14,
        cursor_color="#2A9D8F",
        prefix_icon=ft.Icons.PERSON_OUTLINE,
    )
    # Поле для ввода пароля
    password_field = ft.TextField(
        label="Пароль",
        border_radius=15,
        filled=True,
        bgcolor=ft.Colors.WHITE10,
        focused_bgcolor=ft.Colors.WHITE24,
        width=300,
        height=50,
        text_size=14,
        cursor_color="#2A9D8F",
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        password=True,
    )
    # Поле для ввода названия базы данных
    db_name_field = ft.TextField(
        label="Название базы данных",
        border_radius=15,
        filled=True,
        bgcolor=ft.Colors.WHITE10,
        focused_bgcolor=ft.Colors.WHITE24,
        width=300,
        height=50,
        text_size=14,
        cursor_color="#2A9D8F",
        prefix_icon=ft.Icons.STORAGE,
    )
    # Кнопка входа
    login_button = ft.ElevatedButton(
        text="Войти",
        icon=ft.Icons.LOGIN,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            color="#2A9D8F",
        ),
        on_click=lambda e: authenticate_user(username_field.value, password_field.value, db_name_field.value, page),
        width=300,
        height=50,
    )
    # Контейнер для центрирования элементов
    login_container = ft.Container(
        content=ft.Column(
            [
                app_logo,
                ft.Divider(height=20, color="transparent"),
                username_field,
                ft.Divider(height=10, color="transparent"),
                password_field,
                ft.Divider(height=10, color="transparent"),
                db_name_field,
                ft.Divider(height=20, color="transparent"),
                login_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=20,
        border_radius=15,
        bgcolor=ft.Colors.with_opacity(0.7, "#000000"),  # Полупрозрачный фон для контейнера
        width=400,
        height=500,
    )
    # Основной контейнер с фоном
    main_container = ft.Stack(
        [
            background_image,
            ft.Container(
                content=login_container,
                alignment=ft.alignment.center,
            ),
        ],
        expand=True,
    )
    return main_container

# функция аутентификации
def authenticate_user(username, password, db_name, page):
    # Проверяем, что все поля заполнены
    if not username or not password or not db_name:
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Пожалуйста, заполните все поля", color="#E76F51"),
            bgcolor="#E76F51",
        )
        page.snack_bar.open = True
        page.update()
        return

    # Устанавливаем параметры подключения
    DB_HOST = "localhost"
    DB_USER = username
    DB_PASSWORD = password
    DB_NAME = db_name

    try:
        # Устанавливаем учетные данные для подключения к базе данных
        set_db_credentials(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)

        # Проверяем подключение к базе данных
        conn = get_connection()
        conn.close()

        # Если подключение успешно, показываем сообщение об успешной авторизации
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Успешная авторизация!", color="#2A9D8F"),
            bgcolor="#E9C46A",
        )
        page.snack_bar.open = True
        page.update()

        # Очистка текущего интерфейса
        page.clean()

        # Загрузка главного интерфейса
        main_ui(page)
    except Exception as e:
        # Если произошла ошибка подключения, показываем сообщение об ошибке
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Ошибка подключения: {str(e)}", color="#E76F51"),
            bgcolor="#E76F51",
        )
        page.snack_bar.open = True
        page.update()

# Функция main
def main(page: ft.Page):
    page.title = "MedVision"
    page.theme_mode = ft.ThemeMode.DARK
    
    # начальный экран как экран авторизации
    page.add(create_login_ui(page))


# Запуск приложения
ft.app(target=main, assets_dir="assets")