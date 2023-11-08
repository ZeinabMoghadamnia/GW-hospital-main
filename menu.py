from tkinter import Menu
from datetime import datetime
import models
from models import *
from db_contextmanager import *


class Sign_doctor:

    def __init__(self, number: str):
        self.number = number
        Sign_doctor.check_options(number)

    @staticmethod
    def sign_up():
        with DataBaseContextManager() as doctor:
            name_doctor = input("Enter Your name doktor: ")
            lastname_doctor = input("Enter Your lastname: ")
            medical_code = input("Enter Your medicalcode: ")
            specialty = input("Enter Your speciality: ")
            doctor.insert_doctor(name_doctor, lastname_doctor, medical_code, specialty, 1)
        Menu("1")

    @staticmethod
    def sign_in():
        with DataBaseContextManager() as doctor:
            name_doctor = input("Enter Your name: ")
            password = input("Enter Your password: ")
            result = doctor.login_doctor(name_doctor, password)
            if result == True:
                Sign_doctor.show_paitent(password)
                Menu("1")
            else:
                print(result)
                Menu("1")

    @staticmethod
    def show_paitent(password):
        with DataBaseContextManager() as id:
            with DataBaseContextManager() as doctor:
                doctor_id = id.doctor_id(password)
            result = doctor.list_patient_for_doctor(doctor_id[0][0])
            print('patients: ')
            for i in result:
                print(f'name: {i[0]} \tfamily: {i[1]} \tdate :{i[2]} \thours :{i[3]} ')

    @staticmethod
    def check_options(number):
        match number:
            case '1':
                Sign_doctor.sign_up()
            case '2':
                Sign_doctor.sign_in()
            case "3":
                main()


class Sign_patient:
    values = {
        "1": "sobh",
        "2": "asr",
        "3": "shab"
    }

    def __init__(self, number: str):
        self.number = number
        Sign_patient.check_options(number)

    @staticmethod
    def sign_up():
        with DataBaseContextManager() as patient:
            name_patient = input("Enter Your name: ")
            lastname_patient = input("Enter Your lastname: ")
            code_meli = input("Enter Your national code: ")
            password_patient = input("Enter Your password: ")
            patient.insert_patient(name_patient, lastname_patient, code_meli, password_patient, 1)
        Menu("2")

    @staticmethod
    def sign_in():
        with DataBaseContextManager() as patient:
            code_meli = input("Enter Your national code: ")
            password_patient = input("Enter Your password: ")
            answer = patient.login_patient(code_meli, password_patient)
            if answer == True:
                Sign_patient.show_shifts(code_meli)
            else:
                print(answer)
                Menu("2")

    @staticmethod
    def show_shifts(code_meli):
        for i, j in Sign_patient.values.items():
            print(i, j)
        number = input('Choose an option:  ')
        match number:
            case '1':
                if datetime.now().hour >= 13:
                    print('you cant choose sobh')
                    Sign_patient.show_shifts(code_meli)
                Shifts().shifte_sobh(code_meli)
            case '2':
                if datetime.now().hour >= 21:
                    print('you cant choose asr')
                    Sign_patient.show_shifts(code_meli)
                Shifts().shifte_zohr(code_meli)
            case "3":
                Shifts().shifte_shab(code_meli)

            case _:
                print('invalid number ')
                Sign_patient.show_shifts(code_meli)

    @staticmethod
    def check_options(number):
        match number:
            case '1':
                Sign_patient.sign_up()
            case '2':
                Sign_patient.sign_in()
            case "3":
                main()


class Sign_user:
    def __int__(self):
        pass

    @staticmethod
    def sign_in():
        with DataBaseContextManager() as useradmin:
            name = input("Enter Your Username: ")
            password = input("Enter Your password: ")
            result = useradmin.login_user_admin(name, password)
            if result == True:
                Show_user()
            else:
                print(result)
                Menu("3")


class Show_user:
    def __init__(self):
        Show_user.choice()

    @staticmethod
    def show_doctors():
        with DataBaseContextManager() as doctor:
            result = doctor.list_all_doctor()
            for name in result:
                print(name[1])
            Show_user.choice()

    @staticmethod
    def show_patient():
        with DataBaseContextManager() as patient:
            result = patient.list_all_patient()
            for names in result:
                print(f'name : {names[0]}\t family : {names[1]}')
            Show_user.choice()

    @staticmethod
    def amount_visit():
        with DataBaseContextManager() as amount:
            result = amount.total_visit_amount()
            print(result)
            Show_user.choice()

    @staticmethod
    def history_paitent_doctor():
        medical_code = input("enter your medical code: ")
        with DataBaseContextManager() as id:
            with DataBaseContextManager() as doctor:
                doctor_id = id.doctor_id(medical_code)
            result = doctor.list_patient_for_doctor(doctor_id[0][0])
            print('patients: ')
            for i in result:
                print(f'name: {i[0]} \tfamily: {i[1]} \tdate :{i[2]} \thours :{i[3]} ')
        Show_user.choice()

    @staticmethod
    def history_patient():
        with DataBaseContextManager() as visit:
            code_meli = input('enter code meli...')
            result = visit.count_visit_patient_new(code_meli)
            for results in result:
                print(f'name : {results[0]}\t family : {results[1]}\t date : {results[2]}\t time  : {results[3]}')
        Show_user.choice()

    @staticmethod
    def amount_full():
        Amount_full()
        Show_user.choice()

    @staticmethod
    def choice():
        values = {
            "1": "show doctors",
            "2": "show patient",
            "3": "amount visit",
            "4": "history patient of doctor",
            "5": "amount full",
            "6": "history patient",
            "7": "Back"
        }
        for i, j in values.items():
            print(i, j)
        choice = input("choose your option: ")
        match choice:
            case "1":
                Show_user.show_doctors()
            case "2":
                Show_user.show_patient()
            case "3":
                Show_user.amount_visit()
            case "4":
                Show_user.history_paitent_doctor()
            case "5":
                Show_user.amount_full()
            case "6":
                Show_user.history_patient()
            case "7":
                main()
            case _:
                print("Invalid option")
                Show_user.choice()


class Amount_full:
    def __init__(self):
        Amount_full.choice_option()

    @staticmethod
    def amount_day():
        with DataBaseContextManager() as hospital:
            result = hospital.hospital_total_income_today()
            print(result)
            Amount_full.choice_option()

    @staticmethod
    def amount_week():
        with DataBaseContextManager() as hospital:
            result = hospital.hospital_total_income_week()
            print(result)
            Amount_full.choice_option()

    @staticmethod
    def amount_month():
        with DataBaseContextManager() as hospital:
            result = hospital.hospital_total_income_month()
            print(result)
            Amount_full.choice_option()

    @staticmethod
    def choice_option():
        values = {
            "1": "show day",
            "2": "show week",
            "3": "amount month",
            "4": "Back"
        }
        for i, j in values.items():
            print(i, j)
        choice = input("choose your option: ")
        match choice:
            case "1":
                Amount_full.amount_day()
            case "2":
                Amount_full.amount_week()
            case "3":
                Amount_full.amount_month()
            case "4":
                Show_user.choice()


class Shifts:
    shift_sobh = ['06-07', '07-08', '08-09', '09-10', '10-11', '11-12', '12-13', '13-14']
    shift_zohr = ['14-15', '15-16', '16-17', '17-18', '18-19', '19-20', '20-21', '21-22']
    shift_shab = ['22-23', '23-24', '00-01', '01-02', '02-03', '03-04', '04-05', '05-06']
    choices = ['1', '2', '3', '4', '5', '6', '7', '8']
    doctors = {}
    COUNTER_SHIFT = 8
    patient_id = None

    def __init__(self):
        with DataBaseContextManager() as doctor:
            result = doctor.list_all_doctor()
            for doctor_list in result:
                Shifts.doctors[doctor_list[0]] = doctor_list[1]

    @staticmethod
    def shifte_sobh(code_meli):
        count = 1
        counter = 0
        menu_shifts = []
        first_key = next(iter(Shifts.doctors))
        two_key = list(Shifts.doctors.keys())[1]
        shift_doctor = Shifts.doctors[two_key]
        # Shifts.shift_sobh_new = Shifts.shift_sobh
        for shift in Shifts.shift_sobh:
            if datetime.now().hour >= int(shift[:2]):
                # print(shift[:2])
                counter += 1
                continue
            menu_shifts.append(shift)
            print(f'{count}:({shift})   {datetime.now().date()}      Doctor {shift_doctor}')
            count += 1
        Shifts.get_patient_id(code_meli)
        Shifts.insert_visit(menu_shifts, 1, counter, int(two_key), Shifts.patient_id)
        # choice_shift = input('Enter your shift: ')
        # if choice_shift in Menu.choices:
        #     Menu.shift_sobh_new.pop(int(choice_shift) - 1)
        #     # Menu.option2()
        #     # with DataBaseContextManager() as visit :
        #     #     visit.insert_visit('1402-08-10 14-00','1402-08-10 14-15',170000,'cold', 1, 1)
        # main()

    @staticmethod
    def shifte_zohr(code_meli):
        count = 1
        counter = 0
        menu_shifts = []
        first_key = next(iter(Shifts.doctors))
        two_key = list(Shifts.doctors.keys())[1]
        shift_doctor = Shifts.doctors[first_key]
        # Menu.shift_zohr_new = Shifts.shift_zohr
        for shift in Shifts.shift_zohr:
            if datetime.now().hour >= int(shift[:2]):
                counter += 1
                continue
            menu_shifts.append(shift)
            print(f'{count}:({shift})   {datetime.now().date()}         Doctor {shift_doctor}')
            count += 1
        Shifts.get_patient_id(code_meli)
        Shifts.insert_visit(menu_shifts, 2, counter, int(first_key), Shifts.patient_id)
        # choice_shift = input('Enter your shift:  ')
        # if choice_shift in Menu.choices:
        #     shift = Menu.shift_zohr_new[int(choice_shift)]
        #     print(shift)
        #     Menu.shift_zohr_new.pop(int(choice_shift) - 1)
        #     description = input('Enter your description:  ')
        #     with DataBaseContextManager() as visit:
        #         visit.insert_visit(f'{datetime.now().date()} {shift[:2]}-00', f'{datetime.now().date()} {shift}',
        #                            170000, description, 1, 1)
        main()

    @staticmethod
    def shifte_shab(code_meli):
        count = 1
        counter = 0
        menu_shifts = []
        two_key = list(Shifts.doctors.keys())[1]
        shift_doctor = Shifts.doctors[two_key]
        # Menu.shift_shab_new = Menu.shift_shab
        # date = datetime.now().date()
        # print(f'{date}')
        date = datetime.now().date()
        print(date)
        for shift in Shifts.shift_shab:
            if datetime.now().hour >= int(shift[:2]) and int(shift[0]) != 0:
                counter += 1
                continue
            menu_shifts.append(shift)
            # date = datetime.now().today().date()
            print(f'{count}:({shift})          Doctor {shift_doctor}')
            # print(f'{datetime.now()}')
            count += 1
        Shifts.get_patient_id(code_meli)
        Shifts.insert_visit(menu_shifts, 3, counter, int(two_key), Shifts.patient_id)

    @staticmethod
    def get_patient_id(code_meli):
        with DataBaseContextManager() as patient:
            result = patient.patient_id(code_meli)
            print(result)
            Shifts.patient_id = result[0][0]

    @staticmethod
    def insert_visit(menu_shifts, shifts, counter, doctor_id: int, patient_id: int):
        choice_shift = input('Enter your shift: ')
        counter_shifts = Shifts.COUNTER_SHIFT - counter
        if choice_shift in Shifts.choices and int(choice_shift) <= counter_shifts:
            shift = menu_shifts[int(choice_shift) - 1]
            if shifts == 3:
                Shifts.shift_shab.pop(int(choice_shift) + counter - 1)
            elif shifts == 2:
                Shifts.shift_zohr.pop(int(choice_shift) + counter - 1)
            elif shifts == 1:
                Shifts.shift_sobh.pop(int(choice_shift) + counter - 1)
            description = input('Enter your description:  ')
            with DataBaseContextManager() as visit:
                visit.insert_visit(str(datetime.now().date()), f'{shift}',
                                   170000, description, doctor_id, patient_id)
        else:
            print('invalid number ')
            Shifts.insert_visit(menu_shifts, shifts, counter, doctor_id, patient_id)
        main()


class Menu:
    # shift_sobh = ['6-7', '7-8', '8-9', '9-10', '10-11', '11-12', '12-13', '13-14']
    # shift_zohr = ['14-15', '15-16', '16-17', '17-18', '18-19', '19-20', '20-21', '21-22']
    # shift_shab = ['22-23', '23-24', '00-01', '01-02', '02-03', '03-04', '04-05', '05-06']
    # choices = ['1', '2', '3', '4', '5', '6', '7', '8']
    # shifts = [0, 0, 0]

    def __init__(self, number: str):
        Menu.check_options(number)

    @staticmethod
    def doctor():
        # count = 1
        # Menu.shift_sobh_new = Menu.shift_sobh
        # for shift in Menu.shift_sobh_new:
        #     print(f'{count}: {shift}')
        #     count += 1
        #
        # choice_shift = input('Enter your shift: ')
        # if choice_shift in Menu.choices:
        #     Menu.shift_sobh_new.pop(int(choice_shift) - 1)
        #     Menu.option1()
        # main()
        numbers = ["1", "2", "3"]
        values = {
            "1": "Sign Up:",
            "2": "Sign in",
            "3": "Back"
        }
        for i, j in values.items():
            print(i, j)
        number = input("Choose an option: ")
        if number in numbers:
            Sign_doctor(number)
        else:
            print("your number is mistake")
            Menu.doctor()

    @staticmethod
    def patient():
        # count = 1
        # Menu.shift_zohr_new = Menu.shift_zohr
        # for shift in Menu.shift_zohr_new:
        #     print(f'{count}: {shift}')
        #     count += 1
        #
        # choice_shift = input('Enter your shift:  ')
        # if choice_shift in Menu.choices:
        #     Menu.shift_zohr_new.pop(int(choice_shift) - 1)
        #     Menu.option2()
        numbers = ["1", "2", "3"]
        values = {
            "1": "Sign Up:",
            "2": "Sign in",
            "3": "Back"
        }
        for i, j in values.items():
            print(i, j)
        number = input("Choose an option: ")
        if number in numbers:
            Sign_patient(number)
        else:
            print("your number is mistake")
            Menu.patient()

    @staticmethod
    def user_admin():
        pass

        # count = 1
        # Menu.shift_shab_new = Menu.shift_shab
        # for shift in Menu.shift_shab_new:
        #     print(f'{count}: {shift}')
        #     count += 1
        #
        # choice_shift = input('Enter your shift: ')
        # if choice_shift in Menu.choices:
        #     Menu.shift_shab_new.pop(int(choice_shift) - 1)
        #     Menu.option3()
        # main()

        Sign_user().sign_in()

    @staticmethod
    def check_options(number):
        match number:
            case '1':
                Menu.doctor()
            case '2':
                Menu.patient()
            case '3':
                Menu.user_admin()
            case _:
                pass


def main():
    menu = ['1', '2', '3']
    values = {
        "1": "Doctor",
        "2": "patient",
        "3": "Useradmin"
    }
    for i, j in values.items():
        print(i, j)
    # print("""
    # Menu:
    # 1. Doktor
    # 2. Paitent
    # 3. Useradmin
    # """)

    choice = input("Choose an option: ")
    if choice in menu:
        Menu(choice)
    else:
        print("Invalid option")
        main()


main()
