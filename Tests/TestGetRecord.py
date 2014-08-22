'''
Created on Aug 21, 2014
@author: Mehrdad Dehdashti
'''

from SliceDBMS.SliceEnv import SliceEnv
from SliceDBMS.SliceDB import SliceDB
from SliceDBMS.SliceRecord import SliceRecord

if __name__ == '__main__':
    
    sliceEnv = SliceEnv()
    custDB = sliceEnv.open("CustDB")
    
    custRecord = custDB.get(298)
    
    if(custRecord):
        print "Name " + custRecord.getString("name")
        print "Age " + custRecord.getInt("age")
        print "Address " + custRecord.getString("address")
    
    sliceEnv.close("CustDB")