'''testing for all function in channels.py'''
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import json
import pytest
import requests

# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def url():
    '''generate url'''
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

def test_all_function_channels(url):
    '''Simple test for every function in channels'''
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'samsmith@gmail.com',
        'password' : 'TooGoodToSayGoodbye',
        'name_first' : 'Sam',
        'name_last' : 'Smith',
    })

    ch_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1.json()['token'],
        'name' : 'Channel1',
        'is_public' : True,
    })
    assert ch_1.json() == {'channel_id': 1}

    ch_all = requests.get(f"{url}/channels/listall", params={
        'token' : user1.json()['token']
    })
    assert ch_all.json() == {"channels": [{"channel_id": ch_1.json()['channel_id'],
                                           "name": "Channel1"}]}

    ch_list = requests.get(f"{url}/channels/list", params={
        'token' : user1.json()['token']
        })
    assert ch_list.json() == {'channels': [{'channel_id': 1, 'name': 'Channel1'}]}

def test_channels_function(url):
    '''More test to every function in Channels'''
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'testemail1@email.com',
        'password' : 'testpassword',
        'name_first' : 'test',
        'name_last' : 'program',
    })

    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'testemail2@email.com',
        'password' : 'testpassword',
        'name_first' : 'test2',
        'name_last' : 'program2',
    })

    user3 = requests.post(f"{url}/auth/register", json={
        'email' : 'testemail3@email.com',
        'password' : 'testpassword',
        'name_first' : 'test3',
        'name_last' : 'program3',
    })

    ch_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1.json()['token'],
        'name' : 'channel1',
        'is_public' : True,
    })
    assert ch_1.json() == {'channel_id': 1}

    ch_2 = requests.post(f"{url}/channels/create", json={
        'token' : user2.json()['token'],
        'name' : 'channel2',
        'is_public' : True
        })
    assert ch_2.json() == {'channel_id': 2}

    ch_3 = requests.post(f"{url}/channels/create", json={
        'token' : user3.json()['token'],
        'name' : 'channel3',
        'is_public' : False
        })
    assert ch_3.json() == {'channel_id': 3}

    ch_4 = requests.post(f"{url}/channels/create", json={
        'token' : user1.json()['token'],
        'name' : 'channel4',
        'is_public' : False
        })
    assert ch_4.json() == {'channel_id': 4}

    ch_all = requests.get(f"{url}/channels/listall", params={
        'token' : user1.json()['token'],
    })
    assert ch_all.json() == {'channels': [{'channel_id': 1, 'name': 'channel1'},
                                          {'channel_id': 2, 'name': 'channel2'},
                                          {'channel_id': 3, 'name': 'channel3'},
                                          {'channel_id': 4, 'name': 'channel4'}
                                         ]}

    ch_list = requests.get(f"{url}/channels/list", params={
        'token' : user2.json()['token'],
        })
    assert ch_list.json() == {'channels': [{'channel_id': 2, 'name': 'channel2'}]}

    ch_list = requests.get(f"{url}/channels/list", params={
        'token' : user1.json()['token'],
        })
    assert ch_list.json() == {'channels': [{'channel_id': 1, 'name': 'channel1'},
                                           {'channel_id': 4, 'name': 'channel4'}]}

def test_channels_fucntion_error(url):
    '''Testing scenario for error in each funciton'''
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'testemail1@email.com',
        'password' : 'testpassword',
        'name_first' : 'test',
        'name_last' : 'program',
    })

    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'testemail2@email.com',
        'password' : 'testpassword',
        'name_first' : 'test2',
        'name_last' : 'program2',
    })

    ch_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1.json()['token'],
        'name' : 'channel1',
        'is_public' : True,
    })
    assert ch_1.json() == {'channel_id': 1}

    ch_2 = requests.post(f"{url}/channels/create", json={
        'token' : user2.json()['token'],
        'name' : 'channel2',
        'is_public' : True
        })
    assert ch_2.json() == {'channel_id': 2}

    #creating a channel with invalid token
    ch_3 = requests.post(f"{url}/channels/create", json={
        'token' : 12,
        'name' : 'channel3',
        'is_public' : False
        })
    assert ch_3.status_code == 400

    #creating a channel with a long name

    ch_4 = requests.post(f"{url}/channels/create", json={
        'token' : user1.json()['token'],
        'name' : 'channelwithlongname123456478910',
        'is_public' : True
        })
    assert ch_4.status_code == 400

    ch_5 = requests.post(f"{url}/channels/create", json={
        'token' : user1.json()['token'],
        'name' : 'channel3',
        'is_public' : True
        })
    assert ch_5.json() == {'channel_id': 3}

    ch_all = requests.get(f"{url}/channels/listall", params={
        'token' : user1.json()['token'],
    })
    assert ch_all.json() == {'channels': [{'channel_id': 1, 'name': 'channel1'},
                                          {'channel_id': 2, 'name': 'channel2'},
                                          {'channel_id': 3, 'name': 'channel3'}
                                         ]}

    # listing all channel with invalid tokens
    ch_all = requests.get(f"{url}/channels/listall", params={
        'token' : 1234,
    })
    assert ch_all.status_code == 400

    # listing the user channel success
    ch_list = requests.get(f"{url}/channels/list", params={
        'token' : user1.json()['token'],
        })
    assert ch_list.json() == {'channels': [{'channel_id': 1, 'name': 'channel1'},
                                           {'channel_id': 3, 'name': 'channel3'}]}

    # listing the user channel with invalid token
    ch_list = requests.get(f"{url}/channels/list", params={
        'token' : 1235,
        })
    assert ch_list.status_code == 400
