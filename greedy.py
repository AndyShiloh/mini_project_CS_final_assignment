def find_displacement_of_vectors(vector1,vector2): #find displacement of two vecters
    squre_add=0
    for i in range(len(vector1)):
        squre_add+=(vector1[i]-vector2[i])**2
    return squre_add
def find_average_vector(informationlist): 
    #for every list[s1{},s2{}...] like small group list[s1{},s2{},s3{}..s5{}] and tutorial group list [s1{}...s50{}], we need to find the average vector
    #the function can deal with the small group or the whole tutorial group
    #informationlist:[s1{},s2,s3..] 
    vector_len = len(informationlist[0]["vector"]) # the n_DIM of the vector=2+num(school)
    sum_vector = [0.0] * vector_len 
    num_students = len(informationlist)
    # Summation
    for student in informationlist:
        vector = student["vector"]  # Get the vector tuple
        for i in range(vector_len):
            sum_vector[i] += vector[i]
    # 3. Calculate Average (using the correct divisor: num_students)
    for i in range(vector_len):
        sum_vector[i] = sum_vector[i] / num_students 
    average_vector=tuple(sum_vector.copy())
    return average_vector
def predict_group_average(student_vector, group_average_vector, number_people):
    #number_people is how  many people are in the small group now before adding a new student
    #the function's function is to find the new average vector of a small group ,if I choose one student to the small group
    result = []
    for value1, value2 in zip(student_vector, group_average_vector):
        result.append((value1 + value2 * number_people) / (number_people + 1))
    return tuple(result)

def core_grouping_alogrithm(informationlist,n_DIM):
    #informationlist:[s1{},s2{},s3{}...] 
    #this function is the greedy algorithm, deal with one tutorial group
    group = [[] for _ in range(10)] #give the list like this: [[],[],[],[],[],[],[],[],[],[]] each elements is a small group[]
    group_average_vector_list = [[0.0] * n_DIM for _ in range(10)]#this list contains each small group's present average vector
    total_average_vector=find_average_vector(informationlist)#get the whole average vector of the tutorial group
    for s in informationlist:
        s["difference"] = find_displacement_of_vectors(s["vector"], total_average_vector)#find the difference between studen's vector and tutoral average vector
    informationlist.sort(key=lambda item:item["difference"],reverse=False)#sort all the students according to the difference from low to high
    for num in range(5):# 50 peole 10 people each turn, so repeat 5 turns
        #find nearest students
        nearest_10=informationlist[0:10].copy() # get nearest student about tutorial average vector
        for i in range(10): informationlist.pop(0)# delet them from the tutorial group list
        for i in range(10):#iterate each small group
            minn=0x7f7f7f7f7f # 0x7f7f7f7f is a very big number
            student_ID=0# this is a flag to record students index who can make the small group vector nearest about tutorial group vector
            for j in range(len(nearest_10)):# iterate 10 students
                # if I choose this student in now small group, what the new average vector the small group wil have 
                new_average=predict_group_average(nearest_10[j]["vector"],tuple(group_average_vector_list[i]),num)
                displace=find_displacement_of_vectors(new_average,total_average_vector)# calculate new difference between new small group average vector and tutorial group vector
                if minn > displace:# if the displacement can be smaller, so the student is the most appropriate to arrange into now's group
                    student_ID=j
                    minn=displace
            #arrange student to now's group
            nearest_10[student_ID]["group"]=i+1
            group[i].append(nearest_10[student_ID])
            #calculate the new average vector for now's small group
            for j in range(n_DIM):
                group_average_vector_list[i][j]=((num)*group_average_vector_list[i][j]+nearest_10[student_ID]["vector"][j])/(num+1)
            nearest_10.pop(student_ID)
    return group
    