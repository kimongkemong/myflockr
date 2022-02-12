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

#Make sure url works well
def test_echo(url):
    '''
    A simple test to check echo
    '''
    resp = requests.get(url + 'echo', params={'data': 'hello'})
    assert json.loads(resp.text) == {'data': 'hello'}


#If both args are invalid, the user_profile func should raise an AccessError first
#(We assume that user_profile always first check token)
def test_up_empty(url):

    requests.delete(f"{url}/clear")

    res = requests.get(f"{url}/user/profile", params = {
        'token':1, 
        'u_id':1
    })

    assert res.status_code == 400


#If u_id given is from a non-registered user, then user_profile should raise InputError
def test_up_InvalidUId(url):
    requests.delete(f"{url}/clear")

    data1 = requests.post(f"{url}/auth/register", json = {
        'email':'messi@barca.com', 
        'password':'123456', 
        'name_first':'Lionel', 
        'name_last':'Messi'
    })

    requests.post(f"{url}/auth/register", json = {
        'email':'ronaldo@juventus.com', 
        'password':'654321', 
        'name_first':'Cristiano', 
        'name_last':'Ronaldo'
    })   

    requests.post(f"{url}/auth/register", json = {
        'email':'suarez@atmadrid.com', 
        'password':'lovemessi123', 
        'name_first':'Luis', 
        'name_last':'Suarez'
    })    

    requests.post(f"{url}/auth/register", json = {
        'email':'havertz@chelsea.com', 
        'password':'german098', 
        'name_first':'Kai', 
        'name_last':'Havertz'
    })  

    requests.post(f"{url}/auth/register", json = {
        'email':'bsilva@mancity.com', 
        'password':'iamsilva456', 
        'name_first':'Bernado', 
        'name_last':'Silva'
    }) 

    res = requests.get(f"{url}/user/profile", params = {
        'token':data1.json()['token'],
        'u_id':-1
    })

    assert res.status_code == 400


#Test if user_profile works well if the token and user_id are from the same user
def test_up_same(url):
    requests.delete(f"{url}/clear")

    data1 = requests.post(f"{url}/auth/register", json = {
        'email':'messi@barca.com', 
        'password':'123456', 
        'name_first':'Lionel', 
        'name_last':'Messi'
    })

    requests.post(f"{url}/auth/register", json = {
        'email':'ronaldo@juventus.com', 
        'password':'654321', 
        'name_first':'Cristiano', 
        'name_last':'Ronaldo'
    })   

    requests.post(f"{url}/auth/register", json = {
        'email':'suarez@atmadrid.com', 
        'password':'lovemessi123', 
        'name_first':'Luis', 
        'name_last':'Suarez'
    })    

    requests.post(f"{url}/auth/register", json = {
        'email':'havertz@chelsea.com', 
        'password':'german098', 
        'name_first':'Kai', 
        'name_last':'Havertz'
    })  

    requests.post(f"{url}/auth/register", json = {
        'email':'bsilva@mancity.com', 
        'password':'iamsilva456', 
        'name_first':'Bernado', 
        'name_last':'Silva'
    }) 

    up = requests.get(f"{url}/user/profile", params = {
        'token':data1.json()['token'],
        'u_id':data1.json()['u_id']
    })
    assert up.json() == {
        'user': {'u_id': 1, 
                 'email': 'messi@barca.com',
                 'name_first': 'Lionel',
                 'name_last': 'Messi',
                 'handle_str': 'LionelMessi',
                 'profile_img_url' : "",}
    }   


#Test if user_profile works well if the token and user_id are from different user
def test_up_different(url):
    requests.delete(f"{url}/clear")

    data1 = requests.post(f"{url}/auth/register", json = {
        'email':'messi@barca.com', 
        'password':'123456', 
        'name_first':'Lionel', 
        'name_last':'Messi'
    })

    requests.post(f"{url}/auth/register", json = {
        'email':'ronaldo@juventus.com', 
        'password':'654321', 
        'name_first':'Cristiano', 
        'name_last':'Ronaldo'
    })   

    requests.post(f"{url}/auth/register", json = {
        'email':'suarez@atmadrid.com', 
        'password':'lovemessi123', 
        'name_first':'Luis', 
        'name_last':'Suarez'
    })    

    data4 = requests.post(f"{url}/auth/register", json = {
        'email':'havertz@chelsea.com', 
        'password':'german098', 
        'name_first':'Kai', 
        'name_last':'Havertz'
    })  

    requests.post(f"{url}/auth/register", json = {
        'email':'bsilva@mancity.com', 
        'password':'iamsilva456', 
        'name_first':'Bernado', 
        'name_last':'Silva'
    }) 

    up = requests.get(f"{url}/user/profile", params = {
        'token':data1.json()['token'],
        'u_id':data4.json()['u_id']
    })  

    assert up.json() == {

        'user': {'u_id': 4, 
                 'email': 'havertz@chelsea.com', 
                 'name_first': 'Kai', 
                 'name_last': 'Havertz', 
                 'handle_str': 'KaiHavertz',
                 'profile_img_url' : "",}
    }
                                                                                                