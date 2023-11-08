from db_contextmanager import *

# with DataBaseContextManager() as hospital :
#     hospital.insert_hospital('milad','tehran')



# with DataBaseContextManager() as patient :
#     patient.insert_patient('mohammad','meysam','1234567890','c', 1)


# with DataBaseContextManager() as doctor :
#     doctor.insert_doctor('abolfazl','rasouli','12345678','cardiovascular', 1)



# with DataBaseContextManager() as useradmin :
#     useradmin.insert_user_admin('meysam','tajik','meysam','!Q1w2e3r4', 1)


# with DataBaseContextManager() as visit :
#     visit.insert_visit('1402-08-10','15:00-15:15',170000,'cold', 1, 1)



# with DataBaseContextManager() as patient :
#     answer = patient.login_patient('1234567890','!Q1w2e3r4')
#     print(answer)



# with DataBaseContextManager() as doctor :
#     result = doctor.login_doctor('abolfazl','12345678')
#     print(result)


# with DataBaseContextManager() as useradmin :
#     result = useradmin.login_user_admin('meysam','!Q1w2e3r4')
#     print(result)



# with DataBaseContextManager() as patient :
#     result = patient.list_all_patient()
#     print(result)


# with DataBaseContextManager() as doctor :
#     result = doctor.list_all_doctor()
#     print(result)


with DataBaseContextManager() as visit :
    result = visit.count_visit_patient(1)
    print(result)



# with DataBaseContextManager() as doctor :
#     result = doctor.select_doctor()
#     print(result)
    # for i in result :
    #     for j in i :
    #         print(type(j))




# with DataBaseContextManager() as doctor :
#     result = doctor.list_patient_for_doctor(1)
#     print(result)


# with DataBaseContextManager() as user_admin :
#     result = user_admin.total_visit_amount()
    # print(result)


# with DataBaseContextManager() as doctor:
#     result = doctor.statistics_visit_of_each_doctor("12345678")
#     print(result)


# with DataBaseContextManager() as hospital:
#     result = hospital.hospital_total_income_today()
#     print(result)



# with DataBaseContextManager() as hospital:
#     result = hospital.hospital_total_income_week()
#     print(result)

#
# with DataBaseContextManager() as hospital:
#     result = hospital.hospital_total_income_month()
#     print(result)



