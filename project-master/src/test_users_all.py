from user import *
import auth as a
import channel as c
import channels as cs
from other import clear, users_all
import pytest



#If the token is invalid, then raise an AccessError
def test_ua_empty():
    clear()
    with pytest.raises(AccessError):
        users_all(1)


#If the token is valid, then all the user profiles will be returned
def test_ua_valid():
    clear()
    data1 = a.auth_register('messi@barca.com', '123456', 'Lionel', 'Messi')
    a.auth_register('ronaldo@juventus.com', '654321', 'Cristiano', 'Ronaldo')
    a.auth_register('suarez@atmadrid.com', 'lovemessi123', 'Luis', 'Suarez')
    a.auth_register('havertz@chelsea.com', 'german098', 'Kai', 'Havertz')
    a.auth_register('bsilva@mancity.com', 'iamsilva456', 'Bernado', 'Silva')
    
    assert users_all(data1['token']) == {
        'users': [{'u_id': 1, 
                   'email': 'messi@barca.com', 
                   'name_first': 'Lionel', 
                   'name_last': 'Messi', 
                   'handle_str': 'LionelMessi',
                   'profile_img_url' : "",}, 
                  {'u_id': 2, 'email': 
                   'ronaldo@juventus.com', 
                   'name_first': 'Cristiano', 
                   'name_last': 'Ronaldo', 
                   'handle_str': 'CristianoRonaldo',
                   'profile_img_url' : "",}, 
                  {'u_id': 3, 
                   'email': 'suarez@atmadrid.com', 
                   'name_first': 'Luis', 
                   'name_last': 'Suarez', 
                   'handle_str': 'LuisSuarez',
                   'profile_img_url' : "",}, 
                  {'u_id': 4, 
                   'email': 'havertz@chelsea.com', 
                   'name_first': 'Kai', 
                   'name_last': 'Havertz', 
                   'handle_str': 'KaiHavertz',
                   'profile_img_url' : "",}, 
                  {'u_id': 5, 
                   'email': 'bsilva@mancity.com', 
                   'name_first': 'Bernado', 
                   'name_last': 'Silva', 
                   'handle_str': 'BernadoSilva',
                   'profile_img_url' : "",}]
    }


