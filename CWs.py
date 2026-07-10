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
# Run utility
def run_CW_SAAT(df, start_col, end_col, output_to, group_size=5, extras=(2,6), organise_col="Would you be willing to set up an MS Teams call for your group? (the date and time will be provided for you)"):
    if len(df) > group_size:
        # Allocate SO
        my_SAAT = SAAT.SAAT(
            times = df.loc[:,start_col:end_col], 
            group_size = 5, 
            organise = df[organise_col], 
            department = df["Department"], 
            time_in_company = df['How many years have you been in GORS?'],
            max_free_time_slot_goal=1)
        my_SAAT.set_schedule(my_SAAT.auto(minutes=0.2, steps=200))
        state, e = my_SAAT.anneal()
        print('Energy maximised at: {}'.format(-e))
        print('Final state: {}'.format(state))
        print('Allocation: ' + str(state))
        print('Energy maximised at: ' + str(-e))
        utils.print_pretty_allocations(
            state = state, 
            times = df.loc[:,start_col:end_col], 
            group_size = 5,
            extras = df.iloc[:,extras[0]:extras[1]])
        utils.results_to_csv(
            state = state,
            data = df,
            group_size = group_size,
            name='results/' + output_to + ".csv")
    else:
        df.to_csv("results/" + output_to + ".csv")


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
raw['Department'] = raw["Email"].map(lambda email: utils.email_to_department(email))
raw.insert(6, 'Department', raw.pop('Department'))

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

F2F = raw[raw['Are you registering for:'] == 'Face-to-face (in a local hub)'][
  name_to_grade_cols + F2F_cols
]

Online = raw[raw['Are you registering for:'] == 'Online (via MS Teams)'][
    name_to_grade_cols + online_cols
]

Both_F2F = (raw[raw['Are you registering for:'] == 'Online AND Face-to-face'][
    name_to_grade_cols + both_f2f_cols
]).set_axis(name_to_grade_cols + F2F_cols, axis=1)

Both_Online = (raw[raw['Are you registering for:'] == 'Online AND Face-to-face'][
    name_to_grade_cols + both_online_cols 
]).set_axis(name_to_grade_cols + online_cols, axis=1)

# Join both sign ups together
F2F_all = pd.concat([F2F, Both_F2F], ignore_index=True)
Online_all = pd.concat([Online, Both_Online], ignore_index=True)

# %%
# Separate out topics
social_chat = Online_all[Online_all['Please choose a chat topic:'] == "Social chat (anything goes)"]
GWC = Online_all[Online_all['Please choose a chat topic:'] == "GORS Work & The Community"]
CP = Online_all[Online_all['Please choose a chat topic:'] == "Career Progression"]

# %%
# F2F
print("Find London locations: ", F2F_all['Location (City):'].unique())
london_list = ['Lonond', 'London (Westminster)', 'Westminster', 'London']
F2F_london = F2F_all[F2F_all['Location (City):'].isin(london_list)]
F2F_rest_of_UK = F2F_all[~F2F_all['Location (City):'].isin(london_list)]

# %%
# Run allocations
run_CW_SAAT(social_chat, '12-1pm (lunch slot)', '4-5pm3', "SC")
run_CW_SAAT(GWC, '12-1pm (lunch slot)', '4-5pm3', "GWC")
run_CW_SAAT(CP, '12-1pm (lunch slot)', '4-5pm3', "CP")
run_CW_SAAT(F2F_london, '12-1pm (lunch slot)10', '4-5pm12', "LondonF2F", organise_col='Would you be willing to organise a meeting location for your group (e.g. room in your building / local coffee shop - the date and time will be provided for you)?')

# %%
# Collect and output allocations
GWC = pd.read_csv("results/GWC.csv")
SC = pd.read_csv("results/SC.csv")
CP = pd.read_csv("results/CP.csv")
LondonF2F = pd.read_csv("results/LondonF2F.csv")
F2F_rest_of_UK

with pd.ExcelWriter("results/all_results.xlsx", engine="openpyxl") as writer:
    GWC.to_excel(writer, sheet_name="GWC", index=False)
    SC.to_excel(writer, sheet_name="SC", index=False)
    CP.to_excel(writer, sheet_name="CP", index=False)
    LondonF2F.to_excel(writer, sheet_name="LondonF2F", index=False)
    F2F_rest_of_UK.to_excel(writer, sheet_name="RestOfUK_F2F", index=False)
