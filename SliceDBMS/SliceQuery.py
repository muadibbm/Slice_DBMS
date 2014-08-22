'''
Created on Aug 12, 2014
@author: Mehrdad Dehdashti
'''

class SliceQuery(object):
    '''
    The SliceQuery class contains the query specifications
    '''

    def __init__(self, pColumns, pName, pCondition):
        ''' 
        Constructor
        '''
        self.columns = pColumns
        self.name = pName
        self.condition = pCondition