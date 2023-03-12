---
hide:
  - toc
---

# Data

Here's an example of the structure of data SAAT expects:

| Name    | Email                   | Years_In_Org | Grade  | Setup     | Topic  | 1-2pm | 2-3pm | 3-4pm | 4-5pm | 5-6pm | 1-2pm2 | 2-3pm2 | 3-4pm2 | 4-5pm2 | 5-6pm2 | 1-2pm | 2-3pm3 | 3-4pm3 | 4-5pm3 | 5-6pm3 |
| ------- | ----------------------- | ------------ | ------ | --------- | ------ | ----- | ----- | ----- | ----- | ----- | ------ | ------ | ------ | ------ | ------ | ----- | ------ | ------ | ------ | ------ |
| Person1 | Person1@DepartmentG.com | <1 year      | Level1 | If needed | Topic1 | 0     | 0     | 1     | 1     | 1     | 0      | 0      | 1      | 1      | 1      | 0     | 0      | 1      | 1      | 1      |
| Person2 | Person2@DepartmentN.com | 3-5 years    | Level2 | Yes       | Topic2 | 1     | 1     | 0     | 0     | 0     | 1      | 1      | 1      | 0      | 0      | 1     | 1      | 1      | 0      | 0      |
| Person3 | Person3@DepartmentK.com | 1-3 years    | Level2 | Yes       | Topic2 | 0     | 0     | 1     | 1     | 0     | 1      | 1      | 1      | 0      | 0      | 0     | 1      | 1      | 0      | 0      |
| Person4 | Person4@DepartmentN.com | 5-10 years   | Level3 | Yes       | Topic3 | 1     | 1     | 1     | 1     | 1     | 1      | 0      | 0      | 0      | 1      | 1     | 1      | 1      | 1      | 0      |
| Person5 | Person5@DepartmentL.com | 5-10 years   | Level3 | No        | Topic3 | 1     | 0     | 1     | 1     | 0     | 0      | 0      | 0      | 0      | 0      | 0     | 0      | 0      | 0      | 0      |

Fields:

- Name `<str>`: The name of the person (not necessary for SAAT)
- Email `<str>`: The email of the person for contact (not necessary for SAAT)
- Years_In_Org `<str/int>`: The number of years the person has spent in the organisation (optional)
- Grade `<str/int>`: The level of the individual in the organisation e.g. Manager, Director, etc (optional)
- Setup `<str>` {'Yes', 'No', 'If needed'}: Will the person facilitate setting up a meeting (optional)
- Topic `<str>`: The topic the person wants to discuss (not necessary for SAAT)
- Times e.g. 1-2pm `<int>` {0,1}: Can the person attend at the time specified (essential)

You can download this data on [github](https://github.com/samuelweller21/SAAT/tree/main/data).

