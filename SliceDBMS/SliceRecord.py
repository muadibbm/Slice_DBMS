'''
Created on Aug 12, 2014
@author: Mehrdad Dehdashti
'''

from DBSlice import INT, DOUBLE, STRING

class SliceRecord(object):
    '''
    The SliceRecord class stores and return values of fields specified by the slice database
    '''

    def __init__(self, pSchema):
        ''' 
        Constructor
        '''
        self.record = []
        for schemaField in pSchema:
            self.record.append([schemaField.name, None])
            
    def addSchema(self, pSchema):
        for schemaField in pSchema:
            self.record.append([schemaField.name, None])
        
    def setInt(self, pName, pValue):
        if type(pValue) is INT or pValue == None:
            return self._setValue(pName, pValue)
        else:
            return False
        
    def setDouble(self, pName, pValue):
        if type(pValue) is DOUBLE or pValue == None:
            return self._setValue(pName, pValue)
        else:
            return False
        
    def setString(self, pName, pValue):
        if type(pValue) is STRING:
            return self._setValue(pName, pValue)
        else:
            return False
    
    def _setValue(self, pName, pValue):
        for dataField in self.record:
            if dataField[0] == pName:
                dataField[1] = pValue
                return True
        return False
    
    def getInt(self, pName):
        return self._getValue(pName)
        
    def getDouble(self, pName):
        return self._getValue(pName)
        
    def getString(self, pName):
        return self._getValue(pName)
        
    def _getValue(self, pName):
        for dataField in self.record:
            if dataField[0] == pName:
                return dataField[1]
        return ""
        
    def hasField(self, pName):
        for field in self.record:
            if(field[0] == pName):
                return True
        return False
    
    def getFieldType(self, pName, pSchema):
        for schemaField in pSchema:
            if(schemaField.name == pName):
                return schemaField.type
        return None
    
    def getFieldValue(self, pName):
        for field in self.record:
            if(field[0] == pName):
                return field[1]
        return None