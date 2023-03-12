---
hide:
  - toc
---

# Welcome to SAAT

SAAT (Simulated Annealing Allocation Tool) is a tool intended to optimise the allocation of individuals into groups across teams within an organisation.

## Purpose

Suppose we have some employees who want to learn more about their organisation.  Some know about HR, some finance, some marketing and others logistics.  The CEO decides the best way to do this is to put them into groups and get them to talk to one another.  Each employee has their specialism and diary as below: 

| Employee | Specialism | 1pm | 2pm | 3pm |
| -------- | ---------- | --- | --- | --- |
| Dave | Finance | Busy | - | - |
| Janette | Logistics | - | Busy | Busy |
| John | HR | - | Busy | - |
| ... | ... | | ... |

Ideally, the groups would have a good mix of specialisms, all be about the same size and have as many time slots in which the group can meet.  For large numbers, it's not trivial how to best allocate employees into groups; this is the problem which SAAT approaches.

## Quickstart

```py
# Initialise SAAT
my_SAAT = SAAT.SAAT(
    times = data.loc[:,'1-2pm':'5-6pm3'], 
    group_size = 4, 
    organise = data["Setup"], 
    department = data["Department"], 
    time_in_company = data["Years_In_Org"])

my_SAAT.set_schedule(my_SAAT.auto(minutes=0.1, steps=200))

#Run
# random.seed(1)
state, e = my_SAAT.anneal()

print('Energy maximised at: {}'.format(-e))
print('Final state: {}'.format(state))
```

See [Tutorial](tutorial/data) section for more information or [Demo](https://github.com/samuelweller21/SAAT/blob/main/Demo.ipynb) for a notebook example.
