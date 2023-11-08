import re
from exceptions import *
import hashlib
from jdatetime import datetime
from datetime import timedelta


class Patient:

    def __init__(self, name_patient, lastname_patient, code_meli, password_patient, hospital_id):
        self.name_patient = name_patient
        self.lastname_patient = lastname_patient
        self.__code_meli = Patient.__valid_code_meli(code_meli)
        self.__password_patient = Patient.__valid_pass(password_patient)
        self.hospital_id = hospital_id

    @staticmethod
    def __valid_code_meli(code_meli):
        codemeli_regex = r"^[0-9]{10}$"
        if not re.match(codemeli_regex, code_meli):
            raise InvalidCodeMeli("InvalidCodeMeli")
        else:
            return code_meli

    @staticmethod
    def __valid_pass(password):
        password_regex = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        if not re.match(password_regex, password):
            raise InvalidPassword("InvalidPassword")
        else:
            return hashlib.sha256(str(password).encode('utf-8')).hexdigest()

    @classmethod
    def register_new_patient(cls, name_patient, lastname_patient, code_meli, password_patient, hospital_id):
        return cls(name_patient, lastname_patient, code_meli, password_patient, hospital_id)

    def inser_to_database_patient(self, curser, query):
        data = (self.name_patient, self.lastname_patient, self.__code_meli, self.__password_patient, self.hospital_id)
        curser.execute(query, data)

    @staticmethod
    def login(curser, query, codemeli, password):
        curser.execute(query)
        request_log = curser.fetchall()
        # print(request_log)
        for item in request_log:
            if codemeli in item[0]:
                if item[1] == hashlib.sha256(str(password).encode('utf-8')).hexdigest():
                    return True
                return 'invalid password'
        else:
            return 'invalid codemeli'

    @staticmethod
    def select_all_list_patient(curser, query):
        curser.execute(query)
        request_log = curser.fetchall()
        return request_log

    @staticmethod
    def select_patient_id(curser, query):
        curser.execute(query)
        request_log = curser.fetchall()
        return request_log


class Doctor:

    def __init__(self, name_doctor, lastname_doctor, medical_code, specialty, hospital_id):
        self.name_doctor = name_doctor
        self.lastname_doctor = lastname_doctor
        self.__medical_code = Doctor.__valid_medical_code(medical_code)
        self.specialty = specialty
        self.hospital_id = hospital_id

    @staticmethod
    def __valid_medical_code(code):
        code_regex = r"^[0-9]{8}$"
        if not re.match(code_regex, code):
            raise InvalidMedicalCode("InvalidMedicalCode")
        else:
            return code

    @classmethod
    def register_new_doctor(cls, name_doctor, lastname_doctor, medical_code, specialty, hospital_id):
        return cls(name_doctor, lastname_doctor, medical_code, specialty, hospital_id)

    def insert_to_database_doctor(self, curser, query):
        data = (self.name_doctor, self.lastname_doctor, self.__medical_code, self.specialty, self.hospital_id)
        curser.execute(query, data)

    @staticmethod
    def login(curser, query, name_doctor, medical_code):
        curser.execute(query)
        request_log = curser.fetchall()
        # print(request_log)
        for item in request_log:
            if medical_code in item[1]:
                if item[0] == name_doctor:
                    return True
                return 'invalid name'
        else:
            return 'invalid medical code'

    @staticmethod
    def select_all_list_doctor(curser, query):
        curser.execute(query)
        request_log = curser.fetchall()
        return request_log

    @staticmethod
    def list_patient_for_doc(curser, query, doc_id):
        doc_id = (doc_id,)
        curser.execute(query, doc_id)
        request_log = curser.fetchall()
        return request_log

    @staticmethod
    def visit_statistics(curser, query, medical_code):
        medical_code = (medical_code,)
        curser.execute(query, medical_code)
        request_log = curser.fetchone()
        return request_log


class ListHospital:

    def __init__(self, name_hospital, address):
        self.name_hospital = name_hospital
        self.address = address

    @classmethod
    def register_new_list_hospital(cls, name_hospital, address):
        return cls(name_hospital, address)

    def inser_to_database_list_hospital(self, curser, query):
        data = (self.name_hospital, self.address)
        curser.execute(query, data)

    @staticmethod
    def hospital_total_amount_today(curser, query, current_datetime):
        current_datetime = (current_datetime,)
        curser.execute(query, current_datetime)
        request_log = curser.fetchall()
        my_sum = 0
        for item in request_log:
            for i in item:
                my_sum += i
        return my_sum

    @staticmethod
    def hospital_total_amount_week(curser, query):
        current_datetime = calculate_date_week()
        # current_datetime = (current_datetime,)
        curser.execute(query, current_datetime)
        request_log = curser.fetchall()
        # my_sum = 0
        # for item in request_log:
        #     for i in item :
        #         my_sum += i
        # return my_sum
        return request_log

    @staticmethod
    def hospital_total_amount_month(curser, query):
        current_datetime = calculate_date_month()
        # current_datetime = (current_datetime,)
        curser.execute(query, current_datetime)
        request_log = curser.fetchall()
        # my_sum = 0
        # for item in request_log:
        #     for i in item :
        #         my_sum += i
        # return my_sum
        return request_log


class UserAdmin:

    def __init__(self, name_admin, lastname_admin, username, password_admin, hospital_id):
        self.name_admin = name_admin
        self.lastname_admin = lastname_admin
        self.username = username
        self.__password_admin = UserAdmin.__valid_password_admin(password_admin)
        self.hospital_id = hospital_id

    @staticmethod
    def __valid_password_admin(password_admin):
        code_regex = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        if not re.match(code_regex, password_admin):
            raise InvalidPasswordAdmin("InvalidPasswordAdmin")
        else:
            return hashlib.sha256(str(password_admin).encode('utf-8')).hexdigest()

    @classmethod
    def register_new_user_admin(cls, name_admin, lastname_admin, username, password_admin, hospital_id):
        return cls(name_admin, lastname_admin, username, password_admin, hospital_id)

    def inser_to_database_user_admin(self, curser, query):
        data = (self.name_admin, self.lastname_admin, self.username, self.__password_admin, self.hospital_id)
        curser.execute(query, data)

    @staticmethod
    def login(curser, query, username, password_admin):
        curser.execute(query)
        request_log = curser.fetchall()
        # print(request_log)
        for item in request_log:
            if username in item[0]:
                if item[1] == hashlib.sha256(str(password_admin).encode('utf-8')).hexdigest():
                    return True
                return 'invalid password'
        else:
            return 'invalid user admin'

    @staticmethod
    def total_amount(curser, query, ):
        curser.execute(query)
        request_log = curser.fetchall()

        my_sum = 0
        for item in request_log:
            for i in item:
                my_sum += i
        return my_sum


class Visit:

    def __init__(self, date_visit, time_visit, amount_visit, description, doctor_id, patient_id):
        self.date_visit = date_visit
        self.time_visit = time_visit
        self.amount_visit = amount_visit
        self.description = description
        self.doctor_id = doctor_id
        self.patient_id = patient_id

    @classmethod
    def register_new_visit(cls, date_visit, time_visit, amount_visit, description, doctor_id, patient_id):
        return cls(date_visit, time_visit, amount_visit, description, doctor_id, patient_id)

    def inser_to_database_visit(self, curser, query):
        data = (self.date_visit, self.time_visit, self.amount_visit, self.description, self.doctor_id, self.patient_id)
        curser.execute(query, data)

    @staticmethod
    def select_count_visit_patient(curser, query, patient_id):
        patient_id = (patient_id,)
        curser.execute(query, patient_id)
        request_log = curser.fetchone()
        return request_log

    @staticmethod
    def select_count_visit_patient_new(curser, query, code_meli):
        code_meli = (code_meli,)
        curser.execute(query, code_meli)
        request_log = curser.fetchall()
        return request_log


def calculate_date_week():
    current_datetime = datetime.now()
    current_day = current_datetime.day
    current_month = current_datetime.month
    current_year = current_datetime.year
    days_until_sunday = (current_day - current_datetime.weekday())
    if days_until_sunday < 0:
        days_until_sunday += 30
        current_month -= 1
    if current_month <= 0:
        current_month = 12
        current_year -= 1

    # print(current_datetime)
    # print(days_until_sunday)
    # print(current_month)
    # print(current_year)

    full_date = f'{current_year}-{current_month}-{days_until_sunday}'
    date_object = datetime.strptime(full_date, "%Y-%m-%d")
    print(date_object)
    one_week_ago = date_object - timedelta(weeks=1)
    return one_week_ago.date().strftime('%Y-%m-%d'), full_date


def calculate_date_month():
    current_datetime = datetime.now()
    current_day = current_datetime.day
    current_month = current_datetime.month
    current_year = current_datetime.year
    # days_until_sunday = (current_day - current_datetime.weekday())
    current_day = 1
    current_month -= 1
    if current_month <= 0:
        current_month = 12
        current_year -= 1

    # print(current_datetime)
    # print(days_until_sunday)
    # print(current_month)
    # print(current_year)

    full_date_first = f'{current_year}-{current_month}-{current_day}'
    full_date_last = f'{current_year}-{current_month}-{30}'

    # date_object = datetime.strptime(full_date, "%Y-%m-%d")
    # print(date_object)
    # one_week_ago = date_object - timedelta(weeks=1)
    return full_date_first, full_date_last
