'''Testing for user set email'''
import pytest
from other import clear
from auth import auth_register
from error import AccessError, InputError
from user import user_profile, user_profile_setname

def test_setname_success():
    '''Simple test to make sure the function run properly'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    profile = user_profile(user1['token'], user1['u_id'])
    assert profile == {'user': {'u_id': 1,
                                'email': 'testemail1@test.com',
                                'name_first': 'test',
                                'name_last': 'program',
                                'handle_str': 'testprogram',
                                'profile_img_url' : "",}}
    user_profile_setname(user1['token'], 'real', 'name')
    profile_change = user_profile(user1['token'], user1['u_id'])
    assert profile_change == {'user': {'u_id': 1,
                                       'email': 'testemail1@test.com',
                                       'name_first': 'real',
                                       'name_last': 'name',
                                       'handle_str': 'testprogram',
                                       'profile_img_url' : "",}}

def test_setname_first_name_empty():
    '''Testing to change the first name to be empty'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    profile = user_profile(user1['token'], user1['u_id'])
    assert profile == {'user': {'u_id': 1,
                                'email': 'testemail1@test.com',
                                'name_first': 'test',
                                'name_last': 'program',
                                'handle_str': 'testprogram',
                                'profile_img_url' : "",}}
    with pytest.raises(InputError):
        user_profile_setname(user1['token'], '', 'name')

def test_setname_last_name_empty():
    '''Testing to change the last name to be empty'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    profile = user_profile(user1['token'], user1['u_id'])
    assert profile == {'user': {'u_id': 1,
                                'email': 'testemail1@test.com',
                                'name_first': 'test', 'name_last': 'program',
                                'handle_str': 'testprogram',
                                'profile_img_url' : "",}}
    with pytest.raises(InputError):
        user_profile_setname(user1['token'], 'real', '')

def test_setname_both_name_empty():
    '''Testing to change both of the name to be empty'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    profile = user_profile(user1['token'], user1['u_id'])
    assert profile == {'user': {'u_id': 1,
                                'email': 'testemail1@test.com',
                                'name_first': 'test',
                                'name_last': 'program',
                                'handle_str': 'testprogram',
                                'profile_img_url' : "",}}
    with pytest.raises(InputError):
        user_profile_setname(user1['token'], '', '')

def test_setname_long_first_name():
    '''Testing to change the first name longer than 50 characters'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    profile = user_profile(user1['token'], user1['u_id'])
    assert profile == {'user': {'u_id': 1,
                                'email': 'testemail1@test.com',
                                'name_first': 'test',
                                'name_last': 'program',
                                'handle_str': 'testprogram',
                                'profile_img_url' : "",}}
    with pytest.raises(InputError):
        user_profile_setname(user1['token'],
                             'changenameinfirstnamecannotbemorethan50characters12345678910',
                             'name')

def test_setname_long_last_name():
    '''Testing to change the last name longer than 50 characters'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    profile = user_profile(user1['token'], user1['u_id'])
    assert profile == {'user': {'u_id': 1,
                                'email': 'testemail1@test.com',
                                'name_first': 'test',
                                'name_last': 'program',
                                'handle_str': 'testprogram',
                                'profile_img_url' : "",}}
    with pytest.raises(InputError):
        user_profile_setname(user1['token'],
                             'name',
                             'changenameinlastnamecannotbemorethan50characters12345678910')

def test_setname_long_both_name():
    '''Testing to change the both name longer than 50 characters'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    profile = user_profile(user1['token'], user1['u_id'])
    assert profile == {'user': {'u_id': 1,
                                'email': 'testemail1@test.com',
                                'name_first': 'test',
                                'name_last': 'program',
                                'handle_str': 'testprogram',
                                'profile_img_url' : "",}}
    with pytest.raises(InputError):
        user_profile_setname(user1['token'],
                             'changenameinfirstnamecannotbemorethan50characters12345678910',
                             'changenameinlastnamecannotbemorethan50characters12345678910')

def test_setname_invalid_token():
    '''Testing the function with an invalid token'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    profile = user_profile(user1['token'], user1['u_id'])
    assert profile == {'user': {'u_id': 1,
                                'email': 'testemail1@test.com',
                                'name_first': 'test',
                                'name_last': 'program',
                                'handle_str': 'testprogram',
                                'profile_img_url' : "",}}
    with pytest.raises(AccessError):
        user_profile_setname(12346, 'real', 'name')
