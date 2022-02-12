import pytest
import error
import json

import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import datetime
from datetime import timezone

'''
This url function is taken from the simple_test.py week 5 lab.
'''
@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")


'''
This is a simple test to check that the message react function works
'''
def test_react_simple(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token': user1.json()['token'], 
        'name': "FirstChannel", 
        'is_public': True
    })

    message1id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello"
    })

    requests.post(f"{url}/message/react", json = {
        'token': user1.json()['token'],
        'message_id': message1id.json()['message_id'],
        'react_id': 1
    })

    get_messages1 = requests.get(f"{url}/channel/messages", params = {
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })

    assert get_messages1.json()['messages'][0]['reacts'] == [{
        'react_id': 1,
        'u_ids': [user1.json()['u_id']],
        'is_this_user_reacted': True
    }]

'''
This test checks that an input error is raised when an invalid react ID is passed (ie. anything other than 1)
'''
def test_react_invalid_react_id(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token': user1.json()['token'], 
        'name': "FirstChannel", 
        'is_public': True
    })

    message1id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello"
    })
    reacting = requests.post(f"{url}/message/react", json = {
        'token': user1.json()['token'],
        'message_id': message1id.json()['message_id'],
        'react_id': -1
    })

    assert(reacting.status_code == 400)


'''
This test checks that an access error is raised when an invalid token is passed
'''
def test_react_invalid_token(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token': user1.json()['token'], 
        'name': "FirstChannel", 
        'is_public': True
    })

    message1id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello"
    })
    reacting = requests.post(f"{url}/message/react", json = {
        'token': -1,
        'message_id': message1id.json()['message_id'],
        'react_id': 1
    })

    assert(reacting.status_code == 400)


'''
This test checks that an input error is raised when using an invalid message ID
'''
def test_react_invalid_message(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token': user1.json()['token'], 
        'name': "FirstChannel", 
        'is_public': True
    })

    requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello"
    })
    reacting = requests.post(f"{url}/message/react", json = {
        'token': user1.json()['token'],
        'message_id': -1,
        'react_id': 1
    })

    assert(reacting.status_code == 400)


'''
This test checks that an input error is raised if the authorised user is not a member of the channel
that contains the message they are trying to react to.
'''
def test_react_not_a_member(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user2@gmail.com',
        'password' : 'StrongPassword123',
        'name_first' : 'Albert',
        'name_last' : 'Einstein',
    })

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token': user1.json()['token'], 
        'name': "FirstChannel", 
        'is_public': True
    })

    message1id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello"
    })
    reacting = requests.post(f"{url}/message/react", json = {
        'token': user2.json()['token'],
        'message_id': message1id.json()['message_id'],
        'react_id': 1
    })

    assert(reacting.status_code == 400)


'''
This is a more complex test to check that message react works when called multiple times
'''
def test_react_few(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user2@gmail.com',
        'password' : 'StrongPassword123',
        'name_first' : 'Albert',
        'name_last' : 'Einstein',
    })

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token': user1.json()['token'], 
        'name': "FirstChannel", 
        'is_public': True
    })

    requests.post(f"{url}/channel/invite", json = {
        'token': user1.json()['token'], 
        'channel_id': channel1.json()['channel_id'],
        'u_id': user2.json()['u_id']
    })

    message1id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello"
    })
    
    message2id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Welcome to the Channel!!"
    })

    message3id = requests.post(f"{url}/message/send", json = { 
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Thanks for adding me!"
    })

    message4id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "No worries!"
    })

    requests.post(f"{url}/message/send", json = { 
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "I can't wait to send more messages"
    })

    requests.post(f"{url}/message/react", json = {
        'token': user1.json()['token'],
        'message_id': message1id.json()['message_id'],
        'react_id': 1
    })
    requests.post(f"{url}/message/react", json = {
        'token': user2.json()['token'],
        'message_id': message1id.json()['message_id'],
        'react_id': 1
    })
    requests.post(f"{url}/message/react", json = {
        'token': user2.json()['token'],
        'message_id': message2id.json()['message_id'],
        'react_id': 1
    })

    requests.post(f"{url}/message/react", json = {
        'token': user2.json()['token'],
        'message_id': message3id.json()['message_id'],
        'react_id': 1
    })

    requests.post(f"{url}/message/react", json = {
        'token': user1.json()['token'],
        'message_id': message4id.json()['message_id'],
        'react_id': 1
    })

    get_messages1 = requests.get(f"{url}/channel/messages", params = {
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })

    assert get_messages1.json()['messages'][1]['reacts'] == [{
        'react_id': 1,
        'u_ids': [user1.json()['u_id']],
        'is_this_user_reacted': False
    }]
    assert get_messages1.json()['messages'][2]['reacts'] == [{
        'react_id': 1,
        'u_ids': [user2.json()['u_id']],
        'is_this_user_reacted': True
    }]
    assert get_messages1.json()['messages'][3]['reacts'] == [{
        'react_id': 1,
        'u_ids': [user2.json()['u_id']],
        'is_this_user_reacted': True
    }]
    assert get_messages1.json()['messages'][4]['reacts'] == [{
        'react_id': 1,
        'u_ids': [user1.json()['u_id'], user2.json()['u_id']],
        'is_this_user_reacted': True
    }]


'''
This is a test to check that nothing happens if a user calls message react twice in a row
'''
def test_react_double(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token': user1.json()['token'], 
        'name': "FirstChannel", 
        'is_public': True
    })

    message1id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello"
    })

    requests.post(f"{url}/message/react", json = {
        'token': user1.json()['token'],
        'message_id': message1id.json()['message_id'],
        'react_id': 1
    })

    requests.post(f"{url}/message/react", json = {
        'token': user1.json()['token'],
        'message_id': message1id.json()['message_id'],
        'react_id': 1
    })

    get_messages1 = requests.get(f"{url}/channel/messages", params = {
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })

    assert get_messages1.json()['messages'][0]['reacts'] == [{
        'react_id': 1,
        'u_ids': [user1.json()['u_id']],
        'is_this_user_reacted': True
    }]


'''
This is a simple test to check that a message can be unreacted to
'''
def test_unreact_simple(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user2@gmail.com',
        'password' : 'StrongPassword123',
        'name_first' : 'Albert',
        'name_last' : 'Einstein',
    })

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token': user1.json()['token'], 
        'name': "FirstChannel", 
        'is_public': True
    })

    requests.post(f"{url}/channel/invite", json = {
        'token': user1.json()['token'], 
        'channel_id': channel1.json()['channel_id'],
        'u_id': user2.json()['u_id']
    })

    message1id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello"
    })

    requests.post(f"{url}/message/react", json = {
        'token': user1.json()['token'],
        'message_id': message1id.json()['message_id'],
        'react_id': 1
    })
    requests.post(f"{url}/message/react", json = {
        'token': user2.json()['token'],
        'message_id': message1id.json()['message_id'],
        'react_id': 1
    })
    requests.post(f"{url}/message/unreact", json = {
        'token': user1.json()['token'],
        'message_id': message1id.json()['message_id'],
        'react_id': 1
    })

    get_messages1 = requests.get(f"{url}/channel/messages", params = {
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })
    

    assert get_messages1.json()['messages'][0]['reacts'] == [{
        'react_id': 1,
        'u_ids': [user2.json()['u_id']],
        'is_this_user_reacted': False
    }]


'''
This test checks that an access error is raised when an invalid token is passed
'''
def test_unreact_invalid_token(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token': user1.json()['token'], 
        'name': "FirstChannel", 
        'is_public': True
    })

    message1id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello"
    })

    requests.post(f"{url}/message/react", json = {
        'token': user1.json()['token'],
        'message_id': message1id.json()['message_id'],
        'react_id': 1
    })

    unreacting = requests.post(f"{url}/message/unreact", json = {
        'token': -1,
        'message_id': message1id.json()['message_id'],
        'react_id': 1
    })

    assert(unreacting.status_code == 400)


'''
This test checks that an input error is raised when an invalid react ID is passed (ie. anything other than 1)
'''
def test_unreact_invalid_react_id(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token': user1.json()['token'], 
        'name': "FirstChannel", 
        'is_public': True
    })

    message1id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello"
    })

    requests.post(f"{url}/message/react", json = {
        'token': user1.json()['token'],
        'message_id': message1id.json()['message_id'],
        'react_id': 1
    })

    unreacting = requests.post(f"{url}/message/unreact", json = {
        'token': user1.json()['token'],
        'message_id': message1id.json()['message_id'],
        'react_id': -1
    })

    assert(unreacting.status_code == 400)


'''
This test checks that an input error is raised when using an invalid message ID
'''
def test_unreact_invalid_message_id(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token': user1.json()['token'], 
        'name': "FirstChannel", 
        'is_public': True
    })

    message1id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello"
    })

    requests.post(f"{url}/message/react", json = {
        'token': user1.json()['token'],
        'message_id': message1id.json()['message_id'],
        'react_id': 1
    })

    unreacting = requests.post(f"{url}/message/unreact", json = {
        'token': user1.json()['token'],
        'message_id': -1,
        'react_id': 1
    })

    assert(unreacting.status_code == 400)


'''
This test checks that an input error is raised if the authorised user is not a member of the channel
that contains the message they are trying to unreact to.
'''
def test_unreact_not_a_member(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user2@gmail.com',
        'password' : 'StrongPassword123',
        'name_first' : 'Albert',
        'name_last' : 'Einstein',
    })

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token': user1.json()['token'], 
        'name': "FirstChannel", 
        'is_public': True
    })

    message1id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello"
    })

    requests.post(f"{url}/message/react", json = {
        'token': user1.json()['token'],
        'message_id': message1id.json()['message_id'],
        'react_id': 1
    })

    unreacting = requests.post(f"{url}/message/unreact", json = {
        'token': user2.json()['token'],
        'message_id': message1id.json()['message_id'],
        'react_id': -1
    })

    assert(unreacting.status_code == 400)


'''
This test checks that an input error is raised if there are no existing reacts with
the given react ID when message_unreact is called.
'''
def test_unreact_no_existing_reacts(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token': user1.json()['token'], 
        'name': "FirstChannel", 
        'is_public': True
    })

    message1id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello"
    })

    unreacting = requests.post(f"{url}/message/unreact", json = {
        'token': user1.json()['token'],
        'message_id': message1id.json()['message_id'],
        'react_id': -1
    })

    assert(unreacting.status_code == 400)


'''
This checks that an input error is raised if a user tries to call unreact to a message they have
not reacted to in the first place.
'''
def test_unreact_havent_reacted(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user2@gmail.com',
        'password' : 'StrongPassword123',
        'name_first' : 'Albert',
        'name_last' : 'Einstein',
    })

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token': user1.json()['token'], 
        'name': "FirstChannel", 
        'is_public': True
    })

    requests.post(f"{url}/channel/invite", json = {
        'token': user1.json()['token'], 
        'channel_id': channel1.json()['channel_id'],
        'u_id': user2.json()['u_id']
    })

    message1id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello"
    })

    requests.post(f"{url}/message/react", json = {
        'token': user2.json()['token'],
        'message_id': message1id.json()['message_id'],
        'react_id': 1
    })
    unreacting = requests.post(f"{url}/message/unreact", json = {
        'token': user1.json()['token'],
        'message_id': message1id.json()['message_id'],
        'react_id': 1
    })

    assert(unreacting.status_code == 400)


'''
A more complex test to check that the message unreact function works when called numerous times
'''
def test_unreact_few(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user2@gmail.com',
        'password' : 'StrongPassword123',
        'name_first' : 'Albert',
        'name_last' : 'Einstein',
    })

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token': user1.json()['token'], 
        'name': "FirstChannel", 
        'is_public': True
    })

    requests.post(f"{url}/channel/invite", json = {
        'token': user1.json()['token'], 
        'channel_id': channel1.json()['channel_id'],
        'u_id': user2.json()['u_id']
    })


    message1id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello"
    })

    message2id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Welcome to the Channel!!"
    })

    message3id = requests.post(f"{url}/message/send", json = { 
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Thanks for adding me!"
    })

    message4id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "No worries!"
    })

    requests.post(f"{url}/message/send", json = { 
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "I can't wait to send more messages"
    })

    requests.post(f"{url}/message/react", json = {
        'token': user1.json()['token'],
        'message_id': message1id.json()['message_id'],
        'react_id': 1
    })
    requests.post(f"{url}/message/react", json = {
        'token': user2.json()['token'],
        'message_id': message1id.json()['message_id'],
        'react_id': 1
    })
    requests.post(f"{url}/message/react", json = {
        'token': user1.json()['token'],
        'message_id': message2id.json()['message_id'],
        'react_id': 1
    })

    requests.post(f"{url}/message/react", json = {
        'token': user2.json()['token'],
        'message_id': message2id.json()['message_id'],
        'react_id': 1
    })
    requests.post(f"{url}/message/react", json = {
        'token': user1.json()['token'],
        'message_id': message3id.json()['message_id'],
        'react_id': 1
    })
    requests.post(f"{url}/message/react", json = {
        'token': user2.json()['token'],
        'message_id': message3id.json()['message_id'],
        'react_id': 1
    })
    requests.post(f"{url}/message/react", json = {
        'token': user1.json()['token'],
        'message_id': message4id.json()['message_id'],
        'react_id': 1
    })
    requests.post(f"{url}/message/react", json = {
        'token': user2.json()['token'],
        'message_id': message4id.json()['message_id'],
        'react_id': 1
    })


    requests.post(f"{url}/message/unreact", json = {
        'token': user2.json()['token'],
        'message_id': message1id.json()['message_id'],
        'react_id': 1
    })
    requests.post(f"{url}/message/unreact", json = {
        'token': user1.json()['token'],
        'message_id': message2id.json()['message_id'],
        'react_id': 1
    })
    requests.post(f"{url}/message/unreact", json = {
        'token': user1.json()['token'],
        'message_id': message3id.json()['message_id'],
        'react_id': 1
    })
    requests.post(f"{url}/message/unreact", json = {
        'token': user2.json()['token'],
        'message_id': message4id.json()['message_id'],
        'react_id': 1
    })

    get_messages1 = requests.get(f"{url}/channel/messages", params = {
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })
    

    assert get_messages1.json()['messages'][1]['reacts'] == [{
        'react_id': 1,
        'u_ids': [user1.json()['u_id']],
        'is_this_user_reacted': False
    }]
    assert get_messages1.json()['messages'][2]['reacts'] == [{
        'react_id': 1,
        'u_ids': [user2.json()['u_id']],
        'is_this_user_reacted': True
    }]
    assert get_messages1.json()['messages'][3]['reacts'] == [{
        'react_id': 1,
        'u_ids': [user2.json()['u_id']],
        'is_this_user_reacted': True
    }]
    assert get_messages1.json()['messages'][4]['reacts'] == [{
        'react_id': 1,
        'u_ids': [user1.json()['u_id']],
        'is_this_user_reacted': False
    }]


'''
A simple test to check that the message sendlater functionality works
'''
def test_sendlater_simple(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user2@gmail.com',
        'password' : 'StrongPassword123',
        'name_first' : 'Albert',
        'name_last' : 'Einstein',
    })

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token': user1.json()['token'], 
        'name': "FirstChannel", 
        'is_public': True
    })

    requests.post(f"{url}/channel/invite", json = {
        'token': user1.json()['token'], 
        'channel_id': channel1.json()['channel_id'],
        'u_id': user2.json()['u_id']
    })
    now = datetime.datetime.now(timezone.utc)
    send_at = now + datetime.timedelta(0,3)

    #Creating integer unix timestamp to pass in
    message_timestamp = int(send_at.replace(tzinfo=timezone.utc).timestamp())

    message1id = requests.post(f"{url}/message/sendlater", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello",
        'time_sent': message_timestamp
    })

    message2id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Welcome to the Channel!!"
    })
    
    get_messages1 = requests.get(f"{url}/channel/messages", params = {
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })

    assert get_messages1.json()['messages'][0]['message'] == "Welcome to the Channel!!"
    assert get_messages1.json()['messages'][0]['message_id'] == message2id.json()['message_id']
    assert len(get_messages1.json()['messages']) == 1

    sleep(5)

    get_messages2 = requests.get(f"{url}/channel/messages", params = {
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })
    assert get_messages2.json()['messages'][0]['message'] == "Hello"
    assert get_messages2.json()['messages'][0]['message_id'] == message1id.json()['message_id']
    assert len(get_messages2.json()['messages']) == 2


'''
This test checks that an access error is raised when an invalid token is passed
'''
def test_sendlater_invalid_token(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user2@gmail.com',
        'password' : 'StrongPassword123',
        'name_first' : 'Albert',
        'name_last' : 'Einstein',
    })

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token': user1.json()['token'], 
        'name': "FirstChannel", 
        'is_public': True
    })

    requests.post(f"{url}/channel/invite", json = {
        'token': user1.json()['token'], 
        'channel_id': channel1.json()['channel_id'],
        'u_id': user2.json()['u_id']
    })
    now = datetime.datetime.now(timezone.utc)
    send_at = now + datetime.timedelta(0,3)

    #Creating integer unix timestamp to pass in
    message_timestamp = int(send_at.replace(tzinfo=timezone.utc).timestamp())

    message1id = requests.post(f"{url}/message/sendlater", json = { 
        'token': -1,
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello",
        'time_sent': message_timestamp
    })
    
    assert(message1id.status_code == 400)


'''
This test checks that an input error is raised if message length is greater than 1000 chars.
'''
def test_sendlater_too_long(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user2@gmail.com',
        'password' : 'StrongPassword123',
        'name_first' : 'Albert',
        'name_last' : 'Einstein',
    })

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token': user1.json()['token'], 
        'name': "FirstChannel", 
        'is_public': True
    })

    requests.post(f"{url}/channel/invite", json = {
        'token': user1.json()['token'], 
        'channel_id': channel1.json()['channel_id'],
        'u_id': user2.json()['u_id']
    })
    now = datetime.datetime.now(timezone.utc)
    send_at = now + datetime.timedelta(0,3)

    #Creating integer unix timestamp to pass in
    message_timestamp = int(send_at.replace(tzinfo=timezone.utc).timestamp())
    message = "A" * 1001
    message1id = requests.post(f"{url}/message/sendlater", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': message,
        'time_sent': message_timestamp
    })
    
    assert(message1id.status_code == 400)


'''
This test checks that an access error is raised if the authorised user is not a member of the channel
they are trying to send a message later to.
'''
def test_sendlater_not_a_member(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user2@gmail.com',
        'password' : 'StrongPassword123',
        'name_first' : 'Albert',
        'name_last' : 'Einstein',
    })

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token': user1.json()['token'], 
        'name': "FirstChannel", 
        'is_public': True
    })

    now = datetime.datetime.now(timezone.utc)
    send_at = now + datetime.timedelta(0,3)

    #Creating integer unix timestamp to pass in
    message_timestamp = int(send_at.replace(tzinfo=timezone.utc).timestamp())

    message1id = requests.post(f"{url}/message/sendlater", json = { 
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello",
        'time_sent': message_timestamp
    })
    
    assert(message1id.status_code == 400)


'''
This test checks that an input error is raised when an invalid channel ID is passed
'''
def test_sendlater_invalid_channel_id(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })

    now = datetime.datetime.now(timezone.utc)
    send_at = now + datetime.timedelta(0,3)

    #Creating integer unix timestamp to pass in
    message_timestamp = int(send_at.replace(tzinfo=timezone.utc).timestamp())

    message1id = requests.post(f"{url}/message/sendlater", json = { 
        'token': user1.json()['token'],
        'channel_id': -1,
        'message': "Hello",
        'time_sent': message_timestamp
    })
    
    assert(message1id.status_code == 400)


'''
This test checks that an input error is raised if the scheduled time of the message is in the past
'''
def test_sendlater_time_in_past(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token': user1.json()['token'], 
        'name': "FirstChannel", 
        'is_public': True
    })

    now = datetime.datetime.now(timezone.utc)
    send_at = now + datetime.timedelta(0,-3)

    #Creating integer unix timestamp to pass in
    message_timestamp = int(send_at.replace(tzinfo=timezone.utc).timestamp())

    message1id = requests.post(f"{url}/message/sendlater", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello",
        'time_sent': message_timestamp
    })
    
    assert(message1id.status_code == 400)


'''
A more complex test to check that message_sendlater works when called multiple times
'''
def test_sendlater_more(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user2@gmail.com',
        'password' : 'StrongPassword123',
        'name_first' : 'Albert',
        'name_last' : 'Einstein',
    })

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token': user1.json()['token'], 
        'name': "FirstChannel", 
        'is_public': True
    })

    requests.post(f"{url}/channel/invite", json = {
        'token': user1.json()['token'], 
        'channel_id': channel1.json()['channel_id'],
        'u_id': user2.json()['u_id']
    })
    now = datetime.datetime.now(timezone.utc)
    send_at = now + datetime.timedelta(0,2)
    send_at2 = now + datetime.timedelta(0,5)
    send_at3 = now + datetime.timedelta(0,10)

    #Creating integer unix timestamp to pass in
    message_timestamp = int(send_at.replace(tzinfo=timezone.utc).timestamp())
    message_timestamp2 = int(send_at2.replace(tzinfo=timezone.utc).timestamp())
    message_timestamp3 = int(send_at3.replace(tzinfo=timezone.utc).timestamp())

    message1id = requests.post(f"{url}/message/sendlater", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello",
        'time_sent': message_timestamp3
    })

    message2id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Welcome to the Channel!!"
    })
    message3id = requests.post(f"{url}/message/sendlater", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hi there",
        'time_sent': message_timestamp
    })
    message4id = requests.post(f"{url}/message/sendlater", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hope you see this later",
        'time_sent': message_timestamp2
    })

    get_messages1 = requests.get(f"{url}/channel/messages", params = {
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })

    assert get_messages1.json()['messages'][0]['message'] == "Welcome to the Channel!!"
    assert len(get_messages1.json()['messages']) == 1

    sleep(4)
    get_messages2 = requests.get(f"{url}/channel/messages", params = {
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })
    assert get_messages2.json()['messages'][0]['message'] == "Hi there"
    assert len(get_messages2.json()['messages']) == 2

    sleep(5)
    get_messages3 = requests.get(f"{url}/channel/messages", params = {
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })
    assert get_messages3.json()['messages'][0]['message'] == "Hope you see this later"
    assert len(get_messages3.json()['messages']) == 3

    sleep(5)
    get_messages4 = requests.get(f"{url}/channel/messages", params = {
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })
    assert len(get_messages4.json()['messages']) == 4
    assert get_messages4.json()['messages'][0]['message_id'] == message1id.json()['message_id']
    assert get_messages4.json()['messages'][1]['message_id'] == message4id.json()['message_id']
    assert get_messages4.json()['messages'][2]['message_id'] == message3id.json()['message_id']
    assert get_messages4.json()['messages'][3]['message_id'] == message2id.json()['message_id']
    assert get_messages4.json()['messages'][0]['message'] == "Hello"

'''
A more complex test to check that message_sendlater works when called multiple times
'''
def test_sendlater_more2(url):
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user1@gmail.com',
        'password' : 'Password1234',
        'name_first' : 'Paul',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'user2@gmail.com',
        'password' : 'StrongPassword123',
        'name_first' : 'Albert',
        'name_last' : 'Einstein',
    })

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token': user1.json()['token'], 
        'name': "FirstChannel", 
        'is_public': True
    })

    requests.post(f"{url}/channel/invite", json = {
        'token': user1.json()['token'], 
        'channel_id': channel1.json()['channel_id'],
        'u_id': user2.json()['u_id']
    })

    now = datetime.datetime.now(timezone.utc)
    send_at = now + datetime.timedelta(0,3)
    send_at2 = now + datetime.timedelta(0,7)

    #Creating integer unix timestamp to pass in
    message_timestamp = int(send_at.replace(tzinfo=timezone.utc).timestamp())
    message_timestamp2 = int(send_at2.replace(tzinfo=timezone.utc).timestamp())

    message1id = requests.post(f"{url}/message/sendlater", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello",
        'time_sent': message_timestamp
    })

    message2id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Welcome to the Channel!!"
    })
    message3id = requests.post(f"{url}/message/sendlater", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hi there",
        'time_sent': message_timestamp2
    })

    get_messages1 = requests.get(f"{url}/channel/messages", params = {
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })

    assert get_messages1.json()['messages'][0]['message'] == "Welcome to the Channel!!"
    assert len(get_messages1.json()['messages']) == 1

    sleep(5)
    get_messages2 = requests.get(f"{url}/channel/messages", params = {
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })

    assert len(get_messages2.json()['messages']) == 2
    assert get_messages2.json()['messages'][0]['message'] == "Hello"
    assert get_messages2.json()['messages'][1]['message'] == "Welcome to the Channel!!"
    assert get_messages2.json()['messages'][0]['message_id'] == message1id.json()['message_id']
    assert get_messages2.json()['messages'][1]['message_id'] == message2id.json()['message_id']

    sleep(4)
    get_messages3 = requests.get(f"{url}/channel/messages", params = {
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })

    assert len(get_messages3.json()['messages']) == 3
    assert get_messages3.json()['messages'][0]['message'] == "Hi there"
    assert get_messages3.json()['messages'][0]['message_id'] == message3id.json()['message_id']
    assert get_messages3.json()['messages'][1]['message_id'] == message1id.json()['message_id']
    assert get_messages3.json()['messages'][2]['message_id'] == message2id.json()['message_id']
