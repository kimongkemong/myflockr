from channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner
from channels import channels_create
from data import *
from other import clear
from error import *
import pytest
from auth import auth_register

#We cannnot test channel_messages yet as we have not written the send_message function as a part of iteration 1

#Simple test
def test_channel_details_initial():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    assert channel_details(user1['token'], channel1['channel_id']) == {
        'name': 'FirstChannel',
        'owner_members': [
            {
                'u_id': user1['u_id'],
                'name_first': "Jane",
                'name_last': "Smith",
                'profile_img_url' : "",
            }
        ],
        'all_members': [
            {
                'u_id': user1['u_id'],
                'name_first': "Jane",
                'name_last': "Smith",
                'profile_img_url' : "",
            }
        ]
    }


#Channel Details with 2 members
def test_channel_details_2():
    clear()
    user2 = auth_register("user2email@gmail.com", "MyStrongPassword123", "Paul", "Jones")
    user3 = auth_register("user3email@gmail.com", "MyPassword123", "Albert", "Einstein")
    channel2 = channels_create(user2['token'], "SecondChannel", True)
    channel_invite(user2['token'], channel2['channel_id'], user3['u_id'])

    assert channel_details(user3['token'], channel2['channel_id']) == {
        'name': 'SecondChannel',
        'owner_members': [
            {
                'u_id': user2['u_id'],
                'name_first': "Paul",
                'name_last': "Jones",
                'profile_img_url' : "",
            }
        ],
        'all_members': [
            {
                'u_id': user2['u_id'],
                'name_first': "Paul",
                'name_last': "Jones",
                'profile_img_url' : "",
            },
            {
                'u_id': user3['u_id'],
                'name_first': "Albert",
                'name_last': "Einstein",
                'profile_img_url' : "",
            }
        ]
    }


#Channel details - Access error when trying to access the channel details of a channel one is not a member of
def test_channel_details_Access_Error():
    clear()
    user4 = auth_register("user4email@gmail.com", "ILoveDogs789", "Charles", "Darwin")
    user5 = auth_register("user5email@gmail.com", "ILoveComp1531", "Alan", "Turing")
    user6 = auth_register("user6email@gmail.com", "superSecurePassword", "Marie", "Curie")

    channel3 = channels_create(user4['token'], "ThirdChannel", False)

    channel_invite(user4['token'], channel3['channel_id'], user5['u_id'])
    
    with pytest.raises(AccessError):
        channel_details(user6['token'], channel3['channel_id'])


#Channel details - Input error when invalid channel id is passed in
def test_channel_details_Input_Error():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")

    with pytest.raises(InputError):
        channel_details(user1['token'], -1)


#Remove Owner - check in channel details that this works effectively
def test_channel_removeowner():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    user2 = auth_register("user2email@gmail.com", "MyStrongPassword123", "Paul", "Jones")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    channel_invite(user1['token'], channel1['channel_id'], user2['u_id'])
    channel_addowner(user1['token'], channel1['channel_id'], user2['u_id'])
    channel_removeowner(user2['token'], channel1['channel_id'], user1['u_id'])

    assert channel_details(user1['token'], channel1['channel_id']) == {
        'name': 'FirstChannel',
        'owner_members': [
            {
                'u_id': user2['u_id'],
                'name_first': "Paul",
                'name_last': "Jones",
                'profile_img_url' : "",
            }
        ],
        'all_members': [
            {
                'u_id': user1['u_id'],
                'name_first': "Jane",
                'name_last': "Smith",
                'profile_img_url' : "",
            },
            {
                'u_id': user2['u_id'],
                'name_first': "Paul",
                'name_last': "Jones",
                'profile_img_url' : "",
            }
        ]
    }


#Remove Owner - Access Error if person trying to remove an owner is not an owner themselves (Only owners can remove other owners)
def test_channel_removeowner_Access_Error():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    user2 = auth_register("user2email@gmail.com", "MyStrongPassword123", "Paul", "Jones")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    channel_invite(user1['token'], channel1['channel_id'], user2['u_id'])
    #Access Error

    with pytest.raises(AccessError):
        channel_removeowner(user2['token'], channel1['channel_id'], user1['u_id'])


#Remove Owner - Input Error if trying to remove a member that is not an owner
def test_channel_removeowner_Input_Error1():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    user2 = auth_register("user2email@gmail.com", "MyStrongPassword123", "Paul", "Jones")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    channel_invite(user1['token'], channel1['channel_id'], user2['u_id'])


    #Input Error
    with pytest.raises(InputError):
        channel_removeowner(user1['token'], channel1['channel_id'], user2['u_id'])



#Remove Owner - Input error if invalid channel ID is passed 
def test_channel_removeowner_Input_Error2():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    user2 = auth_register("user2email@gmail.com", "MyStrongPassword123", "Paul", "Jones")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    channel_invite(user1['token'], channel1['channel_id'], user2['u_id'])

    channel_addowner(user1['token'], channel1['channel_id'], user2['u_id'])

    with pytest.raises(InputError):
        channel_removeowner(user1['token'], -1, user2['u_id'])

