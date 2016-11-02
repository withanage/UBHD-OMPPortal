__author__ = "Nils Weiher, Dulip Withanage"


from gluon.contrib.webclient import WebClient
import os, json, sys

class IntegrationTests:
    def __init__(self):
        pass
         
    def read_json(self, f):
        if os.path.isfile(f):
            with open(f) as j:
                return json.load(j)
        else:
            sys.exit(1) 
    def run(self):
        self.config = self.gv.read_json("heibooks.json")

'''
client = WebClient('http://127.0.0.1:8000/welcome/default/',
                   postbacks=True)

client.get('index')
# register
data = dict(first_name='Homer',
            last_name='Simpson',
            email='homer@web2py.com',
            password='test',
            password_two='test',
            _formname='register')
client.post('user/register', data=data)

# logout
client.get('user/logout')

# login again
data = dict(email='homer@web2py.com',
            password='test',
            _formname='login')
client.post('user/login', data=data)

# check registration and login were successful
client.get('index')
assert('Welcome Homer' in client.text)
'''

