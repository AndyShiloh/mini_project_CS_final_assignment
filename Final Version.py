def read():
    import csv
    import re
    with open("records.csv","r") as f:
        students=list(csv.DictReader(f))
    stu_dict = {}
    for row in students:
        number= re.search(r'G-(\d+)',row['Tutorial Group'])
        if number:
            num = int(number.group(1))
            if num not in stu_dict:
                stu_dict[num]=[]
            stu_dict[num].append(row)

    student_list=[]
    for i in sorted(stu_dict.keys()):
        Ti = []
        for j, student in enumerate(stu_dict[i], start=1):
            varname = f's{j}'        
            globals()[varname] = student
            Ti.append(student)
            
        globals()[f'T{i}'] = Ti
        student_list.append(Ti)

    return student_list

def create_student_tuple(students):
    student_vectors = []
    for student in students:
        if student["Gender"] == "Male":
            gender_code = 0.5
        else:
            gender_code = -0.5
        a = float(student["CGPA"])
        gpa = round((a-2.5)/5,3)
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
        if student["School"]  == "CCDS":
            codeCCDS += 1
        elif student["School"]   == "EEE":
            codeEEE += 1
        elif student["School"]   == "CoB":
            codeCoB += 1
        elif student["School"]   == "SoH":
            codeSoH += 1
        elif student["School"]   == "WKW_SCI":
            codeWKW_SCI += 1
        elif student["School"]   == "CoE":
            codeCoE += 1
        elif student["School"]   == "MAE":
            codeMAE += 1
        elif student["School"]   == "SPMS":
            codeSPMS += 1
        elif student["School"]   == "SBS":
            codeSBS += 1
        elif student["School"]   == "SSS":
            codeSSS += 1
        elif student["School"]   == "ASE":
            codeASE += 1
        elif student["School"]   == "NIE":
            codeNIE += 1
        elif student["School"]   == "ADM":
            codeADM += 1
        elif student["School"]   == "MSE":
            codeMSE += 1
        elif student["School"]   == "LKCMedicine":
            codeLKCMedicine += 1
        elif student["School"]   == "CCEB":
            codeCCEB += 1
        elif student["School"]   == "CEE":
            codeCEE += 1
        student_Vector = (gpa,gender_code,codeCCDS,codeEEE,codeCoB,codeSoH,codeWKW_SCI,codeCoE,codeMAE,codeSPMS,codeSBS,codeSSS,codeASE,codeNIE,codeADM,codeMSE,codeLKCMedicine,codeCCEB,codeCEE)
        student.update({"vector":student_Vector})
    return students

def find_displacement_of_vectors(vector1,vector2):
    squre_add=0
    for i in range(len(vector1)):
        squre_add+=(vector1[i]-vector2[i])**2
    return squre_add

def find_average_vector(informationlist): 
    vector_len = len(informationlist[0]["vector"])
    sum_vector = [0.0] * vector_len 
    num_students = len(informationlist)
    for student in informationlist:
        vector = student["vector"]
        for i in range(vector_len):
            sum_vector[i] += vector[i]
    for i in range(vector_len):
        sum_vector[i] = sum_vector[i] / num_students 
    average_vector=tuple(sum_vector.copy())
    return average_vector

def predict_group_average(student_vector, group_average_vector, number_people):
    result = []
    for value1, value2 in zip(student_vector, group_average_vector):
        result.append((value1 + value2 * number_people) / (number_people + 1))
    return tuple(result)

def core_grouping_algorithm(informationlist,n_DIM):
    group = [[] for _ in range(10)]
    group_average_vector_list = [[0.0] * n_DIM for _ in range(10)]
    total_average_vector=find_average_vector(informationlist)
    
    for s in informationlist:
        s["difference"] = find_displacement_of_vectors(s["vector"], total_average_vector)
    informationlist.sort(key=lambda item:item["difference"],reverse=False)
    
    for num in range(5):
        nearest_10=informationlist[0:10].copy()
        for k in range(10): 
            informationlist.pop(0)
        
        for i in range(10):
            minn=0x7f7f7f7f7f
            student_ID=0
            
            for j in range(len(nearest_10)):
                new_average=predict_group_average(nearest_10[j]["vector"],group_average_vector_list[i],num)
                displace=find_displacement_of_vectors(new_average,total_average_vector)
                if minn > displace:
                    student_ID=j
                    minn=displace
            
            nearest_10[student_ID]["group"]=i+1
            group[i].append(nearest_10[student_ID])
            
            for dim in range(n_DIM):
                group_average_vector_list[i][dim]=((num)*group_average_vector_list[i][dim]+nearest_10[student_ID]["vector"][dim])/(num+1)
            
            nearest_10.pop(student_ID)
    return group

if __name__ == "__main__":
    # Read all tutorial groups
    all_groups = read()
    print(f"Total tutorial groups read: {len(all_groups)}")
    
    # Store export data for all groups
    all_export_data = []
    
    # Process each tutorial group in loop
    for group_num in range(1, len(all_groups) + 1):
        try:
            print(f"\n{'='*50}")
            print(f"Processing G-{group_num}...")
            print(f"{'='*50}")
            
            selected_group = all_groups[group_num-1]
            
            # Vectorization processing
            result = create_student_tuple(selected_group)
            informationlist = result
            n_DIM = len(informationlist[0]["vector"])
            print(f"Vectorization completed, vector dimension: {n_DIM}")
            
            # Calculate average vector
            average_vector = find_average_vector(result)
            print(f"Average vector: {average_vector}")
            
            # Run initial grouping algorithm
            print("Performing initial grouping...")
            grouping_result = core_grouping_algorithm(informationlist, n_DIM)
            
            # Iterative optimization part
            print("Starting grouping optimization iteration...")
            
            def find_avg_vector_for_group(student_list):
                if not student_list:
                    return tuple([0.0] * n_DIM)
                vector_len = len(student_list[0]["vector"])
                sum_vector = [0.0] * vector_len 
                num_students = len(student_list)
                for student in student_list:
                    vector = student["vector"]
                    for i in range(vector_len):
                        sum_vector[i] += vector[i]
                for i in range(vector_len):
                    sum_vector[i] = sum_vector[i] / num_students 
                return tuple(sum_vector)

            def check(T, ave, gap=0.01):
                for A in T:
                    group_avg = find_avg_vector_for_group(A)
                    displacement = 0
                    for i in range(len(group_avg)):
                        displacement += (group_avg[i] - ave[i]) ** 2
                    if displacement > gap:
                        return False
                return True

            def swap(A, B, i, j):
                A_new = A.copy()
                B_new = B.copy()
                i_index = None
                j_index = None
                for idx, student in enumerate(A_new):
                    if student["vector"] == i["vector"] and student.get("Name") == i.get("Name"):
                        i_index = idx
                        break
                for idx, student in enumerate(B_new):
                    if student["vector"] == j["vector"] and student.get("Name") == j.get("Name"):
                        j_index = idx
                        break
                if i_index is not None and j_index is not None:
                    student_i = A_new[i_index]
                    student_j = B_new[j_index]
                    A_new[i_index] = student_j
                    B_new[j_index] = student_i
                return A_new, B_new

            def group_swap(A, B, ave, already_move, move_time=50, accuracy=0.02):
                if len(already_move) >= move_time:
                    return A, B
                A_current = A
                B_current = B
                avg_A = find_avg_vector_for_group(A)
                avg_B = find_avg_vector_for_group(B)
                current_displacement_A = 0
                current_displacement_B = 0
                for i in range(len(avg_A)):
                    current_displacement_A += (avg_A[i] - ave[i]) ** 2
                    current_displacement_B += (avg_B[i] - ave[i]) ** 2
                if current_displacement_A <= accuracy and current_displacement_B <= accuracy:
                    return A, B
                for student_a in A:
                    for student_b in B:
                        key = (tuple(student_a["vector"]), tuple(student_b["vector"]))
                        if key not in already_move:
                            already_move[key] = True
                            A_new, B_new = swap(A, B, student_a, student_b)
                            new_avg_A = find_avg_vector_for_group(A_new)
                            new_avg_B = find_avg_vector_for_group(B_new)
                            new_displacement_A = 0
                            new_displacement_B = 0
                            for i in range(len(new_avg_A)):
                                new_displacement_A += (new_avg_A[i] - ave[i]) ** 2
                                new_displacement_B += (new_avg_B[i] - ave[i]) ** 2
                            if (new_displacement_A < current_displacement_A and 
                                new_displacement_B < current_displacement_B):
                                return group_swap(A_new, B_new, ave, already_move, move_time, accuracy)
                return A, B

            def pick_group(T, ave, time=20, gap=0.01):
                def _pick_group_recursive(T, ave, time, gap, current_time=0):
                    if current_time >= time:
                        print(f"Reached maximum iteration count: {time}")
                        return T
                    if check(T, ave, gap):
                        print(f"Accuracy requirement met, iteration completed: {current_time} times")
                        return T
                    print(f"Performing iteration {current_time + 1}...")
                    M = sorted(T, key=lambda g: find_avg_vector_for_group(g), reverse=True)
                    A = M[0]
                    B = M[-1]
                    already_move = {}
                    new_a, new_b = group_swap(A, B, ave, already_move, move_time=20, accuracy=gap)
                    M[0] = new_a
                    M[-1] = new_b
                    return _pick_group_recursive(M, ave, time, gap, current_time + 1)
                return _pick_group_recursive(T, ave, time, gap)

            # Execute iterative optimization
            T_optimize = grouping_result
            optimized_groups = pick_group(T_optimize, average_vector, time=5, gap=0.05)
            
            # Collect export data for current group
            for i, small_group in enumerate(optimized_groups, 1):
                for student in small_group:
                    displacement = find_displacement_of_vectors(student["vector"], average_vector)
                    export_row = student.copy()
                    export_row["Assigned_Group"] = f"G-{group_num}-{i}"
                    export_row["Vector_Displacement"] = round(displacement, 6)
                    if "vector" in export_row:
                        del export_row["vector"]
                    if "difference" in export_row:
                        del export_row["difference"]
                    if "group" in export_row:
                        del export_row["group"]
                    all_export_data.append(export_row)
            
            print(f"G-{group_num} processing completed, total students: {len(selected_group)}")
            
        except Exception as e:
            print(f"Error processing G-{group_num}: {e}")
            continue
    
    # After all groups processed, export to single CSV file
    if all_export_data:
        output_filename = "all_tutorial_groups_results.csv"
        import csv
        with open(output_filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = list(all_export_data[0].keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_export_data)
        print(f"\n{'='*50}")
        print(f"All groups processing completed!")
        print(f"Results exported to file: {output_filename}")
        print(f"Total student records exported: {len(all_export_data)}")
        print(f"Contains {len(all_groups)} tutorial groups")
        print(f"{'='*50}")
    else:
        print("No data to export")
