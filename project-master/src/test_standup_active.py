'''
    Test for standup_active
'''
import time
import pytest
import channel as c
import channels as ch
import auth
import error
from standup import standup_start, standup_send, standup_active
from error import InputError, AccessError
from other import clear
from user import user_profile
from datetime import datetime


def test_standup_active_simple():
    '''
    test standup_active with its normal behaviour
    '''
    clear()
    user1 = auth.auth_register("samsmith@gmail.com", "TooGoodToSayGoodbye", "Sam", "Smith")
    user2 = auth.auth_register("adele@gmail.com", "1sing_veryW3ll", "Adele", "Singer")
    ch_1 = ch.channels_create(user1['token'], "Soloist", True)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    length = 5
    finish = standup_start(user1['token'], ch_1['channel_id'], length)
    time.sleep(2)
    active = standup_active(user1['token'], ch_1['channel_id'])
    assert active == {'is_active': True, 'time_finish': finish}
    time.sleep(length)
    active = standup_active(user1['token'], ch_1['channel_id'])
    assert active == {'is_active': False, 'time_finish': None}

def test_standup_active_other_member_access():
    '''
    test standup_active for other member to access
    '''
    clear()
    user1 = auth.auth_register("samsmith@gmail.com", "TooGoodToSayGoodbye", "Sam", "Smith")
    user2 = auth.auth_register("adele@gmail.com", "1sing_veryW3ll", "Adele", "Singer")
    ch_1 = ch.channels_create(user1['token'], "Soloist", True)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    length = 5
    finish = standup_start(user1['token'], ch_1['channel_id'], length)
    time.sleep(2)
    #Token from user2
    active = standup_active(user2['token'], ch_1['channel_id'])
    assert active == {'is_active': True, 'time_finish': finish}
    time.sleep(length)
    #Token from user2
    active = standup_active(user2['token'], ch_1['channel_id'])
    assert active == {'is_active': False, 'time_finish': None}

def test_standup_active_multiple_channel():
    '''
    test standup_active for multiple channel with all active standup
    '''
    clear()
    user1 = auth.auth_register("samsmith@gmail.com", "TooGoodToSayGoodbye", "Sam", "Smith")
    user2 = auth.auth_register("adele@gmail.com", "1sing_veryW3ll", "Adele", "Singer")
    ch_1 = ch.channels_create(user1['token'], "Soloist", True)
    ch_2 = ch.channels_create(user2['token'], "Fix", False)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    length = 6
    finish1 = standup_start(user1['token'], ch_1['channel_id'], length)
    finish2 = standup_start(user2['token'], ch_2['channel_id'], length)
    time.sleep(3)
    active1 = standup_active(user1['token'], ch_1['channel_id'])
    active2 = standup_active(user2['token'], ch_2['channel_id'])
    assert active1 == {'is_active': True, 'time_finish': finish1}
    assert active2 == {'is_active': True, 'time_finish': finish2}
    time.sleep(length)
    active1 = standup_active(user1['token'], ch_1['channel_id'])
    active2 = standup_active(user2['token'], ch_2['channel_id'])
    assert active1 == {'is_active': False, 'time_finish': None}
    assert active2 == {'is_active': False, 'time_finish': None}

def test_standup_active_multiple_channel_different():
    '''
    test standup_active for multiple channel with different time for active
    '''
    clear()
    user1 = auth.auth_register("samsmith@gmail.com", "TooGoodToSayGoodbye", "Sam", "Smith")
    user2 = auth.auth_register("adele@gmail.com", "1sing_veryW3ll", "Adele", "Singer")
    ch_1 = ch.channels_create(user1['token'], "Soloist", True)
    ch_2 = ch.channels_create(user2['token'], "Fix", False)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    length1 = 6
    length2 = 3
    finish1 = standup_start(user1['token'], ch_1['channel_id'], length1)
    standup_start(user2['token'], ch_2['channel_id'], length2)
    time.sleep(4)
    active1 = standup_active(user1['token'], ch_1['channel_id'])
    active2 = standup_active(user2['token'], ch_2['channel_id'])
    assert active1 == {'is_active': True, 'time_finish': finish1}
    assert active2 == {'is_active': False, 'time_finish': None}
    time.sleep(length1)
    active1 = standup_active(user1['token'], ch_1['channel_id'])
    active2 = standup_active(user2['token'], ch_2['channel_id'])
    assert active1 == {'is_active': False, 'time_finish': None}
    assert active2 == {'is_active': False, 'time_finish': None}

def test_standup_active_multiple_channel_double_standup():
    '''
    test standup_active for multiple channel that start another standup
    after the previous standup finish
    '''
    clear()
    user1 = auth.auth_register("samsmith@gmail.com", "TooGoodToSayGoodbye", "Sam", "Smith")
    user2 = auth.auth_register("adele@gmail.com", "1sing_veryW3ll", "Adele", "Singer")
    ch_1 = ch.channels_create(user1['token'], "Soloist", True)
    ch_2 = ch.channels_create(user2['token'], "Fix", False)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    length1 = 6
    length2 = 3
    finish1 = standup_start(user1['token'], ch_1['channel_id'], length1)
    finish2 = standup_start(user2['token'], ch_2['channel_id'], length2)
    time.sleep(4)
    active1 = standup_active(user1['token'], ch_1['channel_id'])
    active2 = standup_active(user2['token'], ch_2['channel_id'])
    assert active1 == {'is_active': True, 'time_finish': finish1}
    assert active2 == {'is_active': False, 'time_finish': None}
    finish2 = standup_start(user2['token'], ch_2['channel_id'], length2)
    active2 = standup_active(user2['token'], ch_2['channel_id'])
    assert active2 == {'is_active': True, 'time_finish': finish2}
    time.sleep(10)
    active1 = standup_active(user1['token'], ch_1['channel_id'])
    active2 = standup_active(user2['token'], ch_2['channel_id'])
    assert active1 == {'is_active': False, 'time_finish': None}
    assert active2 == {'is_active': False, 'time_finish': None}

def test_standup_active_multiple_chan():
    '''
    test standup_active for multiple channel which one of them do not have
    any standup active
    '''
    clear()
    user1 = auth.auth_register("samsmith@gmail.com", "TooGoodToSayGoodbye", "Sam", "Smith")
    user2 = auth.auth_register("adele@gmail.com", "1sing_veryW3ll", "Adele", "Singer")
    ch_1 = ch.channels_create(user1['token'], "Soloist", True)
    ch_2 = ch.channels_create(user2['token'], "Fix", False)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    length1 = 6
    finish1 = standup_start(user1['token'], ch_1['channel_id'], length1)
    time.sleep(3)
    active1 = standup_active(user1['token'], ch_1['channel_id'])
    active2 = standup_active(user2['token'], ch_2['channel_id'])
    assert active1 == {'is_active': True, 'time_finish': finish1}
    assert active2 == {'is_active': False, 'time_finish': None}
    time.sleep(10)
    active1 = standup_active(user1['token'], ch_1['channel_id'])
    active2 = standup_active(user2['token'], ch_2['channel_id'])
    assert active1 == {'is_active': False, 'time_finish': None}
    assert active2 == {'is_active': False, 'time_finish': None}

def test_standup_active_channel_not_found():
    '''
    test standup_active for no channel found
    '''
    clear()
    user1 = auth.auth_register("samsmith@gmail.com", "TooGoodToSayGoodbye", "Sam", "Smith")
    user2 = auth.auth_register("adele@gmail.com", "1sing_veryW3ll", "Adele", "Singer")
    ch_1 = ch.channels_create(user1['token'], "Soloist", True)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    length1 = 6
    finish1 = standup_start(user1['token'], ch_1['channel_id'], length1)
    time.sleep(3)
    active1 = standup_active(user1['token'], ch_1['channel_id'])
    with pytest.raises(InputError):
        standup_active(user2['token'], 2)
    assert active1 == {'is_active': True, 'time_finish': finish1}
    time.sleep(10)
    active1 = standup_active(user1['token'], ch_1['channel_id'])
    assert active1 == {'is_active': False, 'time_finish': None}

def test_standup_active_invalid_token():
    '''
    test standup_active for invalid token
    '''
    clear()
    user1 = auth.auth_register("samsmith@gmail.com", "TooGoodToSayGoodbye", "Sam", "Smith")
    user2 = auth.auth_register("adele@gmail.com", "1sing_veryW3ll", "Adele", "Singer")
    ch_1 = ch.channels_create(user1['token'], "Soloist", True)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    length1 = 6
    finish1 = standup_start(user1['token'], ch_1['channel_id'], length1)
    time.sleep(3)
    active1 = standup_active(user1['token'], ch_1['channel_id'])
    with pytest.raises(AccessError):
        standup_active(1345, ch_1['channel_id'])
    assert active1 == {'is_active': True, 'time_finish': finish1}
    time.sleep(10)
    active1 = standup_active(user1['token'], ch_1['channel_id'])
    assert active1 == {'is_active': False, 'time_finish': None}

def test_standup_active_not_member():
    '''
    test standup_active if user not a member
    '''
    clear()
    user1 = auth.auth_register("samsmith@gmail.com", "TooGoodToSayGoodbye", "Sam", "Smith")
    user2 = auth.auth_register("adele@gmail.com", "1sing_veryW3ll", "Adele", "Singer")
    ch_1 = ch.channels_create(user1['token'], "Soloist", True)
    length1 = 6
    finish1 = standup_start(user1['token'], ch_1['channel_id'], length1)
    time.sleep(3)
    active1 = standup_active(user1['token'], ch_1['channel_id'])
    with pytest.raises(AccessError):
        standup_active(user2['token'], ch_1['channel_id'])
    assert active1 == {'is_active': True, 'time_finish': finish1}
    time.sleep(10)
    active1 = standup_active(user1['token'], ch_1['channel_id'])
    assert active1 == {'is_active': False, 'time_finish': None}