import pytest
from message import message_send, message_remove
from channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner
from auth import auth_register
from channels import channels_create
from error import *
from other import clear


'''
Simple test to check that a single message can be sent
'''
def test_message_send():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    message1id = message_send(user1['token'], channel1['channel_id'], "Hello")
    get_messages1 = channel_messages(user1['token'], channel1['channel_id'], 0)

    assert get_messages1['messages'][0]['message'] == "Hello"
    assert get_messages1['end'] == -1
    assert get_messages1['messages'][0]['u_id'] == user1['u_id']
    assert get_messages1['messages'][0]['message_id'] == message1id['message_id']

'''
This test checks that an access error is raised if an invalid token is passed into message_send
'''
def test_message_send_invalid_token():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    
    with pytest.raises(AccessError):
        message_send(-1, channel1['channel_id'], "Hello")
    
'''
This test checks that a few message can be sent and are correctly returned using the channel_messages functionality
'''
def test_message_send_few():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    message1id = message_send(user1['token'], channel1['channel_id'], "Hello")
    message2id = message_send(user1['token'], channel1['channel_id'], "Welcome to First Channel!!")
    message3id = message_send(user1['token'], channel1['channel_id'], "Please enjoy your stay!")
    get_messages1 = channel_messages(user1['token'], channel1['channel_id'], 0)

    assert get_messages1['messages'][0]['message'] == "Please enjoy your stay!"
    assert get_messages1['end'] == -1
    assert len(get_messages1['messages']) == 3
    assert get_messages1['messages'][2]['message'] == "Hello"
    assert get_messages1['messages'][0]['u_id'] == user1['u_id']
    assert get_messages1['messages'][1]['u_id'] == user1['u_id']
    assert get_messages1['messages'][2]['u_id'] == user1['u_id']
    assert get_messages1['messages'][0]['message_id'] == message3id['message_id']
    assert get_messages1['messages'][1]['message_id'] == message2id['message_id']
    assert get_messages1['messages'][2]['message_id'] == message1id['message_id']

'''
This test checks that the send message functionality works across multiple users
'''
def test_message_send_mult_users():
    clear()
    user1 = auth_register("user1email@gmail.com", "MyStrongPassword123", "Paul", "Jones")
    user2 = auth_register("user2email@gmail.com", "MyPassword123", "Albert", "Einstein")
    channel1 = channels_create(user1['token'], "2 person channel", True)
    channel_invite(user1['token'], channel1['channel_id'], user2['u_id'])

    message1id = message_send(user1['token'], channel1['channel_id'], "Hello")
    message2id = message_send(user1['token'], channel1['channel_id'], "Welcome to the Channel!!")
    message3id = message_send(user2['token'], channel1['channel_id'], "Thanks for adding me!")
    message4id = message_send(user1['token'], channel1['channel_id'], "No worries!")
    message5id = message_send(user2['token'], channel1['channel_id'], "I can't wait to send more messages")

    get_messages1 = channel_messages(user1['token'], channel1['channel_id'], 0)

    assert get_messages1['messages'][0]['message'] == "I can't wait to send more messages"
    assert get_messages1['end'] == -1
    assert len(get_messages1['messages']) == 5
    assert get_messages1['messages'][4]['message'] == "Hello"

    assert get_messages1['messages'][0]['u_id'] == user2['u_id']
    assert get_messages1['messages'][1]['u_id'] == user1['u_id']
    assert get_messages1['messages'][2]['u_id'] == user2['u_id']
    assert get_messages1['messages'][3]['u_id'] == user1['u_id']
    assert get_messages1['messages'][4]['u_id'] == user1['u_id']

    assert get_messages1['messages'][0]['message_id'] == message5id['message_id']
    assert get_messages1['messages'][1]['message_id'] == message4id['message_id']
    assert get_messages1['messages'][2]['message_id'] == message3id['message_id']
    assert get_messages1['messages'][3]['message_id'] == message2id['message_id']
    assert get_messages1['messages'][4]['message_id'] == message1id['message_id']

'''
Messages over the length of 1000 characters will raise an input error
'''
def test_message_too_long():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    long_message = "A" * 1001

    with pytest.raises(InputError):
        message_send(user1['token'], channel1['channel_id'], long_message)

'''
Access error raised if user is not a part of the channel which they are trying to send a message in
'''
def test_message_send_unauthorised():
    clear()
    user1 = auth_register("user1email@gmail.com", "MyStrongPassword123", "Paul", "Jones")
    user2 = auth_register("user2email@gmail.com", "MyPassword123", "Albert", "Einstein")
    channel1 = channels_create(user1['token'], "2 person channel", True)

    with pytest.raises(AccessError):
        message_send(user2['token'], channel1['channel_id'], "Hello")

'''
This test sends many messages to check that channel/messages only returns the 50 most recent messages.
'''
def test_message_send_many():
    clear()
    user1 = auth_register("user1email@gmail.com", "MyStrongPassword123", "Paul", "Jones")
    user2 = auth_register("user2email@gmail.com", "MyPassword123", "Albert", "Einstein")
    channel1 = channels_create(user1['token'], "2 person channel", True)
    channel_invite(user1['token'], channel1['channel_id'], user2['u_id'])

    message_ids = []
    i = 0

    m_id = {}
    while i < 55:
        if i % 2 == 0:
            m_id = message_send(user1['token'], channel1['channel_id'], "Hello from user 1")
            message_ids.insert(0, m_id)
        
        else:
            m_id = message_send(user2['token'], channel1['channel_id'], "Hello from user 2")
            message_ids.insert(0, m_id)
        
        i += 1

    get_messages1 = channel_messages(user1['token'], channel1['channel_id'], 0)



    assert get_messages1['messages'][0]['message'] == "Hello from user 1"
    assert get_messages1['end'] == 50
    assert len(get_messages1['messages']) == 50
    assert get_messages1['messages'][49]['message'] == "Hello from user 2"

    assert get_messages1['messages'][0]['u_id'] == user1['u_id']
    assert get_messages1['messages'][1]['u_id'] == user2['u_id']
    assert get_messages1['messages'][48]['u_id'] == user1['u_id']
    assert get_messages1['messages'][49]['u_id'] == user2['u_id']

    assert get_messages1['messages'][0]['message_id'] == message_ids[0]['message_id']
    assert get_messages1['messages'][1]['message_id'] == message_ids[1]['message_id']
    assert get_messages1['messages'][48]['message_id'] == message_ids[48]['message_id']
    assert get_messages1['messages'][49]['message_id'] == message_ids[49]['message_id']

'''
Similar to the previous test, this test sends many messages to check that channel/messages 
only returns the 50 most recent messages.
This test uses a start index that is not 0.
'''
def test_message_send_many_2():
    clear()
    user1 = auth_register("user1email@gmail.com", "MyStrongPassword123", "Paul", "Jones")
    user2 = auth_register("user2email@gmail.com", "MyPassword123", "Albert", "Einstein")
    channel1 = channels_create(user1['token'], "2 person channel", True)
    channel_invite(user1['token'], channel1['channel_id'], user2['u_id'])

    message_ids = []
    i = 0

    m_id = {}
    while i < 55:
        if i % 2 == 0:
            m_id = message_send(user1['token'], channel1['channel_id'], "Hello from user 1")
            message_ids.insert(0, m_id)
        
        else:
            m_id = message_send(user2['token'], channel1['channel_id'], "Hello from user 2")
            message_ids.insert(0, m_id)
        
        i += 1

    get_messages1 = channel_messages(user1['token'], channel1['channel_id'], 3)

    assert get_messages1['messages'][0]['message'] == "Hello from user 2"
    assert get_messages1['end'] == 53
    assert get_messages1['start'] == 3
    assert len(get_messages1['messages']) == 50
    assert get_messages1['messages'][49]['message'] == "Hello from user 1"

    assert get_messages1['messages'][0]['u_id'] == user2['u_id']
    assert get_messages1['messages'][1]['u_id'] == user1['u_id']
    assert get_messages1['messages'][48]['u_id'] == user2['u_id']
    assert get_messages1['messages'][49]['u_id'] == user1['u_id']

    assert get_messages1['messages'][0]['message_id'] == message_ids[3]['message_id']
    assert get_messages1['messages'][1]['message_id'] == message_ids[4]['message_id']
    assert get_messages1['messages'][48]['message_id'] == message_ids[51]['message_id']
    assert get_messages1['messages'][49]['message_id'] == message_ids[52]['message_id']

'''
Simple test to check that a message/remove works properly 
'''
def test_message_delete():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    message1id = message_send(user1['token'], channel1['channel_id'], "Hello")
    message2id = message_send(user1['token'], channel1['channel_id'], "Welcome to the Channel!!")

    message_remove(user1['token'], message1id['message_id'])
    get_messages1 = channel_messages(user1['token'], channel1['channel_id'], 0)

    assert get_messages1['messages'][0]['message'] == "Welcome to the Channel!!"
    assert get_messages1['end'] == -1
    assert len(get_messages1['messages']) == 1
    assert get_messages1['messages'][0]['u_id'] == user1['u_id']
    assert get_messages1['messages'][0]['message_id'] == message2id['message_id']
    
    #Input error raised if message has already been deleted
    with pytest.raises(InputError):
        message_remove(user1['token'], message1id['message_id'])

'''
Test to ensure that an owner of the channnel can remove a message that they did not send.
'''
def test_message_owner_remove():
    clear()

    user1 = auth_register("user1email@gmail.com", "MyStrongPassword123", "Paul", "Jones")
    user2 = auth_register("user2email@gmail.com", "MyPassword123", "Albert", "Einstein")
    channel1 = channels_create(user1['token'], "2 person channel", True)
    channel_invite(user1['token'], channel1['channel_id'], user2['u_id'])

    message1id = message_send(user1['token'], channel1['channel_id'], "Hello")
    message2id = message_send(user2['token'], channel1['channel_id'], "Cool!")
    message3id = message_send(user1['token'], channel1['channel_id'], "This is a channel")
    message4id = message_send(user2['token'], channel1['channel_id'], "Thanks!")


    message_remove(user1['token'], message2id['message_id'])

    get_messages1 = channel_messages(user1['token'], channel1['channel_id'], 0)

    assert get_messages1['messages'][0]['message'] == "Thanks!"
    assert get_messages1['messages'][1]['message'] == "This is a channel"
    assert get_messages1['messages'][2]['message'] == "Hello"
    assert get_messages1['end'] == -1
    assert len(get_messages1['messages']) == 3
    assert get_messages1['messages'][0]['u_id'] == user2['u_id']
    assert get_messages1['messages'][0]['message_id'] == message4id['message_id']
    assert get_messages1['messages'][1]['message_id'] == message3id['message_id']
    assert get_messages1['messages'][2]['message_id'] == message1id['message_id']

'''
Access error raised if a member in a channel (not an owner) tries to remove a message that they did not send
'''
def test_message_remove_unathorised():
    clear()

    user1 = auth_register("user1email@gmail.com", "MyStrongPassword123", "Paul", "Jones")
    user2 = auth_register("user2email@gmail.com", "MyPassword123", "Albert", "Einstein")
    channel1 = channels_create(user1['token'], "2 person channel", True)
    channel_invite(user1['token'], channel1['channel_id'], user2['u_id'])

    message1id = message_send(user1['token'], channel1['channel_id'], "Hello")
    message_send(user2['token'], channel1['channel_id'], "Cool!")
    message_send(user1['token'], channel1['channel_id'], "This is a channel")
    message_send(user2['token'], channel1['channel_id'], "Thanks!")

    with pytest.raises(AccessError):
        message_remove(user2['token'], message1id['message_id'])

'''
This test checks that many messages are removed effectively
'''
def test_message_remove_many():
    clear()

    user1 = auth_register("user1email@gmail.com", "MyStrongPassword123", "Paul", "Jones")
    user2 = auth_register("user2email@gmail.com", "MyPassword123", "Albert", "Einstein")
    channel1 = channels_create(user1['token'], "2 person channel", True)
    channel_invite(user1['token'], channel1['channel_id'], user2['u_id'])

    message_ids = []
    i = 0

    m_id = {}
    while i < 70:
        if i % 2 == 0:
            m_id = message_send(user1['token'], channel1['channel_id'], "Hello from user 1")
            message_ids.insert(0, m_id)
        
        else:
            m_id = message_send(user2['token'], channel1['channel_id'], "Hello from user 2")
            message_ids.insert(0, m_id)
        
        i += 1

    i = 0

    while i < 30:
        message_remove(user1['token'], message_ids[i]['message_id'])
        i+=1

    get_messages1 = channel_messages(user1['token'], channel1['channel_id'], 0)

    assert get_messages1['messages'][0]['message'] == "Hello from user 2"
    assert get_messages1['messages'][1]['message'] == "Hello from user 1"
    assert get_messages1['messages'][38]['message'] == "Hello from user 2"
    assert get_messages1['messages'][39]['message'] == "Hello from user 1"
    assert get_messages1['end'] == -1
    assert len(get_messages1['messages']) == 40
    assert get_messages1['messages'][0]['u_id'] == user2['u_id']
    assert get_messages1['messages'][0]['message_id'] == message_ids[30]['message_id']

'''
From many messages, this test checks that messages from the middle of the list are removed effectively.
'''
def test_message_remove_middle():
    clear()

    user1 = auth_register("user1email@gmail.com", "MyStrongPassword123", "Paul", "Jones")
    user2 = auth_register("user2email@gmail.com", "MyPassword123", "Albert", "Einstein")
    channel1 = channels_create(user1['token'], "2 person channel", True)
    channel_invite(user1['token'], channel1['channel_id'], user2['u_id'])

    message_ids = []
    i = 0

    m_id = {}
    while i < 70:
        if i == 25:
            m_id = message_send(user1['token'], channel1['channel_id'], "Hidden middle message!!")
            message_ids.insert(0, m_id)
        elif i % 2 == 0:
            m_id = message_send(user1['token'], channel1['channel_id'], "Hello from user 1")
            message_ids.insert(0, m_id)
        
        else:
            m_id = message_send(user2['token'], channel1['channel_id'], "Hello from user 2")
            message_ids.insert(0, m_id)
        
        i += 1

    message_remove(user1['token'], message_ids[25]['message_id'])

    get_messages1 = channel_messages(user1['token'], channel1['channel_id'], 1)

    assert get_messages1['messages'][0]['message'] == "Hello from user 1"
    assert get_messages1['messages'][1]['message'] == "Hello from user 2"
    assert get_messages1['messages'][23]['message'] == "Hello from user 2"
    assert get_messages1['messages'][24]['message'] == "Hello from user 2"
    assert get_messages1['messages'][25]['message'] == "Hello from user 1"
    assert get_messages1['messages'][48]['message'] == "Hello from user 2"
    assert get_messages1['messages'][49]['message'] == "Hello from user 1"
    assert get_messages1['end'] == 51
    assert len(get_messages1['messages']) == 50
    assert get_messages1['messages'][0]['u_id'] == user1['u_id']
    assert get_messages1['messages'][0]['message_id'] == message_ids[1]['message_id']
    assert get_messages1['messages'][23]['message_id'] == message_ids[24]['message_id']
    assert get_messages1['messages'][24]['message_id'] == message_ids[26]['message_id']
    assert get_messages1['messages'][25]['message_id'] == message_ids[27]['message_id']

'''
Input error raised if the message trying to be removed is not real
'''
def test_message_not_real():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    message_send(user1['token'], channel1['channel_id'], "Hello")
    message_send(user1['token'], channel1['channel_id'], "Welcome to the Channel!!")

    with pytest.raises(InputError):
        message_remove(user1['token'], -1)

'''
This test checks that an Access Error is raised if an invalid token is passed
'''
def test_message_remove_invalid_token():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    message1id = message_send(user1['token'], channel1['channel_id'], "Hello")

    with pytest.raises(AccessError):
        message_remove(-1, message1id['message_id'])

'''
Access error raised if the token of the user trying to get the messages is not in active tokens
'''
def test_get_messages_error1():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    message_send(user1['token'], channel1['channel_id'], "Hello")
    message_send(user1['token'], channel1['channel_id'], "Welcome to the Channel!!")

    with pytest.raises(AccessError):
        channel_messages(-1, channel1['channel_id'], 0)

'''
Input error raised if the channel does not exist
'''
def test_messages_error2():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    message_send(user1['token'], channel1['channel_id'], "Hello")
    message_send(user1['token'], channel1['channel_id'], "Welcome to the Channel!!")

    with pytest.raises(InputError):
        channel_messages(user1['token'], -1, 0)


'''
Access error raised if the user is not a member of the channel
'''
def test_messages_error3():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    user2 = auth_register("user2email@gmail.com", "MyPassword123", "Albert", "Einstein")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    message_send(user1['token'], channel1['channel_id'], "Hello")
    message_send(user1['token'], channel1['channel_id'], "Welcome to the Channel!!")

    with pytest.raises(AccessError):
        channel_messages(user2['token'], channel1['channel_id'], 0)

'''
Input error raised if start position is greater than number of messages in the channel
'''
def test_messages_error4():
    clear()
    user1 = auth_register("user1email@gmail.com", "HelloThere123", "Jane", "Smith")
    channel1 = channels_create(user1['token'], "FirstChannel", True)
    message_send(user1['token'], channel1['channel_id'], "Hello")
    message_send(user1['token'], channel1['channel_id'], "Welcome to the Channel!!")

    with pytest.raises(InputError):
        channel_messages(user1['token'], channel1['channel_id'], 5)

