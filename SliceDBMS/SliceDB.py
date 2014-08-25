'''
Created on Aug 12, 2014
@author: Mehrdad Dehdashti
'''

from SliceRecord import SliceRecord
from DBSlice import toString, INT, DOUBLE, STRING
from OPSlice import EQ, LT, GT

class SliceDB(object):
    '''
    The SliceDB class stores the dynamic slice database
    '''

    def __init__(self, pName, pSchema, pIndex = None):
        ''' 
        Constructor
        '''
        self.name = pName
        self.schema = pSchema
        self.index = pIndex
        self.database = []
        
    def createRecord(self):
        return SliceRecord(self.schema)
    
    def set(self, pRecord):
        if(self.index == None):
            self.database.append(pRecord)
            print 'Record Added'
        else:
            if(pRecord.getFieldValue(self.index) != None):
                self._updateRecord(pRecord)
            else:
                print 'Error: Missing unique index value'
                
    def get(self, pKey):
        for record in self.database:
            if(int(record.getFieldValue(self.index)) == int(pKey)):
                return record
        print 'Error: record with index value ' + str(pKey) + ' not found'
        return None
                
    def update(self, pRecord):
        if(self.index == None):
            print 'Error: Database does not have index value'
        else:
            if(pRecord.getFieldValue(self.index) != None):
                self._updateRecord(pRecord)
            else:
                print 'Error: Missing unique index value'
            
    def add(self, pRecord):
        if(self.index == None):
            self.database.append(pRecord)
            print 'Record Added'
        else:
            if(pRecord.getFieldValue(self.index) != None):
                self._addRecord(pRecord)
            else:
                print 'Error: Missing unique index value'
                
    def load(self, pUploadFileName):
        try:
            dataFile = open(pUploadFileName + ".apd", 'r')
        except (OSError, IOError):
            print "Upload File Not Found"
            return
        newDatabase = []
        for line in dataFile:
            self._local_sliceRecord = SliceRecord(self.schema)
            line = line.translate(None, '\n')
            try:
                if len(line.split('|')) != len(self.schema):
                    print "Upload File schema does not match database schema"
                    return
                for i, field in enumerate(line.split('|')):
                    self._local_sliceRecord.record[i][1] = field
            except (IndexError):
                print "Upload File schema does not match database schema"
                return
            newDatabase.append(self._local_sliceRecord)
        self.database = newDatabase
        dataFile.close()
        print "File " + pUploadFileName + " uploaded successfully"
    
    def join(self, pSliceDB, column = None):
        join_schema = []
        join_pSchema = []
        join_index = []
        join_database = []
        
        if(column):
            for field in self.schema:
                for pField in pSliceDB.schema:
                    if(field.name == column and pField.name == column):
                        join_schema.append(field)
                        join_index.append(field)
            if(join_schema == []):
                print 'Error: Column ' + column + ' does not exist'
                return None
        else:
            for field in self.schema:
                for pField in pSliceDB.schema:
                    if(field.name == pField.name and field.type == pField.type):
                        join_schema.append(field)
                        join_index.append(field)
        
        for record in self.database:
            for field in join_schema:
                if(pSliceDB._getRecordWithValue(field.name, record.getFieldValue(field.name))):
                    join_database.append(record)

        for join_field in join_schema:
            for pField in pSliceDB.schema:
                if(join_field.name != pField.name or join_field.type != pField.type):
                    if(self._isInSchema(join_schema, pField) == False):
                        join_pSchema.append(pField)
                        
        for record in join_database:
            record.addSchema(join_pSchema)
        
        bNotFound = False
        for record in join_database:
            for field in join_index:
                pRecord = pSliceDB._getRecordWithValue(field.name, record.getFieldValue(field.name))
                if(pRecord == None):
                    bNotFound = True
            if(bNotFound == False):
                for field in pRecord.record:
                    record._setValue(field[0], field[1])
        
        dataFile = open(self.name + pSliceDB.name + ".join", 'w')
        for entry in join_database:
            for i, field in enumerate(entry.record):
                if(field[1] != None):
                    dataFile.write(str(field[1]))
                if(i + 1 == len(entry.record)):
                    dataFile.write("\n")
                else:
                    dataFile.write("|")
        dataFile.close()
        
        return join_database
    
    def query(self, pQuery):
        query_result = []
        column = pQuery.condition.column
        operation = pQuery.condition.operation
        
        literalType = None
        for field in self.schema:
            if(field.name == column):
                literalType = field.type
        if(literalType == None):
            print 'Error: Condition column not found'
            return None
        
        try:
            if(literalType == INT):
                literal = int(pQuery.condition.literal)
            elif(literalType == DOUBLE):
                literal = float(pQuery.condition.literal)
            elif(literalType == STRING):
                literal = pQuery.condition.literal
            else:
                print 'Error: Column type does not match literal type'
                return None
        except ValueError:
            print 'Error: Column type does not match literal type'
            return None
        
        for record in self.database:
            if(operation == EQ):
                if(literalType == INT):
                    if(int(record.getFieldValue(column)) == literal):
                        query_result.append(record)
                elif(literalType == DOUBLE):
                    if(float(record.getFieldValue(column)) == literal):
                        query_result.append(record)
                elif(literalType == STRING):
                    if(record.getFieldValue(column) == literal):
                        query_result.append(record)
            elif(operation == LT):
                if(literalType == INT):
                    if(int(record.getFieldValue(column)) < literal):
                        query_result.append(record)
                elif(literalType == DOUBLE):
                    if(float(record.getFieldValue(column)) < literal):
                        query_result.append(record)
                elif(literalType == STRING):
                    if(record.getFieldValue(column) < literal):
                        query_result.append(record)
            elif(operation == GT):
                if(literalType == INT):
                    if(int(record.getFieldValue(column)) > literal):
                        query_result.append(record)
                elif(literalType == DOUBLE):
                    if(float(record.getFieldValue(column)) > literal):
                        query_result.append(record)
                elif(literalType == STRING):
                    if(record.getFieldValue(column) > literal):
                        query_result.append(record)
            else:
                print 'Error: Invalid Operation (Must be EQ, GT or LT)'
                return None
                
        return query_result
                        
    def _isInSchema(self, pSchema, pField):
        for field in pSchema:
            if(field.name == pField.name and field.type == pField.type):
                return True
        return False
                
    def _updateRecord(self, pRecord):
        for record in self.database:
            if(int(record.getFieldValue(self.index)) == int(pRecord.getFieldValue(self.index))):
                print 'Record Updated'
                for field in pRecord.record:
                    if(field[1] != None):
                        record._setValue(field[0], field[1])
                return
        print 'Error: Record with index value ' + str(pRecord.getFieldValue(self.index)) + ' not found'
        
    def _addRecord(self, pRecord):
        for record in self.database:
            if(int(record.getFieldValue(self.index)) == int(pRecord.getFieldValue(self.index))):
                print 'Error: Record with index value ' + str(pRecord.getFieldValue(self.index)) + ' already exists'
                return
        pRecord.setInt(self.index, pRecord.getFieldValue(self.index))
        self.database.append(pRecord)
        print 'Record Added'
        
    def _getRecordWithValue(self, pName, pValue):
        for record in self.database:
            if int(record.getFieldValue(pName)) == int(pValue):
                return record
        return None
    
    def _setRecordWithValue(self, pName, pValue):
        for record in self.database:
            if record.getFieldValue(pName) == None:
                record._setValue(pName, pValue)