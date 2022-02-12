from user import *
import auth as a
import channel as c
import channels as cs
from other import clear
import pytest


#If both args are invalid, the user_profile func should raise an AccessError first
#(We assume that user_profile always first check token)
def test_up_empty():
    clear()
    with pytest.raises(AccessError):
        user_profile(1, 1)


#If u_id given is from a non-registered user, then user_profile should raise InputError
def test_up_invalid_uid():
    clear()
    a.auth_register('messi@barca.com', '123456', 'Lionel', 'Messi')
    data2 = a.auth_register('ronaldo@juventus.com', '654321', 'Cristiano', 'Ronaldo')
    a.auth_register('suarez@atmadrid.com', 'lovemessi123', 'Luis', 'Suarez')
    a.auth_register('havertz@chelsea.com', 'german098', 'Kai', 'Havertz')
    a.auth_register('bsilva@mancity.com', 'iamsilva456', 'Bernado', 'Silva')

    with pytest.raises(InputError):
        user_profile(data2['token'], - 1)


#Test if user_profile works well if the token and user_id are from the same user
def test_up_same():
    clear()
    data1 = a.auth_register('messi@barca.com', '123456', 'Lionel', 'Messi')
    a.auth_register('ronaldo@juventus.com', '654321', 'Cristiano', 'Ronaldo')
    a.auth_register('suarez@atmadrid.com', 'lovemessi123', 'Luis', 'Suarez')
    a.auth_register('havertz@chelsea.com', 'german098', 'Kai', 'Havertz')
    a.auth_register('bsilva@mancity.com', 'iamsilva456', 'Bernado', 'Silva')

    assert user_profile(data1['token'], data1['u_id']) == {
        'user': {'u_id': 1, 
                 'email': 'messi@barca.com', 
                 'name_first': 'Lionel', 
                 'name_last': 'Messi', 
                 'handle_str': 'LionelMessi',
                 'profile_img_url' : "",}
    }


#Test if user_profile works well if the token and user_id are from different user
def test_up_different():
    clear()
    data1 = a.auth_register('messi@barca.com', '123456', 'Lionel', 'Messi')
    a.auth_register('ronaldo@juventus.com', '654321', 'Cristiano', 'Ronaldo')
    a.auth_register('suarez@atmadrid.com', 'lovemessi123', 'Luis', 'Suarez')
    data4 = a.auth_register('havertz@chelsea.com', 'german098', 'Kai', 'Havertz')
    a.auth_register('bsilva@mancity.com', 'iamsilva456', 'Bernado', 'Silva')

    assert user_profile(data1['token'], data4['u_id']) == {
        'user': {'u_id': 4, 
                 'email': 'havertz@chelsea.com', 
                 'name_first': 'Kai', 
                 'name_last': 'Havertz', 
                 'handle_str': 'KaiHavertz',
                 'profile_img_url' : "",}
    }
