'''
Created on Aug 12, 2014
@author: Mehrdad Dehdashti
'''

from SliceDB import SliceDB
from SliceField import SliceField
from DBSlice import toString, toType
from SliceRecord import SliceRecord

class SliceEnv(object):
    '''
    The SliceEnv class is the interface into the database
    '''

    def __init__(self):
        ''' 
        Constructor
        '''
        self.sliceDB = None

    def createDB(self, pName, pSchemaElements, pIndex = None):
        self.sliceDB = SliceDB(pName, pSchemaElements, pIndex)
        self._writeToFile()
        print "Database " + pName + " created"

    def open(self, pName):
        self._readFromFile(pName)
        return self.sliceDB
    
    def close(self, pName):
        self._writeToFile()

    def _writeToFile(self):
        dataFile = open(self.sliceDB.name + ".schema", 'w')
        for i in range(len(self.sliceDB.schema)):
            if i + 1 == len(self.sliceDB.schema):
                if(self.sliceDB.index == None):
                    dataFile.write(self.sliceDB.schema[i].name + ":" + toString(self.sliceDB.schema[i].type) + "\n")
                else:
                    dataFile.write(self.sliceDB.schema[i].name + ":" + toString(self.sliceDB.schema[i].type))
            else:
                dataFile.write(self.sliceDB.schema[i].name + ":" + toString(self.sliceDB.schema[i].type) + "|")
        if(self.sliceDB.index != None):
            dataFile.write("|" + self.sliceDB.index + "\n")
        dataFile.close()
        dataFile = open(self.sliceDB.name + ".slc", 'w')
        for entry in self.sliceDB.database:
            for i, field in enumerate(entry.record):
                if(field[1] != None):
                    dataFile.write(str(field[1]))
                if(i + 1 == len(entry.record)):
                    dataFile.write("\n")
                else:
                    dataFile.write("|")
        dataFile.close()

    def _readFromFile(self, pName):
        try:
            dataFile = open(pName + ".schema", 'r')
        except (OSError, IOError):
            print "Database Schema Not Found"
            return
        self._local_index = None
        self._local_schema = []
        for line in dataFile:
            line = line.translate(None, '\n')
            for entry in line.split('|'):
                field = entry.split(':')
                if(len(field) == 1):
                    self._local_index = field[0]
                else:
                    self._local_schema.append(SliceField(field[0], toType(field[1])))
        self.sliceDB = SliceDB(pName, self._local_schema, self._local_index)
        dataFile.close()
        try:
            dataFile = open(pName + ".slc", 'r')
        except (OSError, IOError):
            print "Database Not Found"
            return
        self._local_index = None
        self._local_schema = []
        for line in dataFile:
            self._local_sliceRecord = SliceRecord(self.sliceDB.schema)
            line = line.translate(None, '\n')
            for i, field in enumerate(line.split('|')):
                self._local_sliceRecord.record[i][1] = field
            self.sliceDB.database.append(self._local_sliceRecord)
        dataFile.close()