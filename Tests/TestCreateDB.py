'''
Created on Aug 12, 2014
@author: Mehrdad Dehdashti
'''

from SliceDBMS import DBSlice
from SliceDBMS.SliceEnv import SliceEnv
from SliceDBMS.SliceField import SliceField

if __name__ == '__main__':
    
    schemaElements = [SliceField("cust", DBSlice.INT),
                      SliceField("name", DBSlice.STRING),
                      SliceField("age", DBSlice.INT),
                      SliceField("phone", DBSlice.STRING),
                      SliceField("address", DBSlice.STRING)]
    
    sliceEnv = SliceEnv()
    sliceEnv.createDB("CustDB", schemaElements, "cust")