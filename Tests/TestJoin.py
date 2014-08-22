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
    salseDB = sliceEnv.open("SalesDB")
    
    joinList = custDB.join(salseDB)

    for record in joinList:
        name = record.getString("name")
        total = record.getDouble("total")
        print "Sales for " + name + ": " + total
    
    sliceEnv.close("SalesDB")
    sliceEnv.close("CustDB")