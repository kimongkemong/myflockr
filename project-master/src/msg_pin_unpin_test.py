from message import *
import auth as a
from other import clear
import channels as cs
import pytest
from error import *
from channel import *

#Tests for message_pin

#If msg_pin is given two invalid args, then it will raise AccessError
#(We always assume that it will examine token first)
def test_msg_pin_empty():
    clear()
    with pytest.raises(AccessError):
        message_pin(1, 1)


#If the msg_id is from a message which is already pinned, 
#Then msg_pin raise an InputError.
def test_msg_pin_AlreadyPinned():
    clear()
    data1 = a.auth_register('messi@barca.com', '123456', 'Lionel', 'Messi')
    data2 = a.auth_register('ronaldo@juventus.com', '654321', 'Cristiano', 'Ronaldo')
    a.auth_register('suarez@atmadrid.com', 'lovemessi123', 'Luis', 'Suarez')
    data4 = a.auth_register('havertz@chelsea.com', 'german098', 'Kai', 'Havertz')
    data5 = a.auth_register('bsilva@mancity.com', 'iamsilva456', 'Bernado', 'Silva')
   
    channel = cs.channels_create(data1['token'],'worldteam', False)
    channel_addowner(data1['token'],channel['channel_id'],data2['u_id'])
    channel_addowner(data1['token'],channel['channel_id'],data5['u_id'])
    channel_invite(data1['token'],channel['channel_id'],data4['u_id'])

    message1_id = message_send(data1['token'], channel['channel_id'], "Hello")['message_id']

    message_pin(data1['token'], message1_id)

    with pytest.raises(InputError):
        message_pin(data1['token'], message1_id)


#If the token is from a user who is not a member of the channel, 
#Then msg_pin raise an AccessError
def test_msg_pin_NotMember():
    clear()
    data1 = a.auth_register('messi@barca.com', '123456', 'Lionel', 'Messi')
    data2 = a.auth_register('ronaldo@juventus.com', '654321', 'Cristiano', 'Ronaldo')
    data3 = a.auth_register('suarez@atmadrid.com', 'lovemessi123', 'Luis', 'Suarez')
    data4 = a.auth_register('havertz@chelsea.com', 'german098', 'Kai', 'Havertz')
    data5 = a.auth_register('bsilva@mancity.com', 'iamsilva456', 'Bernado', 'Silva')
   
    channel = cs.channels_create(data1['token'],'worldteam', False)
    channel_addowner(data1['token'],channel['channel_id'],data2['u_id'])
    channel_addowner(data1['token'],channel['channel_id'],data5['u_id'])
    channel_invite(data1['token'],channel['channel_id'],data4['u_id'])

    message1_id = message_send(data1['token'], channel['channel_id'], "Hello")['message_id']

    with pytest.raises(AccessError):
        message_pin(data3['token'], message1_id)


#If both args are valid, then msg_pin works well
#We examine by calling msg_unpin and no error is raised.
def test_msg_pin_success():
    clear()
    data1 = a.auth_register('messi@barca.com', '123456', 'Lionel', 'Messi')
    data2 = a.auth_register('ronaldo@juventus.com', '654321', 'Cristiano', 'Ronaldo')
    a.auth_register('suarez@atmadrid.com', 'lovemessi123', 'Luis', 'Suarez')
    data4 = a.auth_register('havertz@chelsea.com', 'german098', 'Kai', 'Havertz')
    data5 = a.auth_register('bsilva@mancity.com', 'iamsilva456', 'Bernado', 'Silva')
   
    channel = cs.channels_create(data1['token'],'worldteam', False)
    channel_addowner(data1['token'],channel['channel_id'],data2['u_id'])
    channel_addowner(data1['token'],channel['channel_id'],data5['u_id'])
    channel_invite(data1['token'],channel['channel_id'],data4['u_id'])

    message1_id = message_send(data1['token'], channel['channel_id'], "Hello")['message_id']

    message_pin(data1['token'], message1_id)

    message_unpin(data1['token'], message1_id)


#Tests for message_unpin

#If msg_unpin is given two invalid args, then it will raise AccessError
#(We always assume that it will examine token first)
def test_msg_unpin_empty():
    clear()
    with pytest.raises(AccessError):
        message_unpin(1, 1)


#If the msg_id is from a message which is already pinned, 
#Then msg_unpin raise an InputError.
def test_msg_unpin_AlreadyUnpinned():
    clear()
    data1 = a.auth_register('messi@barca.com', '123456', 'Lionel', 'Messi')
    data2 = a.auth_register('ronaldo@juventus.com', '654321', 'Cristiano', 'Ronaldo')
    a.auth_register('suarez@atmadrid.com', 'lovemessi123', 'Luis', 'Suarez')
    data4 = a.auth_register('havertz@chelsea.com', 'german098', 'Kai', 'Havertz')
    data5 = a.auth_register('bsilva@mancity.com', 'iamsilva456', 'Bernado', 'Silva')
   
    channel = cs.channels_create(data1['token'],'worldteam', False)
    channel_addowner(data1['token'],channel['channel_id'],data2['u_id'])
    channel_addowner(data1['token'],channel['channel_id'],data5['u_id'])
    channel_invite(data1['token'],channel['channel_id'],data4['u_id'])

    message1_id = message_send(data1['token'], channel['channel_id'], "Hello")['message_id']

    with pytest.raises(InputError):
        message_unpin(data1['token'], message1_id)


#If the token is from a user who is not a member of the channel, 
#Then msg_unpin raise an AccessError
def test_msg_unpin_NotMember():
    clear()
    data1 = a.auth_register('messi@barca.com', '123456', 'Lionel', 'Messi')
    data2 = a.auth_register('ronaldo@juventus.com', '654321', 'Cristiano', 'Ronaldo')
    data3 = a.auth_register('suarez@atmadrid.com', 'lovemessi123', 'Luis', 'Suarez')
    data4 = a.auth_register('havertz@chelsea.com', 'german098', 'Kai', 'Havertz')
    data5 = a.auth_register('bsilva@mancity.com', 'iamsilva456', 'Bernado', 'Silva')
   
    channel = cs.channels_create(data1['token'],'worldteam', False)
    channel_addowner(data1['token'],channel['channel_id'],data2['u_id'])
    channel_addowner(data1['token'],channel['channel_id'],data5['u_id'])
    channel_invite(data1['token'],channel['channel_id'],data4['u_id'])

    message1_id = message_send(data1['token'], channel['channel_id'], "Hello")['message_id']

    with pytest.raises(AccessError):
        message_unpin(data3['token'], message1_id)


#If both args are valid, then msg_unpin works well
#We examine by calling msg_pin and no error is raised.
def test_msg_unpin_success():
    clear()
    data1 = a.auth_register('messi@barca.com', '123456', 'Lionel', 'Messi')
    data2 = a.auth_register('ronaldo@juventus.com', '654321', 'Cristiano', 'Ronaldo')
    a.auth_register('suarez@atmadrid.com', 'lovemessi123', 'Luis', 'Suarez')
    data4 = a.auth_register('havertz@chelsea.com', 'german098', 'Kai', 'Havertz')
    data5 = a.auth_register('bsilva@mancity.com', 'iamsilva456', 'Bernado', 'Silva')
   
    channel = cs.channels_create(data1['token'],'worldteam', False)
    channel_addowner(data1['token'],channel['channel_id'],data2['u_id'])
    channel_addowner(data1['token'],channel['channel_id'],data5['u_id'])
    channel_invite(data1['token'],channel['channel_id'],data4['u_id'])

    message1_id = message_send(data1['token'], channel['channel_id'], "Hello")['message_id']

    message_pin(data1['token'], message1_id)

    message_unpin(data1['token'], message1_id)

    message_pin(data1['token'], message1_id)




