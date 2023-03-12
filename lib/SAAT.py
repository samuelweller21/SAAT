import math
import numpy as np
import random
from simanneal import Annealer
import random
import numpy as np
import lib.utils as utils

class SAAT(Annealer):

    def __init__(self, 
                 times, 
                 group_size, 
                 times_wt = 1, 
                 organise_wt = 0.5, 
                 time_in_company_wt = 0.5,
                 department_wt = 0.25,
                 no_time_penalty_wt = 0.5,
                 organise = None, 
                 department = None, 
                 time_in_company = None, 
                 g = None):
        
        if no_time_penalty_wt < 0 or no_time_penalty_wt > 1:
            raise Exception("no_time_penalty_weight must be between 0 and 1")
        
        state = list(range(1,times.shape[0]+1))
        self.x = np.asarray(times)
        self.size = group_size
        self.g = utils.standard_g if g is None else g
        self.organise = None if organise is None else np.asarray(organise)
        self.department = None if department is None else np.asarray(department)
        self.time_in_company = None if time_in_company is None else np.asarray(time_in_company)
        self.times_wt = times_wt*group_size
        self.organise_wt = organise_wt
        self.time_in_company_wt = time_in_company_wt
        self.department_wt = department_wt
        self.no_time_penalty_wt = no_time_penalty_wt
        self.copy_strategy = "slice"
        super(SAAT, self).__init__(state)
    
    def move(self):
        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)
        self.state[a], self.state[b] = self.state[b], self.state[a]

    def energy(self, logging=False):
        grouping = np.array(self.g(len(self.state), self.size))
        number_of_groups = sum(grouping[1:])
        
        index = 0
        total_score = 0
        
        if logging:
            print('Numer of groups: {}'.format(number_of_groups))
        
        for i in range(number_of_groups):
            
            local_score = 0
            
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
            
            # Count total free slots
            slots_count = sum(sum(y))
            
            # Summation
            score = count/slots_count
            local_score = local_score + score*self.times_wt
            
            if logging:
                print('Current total score after free slots: {}'.format(total_score))
                print('Score: {}, Slots: {}, Count: {}'.format(score, slots_count, count)) 
            
            # Retrieve from organise
            if self.organise is not None:
                y = self.organise[group_ids]

                if ((1 in y) or ('Yes' in y)):
                    local_score = local_score + 1*self.organise_wt
                elif ((0.5 in y) or ('If needed' in y)):
                    local_score = local_score + 0.5*self.organise_wt
                
            if logging:
                print('Current total score after organise: {}'.format(total_score))
                
            # Retrieve from time_in_company
            if self.time_in_company is not None:
                local_score = local_score + self.time_in_company_wt * len(np.unique(self.time_in_company[group_ids])) / len(self.time_in_company[group_ids])
            
            if logging:
                print('Current total score after time in org: {}'.format(total_score))
            
            # Retrieve from department
            if self.department is not None:
                local_score = local_score + self.department_wt * len(np.unique(self.department[group_ids])) / len(self.department[group_ids])
                
            if logging:
                print('Current total score after department: {}'.format(total_score))
                
            if logging:
                utils.print_pretty_allocations(self.state, self.x, self.size)
                
            # If no free slots, give penalty
            if count == 0:
                local_score = local_score*(1-self.no_time_penalty_wt)
                
            total_score = total_score + local_score
        
        return -total_score