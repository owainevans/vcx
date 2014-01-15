from IPython.core import display
import numpy as np  

try:
    from IPython.core.magic import (Magics,register_cell_magic, magics_class, line_magic,
                                    cell_magic, line_cell_magic)
except:
    from IPython.core.magic import (register_cell_magic, magics_class, line_magic,
                                    cell_magic, line_cell_magic)                           

try: 
    from venture.shortcuts import *
    print 'found v.shortcuts'    
except:
    try:
        import venture.engine as v2
        print 'found veng'
    except:
        print 'no venture found'                              
    
class MakeFakeRIPL:
    def __init__(self):
        self.id = np.random.randint(10**4)
        self.direcs = {'id':self.id}
        self.direc_count = 0
        print 'Made FakeRIPL, id: %i' % self.id
        
    def add(self,directive):
        tag,arglist = directive
        #if arglist[0] in [self.direcs[k][0] for k in self.direcs.keys() if k[0]=='a']:
        #    print 'Attempt to define same var twice!'
        self.direcs[tag+str(self.direc_count)] = arglist
        self.direc_count += 1
        return None
        
    def vreport(self):
        print 'venture ripl id: %i' % self.id; print self.direcs
        return None
        
    def assume(self,variable,exp):
        #print 'V %i' % self.id
        #print 'ASSUME '+str(variable)+' '+str(exp)
        self.add(('assume',[variable,exp] ) )
        return variable,exp
    
    def observe(self,exp1,exp2):
        #print 'V %i' % self.id
        #print 'obs '+ str(exp1)+'   '+str(exp2)
        self.add(('observe',[exp1,exp2] ) )
        return exp1,exp2
        
    def predict(self,exp):
        #print 'pred '+ str(exp)
        self.add(('predict',[exp] ) )
        return exp
        
    def infer(self,exp):
        #print 'inf '+ str(exp)
        self.add(('infer',[exp] ) )
        return exp
        
    def clear(self):
        #print 'clear'
        self.direcs.clear(); self.direc_count = 0
        return None
        
    
        
    
    
@magics_class
class VentureMagics(Magics):

    def __init__(self, shell):
        super(VentureMagics, self).__init__(shell)
        
        self.v = MakeFakeRIPL()  # always make fake ripl
        self.vent_state = 'no vent'
        
        try:
            self.vxx = make_church_prime_ripl()
            self.vent_state = 'vxx'
        except:
            try:
                self.v2 = v2
                self.vent_state = 'v2'
            except:
                print 'no vent instance created'
    
    
    @line_cell_magic
    def vp(self, line, cell=None):
        
        if cell is None:
            
            py_lines = self.cell_to_venture(line)
            fake_outs = eval(py_lines[0])
            
            if self.vent_state == 'vxx':
                vouts = eval(py_lines[0].replace('self.v.','self.vxx.'))
            
            if self.vent_state == 'v2':
                vouts = eval(py_lines[0].replace('self.v.','self.v2.'))
                
            print vouts  # just to see venture output on loops
            return py_lines[0].replace('self.v.','vxx.'), vouts
            
            
        else:
            return self.cell_vp(line,cell)
            
                
    @cell_magic
    def cell_vp(self, line, cell):
        
        terse=0
        if line:
            if line.lower().strip().find('as') > -1: terse=1 
        
        # code in v.assume py form
        py_lines = self.cell_to_venture(cell,terse) 
        
        fake_outs = [];
        for py_line in py_lines:
            fake_outs.append( eval(py_line) )
        
        if self.vent_state == 'vxx':
            vxx_outs = []
            for py_line in py_lines:
                vxx_outs.append( eval(py_line.replace('self.v.','self.vxx.')) )
            vouts = vxx_outs  
        
        if self.vent_state == 'v2':
            v2_outs = []
            for py_line in py_lines:
                v2_outs.append( eval(py_line.replace('self.v.','self.v2.')) )  
            vouts = v2_outs                        
        
        # output the converted lines that are fed to python        
        py_lines_clean = [py_line.replace('self.v.','vxx.') for py_line in py_lines]
       
       #verbose mode (extra output)
        if line.lower().strip() == '-v':
            return 'cell:',cell,'\n py_lines:', py_lines,'\n fake_outs:',fake_outs,'\n vouts:',vouts                                                         
        
        #non_verbose mode
        else:
            return py_lines_clean,vouts
        
                                                               
                                                                        
    @cell_magic
    def vl(self, line, cell):
        
        py_lines = self.cell_to_venture(cell)
        
        fake_outs = [];
        for py_line in py_lines:
            fake_outs.append( eval(py_line) )
        
        if self.vent_state == 'vxx':
            vxx_outs = []
            for py_line in py_lines:
                vxx_outs.append( eval(py_line.replace('self.v.','self.vxx.')) )
            vouts = vxx_outs  
        
        if self.vent_state == 'v2': 
            vouts = self.v2.load(cell)                        
       
       #verbose mode
        if line.lower().strip() == '-v':
            return 'cell:',cell,'cell2ven:', py_lines,'fake_outs:',
            fake_outs,'%s' % self.vent_state,'vouts:',vouts                                                         
        else:
            return '%s' % self.vent_state,vouts
            
                                                                                            
                                                                                                                                                                                                                                                            
    def remove_white(self,s):
        t=s.replace('  ',' ')
        return s if s==t else self.remove_white(t)
        
        
    def cell_to_venture(self,s,terse=0):
        """Converts vchurch to python self.v.assume (OBSERVE is broken)"""
        s = str(s)
        s = s[:s.rfind(']')]
        ls = s.split(']')
        ls = [ self.remove_white(line.replace('\n','')) for line in ls]
        v_ls = []
        
        for line in ls:
            if terse==1: line = '[ASSUME '+line[1:]
            
            lparen = line.find('[')        
            tag = line[ lparen+1: ].split()[0].lower()
            
            if tag=='assume':
                var=line[1:].split()[1]
                exp = ' '.join( line[1:].split()[2:] )
                v_ls.append( "self.v.assume('%s','%s')" % ( var, exp ) )
                
            elif tag=='observe':
                var=line[1:].split()[1]
                exp = ' '.join( line[1:].split()[2:] )
                v_ls.append( "self.v.observe('%s','%s')" % ( var, exp ) )
            
            elif tag=='predict':
                exp = ' '.join( line[1:].split()[1:] )
                v_ls.append( "self.v.predict('%s')" % exp  )
                
            elif tag=='infer':
                num = line[1:].split()[1]
                v_ls.append( "self.v.infer(%i)" % int(num) )
            
            elif tag=='clear':
                v_ls.append( "self.v.clear()" )
            
            else:
                assert 0==1,"Did not recognize directive"
        
        return v_ls
    
    
    
    
    
    ## for ipythonNB, remove function defintion and uncomment following two lines
def load_ipython_extension(ip):
    """Load the extension in IPython."""
    ip.register_magics(VentureMagics)

try:
    ip = get_ipython()
    ip.register_magics(VentureMagics)
    print 'ip=get_ipython() ran'
except:
    print 'ip=get_ipython() didnt run'   

print 'VentureMagics is active'