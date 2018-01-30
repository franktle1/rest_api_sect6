#will have an inmemory table with registered users in lieu of a databases
from resources.user import UserModel
from werkzeug.security import safe_str_cmp
#safe str cmp compares strings
#we can import UserModel Class from user


#username_mapping = {u.username: u for u in users} #this is a list comprehension
#userid_mapping = {u.id: u for u in users}

'''
username_mapping = {'bob': {
    'id': 1,
    'username':'bob',
    'password': 'bblah'
    }
}
userid_mapping = {1: {
    'id': 1,
    'username':'bob',
    'password': 'bblah'
}}
'''
#we have the above to avoid having to iterating the whole list
#find user by username
def authenticate(username, password):
    #.get() gets values of te key 'username'; useful for setting a default value
    #username_mapping['username'] <-- similar to .get without having a default
    #user = username_mapping.get(username, None) #replacing userid_mapping with database

    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

#payload is the content of the JWT token
#THIS METHOD IS EXCLUSIVE TO JWT
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
    #return userid_mapping.get(user_id, None) #replacing userid_mapping with database instead of a in-memory db
