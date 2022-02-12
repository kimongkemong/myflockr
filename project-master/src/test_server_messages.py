import pytest
import error
import json

import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests

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
Simple test to check that a single message can be sent
'''
def test_send_message(url):
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

    get_messages1 = requests.get(f"{url}/channel/messages", params = {
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })
    
    assert get_messages1.json()['messages'][0]['message'] == "Hello"
    assert get_messages1.json()['end'] == -1 
    assert get_messages1.json()['messages'][0]['message_id'] == message1id.json()['message_id']

'''
This test checks that a few message can be sent and are correctly returned using the channel_messages functionality
'''
def test_message_send_few(url):
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

    message2id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Welcome to the First Channel!!"
    })
    message3id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Please enjoy your stay!"
    })

    get_messages1 = requests.get(f"{url}/channel/messages", params = {
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })

    assert get_messages1.json()['messages'][0]['message'] == "Please enjoy your stay!"
    assert get_messages1.json()['end'] == -1 
    assert get_messages1.json()['messages'][0]['message_id'] == message3id.json()['message_id']
    assert len(get_messages1.json()['messages']) == 3
    assert get_messages1.json()['messages'][2]['message'] == "Hello"

    assert get_messages1.json()['messages'][0]['message_id'] == message3id.json()['message_id']
    assert get_messages1.json()['messages'][1]['message_id'] == message2id.json()['message_id']
    assert get_messages1.json()['messages'][2]['message_id'] == message1id.json()['message_id']

    assert get_messages1.json()['messages'][0]['u_id'] == user1.json()['u_id']
    assert get_messages1.json()['messages'][1]['u_id'] == user1.json()['u_id']
    assert get_messages1.json()['messages'][2]['u_id'] == user1.json()['u_id']

'''
Messages over the length of 1000 characters will raise an input error
'''
def test_message_too_long(url):
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

    long_message = "A" * 1001
    message1id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': long_message
    })
    
    assert(message1id.status_code == 400)

'''
Access error raised if user is not a part of the channel which they are trying to send a message in
'''
def test_message_send_unauthorised(url):
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
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello"
    })

    assert(message1id.status_code == 400)

'''
This test sends many messages to check that channel/messages only returns the 50 most recent messages.
'''
def test_message_send_many(url):
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


    message_ids = []
    i = 0

    m_id = {}
    while i < 55:
        if i % 2 == 0:
            m_id = requests.post(f"{url}/message/send", json = { 
                'token': user1.json()['token'],
                'channel_id': channel1.json()['channel_id'],
                'message': "Hello from user 1"
            })
            message_ids.insert(0, m_id.json())
        
        else:
            m_id = requests.post(f"{url}/message/send", json = { 
                'token': user2.json()['token'],
                'channel_id': channel1.json()['channel_id'],
                'message': "Hello from user 2"
            })
            message_ids.insert(0, m_id.json())
        
        i += 1


    get_messages1 = requests.get(f"{url}/channel/messages", params = {
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })

    assert get_messages1.json()['messages'][0]['message'] == "Hello from user 1"
    assert get_messages1.json()['end'] == 50
    assert len(get_messages1.json()['messages']) == 50
    assert get_messages1.json()['messages'][49]['message'] == "Hello from user 2"

    assert get_messages1.json()['messages'][0]['u_id'] == user1.json()['u_id']
    assert get_messages1.json()['messages'][1]['u_id'] == user2.json()['u_id']
    assert get_messages1.json()['messages'][48]['u_id'] == user1.json()['u_id']
    assert get_messages1.json()['messages'][49]['u_id'] == user2.json()['u_id']

    assert get_messages1.json()['messages'][0]['message_id'] == message_ids[0]['message_id']
    assert get_messages1.json()['messages'][1]['message_id'] == message_ids[1]['message_id']
    assert get_messages1.json()['messages'][48]['message_id'] == message_ids[48]['message_id']
    assert get_messages1.json()['messages'][49]['message_id'] == message_ids[49]['message_id']

'''
Simple test to check that a message/remove works properly 
'''
def test_message_delete(url):
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

    message2id = requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Welcome to the Channel!"
    })

    requests.delete(f"{url}/message/remove", json = {
        'token': user1.json()['token'],
        'message_id': message1id.json()['message_id']
    })
    
    get_messages1 = requests.get(f"{url}/channel/messages", params = {
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })

    assert get_messages1.json()['messages'][0]['message'] == "Welcome to the Channel!"
    assert get_messages1.json()['end'] == -1
    assert len(get_messages1.json()['messages']) == 1
    assert get_messages1.json()['messages'][0]['u_id'] == user1.json()['u_id']
    assert get_messages1.json()['messages'][0]['message_id'] == message2id.json()['message_id']
    
    #Input error raised if message has already been deleted
    result = requests.delete(f"{url}/message/remove", json = {
        'token': user1.json()['token'],
        'message_id': message1id.json()['message_id']
    })
    assert(result.status_code == 400)


'''
Test to ensure that an owner of the channnel can remove a message that they did not send.
'''
def test_message_owner_remove(url):
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
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hi there!"
    })

    requests.delete(f"{url}/message/remove", json = {
        'token': user1.json()['token'],
        'message_id': message2id.json()['message_id']
    })

    get_messages1 = requests.get(f"{url}/channel/messages", params = {
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })
    

    assert get_messages1.json()['messages'][0]['message'] == "Hello"
    assert get_messages1.json()['end'] == -1
    assert len(get_messages1.json()['messages']) == 1
    assert get_messages1.json()['messages'][0]['u_id'] == user1.json()['u_id']
    assert get_messages1.json()['messages'][0]['message_id'] == message1id.json()['message_id']


'''
Access error raised if a member in a channel (not an owner) tries to remove a message that they did not send
'''
def test_message_remove_unathorised(url):
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

    requests.post(f"{url}/message/send", json = { 
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hi there!"
    })

    result = requests.delete(f"{url}/message/remove", json = {
        'token': user2.json()['token'],
        'message_id': message1id.json()['message_id']
    })

    # access error if not authorised to remove message
    assert(result.status_code == 400)

'''
This test checks that many messages are removed effectively
'''
def test_remove_many(url):
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


    message_ids = []
    i = 0

    m_id = {}
    while i < 60:
        if i % 2 == 0:
            m_id = requests.post(f"{url}/message/send", json = { 
                'token': user1.json()['token'],
                'channel_id': channel1.json()['channel_id'],
                'message': "Hello from user 1"
            })
            message_ids.insert(0, m_id.json())
        
        else:
            m_id = requests.post(f"{url}/message/send", json = { 
                'token': user2.json()['token'],
                'channel_id': channel1.json()['channel_id'],
                'message': "Hello from user 2"
            })
            message_ids.insert(0, m_id.json())
        
        i += 1


    get_messages1 = requests.get(f"{url}/channel/messages", params = {
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })

    i = 0

    while i < 30:
        requests.delete(f"{url}/message/remove", json = {
            'token': user1.json()['token'],
            'message_id': message_ids[i]['message_id']
        })
        i+=1

    get_messages1 = requests.get(f"{url}/channel/messages", params = {
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })



    assert get_messages1.json()['messages'][0]['message'] == "Hello from user 2"
    assert get_messages1.json()['end'] == -1
    assert len(get_messages1.json()['messages']) == 30
    assert get_messages1.json()['messages'][29]['message'] == "Hello from user 1"

    assert get_messages1.json()['messages'][0]['u_id'] == user2.json()['u_id']
    assert get_messages1.json()['messages'][1]['u_id'] == user1.json()['u_id']
    assert get_messages1.json()['messages'][28]['u_id'] == user2.json()['u_id']
    assert get_messages1.json()['messages'][29]['u_id'] == user1.json()['u_id']

    assert get_messages1.json()['messages'][0]['message_id'] == message_ids[30]['message_id']
    assert get_messages1.json()['messages'][1]['message_id'] == message_ids[31]['message_id']
    assert get_messages1.json()['messages'][28]['message_id'] == message_ids[58]['message_id']
    assert get_messages1.json()['messages'][29]['message_id'] == message_ids[59]['message_id']

'''
Input error raised if the message trying to be removed is not real
'''
def test_message_not_real(url):
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
    requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Welcome to the Channel!!"
    })

    result = requests.delete(f"{url}/message/remove", json = {
            'token': user1.json()['token'],
            'message_id': -1
        })

    assert(result.status_code == 400)

'''
Access error raised if the token of the user trying to get the messages is not in active tokens
'''
def test_get_messages_error1(url):
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
    requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Welcome to the Channel!!"
    })
    get_messages1 = requests.get(f"{url}/channel/messages", params = {
        'token': -1,
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })

    assert(get_messages1.status_code == 400)


'''
Input error raised if the channel does not exist
'''
def test_messages_error2(url):
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
    requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Welcome to the Channel!!"
    })
    get_messages1 = requests.get(f"{url}/channel/messages", params = {
        'token': user1.json()['token'],
        'channel_id': -1,
        'start': 0
    })

    assert(get_messages1.status_code == 400)

'''
Access error raised if the user is not a member of the channel
'''
def test_messages_error3(url):
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

    requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello"
    })
    requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Welcome to the Channel!!"
    })
    get_messages1 = requests.get(f"{url}/channel/messages", params = {
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })

    assert(get_messages1.status_code == 400)

'''
Input error raised if start position is greater than number of messages in the channel
'''
def test_messages_error4(url):
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
    requests.post(f"{url}/message/send", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Welcome to the Channel!!"
    })
    get_messages1 = requests.get(f"{url}/channel/messages", params = {
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 5
    })

    assert(get_messages1.status_code == 400)
