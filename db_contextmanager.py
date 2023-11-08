from models import *
from exceptions import *
from db_connect import connect


class DataBaseContextManager:
    def __init__(self) -> None:
        self.conn = None
        self.cur = None
        self.local_connection = None
        self.result = None
        self.err = None
        self.dbcontextmanager = None
        self.exc_val = None

    def __enter__(self):
        return self

    # =========================================== Insert Hospital =====================================
    def insert_hospital(self, name_hospital, address, conn=None, cur=None):
        if all([name_hospital, address]):
            self.dbcontextmanager = ListHospital.register_new_list_hospital(name_hospital, address)
        else:
            raise HospitalCreateFail('HospitalCreateFail')

        if self.dbcontextmanager:
            self.conn, self.cur, self.local_connection = connect(conn, cur)
            query = """INSERT INTO list_hospital(name_hospital, address) values(%s,%s)"""
            self.dbcontextmanager.inser_to_database_list_hospital(self.cur, query)

    # ============================================= Insert Patient =======================================
    def insert_patient(self, name_patient, lastname_patient, code_meli, password_patient, hospital_id, conn=None,
                       cur=None):
        if all([name_patient, lastname_patient, code_meli, password_patient, hospital_id]):
            self.dbcontextmanager = Patient.register_new_patient(name_patient, lastname_patient, code_meli,
                                                                 password_patient, hospital_id)
        else:
            raise HospitalCreateFail('HospitalCreateFail')

        if self.dbcontextmanager:
            self.conn, self.cur, self.local_connection = connect(conn, cur)
            query = """INSERT INTO patient(name_patient, lastname_patient, code_meli, password_patient, hospital_id) values(%s,%s,%s,%s,%s)"""
            self.dbcontextmanager.inser_to_database_patient(self.cur, query)

    # ============================================== Insert doctor ==================================================

    def insert_doctor(self, name_doctor, lastname_doctor, medical_code, specialty, hospital_id, conn=None, cur=None):
        if all([name_doctor, lastname_doctor, medical_code, specialty, hospital_id]):
            self.dbcontextmanager = Doctor.register_new_doctor(name_doctor, lastname_doctor, medical_code, specialty,
                                                               hospital_id)
        else:
            raise HospitalCreateFail('HospitalCreateFail')

        if self.dbcontextmanager:
            self.conn, self.cur, self.local_connection = connect(conn, cur)
            query = """INSERT INTO doctor(name_doctor, lastname_doctor, medical_code, specialty, hospital_id) values(%s,%s,%s,%s,%s)"""
            self.dbcontextmanager.insert_to_database_doctor(self.cur, query)

    # =============================================== Insert user admin ====================================================

    def insert_user_admin(self, name_admin, lastname_admin, username, password_admin, hospital_id, conn=None, cur=None):
        if all([name_admin, lastname_admin, username, password_admin, hospital_id]):
            self.dbcontextmanager = UserAdmin.register_new_user_admin(name_admin, lastname_admin, username,
                                                                      password_admin, hospital_id)
        else:
            raise HospitalCreateFail('HospitalCreateFail')

        if self.dbcontextmanager:
            self.conn, self.cur, self.local_connection = connect(conn, cur)
            query = """INSERT INTO user_admin(name_admin, lastname_admin, username, password_admin, hospital_id) values(%s,%s,%s,%s,%s)"""
            self.dbcontextmanager.inser_to_database_user_admin(self.cur, query)

    # ========================================== Insert visit =================================================================

    def insert_visit(self, date_visit, time_visit, amount_visit, description, doctor_id, patient_id, conn=None,
                     cur=None):
        if all([date_visit, time_visit, amount_visit, description, doctor_id, patient_id]):
            self.dbcontextmanager = Visit.register_new_visit(date_visit, time_visit, amount_visit, description,
                                                             doctor_id, patient_id)
        else:
            raise VisitCreateFail('VisitCreateFail')

        if self.dbcontextmanager:
            self.conn, self.cur, self.local_connection = connect(conn, cur)
            query = """INSERT INTO visit(date_visit, time_visit, amount_visit, description, doctor_id, patient_id) values(%s,%s,%s,%s,%s,%s)"""
            self.dbcontextmanager.inser_to_database_visit(self.cur, query)

    # ============================================= Login patient =================================================

    def login_patient(self, code_meli, password, conn=None, cur=None):
        self.conn, self.cur, self.local_connection = connect(conn, cur)
        pg_select = """ SELECT code_meli, password_patient FROM "patient" """
        result = Patient.login(self.cur, pg_select, code_meli, password)
        return result

    # ============================================= Login doctor =================================================

    def login_doctor(self, name_doctor, medical_code, conn=None, cur=None):
        self.conn, self.cur, self.local_connection = connect(conn, cur)
        pg_select = """ SELECT name_doctor, medical_code FROM "doctor" """
        result = Doctor.login(self.cur, pg_select, name_doctor, medical_code)
        return result

    # ============================================ Login user_admin ==============================================

    def login_user_admin(self, username, password_admin, conn=None, cur=None):
        self.conn, self.cur, self.local_connection = connect(conn, cur)
        pg_select = """ SELECT username, password_admin FROM "user_admin" """
        result = UserAdmin.login(self.cur, pg_select, username, password_admin)
        return result

    # =========================================== List All Patient =============================================

    # def select_all_patient(self, table, *columns, conn=None, cur=None):
    #     self.conn, self.cur, self.local_connection = connect(conn, cur)
    #     pg_select = " SELECT {0} FROM {1}".format(", ".join(columns), table)
    #     pg_select += ";"
    #     Patient.select_all(self.cur,pg_select)

    def list_all_patient(self, conn=None, cur=None):
        self.conn, self.cur, self.local_connection = connect(conn, cur)
        pg_select = """ SELECT name_patient, lastname_patient, code_meli FROM "patient" """
        result = Patient.select_all_list_patient(self.cur, pg_select)
        return result

    def patient_id(self, code_meli_enter, conn=None, cur=None):
        self.conn, self.cur, self.local_connection = connect(conn, cur)
        pg_select = f""" SELECT patient_id FROM "patient" WHERE code_meli='{code_meli_enter}'"""
        result = Patient.select_patient_id(self.cur, pg_select)
        return result

    # ========================================= List All doctor =====================================================

    def list_all_doctor(self, conn=None, cur=None):
        self.conn, self.cur, self.local_connection = connect(conn, cur)
        pg_select = """ SELECT doctor_id,name_doctor, lastname_doctor, specialty FROM "doctor" """
        result = Doctor.select_all_list_doctor(self.cur, pg_select)
        return result

    def doctor_id(self, medical_code_get, conn=None, cur=None):
        self.conn, self.cur, self.local_connection = connect(conn, cur)
        pg_select = f""" SELECT doctor_id FROM "doctor" WHERE medical_code='{medical_code_get}'"""
        result = Patient.select_patient_id(self.cur, pg_select)
        return result

    # ======================================== count visit patient ==================================================

    def count_visit_patient(self, conn=None, cur=None):
        self.conn, self.cur, self.local_connection = connect(conn, cur)
        pg_select = """ SELECT COUNT(patient_id) FROM "visit" GROUP BY patient_id """
        result = Visit.select_count_visit_patient(self.cur, pg_select)
        return result

    def count_visit_patient_new(self, code_meli, conn=None, cur=None):
        self.conn, self.cur, self.local_connection = connect(conn, cur)
        pg_select = """ SELECT name_patient, lastname_patient, date_visit::text, time_visit FROM "patient" 
               JOIN "visit" ON patient.patient_id = visit.patient_id
               where code_meli = %s """
        result = Visit.select_count_visit_patient_new(self.cur, pg_select, code_meli)
        return result

    def list_patient_for_doctor(self, doc_id, conn=None, cur=None):
        self.conn, self.cur, self.local_connection = connect(conn, cur)
        pg_select = """ SELECT name_patient, lastname_patient, date_visit::text, time_visit FROM "patient" 
               JOIN "visit" ON patient.patient_id = visit.patient_id
               where doctor_id = %s """
        result = Doctor.list_patient_for_doc(self.cur, pg_select, doc_id)
        return result

    def hospital_total_income_today(self, conn=None, cur=None):
        # current_datetime = datetime.now().date()
        # current_datetime = current_datetime.strftime('%Y-%m-%d')
        # print(current_datetime)
        current_datetime = '1402-08-10'
        self.conn, self.cur, self.local_connection = connect(conn, cur)
        pg_select = """ SELECT amount_visit::integer FROM "visit"
               where date_visit = %s """
        result = ListHospital.hospital_total_amount_today(self.cur, pg_select, current_datetime)
        return result

    def hospital_total_income_week(self, conn=None, cur=None):
        self.conn, self.cur, self.local_connection = connect(conn, cur)
        pg_select = """ SELECT amount_visit::integer FROM "visit"
            where date_visit BETWEEN %s And %s """
        result = ListHospital.hospital_total_amount_week(self.cur, pg_select)
        return result

    def hospital_total_income_month(self, conn=None, cur=None):
        self.conn, self.cur, self.local_connection = connect(conn, cur)
        pg_select = """ SELECT amount_visit::integer FROM "visit"
            where date_visit BETWEEN %s And %s """
        result = ListHospital.hospital_total_amount_month(self.cur, pg_select)
        return result

    def statistics_visit_of_each_doctor(self, medical_code, conn=None, cur=None):
        self.conn, self.cur, self.local_connection = connect(conn, cur)
        pg_select = """ SELECT doctor_id FROM "doctor"
            where medical_code = %s """
        result = Doctor.visit_statistics(self.cur, pg_select, medical_code)
        return result

    def total_visit_amount(self, conn=None, cur=None):
        self.conn, self.cur, self.local_connection = connect(conn, cur)
        pg_select = """ SELECT amount_visit::integer FROM "visit" """
        result = UserAdmin.total_amount(self.cur, pg_select)
        return result

    def count_visit_patient(self, patient_id, conn=None, cur=None):
        self.conn, self.cur, self.local_connection = connect(conn, cur)
        pg_select = """ SELECT COUNT(patient_id) FROM "visit"  where patient_id = %s """
        result = Visit.select_count_visit_patient(self.cur, pg_select, patient_id)
        return result

    def select_doctor(self, conn=None, cur=None):
        self.conn, self.cur, self.local_connection = connect(conn, cur)
        pg_select = """ SELECT doctor_id, name_doctor FROM "doctor" """
        result = Doctor.select_doctor_as_patient(self.cur, pg_select)
        return result

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val and self.local_connection:
            self.dbcontextmanager = None
            self.err = f'Create patient fail --> {exc_val}'
            print(self.err)
            self.cur.close()
            self.conn.close()
        elif not exc_val and self.dbcontextmanager is not None and self.local_connection:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            self.result = 'Create patient'
            print(self.result)
