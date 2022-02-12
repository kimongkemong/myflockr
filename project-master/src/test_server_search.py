import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json

# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
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

def test_echo(url):
    '''
    A simple test to check echo
    '''
    resp = requests.get(url + 'echo', params={'data': 'hello'})
    assert json.loads(resp.text) == {'data': 'hello'}

def test_server_search(url):
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'Dobbyis_Afree_elf',
        'name_first' : 'Harry',
        'name_last' : 'Potter',
    })
    assert user1.status_code == 200

    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'hermione_granger12@gmail.com',
        'password' : 'Wingardium_leviosa',
        'name_first' : 'Hermione',
        'name_last' : 'Granger',
    })
    assert user2.status_code == 200

    user3 = requests.post(f"{url}/auth/register", json = {
        'email' : 'ronweasley@gmail.com',
        'password' : 'ginny_lil_sis',
        'name_first' : 'Ron',
        'name_last' : 'Weasley',
    })
    assert user3.status_code == 200

    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user1.json()['token'],
        'name' : 'hogwards',
        'is_public' : False,
    })
    assert ch_1.status_code == 200

    test1 = requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user3.json()['u_id'],
    })
    assert test1.status_code == 200

    test2 = requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    assert test2.status_code == 200

    test3 = requests.post(f"{url}/message/send", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : "I'm Harry Potter",
    })
    assert test3.status_code == 200

    test4 = requests.post(f"{url}/message/send", json = {
        'token' : user2.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : "Hello I'm Ron",
    })
    assert test4.status_code == 200

    test5 = requests.post(f"{url}/message/send", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : "Great to see you guys",
    })
    assert test5.status_code == 200

    test6 = requests.post(f"{url}/message/send", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : "My name's Hermione, I'm from England",
    })
    assert test6.status_code == 200

    get_message = requests.get(f"{url}/channel/messages", params = {
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id'],
        'start': 0
    })
    assert get_message.status_code == 200

    found = requests.get(f"{url}/search", params = {
        'token': user1.json()['token'],
        'query_str': "I'm",
    })
    assert found.status_code == 200

    assert found.json() == {'messages': [
        {'message_id': get_message.json()['messages'][0]['message_id'],
         'u_id': get_message.json()['messages'][0]['u_id'],
         'message': get_message.json()['messages'][0]['message'],
         'time_created': get_message.json()['messages'][0]['time_created'],
         'reacts': get_message.json()['messages'][0]['reacts'],
         'is_pinned': get_message.json()['messages'][0]['is_pinned']
        },
        {'message_id': get_message.json()['messages'][2]['message_id'],
         'u_id': get_message.json()['messages'][2]['u_id'],
         'message': get_message.json()['messages'][2]['message'],
         'time_created': get_message.json()['messages'][2]['time_created'],
         'reacts': get_message.json()['messages'][2]['reacts'],
         'is_pinned': get_message.json()['messages'][2]['is_pinned']
        },
        {'message_id': get_message.json()['messages'][3]['message_id'],
         'u_id': get_message.json()['messages'][3]['u_id'],
         'message': get_message.json()['messages'][3]['message'],
         'time_created': get_message.json()['messages'][3]['time_created'],
         'reacts': get_message.json()['messages'][3]['reacts'],
         'is_pinned': get_message.json()['messages'][3]['is_pinned']
        }],}

def test_server_search_notfound(url):

    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'Dobbyis_Afree_elf',
        'name_first' : 'Harry',
        'name_last' : 'Potter',
    })
    assert user1.status_code == 200

    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'hermione_granger12@gmail.com',
        'password' : 'Wingardium_leviosa',
        'name_first' : 'Hermione',
        'name_last' : 'Granger',
    })
    assert user2.status_code == 200

    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user1.json()['token'],
        'name' : 'hogwards',
        'is_public' : False,
    })
    assert ch_1.status_code == 200

    test1 = requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    assert test1.status_code == 200

    test3 = requests.post(f"{url}/message/send", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : "How R u?",
    })
    assert test3.status_code == 200

    test4 = requests.post(f"{url}/message/send", json = {
        'token' : user2.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : "Awesome...",
    })
    assert test4.status_code == 200

    found = requests.get(f"{url}/search", params = {
        'token': user1.json()['token'],
        'query_str': "Good Morning",
    })
    assert found.status_code == 400

def test_server_search_lower_upper(url):
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'samsmith@gmail.com',
        'password' : 'TooGoodToSayGoodbye',
        'name_first' : 'Sam',
        'name_last' : 'Smith',
    })
    assert user1.status_code == 200

    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'adele@gmail.com',
        'password' : '1sing_veryW3ll',
        'name_first' : 'Adele',
        'name_last' : 'Singer',
    })
    assert user2.status_code == 200

    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user1.json()['token'],
        'name' : 'Soloist',
        'is_public' : False,
    })
    assert ch_1.status_code == 200

    test1 = requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    assert test1.status_code == 200

    test2 = requests.post(f"{url}/message/send", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : "Hello Adele",
    })
    assert test2.status_code == 200

    test3 = requests.post(f"{url}/message/send", json = {
        'token' : user2.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : "hello, Sam Smith!!",
    })
    assert test3.status_code == 200

    test4 = requests.post(f"{url}/message/send", json = {
        'token' : user2.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : "heLLo..... everybody",
    })
    assert test4.status_code == 200

    get_message = requests.get(f"{url}/channel/messages", params = {
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id'],
        'start': 0
    })
    assert get_message.status_code == 200
    
    found = requests.get(f"{url}/search", params = {
        'token': user1.json()['token'],
        'query_str': "heLLo",
    })
    assert found.json() == {'messages': [
        {'message_id': get_message.json()['messages'][0]['message_id'],
         'u_id': get_message.json()['messages'][0]['u_id'],
         'message': get_message.json()['messages'][0]['message'],
         'time_created': get_message.json()['messages'][0]['time_created'],
         'reacts': get_message.json()['messages'][0]['reacts'],
         'is_pinned': get_message.json()['messages'][0]['is_pinned']
        }],}

