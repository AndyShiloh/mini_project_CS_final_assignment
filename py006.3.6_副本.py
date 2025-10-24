import csv
import random
import copy
# 此版新加入了输入成绩误差控制
def input_grade():
    try:
        return float(input("Enter range of grade: "))
    except :
        print("there is a mistake in the input will took 0.01 as the range of grade")
        return 0.01
range_of_grade = input_grade()

def read_CSV(a):
    group_list = []
    A = "G-" + str(a)
    print(A)
    with open("/Users/linsa/Desktop/python集合/records.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["Tutorial Group"] == A:
                group_list.append(row)
    print(f"read record:{len(group_list)} ")
    return group_list

group_list = read_CSV(7)


def ave_grade(list_):
    global stu_grade
    stu_grade = {}
    total = 0
    for i in list_:
        A = i["Student ID"]
        stu_grade[A] = float(i["CGPA"])
        total += float(i["CGPA"])
    avg = total / len(list_)
    print(f"average grade: {avg:.3f}")
    return avg


avg_grade = ave_grade(group_list)


def per_Gender(list_):
    global list_male, list_female
    list_male, list_female = [], []
    for i in list_:
        if i["Gender"] == "Male":
            list_male.append(i["Student ID"])
        elif i["Gender"] == "Female":
            list_female.append(i["Student ID"])
    print(f"male: {len(list_male)}, female: {len(list_female)}")
    return len(list_male), len(list_female)


male, female = per_Gender(group_list)


def type_school(list_):
    global stu_school
    stu_school = {}
    for i in list_:
        stu_school[i["Student ID"]] = i["School"]
    return stu_school


type_school(group_list)


def cal_type(a, b):
    diff = a - b
    # 四种组型: [三男两女, 三女两男, 四男一女, 四女一男]
    if diff > 10:
        return [b - 10, 0, 20 - b, 0]
    elif diff < -10:
        return [0, a - 10, 0, 20 - a]
    else:
        return [a - 20, 30 - a, 0, 0]


type_group = cal_type(male, female)
print(f"type of group:3male 2female:{type_group[0]};2male 3female:{type_group[1]};4male 1female:{type_group[2]};1male 4female:{type_group[3]}")


def check_avg(stu, target_avg, tolerance):
    total = sum(stu_grade[i] for i in stu)
    avg = total / len(stu)
    if check_school(stu,stu_school,mix_school = 2):
        return abs(avg - target_avg) <= tolerance
    else:
        return False

def check_school(stu,stu_school,mix_school = 2):
    both_school = 0
    if len(stu) <= 1:
        return True
    for i in stu:
        for j in stu:
            if j == i:
                continue
            if stu_school[i] == stu_school[j]:
                both_school += 1
            else :
                continue
    if both_school > mix_school:
        return False
    return True

def generate_one_group(males, females, pattern, tolerance,group_size=5):
    """
    pattern: 1=三男两女, 2=三女两男, 3=四男一女, 4=四女一男
    """
    if pattern == 1:
        need_m, need_f = 3, 2
    elif pattern == 2:
        need_m, need_f = 2, 3
    elif pattern == 3:
        need_m, need_f = 4, 1
    else:
        need_m, need_f = 1, 4

    if len(males) < need_m or len(females) < need_f:
        return None

    for _ in range(500):
        selected_m = random.sample(males, need_m)
        selected_f = random.sample(females, need_f)
        group = selected_m + selected_f
        if check_avg(group, avg_grade, tolerance):
            return group
    return None

def full_grouping(males, females, type_group, tolerance, group_size=5):
    all_groups = []
    patterns = (
        [1] * type_group[0]
        + [2] * type_group[1]
        + [3] * type_group[2]
        + [4] * type_group[3]
    )
    total_needed = sum(type_group)
    print(f"target:  {total_needed} group, {group_size} students per group")

    def backtrack(current_idx, remaining_m, remaining_f, current_groups):
        if current_idx == len(patterns):
            # 所有人都成功分组
            return current_groups

        pattern = patterns[current_idx]
        group = generate_one_group(remaining_m, remaining_f, pattern, tolerance,group_size )
        if not group:
            return None

        # 移除已使用学生
        new_m = [m for m in remaining_m if m not in group]
        new_f = [f for f in remaining_f if f not in group]

        res = backtrack(current_idx + 1, new_m, new_f, current_groups + [group])
        if res:
            return res

        # 如果失败，尝试重新生成该组
        return None

    for attempt in range(200):  # 多次尝试不同随机路径
        random.shuffle(males)
        random.shuffle(females)
        result = backtrack(0, males.copy(), females.copy(), [])
        if result:
            print("✅Process finished")
            return result
    print("❌Fail")
    return None

def re_team(A,B):
    if A == None:
        B += 0.01
        print(f"the range of grade is too small, add to {B}")
        C = full_grouping(list_male, list_female, type_group,5,B)
        D = re_team(C,B)
        return D
    else:
        return A



A = full_grouping(list_male, list_female, type_group,range_of_grade)
all_groups = re_team(A,range_of_grade)
if all_groups:
    for i, g in enumerate(all_groups, 1):
        print(f"Group {i}: {g}")
def export_team_csv(groups, group_list,filename):
    with open(filename, "a+", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Tutorial Group", "Student ID", "School", "Name", "Gender", "CGPA", "Team Assigned"])
        for team_index, team in enumerate(groups, start=1):
            team_name = f"T{team_index:02d}"
            for sid in team:
                # 在 group_list 中找到该学生的详细资料
                for row in group_list:
                    if row["Student ID"] == sid:
                        writer.writerow([
                            row["Tutorial Group"],
                            row["Student ID"],
                            row["School"],
                            row["Name"],
                            row["Gender"],
                            row["CGPA"],
                            team_name
                        ])
                        break



import matplotlib.pyplot as plt
from collections import Counter

def analyze_groups(groups, group_list, delta=0.1):
    # 构建学生详细信息字典
    student_info = {row["Student ID"]: row for row in group_list}

    group_stats = []

    for idx, group in enumerate(groups, 1):
        grades = [float(student_info[sid]["CGPA"]) for sid in group]
        avg_grade = sum(grades) / len(grades)

        genders = [student_info[sid]["Gender"] for sid in group]
        male_count = genders.count("Male")
        female_count = genders.count("Female")

        schools = [student_info[sid]["School"] for sid in group]
        school_counter = Counter(schools)

        group_stats.append({
            "Group": f"G{idx:02d}",
            "AvgGrade": avg_grade,
            "Male": male_count,
            "Female": female_count,
            "SchoolDist": school_counter
        })

    groups_names = [g["Group"] for g in group_stats]
    overall_avg = sum([float(row["CGPA"]) for row in group_list]) / len(group_list)

    # -------------------- 平均成绩柱状图 --------------------
    plt.figure(figsize=(10, 5))
    avg_grades = [g["AvgGrade"] for g in group_stats]
    bars = plt.bar(groups_names, avg_grades, color="skyblue")
    plt.axhline(overall_avg, color='red', linestyle='--', label=f"Overall Avg: {overall_avg:.2f}")

    # 在柱子上显示具体数据
    for bar, grade in zip(bars, avg_grades):
        plt.text(bar.get_x() + bar.get_width()/2, grade + 0.002, f"{grade:.2f}",
                 ha='center', va='bottom', fontsize=9)

    # 缩放 y 轴，只显示平均附近 ± delta
    plt.ylim(overall_avg - delta, overall_avg + delta)
    plt.ylabel("Average CGPA")
    plt.title("Group Average Grades vs Overall Average (Zoomed)")
    plt.legend()
    plt.show()

    # -------------------- 男女比例堆叠图 --------------------
    plt.figure(figsize=(10, 5))
    male_counts = [g["Male"] for g in group_stats]
    female_counts = [g["Female"] for g in group_stats]
    plt.bar(groups_names, male_counts, label="Male")
    plt.bar(groups_names, female_counts, bottom=male_counts, label="Female")
    plt.ylabel("Number of Students")
    plt.title("Gender Distribution in Each Group")
    plt.legend()
    plt.show()

    # -------------------- 学院占比堆叠图（带标号） --------------------
    all_schools = list({row["School"] for row in group_list})
    school_matrix = []
    for g in group_stats:
        school_matrix.append([g["SchoolDist"].get(school, 0) for school in all_schools])

    school_matrix = list(zip(*school_matrix))  # 转置方便堆叠
    plt.figure(figsize=(12, 6))
    bottom = [0]*len(group_stats)

    for idx, school_counts in enumerate(school_matrix):
        plt.bar(groups_names, school_counts, bottom=bottom, label=all_schools[idx])

        # 在柱子堆上标注学院名+人数
        for i, (b, count) in enumerate(zip(bottom, school_counts)):
            if count > 0:  # 只标注非零部分
                plt.text(i, b + count/2, f"{all_schools[idx]} ({count})",
                         ha='center', va='center', fontsize=8, rotation=90)
        bottom = [sum(x) for x in zip(bottom, school_counts)]

    plt.ylabel("Number of Students")
    plt.title("School Distribution in Each Group (Labeled)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # 图例放到右边
    plt.tight_layout()
    plt.show()

    return group_stats

# 使用示例
stats = analyze_groups(all_groups, group_list, delta=0.1)




filename = "team_allocation.csv"
for i in range (2,3):
    group_list = read_CSV(i)
    avg_grade = ave_grade(group_list)
    male, female = per_Gender(group_list)
    type_school(group_list)
    type_group = cal_type(male, female)
    A = full_grouping(list_male, list_female, type_group, 5, range_of_grade)
    all_groups = re_team(A, range_of_grade)
    export_team_csv(all_groups, group_list, filename)
    if all_groups:
        for i, g in enumerate(all_groups, 1):
            print(f"Group {i}: {g}")