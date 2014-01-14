Ipython cell magic for venture
----------

1. Get IPython 1.x (latest stable version).

2. Copy vent_magic.py to IPython profile startup directory. Try following
at the terminal:
ipython locate config

3. Cell magics are '%%vl' and '%%vp'. Currently must use 'vp' as it converts
as follows:
[ASSUME x 1] -> self.ripl.assume('x','1')



Notes:
1. Only works as cell magics (%%) and not as line magic (%). Could add line
magic later.

2. The 'vp' mode converts to Python method syntax:
[ASSUME x 1] -> self.ripl.assume('x','1')
This only works if square brackets are used for all and only directives and 
if observe only takes a variable as first argument (not an expression). 

Directives are ASSUME var exp, OBSERVE var exp , INFER int, CLEAR, PREDICT exp. 

