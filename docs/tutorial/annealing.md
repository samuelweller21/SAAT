---
hide:
  - toc
---

# Annealing

Next we need to set up the annealer.  For reference the annealing takes:

```py
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
```

We can now simply pass to SAAT from our dataframe in [Data](/tutorial/data):

```py
my_SAAT = SAAT.SAAT(
    times = data.loc[:,'1-2pm':'5-6pm3'], 
    group_size = 4, 
    organise = data["Setup"], 
    department = data["Department"], 
    time_in_company = data["Years_In_Org"])
```

<font size='2'> For more details on tuning the default weights see [Weights](/tutorial/weights). </font>

Next we need to tune all the simulated annealing parameters.  The underlying simulated annealing framework of SAAT ([SimAnneal](https://github.com/perrygeo/simanneal)) provides a hueristic which will do all the hard work for us.  All we need to specify is:

- steps: how many iterations it should spend tuning the parameters, default is 2,000
- minutes: how many minutes we want it to spend looking for a solution

```py
my_SAAT.set_schedule(my_SAAT.auto(minutes=0.1, steps=200))
```

<font size='2'> Testing tended to suggest conversion on a good minimum within 200 steps and just a couple of seconds for small group problems. </font>

Now run anneal which will return the optimal state and energy found:

```py
# random.seed(1)
state, e = my_SAAT.anneal()
```

You'll see the SimAnneal process logging as it runs.  Note, if you want reproducible results then you can simply set Python's random.seed.  Also note, g is the function which decides the group sizes to allocate, see the [Paper](/paper) for more details.