from datetime import datetime
import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json

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

###################### SERVER TEST FOR STANDUP_START ##########################

def test_standup_start_server(url):
    '''
    test standup_start_server with its normal behaviour but with longer time
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json ={
        'email' : 'samsmith@gmail.com',
        'password' : 'TooGoodToSayGoodbye',
        'name_first' : 'Sam',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json ={
        'email' : 'adele@gmail.com',
        'password' : '1sing_veryW3ll',
        'name_first' : 'Adele',
        'name_last' : 'Singer',
    })
    ch_1 = requests.post(f"{url}/channels/create", json ={
        'token' : user1.json()['token'],
        'name' : 'Soloist',
        'is_public' : True,
    })
    requests.post(f"{url}/channel/invite", json ={
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    length = 50
    requests.post(f"{url}/standup/start", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'length' : length,
    })
    sleep(10)
    active = requests.get(f"{url}/standup/active", params ={
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    print(active)
    #active = standup_active(user1['token'], ch_1['channel_id'])
    assert active.json()['is_active'] is True
    sleep(length)
    active = requests.get(f"{url}/standup/active", params ={
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    assert active.json()['is_active'] is False

def test_standup_start_server_multi_ch(url):
    '''
    test standup_start_server to run standup concurrently on multiple channel
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'steveroger@gmail.com',
        'password' : 'is_groot_animal?',
        'name_first' : 'Steve',
        'name_last' : 'Roger',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'rdj_cool@gmail.com',
        'password' : 'jarvis_Annoying',
        'name_first' : 'Tony',
        'name_last' : 'Stark',
    })
    user3 = requests.post(f"{url}/auth/register", json = {
        'email' : 'antman@gmail.com',
        'password' : 'shakira_saminamina',
        'name_first' : 'Scott',
        'name_last' : 'Lang',
    })
    user4 = requests.post(f"{url}/auth/register", json = {
        'email' : 'thewasp@gmail.com',
        'password' : 'antman_annoying',
        'name_first' : 'Hope',
        'name_last' : 'Pym',
    })
    user5 = requests.post(f"{url}/auth/register", json = {
        'email' : 'spiderman_amazing@gmail.com',
        'password' : 'zendaya_love',
        'name_first' : 'Peter',
        'name_last' : 'Parker',
    })
    user6 = requests.post(f"{url}/auth/register", json = {
        'email' : 'thor_isgod@gmail.com',
        'password' : '1234_iamgod',
        'name_first' : 'Thor',
        'name_last' : 'God',
    })
    user7 = requests.post(f"{url}/auth/register", json = {
        'email' : 'starlord@gmail.com',
        'password' : 'gamora_comeback12',
        'name_first' : 'Star',
        'name_last' : 'Lord',
    })
    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user1.json()['token'],
        'name' : 'Avengers',
        'is_public' : True,
    })
    ch_2 = requests.post(f"{url}/channels/create", json = {
        'token' : user3.json()['token'],
        'name' : 'Tiny Hero',
        'is_public' : True,
    })
    ch_3 = requests.post(f"{url}/channels/create", json = {
        'token' : user6.json()['token'],
        'name' : 'Space Hero',
        'is_public' : True,
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    #c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user4.json()['u_id'],
    })
    #c.channel_invite(user1['token'], ch_1['channel_id'], user4['u_id'])
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user3.json()['u_id'],
    })
    #c.channel_invite(user1['token'], ch_1['channel_id'], user3['u_id'])
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user7.json()['u_id'],
    })
    #c.channel_invite(user1['token'], ch_1['channel_id'], user7['u_id'])
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user5.json()['u_id'],
    })
    #c.channel_invite(user1['token'], ch_1['channel_id'], user5['u_id'])
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user6.json()['u_id'],
    })
    #c.channel_invite(user1['token'], ch_1['channel_id'], user6['u_id'])
    requests.post(f"{url}/channel/invite", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_2.json()['channel_id'],
        'u_id' : user4.json()['u_id'],
    })
    #c.channel_invite(user3['token'], ch_2['channel_id'], user4['u_id'])
    requests.post(f"{url}/channel/invite", json = {
        'token' : user6.json()['token'],
        'channel_id' : ch_3.json()['channel_id'],
        'u_id' : user5.json()['u_id'],
    })
    #c.channel_invite(user6['token'], ch_3['channel_id'], user5['u_id'])
    requests.post(f"{url}/channel/invite", json = {
        'token' : user6.json()['token'],
        'channel_id' : ch_3.json()['channel_id'],
        'u_id' : user7.json()['u_id'],
    })
    #c.channel_invite(user6['token'], ch_3['channel_id'], user7['u_id'])
    length1 = 10
    length2 = 8
    length3 = 5
    requests.post(f"{url}/standup/start", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'length' : length1,
    })
    #standup_start(user1['token'], ch_1['channel_id'], length1)
    requests.post(f"{url}/standup/start", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_2.json()['channel_id'],
        'length' : length2,
    })
    #standup_start(user3['token'], ch_2['channel_id'], length2)
    requests.post(f"{url}/standup/start", json = {
        'token' : user6.json()['token'],
        'channel_id' : ch_3.json()['channel_id'],
        'length' : length3,
    })
    #standup_start(user6['token'], ch_3['channel_id'], length3)
    sleep(3)
    active1 = requests.get(f"{url}/standup/active", params = {
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    #active1 = standup_active(user1['token'], ch_1['channel_id'])
    active2 = requests.get(f"{url}/standup/active", params = {
        'token': user3.json()['token'],
        'channel_id': ch_2.json()['channel_id']
    })
    #active2 = standup_active(user3['token'], ch_2['channel_id'])
    active3 = requests.get(f"{url}/standup/active", params = {
        'token': user6.json()['token'],
        'channel_id': ch_3.json()['channel_id']
    })
    #active3 = standup_active(user6['token'], ch_3['channel_id'])
    assert active1.json()['is_active'] is True
    assert active2.json()['is_active'] is True
    assert active3.json()['is_active'] is True
    sleep(length1)
    active1 = requests.get(f"{url}/standup/active", params = {
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    #active1 = standup_active(user1['token'], ch_1['channel_id'])
    active2 = requests.get(f"{url}/standup/active", params = {
        'token': user3.json()['token'],
        'channel_id': ch_2.json()['channel_id']
    })
    #active2 = standup_active(user3['token'], ch_2['channel_id'])
    active3 = requests.get(f"{url}/standup/active", params = {
        'token': user6.json()['token'],
        'channel_id': ch_3.json()['channel_id']
    })
    assert active1.json()['is_active'] is False
    assert active2.json()['is_active'] is False
    assert active3.json()['is_active'] is False

def test_standup_start_server_invalid_token(url):
    '''
    test standup_start_server with invalid token
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'kenclark@gmail.com',
        'password' : 'Ihate_cryptonite',
        'name_first' : 'Kent',
        'name_last' : 'Clark',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'karasupergirl@gmail.com',
        'password' : 'MissingMonel123',
        'name_first' : 'Kara',
        'name_last' : 'Zor-el',
    })
    user3 = requests.post(f"{url}/auth/register", json = {
        'email' : 'iambatman@gmail.com',
        'password' : 'who_is_wonderWoman',
        'name_first' : 'Bruce',
        'name_last' : 'Wayne',
    })
    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user3.json()['token'],
        'name' : 'Just League',
        'is_public' : True,
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user1.json()['u_id'],
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    length = 10
    standup = requests.post(f"{url}/standup/start", json = {
        'token' : 123456,
        'channel_id' : ch_1.json()['channel_id'],
        'length' : length,
    })
    assert standup.status_code == 400
    active = requests.get(f"{url}/standup/active", params = {
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    assert active.json()['is_active'] is False

def test_standup_start_server_not_member(url):
    '''
    test standup_start_server with user is not a member of the channel
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'kenclark@gmail.com',
        'password' : 'Ihate_cryptonite',
        'name_first' : 'Kent',
        'name_last' : 'Clark',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'karasupergirl@gmail.com',
        'password' : 'MissingMonel123',
        'name_first' : 'Kara',
        'name_last' : 'Zor-el',
    })
    user3 = requests.post(f"{url}/auth/register", json = {
        'email' : 'iambatman@gmail.com',
        'password' : 'who_is_wonderWoman',
        'name_first' : 'Bruce',
        'name_last' : 'Wayne',
    })
    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user3.json()['token'],
        'name' : 'Just League',
        'is_public' : True,
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user1.json()['u_id'],
    })
    length = 10
    standup = requests.post(f"{url}/standup/start", json = {
        'token' : user2.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'length' : length,
    })    
    assert standup.status_code == 400
    active = requests.get(f"{url}/standup/active", params = {
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    assert active.json()['is_active'] is False

def test_standup_start_server_invalid_ch(url):
    '''
    test standup_start_server with invalid channel_id
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'kenclark@gmail.com',
        'password' : 'Ihate_cryptonite',
        'name_first' : 'Kent',
        'name_last' : 'Clark',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'karasupergirl@gmail.com',
        'password' : 'MissingMonel123',
        'name_first' : 'Kara',
        'name_last' : 'Zor-el',
    })
    user3 = requests.post(f"{url}/auth/register", json = {
        'email' : 'iambatman@gmail.com',
        'password' : 'who_is_wonderWoman',
        'name_first' : 'Bruce',
        'name_last' : 'Wayne',
    })
    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user3.json()['token'],
        'name' : 'Just League',
        'is_public' : True,
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user1.json()['u_id'],
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })    
    length = 10
    standup = requests.post(f"{url}/standup/start", json = {
        'token' : user2.json()['token'],
        'channel_id' : 12345,
        'length' : length,
    })    
    assert standup.status_code == 400
    active = requests.get(f"{url}/standup/active", params = {
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    assert active.json()['is_active'] is False

def test_standup_start_server_2active_standup(url):
    '''
    test standup_start_server by starting 2 standup in 1 channel
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'Dobbyis_Afree_elf',
        'name_first' : 'Harry',
        'name_last' : 'Potter',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'hermione_granger12@gmail.com',
        'password' : 'Wingardium_leviosa',
        'name_first' : 'Hermione',
        'name_last' : 'Granger',
    })
    user3 = requests.post(f"{url}/auth/register", json = {
        'email' : 'ronweasley@gmail.com',
        'password' : 'ginny_lil_sis',
        'name_first' : 'Ron',
        'name_last' : 'Weasley',
    })
    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user1.json()['token'],
        'name' : 'hogwards',
        'is_public' : False,
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user3.json()['u_id'],
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    length1 = 20
    length2 = 5
    requests.post(f"{url}/standup/start", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'length' : length1,
    })
    standup2 = requests.post(f"{url}/standup/start", json = {
        'token' : user2.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'length' : length2,
    })
    assert standup2.status_code == 400
    sleep(10)
    active = requests.get(f"{url}/standup/active", params = {
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    assert active.json()['is_active'] is True
    sleep(length1)
    active = requests.get(f"{url}/standup/active", params = {
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    assert active.json()['is_active'] is False

def test_standup_start_server_lessthan1_second(url):
    '''
    test standup_start with less than 1 second period of standup
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'Dobbyis_Afree_elf',
        'name_first' : 'Harry',
        'name_last' : 'Potter',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'hermione_granger12@gmail.com',
        'password' : 'Wingardium_leviosa',
        'name_first' : 'Hermione',
        'name_last' : 'Granger',
    })
    user3 = requests.post(f"{url}/auth/register", json = {
        'email' : 'ronweasley@gmail.com',
        'password' : 'ginny_lil_sis',
        'name_first' : 'Ron',
        'name_last' : 'Weasley',
    })
    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user1.json()['token'],
        'name' : 'hogwards',
        'is_public' : False,
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user3.json()['u_id'],
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    length1 = 0
    standup1 = requests.post(f"{url}/standup/start", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'length' : length1,
    })
    assert standup1.status_code == 400
    active = requests.get(f"{url}/standup/active", params = {
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    assert active.json()['is_active'] is False
    length2 = -12
    standup1 = requests.post(f"{url}/standup/start", json = {
        'token' : user2.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'length' : length2,
    })
    assert standup1.status_code == 400
    active = requests.get(f"{url}/standup/active", params = {
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    assert active.json()['is_active'] is False

###################### SERVER TEST FOR STANDUP_SEND ##########################
def test_standup_send_server_simple(url):
    '''
    test standup_send_server with its normal behaviour
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'samsmith@gmail.com',
        'password' : 'TooGoodToSayGoodbye',
        'name_first' : 'Sam',
        'name_last' : 'Smith',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'adele@gmail.com',
        'password' : '1sing_veryW3ll',
        'name_first' : 'Adele',
        'name_last' : 'Singer',
    })
    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user1.json()['token'],
        'name' : 'Soloist',
        'is_public' : True,
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    length = 10
    requests.post(f"{url}/standup/start", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'length' : length,
    })
    requests.post(f"{url}/standup/send", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : 'Hi everyone',
    })
    requests.post(f"{url}/standup/send", json = {
        'token' : user2.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : 'aloha',
    })
    sleep(length)
    get_message = requests.get(f"{url}/channel/messages", params = {
        'token': user2.json()['token'],
        'channel_id': ch_1.json()['channel_id'],
        'start': 0
    })
    profile1 = requests.get(f"{url}/user/profile", params = {
        'token':user1.json()['token'],
        'u_id':user1.json()['u_id']
    })
    profile2 = requests.get(f"{url}/user/profile", params = {
        'token':user2.json()['token'],
        'u_id':user2.json()['u_id']
    })
    message = f"{profile1.json()['user']['handle_str']}: Hi everyone\n{profile2.json()['user']['handle_str']}: aloha\n"
    assert get_message.json()['messages'][0]['message'] == message
    assert get_message.json()['messages'][0]['u_id'] == user1.json()['u_id']
    #assert get_messages1['messages'][0]['message_id'] == message3id['message_id']

def test_standup_send_server_multiple_ch(url):
    '''
    test standup_send_server to run standup concurrently on multiple channel
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'steveroger@gmail.com',
        'password' : 'is_groot_animal?',
        'name_first' : 'Steve',
        'name_last' : 'Roger',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'rdj_cool@gmail.com',
        'password' : 'jarvis_Annoying',
        'name_first' : 'Tony',
        'name_last' : 'Stark',
    })
    user3 = requests.post(f"{url}/auth/register", json = {
        'email' : 'antman@gmail.com',
        'password' : 'shakira_saminamina',
        'name_first' : 'Scott',
        'name_last' : 'Lang',
    })
    user4 = requests.post(f"{url}/auth/register", json = {
        'email' : 'thewasp@gmail.com',
        'password' : 'antman_annoying',
        'name_first' : 'Hope',
        'name_last' : 'Pym',
    })
    user5 = requests.post(f"{url}/auth/register", json = {
        'email' : 'spiderman_amazing@gmail.com',
        'password' : 'zendaya_love',
        'name_first' : 'Peter',
        'name_last' : 'Parker',
    })
    user6 = requests.post(f"{url}/auth/register", json = {
        'email' : 'thor_isgod@gmail.com',
        'password' : '1234_iamgod',
        'name_first' : 'Thor',
        'name_last' : 'God',
    })
    user7 = requests.post(f"{url}/auth/register", json = {
        'email' : 'starlord@gmail.com',
        'password' : 'gamora_comeback12',
        'name_first' : 'Star',
        'name_last' : 'Lord',
    })
    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user1.json()['token'],
        'name' : 'Avengers',
        'is_public' : True,
    })
    ch_2 = requests.post(f"{url}/channels/create", json = {
        'token' : user3.json()['token'],
        'name' : 'Tiny Hero',
        'is_public' : True,
    })
    ch_3 = requests.post(f"{url}/channels/create", json = {
        'token' : user6.json()['token'],
        'name' : 'Space Hero',
        'is_public' : True,
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    #c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user4.json()['u_id'],
    })
    #c.channel_invite(user1['token'], ch_1['channel_id'], user4['u_id'])
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user3.json()['u_id'],
    })
    #c.channel_invite(user1['token'], ch_1['channel_id'], user3['u_id'])
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user7.json()['u_id'],
    })
    #c.channel_invite(user1['token'], ch_1['channel_id'], user7['u_id'])
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user5.json()['u_id'],
    })
    #c.channel_invite(user1['token'], ch_1['channel_id'], user5['u_id'])
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user6.json()['u_id'],
    })
    #c.channel_invite(user1['token'], ch_1['channel_id'], user6['u_id'])
    requests.post(f"{url}/channel/invite", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_2.json()['channel_id'],
        'u_id' : user4.json()['u_id'],
    })
    #c.channel_invite(user3['token'], ch_2['channel_id'], user4['u_id'])
    requests.post(f"{url}/channel/invite", json = {
        'token' : user6.json()['token'],
        'channel_id' : ch_3.json()['channel_id'],
        'u_id' : user5.json()['u_id'],
    })
    #c.channel_invite(user6['token'], ch_3['channel_id'], user5['u_id'])
    requests.post(f"{url}/channel/invite", json = {
        'token' : user6.json()['token'],
        'channel_id' : ch_3.json()['channel_id'],
        'u_id' : user7.json()['u_id'],
    })
    length1 = 10
    length2 = 8
    length3 = 5
    requests.post(f"{url}/standup/start", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'length' : length1,
    })
    # standup_start(user1['token'], ch_1['channel_id'], length1)
    requests.post(f"{url}/standup/send", json = {
        'token' : user2.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : 'Good morning',
    })
    requests.post(f"{url}/standup/send", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : 'good afternoon',
    })
    requests.post(f"{url}/standup/send", json = {
        'token' : user4.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : 'Good night',
    })
    requests.post(f"{url}/standup/start", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_2.json()['channel_id'],
        'length' : length2,
    })
    # standup_start(user3['token'], ch_2['channel_id'], length2)
    requests.post(f"{url}/standup/send", json = {
        'token' : user4.json()['token'],
        'channel_id' : ch_2.json()['channel_id'],
        'message' : 'Happy birthday',
    })
    requests.post(f"{url}/standup/send", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_2.json()['channel_id'],
        'message' : 'thank you',
    })
    # standup_send(user4['token'], ch_2['channel_id'], 'Happy birthday')
    # standup_send(user3['token'], ch_2['channel_id'], 'thank you')
    requests.post(f"{url}/standup/start", json = {
        'token' : user5.json()['token'],
        'channel_id' : ch_3.json()['channel_id'],
        'length' : length3,
    })
    # standup_start(user5['token'], ch_3['channel_id'], length3)
    requests.post(f"{url}/standup/send", json = {
        'token' : user6.json()['token'],
        'channel_id' : ch_3.json()['channel_id'],
        'message' : 'How r u today?',
    })
    requests.post(f"{url}/standup/send", json = {
        'token' : user7.json()['token'],
        'channel_id' : ch_3.json()['channel_id'],
        'message' : 'I am very great today',
    })
    # standup_send(user6['token'], ch_3['channel_id'], 'How r u today?')
    # standup_send(user7['token'], ch_3['channel_id'], 'I am very great today')
    sleep(length1)
    get_message1 = requests.get(f"{url}/channel/messages", params = {
        'token': user2.json()['token'],
        'channel_id': ch_1.json()['channel_id'],
        'start': 0
    })
    get_message2 = requests.get(f"{url}/channel/messages", params = {
        'token': user3.json()['token'],
        'channel_id': ch_2.json()['channel_id'],
        'start': 0
    })
    get_message3 = requests.get(f"{url}/channel/messages", params = {
        'token': user6.json()['token'],
        'channel_id': ch_3.json()['channel_id'],
        'start': 0
    })
    # get_message1 = c.channel_messages(user2['token'], ch_1['channel_id'], 0)
    # get_message2 = c.channel_messages(user3['token'], ch_2['channel_id'], 0)
    # get_message3 = c.channel_messages(user6['token'], ch_3['channel_id'], 0)
    requests.get(f"{url}/user/profile", params = {
        'token':user1.json()['token'],
        'u_id':user1.json()['u_id']
    })
    profile2 = requests.get(f"{url}/user/profile", params = {
        'token':user1.json()['token'],
        'u_id':user2.json()['u_id']
    })
    profile3 = requests.get(f"{url}/user/profile", params = {
        'token':user1.json()['token'],
        'u_id':user3.json()['u_id']
    })    
    profile4 = requests.get(f"{url}/user/profile", params = {
        'token':user1.json()['token'],
        'u_id':user4.json()['u_id']
    })
    requests.get(f"{url}/user/profile", params = {
        'token':user6.json()['token'],
        'u_id':user5.json()['u_id']
    })
    profile6 = requests.get(f"{url}/user/profile", params = {
        'token':user6.json()['token'],
        'u_id':user6.json()['u_id']
    })
    profile7 = requests.get(f"{url}/user/profile", params = {
        'token':user6.json()['token'],
        'u_id':user7.json()['u_id']
    })
    message1 = str({profile2.json()['user']['handle_str']: 'Good morning',
                    profile3.json()['user']['handle_str']: 'good afternoon',
                    profile4.json()['user']['handle_str']: 'Good night'})
    message2 = str({profile4.json()['user']['handle_str']: 'Happy birthday',
                    profile3.json()['user']['handle_str']: 'thank you'})
    message3 = str({profile6.json()['user']['handle_str']: 'How r u today?',
                    profile7.json()['user']['handle_str']: 'I am very great today'})
    message1 = f"{profile2.json()['user']['handle_str']}: Good morning\n{profile3.json()['user']['handle_str']}: good afternoon\n\
{profile4.json()['user']['handle_str']}: Good night\n"
    message2 = f"{profile4.json()['user']['handle_str']}: Happy birthday\n{profile3.json()['user']['handle_str']}: thank you\n"
    message3 = f"{profile6.json()['user']['handle_str']}: How r u today?\n\
{profile7.json()['user']['handle_str']}: I am very great today\n"
    assert get_message1.json()['messages'][0]['message'] == message1
    assert get_message1.json()['messages'][0]['u_id'] == user1.json()['u_id']
    assert get_message2.json()['messages'][0]['message'] == message2
    assert get_message2.json()['messages'][0]['u_id'] == user3.json()['u_id']
    #print(get_message3.json()['messages'])
    assert get_message3.json()['messages'][0]['message'] == message3
    assert get_message3.json()['messages'][0]['u_id'] == user5.json()['u_id']

def test_standup_send_server_invalid_token(url):
    '''
    test standup_send_server with invalid token
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'kenclark@gmail.com',
        'password' : 'Ihate_cryptonite',
        'name_first' : 'Kent',
        'name_last' : 'Clark',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'karasupergirl@gmail.com',
        'password' : 'MissingMonel123',
        'name_first' : 'Kara',
        'name_last' : 'Zor-el',
    })
    user3 = requests.post(f"{url}/auth/register", json = {
        'email' : 'iambatman@gmail.com',
        'password' : 'who_is_wonderWoman',
        'name_first' : 'Bruce',
        'name_last' : 'Wayne',
    })
    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user3.json()['token'],
        'name' : 'Just League',
        'is_public' : True,
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user1.json()['u_id'],
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    length = 10
    requests.post(f"{url}/standup/start", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'length' : length,
    })
    # standup_start(user1['token'], ch_1['channel_id'], length)
    send = requests.post(f"{url}/standup/send", json = {
        'token' : 123456,
        'channel_id' : ch_1.json()['channel_id'],
        'message' : 'Hi everyone',
    })
    assert send.status_code == 400
    sleep(5)
    active = requests.get(f"{url}/standup/active", params = {
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    assert active.json()['is_active'] is True

def test_standup_send_server_invalid_ch(url):
    '''
    test standup_send_server with invalid channel id
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'kenclark@gmail.com',
        'password' : 'Ihate_cryptonite',
        'name_first' : 'Kent',
        'name_last' : 'Clark',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'karasupergirl@gmail.com',
        'password' : 'MissingMonel123',
        'name_first' : 'Kara',
        'name_last' : 'Zor-el',
    })
    user3 = requests.post(f"{url}/auth/register", json = {
        'email' : 'iambatman@gmail.com',
        'password' : 'who_is_wonderWoman',
        'name_first' : 'Bruce',
        'name_last' : 'Wayne',
    })
    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user3.json()['token'],
        'name' : 'Just League',
        'is_public' : True,
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user1.json()['u_id'],
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    length = 10
    requests.post(f"{url}/standup/start", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'length' : length,
    })
    # standup_start(user1['token'], ch_1['channel_id'], length)
    send = requests.post(f"{url}/standup/send", json = {
        'token' : user3.json()['token'],
        'channel_id' : 12345,
        'message' : 'Hi everyone',
    })
    assert send.status_code == 400
    sleep(5)
    active = requests.get(f"{url}/standup/active", params = {
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    assert active.json()['is_active'] is True

def test_standup_send_server_not_member(url):
    '''
    test standup_start_server with user is not a member of the channel
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'kenclark@gmail.com',
        'password' : 'Ihate_cryptonite',
        'name_first' : 'Kent',
        'name_last' : 'Clark',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'karasupergirl@gmail.com',
        'password' : 'MissingMonel123',
        'name_first' : 'Kara',
        'name_last' : 'Zor-el',
    })
    user3 = requests.post(f"{url}/auth/register", json = {
        'email' : 'iambatman@gmail.com',
        'password' : 'who_is_wonderWoman',
        'name_first' : 'Bruce',
        'name_last' : 'Wayne',
    })
    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user3.json()['token'],
        'name' : 'Just League',
        'is_public' : True,
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user1.json()['u_id'],
    })
    # c.channel_invite(user3['token'], ch_1['channel_id'], user1['u_id'])
    length = 10
    requests.post(f"{url}/standup/start", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'length' : length,
    })
    send = requests.post(f"{url}/standup/send", json = {
        'token' : user2.json()['token'],
        'channel_id' : 12345,
        'message' : 'Hi everyone',
    })
    assert send.status_code == 400
    active = requests.get(f"{url}/standup/active", params = {
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    assert active.json()['is_active'] is True

def test_standup_send_server_msg_toolong(url):
    '''
    test standup_send with messages being too long (more than 1000 characters)
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'kenclark@gmail.com',
        'password' : 'Ihate_cryptonite',
        'name_first' : 'Kent',
        'name_last' : 'Clark',
    })
    requests.post(f"{url}/auth/register", json = {
        'email' : 'karasupergirl@gmail.com',
        'password' : 'MissingMonel123',
        'name_first' : 'Kara',
        'name_last' : 'Zor-el',
    })
    user3 = requests.post(f"{url}/auth/register", json = {
        'email' : 'iambatman@gmail.com',
        'password' : 'who_is_wonderWoman',
        'name_first' : 'Bruce',
        'name_last' : 'Wayne',
    })
    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user3.json()['token'],
        'name' : 'Just League',
        'is_public' : True,
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user1.json()['u_id'],
    })
    length = 10
    text = 510 * "abc"
    requests.post(f"{url}/standup/start", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'length' : length,
    })
    send = requests.post(f"{url}/standup/send", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : text,
    })
    assert send.status_code == 400
    active = requests.get(f"{url}/standup/active", params = {
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    assert active.json()['is_active'] is True

def test_standup_send_server_not_active(url):
    '''
    test standup_send with no active standup currently running
    '''
    requests.delete(f"{url}/clear")
    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'kenclark@gmail.com',
        'password' : 'Ihate_cryptonite',
        'name_first' : 'Kent',
        'name_last' : 'Clark',
    })
    requests.post(f"{url}/auth/register", json = {
        'email' : 'karasupergirl@gmail.com',
        'password' : 'MissingMonel123',
        'name_first' : 'Kara',
        'name_last' : 'Zor-el',
    })
    user3 = requests.post(f"{url}/auth/register", json = {
        'email' : 'iambatman@gmail.com',
        'password' : 'who_is_wonderWoman',
        'name_first' : 'Bruce',
        'name_last' : 'Wayne',
    })
    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user3.json()['token'],
        'name' : 'Just League',
        'is_public' : True,
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user1.json()['u_id'],
    })
    send = requests.post(f"{url}/standup/send", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : 'Hi everyone',
    })
    assert send.status_code == 400
    active = requests.get(f"{url}/standup/active", params = {
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id']
    })
    assert active.json()['is_active'] is False
