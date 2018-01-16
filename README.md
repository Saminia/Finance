# Finance

#pv.py
- This widget calculates the present value for series of future cash flows. 
- PV=CashFlow/(1+InterestRate x Compouding)^(Compouding x (TimePeriod-I))
- I is an indicator function where gets the value of 0 if the payments are at the "end" and value of 1 if the payments are in the "begining".
- The total Present value is obtained by summation over all present values for all cash flows. 


