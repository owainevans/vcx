Ipython cell magic for venture
----------

1. Get IPython 1.x (latest stable version).

2. Copy vent_magic.py to IPython profile startup directory. Try following
at the terminal to get config: 
'ipython locate config'.

Then find the 'startup' folder. On my Ubuntu 1204 the full directory is:

~/.config/ipython/profile_default/startup


3. Cell magics are '%%vl' and '%%vp'. Currently one must use '%%vp', which 
converts as follows:

[ASSUME x 1] -> ripl.assume('x','1')

Note that OBSERVE only works when its first argument is a variable.



4. Code example:

In[1]:
%%vp
[clear]
[assume y (beta 1 5) ]
[assume z (flip y) ]
[observe z true]
[infer 100]
[predict y]

Out[1]: 
(['vxx.clear()',
  "vxx.assume('y','(beta 1 5)')",
  "vxx.assume('z','(and (flip y) (flip y))')",
  "vxx.observe('z','true')",
  'vxx.infer(100)',
  "vxx.predict('y')"],
 [None,
  (1, 0.10698417473901296),
  (2, False),
  3,
  None,
  (4, 0.4161203311540787)])




    
Notes:
1. Only works as cell magics (%%) and not as line magic (%). Could add line
magic later.

2. The 'vp' mode converts to Python method syntax:
[ASSUME x 1] -> self.ripl.assume('x','1')
This only works if square brackets are used for all and only directives and 
if observe only takes a variable as first argument (not an expression). 

Directives are ASSUME var exp, OBSERVE var exp , INFER int, CLEAR, PREDICT exp    . 

