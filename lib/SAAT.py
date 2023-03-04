import math
import numpy as np
import random
from simanneal import Annealer
import random
import numpy as np
from termcolor import colored, cprint

def g(n, size):
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
        return g(n, size-1)

class SAAT(Annealer):

    # pass extra data into the constructor
    def __init__(self, times, group_size, organise = None, department = None, time_in_company = None):
        state = list(range(1,times.shape[0]+1))
        self.x = np.asarray(times)
        self.size = group_size
        self.organise = None if organise is None else np.asarray(organise)
        self.department = None if department is None else np.asarray(department)
        self.time_in_company = None if time_in_company is None else np.asarray(time_in_company)
        super(SAAT, self).__init__(state)  # important!
    
    def move(self):
        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)
        self.state[a], self.state[b] = self.state[b], self.state[a]

    def energy(self):
        # Recall:
        # g is our grouping function
        # x is our timeslot matrix [0,0,1 // 1,0,1 // 1,1,1]
        # size is our ideal group sizes
        
        grouping = np.array(g(len(self.state), self.size))
        number_of_groups = sum(grouping[1:])
        
        index = 0
        total_score = 0
        for i in range(number_of_groups):

            size_of_group = grouping[0] if i < grouping[1] else grouping[0] + 1

            group_ids = self.state[index:(index+size_of_group)]

            index = index + size_of_group

            # Subtract one from each
            group_ids = [x-2 for x in group_ids]
            
            # Retrieve from x
            y = self.x[group_ids, :]

            # Count number of matching columns
            count = 0
            for c in range(y.shape[1]):
                temp = 0
                if sum(y[:,c]) == y.shape[0]:
                    temp = temp + 1
                # If no free slots, give massive penalty
                if temp == 0:
                    temp = -3
                count = count + temp

            # Count total free slots
            slots_count = sum(sum(y))

            # Summation
            score = 5*count/slots_count
            total_score = total_score + score
            
            # Retrieve from organise
            if self.organise is not None:
                y = self.organise[group_ids]

                if ((1 in y) or ('Yes' in y)):
                    total_score = total_score + 1
                elif ((0.5 in y) or ('If needed' in y)):
                    total_score = total_score + 0.5
                
            # Retrieve from time_in_company
            if self.time_in_company is not None:
                total_score = total_score + len(np.unique(self.time_in_company[group_ids]))/len(self.time_in_company[group_ids])
            
            # Retrieve from department
            if self.department is not None:
                total_score = total_score + len(np.unique(self.department[group_ids]))/len(self.department[group_ids])
        
        return -total_score