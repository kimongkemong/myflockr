'''
    Test for standup_start, standup_send
'''
import time
import pytest
import channel as c
import channels as ch
import auth
import error
from standup import standup_start, standup_send, standup_active
from other import clear
from user import user_profile
from datetime import datetime

################################# TEST STANDUP_START ########################################

def test_standup_start_simple():
    '''
    test standup_start with its normal behaviour
    '''
    clear()
    user1 = auth.auth_register("samsmith@gmail.com", "TooGoodToSayGoodbye", "Sam", "Smith")
    user2 = auth.auth_register("adele@gmail.com", "1sing_veryW3ll", "Adele", "Singer")
    ch_1 = ch.channels_create(user1['token'], "Soloist", True)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    length = 5
    finish = standup_start(user1['token'], ch_1['channel_id'], length)
    now = datetime.now()
    now_timestamp = int(now.replace().timestamp())
    time.sleep(2)
    active = standup_active(user1['token'], ch_1['channel_id'])
    assert active['is_active'] is True
    finish_at = now_timestamp + length
    assert finish_at == finish
    time.sleep(length)
    active = standup_active(user1['token'], ch_1['channel_id'])
    assert active['is_active'] is False

def test_standup_start_longer():
    '''
    test standup_start with its normal behaviour but with longer time
    '''
    clear()
    user1 = auth.auth_register("samsmith@gmail.com", "TooGoodToSayGoodbye", "Sam", "Smith")
    user2 = auth.auth_register("adele@gmail.com", "1sing_veryW3ll", "Adele", "Singer")
    ch_1 = ch.channels_create(user1['token'], "Soloist", True)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    length = 50
    finish = standup_start(user1['token'], ch_1['channel_id'], length)
    now = datetime.now()
    now_timestamp = int(now.replace().timestamp())
    time.sleep(10)
    active = standup_active(user1['token'], ch_1['channel_id'])
    assert active['is_active'] is True
    time.sleep(length)
    active = standup_active(user1['token'], ch_1['channel_id'])
    assert active['is_active'] is False
    finish_at = now_timestamp + length
    assert finish_at == finish

def test_standup_start_multi_ch():
    '''
    test standup_start to run standup concurrently on multiple channel
    '''
    clear()
    user1 = auth.auth_register("steveroger@gmail.com", "is_groot_animal?", "Steve", "Roger")
    user2 = auth.auth_register("rdj_cool@gmail.com", "jarvis_Annoying", "Tony", "Stark")
    user3 = auth.auth_register("antman@gmail.com", "shakira_saminamina", "Scott", "Lang")
    user4 = auth.auth_register("thewasp@gmail.com", "antman_annoying", "Hope", "Pym")
    user5 = auth.auth_register("spiderman_amazing@gmail.com", "zendaya_love", "Peter", "Parker")
    user6 = auth.auth_register("thor_isgod@gmail.com", "1234_iamgod", "Thor", "God")
    user7 = auth.auth_register("starlord@gmail.com", "gamora_comeback12", "Star", "Lord")
    ch_1 = ch.channels_create(user1['token'], "Avengers", True)
    ch_2 = ch.channels_create(user3['token'], "Tiny Hero", True)
    ch_3 = ch.channels_create(user6['token'], "Space Hero", True)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user4['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user3['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user7['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user5['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user6['u_id'])
    c.channel_invite(user3['token'], ch_2['channel_id'], user4['u_id'])
    c.channel_invite(user6['token'], ch_3['channel_id'], user5['u_id'])
    c.channel_invite(user6['token'], ch_3['channel_id'], user7['u_id'])
    length1 = 10
    length2 = 8
    length3 = 5
    finish1 = standup_start(user1['token'], ch_1['channel_id'], length1)
    finish2 = standup_start(user3['token'], ch_2['channel_id'], length2)
    finish3 = standup_start(user6['token'], ch_3['channel_id'], length3)
    now = datetime.now()
    now_timestamp = int(now.replace().timestamp())
    time.sleep(6)
    active1 = standup_active(user1['token'], ch_1['channel_id'])
    active2 = standup_active(user3['token'], ch_2['channel_id'])
    active3 = standup_active(user6['token'], ch_3['channel_id'])
    assert active1['is_active'] is True
    assert active2['is_active'] is True
    assert active3['is_active'] is False
    time.sleep(length1)
    active1 = standup_active(user1['token'], ch_1['channel_id'])
    active2 = standup_active(user3['token'], ch_2['channel_id'])
    active3 = standup_active(user6['token'], ch_3['channel_id'])
    assert active1['is_active'] is False
    assert active2['is_active'] is False
    assert active3['is_active'] is False
    finish1_at = now_timestamp + length1
    finish2_at = now_timestamp + length2
    finish3_at = now_timestamp + length3
    assert finish1_at == finish1
    assert finish2_at == finish2
    assert finish3_at == finish3

def test_standup_start_invalid_token():
    '''
    test standup_start with invalid token
    '''
    clear()
    user1 = auth.auth_register("kenclark@gmail.com", "Ihate_cryptonite", "Kent", "Clark")
    user2 = auth.auth_register("karasupergirl@gmail.com", "MissingMonel123", "Kara", "Zor-el")
    user3 = auth.auth_register("iambatman@gmail.com", "who_is_wonderWoman", "Bruce", "Wayne")
    ch_1 = ch.channels_create(user3['token'], "Just League", True)
    c.channel_invite(user3['token'], ch_1['channel_id'], user1['u_id'])
    c.channel_invite(user3['token'], ch_1['channel_id'], user2['u_id'])
    length = 10
    with pytest.raises(error.AccessError):
        standup_start(123456, ch_1['channel_id'], length)
    active = standup_active(user1['token'], ch_1['channel_id'])
    assert active['is_active'] is False

def test_standup_start_not_member():
    '''
    test standup_start with user is not a member of the channel
    '''
    clear()
    user1 = auth.auth_register("kenclark@gmail.com", "Ihate_cryptonite", "Kent", "Clark")
    user2 = auth.auth_register("karasupergirl@gmail.com", "MissingMonel123", "Kara", "Zor-el")
    user3 = auth.auth_register("iambatman@gmail.com", "who_is_wonderWoman", "Bruce", "Wayne")
    ch_1 = ch.channels_create(user3['token'], "Just League", True)
    c.channel_invite(user3['token'], ch_1['channel_id'], user1['u_id'])
    length = 10
    with pytest.raises(error.AccessError):
        standup_start(user2['token'], ch_1['channel_id'], length)
    active = standup_active(user1['token'], ch_1['channel_id'])
    assert active['is_active'] is False

def test_standup_start_invalid_ch():
    '''
    test standup_start with invalid channel_id
    '''
    clear()
    user1 = auth.auth_register("kenclark@gmail.com", "Ihate_cryptonite", "Kent", "Clark")
    user2 = auth.auth_register("karasupergirl@gmail.com", "MissingMonel123", "Kara", "Zor-el")
    user3 = auth.auth_register("iambatman@gmail.com", "who_is_wonderWoman", "Bruce", "Wayne")
    ch_1 = ch.channels_create(user3['token'], "Just League", True)
    c.channel_invite(user3['token'], ch_1['channel_id'], user1['u_id'])
    c.channel_invite(user3['token'], ch_1['channel_id'], user2['u_id'])
    length = 10
    with pytest.raises(error.InputError):
        standup_start(user1['token'], 1234, length)
    active = standup_active(user1['token'], ch_1['channel_id'])
    assert active['is_active'] is False

def test_standup_start_2active_standup():
    '''
    test standup_start by starting 2 standup in 1 channel
    '''
    clear()
    user1 = auth.auth_register("harrypotter@gmail.com", "Dobbyis_Afree_elf", "Harry", "Potter")
    user2 = auth.auth_register("hermione_granger12@gmail.com", "Wingardium_leviosa",
                               "Hermione", "Granger")
    user3 = auth.auth_register("ronweasley@gmail.com", "ginny_lil_sis", "Ron", "Weasley")
    ch_1 = ch.channels_create(user1['token'], "hogwards", False)
    c.channel_invite(user1['token'], ch_1['channel_id'], user3['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    length1 = 20
    length2 = 5
    standup_start(user1['token'], ch_1['channel_id'], length1)
    with pytest.raises(error.InputError):
        standup_start(user2['token'], ch_1['channel_id'], length2)
    time.sleep(10)
    active = standup_active(user1['token'], ch_1['channel_id'])
    assert active['is_active'] is True
    time.sleep(length1)
    active = standup_active(user1['token'], ch_1['channel_id'])
    assert active['is_active'] is False

def test_standup_start_lessthan1_second():
    '''
    test standup_start with less than 1 second period of standup
    '''
    clear()
    user1 = auth.auth_register("harrypotter@gmail.com", "Dobbyis_Afree_elf", "Harry", "Potter")
    user2 = auth.auth_register("hermione_granger12@gmail.com", "Wingardium_leviosa",
                               "Hermione", "Granger")
    user3 = auth.auth_register("ronweasley@gmail.com", "ginny_lil_sis", "Ron", "Weasley")
    ch_1 = ch.channels_create(user1['token'], "hogwards", False)
    c.channel_invite(user1['token'], ch_1['channel_id'], user3['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    length1 = 0
    with pytest.raises(error.InputError):
        standup_start(user1['token'], ch_1['channel_id'], length1)
    active = standup_active(user1['token'], ch_1['channel_id'])
    assert active['is_active'] is False
    length2 = -12
    with pytest.raises(error.InputError):
        standup_start(user2['token'], ch_1['channel_id'], length2)
    active = standup_active(user1['token'], ch_1['channel_id'])
    assert active['is_active'] is False

##################### TEST STANDUP_SEND ###################################################
def test_standup_send_double():
    '''
    test standup_send with its normal behaviour
    '''
    clear()
    user1 = auth.auth_register("samsmith@gmail.com", "TooGoodToSayGoodbye", "Sam", "Smith")
    user2 = auth.auth_register("adele@gmail.com", "1sing_veryW3ll", "Adele", "Singer")
    ch_1 = ch.channels_create(user1['token'], "Soloist", True)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    length = 10
    standup_start(user1['token'], ch_1['channel_id'], length)
    standup_send(user1['token'], ch_1['channel_id'], 'Hi everyone')
    standup_send(user2['token'], ch_1['channel_id'], 'aloha')
    time.sleep(length + 1)
    get_message = c.channel_messages(user2['token'], ch_1['channel_id'], 0)
    profile1 = user_profile(user1['token'], user1['u_id'])['user']['handle_str']
    profile2 = user_profile(user2['token'], user2['u_id'])['user']['handle_str']
    message = f"{profile1}: Hi everyone\n{profile2}: aloha\n"
    # print(f"halo {get_message}")
    assert get_message['messages'][0]['message'] == message
    assert get_message['messages'][0]['u_id'] == user1['u_id']
    length2 = 5
    standup_start(user2['token'], ch_1['channel_id'], length2)
    standup_send(user1['token'], ch_1['channel_id'], 'Hi second')
    time.sleep(length2 + 1)
    get_message = c.channel_messages(user1['token'], ch_1['channel_id'], 0)
    message = f"{profile1}: Hi second\n"
    assert get_message['messages'][0]['message'] == message
    assert get_message['messages'][0]['u_id'] == user2['u_id']

def test_standup_send_long():
    '''
    test standup_send with longer time & more messages
    '''
    clear()
    user1 = auth.auth_register("steveroger@gmail.com", "is_groot_animal?", "Steve", "Roger")
    user2 = auth.auth_register("rdj_cool@gmail.com", "jarvis_Annoying", "Tony", "Stark")
    user3 = auth.auth_register("antman@gmail.com", "shakira_saminamina", "Scott", "Lang")
    user4 = auth.auth_register("thewasp@gmail.com", "antman_annoying", "Hope", "Pym")
    ch_1 = ch.channels_create(user1['token'], "Soloist", True)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user3['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user4['u_id'])
    length = 30
    standup_start(user1['token'], ch_1['channel_id'], length)
    standup_send(user1['token'], ch_1['channel_id'], 'Summer after high school')
    standup_send(user2['token'], ch_1['channel_id'], 'when we first met')
    standup_send(user3['token'], ch_1['channel_id'], "Wed make-out in your Mustang to Radiohead")
    standup_send(user4['token'], ch_1['channel_id'], 'And on my 18th birthday')
    standup_send(user3['token'], ch_1['channel_id'], 'we got matching tattoos')
    standup_send(user2['token'], ch_1['channel_id'], 'Used to steal your parents liquor and climb to the roof')
    time.sleep(length + 1)
    get_message = c.channel_messages(user2['token'], ch_1['channel_id'], 0)
    profile1 = user_profile(user1['token'], user1['u_id'])['user']['handle_str']
    profile2 = user_profile(user1['token'], user2['u_id'])['user']['handle_str']
    profile3 = user_profile(user1['token'], user3['u_id'])['user']['handle_str']
    profile4 = user_profile(user1['token'], user4['u_id'])['user']['handle_str']
    message = f"{profile1}: Summer after high school\n{profile2}: when we first met\n\
{profile3}: Wed make-out in your Mustang to Radiohead\n\
{profile4}: And on my 18th birthday\n{profile3}: we got matching tattoos\n\
{profile2}: Used to steal your parents liquor and climb to the roof\n"
    assert get_message['messages'][0]['message'] == message
    assert get_message['messages'][0]['u_id'] == user1['u_id']

def test_standup_send_multiple_ch():
    '''
    test stand_up_send to run standup concurrently on multiple channel
    '''
    clear()
    user1 = auth.auth_register("steveroger@gmail.com", "is_groot_animal?", "Steve", "Roger")
    user2 = auth.auth_register("rdj_cool@gmail.com", "jarvis_Annoying", "Tony", "Stark")
    user3 = auth.auth_register("antman@gmail.com", "shakira_saminamina", "Scott", "Lang")
    user4 = auth.auth_register("thewasp@gmail.com", "antman_annoying", "Hope", "Pym")
    user5 = auth.auth_register("spiderman_amazing@gmail.com", "zendaya_love", "Peter", "Parker")
    user6 = auth.auth_register("thor_isgod@gmail.com", "1234_iamgod", "Thor", "God")
    user7 = auth.auth_register("starlord@gmail.com", "gamora_comeback12", "Star", "Lord")
    ch_1 = ch.channels_create(user1['token'], "Avengers", True)
    ch_2 = ch.channels_create(user3['token'], "Tiny Hero", True)
    ch_3 = ch.channels_create(user6['token'], "Space Hero", True)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user4['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user3['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user7['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user5['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user6['u_id'])
    c.channel_invite(user3['token'], ch_2['channel_id'], user4['u_id'])
    c.channel_invite(user6['token'], ch_3['channel_id'], user5['u_id'])
    c.channel_invite(user6['token'], ch_3['channel_id'], user7['u_id'])
    length1 = 10
    length2 = 8
    length3 = 5
    standup_start(user1['token'], ch_1['channel_id'], length1)
    standup_send(user2['token'], ch_1['channel_id'], 'Good morning')
    standup_send(user3['token'], ch_1['channel_id'], 'good afternoon')
    standup_send(user4['token'], ch_1['channel_id'], "Good night")
    standup_start(user3['token'], ch_2['channel_id'], length2)
    standup_send(user4['token'], ch_2['channel_id'], 'Happy birthday')
    standup_send(user3['token'], ch_2['channel_id'], 'thank you')
    standup_start(user5['token'], ch_3['channel_id'], length3)
    standup_send(user6['token'], ch_3['channel_id'], 'How r u today?')
    standup_send(user7['token'], ch_3['channel_id'], 'I am very great today')
    time.sleep(length1)
    get_message1 = c.channel_messages(user2['token'], ch_1['channel_id'], 0)
    get_message2 = c.channel_messages(user3['token'], ch_2['channel_id'], 0)
    get_message3 = c.channel_messages(user6['token'], ch_3['channel_id'], 0)
    profile2 = user_profile(user1['token'], user2['u_id'])['user']['handle_str']
    profile3 = user_profile(user1['token'], user3['u_id'])['user']['handle_str']
    profile4 = user_profile(user1['token'], user4['u_id'])['user']['handle_str']
    profile6 = user_profile(user6['token'], user6['u_id'])['user']['handle_str']
    profile7 = user_profile(user6['token'], user7['u_id'])['user']['handle_str']
    message1 = f"{profile2}: Good morning\n{profile3}: good afternoon\n{profile4}: Good night\n"
    message2 = f"{profile4}: Happy birthday\n{profile3}: thank you\n"
    message3 = f"{profile6}: How r u today?\n{profile7}: I am very great today\n"
    # print(f"halo{get_message1['messages']}")
    assert get_message1['messages'][0]['message'] == message1
    assert get_message1['messages'][0]['u_id'] == user1['u_id']
    assert get_message2['messages'][0]['message'] == message2
    assert get_message2['messages'][0]['u_id'] == user3['u_id']
    assert get_message3['messages'][0]['message'] == message3
    assert get_message3['messages'][0]['u_id'] == user5['u_id']

def test_standup_send_invalid_token():
    '''
    test standup_send with invalid token
    '''
    clear()
    user1 = auth.auth_register("kenclark@gmail.com", "Ihate_cryptonite", "Kent", "Clark")
    user2 = auth.auth_register("karasupergirl@gmail.com", "MissingMonel123", "Kara", "Zor-el")
    user3 = auth.auth_register("iambatman@gmail.com", "who_is_wonderWoman", "Bruce", "Wayne")
    ch_1 = ch.channels_create(user3['token'], "Just League", True)
    c.channel_invite(user3['token'], ch_1['channel_id'], user1['u_id'])
    c.channel_invite(user3['token'], ch_1['channel_id'], user2['u_id'])
    length = 5
    standup_start(user1['token'], ch_1['channel_id'], length)
    with pytest.raises(error.AccessError):
        standup_send(123456, ch_1['channel_id'], 'Hi everyone')
    time.sleep(3)
    active = standup_active(user1['token'], ch_1['channel_id'])
    assert active['is_active'] is True
    time.sleep(length)

def test_standup_send_invalid_ch():
    '''
    test standup_send with invalid channel id
    '''
    clear()
    user1 = auth.auth_register("kenclark@gmail.com", "Ihate_cryptonite", "Kent", "Clark")
    user2 = auth.auth_register("karasupergirl@gmail.com", "MissingMonel123", "Kara", "Zor-el")
    user3 = auth.auth_register("iambatman@gmail.com", "who_is_wonderWoman", "Bruce", "Wayne")
    ch_1 = ch.channels_create(user3['token'], "Just League", True)
    c.channel_invite(user3['token'], ch_1['channel_id'], user1['u_id'])
    c.channel_invite(user3['token'], ch_1['channel_id'], user2['u_id'])
    length = 5
    standup_start(user1['token'], ch_1['channel_id'], length)
    with pytest.raises(error.InputError):
        standup_send(user3['token'], 12345, 'Hi everyone')
    time.sleep(3)
    active = standup_active(user1['token'], ch_1['channel_id'])
    assert active['is_active'] is True
    time.sleep(length)

def test_standup_send_not_member():
    '''
    test standup_start with user is not a member of the channel
    '''
    clear()
    user1 = auth.auth_register("kenclark@gmail.com", "Ihate_cryptonite", "Kent", "Clark")
    user2 = auth.auth_register("karasupergirl@gmail.com", "MissingMonel123", "Kara", "Zor-el")
    user3 = auth.auth_register("iambatman@gmail.com", "who_is_wonderWoman", "Bruce", "Wayne")
    ch_1 = ch.channels_create(user3['token'], "Just League", True)
    c.channel_invite(user3['token'], ch_1['channel_id'], user1['u_id'])
    length = 5
    standup_start(user1['token'], ch_1['channel_id'], length)
    with pytest.raises(error.AccessError):
        standup_send(user2['token'], ch_1['channel_id'], "Hi everyone")
    active = standup_active(user1['token'], ch_1['channel_id'])
    assert active['is_active'] is True
    time.sleep(length)

def test_standup_send_msg_toolong():
    '''
    test standup_send with messages being too long (more than 1000 characters)
    '''
    clear()
    user1 = auth.auth_register("kenclark@gmail.com", "Ihate_cryptonite", "Kent", "Clark")
    auth.auth_register("karasupergirl@gmail.com", "MissingMonel123", "Kara", "Zor-el")
    user3 = auth.auth_register("iambatman@gmail.com", "who_is_wonderWoman", "Bruce", "Wayne")
    ch_1 = ch.channels_create(user3['token'], "Just League", True)
    c.channel_invite(user3['token'], ch_1['channel_id'], user1['u_id'])
    length = 5
    text = 1001 * "a"
    standup_start(user1['token'], ch_1['channel_id'], length)
    with pytest.raises(error.InputError):
        standup_send(user3['token'], ch_1['channel_id'], text)
    active = standup_active(user1['token'], ch_1['channel_id'])
    assert active['is_active'] is True
    time.sleep(length + 1)
    active = standup_active(user1['token'], ch_1['channel_id'])
    assert active['is_active'] is False

def test_standup_send_not_active():
    '''
    test standup_send with no active standup currently running
    '''
    clear()
    user1 = auth.auth_register("kenclark@gmail.com", "Ihate_cryptonite", "Kent", "Clark")
    auth.auth_register("karasupergirl@gmail.com", "MissingMonel123", "Kara", "Zor-el")
    user3 = auth.auth_register("iambatman@gmail.com", "who_is_wonderWoman", "Bruce", "Wayne")
    ch_1 = ch.channels_create(user3['token'], "Just League", True)
    c.channel_invite(user3['token'], ch_1['channel_id'], user1['u_id'])
    with pytest.raises(error.InputError):
        standup_send(user3['token'], ch_1['channel_id'], "Hi everybody")
    active = standup_active(user1['token'], ch_1['channel_id'])
    assert active['is_active'] is False
