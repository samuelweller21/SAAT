---
hide:
  - toc
---

# Weights

The suggested method of using SAAT is with ```my_SAAT.set_schedule(my_SAAT.auto(minutes=0.1, steps=200))``` along with the default weights in ````__init__```.

If, however, you need greater performance the first thing to try is increasing the annealing time e.g. to:

```my_SAAT.set_schedule(my_SAAT.auto(minutes=1, steps=2000))```

If this doesn't yield better results it's unlikely longer anneal times will perform better.  Instead you may need to identify the nature of the algorithm's poor performance.  (Note, if you are getting groups without any free slots first consider if it's possible to allocate such a group).

SAAT uses a system where all weights are between 0 and 1.  The defaults are:

```py
times_wt = 1
organise_wt = 0.5
time_in_company_wt = 0.5
department_wt = 0.25
no_time_penalty_wt = 0.5
```

If you want a better mix of departments then maybe try incrasing department_wt to 0.75.  Alternatively, if you want to further avoid groups being allocated with no free slots increase the no_time_penalty_wt to 0.8  

<font size="2"> Note, technically weights > 1 can be used but keeping all weights [0,1] mkes things most intuitive </font>