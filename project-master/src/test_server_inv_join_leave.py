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

def test_channel_invite_server(url):
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
        'name' : 'hogwards',
        'is_public' : True,
    })

    test = requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    assert test.json() == {}

    ch_details1 = requests.get(f"{url}/channel/details", params = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
    })
    
    assert ch_details1.json() == {
        'name' :  'hogwards',
        'owner_members' : [{'u_id': user1.json()['u_id'], 'name_first': 'Sam', 'name_last': 'Smith','profile_img_url' : "",}],
        'all_members' : [{'u_id': user1.json()['u_id'], 'name_first': 'Sam', 'name_last': 'Smith','profile_img_url' : "",},
                         {'u_id': user2.json()['u_id'], 'name_first': 'Adele', 'name_last': 'Singer','profile_img_url' : "",}]
    }

def test_server_invite_unauth(url):
    requests.delete(f"{url}/clear")
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'karasupergirl@gmail.com',
        'password' : 'MissingMonel123',
        'name_first' : 'Kara',
        'name_last' : 'Zor-el',
    })
    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user2.json()['token'],
        'name' : 'Just League',
        'is_public' : True,
    })
    invite = requests.post(f"{url}/channel/invite", json = {
        'token' : user2.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    assert invite.status_code == 400

def test_server_invite_user_error(url):
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : "iambatman@gmail.com",
        'password' : 'who_is_wonderWoman',
        'name_first' : 'Bruce',
        'name_last' : 'Wayne',
    })
    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user1.json()['token'],
        'name' : 'Just League',
        'is_public' : True,
    })
    invite = requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : 16,
    })
    assert invite.status_code == 400

def test_server_invite_already_a_member(url):
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'karasupergirl@gmail.com',
        'password' : 'MissingMonel123',
        'name_first' : 'Kara',
        'name_last' : 'Zor-el',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'iambatman@gmail.com',
        'password' : 'who_is_wonderWoman',
        'name_first' : 'Bruce',
        'name_last' : 'Wayne',
    })
    user3 = requests.post(f"{url}/auth/register", json = {
        'email' : 'luthorevil@gmail.com',
        'password' : 'LenaLuthoramazing',
        'name_first' : 'Lena',
        'name_last' : 'Luthor',
    })
    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user1.json()['token'],
        'name' : 'Just League',
        'is_public' : True,
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user3.json()['u_id'],
    })
    invite = requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user3.json()['u_id'],
    })
    assert invite.status_code == 400

################################################################################################
###################------------------ TEST LEAVE ------------------#############################
def test_server_leave(url):
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'spongebobsquarepants@gmail.com',
        'password' : 'garry_is_lovely',
        'name_first' : 'Spongebob',
        'name_last' : 'Squarepants',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'patrickstar@gmail.com',
        'password' : 'nothing_todo',
        'name_first' : 'Patrick',
        'name_last' : 'Star',
    })
    user3 = requests.post(f"{url}/auth/register", json = {
        'email' : 'plankton@gmail.com',
        'password' : 'i_WANT_the_RECIPE',
        'name_first' : 'Plankton',
        'name_last' : 'Evil',
    })
    user4 = requests.post(f"{url}/auth/register", json = {
        'email' : 'karen_computer@gmail.com',
        'password' : 'i_wannabe_alive',
        'name_first' : 'Karen',
        'name_last' : 'Computer',
    })
    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user1.json()['token'],
        'name' : 'bikini bottom',
        'is_public' : True,
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user3.json()['u_id'],
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user4.json()['u_id'],
    })
    requests.post(f"{url}/channel/leave", json = {
        'token' : user2.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
    })
    ch_details = requests.get(f"{url}/channel/details", params = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
    })
    assert ch_details.json() == {
        'name' : 'bikini bottom',
        'owner_members' : [{'u_id': user1.json()['u_id'], 'name_first': 'Spongebob',
                            'name_last': 'Squarepants','profile_img_url' : "",}],
        'all_members' : [{'u_id': user1.json()['u_id'], 'name_first': 'Spongebob',
                          'name_last': 'Squarepants','profile_img_url' : "",},
                         {'u_id': user3.json()['u_id'], 'name_first': 'Plankton', 'name_last': 'Evil','profile_img_url' : "",},
                         {'u_id': user4.json()['u_id'], 'name_first': 'Karen', 'name_last': 'Computer','profile_img_url' : "",}]
    }

def test_server_leave_unauth(url):
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
        'u_id' : user2.json()['u_id'],
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user3.json()['u_id'],
    })

    leave = requests.post(f"{url}/channel/leave", json = {
        'token' : user3.json()['token'],
        'channel_id' : 17,
    })
    assert leave.status_code == 400

def test_server_leave_not_member(url):
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
        'u_id' : user2.json()['u_id'],
    })

    leave = requests.post(f"{url}/channel/leave", json = {
        'token' : user3.json()['token'],
        'channel_id' : 17,
    })
    assert leave.status_code == 400

##################################################################################################
##############################------------ TEST JOIN ------------------###########################
def test_join_server(url):
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
    user3 = requests.post(f"{url}/auth/register", json = {
        'email' : 'ed_sheeran@gmail.com',
        'password' : 'guitar_mylife',
        'name_first' : 'Ed',
        'name_last' : 'Sheeran',
    })
    assert user3.status_code == 200

    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user1.json()['token'],
        'name' : 'Soloist',
        'is_public' : True,
    })
    assert ch_1.status_code == 200

    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    requests.post(f"{url}/channel/join", json = {
        'token' : user3.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
    })

    ch_details = requests.get(f"{url}/channel/details", params = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
    })
    
    assert ch_details.json() == {
        'name' : 'Soloist',
        'owner_members' : [{'u_id': user1.json()['u_id'], 'name_first': 'Sam', 'name_last': 'Smith','profile_img_url' : "",}],
        'all_members' : [{'u_id': user1.json()['u_id'], 'name_first': 'Sam', 'name_last': 'Smith','profile_img_url' : "",},
                         {'u_id': user2.json()['u_id'], 'name_first': 'Adele', 'name_last': 'Singer','profile_img_url' : "",},
                         {'u_id': user3.json()['u_id'], 'name_first': 'Ed', 'name_last': 'Sheeran','profile_img_url' : "",}]
    }

def test_server_join_unauth(url):
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'spongebobsquarepants@gmail.com',
        'password' : 'garry_is_lovely',
        'name_first' : 'Spongebob',
        'name_last' : 'Squarepants',
    })
    user3 = requests.post(f"{url}/auth/register", json = {
        'email' : 'plankton@gmail.com',
        'password' : 'i_WANT_the_RECIPE',
        'name_first' : 'Plankton',
        'name_last' : 'Evil',
    })
    requests.post(f"{url}/channels/create", json = {
        'token' : user1.json()['token'],
        'name' : 'KrustyKrab',
        'is_public' : True,
    })
    join = requests.post(f"{url}/channel/join", json = {
        'token' : user3.json()['token'],
        'channel_id' : 13,
    })
    assert join.status_code == 400

def test_server_join_private(url):
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'spongebobsquarepants@gmail.com',
        'password' : 'garry_is_lovely',
        'name_first' : 'Spongebob',
        'name_last' : 'Squarepants',
    })
    user4 = requests.post(f"{url}/auth/register", json = {
        'email' : 'karen_computer@gmail.com',
        'password' : 'i_wannabe_alive',
        'name_first' : 'Karen',
        'name_last' : 'Computer',
    })
    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user1.json()['token'],
        'name' : 'Chum Bucket',
        'is_public' : False,
    })
    join = requests.post(f"{url}/channel/join", json = {
        'token' : user4.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
    })
    assert join.status_code == 400

def test_server_join_already_a_member(url):
    requests.delete(f"{url}/clear")

    user1 = requests.post(f"{url}/auth/register", json = {
        'email' : 'spongebobsquarepants@gmail.com',
        'password' : 'garry_is_lovely',
        'name_first' : 'Spongebob',
        'name_last' : 'Squarepants',
    })
    user2 = requests.post(f"{url}/auth/register", json = {
        'email' : 'patrickstar@gmail.com',
        'password' : 'nothing_todo',
        'name_first' : 'Patrick',
        'name_last' : 'Star',
    })
    ch_1 = requests.post(f"{url}/channels/create", json = {
        'token' : user1.json()['token'],
        'name' : 'KrustyKrab',
        'is_public' : True,
    })
    requests.post(f"{url}/channel/invite", json = {
        'token' : user1.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
        'u_id' : user2.json()['u_id'],
    })
    join = requests.post(f"{url}/channel/join", json = {
        'token' : user2.json()['token'],
        'channel_id' : ch_1.json()['channel_id'],
    })
    assert join.status_code == 400
