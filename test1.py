import unittest
import psycopg2
from db_connect import config, connect
from db_contextmanager import DataBaseContextManager
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from models import Patient, Doctor, UserAdmin, ListHospital, Visit
import hashlib
import re
import random
import string

DATABASE_CONNECTION = {
    'dbname': 'hospital',
    'user': 'postgres',
    'password': '0020@002062',
    'host': 'localhost',
    'port': '5432'
}



# generate a valid test password
def generate_test_password():
    password_pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    while True:
        password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(12))
        if re.match(password_pattern, password):
            return password

# generate a valid code_meli
def generate_test_code_meli():
    code_meli = ''.join(random.choices('0123456789', k=10))
    return code_meli

# generate a valid test password for admin
def generate_valid_medical_code():
    generate_medical_code = ''.join(str(random.randint(0, 9)) for _ in range(8))
    return generate_medical_code


test_password = generate_test_password()
test_codemelli = generate_test_code_meli()
test_admin_password = generate_test_password()
medical_code = generate_valid_medical_code()



def connect(database, user, password, host, port):
    try:
        conn = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()
        return conn, cur, True
    except Exception as e:
        print(f"Error: {e}")
        return None, None, False


class TestDatabaseConnection(unittest.TestCase):

    def setUp(self):
        # test database connection
        self.test_db_config = {
            'database': 'hospital',
            'user': 'postgres',
            'password': '0020@002062',
            'host': 'localhost',
            'port': '5432'
        }

    def test_config(self):
        params = config('database.ini', 'xxxx')
        self.assertIsInstance(params, dict)
        self.assertIn('database', params)
        self.assertIn('user', params)
        self.assertIn('password', params)
        self.assertIn('host', params)
        self.assertIn('port', params)

    def test_connect(self):
        conn, cur, local_connection = connect(self.test_db_config['database'], self.test_db_config['user'], self.test_db_config['password'], self.test_db_config['host'], self.test_db_config['port'])
        self.assertTrue(local_connection)
        self.assertIsInstance(conn, psycopg2.extensions.connection)
        self.assertIsInstance(cur, psycopg2.extensions.cursor)

        cur.close()
        conn.close()


    def setUp(self):
        # test database connection
        self.test_db_config = {
            'database': 'hospital',
            'user': 'postgres',
            'password': '0020@002062',
            'host': 'localhost',
            'port': '5432'
        }

    def test_config(self):
        params = config('database.ini', 'xxxx')
        self.assertIsInstance(params, dict)
        self.assertIn('database', params)
        self.assertIn('user', params)
        self.assertIn('password', params)
        self.assertIn('host', params)
        self.assertIn('port', params)

    def test_connect(self):
        conn, cur, local_connection = connect(self.test_db_config['database'], self.test_db_config['user'], self.test_db_config['password'], self.test_db_config['host'], self.test_db_config['port'])
        self.assertTrue(local_connection)
        self.assertIsInstance(conn, psycopg2.extensions.connection)
        self.assertIsInstance(cur, psycopg2.extensions.cursor)

        cur.close()
        conn.close()




class TestDoctor(unittest.TestCase):

    def setUp(self):
        self.conn = psycopg2.connect(**DATABASE_CONNECTION)
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.conn.cursor()

        self.doctor = Doctor.register_new_doctor('test_doctor_n', 'test_doctor_f', '48178124', 'test_especialty', 1)

    def tearDown(self):
        self.cur.close()
        self.conn.close()

    def test_register_new_doctor(self):
        self.assertEqual(self.doctor.name_doctor, 'test_doctor_n')
        self.assertEqual(self.doctor.lastname_doctor, 'test_doctor_f')
        self.assertEqual(self.doctor.__medical_code, '48178124')
        self.assertEqual(self.doctor.specialty, 'test_especialty')

    def test_insert_to_database_doctor(self):
        query = "INSERT INTO doctor(name_doctor, lastname_doctor, medical_code, specialty, hospital_id) VALUES (%s, %s, %s, %s, %s)"
        self.doctor.insert_to_database_doctor(self.cur, query)

        query = "SELECT * FROM doctor WHERE medical_code = %s"
        self.cur.execute(query, ('49178124',))
        result = self.cur.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[1], 'test_doctor_n')
        self.assertEqual(result[2], 'test_doctor_f')
        self.assertEqual(result[3], '49178124' )
        self.assertEqual(result[4], 'test_especialty')
        self.assertEqual(result[5], 1)

    def test_login(self):
        query = "INSERT INTO doctor(name_doctor, lastname_doctor, medical_code, specialty, hospital_id) VALUES (%s, %s, %s, %s, %s)"
        self.doctor.insert_to_database_doctor(self.cur, query)

        result = Doctor.login(self.cur, "SELECT name_doctor, medical_code FROM doctor", 'test_doctor_n', '38178124')
        self.assertTrue(result)

        result = Doctor.login(self.cur, "SELECT name_doctor, medical_code FROM doctor", 'docotor_wrong', '38178124')
        self.assertEqual(result, 'invalid name')
        result = Doctor.login(self.cur, "SELECT name_doctor, medical_code FROM doctor", 'test_doctor_n', '12345678')
        self.assertEqual(result, 'invalid medical code')

    def test_select_all_doctor(self):
        query = "INSERT INTO doctor(name_doctor, lastname_doctor, medical_code, specialty, hospital_id) VALUES (%s, %s, %s, %s, %s)"
        self.doctor.insert_to_database_doctor(self.cur, query)
        self.doctor.insert_to_database_doctor(self.cur, query)

        result = Doctor.select_all_doctor(self.cur, "SELECT * FROM doctor")
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)

    def test_patient_for_doc(self):
        doc_id = 1
        query = "INSERT INTO patient(name_patient, lastname_patient, code_meli, password_patient, hospital_id) VALUES (%s, %s, %s, %s, %s)"
        self.doctor.insert_to_database_doctor(self.cur, query)
        self.doctor.insert_to_database_doctor(self.cur, query)


        result = Doctor.patient_for_doc(self.cur, "SELECT * FROM patient WHERE hospital_id = %s", doc_id)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)

    def test_visit_statistics(self):
        medical_code = medical_code
        query = "INSERT INTO patient(name_patient, lastname_patient, code_meli, password_patient, hospital_id) VALUES (%s, %s, %s, %s, %s)"
        self.doctor.insert_to_database_doctor(self.cur, query)
        self.doctor.insert_to_database_doctor(self.cur, query)
        result = Doctor.visit_statistics(self.cur, "SELECT COUNT(*) FROM patient WHERE hospital_id = %s", medical_code)
        self.assertEqual(result, 2)



class TestListHospital(unittest.TestCase):

    def setUp(self):
        self.conn = psycopg2.connect(**DATABASE_CONNECTION)
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.conn.cursor()

        self.hospital = ListHospital.register_new_list_hospital('hospital_name', 'hospital_address')

    def tearDown(self):
        self.cur.close()
        self.conn.close()

    def test_register_new_list_hospital(self):
        self.assertEqual(self.hospital.name_hospital, 'hospital_name')
        self.assertEqual(self.hospital.address, 'hospital_address')

    def test_insert_to_database_list_hospital(self):
        query = "INSERT INTO list_hospital(name_hospital, address) VALUES (%s, %s)"
        self.hospital.inser_to_database_list_hospital(self.cur, query)

        query = "SELECT * FROM list_hospital WHERE name_hospital = %s"
        self.cur.execute(query, ('hospital_name',))
        result = self.cur.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[1], 'hospital_name')
        self.assertEqual(result[2], 'hospital_address')



class TestUserAdmin(unittest.TestCase):

    def setUp(self):
        self.conn = psycopg2.connect(**DATABASE_CONNECTION)
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.conn.cursor()

        self.user_admin = UserAdmin.register_new_user_admin('test_admin_f', 'test_admin_l', 'test_admin', test_admin_password, 1)

    def tearDown(self):
        self.cur.close()
        self.conn.close()

    def test_register_new_user_admin(self):
        self.assertEqual(self.user_admin.name_admin, 'test_admin_f')
        self.assertEqual(self.user_admin.lastname_admin, 'test_admin_l')
        self.assertEqual(self.user_admin.username, 'test_admin')

    def test_insert_to_database_user_admin(self):
        query = "INSERT INTO user_admin(name_admin, lastname_admin, username, password_admin, hospital_id) VALUES (%s, %s, %s, %s, %s)"
        self.user_admin.inser_to_database_user_admin(self.cur, query)

        query = "SELECT * FROM user_admin WHERE name_admin = %s"
        self.cur.execute(query, ('test_admin_f',))
        result = self.cur.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[1], 'test_admin_f')
        self.assertEqual(result[2], 'test_admin_l')
        self.assertEqual(result[3], 'test_admin')


class TestVisit(unittest.TestCase):

    def setUp(self):
        self.conn = psycopg2.connect(**DATABASE_CONNECTION)
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.conn.cursor()

        self.visit = Visit.register_new_visit('1380-02-19', '11:00', 100, 'heart', 1, 1)

    def tearDown(self):
        self.cur.close()
        self.conn.close()

    def test_register_new_visit(self):
        self.assertEqual(self.visit.date_visit, '1380-02-19')
        self.assertEqual(self.visit.time_visit, '11:00')
        self.assertEqual(self.visit.amount_visit, 100)

    def test_insert_to_database_visit(self):
        query = "INSERT INTO visit(date_visit, time_visit, amount_visit, description, doctor_id, patient_id) VALUES (%s, %s, %s, %s, %s, %s)"
        self.visit.inser_to_database_visit(self.cur, query)

        query = "SELECT * FROM visit WHERE date_visit = %s"
        self.cur.execute(query, ('1380-02-19',))
        result = self.cur.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[1], '1380-02-19')
        self.assertEqual(result[2], '11:00')
        self.assertEqual(result[3], 100)



if __name__ == '__main__':
    unittest.main()
