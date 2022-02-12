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

def test_server_msg_edit(url):
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'luthorevil@gmail.com',
        'password' : 'LenaLuthoramazing',
        'name_first' : 'Lena',
        'name_last' : 'Luthor',
    })
    assert user1.status_code == 200

    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : "karasupergirl@gmail.com",
        'password' : 'MissingMonel123',
        'name_first' : 'Kara',
        'name_last' : 'Zor-el',
    })
    assert user2.status_code == 200

    user3 = requests.post(f"{url}/auth/register", json = {
        'email' : "iambatman@gmail.com",
        'password' : 'who_is_wonderWoman',
        'name_first' : 'Bruce',
        'name_last' : 'Wayne',
    })
    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user3.json()['token'],
        'name' : 'Just League',
        'is_public' : True,
    })
    assert user3.status_code == 200

    
    ch_inv = requests.post(f"{url}/channel/invite", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user1.json()['u_id'],
    })
    assert ch_inv.status_code == 200

    ch_join = requests.post(f"{url}/channel/join", json = {
        'token' : user2.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
    })
    assert ch_join.status_code == 200

    msg1 = requests.post(f"{url}/message/send", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : "Have you heard this?",
    })
    assert msg1.status_code == 200

    msg2 = requests.post(f"{url}/message/send", json = {
        'token' : user2.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : "Whose album is that?",
    })
    assert msg2.status_code == 200

    test3 = requests.put(f"{url}/message/edit", json = {
        'token' : user1.json()['token'],
        'message_id' : msg1.json()['message_id'],
        'message' : "This album is very nice",
    })
    assert test3.status_code == 200

    test4 = requests.put(f"{url}/message/edit", json = {
        'token' : user3.json()['token'],
        'message_id' : msg2.json()['message_id'],
        'message' : "Is that ed sheeran's?",
    })
    assert test4.status_code == 200

    get_messages1 = requests.get(f"{url}/channel/messages", params = {
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id'],
        'start': 0
    })

    assert get_messages1.json()['messages'][1]['message'] == "This album is very nice"
    assert get_messages1.json()['messages'][0]['message'] == "Is that ed sheeran's?"

def test_server_msg_edit_unauth(url):
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
    msg1 = requests.post(f"{url}/message/send", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : "How R u?",
    })
    assert msg1.status_code == 200
    requests.post(f"{url}/message/send", json = {
        'token' : user2.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : "How R u?",
    })
    test = requests.put(f"{url}/message/edit", json = {
        'token' : user3.json()['token'],
        'message_id' : msg1.json()['message_id'],
        'message' : "How are you??",
    })
    assert test.status_code == 400

def test_server_msg_edit_nomsg_id(url):
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
    requests.post(f"{url}/message/send", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : "How R u?",
    })
    requests.post(f"{url}/message/send", json = {
        'token' : user2.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : "How R u?",
    })
    test = requests.put(f"{url}/message/edit", json = {
        'token' : user3.json()['token'],
        'message_id' : 15,
        'message' : "How are you??",
    })
    assert test.status_code == 400

def test_server_msg_edit_empty(url):
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
    msg1 = requests.post(f"{url}/message/send", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'message' : "How R u?",
    })
    requests.put(f"{url}/message/edit", json = {
        'token' : user3.json()['token'],
        'message_id' : msg1.json()['message_id'],
        'message' : "",
    })

    get_message = requests.get(f"{url}/channel/messages", params = {
        'token': user1.json()['token'],
        'channel_id': ch_1.json()['channel_id'],
        'start': 0
    })
    assert get_message.json()['end'] == -1


