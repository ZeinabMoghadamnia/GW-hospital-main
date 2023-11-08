import unittest
import psycopg2
from models import Patient, Doctor, ListHospital, UserAdmin, Visit

class TestHospitalApp(unittest.TestCase):
    def setUp(self):
        # Set up a test database connection
        self.conn = psycopg2.connect(
            dbname='test_database',
            user='postgres',
            password='0020@002062',
            host='localhost',
            port=5432
        )

    def tearDown(self):
        # Clean up the test database
        self.conn.close()

    def test_patient_registration_and_login(self):
        # Create a patient and insert into the database
        with self.conn.cursor() as cursor:
            patient = Patient.register_new_patient("asghar", "asghari", "1234567890", "TestPassword1", 1)
            patient.inser_to_database_patient(cursor, "INSERT INTO patients (name_patient, lastname_patient, code_meli, password_patient, hospital_id) values(%s, %s, %s, %s, %s)")

        # Check if the patient was inserted correctly
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM patients WHERE code_meli = %s", ("1234567890",))
            result = cursor.fetchone()
            self.assertIsNotNone(result)

        # Test patient login
        with self.conn.cursor() as cursor:
            login_result = Patient.login(cursor, "SELECT code_meli, password_patient FROM patients WHERE code_meli = %s", "1234567890", "TestPassword1")
            self.assertTrue(login_result)

    def test_doctor_registration_and_login(self):
        # Create a doctor and insert into the database
        with self.conn.cursor() as cursor:
            doctor = Doctor.register_new_doctor("Dr. jafari", "Cardiologist", "12345678", "Cardiology", 1)
            doctor.insert_to_database_doctor(cursor, "INSERT INTO doctors (name_doctor, lastname_doctor, medical_code, specialty, hospital_id) values(%s, %s, %s, %s, %s)")
            
        # Check if the doctor was inserted correctly
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM doctors WHERE medical_code = %s", ("12345678",))
            result = cursor.fetchone()
            self.assertIsNotNone(result)

        # Test doctor login
        with self.conn.cursor() as cursor:
            login_result = Doctor.login(cursor, "SELECT name_doctor, medical_code FROM doctors WHERE medical_code = %s", "Dr. jafari", "12345678")
            self.assertTrue(login_result)

    def test_list_hospital_registration(self):
        # Create a hospital and insert into the database
        with self.conn.cursor() as cursor:
            hospital = ListHospital.register_new_list_hospital("Test Hospital", "sadeghieh Sq.")
            hospital.inser_to_database_list_hospital(cursor, "INSERT INTO list_hospitals (name_hospital, address) VALUES (%s, %s)")
            
        # Check if the hospital was inserted correctly
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM list_hospitals WHERE name_hospital = %s", ("Test Hospital",))
            result = cursor.fetchone()
            self.assertIsNotNone(result)

    def test_user_admin_registration_and_login(self):
        # Create a user admin and insert into the database
        with self.conn.cursor() as cursor:
            user_admin = UserAdmin.register_new_user_admin("mammad", "mammadi", "adminuser", "AdminPassword1", 1)
            user_admin.inser_to_database_user_admin(cursor, "INSERT INTO user_admins (name_admin, lastname_admin, username, password_admin, hospital_id) VALUES (%s, %s, %s, %s, %s)")

        # Check if the user admin was inserted correctly
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM user_admins WHERE username = %s", ("adminuser",))
            result = cursor.fetchone()
            self.assertIsNotNone(result)

        # Test user admin login
        with self.conn.cursor() as cursor:
            login_result = UserAdmin.login(cursor, "SELECT username, password_admin FROM user_admins WHERE username = %s", "adminuser", "AdminPassword1")
            self.assertTrue(login_result)

    def test_visit_registration(self):
        # Create a patient and doctor
        with self.conn.cursor() as cursor:
            patient = Patient.register_new_patient("asghar", "asghari", "1234567890", "TestPassword1", 1)
            patient.inser_to_database_patient(cursor, "INSERT INTO patients (name_patient, lastname_patient, code_meli, password_patient, hospital_id) VALUES (%s, %s, %s, %s, %s)")
            doctor = Doctor.register_new_doctor("Dr. jafari", "Cardiologist", "12345678", "Cardiology", 1)
            doctor.insert_to_database_doctor(cursor, "INSERT INTO doctors (name_doctor, lastname_doctor, medical_code, specialty, hospital_id) VALUES (%s, %s, %s, %s, %s)")

        # Create a visit and insert into the database
        with self.conn.cursor() as cursor:
            visit = Visit.register_new_visit("2023-11-08", "10:00", 100, "Heart checkup", 1, 1)
            visit.inser_to_database_visit(cursor, "IINSERT INTO visits (date_visit, time_visit, amount_visit, description, doctor_id, patient_id) VALUES (%s, %s, %s, %s, %s, %s)")

        # Check if the visit was inserted correctly
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM visits WHERE description = %s", ("Heart checkup",))
            result = cursor.fetchone()
            self.assertIsNotNone(result)



if __name__ == '__main__':
    unittest.main()
