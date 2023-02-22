import math
import pandas as pd
import numpy as np
import random
from simanneal import Annealer
import random
import numpy as np
import re
from termcolor import colored, cprint
import warnings
warnings.simplefilter('ignore', FutureWarning)

def standard_g(n, size):
        #Strategy: Assign groups of size g or g+1, if that fails reduce group size by 1 and try again

        # Begin by trying to maximise the number of groups of size g i.e. a in a*g + b*(g+1) = n
        a = math.floor(n/size)

        # Then decrease a until a sufficient b is found
        b = 0
        # If a goes negative try a smaller group size (won't affect large n, small size)
        while(a >= 0):
            if (a*size + b*(size+1)) == n:
                return [size,a,b]
            elif (a*size + b*(size+1)) > n:
                a = a - 1
                b = 0
            else:
                b = b + 1
        else:
            return standard_g(n, size-1)

def results_to_csv(state, data, group_size, name='Allocation.csv', g=standard_g):
    grouping = np.array(g(len(state), group_size))
    number_of_groups = sum(grouping[1:])
    
    df = pd.DataFrame(columns=data.columns)

    index = 0
    for i in range(number_of_groups):

        size_of_group = grouping[0] if i < grouping[1] else grouping[0] + 1

        group_ids = state[index:(index+size_of_group)]

        index = index + size_of_group

        # Subtract one from each
        group_ids = [x-1 for x in group_ids]
        
        # Retrieve from data
        y = data.iloc[group_ids, :]
        df = df.append(y)
        df = df.append(pd.Series(), ignore_index=True)

    df.to_csv(name, index=False)

def email_to_department(email):
    email = email[email.index("@")+1:]
    email = email[0:email.index(".")]
    return email.lower()

def generate_data(n, m):
    # n is number of people
    # m is timeslots
    data = np.arange(n*m).reshape(n,m)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            data[i,j] = random.randint(0,1)
    return data

def pad(x):
    return str(x) + " "

def test(x):
    return x+1

    
def get_color(x):
    if (x == 0):
        return "\033[1;41;41m 0"
    else:
        return "\033[1;42;42m 1"

def print_pretty_allocations(state, times, group_size, g = standard_g, extras = None):
    x = np.asarray(times)
    size = group_size
    digits = math.floor(round(math.log(len(state)-1,10),5)) + 1
    grouping = np.array(g(len(state), size))
    number_of_groups = sum(grouping[1:])

    index = 0
    for i in range(number_of_groups):

        size_of_group = grouping[0] if i < grouping[1] else grouping[0] + 1

        group_ids = state[index:(index+size_of_group)]

        index = index + size_of_group
        
        # Subtract one from each
        group_ids = [x-1 for x in group_ids]
        
        # Retrieve from x
        y = x[group_ids, :]
        
        if extras is not None:
            extra = extras.iloc[group_ids, :]
        
        print()
        
        for j in range(y.shape[0]):

            # Pad string for pretty formatting
            s = str(group_ids[j]+1)
            for i in range(int(digits - math.floor(math.log(group_ids[j]+1 if group_ids[j]+1 > 0 else 1,10)))-1):
                s = pad(s)
            
            
            # Add colours to make pretty
            for c in range(y[j,:].shape[0]):
                s = s + get_color(y[j,c])
            s = s + "\033[0m"
            
            if extras is not None:
                # Add extras
                for c in range(extra.iloc[j].shape[0]):
                    s = s + " ---- " + str(extra.iloc[j,c])
            
            print(s)
            
# def print_pretty_allocations(state, x, g, size, extras=None):
#     digits = math.floor(round(math.log(len(state)-1,10),5)) + 1
#     print("Digits: " + str(digits))
#     grouping = np.array(g(len(state), size))
#     number_of_groups = sum(grouping[1:])

#     index = 0
#     for i in range(number_of_groups):

#         size_of_group = grouping[0] if i < grouping[1] else grouping[0] + 1

#         group_ids = state[index:(index+size_of_group)]

#         index = index + size_of_group

#         # Subtract one from each
#         group_ids = [x-1 for x in group_ids]
        
#         # Retrieve from x
#         y = x[group_ids, :]
        
#         if extra != None:
#             extra = extras.iloc[group_ids, :]
        
#         print()
        
#         for j in range(y.shape[0]):

#             # Pad string for pretty formatting
#             s = str(group_ids[j])
#             for i in range(int(digits - math.floor(math.log(group_ids[j] if group_ids[j] > 0 else 1,10)))-1):
#                 s = pad(s)
            
            
#             # Add colours to make pretty
#             for c in range(y[j,:].shape[0]):
#                 s = s + get_color(y[j,c])
#             s = s + "\033[0m"
            
#             if extra != None:
#             # Add extras
#                 for c in range(extra.iloc[j].shape[0]):
#                     s = s + " ---- " + str(extra.iloc[j,c])
            
#             print(s)