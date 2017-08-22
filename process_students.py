from collections import OrderedDict
import pandas as pd
import re

students = []
with open('students.txt') as f:
    data = f.readlines()
    school = ""
    cohort_num = None
    for line in data:
        if line[0] == '*':
            try:
                a = re.search('\*\s(.*?)\s-', line)
                b = re.search('\[(.*?)\]', line)
                c = re.search('//(.*?)\)', line)
                name = " ".join(a.group()[2:-2].split())
                project_name = b.group()[1:-1]
                project_url = c.group()[2:-1]
            except AttributeError:
                pass
            student = OrderedDict()
            student['name'] = name
            student['project_name'] = project_name
            student['project_url'] = project_url
            student['school'] = school
            student['cohort_num']= cohort_num
            students.append(student)

        elif line[0:2] == '##':
            try:
                string = re.search('\((.*?)\)', line)
                school = string.group()[1:-1].split()[0]
                cohort_num = int(string.group()[1:-1].split()[2])
            except AttributeError:
                pass

df = pd.DataFrame(students)
df.to_csv('students.csv', index=False)
