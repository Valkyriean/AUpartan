from flaskext.couchdb import Document, CouchDBManager,ViewDefnition

#this should return total value of nlpvalue attribute
average = ViewDefnition('doc name here','average','''/
    function(doc){
        emit(doc.sa3_id, doc.nlpvalue);
    }''','''function(keys, values, rereduce){
            return sum(values);
    }
    '''
)
#this should return the total number of record.
lengthoftweets = ViewDefnition('doc name here','totalnumber','''/
    function(doc){
        emit(doc.sa3_id, 1);
    }''','''function(keys, values, rereduce){
            return sum(values);
    }
    '''
)
