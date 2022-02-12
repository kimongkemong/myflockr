'''Testing channels listall function'''
import pytest
from channels import channels_create, channels_listall
from other import clear
from auth import auth_register
from error import AccessError

def test_channels_listall_valid_token():
    '''list all the channel success with valid token'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    user2 = auth_register('testemail2@test.com', 'testing124', 'comp', '1531')
    channels_create(user1['token'], "Channel1", True)
    channels_create(user1['token'], "Channel2", True)
    channels_create(user2['token'], "Channel3", True)
    assert channels_listall(user1['token']) == {'channels': [
        {'channel_id': 1, 'name': 'Channel1'},
        {'channel_id': 2, 'name': 'Channel2'},
        {'channel_id': 3, 'name': 'Channel3'}]}

def test_channels_listall_1_channels():
    '''list all the channel when there is only one channel'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    channels_create(user1['token'], "Channel1", True)
    assert channels_listall(user1['token']) == {'channels': [
        {'channel_id': 1, 'name': 'Channel1'}]}

def test_channels_listall_no_channels():
    '''list all the channel when there is no channel created'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    assert channels_listall(user1['token']) == {'channels': []}

def test_channels_listall_not_included():
    '''list all the channel even when the users are not in it'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    user2 = auth_register('testemail2@test.com', 'testing124', 'comp', '1531')
    channels_create(user1['token'], "Channel1", True)
    channels_create(user1['token'], "Channel2", True)
    channels_create(user2['token'], "Channel3", False)
    assert channels_listall(user1['token']) == {'channels': [
        {'channel_id': 1, 'name': 'Channel1'},
        {'channel_id': 2, 'name': 'Channel2'},
        {'channel_id': 3, 'name': 'Channel3'}]}

def test_channels_listall_invalid_token():
    '''list all the channel with invalid token'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    user2 = auth_register('testemail2@test.com', 'testing124', 'comp', '1531')
    channels_create(user1['token'], "Channel1", True)
    channels_create(user1['token'], "Channel2", True)
    channels_create(user2['token'], "Channel3", False)
    with pytest.raises(AccessError):
        channels_listall(123456)

def test_channels_listall_more_invalid_token():
    '''list all the channel after an invalid token'''
    clear()
    user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
    user2 = auth_register('testemail2@test.com', 'testing124', 'comp', '1531')
    channels_create(user1['token'], "Channel1", True)
    channels_create(user1['token'], "Channel2", True)
    channels_create(user2['token'], "Channel3", False)
    with pytest.raises(AccessError):
        channels_listall(125848)
    assert channels_listall(user1['token']) == {'channels': [
        {'channel_id': 1, 'name': 'Channel1'},
        {'channel_id': 2, 'name': 'Channel2'},
        {'channel_id': 3, 'name': 'Channel3'}]}
