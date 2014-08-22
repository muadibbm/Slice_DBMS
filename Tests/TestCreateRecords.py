'''
Created on Aug 12, 2014
@author: Mehrdad Dehdashti
'''

from SliceDBMS.SliceEnv import SliceEnv
from SliceDBMS.SliceDB import SliceDB
from SliceDBMS.SliceRecord import SliceRecord

if __name__ == '__main__':
    
    sliceEnv = SliceEnv()
    custDB = sliceEnv.open("CustDB")
    
    custRecord = custDB.createRecord()
    
    custRecord.setString("name", "Joe Smith")
    custRecord.setInt("age", 43)
    custRecord.setString("address", "Montreal")
    
    custDB.set(custRecord)
    
    sliceEnv.close("CustDB")
    