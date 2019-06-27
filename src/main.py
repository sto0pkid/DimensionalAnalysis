from sympy import *
from IPython.display import display, Math
from functools import partial
import numbers

def sg_fold_op(f,z,l):
    if len(l) == 0:
        return z
    elif len(l) == 1:
        return l[0]
    else:
        return f(l[0],sg_fold_op(f,z,l[1:]))
    
class Tree:
    def __init__(self,data=None,children=[]):
        self.data = data
        self.children = children
    def __str__(self):
        return str(self.data) + str(self.children)

def tree_map(m,t):
    if type(t) is Tree:
        if t.data is None:
            r = list(map(lambda child: tree_map(m,child),t.children))
            return r
        if t.data in m:
            r = m[t.data](*map(lambda child: tree_map(m,child),t.children))
            return r
        else:
            r = m['default'](*map(lambda child: tree_map(m,child),t.children))
            return r
    else:
        r = m['default'](t)
        return r

class Unit:
    def __init__(self,val={},order=None):
        self.val = {}
        if val:
            for k,v in val.items():
                if not v == 0:
                    self.val[k] = v
    
    def __mul__(self,other):
        if not type(other) is Unit:
            if other is 1:
                return self * Unit()
            else:
                raise TypeError
        res = Unit()
        for k,v in self.val.items():
            if k in other.val:
                val = v + other.val[k]
                if val != 0:
                    res.val[k] = val
            else:
                res.val[k] = self.val[k]
        for k,v in other.val.items():
            if not k in self.val:
                res.val[k] = other.val[k]
        return res
    
    def __rmul__(self,other):
        if not isinstance(other,numbers.Number):
            raise TypeError
        return Quantity(other,self)
    
    def __truediv__(self,other):
        if not type(other) is Unit:
            if other is 1:
                return self / Unit()
            else:
                raise TypeError
            
        res = Unit()
        for k,v in self.val.items():
            if k in other.val:
                val = v - other.val[k]
                if val != 0:
                    res.val[k] = val
            else:
                res.val[k] = self.val[k]
        for k,v in other.val.items():
            if not k in self.val:
                res.val[k] = -v
        return res
    
    def __add__(self,other):
        if self != other:
            raise ValueError
        else:
            return Unit(self.val)
        
    def __sub__(self,other):
        if self != other:
            raise ValueError
        else:
            return Unit(self.val)
    
    def __pow__(self,other):
        if not type(other) is int:
            raise TypeError
        res = Unit()
        for k,v in self.val.items():
            res.val[k] = v * other
        return res
    
    __xor__ = __pow__
    
    def __eq__(self,other):
        if not type(other) is Unit:
            return False
        for k,v in self.val.items():
            if not k in other.val:
                return False
            if v != other.val[k]:
                return False
        return True
    
    def ast_separate(self):
        pos = []
        neg = []
        for k,v in self.val.items():
            if v > 0:
                pos.append((k,v))
            elif v < 0:
                neg.append((k,-v))
        return (pos,neg)
    def ast_fractional(self):
        pos,neg = ([Tree('exp',[k,v]) for k,v in l] for l in self.ast_separate())
        
        return Tree('frac',[Tree('prod',pos),Tree('prod',neg)])
    
                
    def ast(self):
        if not self.val:
            return 1
        else:
            pos = []
            neg = []
            for k,v in self.val.items():
                if v > 0:
                    pos.append((k,v))
                elif v < 0:
                    neg.append((k,-v))
                else:
                    assert False
            pos = [Tree('exp',[k,v]) if v != 1 else k for k,v in pos] 
            neg = [Tree('exp',[k,v]) if v != 1 else k for k,v in neg]
            if neg:
                num = Tree('prod',pos) if len(pos) > 1 else (pos[0] if pos else 1)
                den = Tree('prod',neg) if len(neg) > 1 else neg[0]
                return Tree('frac',[num,den])
            else:
                return Tree('prod',pos)
        
    def __str__(self):
        str_map = {
            'frac': lambda x, y: x + "/" + y,
            'exp': lambda x, y: x + "^" + y,
            'prod': lambda *x: "*".join(x),
            'default':str
        }
        
        return tree_map(str_map,self.ast())
    
    def latex(self):
        latex_map = {
            'default': lambda *x : x,
        }
        return tree_map(latex_map,self.ast())
        
    def to_sympy(self):
        sympy_map = {
            'frac': lambda x, y: x/y,
            'exp': lambda x, y: Pow(x,y,evaluate=False),
            'prod': lambda *x: sg_fold_op(lambda a, b: Mul(a,b,evaluate=False),1,x),
            'default': lambda x : x if type(x) is int \
                                    else Symbol(x) if type(x) is str \
                                    else x 
        }
        return tree_map(sympy_map,self.ast())
    
    def from_sympy(self):
        pass
    
    def to_mathjax(self):
        mathjax_map = {
            'frac': lambda x, y: r'\frac{' + x + '}{' + y + '}',
            'exp': lambda x, y: x + r'^{' + y + '}',
            'prod': lambda *x: sg_fold_op(lambda a, b: a + b,"1",x),
            'default': lambda x : str(x)
        }
        return tree_map(mathjax_map,self.ast())
    
    def display(self):
        display(Math(self.to_mathjax()))
        
class Quantity:
    def __init__(self,val=1,unit=Unit()):
        self.val = val
        self.unit = unit
    
    def __add__(self,other):
        if type(other) is Unit:
            return self + Quantity(1,other)
        elif type(other) is Quantity:
            if self.unit != other.unit:
                raise ValueError
            else:
                return Quantity(self.val + other.val, self.unit + other.unit)
        else:
            raise TypeError
        
    def __sub__(self,other):
        if type(other) is Unit:
            return self - Quantity(1,other)
        elif type(other) is Quantity:
            if self.unit != other.unit:
                raise ValueError
            else:
                return Quantity(self.val - other.val, self.unit - other.unit)
        else:
            raise TypeError
            
    def __mul__(self,other):
        if type(other) is Unit:
            return self * Quantity(1,other)
        elif type(other) is Quantity:
            return Quantity(self.val * other.val, self.unit * other.unit)
        else:
            raise TypeError

    def __truediv__(self,other):
        if type(other) is Unit:
            return self / Quantity(1,other)
        elif type(other) is Quantity:
            return Quantity(self.val / other.val , self.unit / other.unit)
        else:
            raise TypeError
            
    def __pow__(self,other):
        if not type(other) is int:
            raise TypeError
        return Quantity(self.val ** other , self.unit ** other)
    
    __xor__ = __pow__
    
    def __eq__(self,other):
        if type(other) is Unit:
            return self == Quantity(1,other)
        if not type(other) is Quantity:
            return (self.val == other.val) and (self.unit == other.unit)
        
    def __str__(self):
        return str(self.val) + " " + str(self.unit)
    
    def latex(self):
        display(Math(str(self)))
    
    def to_sympy(self):
        return Mul(self.val,self.unit.to_sympy(),evaluate=False)
    
    def from_sympy(self):
        pass
    
    def to_mathjax(self):
        return str(self.val) + self.unit.to_mathjax()
    
    def display(self):
        display(Math(self.to_mathjax()))
