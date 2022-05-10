from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField, FloatField, ListField
from couchdb.design import ViewDefinition
from flaskext.couchdb import Row

'''
name:[city list here/sa3 name]
x:value[value list]
y:value[value list]
'''
'''
key._id
value.nlpemo
'''

'''

'''
def gateway_View(doc_Aurin, doc_Hist, doc_Search):
    AurinTarget_View = ViewDefinition(doc_Aurin, 'AurinTargetView','''\
            function(doc){
                emit(doc._id, doc.target_value);
            }''')

    Historic_View_emo = ViewDefinition(doc_Hist, 'HistoricViewEmo','''\
            function(doc){
                emit(doc._id, doc.nlpemo);
            }'''
    )
    Search_View_emo = ViewDefinition(doc_Search, 'SearchViewEmo','''\
            function(doc){
                emit(doc._id, doc.nlpemo);
            }
    ''')
    Historic_View_count = ViewDefinition(doc_Hist, 'HistoricViewCount','''\
            function(doc){
                emit(doc._id, doc.tweet_count);
            }'''
    )
    Search_View_count = ViewDefinition(doc_Search, 'SearchViewCount','''\
            function(doc){
                emit(doc._id, doc.tweet_count);
            }
    ''')
    AurinTarget_View.sync(doc_Aurin)
    Historic_View_emo.sync(doc_Hist)
    Historic_View_count.sync(doc_Hist)
    Search_View_emo.sync(doc_Search)
    Search_View_count.sync(doc_Search)

    return AurinTarget_View, Historic_View_emo, Search_View_emo, Historic_View_count, Search_View_count

def extra_data_view(view_function, db):
    view_result = view_function(db)
    result_list = {}
    for row in view_result:
        result_list[row.key] = row.value
    return result_list


