---
hide:
  - toc
---

# Setup

We'll use the following imports for all code extracts:

```py
# Imports
import pandas as pd
import lib.SAAT as SAAT
import lib.utils as utils
```

First we read in the data:

```py
# Read & Clean
data = pd.read_csv("data/example_data.csv")
```

Then we extract each persons department from their email: 

```py
# Get department from email
data["Department"] = data["Email"].map(lambda email: utils.email_to_department(email))
```
<font size="2">(this is only appropriate if your organisation follows the person@department.organisation.com email format, otherwise you'll probably already have a department field) </font>

And select only those who are going to discuss 'Topic1':

```py
data = data[data['Topic'] == 'Topic1']
data.head()
```
| Name     | Email                    | Years_In_Org | Grade  | Setup     | Topic  | 1-2pm | ... | 5-6pm3 | Department  |
| -------- | ------------------------ | ------------ | ------ | --------- | ------ | ----- | --- | ------ | ----------- |
| Person1  | Person1@DepartmentG.com  | <1 year      | Level1 | If needed | Topic1 | 0     | ... | 1      | departmentg |
| Person10 | Person10@DepartmentF.com | 1-3 years    | Level2 | If needed | Topic1 | 1     | ... | 0      | departmentf |
| Person12 | Person12@DepartmentH.com | 5-10 years   | Level2 | Yes       | Topic1 | 0     | ... | 0      | departmenth |
| Person16 | Person16@DepartmentL.com | 1-3 years    | Level2 | If needed | Topic1 | 0     | ... | 0      | departmentl |
| Person17 | Person17@DepartmentG.com | \>10 years   | Level2 | No        | Topic1 | 1     | ... | 0      | departmentg |

Note, your setup is likely to look somewhat different to this depending on your data format.


