import unittest
import psycopg2
from unittest.mock import Mock, patch
from db_connect import config, connect
from db_contextmanager import *

class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        # Set up a mock for ConfigParser to avoid reading an actual config file
        self.config_parser_mock = Mock()
        self.config_parser_mock.has_section.return_value = True
        self.config_parser_mock.items.return_value = [
            ('host', 'localhost'),
            ('database', 'hospital'),
            ('user', 'postgres'),
            ('password', '0020@002062'),
            ('port', '5432')
        ]

    def test_config(self):
        """Test the config function."""
        with patch('db_connect.ConfigParser', return_value=self.config_parser_mock):
            params = config('database.ini', 'xxxx')
        
        expected_params = {
            'host': 'localhost',
            'database': 'hospital',
            'user': 'postgres',
            'password': '0020@002062',
            'port': '5432'
        }
        self.assertEqual(params, expected_params)

    def test_connect_exception_handling(self):
        """Test the connect function with an exception."""
        with patch('db_connect.config', side_effect=Exception("Error")):
            conn, cur, local_connection = connect(None, None)

        self.assertIsNone(conn)
        self.assertIsNone(cur)
        self.assertIsNone(local_connection)

class TestDataBaseContextManager(unittest.TestCase):
    
    @patch('db_connect.connect', return_value=(None, None, True))
    def test_insert_hospital_success(self, connect_mock):
        db_context = DataBaseContextManager()
        db_context.insert_hospital("Hospital Name", "Hospital Address")
        # Add assertions here to check if the hospital has been successfully inserted.
        
    @patch('db_connect.connect', return_value=(None, None, True))
    def test_insert_hospital_failure(self, connect_mock):
        db_context = DataBaseContextManager()
        with self.assertRaises(Exception):
            db_context.insert_hospital("", "Invalid Address")
    # Similar tests for other methods like insert_patient, insert_doctor, etc.
    
    @patch('db_connect.connect', return_value=(None, None, True))
    def test_login_patient_success(self, connect_mock):
        db_context = DataBaseContextManager()
        result = db_context.login_patient("code_meli", "password")
        # Add assertions here to check if the login was successful.
        
    @patch('db_connect.connect', return_value=(None, None, True))
    def test_login_patient_failure(self, connect_mock):
        db_context = DataBaseContextManager()
        result = db_context.login_patient("code_meli", "invalid_password")
        # Add assertions here to check if the login failed as expected.
        
    @patch('db_connect.connect', return_value=(None, None, True))    
    def test_login_doctor_success(self, connect_mock):
        db_context = DataBaseContextManager()
        result = db_context.login_doctor("Doctor Name", "Medical Code")
        # Add assertions here to check if the doctor login was successful.
        
    @patch('db_connect.connect', return_value=(None, None, True))
    def test_login_doctor_failure(self, connect_mock):
        db_context = DataBaseContextManager()
        result = db_context.login_doctor("Invalid Name", "Invalid Medical Code")
        # Add assertions here to check if the doctor login failed as expected.
        
    @patch('db_connect.connect', return_value=(None, None, True))
    def test_login_user_admin_success(self, connect_mock):
        db_context = DataBaseContextManager()
        result = db_context.login_user_admin("Admin Username", "Admin Password")
        # Add assertions here to check if the user admin login was successful.
        
    @patch('db_connect.connect', return_value=(None, None, True))
    def test_login_user_admin_failure(self, connect_mock):
        db_context = DataBaseContextManager()
        result = db_context.login_user_admin("Invalid Username", "Invalid Password")    

if __name__ == '__main__':
    unittest.main()
