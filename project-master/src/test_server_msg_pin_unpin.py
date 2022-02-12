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


#Make sure that url works well
def test_echo(url):
    '''
    A simple test to check echo
    '''
    resp = requests.get(url + 'echo', params={'data': 'hello'})
    assert json.loads(resp.text) == {'data': 'hello'}


#Tests for message_pin_flask

#If msg_pin is given two invalid args, then it will raise AccessError
#(We always assume that it will examine token first)
def test_pin_empty(url):
    requests.delete(f"{url}/clear")

    res = requests.post(f"{url}/message/pin", json = {
        'token': 1,
        'message_id': 1
    })

    assert res.status_code == 400


#If the msg_id is from a message which is already pinned, 
#Then msg_pin raise an InputError.
def test_pin_Pinned(url):
    requests.delete(f"{url}/clear")

    data1 = requests.post(f"{url}/auth/register", json = {
        'email':'messi@barca.com', 
        'password':'123456', 
        'name_first':'Lionel', 
        'name_last':'Messi'
    })

    data2 = requests.post(f"{url}/auth/register", json = {
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

    data5 = requests.post(f"{url}/auth/register", json = {
        'email':'bsilva@mancity.com', 
        'password':'iamsilva456', 
        'name_first':'Bernado', 
        'name_last':'Silva'
    }) 

    channel = requests.post(f"{url}/channels/create", json = {
        'token':data1.json()['token'],
        'name':'worldteam',
        'is_public': False
    })

    requests.post(f"{url}/channel/addowner", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data2.json()['u_id']
    }) 

    requests.post(f"{url}/channel/addowner", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data5.json()['u_id']
    })   

    requests.post(f"{url}/channel/invite", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data4.json()['u_id']
    })  

    message = requests.post(f"{url}/message/send", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'message': "Hello"
    })  

    requests.post(f"{url}/message/pin", json = {
        'token': data1.json()['token'],
        'message_id': message.json()['message_id']
    })

    res = requests.post(f"{url}/message/pin", json = {
        'token': data1.json()['token'],
        'message_id': message.json()['message_id']
    })

    assert res.json()['code'] == 400


#If the token is from a user who is not a member of the channel, 
#Then msg_pin raise an AccessError
def test_pin_NotMember(url):
    requests.delete(f"{url}/clear")

    data1 = requests.post(f"{url}/auth/register", json = {
        'email':'messi@barca.com', 
        'password':'123456', 
        'name_first':'Lionel', 
        'name_last':'Messi'
    })

    data2 = requests.post(f"{url}/auth/register", json = {
        'email':'ronaldo@juventus.com', 
        'password':'654321', 
        'name_first':'Cristiano', 
        'name_last':'Ronaldo'
    })   

    data3 = requests.post(f"{url}/auth/register", json = {
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

    data5 = requests.post(f"{url}/auth/register", json = {
        'email':'bsilva@mancity.com', 
        'password':'iamsilva456', 
        'name_first':'Bernado', 
        'name_last':'Silva'
    }) 

    channel = requests.post(f"{url}/channels/create", json = {
        'token':data1.json()['token'],
        'name':'worldteam',
        'is_public': False
    })

    requests.post(f"{url}/channel/addowner", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data2.json()['u_id']
    }) 

    requests.post(f"{url}/channel/addowner", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data5.json()['u_id']
    })   

    requests.post(f"{url}/channel/invite", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data4.json()['u_id']
    })  

    message = requests.post(f"{url}/message/send", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'message': "Hello"
    })  

    res = requests.post(f"{url}/message/pin", json = {
        'token': data3.json()['token'],
        'message_id': message.json()['message_id']
    })

    assert res.json()['code'] == 400


#If both args are valid, then msg_pin works well
#We examine by calling msg_unpin and no error is raised.
def test_pin_Success(url):
    requests.delete(f"{url}/clear")

    data1 = requests.post(f"{url}/auth/register", json = {
        'email':'messi@barca.com', 
        'password':'123456', 
        'name_first':'Lionel', 
        'name_last':'Messi'
    })

    data2 = requests.post(f"{url}/auth/register", json = {
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

    data5 = requests.post(f"{url}/auth/register", json = {
        'email':'bsilva@mancity.com', 
        'password':'iamsilva456', 
        'name_first':'Bernado', 
        'name_last':'Silva'
    }) 

    channel = requests.post(f"{url}/channels/create", json = {
        'token':data1.json()['token'],
        'name':'worldteam',
        'is_public': False
    })

    requests.post(f"{url}/channel/addowner", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data2.json()['u_id']
    }) 

    requests.post(f"{url}/channel/addowner", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data5.json()['u_id']
    })   

    requests.post(f"{url}/channel/invite", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data4.json()['u_id']
    })  

    message = requests.post(f"{url}/message/send", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'message': "Hello"
    })  

    res = requests.post(f"{url}/message/pin", json = {
        'token': data1.json()['token'],
        'message_id': message.json()['message_id']
    })

    assert res.status_code == 200


    #Tests for message_unpin_flask


#If msg_unpin is given two invalid args, then it will raise AccessError
#(We always assume that it will examine token first)
def test_unpin_empty(url):
    requests.delete(f"{url}/clear")

    res = requests.post(f"{url}/message/unpin", json = {
        'token': 1,
        'message_id': 1
    })

    assert res.json()['code'] == 400


#If the msg_id is from a message which is already pinned, 
#Then msg_unpin raise an InputError.
def test_unpin_Pinned(url):
    requests.delete(f"{url}/clear")

    data1 = requests.post(f"{url}/auth/register", json = {
        'email':'messi@barca.com', 
        'password':'123456', 
        'name_first':'Lionel', 
        'name_last':'Messi'
    })

    data2 = requests.post(f"{url}/auth/register", json = {
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

    data5 = requests.post(f"{url}/auth/register", json = {
        'email':'bsilva@mancity.com', 
        'password':'iamsilva456', 
        'name_first':'Bernado', 
        'name_last':'Silva'
    }) 

    channel = requests.post(f"{url}/channels/create", json = {
        'token':data1.json()['token'],
        'name':'worldteam',
        'is_public': False
    })

    requests.post(f"{url}/channel/addowner", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data2.json()['u_id']
    }) 

    requests.post(f"{url}/channel/addowner", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data5.json()['u_id']
    })   

    requests.post(f"{url}/channel/invite", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data4.json()['u_id']
    })  

    message = requests.post(f"{url}/message/send", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'message': "Hello"
    })  

    requests.post(f"{url}/message/unpin", json = {
        'token': data1.json()['token'],
        'message_id': message.json()['message_id']
    })

    res = requests.post(f"{url}/message/unpin", json = {
        'token': data1.json()['token'],
        'message_id': message.json()['message_id']
    })

    assert res.json()['code'] == 400


#If the token is from a user who is not a member of the channel, 
#Then msg_unpin raise an AccessError
def test_unpin_NotMember(url):
    requests.delete(f"{url}/clear")

    data1 = requests.post(f"{url}/auth/register", json = {
        'email':'messi@barca.com', 
        'password':'123456', 
        'name_first':'Lionel', 
        'name_last':'Messi'
    })

    data2 = requests.post(f"{url}/auth/register", json = {
        'email':'ronaldo@juventus.com', 
        'password':'654321', 
        'name_first':'Cristiano', 
        'name_last':'Ronaldo'
    })   

    data3 = requests.post(f"{url}/auth/register", json = {
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

    data5 = requests.post(f"{url}/auth/register", json = {
        'email':'bsilva@mancity.com', 
        'password':'iamsilva456', 
        'name_first':'Bernado', 
        'name_last':'Silva'
    }) 

    channel = requests.post(f"{url}/channels/create", json = {
        'token':data1.json()['token'],
        'name':'worldteam',
        'is_public': False
    })

    requests.post(f"{url}/channel/addowner", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data2.json()['u_id']
    }) 

    requests.post(f"{url}/channel/addowner", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data5.json()['u_id']
    })   

    requests.post(f"{url}/channel/invite", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data4.json()['u_id']
    })  

    message = requests.post(f"{url}/message/send", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'message': "Hello"
    })  

    res = requests.post(f"{url}/message/unpin", json = {
        'token': data3.json()['token'],
        'message_id': message.json()['message_id']
    })

    assert res.json()['code'] == 400


#If both args are valid, then msg_unpin works well
#We examine by calling msg_pin and no error is raised.
def test_unpin_Success(url):
    requests.delete(f"{url}/clear")

    data1 = requests.post(f"{url}/auth/register", json = {
        'email':'messi@barca.com', 
        'password':'123456', 
        'name_first':'Lionel', 
        'name_last':'Messi'
    })

    data2 = requests.post(f"{url}/auth/register", json = {
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

    data5 = requests.post(f"{url}/auth/register", json = {
        'email':'bsilva@mancity.com', 
        'password':'iamsilva456', 
        'name_first':'Bernado', 
        'name_last':'Silva'
    }) 

    channel = requests.post(f"{url}/channels/create", json = {
        'token':data1.json()['token'],
        'name':'worldteam',
        'is_public': False
    })

    requests.post(f"{url}/channel/addowner", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data2.json()['u_id']
    }) 

    requests.post(f"{url}/channel/addowner", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data5.json()['u_id']
    })   

    requests.post(f"{url}/channel/invite", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data4.json()['u_id']
    })  

    message = requests.post(f"{url}/message/send", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'message': "Hello"
    }) 

    requests.post(f"{url}/message/pin", json = {
        'token': data1.json()['token'],
        'message_id': message.json()['message_id']
    }) 

    res = requests.post(f"{url}/message/unpin", json = {
        'token': data1.json()['token'],
        'message_id': message.json()['message_id']
    })

    assert res.status_code == 200