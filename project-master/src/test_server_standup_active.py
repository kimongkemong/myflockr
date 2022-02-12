from datetime import datetime
import pytest
import error
import json
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests


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


###################### SERVER TEST FOR STANDUP_ACTIVE ##########################

def test_standup_active_server(url):
    '''
    test standup_start_active with its normal behaviour
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'samsmith@gmail.com',
        'password' : 'TooGoodToSayGoodbye',
        'name_first' : 'Sam',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'adele@gmail.com',
        'password' : '1sing_veryW3ll',
        'name_first' : 'Adele',
        'name_last' : 'Singer',
    })
    ch_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1.json()['token'],
        'name' : 'Soloist',
        'is_public' : True,
    })
    requests.post(f"{url}/channel/invite", json={
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    length = 5
    finish = requests.post(f"{url}/standup/start", json={
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'length' : length,
    })
    sleep(2)
    active = requests.get(f"{url}/standup/active", params={
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    assert active.json() == {'is_active': True, 'time_finish': finish.json()}
    sleep(length)
    active = requests.get(f"{url}/standup/active", params={
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    assert active.json() == {'is_active': False, 'time_finish': None}

def test_standup_active_server_other_member(url):
    '''
    test standup_start_active with other member accessing the active
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'samsmith@gmail.com',
        'password' : 'TooGoodToSayGoodbye',
        'name_first' : 'Sam',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'adele@gmail.com',
        'password' : '1sing_veryW3ll',
        'name_first' : 'Adele',
        'name_last' : 'Singer',
    })
    ch_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1.json()['token'],
        'name' : 'Soloist',
        'is_public' : True,
    })
    requests.post(f"{url}/channel/invite", json={
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    length = 5
    finish = requests.post(f"{url}/standup/start", json={
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'length' : length,
    })
    sleep(2)
    active = requests.get(f"{url}/standup/active", params={
        'token': user2.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    assert active.json() == {'is_active': True, 'time_finish': finish.json()}
    sleep(length)
    active = requests.get(f"{url}/standup/active", params={
        'token': user2.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    assert active.json() == {'is_active': False, 'time_finish': None}

def test_standup_active_server_multi_ch(url):
    '''
    test standup_start_active with multiple channel
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'samsmith@gmail.com',
        'password' : 'TooGoodToSayGoodbye',
        'name_first' : 'Sam',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'adele@gmail.com',
        'password' : '1sing_veryW3ll',
        'name_first' : 'Adele',
        'name_last' : 'Singer',
    })
    ch_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1.json()['token'],
        'name' : 'Soloist',
        'is_public' : True,
    })
    ch_2 = requests.post(f"{url}/channels/create", json={
        'token' : user2.json()['token'],
        'name' : 'Double',
        'is_public' : False,
    })
    requests.post(f"{url}/channel/invite", json={
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    length = 5
    finish1 = requests.post(f"{url}/standup/start", json={
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'length' : length,
    })
    finish2 = requests.post(f"{url}/standup/start", json={
        'token' : user2.json()['token'],
        'channel_id' : ch_2.json()['channel_id'],
        'length' : length,
    })
    sleep(2)
    active1 = requests.get(f"{url}/standup/active", params={
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    active2 = requests.get(f"{url}/standup/active", params={
        'token': user2.json()['token'],
        'channel_id': ch_2.json()['channel_id']
    })
    assert active1.json() == {'is_active': True, 'time_finish': finish1.json()}
    assert active2.json() == {'is_active': True, 'time_finish': finish2.json()}
    sleep(length)
    active1 = requests.get(f"{url}/standup/active", params={
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    active2 = requests.get(f"{url}/standup/active", params={
        'token': user2.json()['token'],
        'channel_id': ch_2.json()['channel_id']
    })
    assert active1.json() == {'is_active': False, 'time_finish': None}
    assert active2.json() == {'is_active': False, 'time_finish': None}

def test_standup_active_server_multi_ch_different_time(url):
    '''
    test standup_start_active with multiple channel and different
    time of active
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'samsmith@gmail.com',
        'password' : 'TooGoodToSayGoodbye',
        'name_first' : 'Sam',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'adele@gmail.com',
        'password' : '1sing_veryW3ll',
        'name_first' : 'Adele',
        'name_last' : 'Singer',
    })
    ch_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1.json()['token'],
        'name' : 'Soloist',
        'is_public' : True,
    })
    ch_2 = requests.post(f"{url}/channels/create", json={
        'token' : user2.json()['token'],
        'name' : 'Double',
        'is_public' : False,
    })
    requests.post(f"{url}/channel/invite", json={
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    length1 = 5
    length2 = 10
    requests.post(f"{url}/standup/start", json={
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'length' : length1,
    })
    finish2 = requests.post(f"{url}/standup/start", json={
        'token' : user2.json()['token'],
        'channel_id' : ch_2.json()['channel_id'],
        'length' : length2,
    })
    sleep(6)
    active1 = requests.get(f"{url}/standup/active", params={
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    active2 = requests.get(f"{url}/standup/active", params={
        'token': user2.json()['token'],
        'channel_id': ch_2.json()['channel_id']
    })
    assert active1.json() == {'is_active': False, 'time_finish': None}
    assert active2.json() == {'is_active': True, 'time_finish': finish2.json()}
    sleep(length2)
    active1 = requests.get(f"{url}/standup/active", params={
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    active2 = requests.get(f"{url}/standup/active", params={
        'token': user2.json()['token'],
        'channel_id': ch_2.json()['channel_id']
    })
    assert active1.json() == {'is_active': False, 'time_finish': None}
    assert active2.json() == {'is_active': False, 'time_finish': None}

def test_standup_active_server_multi_ch_double_standup(url):
    '''
    test standup_start_active with multiple channel and active
    another one after finish
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'samsmith@gmail.com',
        'password' : 'TooGoodToSayGoodbye',
        'name_first' : 'Sam',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'adele@gmail.com',
        'password' : '1sing_veryW3ll',
        'name_first' : 'Adele',
        'name_last' : 'Singer',
    })
    ch_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1.json()['token'],
        'name' : 'Soloist',
        'is_public' : True,
    })
    ch_2 = requests.post(f"{url}/channels/create", json={
        'token' : user2.json()['token'],
        'name' : 'Double',
        'is_public' : False,
    })
    requests.post(f"{url}/channel/invite", json={
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    length1 = 5
    length2 = 10
    requests.post(f"{url}/standup/start", json={
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'length' : length1,
    })
    finish2 = requests.post(f"{url}/standup/start", json={
        'token' : user2.json()['token'],
        'channel_id' : ch_2.json()['channel_id'],
        'length' : length2,
    })
    sleep(6)
    active1 = requests.get(f"{url}/standup/active", params={
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    active2 = requests.get(f"{url}/standup/active", params={
        'token': user2.json()['token'],
        'channel_id': ch_2.json()['channel_id']
    })
    assert active1.json() == {'is_active': False, 'time_finish': None}
    assert active2.json() == {'is_active': True, 'time_finish': finish2.json()}
    sleep(length2)
    active1 = requests.get(f"{url}/standup/active", params={
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    active2 = requests.get(f"{url}/standup/active", params={
        'token': user2.json()['token'],
        'channel_id': ch_2.json()['channel_id']
    })
    assert active1.json() == {'is_active': False, 'time_finish': None}
    assert active2.json() == {'is_active': False, 'time_finish': None}
    finish2 = requests.post(f"{url}/standup/start", json={
        'token' : user2.json()['token'],
        'channel_id' : ch_2.json()['channel_id'],
        'length' : length2,
    })
    sleep(2)
    active2 = requests.get(f"{url}/standup/active", params={
        'token': user2.json()['token'],
        'channel_id': ch_2.json()['channel_id']
    })
    assert active2.json() == {'is_active': True, 'time_finish': finish2.json()}
    sleep(length2)
    active2 = requests.get(f"{url}/standup/active", params={
        'token': user2.json()['token'],
        'channel_id': ch_2.json()['channel_id']
    })
    assert active2.json() == {'is_active': False, 'time_finish': None}

def test_standup_active_server_multi_ch_one_not_active(url):
    '''
    test standup_start_active with multiple channel and
    one of the channel do not have any standup active
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'samsmith@gmail.com',
        'password' : 'TooGoodToSayGoodbye',
        'name_first' : 'Sam',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'adele@gmail.com',
        'password' : '1sing_veryW3ll',
        'name_first' : 'Adele',
        'name_last' : 'Singer',
    })
    ch_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1.json()['token'],
        'name' : 'Soloist',
        'is_public' : True,
    })
    ch_2 = requests.post(f"{url}/channels/create", json={
        'token' : user2.json()['token'],
        'name' : 'Double',
        'is_public' : False,
    })
    requests.post(f"{url}/channel/invite", json={
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    length2 = 10
    finish2 = requests.post(f"{url}/standup/start", json={
        'token' : user2.json()['token'],
        'channel_id' : ch_2.json()['channel_id'],
        'length' : length2,
    })
    sleep(6)
    active1 = requests.get(f"{url}/standup/active", params={
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    active2 = requests.get(f"{url}/standup/active", params={
        'token': user2.json()['token'],
        'channel_id': ch_2.json()['channel_id']
    })
    assert active1.json() == {'is_active': False, 'time_finish': None}
    assert active2.json() == {'is_active': True, 'time_finish': finish2.json()}
    sleep(length2)
    active1 = requests.get(f"{url}/standup/active", params={
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    active2 = requests.get(f"{url}/standup/active", params={
        'token': user2.json()['token'],
        'channel_id': ch_2.json()['channel_id']
    })
    assert active1.json() == {'is_active': False, 'time_finish': None}
    assert active2.json() == {'is_active': False, 'time_finish': None}

def test_standup_active_server_channel_not_found(url):
    '''
    test standup_start_active with invalid channel id
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'samsmith@gmail.com',
        'password' : 'TooGoodToSayGoodbye',
        'name_first' : 'Sam',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'adele@gmail.com',
        'password' : '1sing_veryW3ll',
        'name_first' : 'Adele',
        'name_last' : 'Singer',
    })
    ch_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1.json()['token'],
        'name' : 'Soloist',
        'is_public' : True,
    })
    requests.post(f"{url}/channel/invite", json={
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    length1 = 5
    finish1 = requests.post(f"{url}/standup/start", json={
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'length' : length1,
    })
    sleep(3)
    active1 = requests.get(f"{url}/standup/active", params={
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    active2 = requests.get(f"{url}/standup/active", params={
        'token': user2.json()['token'],
        'channel_id': 2
    })
    assert active1.json() == {'is_active': True, 'time_finish': finish1.json()}
    assert active2.status_code == 400
    sleep(length1)
    active1 = requests.get(f"{url}/standup/active", params={
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    assert active1.json() == {'is_active': False, 'time_finish': None}

def test_standup_active_server_invalid_token(url):
    '''
    test standup_start_active with invalid token
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'samsmith@gmail.com',
        'password' : 'TooGoodToSayGoodbye',
        'name_first' : 'Sam',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'adele@gmail.com',
        'password' : '1sing_veryW3ll',
        'name_first' : 'Adele',
        'name_last' : 'Singer',
    })
    ch_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1.json()['token'],
        'name' : 'Soloist',
        'is_public' : True,
    })
    requests.post(f"{url}/channel/invite", json={
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    length1 = 5
    finish1 = requests.post(f"{url}/standup/start", json={
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'length' : length1,
    })
    sleep(3)
    active1 = requests.get(f"{url}/standup/active", params={
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    active2 = requests.get(f"{url}/standup/active", params={
        'token': 1234,
        'channel_id': ch_1.json()['channel_id']
    })
    assert active1.json() == {'is_active': True, 'time_finish': finish1.json()}
    assert active2.status_code == 400
    sleep(length1)
    active1 = requests.get(f"{url}/standup/active", params={
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    assert active1.json() == {'is_active': False, 'time_finish': None}

def test_standup_active_server_not_a_member(url):
    '''
    test standup_start_active with a non-member accessing the active standup
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'samsmith@gmail.com',
        'password' : 'TooGoodToSayGoodbye',
        'name_first' : 'Sam',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'adele@gmail.com',
        'password' : '1sing_veryW3ll',
        'name_first' : 'Adele',
        'name_last' : 'Singer',
    })
    ch_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1.json()['token'],
        'name' : 'Soloist',
        'is_public' : True,
    })
    length1 = 5
    finish1 = requests.post(f"{url}/standup/start", json={
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'length' : length1,
    })
    sleep(3)
    active1 = requests.get(f"{url}/standup/active", params={
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    active2 = requests.get(f"{url}/standup/active", params={
        'token': user2.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    assert active1.json() == {'is_active': True, 'time_finish': finish1.json()}
    assert active2.status_code == 400
    sleep(length1)
    active1 = requests.get(f"{url}/standup/active", params={
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    assert active1.json() == {'is_active': False, 'time_finish': None}
