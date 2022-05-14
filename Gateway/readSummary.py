from couchdb.design import ViewDefinition


def gateway_aurin(db, key_Search):

    viewName = "aurin" + key_Search + "Target"
    AurinTarget_View = ViewDefinition("aurin", viewName,'''\
            function(doc){
                emit(doc.code, doc.target_value);
            }''')
    AurinTarget_View.sync(db)

    return AurinTarget_View

def gateway_tweet(db, key_Search, harvest_method, level):

    viewName = harvest_method + key_Search + level

    if level == "count":
        TweetTarget_View = ViewDefinition(harvest_method, viewName,'''\
            function(doc){
                emit(doc._id, doc.tweet_count);
            }''')

    elif level == "sentiment":
        TweetTarget_View = ViewDefinition(harvest_method, viewName,'''\
            function(doc){
                emit(doc._id, doc.nlpemo);
            }''')

    TweetTarget_View.sync(db)

    return TweetTarget_View

def extra_data_view(view_function, db):
    view_result = view_function(db)
    result_dict = {}
    for row in view_result:
        result_dict[row.key] = row.value
    return result_dict

def extract_summary(couch, summary_db):

    if "aurin" in summary_db["name"]:
        search_key = summary_db["name"].split("_")[1]
        for i in couch:
            if "aurin" in i:
                if search_key in i:
                    if summary_db["level"] in i:
                        if "summary" in i:
                            required_db = couch[i]
                            break
        gateway_view = gateway_aurin(required_db, search_key)
    
    else:
        search_method = summary_db["name"].split("_")[0]
        search_key = summary_db["name"].split("_")[1]
        search_stat = summary_db["method"]
        for i in couch:
            if search_method in i:
                if search_key in i:
                    if "summary" in i:
                        required_db = couch[i]
                        break
        gateway_view = gateway_tweet(required_db, search_key, search_method, search_stat)
    
    result_dict = extra_data_view(gateway_view, required_db)

    return result_dict