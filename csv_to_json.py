csv_in = open('test_data.csv')
tags = next(csv_in).strip().split(',')
from collections import defaultdict
json = defaultdict(dict)
def next_val(s):
    result = ''
    if s != '':
        if s[0] == '"':
            for i in range(len(s[2:])):
                if s[i+2] == ']':
                    return result,s[i+5:]
                result+=s[i+2]
        elif s[0] == '[':
            for i in range(len(s[1:])):
                if s[i + 1] == ']':
                    return result, s[i + 3:]
                result += s[i + 1]
        else:
            for i in range(len(s)):
                if s[i] == ',':
                    return result,s[i+1:]
                result+=s[i]
    return result,''


for row in csv_in:
    row = row.strip()
    ucinetid,row = next_val(row)
    print(ucinetid,row)
    for i in range(1,len(tags)):
        val,row = next_val(row)
        if i>=4 and i<11:
            if 'times' not in json[ucinetid].keys():
                json[ucinetid]['times'] = {}
            print('this is val:',val)
            json[ucinetid]['times'][tags[i]] = list(map(lambda x: int(x.rstrip(',')),val.split()))

        else:
            if i in [3,2,13,14,15]:
                json[ucinetid][tags[i]] = int(val)
            elif i in [11,12]:
                json[ucinetid][tags[i]] = val == 'TRUE'
            else:
                json[ucinetid][tags[i]] = val
json = dict(json)
csv_in.close()
db = open('dankbase.json','w')
db.write(str(json))
db.close()
print(json)