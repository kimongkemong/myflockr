'''Testing the channel_create function'''
import pytest
from channels import channels_create, channels_listall
from other import clear
from auth import auth_register
from error import AccessError, InputError

def test_channels_create_success():
    '''creating one success test'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    assert channels_create(user1['token'], "Project COMP1531 T3", True) == {'channel_id': 1}
    assert channels_listall(user1['token']) == {'channels':[
        {'channel_id': 1, 'name': 'Project COMP1531 T3'}]}

def test_channels_create_long_name():
    '''create channel with long name'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    with pytest.raises(InputError):
        channels_create(user1['token'], "Project COMP1531 T3 UNSW", True)
    assert channels_listall(user1['token']) == {'channels': []}

def test_channels_create_private():
    '''creating a private channel'''
    clear()
    user1 = auth_register('testemail2@test.com', 'testing123', 'test', 'program')
    assert channels_create(user1['token'], "Project COMP1531 T3", False) == {'channel_id': 1}
    assert channels_listall(user1['token']) == {'channels': [
        {'channel_id': 1, 'name': 'Project COMP1531 T3'}]}

def test_channels_create_long_name_private():
    '''creating a private long name channel'''
    clear()
    user1 = auth_register('testemail3@test.com', 'testing123', 'test', 'program')
    with pytest.raises(InputError):
        channels_create(user1['token'], "Project COMP1531 T3 UNSW", False)
    assert channels_listall(user1['token']) == {'channels': []}

def test_channels_add_more_private():
    '''creating more private channel'''
    clear()
    user1 = auth_register('testemail4@test.com', 'testing123', 'test', 'program')
    assert channels_create(user1['token'], "Project COMP1531 T3", False) == {'channel_id': 1}
    assert channels_listall(user1['token']) == {'channels': [
        {'channel_id': 1, 'name': 'Project COMP1531 T3'}]}

def test_channels_more_public():
    '''creating more public channel'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    assert channels_create(user1['token'], "Group 1 grape", True) == {'channel_id': 1}
    assert channels_listall(user1['token']) == {'channels': [
        {'channel_id': 1, 'name': 'Group 1 grape'}]}

def test_channels_invalid_token_one_channel():
    '''creating a channel with invalid token'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    with pytest.raises(AccessError):
        channels_create(123456, "Group 1 grape", False)
    assert channels_listall(user1['token']) == {'channels': []}

def test_channels_one_user_create_more_than_one():
    '''creating more channel with only one user'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    assert channels_create(user1['token'], "Group 1 grape", True) == {'channel_id': 1}
    assert channels_create(user1['token'], "Group 2 grape", False) == {'channel_id': 2}
    assert channels_create(user1['token'], "Group 3 grape", True) == {'channel_id': 3}
    assert channels_listall(user1['token']) == {'channels': [
        {'channel_id': 1, 'name': 'Group 1 grape'},
        {'channel_id': 2, 'name': 'Group 2 grape'},
        {'channel_id': 3, 'name': 'Group 3 grape'}]}

def test_channels_different_user():
    '''creating multiple channel with different user'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    user2 = auth_register('testemail2@test.com', 'testing124', 'comp', '1531')
    assert channels_create(user1['token'], "Group 1 grape", True) == {'channel_id': 1}
    assert channels_create(user2['token'], "Group 2 grape", False) == {'channel_id': 2}
    assert channels_create(user1['token'], "Group 3 grape", True) == {'channel_id': 3}
    assert channels_listall(user1['token']) == {'channels': [
        {'channel_id': 1, 'name': 'Group 1 grape'},
        {'channel_id': 2, 'name': 'Group 2 grape'},
        {'channel_id': 3, 'name': 'Group 3 grape'}]}

def test_channels_invalid_token():
    '''creating a channel then creating a channel with invalid token'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    user2 = auth_register('testemail2@test.com', 'testing124', 'comp', '1531')
    assert channels_create(user1['token'], "Group 1 grape", True) == {'channel_id': 1}
    assert channels_create(user2['token'], "Group 2 grape", False) == {'channel_id': 2}
    with pytest.raises(AccessError):
        channels_create(1234566, "Group 3 grape", False)
    assert channels_listall(user1['token']) == {'channels': [
        {'channel_id': 1, 'name': 'Group 1 grape'},
        {'channel_id': 2, 'name': 'Group 2 grape'}]}

def test_channels_more_invalid_token():
    '''creating a channel after invalid token'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    user2 = auth_register('testemail2@test.com', 'testing124', 'comp', '1531')
    assert channels_create(user1['token'], "Group 1 grape", True) == {'channel_id': 1}
    assert channels_create(user2['token'], "Group 2 grape", False) == {'channel_id': 2}
    with pytest.raises(AccessError):
        channels_create(12378, "Group 3 grape", False)
    assert channels_create(user2['token'], "Group 3 grape", True) == {'channel_id': 3}
    assert channels_listall(user1['token']) == {'channels': [
        {'channel_id': 1, 'name': 'Group 1 grape'},
        {'channel_id': 2, 'name': 'Group 2 grape'},
        {'channel_id': 3, 'name': 'Group 3 grape'}]}