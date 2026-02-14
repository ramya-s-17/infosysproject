# Sample Python file for testing the parser

def calculate_sum(a,b,c):
    x=a+b
    y=x+c
    return y

class Calculator:
    def __init__(self,name):
        self.name=name
        self.result=0
    
    def add(self,x,y):
        self.result=x+y
        return self.result
    
    def multiply(self,x,y):
        self.result=x*y
        return self.result

import math
from datetime import datetime

def fibonacci(n):
    if n<=0:
        return 0
    elif n==1:
        return 1
    else:
        return fibonacci(n-1)+fibonacci(n-2)

# Main execution
if __name__=="__main__":
    calc=Calculator("MyCalc")
    result=calc.add(5,10)
    print(result)
