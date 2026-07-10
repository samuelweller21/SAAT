# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.7
#   kernelspec:
#     display_name: Python 3.11
#     language: python
#     name: py311
# ---

# %%
import pandas as pd
import lib.SAAT as SAAT
import lib.utils as utils

# %%
# Read data
raw = pd.read_excel("data/sign_ups.xlsx")

# %%
# Drop empty columns
raw.drop(columns=['Email', 'Name'], inplace=True)

# %%
# Rename long columns
raw.rename(columns={
    "Work email address:": "Email",
    "Full name:": "Name"
},
inplace=True)

# %%
# Replace Free/Busy with 1/0
raw.replace("Busy", 0, inplace=True)
raw.replace("Free", 1, inplace=True)

# Infer department
raw['department'] = raw["Email"].map(lambda email: utils.email_to_department(email))

# %%
# Check for duplicates
duplicates = raw[raw['Email'].duplicated()]
if len(duplicates) > 0:
    raise Exception("Duplicate email found", duplicates[['Email', 'Name']])

# %%
# Separate out F2F and Online
name_to_grade_cols = list(raw.loc[:, 'Name':'Grade:'].columns)
F2F_cols = list(raw.loc[:, 'Location (City):':'4-5pm12'].columns)
online_cols = list(raw.loc[:, 'Would you be willing to set up an MS Teams call for your group? (the date and time will be provided for you)':'4-5pm3'].columns)
both_f2f_cols = list(raw.loc[:, '(F2F): Location (City):':'4-5pm9'].columns)
both_online_cols = list(raw.loc[:, '(ONLINE): Would you be willing to set up an MS Teams call for your group? (the date and time will be provided for you)':'4-5pm6'].columns)

F2F = raw[raw[registration_col] == 'Face-to-face (in a local hub)'][
  name_to_grade_cols + F2F_cols
]

Online = raw[raw[registration_col] == 'Online (via MS Teams)'][
    name_to_grade_cols + online_cols
]

Both_F2F = (raw[raw[registration_col] == 'Online AND Face-to-face'][
    name_to_grade_cols + both_f2f_cols
]).set_axis(name_to_grade_cols + F2F_cols, axis=1)

Both_Online = (raw[raw[registration_col] == 'Online AND Face-to-face'][
    name_to_grade_cols + both_online_cols 
]).set_axis(name_to_grade_cols + online_cols, axis=1)

# Join both sign ups together
F2F_all = pd.concat([F2F, Both_F2F], ignore_index=True)
Online_all = pd.concat([Online, Both_Online], ignore_index=True)

# %%
# Separate out topics
social_chat = Online_all[Online_all['Please choose a chat topic:'] == "Social chat (anything goes)"]
GWC_chat = Online_all[Online_all['Please choose a chat topic:'] == "GORS Work & The Community "]
CP_chat = Online_all[Online_all['Please choose a chat topic:'] == "Career Progression"]

# %%
social_chat.columns

# %%
# Allocate
my_SAAT = SAAT.SAAT(
    times = social_chat.loc[:,'1-2pm':'5-6pm3'], 
    group_size = 4, 
    organise = social_chat['Would you be willing to set up an MS Teams call for your group? (the date and time will be provided for you)'], 
    department = data["Department"], 
    time_in_company = data['How many years have you been in GORS?'],
    max_free_time_slot_goal=2)

my_SAAT.set_schedule(my_SAAT.auto(minutes=0.1, steps=200))
state, e = my_SAAT.anneal()

print('Energy maximised at: {}'.format(-e))
print('Final state: {}'.format(state))
