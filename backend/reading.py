import json

def read_requirement(requ):
    read_in = json.loads(requ)
    method = read_in['method']
    source = {}
    keys = {}
    method = {}
    area = {}
    st = {}
    for key in read_in.keys():
        if key != 'method':
            source[key] = read_in[key]['source']
            keys[key] = read_in[key]['key']
            method[key] = read_in[key]['mehod']
            area[key] = read_in[key]['area']
            st[key] = read_in[key]['S/T']


    return method, source, keys, method, area, st


