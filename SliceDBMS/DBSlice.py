'''
Created on Aug 13, 2014
@author: Mehrdad Dehdashti
'''

from types import IntType as _IntType, FloatType as _FloatType, StringType as _StringType

''' DB Types '''
INT = _IntType
DOUBLE = _FloatType
STRING = _StringType

def toString(pType):
    if pType == INT:
        return "INT"
    elif pType == DOUBLE:
        return "DOUBLE"
    elif pType == STRING:
        return "STRING"
    
def toType(pString):
    if pString == "INT":
        return INT
    elif pString == "DOUBLE":
        return DOUBLE
    elif pString == "STRING":
        return STRING