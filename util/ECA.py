# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 20:21:50 2019

@author: Qin Lei
"""

import numpy as np

class ECA:
    
    def __init__(self, rule, init_state='0'*50+'1'+'0'*50,alpha=1.0, d_ini=0.5, k=0, Ttrs=0, Tsample=100, run_num=100, ConvergeMode=0):
        """Initialize the CA with the given rule and initial state."""
        self.binary = f'{rule:08b}'        # transform the rule number to a binary code (Example: rule 90 is 01011010 in binary code)
        self.rule = rule
        self.dict= {                       # make a dictionary to store the 8 possible pairs of 3 neighbourhood elements (with values 1 and 0)
          "111": (self.binary[0]),         # assign to each key, a value equivalent to a character from the binary code (from index 0 to index 7)
          "110": (self.binary[1]),
          "101": (self.binary[2]),
          "100": (self.binary[3]),
          "011": (self.binary[4]),
          "010": (self.binary[5]),
          "001": (self.binary[6]),
          "000": (self.binary[7])
        }
        # for ring data
        self.init_state = init_state
        self.n_cell = len(init_state)
        
        self.current_state = ""
        self.run_num = run_num
        self.alpha = alpha
        self.d_ini = d_ini
        self.k = k
        self.n_1 = []
        self.n_1.append(self.init_state.count('1'))
        self.space = []
        #self.space.append(self.init_state[-1] + self.init_state + self.init_state[0])
        self.space.append(self.init_state)
        # paramters for convergence
        self.ConvergeMode = ConvergeMode
        if self.ConvergeMode == 1 or self.ConvergeMode == 2 :
            self.runStop = False
            self.K_stop = int(1 / self.alpha)
        
        self.Ttrs = Ttrs
        self.Tsample = Tsample
        
        
        
    def printDict(self):
        print(self.dict)

    def __state(self):
        """Returns the current state."""
        return self.current_state

    def __asyNext(self):
        self.init_state = self.init_state[-1] + self.init_state + self.init_state[0]
        self.current_state = ''
        group = ''
        for i in range(1, len(self.init_state) - 1):
            
            randNum = np.random.random()
            
            #print("turn "+str(i)+": ECA the randNum is "+ str(randNum))
            
            if randNum >= self.alpha:
                self.current_state += self.init_state[i]
            else:
                for j in range(i - 1, i + 2):               # get groups of 3 elements (left, center, right)
                    group += self.init_state[j]             # add elemnts to group
                #             print(group)
                self.current_state += self.dict[
                    group]                          # add value (1 or 0) in self.current_state, after corresponding dictionary value of the 3 group characters
                group = '' 
        
        
        # consider the convergence 
        if self.ConvergeMode == 1:
            if len(self.space) >= self.K_stop:
                K_sliced = self.space[-self.K_stop:]
                K_sliced.append(self.current_state)
                if len(set(K_sliced)) == 1:
                    self.runStop = True
                    self.init_state = self.__state()        # prepare self.init_state for next itteration
                    return self.current_state
                
        if self.ConvergeMode == 2:
            if self.__SyncNext(self.current_state) == self.current_state:
                self.runStop = True
                self.init_state = self.__state()        # prepare self.init_state for next itteration
                return self.current_state
            
            
        self.n_1.append(self.current_state.count('1'))
        self.space.append(self.current_state)
        
        self.init_state = self.__state()        # prepare self.init_state for next itteration
        return self.current_state
    
    def __SyncNext(self, config):
        config = config[-1] + config + config[0]
        current_state = ""
        group = ''
        for i in range(1, len(config) - 1):
            for j in range(i - 1, i + 2):               # get groups of 3 elements (left, center, right)
                group += config[j]             # add elemnts to group
            current_state += self.dict[group]                          # add value (1 or 0) in self.current_state, after corresponding dictionary value of the 3 group characters
            group = '' 
        return current_state
        

    def run(self, isPrint = True):
        """Progress and print num states.
        0s are replaced by spaces, and 1s are replaced by * for pretty printing."""
        if isPrint is True:
            print(self.init_state.replace("0", " ").replace("1", "*"))        # print the first line
        for i in range(1, self.run_num):
            if isPrint is True:    
                print(self.__asyNext().replace("0", " ").replace("1", "*"))
            else:
                self.__asyNext()
            
            if self.ConvergeMode == 1 or self.ConvergeMode == 2 :
                if self.runStop:
                    break
       
    
    def getu(self):
        #run_num 个时间的密度 den 
        den = np.array(self.n_1) / self.n_cell
        u = 1.0/self.Tsample * den[self.Ttrs:self.Ttrs+self.Tsample].sum()
        
        return u
    
    def reset(self, **kargs):
        if "alpha" in kargs.keys():
            
            self.alpha = kargs['alpha']
            
        if "init_state" in kargs.keys():
            
            self.init_state = kargs['init_state']
            self.n_cell = len(self.init_state) + 2
            
        if "rule" in kargs.keys():
            rule = kargs['rule']
            self.binary = f'{rule:08b}'       
            self.dict= {                      
                    "111": (self.binary[0]),      
                    "110": (self.binary[1]),
                    "101": (self.binary[2]),
                    "100": (self.binary[3]),
                    "011": (self.binary[4]),
                    "010": (self.binary[5]),
                    "001": (self.binary[6]),
                    "000": (self.binary[7])
                    }
        if "run_num" in kargs.keys():
            self.run_num = kargs['run_num']
        
        # clear and re assign
        
        self.current_state = ""
        
        self.n_1 = []
        self.n_1.append(self.init_state.count('1'))
        self.space = []
        self.space.append(self.init_state)
    
    
def getInitState(n_cell, d_ini):
    init_state = ''
    for i in range(0, n_cell):
        rand = np.random.rand()
        if rand >= d_ini:
            init_state += '0'
        else:
            init_state += '1'
    return init_state

if __name__ == '__main__':
    ca = ECA(50)
    ca.printDict()
    ca.run()
