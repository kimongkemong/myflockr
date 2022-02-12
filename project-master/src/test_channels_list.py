'''Testing the channels list function'''
import pytest
from channels import channels_create, channels_list
from other import clear
from auth import auth_register
from error import AccessError

def test_channels_list_valid_token():
    '''listing channel success with valid token'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    user2 = auth_register('testemail2@test.com', 'testing124', 'comp', '1531')
    channels_create(user1['token'], "Channel1", True)
    channels_create(user1['token'], "Channel2", False)
    channels_create(user2['token'], "Channel3", True)
    assert channels_list(user1['token']) == {'channels': [
        {'channel_id': 1, 'name': 'Channel1'},
        {'channel_id': 2, 'name': 'Channel2'}]}

def test_channels_list_spesific_user():
    '''list channel with a requested user in it'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    user2 = auth_register('testemail2@test.com', 'testing124', 'comp', '1531')
    user3 = auth_register('testemail3@test.com', 'testing125', 'test2', 'program4')
    channels_create(user1['token'], "Channel1", True)
    channels_create(user2['token'], "Channel2", True)
    channels_create(user2['token'], "Channel3", False)
    channels_create(user3['token'], "Channel4", True)
    assert channels_list(user3['token']) == {'channels': [
        {'channel_id': 4, 'name': 'Channel4'}]}

def test_channels_list_no_channels():
    '''list channel when there is no channel created'''
    clear()
    user1 = auth_register('testemail4@test.com', 'testing145', 'comp1', '1511')
    assert channels_list(user1['token']) == {'channels': []}

def test_channels_list_no_channel_as_requested():
    '''list channel when there is no channel that the users are in it'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    user2 = auth_register('testemail2@test.com', 'testing124', 'comp', '1531')
    user3 = auth_register('testemail3@test.com', 'testing125', 'test2', 'program4')
    channels_create(user1['token'], "Channel1", True)
    channels_create(user1['token'], "Channel2", False)
    channels_create(user2['token'], "Channel3", True)
    channels_create(user2['token'], "Channel4", False)
    assert channels_list(user3['token']) == {'channels': []}

def test_channels_list_1_channels():
    '''list channel as user request when there is only one channel'''
    clear()
    user1 = auth_register('testemail2@test.com', 'testing124', 'comp', '1531')
    channels_create(user1['token'], "Channel1", True)
    assert channels_list(user1['token']) == {'channels': [
        {'channel_id': 1, 'name': 'Channel1'}]}

def test_channels_list_more_spesific_user():
    '''list channel as requested by user'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    user2 = auth_register('testemail2@test.com', 'testing124', 'comp', '1531')
    user3 = auth_register('testemail3@test.com', 'testing125', 'test2', 'program4')
    channels_create(user1['token'], "Channel1", True)
    channels_create(user2['token'], "Channel2", False)
    channels_create(user3['token'], "Channel3", True)
    channels_create(user2['token'], "Channel4", False)
    assert channels_list(user2['token']) == {'channels': [
        {'channel_id': 2, 'name': 'Channel2'},
        {'channel_id': 4, 'name': 'Channel4'}]}

def test_channels_invalid_token():
    '''listing channel with invalid token'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    user2 = auth_register('testemail2@test.com', 'testing124', 'comp', '1531')
    channels_create(user1['token'], "Channel1", True)
    channels_create(user2['token'], "Channel2", False)
    with pytest.raises(AccessError):
        channels_list(123456)

def test_channels_invalid_token_after():
    '''listing channel after invalid token and '''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    user2 = auth_register('testemail2@test.com', 'testing124', 'comp', '1531')
    channels_create(user1['token'], "Channel1", True)
    channels_create(user2['token'], "Channel2", False)
    with pytest.raises(AccessError):
        channels_list(123485)
    channels_create(user2['token'], "Channel3", True)
    assert channels_list(user2['token']) == {'channels': [
        {'channel_id': 2, 'name': 'Channel2'},
        {'channel_id': 3, 'name': 'Channel3'}]}
