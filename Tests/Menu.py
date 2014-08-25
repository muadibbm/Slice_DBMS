'''
Created on Aug 12, 2014
@author: Mehrdad Dehdashti
'''

import sys
import subprocess
from SliceDBMS import DBSlice
from SliceDBMS.SliceEnv import SliceEnv
from SliceDBMS.SliceField import SliceField
from SliceDBMS.SliceCondition import SliceCondition
from SliceDBMS.SliceQuery import SliceQuery
    
def _run():
    while True:
        print ("\nSlice DBMS Menu\n" + 
                "1. Create Database\n" +
                "2. Update Record\n"+
                "3. Add Record\n"+
                "4. Delete Record\n"+
                "5. Bulk Load\n"+
                "6. Display Join\n"+
                "7. Run Query\n"+
                "8. Report 1\n"+
                "9. Report 2\n"+
                "10. Exit\n")
        client_input = _getInput('Select')
        if(client_input == '1'):
            _createDatabase()
        elif(client_input == '2'):
            _updateRecord()
        elif(client_input == '3'):
            _addRecord()
        elif(client_input == '4'):
            _deleteRecord()
        elif(client_input == '5'):
            _bulkLoad()
        elif(client_input == '6'):
            _displayJoin()
        elif(client_input == '7'):
            _runQuery()
        elif(client_input == '8'):
            _report1()
        elif(client_input == '9'):
            _report2()
        elif(client_input == '10'):
            print "Application terminated - Goodbye!"
            sys.exit()
        else:
            print "Invalid input"
            
def _createDatabase():
    dataabaseName = _getInput('Enter Database Name')
    count = _processInteger('Enter Number of Fields')
    schemaElements = []
    i = 0
    while i < count:
        field_name = _getInput('Enter Field Name')
        if _checkIfAlreadyExists(field_name, schemaElements):
            print "Error: Field name already exits"
        else:
            while True:
                print ("\nChoose Field Type\n" +
                       "1. INT\n" + 
                       "2. DOUBLE\n" +
                       "3. STRING\n")
                client_input = _getInput('Select')
                if(client_input == '1'):
                    field_type = DBSlice.INT
                    break
                elif(client_input == '2'):
                    field_type = DBSlice.DOUBLE
                    break
                elif(client_input == '3'):
                    field_type = DBSlice.STRING
                    break
                else:
                    print "Error: Invalid input"
            schemaElements.append(SliceField(field_name, field_type))
            i = i + 1
    indexNotGood = True
    while indexNotGood:
        index = _getInput('Enter Index Name (Optional, INT Type)')
        if index == '':
            indexNotGood = False
        for field in schemaElements:
            if field.name == index and field.type == DBSlice.INT:
                indexNotGood = False
    if index == '':
        index = None
    sliceEnv = SliceEnv()
    sliceEnv.createDB(dataabaseName, schemaElements, index)

def _updateRecord():
    sliceEnv = SliceEnv()
    custDB = sliceEnv.open(_getInput('Enter Database Name'))
    if custDB == None:
        return
    custRecord = custDB.createRecord()
    for field in custRecord.record:
        if custRecord.getFieldType(field[0], custDB.schema) ==  DBSlice.INT:
            custRecord.setInt(field[0], _processInteger('Enter ' + field[0]))
        elif custRecord.getFieldType(field[0], custDB.schema) ==  DBSlice.DOUBLE:
            custRecord.setDouble(field[0], _processFloat('Enter ' + field[0]))
        elif custRecord.getFieldType(field[0], custDB.schema) ==  DBSlice.STRING:
            custRecord.setString(field[0], _getInput('Enter ' + field[0]))
    custDB.update(custRecord)
    sliceEnv.close("CustDB")
        
def _addRecord():
    sliceEnv = SliceEnv()
    custDB = sliceEnv.open(_getInput('Enter Database Name'))
    if custDB == None:
        return
    custRecord = custDB.createRecord()
    for field in custRecord.record:
        if custRecord.getFieldType(field[0], custDB.schema) ==  DBSlice.INT:
            custRecord.setInt(field[0], _processInteger('Enter ' + field[0]))
        elif custRecord.getFieldType(field[0], custDB.schema) ==  DBSlice.DOUBLE:
            custRecord.setDouble(field[0], _processFloat('Enter ' + field[0]))
        elif custRecord.getFieldType(field[0], custDB.schema) ==  DBSlice.STRING:
            custRecord.setString(field[0], _getInput('Enter ' + field[0]))
    custDB.add(custRecord)
    sliceEnv.close("CustDB")
    
def _deleteRecord():
    sliceEnv = SliceEnv()
    custDB = sliceEnv.open(_getInput('Enter Database Name'))
    if custDB == None:
        return
    if custDB.index == None:
        print "Error: Cannot perform deletion on database without index"
        return
    keyValue = _processInteger('Enter ' + custDB.index)
    for i, record in enumerate(custDB.database):
        if int(record.getFieldValue(custDB.index)) == keyValue:
            custDB.database.pop(i)
            sliceEnv.close("CustDB")
            print "Record Deleted"
            return
        i = i + 1
    print "Error: Record does not exist"
    
def _bulkLoad():
    sliceEnv = SliceEnv()
    custDB = sliceEnv.open(_getInput('Enter Database Name'))
    if custDB == None:
        return
    print 'Only accepts file with .apd extension'
    custDB.load(_getInput('Enter Upload File Name (without .apd)'))
    sliceEnv.close("CustDB")
    
def _displayJoin():
    sliceEnv = SliceEnv()
    custDB = sliceEnv.open(_getInput('Enter First Database Name'))
    if custDB == None:
        return
    salesDB = sliceEnv.open(_getInput('Enter Second Database Name'))
    if salesDB == None:
        return
    join_column = _getInput('Enter the join column')
    join_database = []
    if(join_column == ''):
        join_database = custDB.join(salesDB)
    else:
        join_database = custDB.join(salesDB, join_column)
    if(join_database != None):
        print "You can find the join database in the file " + custDB.name + salesDB.name + ".join"
    sliceEnv.close("SalesDB")
    sliceEnv.close("CustDB")
    
def _runQuery():
    sliceEnv = SliceEnv()
    custDB = sliceEnv.open(_getInput('Enter Database Name'))
    if custDB == None:
        return
    columns = _getInput('Enter the list of columns to be displayed separated by the symbol "|"').split('|')
    conditionAttributes = _getInput('Enter the column, condition and the literal value separated by the symbol "|"').split('|')
    if(len(conditionAttributes) == 3):
        condition = SliceCondition(conditionAttributes[0], conditionAttributes[1], conditionAttributes[2])
    else:
        print 'Error: Condition format should be column_name|operation|literal_value'
        return
    custQuery = SliceQuery(columns, custDB, condition)
    sliceRecords = custDB.query(custQuery)
    if(sliceRecords == None):
        return
    output = " "
    for column in columns:
        output += column + "   "
    print output
    for record in sliceRecords:
        output = " "
        for column in columns:
            output += record._getValue(column) + "   " 
        print output
    sliceEnv.close("CustDB")

def _report1():
    subprocess.check_call(["runhaskell", "report1"])

def _report2():
    sliceEnv = SliceEnv()
    custDB = sliceEnv.open("CustDB")
    salseDB = sliceEnv.open("SalesDB")
    orderDB = sliceEnv.open("OrderDB")
    join_database = custDB.join(salseDB, "cust")
    if(join_database == None):
        return
    join_database = orderDB.join(salseDB, "order")
    if(join_database == None):
        return
    subprocess.check_call(["runhaskell", "report2"])

def _getInput(promotMessage):
    while True:
        value = raw_input(promotMessage + ': ')
        if((promotMessage == 'Enter Database Name' or promotMessage == 'Enter Field Name') and 
            value.translate(None, ' ') == ''):
            print 'Error: Name cannot be empty'
        else:
            break
    return value

def _processInteger(promotMessage):
    while True:
        try:
            pInt = _getInput(promotMessage)
            if(pInt == ''):
                return None
            return int(pInt)
        except ValueError:
            print 'Error: Invalid Input'
        
def _processFloat(promotMessage):
    while True:
        try:
            pFloat = _getInput(promotMessage)
            if(pFloat == ''):
                return None
            return float(pFloat)
        except ValueError:
            print 'Error: Invalid Input'

def _checkIfAlreadyExists(fieldName, schemaElements):
    for sliceField in schemaElements:
        if(sliceField.name == fieldName):
            return True
    return False

if __name__ == '__main__':
    _run()