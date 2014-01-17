Ipython cell magic for venture
----------

<ol><li> Get IPython 1.x (latest stable version).

<li>Copy vent_magic.py to IPython profile startup directory. Try following
at the terminal to get config: 
   ipython locate config

Then find the 'startup' folder. On my Ubuntu 1204 the full directory is:

      ~/.config/ipython/profile_default/startup

If you now open a new IPython terminal, you should get this  message:

   VentureMagics is active: see %vl? for docs



<li>Basic examples can be found in the venture_magic_demo_vl.ipynb notebook 
or in the corresponding .html file. You can also use %vl? in the terminal.