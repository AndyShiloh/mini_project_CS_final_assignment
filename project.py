#!/usr/bin/env python
# coding: utf-8

# In[1]:


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

print(student_list)






# In[3]:


import os
print(os.getcwd())
      


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




