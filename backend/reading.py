import json
import time


def read_requirement(requ):
    read_in = json.loads(requ)
    return read_Recursive(read_in, read_in['scale'])


def read_Recursive(jsonObject, scale):
    if 'operator' in jsonObject.keys():
        # have operator means this is not the final layer of recursive
        operate = jsonObject['operator']
        tasks0, sequance0 = read_Recursive(jsonObject['data0'], scale)
        tasks1, sequance1 = read_Recursive(jsonObject['data1'], scale)
        return tasks0 + tasks1, [operate, sequance0, sequance1]
    else:
        # final layer of recursive, find out the get method and its parameters
        if 'file' in jsonObject.keys():
            # pre calculated
            task = {'task': 'preCalculated', 
                    'file': jsonObject['file'],
                    'scale': scale}
            
        elif 'word' in jsonObject.keys():
            # get from Twitter 
            task = {'task': 'twitter', 
                    'city': jsonObject['city'],
                    'word': jsonObject['word'],
                    'method': jsonObject['method'],
                    'process': jsonObject['process'],
                    'scale': scale}
        return [task], task
        
f = open('json_temp/test.json',)
data = read_requirement(f.read())
f.close()
print (data)
