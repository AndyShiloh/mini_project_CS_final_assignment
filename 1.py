def create_student_tuple(students):
    student_vectors = []
    for student in students:
        if student.Gender == "Male":
            gender_code = 0.5
        else:
            gender_code = -0.5
        a = CGPA
        gpa = (a-2.5)/5
        codeCCDS = 0
        codeEEE = 0
        codeCoB = 0
        codeSoH = 0
        codeWKW_SCI = 0
        codeCoE = 0
        codeMAE = 0
        codeSPMS = 0
        codeSBS = 0
        codeSSS = 0
        codeASE = 0
        codeNIE = 0
        codeADM = 0
        codeMSE = 0
        codeLKCMedicine = 0
        codeCCEB = 0
        codeCEE = 0
        if student.school == "CCDS":
            codeCCDS += 1
        elif student.school == "EEE":
            codeEEE += 1
        elif student.school == "CoB":
            codeCoB += 1
        elif student.school == "SoH":
            codeSoH += 1
        elif student.school == "WKW_SCI":
            codeWKW_SCI += 1
        elif student.school == "CoE":
            codeCoE += 1
        elif student.school == "MAE":
            codeMAE += 1
        elif student.school == "SPMS":
            codeSPMS += 1
        elif student.school == "SBS":
            codeSBS += 1
        elif student.school == "SSS":
            codeSSS += 1
        elif student.school == "ASE":
            codeASE += 1
        elif student.school == "NIE":
            codeNIE += 1
        elif student.school == "ADM":
            codeADM += 1
        elif student.school == "MSE":
            codeMAS += 1
        elif student.school == "LKCMedicine":
            codeLCKMedicine += 1
        elif student.school == "CCEB":
            codeCCEB += 1
        elif student.school == "CEE":
            codeCEE += 1
        student_Vector = (gpa,gender_code,codeCCDS,codeEEE,codeCoB,codeSoH,codeWKW_SCI,codeCoE,codeMAE,codeSPMS,codeSBS,codeSSS,codeASE,codeNIE,codeADM,codeMSE,codeLKCMedicine,codeCCEB,codeCEE)
        student_vectors.append(student_Vector)
    return tuple(student_vectors)






            
          
