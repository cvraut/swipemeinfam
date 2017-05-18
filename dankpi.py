import json
from collections import defaultdict


class dankpi:
    def __init__(self):
        db = open('dankbase.json')
        self._db = defaultdict(dict)
        self._db.update(json.load(db))
        db.close()

    def _update_db(self):
        for ucinetid in self._db:
            if self._db[ucinetid] == {}:
                del self._db[ucinetid]
        db = open('dankbase.json','w')
        json_str = str(dict(self._db)).replace('True', 'true')
        json_str = json_str.replace('False', 'false')
        db.write(json_str.replace("'", '"'))
        db.close()

    def get_all(self):
        return dict(self._db)

    def get_request(self,params: dict) -> dict:
        ''' This function gets the information from the API as a JSON and returns it.
            params is a dictionary of query parameters (name, swipes, cost, etc.)'''
        result = {}
        for ucinetid in self._db:
            good = True
            for k in params:
                if params[k] != self._db[ucinetid][k]:
                    good = False
                    break
            if good:
                result[ucinetid] = self._db[ucinetid]
        return result

    def get_request_ucinetid(self,ucinetid) -> str:
        ''' returns value at said ucinetid, empty dict if otherwise'''
        return self._db[ucinetid]

    def post_request(self,ucinetid: str, params: dict) -> str:
        '''posts new user into system'''
        if 'name' not in params and 'swipes' not in params:
            raise SyntaxError(
                'You need to specify at least a name and number of swipes in the paramters')
        self.delete_request(ucinetid)
        return self.put_request(ucinetid,params)

    def put_request(self,ucinetid: str, params: dict) -> str:
        '''update'''
        previous = self._db[ucinetid]
        n = params['name'] if 'name' in params.keys() else previous['name']
        swipes = params['swipes'] if 'swipes' in params.keys() else previous['swipes']

        s = previous['success'] if 'success' in previous.keys() else 0
        f = previous['failure'] if 'failure' in previous.keys() else 1
        r = previous['response_time'] if 'response_time' in previous.keys() else 0
        p = previous['pippin'] if 'pippin' in previous.keys() else True
        a = previous['anteatery'] if 'anteatery' in previous.keys() else True
        c = previous['cost'] if 'cost' in previous.keys() else 0
        times = previous['times'] if 'times' in previous.keys() else {"Wednesday": [], "Sunday": [], "Friday": [], "Monday": [],"Saturday": [], "Thrusday": [], "Tuesday": []}


        if "pippin" in params.keys():
            p = params["pippin"]
        if "anteatery" in params.keys():
            a = params["anteatery"]
        if "cost" in params.keys():
            c = params["cost"]
        if "times" in params.keys():
            for day in params['times']:
                times[day] = params['times'][day]

        user = {'success': s, 'failure': f, "response_time": r,
                "name": n, 'swipes': swipes,
                "times": times, "pippin": p, "anteatery": a, "cost": c}
        self._db[ucinetid] = user
        self._update_db()
        return '{"success":true}'

    def delete_request(self,ucinetid: str) -> str:
        ''' This function gets the information from the API as a JSON and returns it'''
        if ucinetid in self._db.keys():
            del self._db[ucinetid]
        return '{"success":true}'

    def inc_success(self,ucinetid:str):
        pass

    def inc_failure(self,ucinetid:str):
        pass

    def inc_response_time(self,ucinetid:str,response_time=0):
        pass