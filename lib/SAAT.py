import math
import numpy as np
import random
from simanneal import Annealer
import random
import numpy as np
from termcolor import colored, cprint
import lib.utils as utils

class SAAT(Annealer):

    # pass extra data into the constructor
    def __init__(self, times, group_size, organise = None, department = None, time_in_company = None, g = None):
        state = list(range(1,times.shape[0]+1))
        self.x = np.asarray(times)
        self.size = group_size
        self.g = utils.standard_g
        self.organise = None if organise is None else np.asarray(organise)
        self.department = None if department is None else np.asarray(department)
        self.time_in_company = None if time_in_company is None else np.asarray(time_in_company)
        super(SAAT, self).__init__(state)  # important!
    
    def move(self):
        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)
        self.state[a], self.state[b] = self.state[b], self.state[a]

    def energy(self, logging=False):
        # Recall:
        # g is our grouping function
        # x is our timeslot matrix [0,0,1 // 1,0,1 // 1,1,1]
        # size is our ideal group sizes
        
        grouping = np.array(self.g(len(self.state), self.size))
        number_of_groups = sum(grouping[1:])
        
        index = 0
        total_score = 0
        
        if logging:
            print('Numer of groups: {}'.format(number_of_groups))
        
        for i in range(number_of_groups):
            
            if logging:
                print('Group: {}'.format(i))

            size_of_group = grouping[0] if i < grouping[1] else grouping[0] + 1

            group_ids = self.state[index:(index+size_of_group)]

            index = index + size_of_group

            # Subtract one from each
            group_ids = [x-1 for x in group_ids]
            
            # Retrieve from x
            y = self.x[group_ids, :]

            # Count number of matching columns
            count = 0
            for c in range(y.shape[1]):
                if sum(y[:,c]) == y.shape[0]:
                    count = count + 1
            
            # If no free slots, give massive penalty
            if count == 0:
                count = -y.shape[1]/3
            
            # Count total free slots
            slots_count = sum(sum(y))
            
            # Summation
            score = 15*count/slots_count
            total_score = total_score + score
            
            if logging:
                print('Current total score after free slots: {}'.format(total_score))
                print('Score: {}, Slots: {}, Count: {}'.format(score, slots_count, count)) 
            
            # Retrieve from organise
            if self.organise is not None:
                y = self.organise[group_ids]

                if ((1 in y) or ('Yes' in y)):
                    total_score = total_score + 1
                elif ((0.5 in y) or ('If needed' in y)):
                    total_score = total_score + 0.5
                
            if logging:
                print('Current total score after organise: {}'.format(total_score))
                
            # Retrieve from time_in_company
            if self.time_in_company is not None:
                total_score = total_score + len(np.unique(self.time_in_company[group_ids]))/len(self.time_in_company[group_ids])
            
            if logging:
                print('Current total score after time in org: {}'.format(total_score))
            
            # Retrieve from department
            if self.department is not None:
                total_score = total_score + len(np.unique(self.department[group_ids]))/len(self.department[group_ids])
                
            if logging:
                print('Current total score after department: {}'.format(total_score))
                
            if logging:
                utils.print_pretty_allocations(self.state, self.x, self.size)
        
        return -total_score