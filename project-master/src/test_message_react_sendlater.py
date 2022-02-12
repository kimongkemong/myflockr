import pytest
from message import message_send, message_remove, message_react, message_unreact, message_sendlater
from channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner
from auth import auth_register
from channels import channels_create
from error import *
from other import clear
import datetime
import time
from datetime import timezone
 
'''
This is a simple test to check that the message react function works
'''
def test_react_simple():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    message1id = message_send(user1['token'], channel1['channel_id'], "Hello")

    message_react(user1['token'], message1id['message_id'], 1)
    get_messages1 = channel_messages(user1['token'], channel1['channel_id'], 0)

    assert get_messages1['messages'][0]['reacts'] == [{
        'react_id': 1,
        'u_ids': [user1['u_id']],
        'is_this_user_reacted': True
    }]

'''
This test checks that an input error is raised when an invalid react ID is passed (ie. anything other than 1)
'''
def test_react_invalid_react_id():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    message1id = message_send(user1['token'], channel1['channel_id'], "Hello")

    with pytest.raises(InputError):
        message_react(user1['token'], message1id['message_id'], -1)

'''
This test checks that an access error is raised when an invalid token is passed
'''
def test_react_invalid_token():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    message1id = message_send(user1['token'], channel1['channel_id'], "Hello")

    with pytest.raises(AccessError):
        message_react(-1, message1id['message_id'], 1)

'''
This test checks that an input error is raised when using an invalid message ID
'''
def test_react_invalid_message():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    message_send(user1['token'], channel1['channel_id'], "Hello")

    with pytest.raises(InputError):
        message_react(user1['token'], -1, 1)

'''
This test checks that an input error is raised if the authorised user is not a member of the channel
that contains the message they are trying to react to.
'''
def test_react_not_a_member():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    user2 = auth_register("user2email@gmail.com", "MyPassword123", "Albert", "Einstein")

    channel1 = channels_create(user1['token'], "FirstChannel", True)
    message1id = message_send(user1['token'], channel1['channel_id'], "Hello")

    with pytest.raises(InputError):
        message_react(user2['token'], message1id['message_id'], 1)

'''
This is a more complex test to check that message react works when called multiple times
'''
def test_react_few():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    user2 = auth_register("user2email@gmail.com", "MyPassword123", "Albert", "Einstein")

    channel1 = channels_create(user1['token'], "FirstChannel", True)
    channel_invite(user1['token'], channel1['channel_id'], user2['u_id'])

    message1id = message_send(user1['token'], channel1['channel_id'], "Hello")
    message2id = message_send(user1['token'], channel1['channel_id'], "Welcome to the Channel!!")
    message3id = message_send(user2['token'], channel1['channel_id'], "Thanks for adding me!")
    message4id = message_send(user1['token'], channel1['channel_id'], "No worries!")
    message_send(user2['token'], channel1['channel_id'], "I can't wait to send more messages")

    message_react(user1['token'], message1id['message_id'], 1)
    message_react(user2['token'], message1id['message_id'], 1)
    message_react(user2['token'], message2id['message_id'], 1)
    message_react(user2['token'], message3id['message_id'], 1)
    message_react(user1['token'], message4id['message_id'], 1)

    get_messages1 = channel_messages(user2['token'], channel1['channel_id'], 0)

    assert get_messages1['messages'][1]['reacts'] == [{
        'react_id': 1,
        'u_ids': [user1['u_id']],
        'is_this_user_reacted': False
    }]
    assert get_messages1['messages'][2]['reacts'] == [{
        'react_id': 1,
        'u_ids': [user2['u_id']],
        'is_this_user_reacted': True
    }]
    assert get_messages1['messages'][3]['reacts'] == [{
        'react_id': 1,
        'u_ids': [user2['u_id']],
        'is_this_user_reacted': True
    }]
    assert get_messages1['messages'][4]['reacts'] == [{
        'react_id': 1,
        'u_ids': [user1['u_id'], user2['u_id']],
        'is_this_user_reacted': True
    }]

'''
This is a test to check that nothing happens if a user calls message react twice in a row
'''
def test_react_double():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    message1id = message_send(user1['token'], channel1['channel_id'], "Hello")

    message_react(user1['token'], message1id['message_id'], 1)
    message_react(user1['token'], message1id['message_id'], 1)
    get_messages1 = channel_messages(user1['token'], channel1['channel_id'], 0)

    assert get_messages1['messages'][0]['reacts'] == [{
        'react_id': 1,
        'u_ids': [user1['u_id']],
        'is_this_user_reacted': True
    }]

'''
This is a simple test to check that a message can be unreacted to
'''
def test_unreact_simple():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    user2 = auth_register("user2email@gmail.com", "MyPassword123", "Albert", "Einstein")

    channel1 = channels_create(user1['token'], "FirstChannel", True)
    channel_invite(user1['token'], channel1['channel_id'], user2['u_id'])

    message1id = message_send(user1['token'], channel1['channel_id'], "Hello")

    message_react(user1['token'], message1id['message_id'], 1)
    message_react(user2['token'], message1id['message_id'], 1)
    message_unreact(user1['token'], message1id['message_id'], 1)
    get_messages1 = channel_messages(user1['token'], channel1['channel_id'], 0)

    assert get_messages1['messages'][0]['reacts'] == [{
        'react_id': 1,
        'u_ids': [user2['u_id']],
        'is_this_user_reacted': False
    }]

'''
This test checks that an access error is raised when an invalid token is passed
'''
def test_unreact_invalid_token():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    channel1 = channels_create(user1['token'], "FirstChannel", True)

    message1id = message_send(user1['token'], channel1['channel_id'], "Hello")
    message_react(user1['token'], message1id['message_id'], 1)

    with pytest.raises(AccessError):
        message_unreact(-1, message1id['message_id'], 1)

'''
This test checks that an input error is raised when an invalid react ID is passed (ie. anything other than 1)
'''
def test_unreact_invalid_react_id():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    channel1 = channels_create(user1['token'], "FirstChannel", True)

    message1id = message_send(user1['token'], channel1['channel_id'], "Hello")
    message_react(user1['token'], message1id['message_id'], 1)

    with pytest.raises(InputError):
        message_unreact(user1['token'], message1id['message_id'], -1)

'''
This test checks that an input error is raised when using an invalid message ID
'''
def test_unreact_invalid_message_id():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    channel1 = channels_create(user1['token'], "FirstChannel", True)

    message1id = message_send(user1['token'], channel1['channel_id'], "Hello")
    message_react(user1['token'], message1id['message_id'], 1)

    with pytest.raises(InputError):
        message_unreact(user1['token'], -1, 1)

'''
This test checks that an input error is raised if the authorised user is not a member of the channel
that contains the message they are trying to unreact to.
'''
def test_unreact_not_a_member():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    user2 = auth_register("user2email@gmail.com", "MyPassword123", "Albert", "Einstein")
    channel1 = channels_create(user1['token'], "FirstChannel", True)

    message1id = message_send(user1['token'], channel1['channel_id'], "Hello")
    message_react(user1['token'], message1id['message_id'], 1)

    with pytest.raises(InputError):
        message_unreact(user2['token'], message1id['message_id'], 1)

'''
This test checks that an input error is raised if there are no existing reacts with
the given react ID when message_unreact is called.
'''
def test_unreact_no_existing_reacts():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    channel1 = channels_create(user1['token'], "FirstChannel", True)

    message1id = message_send(user1['token'], channel1['channel_id'], "Hello")

    with pytest.raises(InputError):
        message_unreact(user1['token'], message1id['message_id'], 1)


'''
This checks that an input error is raised if a user tries to call unreact to a message they have
not reacted to in the first place.
'''
def test_unreact_havent_reacted():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    user2 = auth_register("user2email@gmail.com", "MyPassword123", "Albert", "Einstein")

    channel1 = channels_create(user1['token'], "FirstChannel", True)
    channel_invite(user1['token'], channel1['channel_id'], user2['u_id'])

    message1id = message_send(user1['token'], channel1['channel_id'], "Hello")
    message_react(user2['token'], message1id['message_id'], 1)

    with pytest.raises(InputError):
        message_unreact(user1['token'], message1id['message_id'], 1)

'''
A more complex test to check that the message unreact function works when called numerous times
'''
def test_unreact_few():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    user2 = auth_register("user2email@gmail.com", "MyPassword123", "Albert", "Einstein")

    channel1 = channels_create(user1['token'], "FirstChannel", True)
    channel_invite(user1['token'], channel1['channel_id'], user2['u_id'])

    message1id = message_send(user1['token'], channel1['channel_id'], "Hello")
    message2id = message_send(user1['token'], channel1['channel_id'], "Welcome to the Channel!!")
    message3id = message_send(user2['token'], channel1['channel_id'], "Thanks for adding me!")
    message4id = message_send(user1['token'], channel1['channel_id'], "No worries!")
    message_send(user2['token'], channel1['channel_id'], "I can't wait to send more messages")

    message_react(user1['token'], message1id['message_id'], 1)
    message_react(user2['token'], message1id['message_id'], 1)
    message_react(user1['token'], message2id['message_id'], 1)
    message_react(user2['token'], message2id['message_id'], 1)
    message_react(user1['token'], message3id['message_id'], 1)
    message_react(user2['token'], message3id['message_id'], 1)
    message_react(user1['token'], message4id['message_id'], 1)
    message_react(user2['token'], message4id['message_id'], 1)

    message_unreact(user2['token'], message1id['message_id'], 1)
    message_unreact(user1['token'], message2id['message_id'], 1)
    message_unreact(user1['token'], message3id['message_id'], 1)
    message_unreact(user2['token'], message4id['message_id'], 1)

    get_messages1 = channel_messages(user2['token'], channel1['channel_id'], 0)
    assert get_messages1['messages'][1]['reacts'] == [{
        'react_id': 1,
        'u_ids': [user1['u_id']],
        'is_this_user_reacted': False
    }]
    assert get_messages1['messages'][2]['reacts'] == [{
        'react_id': 1,
        'u_ids': [user2['u_id']],
        'is_this_user_reacted': True
    }]
    assert get_messages1['messages'][3]['reacts'] == [{
        'react_id': 1,
        'u_ids': [user2['u_id']],
        'is_this_user_reacted': True
    }]
    assert get_messages1['messages'][4]['reacts'] == [{
        'react_id': 1,
        'u_ids': [user1['u_id']],
        'is_this_user_reacted': False
    }]

'''
A simple test to check that the message sendlater functionality works
'''
def test_sendlater_simple():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    user2 = auth_register("user2email@gmail.com", "MyPassword123", "Albert", "Einstein")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    channel_invite(user1['token'], channel1['channel_id'], user2['u_id'])

    now = datetime.datetime.now(timezone.utc)
    send_at = now + datetime.timedelta(0,3)

    #Creating integer unix timestamp to pass in
    message_timestamp = int(send_at.replace(tzinfo=timezone.utc).timestamp())

    message_sendlater(user1['token'], channel1['channel_id'], "Hello", message_timestamp)
    message_send(user1['token'], channel1['channel_id'], "Welcome to the Channel!!")

    get_messages1 = channel_messages(user2['token'], channel1['channel_id'], 0)
    assert get_messages1['messages'][0]['message'] == "Welcome to the Channel!!"
    assert len(get_messages1['messages']) == 1

    time.sleep(5)
    get_messages2 = channel_messages(user2['token'], channel1['channel_id'], 0)
    assert get_messages2['messages'][0]['message'] == "Hello"
    assert len(get_messages2['messages']) == 2

'''
This test checks that an access error is raised when an invalid token is passed
'''
def test_sendlater_invalid_token():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    user2 = auth_register("user2email@gmail.com", "MyPassword123", "Albert", "Einstein")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    channel_invite(user1['token'], channel1['channel_id'], user2['u_id'])

    now = datetime.datetime.now(timezone.utc)
    send_at = now + datetime.timedelta(0,3)

    #Creating integer unix timestamp to pass in
    message_timestamp = int(send_at.replace(tzinfo=timezone.utc).timestamp())

    with pytest.raises(AccessError):
        message_sendlater(-1, channel1['channel_id'], "Hello", message_timestamp)

'''
This test checks that an input error is raised if message length is greater than 1000 chars.
'''
def test_sendlater_too_long():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    user2 = auth_register("user2email@gmail.com", "MyPassword123", "Albert", "Einstein")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    channel_invite(user1['token'], channel1['channel_id'], user2['u_id'])

    now = datetime.datetime.now(timezone.utc)
    send_at = now + datetime.timedelta(0,3)

    #Creating integer unix timestamp to pass in
    message_timestamp = int(send_at.replace(tzinfo=timezone.utc).timestamp())

    message = "A" * 1001

    with pytest.raises(InputError):
        message_sendlater(user1['token'], channel1['channel_id'], message, message_timestamp)

'''
This test checks that an access error is raised if the authorised user is not a member of the channel
they are trying to send a message later to.
'''
def test_sendlater_not_a_member():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    user2 = auth_register("user2email@gmail.com", "MyPassword123", "Albert", "Einstein")
    channel1 = channels_create(user1['token'], "FirstChannel", True)

    now = datetime.datetime.now(timezone.utc)
    send_at = now + datetime.timedelta(0,3)

    #Creating integer unix timestamp to pass in
    message_timestamp = int(send_at.replace(tzinfo=timezone.utc).timestamp())


    with pytest.raises(AccessError):
        message_sendlater(user2['token'], channel1['channel_id'], "Hello", message_timestamp)

'''
This test checks that an input error is raised when an invalid channel ID is passed
'''
def test_sendlater_invalid_channel_id():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    
    now = datetime.datetime.now(timezone.utc)
    send_at = now + datetime.timedelta(0,3)

    #Creating integer unix timestamp to pass in
    message_timestamp = int(send_at.replace(tzinfo=timezone.utc).timestamp())


    with pytest.raises(InputError):
        message_sendlater(user1['token'], -1, "Hello", message_timestamp)

'''
This test checks that an input error is raised if the scheduled time of the message is in the past
'''
def test_sendlater_time_in_past():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    channel1 = channels_create(user1['token'], "FirstChannel", True)

    now = datetime.datetime.now(timezone.utc)
    send_at = now + datetime.timedelta(0,-3)

    #Creating integer unix timestamp to pass in
    message_timestamp = int(send_at.replace(tzinfo=timezone.utc).timestamp())


    with pytest.raises(InputError):
        message_sendlater(user1['token'], channel1['channel_id'], "Hello", message_timestamp)

'''
A more complex test to check that message_sendlater works when called multiple times
'''
def test_sendlater_more():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    user2 = auth_register("user2email@gmail.com", "MyPassword123", "Albert", "Einstein")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    channel_invite(user1['token'], channel1['channel_id'], user2['u_id'])

    now = datetime.datetime.now(timezone.utc)
    send_at = now + datetime.timedelta(0,2)
    send_at2 = now + datetime.timedelta(0,5)
    send_at3 = now + datetime.timedelta(0,10)

    #Creating integer unix timestamp to pass in
    message_timestamp = int(send_at.replace(tzinfo=timezone.utc).timestamp())
    message_timestamp2 = int(send_at2.replace(tzinfo=timezone.utc).timestamp())
    message_timestamp3 = int(send_at3.replace(tzinfo=timezone.utc).timestamp())

    message1id = message_sendlater(user1['token'], channel1['channel_id'], "Hello", message_timestamp3)
    message2id = message_send(user1['token'], channel1['channel_id'], "Welcome to the Channel!!")
    message3id = message_sendlater(user1['token'], channel1['channel_id'], "Hi there", message_timestamp)
    message4id = message_sendlater(user2['token'], channel1['channel_id'], "Hope you see this later", message_timestamp2)

    get_messages1 = channel_messages(user2['token'], channel1['channel_id'], 0)
    assert get_messages1['messages'][0]['message'] == "Welcome to the Channel!!"
    assert len(get_messages1['messages']) == 1

    time.sleep(4)
    get_messages2 = channel_messages(user2['token'], channel1['channel_id'], 0)
    assert get_messages2['messages'][0]['message'] == "Hi there"
    assert len(get_messages2['messages']) == 2

    time.sleep(5)
    get_messages3 = channel_messages(user2['token'], channel1['channel_id'], 0)
    assert get_messages3['messages'][0]['message'] == "Hope you see this later"
    assert len(get_messages3['messages']) == 3

    time.sleep(5)
    get_messages4 = channel_messages(user2['token'], channel1['channel_id'], 0)
    assert len(get_messages4['messages']) == 4
    assert get_messages4['messages'][0]['message_id'] == message1id['message_id']
    assert get_messages4['messages'][1]['message_id'] == message4id['message_id']
    assert get_messages4['messages'][2]['message_id'] == message3id['message_id']
    assert get_messages4['messages'][3]['message_id'] == message2id['message_id']
    assert get_messages4['messages'][0]['message'] == "Hello"

'''
A more complex test to check that message_sendlater works when called multiple times
'''
def test_sendlater_more2():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    user2 = auth_register("user2email@gmail.com", "MyPassword123", "Albert", "Einstein")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    channel_invite(user1['token'], channel1['channel_id'], user2['u_id'])

    now = datetime.datetime.now(timezone.utc)
    send_at = now + datetime.timedelta(0,3)
    send_at2 = now + datetime.timedelta(0,7)

    #Creating integer unix timestamp to pass in
    message_timestamp = int(send_at.replace(tzinfo=timezone.utc).timestamp())
    message_timestamp2 = int(send_at2.replace(tzinfo=timezone.utc).timestamp())


    message1id = message_sendlater(user1['token'], channel1['channel_id'], "Hello", message_timestamp)
    message2id = message_send(user1['token'], channel1['channel_id'], "Welcome to the Channel!!")
    message3id = message_sendlater(user1['token'], channel1['channel_id'], "Hi there", message_timestamp2)

    get_messages1 = channel_messages(user2['token'], channel1['channel_id'], 0)
    assert get_messages1['messages'][0]['message'] == "Welcome to the Channel!!"
    assert len(get_messages1['messages']) == 1


    time.sleep(4)
    get_messages2 = channel_messages(user2['token'], channel1['channel_id'], 0)
    assert get_messages2['messages'][0]['message_id'] == message1id['message_id']
    assert get_messages2['messages'][1]['message_id'] == message2id['message_id']
    assert len(get_messages2['messages']) == 2
    assert get_messages2['messages'][0]['message'] == "Hello"
    assert get_messages2['messages'][1]['message'] == "Welcome to the Channel!!"
    
    

    time.sleep(5)
    get_messages3 = channel_messages(user2['token'], channel1['channel_id'], 0)
    assert len(get_messages3['messages']) == 3
    assert get_messages3['messages'][0]['message'] == "Hi there"
    assert get_messages3['messages'][0]['message_id'] == message3id['message_id']
    assert get_messages3['messages'][1]['message_id'] == message1id['message_id']
    assert get_messages3['messages'][2]['message_id'] == message2id['message_id']
