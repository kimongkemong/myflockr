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

#Basic test, make sure that url works well
def test_echo(url):
    '''
    A simple test to check echo
    '''
    resp = requests.get(url + 'echo', params={'data': 'hello'})
    assert json.loads(resp.text) == {'data': 'hello'}


#Tests for channel_details

#Given two wrong input (wrong token and wrong channel_id), then channel_details will
#raise AccessError. (Since we assume it will always examine token first)
def test_details_empty(url):
    requests.delete(f"{url}/clear")

    res = requests.get(f"{url}/channel/details", params = {
        'token':1, 
        'channel_id':1
    })

    assert res.json()['code'] == 400


#In this test, channel_details takes a token which belongs to a user who is not a channel member.
#Thus, channel_details will raise AccessError
def test_details_NotMember(url):
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

    res = requests.get(f"{url}/channel/details", params = {
        'token': data3.json()['token'], 
        'channel_id':channel.json()['channel_id']
    })  

    assert res.status_code == 400


#In this test, channel_details takes a negative channel_id(which is invalid).
#Thus, channel_details will raise InputError
def test_details_InvalidChannelID(url):

    requests.delete(f"{url}/clear")

    data1 = requests.post(f"{url}/auth/register", json = {
        'email':'messi@barca.com', 
        'password':'123456', 
        'name_first':'Lionel', 
        'name_last':'Messi'
    })

    channel = requests.post(f"{url}/channels/create", json = {
        'token':data1.json()['token'],
        'name':'worldteam',
        'is_public': False
    })

    res = requests.get(f"{url}/channel/details", params = {
        'token': data1.json()['token'], 
        'channel_id':-channel.json()['channel_id']
    })  

    assert res.status_code == 400   


#In this test, channel_details takes a token which belongs to a user who is a channel member 
#but not an owner.
#Thus, channel_details will still return details of the channel.
def test_details_NotOwner(url):

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

    channel_detail = requests.get(f"{url}/channel/details", params = {
        'token': data4.json()['token'], 
        'channel_id':channel.json()['channel_id']
    }) 

    assert channel_detail.json() == {'name': 'worldteam', 
                                     'owner_members': [
                                            {'u_id': 1, 
                                             'name_first': 'Lionel', 
                                             'name_last': 'Messi',
                                             'profile_img_url' : "",}, 
                                            {'u_id': 2, 
                                             'name_first': 'Cristiano', 
                                             'name_last': 'Ronaldo',
                                             'profile_img_url' : "",}, 
                                            {'u_id': 5, 
                                             'name_first': 'Bernado', 
                                             'name_last': 'Silva',
                                             'profile_img_url' : "",}], 
                                             'all_members': [
                                            {'u_id': 1, 
                                             'name_first': 'Lionel', 
                                             'name_last': 'Messi',
                                             'profile_img_url' : "",}, 
                                            {'u_id': 2, 
                                             'name_first': 'Cristiano', 
                                             'name_last': 'Ronaldo',
                                             'profile_img_url' : "",}, 
                                            {'u_id': 5, 
                                             'name_first': 'Bernado', 
                                             'name_last': 'Silva',
                                             'profile_img_url' : "",},
                                            {'u_id': 4, 
                                             'name_first': 'Kai', 
                                             'name_last': 'Havertz',
                                             'profile_img_url' : "",}]}                                                                                                     


#In this test, channel_details takes two valid arguments. So it will return correct outputs
def test_details_Owner(url):
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

    channel_detail = requests.get(f"{url}/channel/details", params = {
        'token': data1.json()['token'], 
        'channel_id':channel.json()['channel_id']
    }) 

    assert channel_detail.json() == {'name': 'worldteam', 
                                     'owner_members': [
                                         {'u_id': 1, 
                                          'name_first': 'Lionel', 
                                          'name_last': 'Messi',
                                          'profile_img_url' : "",}, 
                                         {'u_id': 2, 
                                          'name_first': 'Cristiano', 
                                          'name_last': 'Ronaldo',
                                          'profile_img_url' : "",}, 
                                         {'u_id': 5, 
                                          'name_first': 'Bernado', 
                                          'name_last': 'Silva',
                                          'profile_img_url' : "",}], 
                                     'all_members': [
                                         {'u_id': 1, 
                                          'name_first': 'Lionel', 
                                          'name_last': 'Messi',
                                          'profile_img_url' : "",}, 
                                         {'u_id': 2, 
                                          'name_first': 'Cristiano', 
                                          'name_last': 'Ronaldo',
                                          'profile_img_url' : "",}, 
                                         {'u_id': 5, 
                                          'name_first': 'Bernado', 
                                          'name_last': 'Silva',
                                          'profile_img_url' : "",},
                                         {'u_id': 4, 
                                          'name_first': 'Kai', 
                                          'name_last': 'Havertz',
                                          'profile_img_url' : "",}]}


#In this case, we create more channels, and see that if channel_details takes in two valid args,
#it still works well.
def test_details_MoreChannels(url):

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

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token':data1.json()['token'],
        'name':'worldteam',
        'is_public': False
    })

    requests.post(f"{url}/channel/addowner", json = {
        'token': data1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'u_id': data2.json()['u_id']
    }) 

    requests.post(f"{url}/channel/addowner", json = {
        'token': data1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'u_id': data5.json()['u_id']
    })   

    requests.post(f"{url}/channel/invite", json = {
        'token': data1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'u_id': data3.json()['u_id']
    }) 

    requests.post(f"{url}/channel/invite", json = {
        'token': data1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'u_id': data4.json()['u_id']
    }) 

    channel2 = requests.post(f"{url}/channels/create", json = {
        'token':data2.json()['token'],
        'name':'Portugual',
        'is_public': False
    })

    requests.post(f"{url}/channel/invite", json = {
        'token': data2.json()['token'],
        'channel_id': channel2.json()['channel_id'],
        'u_id': data5.json()['u_id']
    })    

    channel3 = requests.post(f"{url}/channels/create", json = {
        'token':data1.json()['token'],
        'name':'gonetoSpain',
        'is_public': False
    }) 

    requests.post(f"{url}/channel/invite", json = {
        'token': data1.json()['token'],
        'channel_id': channel3.json()['channel_id'],
        'u_id': data2.json()['u_id']
    }) 

    requests.post(f"{url}/channel/invite", json = {
        'token': data1.json()['token'],
        'channel_id': channel3.json()['channel_id'],
        'u_id': data3.json()['u_id']
    }) 

    channel4 = requests.post(f"{url}/channels/create", json = {
        'token':data4.json()['token'],
        'name':'forFans',
        'is_public': True
    })

    requests.post(f"{url}/channel/invite", json = {
        'token': data4.json()['token'],
        'channel_id': channel4.json()['channel_id'],
        'u_id': data1.json()['u_id']
    }) 

    requests.post(f"{url}/channel/invite", json = {
        'token': data4.json()['token'],
        'channel_id': channel4.json()['channel_id'],
        'u_id': data2.json()['u_id']
    })   

    requests.post(f"{url}/channel/invite", json = {
        'token': data4.json()['token'],
        'channel_id': channel4.json()['channel_id'],
        'u_id': data3.json()['u_id']
    }) 

    requests.post(f"{url}/channel/invite", json = {
        'token': data4.json()['token'],
        'channel_id': channel4.json()['channel_id'],
        'u_id': data5.json()['u_id']
    })   

    channel_detail = requests.get(f"{url}/channel/details", params = {
        'token': data1.json()['token'], 
        'channel_id':channel3.json()['channel_id']
    })   

    assert channel_detail.json() == {'name': 'gonetoSpain', 
                                     'owner_members': [
                                         {'u_id': 1, 
                                          'name_first': 'Lionel', 
                                          'name_last': 'Messi',
                                          'profile_img_url' : "",}], 
                                     'all_members': [
                                         {'u_id': 1, 
                                          'name_first': 'Lionel', 
                                          'name_last': 'Messi',
                                          'profile_img_url' : "",}, 
                                         {'u_id': 2, 
                                          'name_first': 'Cristiano', 
                                          'name_last': 'Ronaldo',
                                          'profile_img_url' : "",}, 
                                         {'u_id': 3, 
                                          'name_first': 'Luis', 
                                          'name_last': 'Suarez',
                                          'profile_img_url' : "",}]}            


#Tests for channel_addowner


#Given three wrong input (wrong token ,wrong channel_id and wrong user_id), 
#then channel_addowner will
#raise AccessError. (Since we assume it will always examine token first)
def test_addowner_empty(url):
    requests.delete(f"{url}/clear")

    res = requests.post(f"{url}/channel/addowner", json = {
        'token':1,
        'channel_id':1,
        'u_id':1
    })

    assert res.status_code == 400


#In this test, channel_addowner takes in an invalid channel id.
#Thus, channel_addowner will raise InputError
def test_addowner_InvalidChannelId(url):

    requests.delete(f"{url}/clear")

    data1 = requests.post(f"{url}/auth/register", json = {
        'email':'messi@barca.com', 
        'password':'123456', 
        'name_first':'Lionel', 
        'name_last':'Messi'
    })

    channel = requests.post(f"{url}/channels/create", json = {
        'token':data1.json()['token'],
        'name':'worldteam',
        'is_public': False
    })

    res = requests.post(f"{url}/channel/addowner", json = {
        'token':data1.json()['token'],
        'channel_id':-channel.json()['channel_id'],
        'u_id':data1.json()['u_id'] + 1
    })

    assert res.status_code == 400 


#In this test, the token is from a user who is not the owner of the channel,
#Thus channel_addowner will raise an AccessError
def test_add_notOwner(url):
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

    res = requests.post(f"{url}/channel/addowner", json = {
        'token': data4.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data3.json()['u_id']
    })      

    assert res.status_code == 400


#In this test, channel_addowner takes a user_id which belongs to a user who is not a channel member.
#So the user will be added as an owner of the channel as well as a member.
def test_add_NotMember(url):

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

    requests.post(f"{url}/channel/addowner", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data3.json()['u_id']
    })                                                                                                                                                   

    channel_detail = requests.get(f"{url}/channel/details", params = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id']
    }) 

    channel_detail = channel_detail.json()                                                 

    assert len(channel_detail['owner_members']) == 4

    assert len(channel_detail['all_members']) == 5


#In this test, channel_addowner takes all valid args. Just test its validity when there are
#more than 2 channels.
def test_add_Morechannels(url):
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

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token':data1.json()['token'],
        'name':'worldteam',
        'is_public': False
    })

    requests.post(f"{url}/channel/addowner", json = {
        'token': data1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'u_id': data2.json()['u_id']
    }) 

    requests.post(f"{url}/channel/addowner", json = {
        'token': data1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'u_id': data5.json()['u_id']
    })   

    requests.post(f"{url}/channel/invite", json = {
        'token': data1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'u_id': data3.json()['u_id']
    }) 

    requests.post(f"{url}/channel/invite", json = {
        'token': data1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'u_id': data4.json()['u_id']
    }) 

    channel2 = requests.post(f"{url}/channels/create", json = {
        'token':data2.json()['token'],
        'name':'Portugual',
        'is_public': False
    })

    requests.post(f"{url}/channel/invite", json = {
        'token': data2.json()['token'],
        'channel_id': channel2.json()['channel_id'],
        'u_id': data5.json()['u_id']
    })    

    channel3 = requests.post(f"{url}/channels/create", json = {
        'token':data1.json()['token'],
        'name':'gonetoSpain',
        'is_public': False
    }) 

    requests.post(f"{url}/channel/invite", json = {
        'token': data1.json()['token'],
        'channel_id': channel3.json()['channel_id'],
        'u_id': data2.json()['u_id']
    }) 

    requests.post(f"{url}/channel/invite", json = {
        'token': data1.json()['token'],
        'channel_id': channel3.json()['channel_id'],
        'u_id': data3.json()['u_id']
    }) 

    channel4 = requests.post(f"{url}/channels/create", json = {
        'token':data4.json()['token'],
        'name':'forFans',
        'is_public': True
    })

    requests.post(f"{url}/channel/invite", json = {
        'token': data4.json()['token'],
        'channel_id': channel4.json()['channel_id'],
        'u_id': data1.json()['u_id']
    }) 

    requests.post(f"{url}/channel/invite", json = {
        'token': data4.json()['token'],
        'channel_id': channel4.json()['channel_id'],
        'u_id': data2.json()['u_id']
    })   

    requests.post(f"{url}/channel/invite", json = {
        'token': data4.json()['token'],
        'channel_id': channel4.json()['channel_id'],
        'u_id': data3.json()['u_id']
    }) 

    requests.post(f"{url}/channel/invite", json = {
        'token': data4.json()['token'],
        'channel_id': channel4.json()['channel_id'],
        'u_id': data5.json()['u_id']
    }) 

    requests.post(f"{url}/channel/addowner", json = {
        'token': data1.json()['token'],
        'channel_id': channel3.json()['channel_id'],
        'u_id': data5.json()['u_id']
    })                                                 

    channel_detail = requests.get(f"{url}/channel/details", params = {
        'token': data1.json()['token'], 
        'channel_id':channel3.json()['channel_id']
    }) 

    channel_detail = channel_detail.json()                                                                  

    assert len(channel_detail['owner_members']) == 2


#If channel_addowner takes user_id from a user who is already an owner of the channel,
#then channel_addowner will raise an InputError
def test_add_InOwner(url):
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
        'name_last':'Havertz'})  

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

    res = requests.post(f"{url}/channel/addowner", json = {
        'token': data1.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data1.json()['u_id']
    })  

    assert res.status_code == 400


#Tests for channel_removeowner


#Given three wrong input (wrong token ,wrong channel_id and wrong user_id), 
#then channel_removeowner will
#raise AccessError. (Since we assume it will always examine token first)
def test_rem_empty(url):
    requests.delete(f"{url}/clear")

    res = requests.post(f"{url}/channel/removeowner", json = {
        'token': 1,
        'channel_id': 1,
        'u_id': 1
    })

    assert res.status_code == 400


#In this test, channel_removeowner takes in an invalid channel id.
#Thus, channel_removeowner will raise InputError
def test_rem_InvalidChannelId(url):
    requests.delete(f"{url}/clear")

    data1 = requests.post(f"{url}/auth/register", json = {
        'email':'messi@barca.com', 
        'password':'123456', 
        'name_first':'Lionel', 
        'name_last':'Messi'
    })

    channel = requests.post(f"{url}/channels/create", json = {
        'token':data1.json()['token'],
        'name':'worldteam',
        'is_public': False
    })

    res = requests.post(f"{url}/channel/removeowner", json = {
        'token':data1.json()['token'],
        'channel_id':-channel.json()['channel_id'],
        'u_id':data1.json()['u_id']
    })

    assert res.status_code == 400


#In this test, the token is from a user who is not the owner of the channel,
#Thus channel_removeowner will raise an AccessError
def test_rem_NotOwner(url):
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
        'name_last':'Havertz'})  

    data5 = requests.post(f"{url}/auth/register", json = {
        'email':'bsilva@mancity.com', 
        'password':'iamsilva456', 
        'name_first':'Bernado', 
        'name_last':'Silva'
    })

    channel = requests.post(f"{url}/channels/create", json = {
        'token':data1.json()['token'],
        'name':'worldteam',
        'is_public': False})

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

    res = requests.post(f"{url}/channel/removeowner", json = {
        'token': data4.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data1.json()['u_id']
    })  

    assert res.status_code == 400


#In this test we only check that channel_removeowner works well when there are more than 
#2 channels.
def test_rem_MoreChannels(url):
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

    channel1 = requests.post(f"{url}/channels/create", json = {
        'token':data1.json()['token'],
        'name':'worldteam',
        'is_public': False
    })

    requests.post(f"{url}/channel/addowner", json = {
        'token': data1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'u_id': data2.json()['u_id']
    }) 

    requests.post(f"{url}/channel/addowner", json = {
        'token': data1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'u_id': data5.json()['u_id']
    })   

    requests.post(f"{url}/channel/invite", json = {
        'token': data1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'u_id': data3.json()['u_id']
    }) 

    requests.post(f"{url}/channel/invite", json = {
        'token': data1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'u_id': data4.json()['u_id']
    }) 

    channel2 = requests.post(f"{url}/channels/create", json = {
        'token':data2.json()['token'],
        'name':'Portugual',
        'is_public': False
    })

    requests.post(f"{url}/channel/invite", json = {
        'token': data2.json()['token'],
        'channel_id': channel2.json()['channel_id'],
        'u_id': data5.json()['u_id']
    })    

    channel3 = requests.post(f"{url}/channels/create", json = {
        'token':data1.json()['token'],
        'name':'gonetoSpain',
        'is_public': False
    }) 

    requests.post(f"{url}/channel/invite", json = {
        'token': data1.json()['token'],
        'channel_id': channel3.json()['channel_id'],
        'u_id': data2.json()['u_id']
    }) 

    requests.post(f"{url}/channel/invite", json = {
        'token': data1.json()['token'],
        'channel_id': channel3.json()['channel_id'],
        'u_id': data3.json()['u_id']
    }) 

    channel4 = requests.post(f"{url}/channels/create", json = {
        'token':data4.json()['token'],
        'name':'forFans',
        'is_public': True
    })

    requests.post(f"{url}/channel/invite", json = {
        'token': data4.json()['token'],
        'channel_id': channel4.json()['channel_id'],
        'u_id': data1.json()['u_id']
    }) 

    requests.post(f"{url}/channel/invite", json = {
        'token': data4.json()['token'],
        'channel_id': channel4.json()['channel_id'],
        'u_id': data2.json()['u_id']
    })   

    requests.post(f"{url}/channel/invite", json = {
        'token': data4.json()['token'],
        'channel_id': channel4.json()['channel_id'],
        'u_id': data3.json()['u_id']
    }) 

    requests.post(f"{url}/channel/invite", json = {
        'token': data4.json()['token'],
        'channel_id': channel4.json()['channel_id'],
        'u_id': data5.json()['u_id']
    }) 

    requests.post(f"{url}/channel/removeowner", json = {
        'token': data2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'u_id': data1.json()['u_id']
    })                                                 

    channel_detail = requests.get(f"{url}/channel/details", params = {
        'token': data2.json()['token'], 
        'channel_id':channel1.json()['channel_id']
    })

    channel_detail = channel_detail.json()                                                                   

    assert len(channel_detail['owner_members']) == 2


#In our assumption, we assume that the owner can't be removed if he is the only owner of the channel
#So in this case, channel_removeowner will raise an InputError.
def test_rem_OneOwner(url):
    requests.delete(f"{url}/clear")

    requests.post(f"{url}/auth/register", json = {
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
        'token':data4.json()['token'],
        'name':'forFans',
        'is_public': True
    })

    requests.post(f"{url}/channel/invite", json = {
        'token': data4.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data2.json()['u_id']
    }) 

    requests.post(f"{url}/channel/invite", json = {
        'token': data4.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data3.json()['u_id']
    })   

    requests.post(f"{url}/channel/invite", json = {
        'token': data4.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data5.json()['u_id']
    })                                               

    res = requests.post(f"{url}/channel/removeowner", json = {
        'token': data4.json()['token'],
        'channel_id': channel.json()['channel_id'],
        'u_id': data4.json()['u_id']
    })  

    assert res.status_code == 400













                                                                                                                                                                                                                                                                                             











