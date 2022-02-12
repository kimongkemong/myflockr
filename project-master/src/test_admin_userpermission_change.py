'''Test for changing permission'''
import pytest
from other import clear, admin_userpermission_change
from auth import auth_register
from error import AccessError, InputError
import channel as c
import channels as ch

def test_permission_change_success():
	'''Simple test to make sure the function run properly'''
	clear()
	user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
	user2 = auth_register('testemail2@test.com', 'testing122', 'test2', 'program2')
	user3 = auth_register('testemail3@test.com', 'testing122', 'test3', 'program3')
	ch_1 = ch.channels_create(user1['token'], "Soloist", True)

	admin_userpermission_change(user1['token'],user2['u_id'],1)
	c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
	#MAKE SURE THE GLOBAL OWNER IS NOT AN OWNER IN A CHANNEL
	assert len(c.channel_details(user1['token'], ch_1['channel_id'])['owner_members'])== 1
	c.channel_addowner(user2['token'], ch_1['channel_id'], user3['u_id'])
	#CHECK IF GLOBAL OWNER USER 2 HAS THE SAME POWER
	assert len(c.channel_details(user1['token'], ch_1['channel_id'])['owner_members'])== 2

def test_permission_change_not_owner_access():
	'''Change permission but not an owner'''
	clear()
	user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
	user2 = auth_register('testemail2@test.com', 'testing122', 'test2', 'program2')
	with pytest.raises(AccessError):
		admin_userpermission_change(user2['token'],user1['u_id'],1)

def test_permission_change_invalid_target():
	'''Targeted u_id is an invalid user'''
	clear()
	user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
	with pytest.raises(InputError):
	    admin_userpermission_change(user1['token'],3,1)

def test_permission_change_invalid_permission_id():
	'''Permission id is either 1 or 2 which is owner or member'''
	clear()
	user1 = auth_register('testemail1@test.com', 'testing123', 'test', 'program')
	user2 = auth_register('testemail2@test.com', 'testing122', 'test2', 'program2')
	with pytest.raises(InputError):
	    admin_userpermission_change(user1['token'], user2['token'], 3)

def test_permission_change_invalid_token():
	'''Change permission with invalid token'''
	clear()
	auth_register('testemail1@test.com', 'testing123', 'test', 'program')
	user2 = auth_register('testemail2@test.com', 'testing122', 'test2', 'program2')
	with pytest.raises(AccessError):
		admin_userpermission_change(12345,user2['u_id'],1)
