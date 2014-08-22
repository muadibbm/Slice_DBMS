'''
Created on Aug 12, 2014
@author: Mehrdad Dehdashti
'''

class SliceField(object):
    '''
    The SliceField class contains a type and a name
    '''

    def __init__(self, pName, pType):
        ''' 
        Constructor
        '''
        self.name = pName
        self.type = pType