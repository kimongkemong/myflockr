from channel import *
import auth as a
from other import clear
import channels as cs
import pytest
from error import *




 #tests for channel_details


#Given two wrong input (wrong token and wrong channel_id), then channel_details will
#raise AccessError. (Since we assume it will always examine token first)
def test_details_empty():
    clear()
    with pytest.raises(AccessError):
        channel_details(1, 1)


#In this test, channel_details takes a token which belongs to a user who is not a channel member.
#Thus, channel_details will raise AccessError
def test_details_NotMember():
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
    
    with pytest.raises(AccessError):
        channel_details(data3['token'], channel['channel_id'])


#In this test, channel_details takes a negative channel_id(which is invalid).
#Thus, channel_details will raise InputError
def test_details_InvalidChannelId():
    clear()
    data = a.auth_register('example_one@abc.com', '123456', 'Lionel', 'Messi')
    channel = cs.channels_create(data['token'],'Barca', False)
    with pytest.raises(InputError):
        channel_details(data['token'], -channel['channel_id'])


#In this test, channel_details takes a token which belongs to a user who is a channel member 
#but not an owner.
#Thus, channel_details will still return details of the channel.
def test_details_NotOwner():
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
    
    assert channel_details(data4['token'], channel['channel_id']) == {'name': 'worldteam', 
                                                                      'owner_members': [
                                                                            {'u_id': 1, 
                                                                             'name_first': 'Lionel', 
                                                                             'name_last': 'Messi',
                                                                             'profile_img_url' : "",}, 
                                                                            {'u_id': 2, 
                                                                             'name_first': 'Cristiano', 
                                                                             'name_last': 'Ronaldo',
                                                                             'profile_img_url' : "",}, 
                                                                            {'u_id': 5, 
                                                                             'name_first': 'Bernado', 
                                                                             'name_last': 'Silva',
                                                                             'profile_img_url' : "",}], 
                                                                      'all_members': [
                                                                            {'u_id': 1, 
                                                                             'name_first': 'Lionel', 
                                                                             'name_last': 'Messi',
                                                                             'profile_img_url' : "",}, 
                                                                            {'u_id': 2, 
                                                                             'name_first': 'Cristiano', 
                                                                             'name_last': 'Ronaldo',
                                                                             'profile_img_url' : "",}, 
                                                                            {'u_id': 5, 
                                                                             'name_first': 'Bernado', 
                                                                             'name_last': 'Silva',
                                                                             'profile_img_url' : "",},
                                                                            {'u_id': 4, 
                                                                             'name_first': 'Kai', 
                                                                             'name_last': 'Havertz',
                                                                             'profile_img_url' : "",}]}


#In this test, channel_details takes two valid arguments. So it will return correct outputs
def test_details_OneChannel():
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
    
    assert channel_details(data1['token'], channel['channel_id']) == {'name': 'worldteam', 
                                                                      'owner_members': [
                                                                           {'u_id': 1, 
                                                                            'name_first': 'Lionel', 
                                                                            'name_last': 'Messi',
                                                                            'profile_img_url' : "",}, 
                                                                           {'u_id': 2, 
                                                                            'name_first': 'Cristiano', 
                                                                            'name_last': 'Ronaldo',
                                                                            'profile_img_url' : "",}, 
                                                                           {'u_id': 5, 
                                                                            'name_first': 'Bernado', 
                                                                            'name_last': 'Silva',
                                                                            'profile_img_url' : "",}], 
                                                                      'all_members': [
                                                                           {'u_id': 1, 
                                                                            'name_first': 'Lionel', 
                                                                            'name_last': 'Messi',
                                                                            'profile_img_url' : "",}, 
                                                                           {'u_id': 2, 
                                                                            'name_first': 'Cristiano', 
                                                                            'name_last': 'Ronaldo',
                                                                            'profile_img_url' : "",}, 
                                                                           {'u_id': 5, 
                                                                            'name_first': 'Bernado', 
                                                                            'name_last': 'Silva',
                                                                            'profile_img_url' : "",},
                                                                           {'u_id': 4, 
                                                                            'name_first': 'Kai', 
                                                                            'name_last': 'Havertz',
                                                                            'profile_img_url' : "",}]}

#In this case, we create more channels, and see that if channel_details takes in two valid args,
#it still works well.
def test_details_MoreChannels():
    clear()
    data1 = a.auth_register('messi@barca.com', '123456', 'Lionel', 'Messi')
    data2 = a.auth_register('ronaldo@juventus.com', '654321', 'Cristiano', 'Ronaldo')
    data3 = a.auth_register('suarez@atmadrid.com', 'lovemessi123', 'Luis', 'Suarez')
    data4 = a.auth_register('havertz@chelsea.com', 'german098', 'Kai', 'Havertz')
    data5 = a.auth_register('bsilva@mancity.com', 'iamsilva456', 'Bernado', 'Silva')


    channel1 = cs.channels_create(data1['token'],'worldteam', False)
    channel_addowner(data1['token'],channel1['channel_id'],data2['u_id'])
    channel_addowner(data1['token'],channel1['channel_id'],data5['u_id'])
    channel_invite(data1['token'],channel1['channel_id'],data3['u_id'])
    channel_invite(data1['token'],channel1['channel_id'],data4['u_id'])

    channel2 = cs.channels_create(data2['token'],'Portugual', False)
    channel_invite(data2['token'],channel2['channel_id'],data5['u_id'])

    channel3 = cs.channels_create(data1['token'],'gonetoSpain', False)
    channel_invite(data1['token'],channel3['channel_id'],data2['u_id'])
    channel_invite(data1['token'],channel3['channel_id'],data3['u_id'])

    channel4 = cs.channels_create(data4['token'],'forFans', True)
    channel_invite(data4['token'],channel4['channel_id'],data1['u_id'])
    channel_invite(data4['token'],channel4['channel_id'],data2['u_id'])
    channel_invite(data4['token'],channel4['channel_id'],data3['u_id'])
    channel_invite(data4['token'],channel4['channel_id'],data5['u_id'])

    assert channel_details(data1['token'], channel3['channel_id']) == {'name': 'gonetoSpain', 
                                                                       'owner_members': [
                                                                           {'u_id': 1, 
                                                                            'name_first': 'Lionel', 
                                                                            'name_last': 'Messi',
                                                                            'profile_img_url' : "",}], 
                                                                       'all_members': [
                                                                           {'u_id': 1, 
                                                                            'name_first': 'Lionel', 
                                                                            'name_last': 'Messi',
                                                                            'profile_img_url' : "",}, 
                                                                           {'u_id': 2, 
                                                                            'name_first': 'Cristiano', 
                                                                            'name_last': 'Ronaldo',
                                                                            'profile_img_url' : "",}, 
                                                                           {'u_id': 3, 
                                                                            'name_first': 'Luis', 
                                                                            'name_last': 'Suarez',
                                                                            'profile_img_url' : "",}]}


#tests for channel_addowner

#Given three wrong input (wrong token ,wrong channel_id and wrong user_id), 
#then channel_addowner will
#raise AccessError. (Since we assume it will always examine token first)
def test_add_empty():
    clear()
    with pytest.raises(AccessError):
        channel_addowner(1, 1, 1)


#In this test, channel_addowner takes in an invalid channel id.
#Thus, channel_addowner will raise InputError
def test_add_InvalidChannelId():
    clear()
    data = a.auth_register('example_one@abc.com', '123456', 'Lionel', 'Messi')
    channel = cs.channels_create(data['token'],'Barca', False)
    with pytest.raises(InputError):
        channel_addowner(data['token'], channel['channel_id'] + 1, data['u_id'])
    

#In this test, the token is from a user who is not the owner of the channel,
#Thus channel_addowner will raise an AccessError
def test_add_NotOwner():
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
   
    with pytest.raises(AccessError):
        channel_addowner(data4['token'], channel['channel_id'], data3['u_id'])
    

#In this test, channel_addowner takes a user_id which belongs to a user who is not a channel member.
#So the user will be added as an owner of the channel as well as a member.
def test_add_NotMember():
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

    assert len(channel_details(data1['token'], channel['channel_id'])['owner_members']) == 3
    assert len(channel_details(data1['token'], channel['channel_id'])['all_members']) == 4

    channel_addowner(data1['token'], channel['channel_id'], data3['u_id']) 

    assert len(channel_details(data1['token'], channel['channel_id'])['owner_members']) == 4
    assert len(channel_details(data1['token'], channel['channel_id'])['all_members']) == 5
    

#In this test, channel_addowner takes all valid args. Just test its validity when there are
#more than 2 channels.
def test_add_MoreChannels():
    clear()
    data1 = a.auth_register('messi@barca.com', '123456', 'Lionel', 'Messi')
    data2 = a.auth_register('ronaldo@juventus.com', '654321', 'Cristiano', 'Ronaldo')
    data3 = a.auth_register('suarez@atmadrid.com', 'lovemessi123', 'Luis', 'Suarez')
    data4 = a.auth_register('havertz@chelsea.com', 'german098', 'Kai', 'Havertz')
    data5 = a.auth_register('bsilva@mancity.com', 'iamsilva456', 'Bernado', 'Silva')


    channel1 = cs.channels_create(data1['token'],'worldteam', False)
    channel_addowner(data1['token'],channel1['channel_id'],data2['u_id'])
    channel_addowner(data1['token'],channel1['channel_id'],data5['u_id'])
    channel_invite(data1['token'],channel1['channel_id'],data3['u_id'])
    channel_invite(data1['token'],channel1['channel_id'],data4['u_id'])

    channel2 = cs.channels_create(data2['token'],'Portugual', False)
    channel_invite(data2['token'],channel2['channel_id'],data5['u_id'])

    channel3 = cs.channels_create(data1['token'],'gonetoSpain', False)
    channel_invite(data1['token'],channel3['channel_id'],data2['u_id'])
    channel_invite(data1['token'],channel3['channel_id'],data3['u_id'])

    channel4 = cs.channels_create(data4['token'],'forFans', True)
    channel_invite(data4['token'],channel4['channel_id'],data1['u_id'])
    channel_invite(data4['token'],channel4['channel_id'],data2['u_id'])
    channel_invite(data4['token'],channel4['channel_id'],data3['u_id'])
    channel_invite(data4['token'],channel4['channel_id'],data5['u_id'])

    assert len(channel_details(data1['token'], channel3['channel_id'])['owner_members']) == 1

    channel_addowner(data1['token'], channel3['channel_id'], data5['u_id'])

    assert len(channel_details(data1['token'], channel3['channel_id'])['owner_members']) == 2


#If channel_addowner takes user_id from a user who is already an owner of the channel,
#then channel_addowner will raise an InputError
def test_add_InOwners():
    clear()
    data1 = a.auth_register('messi@barca.com', '123456', 'Lionel', 'Messi')
    data2 = a.auth_register('ronaldo@juventus.com', '654321', 'Cristiano', 'Ronaldo')
    data3 = a.auth_register('suarez@atmadrid.com', 'lovemessi123', 'Luis', 'Suarez')
    data4 = a.auth_register('havertz@chelsea.com', 'german098', 'Kai', 'Havertz')
    data5 = a.auth_register('bsilva@mancity.com', 'iamsilva456', 'Bernado', 'Silva')


    channel1 = cs.channels_create(data1['token'],'worldteam', False)
    channel_addowner(data1['token'],channel1['channel_id'],data2['u_id'])
    channel_addowner(data1['token'],channel1['channel_id'],data5['u_id'])
    channel_invite(data1['token'],channel1['channel_id'],data3['u_id'])
    channel_invite(data1['token'],channel1['channel_id'],data4['u_id'])

    channel2 = cs.channels_create(data2['token'],'Portugual', False)
    channel_invite(data2['token'],channel2['channel_id'],data5['u_id'])

    channel3 = cs.channels_create(data1['token'],'gonetoSpain', False)
    channel_invite(data1['token'],channel3['channel_id'],data2['u_id'])
    channel_invite(data1['token'],channel3['channel_id'],data3['u_id'])

    channel4 = cs.channels_create(data4['token'],'forFans', True)
    channel_invite(data4['token'],channel4['channel_id'],data1['u_id'])
    channel_invite(data4['token'],channel4['channel_id'],data2['u_id'])
    channel_invite(data4['token'],channel4['channel_id'],data3['u_id'])
    channel_invite(data4['token'],channel4['channel_id'],data5['u_id'])

    with pytest.raises(InputError):
        channel_addowner(data2['token'], channel2['channel_id'], data2['u_id'])
    
    

#If channel_addowner takes user_id from a user who is already an member of the channel,
#then channel_addowner will only add the user to the owner list.
def test_add_InMembers():
    clear()
    data1 = a.auth_register('messi@barca.com', '123456', 'Lionel', 'Messi')
    data2 = a.auth_register('ronaldo@juventus.com', '654321', 'Cristiano', 'Ronaldo')
    data3 = a.auth_register('suarez@atmadrid.com', 'lovemessi123', 'Luis', 'Suarez')
    data4 = a.auth_register('havertz@chelsea.com', 'german098', 'Kai', 'Havertz')
    data5 = a.auth_register('bsilva@mancity.com', 'iamsilva456', 'Bernado', 'Silva')


    channel1 = cs.channels_create(data1['token'],'worldteam', False)
    channel_addowner(data1['token'],channel1['channel_id'],data2['u_id'])
    channel_addowner(data1['token'],channel1['channel_id'],data5['u_id'])
    channel_invite(data1['token'],channel1['channel_id'],data3['u_id'])
    channel_invite(data1['token'],channel1['channel_id'],data4['u_id'])

    channel2 = cs.channels_create(data2['token'],'Portugual', False)
    channel_invite(data2['token'],channel2['channel_id'],data5['u_id'])

    channel3 = cs.channels_create(data1['token'],'gonetoSpain', False)
    channel_invite(data1['token'],channel3['channel_id'],data2['u_id'])
    channel_invite(data1['token'],channel3['channel_id'],data3['u_id'])

    channel4 = cs.channels_create(data4['token'],'forFans', True)
    channel_invite(data4['token'],channel4['channel_id'],data1['u_id'])
    channel_invite(data4['token'],channel4['channel_id'],data2['u_id'])
    channel_invite(data4['token'],channel4['channel_id'],data3['u_id'])
    channel_invite(data4['token'],channel4['channel_id'],data5['u_id'])

    assert len(channel_details(data4['token'], channel4['channel_id'])['owner_members']) == 1

    channel_addowner(data4['token'], channel4['channel_id'], data3['u_id'])

    assert len(channel_details(data4['token'], channel4['channel_id'])['owner_members']) == 2


#tests for channel_removeowner

#Given three wrong input (wrong token ,wrong channel_id and wrong user_id), 
#then channel_removeowner will
#raise AccessError. (Since we assume it will always examine token first)
def test_rem_empty():
    clear()
    with pytest.raises(AccessError):
        channel_removeowner(1, 1, 1)


#In this test, channel_removeowner takes in an invalid channel id.
#Thus, channel_removeowner will raise InputError
def test_rem_InvalidChannelId():
    clear()
    data = a.auth_register('example_one@abc.com', '123456', 'Lionel', 'Messi')
    channel = cs.channels_create(data['token'],'Barca', False)
    with pytest.raises(InputError):
        channel_removeowner(data['token'], channel['channel_id'] + 1, data['u_id'])


#In this test, the token is from a user who is not the owner of the channel,
#Thus channel_removeowner will raise an AccessError
def test_rem_NotOwner():
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
    
    with pytest.raises(AccessError):
        channel_removeowner(data4['token'], channel['channel_id'], data1['u_id'])


#In this test, the user_id is from a user who is not a member of the channel
#Thus not an owner of the channel
#So channel_removeowner will raise an InputError
def test_rem_NotMember():
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

    with pytest.raises(InputError):
        channel_removeowner(data1['token'], channel['channel_id'], data3['u_id'])
    

#In this test we only check that channel_removeowner works well when there are more than 
#2 channels.
def test_rem_MoreChannels():
    clear()
    data1 = a.auth_register('messi@barca.com', '123456', 'Lionel', 'Messi')
    data2 = a.auth_register('ronaldo@juventus.com', '654321', 'Cristiano', 'Ronaldo')
    data3 = a.auth_register('suarez@atmadrid.com', 'lovemessi123', 'Luis', 'Suarez')
    data4 = a.auth_register('havertz@chelsea.com', 'german098', 'Kai', 'Havertz')
    data5 = a.auth_register('bsilva@mancity.com', 'iamsilva456', 'Bernado', 'Silva')


    channel1 = cs.channels_create(data1['token'],'worldteam', False)
    channel_addowner(data1['token'],channel1['channel_id'],data2['u_id'])
    channel_addowner(data1['token'],channel1['channel_id'],data5['u_id'])
    channel_invite(data1['token'],channel1['channel_id'],data3['u_id'])
    channel_invite(data1['token'],channel1['channel_id'],data4['u_id'])

    channel2 = cs.channels_create(data2['token'],'Portugual', False)
    channel_invite(data2['token'],channel2['channel_id'],data5['u_id'])

    channel3 = cs.channels_create(data1['token'],'gonetoSpain', False)
    channel_invite(data1['token'],channel3['channel_id'],data2['u_id'])
    channel_invite(data1['token'],channel3['channel_id'],data3['u_id'])

    channel4 = cs.channels_create(data4['token'],'forFans', True)
    channel_invite(data4['token'],channel4['channel_id'],data1['u_id'])
    channel_invite(data4['token'],channel4['channel_id'],data2['u_id'])
    channel_invite(data4['token'],channel4['channel_id'],data3['u_id'])
    channel_invite(data4['token'],channel4['channel_id'],data5['u_id'])

    assert len(channel_details(data2['token'], channel1['channel_id'])['owner_members']) == 3

    channel_removeowner(data2['token'], channel1['channel_id'], data1['u_id'])

    assert len(channel_details(data2['token'], channel1['channel_id'])['owner_members']) == 2


#In our assumption, we assume that the owner can't be removed if he is the only owner of the channel
#So in this case, channel_removeowner will raise an InputError.
def test_rem_OneOwner():
    clear()
    data1 = a.auth_register('messi@barca.com', '123456', 'Lionel', 'Messi')
    data2 = a.auth_register('ronaldo@juventus.com', '654321', 'Cristiano', 'Ronaldo')
    data3 = a.auth_register('suarez@atmadrid.com', 'lovemessi123', 'Luis', 'Suarez')
    data4 = a.auth_register('havertz@chelsea.com', 'german098', 'Kai', 'Havertz')
    data5 = a.auth_register('bsilva@mancity.com', 'iamsilva456', 'Bernado', 'Silva')


    channel1 = cs.channels_create(data1['token'],'worldteam', False)
    channel_addowner(data1['token'],channel1['channel_id'],data2['u_id'])
    channel_addowner(data1['token'],channel1['channel_id'],data5['u_id'])
    channel_invite(data1['token'],channel1['channel_id'],data3['u_id'])
    channel_invite(data1['token'],channel1['channel_id'],data4['u_id'])

    channel2 = cs.channels_create(data2['token'],'Portugual', False)
    channel_invite(data2['token'],channel2['channel_id'],data5['u_id'])

    channel3 = cs.channels_create(data1['token'],'gonetoSpain', False)
    channel_invite(data1['token'],channel3['channel_id'],data2['u_id'])
    channel_invite(data1['token'],channel3['channel_id'],data3['u_id'])

    channel4 = cs.channels_create(data4['token'],'forFans', True)
    channel_invite(data4['token'],channel4['channel_id'],data2['u_id'])
    channel_invite(data4['token'],channel4['channel_id'],data3['u_id'])
    channel_invite(data4['token'],channel4['channel_id'],data5['u_id'])

    with pytest.raises(InputError):
        channel_removeowner(data4['token'], channel4['channel_id'], data4['u_id'])


#If the user id is from a user who is only a member of the channel(not an owner)
#Then channel_removeowner will raise an InputError
def test_rem_InMembers():
    clear()
    data1 = a.auth_register('messi@barca.com', '123456', 'Lionel', 'Messi')
    data2 = a.auth_register('ronaldo@juventus.com', '654321', 'Cristiano', 'Ronaldo')
    data3 = a.auth_register('suarez@atmadrid.com', 'lovemessi123', 'Luis', 'Suarez')
    data4 = a.auth_register('havertz@chelsea.com', 'german098', 'Kai', 'Havertz')
    data5 = a.auth_register('bsilva@mancity.com', 'iamsilva456', 'Bernado', 'Silva')


    channel1 = cs.channels_create(data1['token'],'worldteam', False)
    channel_addowner(data1['token'],channel1['channel_id'],data2['u_id'])
    channel_addowner(data1['token'],channel1['channel_id'],data5['u_id'])
    channel_invite(data1['token'],channel1['channel_id'],data3['u_id'])
    channel_invite(data1['token'],channel1['channel_id'],data4['u_id'])

    channel2 = cs.channels_create(data2['token'],'Portugual', False)
    channel_invite(data2['token'],channel2['channel_id'],data5['u_id'])

    channel3 = cs.channels_create(data1['token'],'gonetoSpain', False)
    channel_invite(data1['token'],channel3['channel_id'],data2['u_id'])
    channel_invite(data1['token'],channel3['channel_id'],data3['u_id'])

    channel4 = cs.channels_create(data4['token'],'forFans', True)
    channel_invite(data4['token'],channel4['channel_id'],data1['u_id'])
    channel_invite(data4['token'],channel4['channel_id'],data2['u_id'])
    channel_invite(data4['token'],channel4['channel_id'],data3['u_id'])
    channel_invite(data4['token'],channel4['channel_id'],data5['u_id'])

    with pytest.raises(InputError):
        channel_removeowner(data4['token'], channel4['channel_id'], data2['u_id'])
    
    
