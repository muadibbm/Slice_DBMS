'''
Created on Aug 21, 2014
@author: Mehrdad Dehdashti
'''

from SliceDBMS.SliceEnv import SliceEnv
from SliceDBMS.SliceDB import SliceDB
from SliceDBMS.SliceRecord import SliceRecord
from SliceDBMS.SliceCondition import SliceCondition
from SliceDBMS.SliceQuery import SliceQuery
from SliceDBMS import OPSlice

if __name__ == '__main__':
    
    sliceEnv = SliceEnv()
    custDB = sliceEnv.open("CustDB")
    
    columns = []
    columns.append('name')
    columns.append('age')
    
    condition = SliceCondition("name", OPSlice.EQ, "Marcia Vang")
    
    custQuery = SliceQuery(columns, "CustDB", condition)
    
    sliceRecords = custDB.query(custQuery)
    
    print "Customer Age"
    for record in sliceRecords:
        name = record.getString("name")
        age = record.getInt("age")
        print name + " " + age
    
    sliceEnv.close("CustDB")