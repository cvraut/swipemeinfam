from mongoengine import *
import json

CONNECTION = 'mongodb://cluster0-shard-00-00-tijfs.mongodb.net:27017,cluster0-shard-00-01-tijfs.mongodb.net:27017,cluster0-shard-00-02-tijfs.mongodb.net:27017/users?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin'

connect(db='users', host=CONNECTION, username='swipe', password='zotzotzot', alias='default')

COST_DEFAULT = 0.0
TIMES_DEFAULT = ''
PIPPIN_DEFAULT = True
ANTEATERY_DEFAULT = True
LAST_UPDATED_DEFAULT = ''
CREDIBILITY_INDEX_DEFAULT = 1.0
IMG_URL_DEFAULT = ''

VALID_FIELDS = ('ucinetid', 'name', 'swipes', 'cost', 'wd_times', 'we_times', 'pippin', 'anteatery', 'last_updated', 'credibility_index', 'img_url')

class User(Document):
    ucinetid = StringField(required=True, max_length = 9)
    name = StringField(required=True, max_length = 20)
    swipes = IntField(required=True)
    cost = FloatField(default=COST_DEFAULT)
    wd_times = StringField(default=TIMES_DEFAULT)
    we_times = StringField(default=TIMES_DEFAULT)
    pippin = BooleanField(default=PIPPIN_DEFAULT)
    anteatery = BooleanField(default=ANTEATERY_DEFAULT)
    last_updated = StringField(default=LAST_UPDATED_DEFAULT)
    credibility_index = FloatField(default=CREDIBILITY_INDEX_DEFAULT)
    img_url = StringField(dfeault=IMG_URL_DEFAULT)


def create_user_json(user):
    return {'ucinetid': user.ucinetid, 'name': user.name, 'swipes': user.swipes, 'cost': user.cost, 'times': {'wd_times': user.wd_times, 'we_times': user.we_times}, 'places': {'pippin': user.pippin, 'anteatery': user.anteatery}, 'last_updated': user.last_updated, 'credibility_index': user.credibility_index, 'img_url': user.img_url}

def create_success_json(success):
    return json.dumps({'success': success})

def get_user_by_id(ucinetid):
    return User.objects(ucinetid=ucinetid)[0]

def db_get_user_list(**kwargs):
    return json.dumps({'users': [create_user_json(user) for user in User.objects(**kwargs)]})

def db_get_user(ucinetid):
    return db_get_user_list(ucinetid=ucinetid)

def db_post_user(ucinetid, name, swipes, cost=COST_DEFAULT, times=TIMES_DEFAULT, pippin=PIPPIN_DEFAULT, anteatery=ANTEATERY_DEFAULT):
    if list(User.objects(ucinetid=ucinetid)) == []:
        try:
            User(ucinetid=ucinetid, name=name, swipes=swipes, cost=cost, times=times, pippin=pippin, anteatery=anteatery).save()
            return create_success_json(True)
        except:
            return create_success_json(False)
    return create_success_json(False)

def db_put_user(ucinetid, **kwargs):
    if list(User.objects(ucinetid=ucinetid)) == []:
        return create_success_json(False)
    user = get_user_by_id(ucinetid)
    user.update(**kwargs)
    return create_success_json(True)

def db_delete_user(ucinetid):
    if list(User.objects(ucinetid=ucinetid)) == []:
        return create_success_json(False)
    user = get_user_by_id(ucinetid)
    user.delete()
    return create_success_json(True)
