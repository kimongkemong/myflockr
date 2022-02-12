'''
    Test for search
'''
import pytest
import channel as c
import channels as ch
import auth
import error
import message as msg
from other import clear, search

##############################################################################################
################################---TEST MESSAGE EDIT---#######################################
def test_search_invalid_token():
    '''
    test message_edit with its normal behaviour
    '''
    clear()
    user1 = auth.auth_register("samsmith@gmail.com", "TooGoodToSayGoodbye", "Sam", "Smith")
    user2 = auth.auth_register("adele@gmail.com", "1sing_veryW3ll", "Adele", "Singer")
    ch_1 = ch.channels_create(user1['token'], "Soloist", True)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    message1 = "Hello Adele"
    message2 = "Hi, Sam Smith!!"
    msg.message_send(user1['token'], ch_1['channel_id'], message1)
    msg.message_send(user2['token'], ch_1['channel_id'], message2)
    with pytest.raises(error. AccessError):
        search(123456, "Hello") 

def test_search_simple():
    '''
    test message_edit with its normal behaviour
    '''
    clear()
    user1 = auth.auth_register("samsmith@gmail.com", "TooGoodToSayGoodbye", "Sam", "Smith")
    user2 = auth.auth_register("adele@gmail.com", "1sing_veryW3ll", "Adele", "Singer")
    ch_1 = ch.channels_create(user1['token'], "Soloist", True)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    message1 = "Hello Adele"
    message2 = "Hi, Sam Smith!!"
    msg.message_send(user1['token'], ch_1['channel_id'], message1)
    msg.message_send(user2['token'], ch_1['channel_id'], message2)
    get_message = c.channel_messages(user2['token'], ch_1['channel_id'], 0)
    assert search(user1['token'], "Hello") == {'messages': [
        {'message_id': get_message['messages'][1]['message_id'],
         'u_id': get_message['messages'][1]['u_id'],
         'message': get_message['messages'][1]['message'],
         'time_created': get_message['messages'][1]['time_created'],
         'reacts': get_message['messages'][1]['reacts'],
         'is_pinned': get_message['messages'][1]['is_pinned']
        }]}

def test_search_simple_multiple():
    '''
    test search with multiple message found in 1 channel
    '''
    clear()
    user1 = auth.auth_register("harrypotter@gmail.com", "Dobbyis_Afree_elf", "Harry", "Potter")
    user2 = auth.auth_register("hermione_granger12@gmail.com", "Wingardium_leviosa",
                               "Hermione", "Granger")
    user3 = auth.auth_register("ronweasley@gmail.com", "ginny_lil_sis", "Ron", "Weasley")
    ch_1 = ch.channels_create(user1['token'], "hogwards", False)
    c.channel_invite(user1['token'], ch_1['channel_id'], user3['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    message1 = "I'm Harry Potter"
    message2 = "Hello I'm Ron"
    message3 = "Great to see you guys"
    message31 = "My name's Hermione, I'm from England"
    msg.message_send(user1['token'], ch_1['channel_id'], message1)
    msg.message_send(user2['token'], ch_1['channel_id'], message2)
    msg.message_send(user3['token'], ch_1['channel_id'], message3)
    msg.message_send(user3['token'], ch_1['channel_id'], message31)
    get_message = c.channel_messages(user1['token'], ch_1['channel_id'], 0)
    assert search(user1['token'], "I'm") == {'messages': [
        {'message_id': get_message['messages'][0]['message_id'],
         'u_id': get_message['messages'][0]['u_id'],
         'message': get_message['messages'][0]['message'],
         'time_created': get_message['messages'][0]['time_created'],
         'reacts': get_message['messages'][0]['reacts'],
         'is_pinned': get_message['messages'][0]['is_pinned']
        },
        {'message_id': get_message['messages'][2]['message_id'],
         'u_id': get_message['messages'][2]['u_id'],
         'message': get_message['messages'][2]['message'],
         'time_created': get_message['messages'][2]['time_created'],
         'reacts': get_message['messages'][2]['reacts'],
         'is_pinned': get_message['messages'][2]['is_pinned']
        },
        {'message_id': get_message['messages'][3]['message_id'],
         'u_id': get_message['messages'][3]['u_id'],
         'message': get_message['messages'][3]['message'],
         'time_created': get_message['messages'][3]['time_created'],
         'reacts': get_message['messages'][3]['reacts'],
         'is_pinned': get_message['messages'][3]['is_pinned']
        }],}

def test_search_multiple_ch():
    '''
    #test search with multiple messages on multiple channels
    '''
    clear()
    user1 = auth.auth_register("steveroger@gmail.com", "is_groot_animal?", "Steve", "Roger")
    user2 = auth.auth_register("rdj_cool@gmail.com", "jarvis_Annoying", "Tony", "Stark")
    user3 = auth.auth_register("antman@gmail.com", "shakira_saminamina", "Scott", "Lang")
    user4 = auth.auth_register("thewasp@gmail.com", "antman_annoying", "Hope", "Pym")
    user5 = auth.auth_register("spiderman_amazing@gmail.com", "zendaya_love", "Peter", "Parker")
    user6 = auth.auth_register("thor_isgod@gmail.com", "1234_iamgod", "Thor", "God")
    user7 = auth.auth_register("starlord@gmail.com", "gamora_comeback12", "Star", "Lord")
    ch_1 = ch.channels_create(user1['token'], "Avengers", False)
    ch_2 = ch.channels_create(user3['token'], "Tiny Hero", True)
    ch_3 = ch.channels_create(user6['token'], "Space Hero", False)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user4['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user3['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user7['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user5['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user6['u_id'])
    c.channel_invite(user3['token'], ch_2['channel_id'], user4['u_id'])
    c.channel_invite(user6['token'], ch_3['channel_id'], user5['u_id'])
    c.channel_invite(user6['token'], ch_3['channel_id'], user7['u_id'])
    c.channel_invite(user6['token'], ch_3['channel_id'], user3['u_id'])
    msg.message_send(user3['token'], ch_1['channel_id'], "Good morning, everyone")
    msg.message_send(user1['token'], ch_1['channel_id'], "R you okay?")
    msg.message_send(user2['token'], ch_1['channel_id'], "I'm fine thanks everyone")
    msg.message_send(user4['token'], ch_1['channel_id'], "Hi everyone!")
    msg.message_send(user3['token'], ch_2['channel_id'], "everyone coming?")
    msg.message_send(user4['token'], ch_2['channel_id'], "Not sure")
    msg.message_send(user5['token'], ch_3['channel_id'], "Happy Birtday")
    msg.message_send(user6['token'], ch_3['channel_id'], "Thank you everyone")
    msg.message_send(user6['token'], ch_3['channel_id'], "<3 <3")
    get_message1 = c.channel_messages(user1['token'], ch_1['channel_id'], 0)
    get_message2 = c.channel_messages(user3['token'], ch_2['channel_id'], 0)
    get_message3 = c.channel_messages(user6['token'], ch_3['channel_id'], 0)
    assert search(user1['token'], "everyone") == {'messages': [
        {'message_id': get_message1['messages'][0]['message_id'],
         'u_id': get_message1['messages'][0]['u_id'],
         'message': get_message1['messages'][0]['message'],
         'time_created': get_message1['messages'][0]['time_created'],
         'reacts': get_message1['messages'][0]['reacts'],
         'is_pinned': get_message1['messages'][0]['is_pinned']
        },
        {'message_id': get_message1['messages'][1]['message_id'],
         'u_id': get_message1['messages'][1]['u_id'],
         'message': get_message1['messages'][1]['message'],
         'time_created': get_message1['messages'][1]['time_created'],
         'reacts': get_message1['messages'][1]['reacts'],
         'is_pinned': get_message1['messages'][1]['is_pinned']
        },
        {'message_id': get_message1['messages'][3]['message_id'],
         'u_id': get_message1['messages'][3]['u_id'],
         'message': get_message1['messages'][3]['message'],
         'time_created': get_message1['messages'][3]['time_created'],
         'reacts': get_message1['messages'][3]['reacts'],
         'is_pinned': get_message1['messages'][3]['is_pinned']
        }],}
    assert search(user3['token'], "everyone") == {'messages': [
        {'message_id': get_message1['messages'][0]['message_id'],
         'u_id': get_message1['messages'][0]['u_id'],
         'message': get_message1['messages'][0]['message'],
         'time_created': get_message1['messages'][0]['time_created'],
         'reacts': get_message1['messages'][0]['reacts'],
         'is_pinned': get_message1['messages'][0]['is_pinned']
        },
        {'message_id': get_message1['messages'][1]['message_id'],
         'u_id': get_message1['messages'][1]['u_id'],
         'message': get_message1['messages'][1]['message'],
         'time_created': get_message1['messages'][1]['time_created'],
         'reacts': get_message1['messages'][1]['reacts'],
         'is_pinned': get_message1['messages'][1]['is_pinned']
        },
        {'message_id': get_message1['messages'][3]['message_id'],
         'u_id': get_message1['messages'][3]['u_id'],
         'message': get_message1['messages'][3]['message'],
         'time_created': get_message1['messages'][3]['time_created'],
         'reacts': get_message1['messages'][3]['reacts'],
         'is_pinned': get_message1['messages'][3]['is_pinned']
        },
        {'message_id': get_message2['messages'][1]['message_id'],
         'u_id': get_message2['messages'][1]['u_id'],
         'message': get_message2['messages'][1]['message'],
         'time_created': get_message2['messages'][1]['time_created'],
         'reacts': get_message2['messages'][1]['reacts'],
         'is_pinned': get_message2['messages'][1]['is_pinned']
        },
        {'message_id': get_message3['messages'][1]['message_id'],
         'u_id': get_message3['messages'][1]['u_id'],
         'message': get_message3['messages'][1]['message'],
         'time_created': get_message3['messages'][1]['time_created'],
         'reacts': get_message3['messages'][1]['reacts'],
         'is_pinned': get_message3['messages'][1]['is_pinned']
        }],}

def test_search_not_found():
    '''
    #test search with no match of query_str
    '''
    clear()
    user1 = auth.auth_register("harrypotter@gmail.com", "Dobbyis_Afree_elf", "Harry", "Potter")
    user2 = auth.auth_register("hermione_granger12@gmail.com", "Wingardium_leviosa",
                               "Hermione", "Granger")
    ch_1 = ch.channels_create(user1['token'], "hogwards", False)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    message1 = "How R u?"
    message2 = "Awesome..."
    msg.message_send(user1['token'], ch_1['channel_id'], message1)
    msg.message_send(user2['token'], ch_1['channel_id'], message2)
    with pytest.raises(error.InputError):
        search(user1['token'], "Good Morning")

def test_search_not_member():
    '''
    #test search with user not a member of any channel
    '''
    clear()
    user1 = auth.auth_register("harrypotter@gmail.com", "Dobbyis_Afree_elf", "Harry", "Potter")
    user2 = auth.auth_register("hermione_granger12@gmail.com", "Wingardium_leviosa",
                               "Hermione", "Granger")
    user3 = auth.auth_register("ronweasley@gmail.com", "ginny_lil_sis", "Ron", "Weasley")
    ch_1 = ch.channels_create(user1['token'], "hogwards", False)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    message1 = "How R u?"
    message2 = "Awesome..."
    msg.message_send(user1['token'], ch_1['channel_id'], message1)
    msg.message_send(user2['token'], ch_1['channel_id'], message2)
    with pytest.raises(error.AccessError):
        search(user3['token'], "Good Morning")

def test_search_lower_upper():
    '''
    test search with various similar message
    '''
    clear()
    user1 = auth.auth_register("samsmith@gmail.com", "TooGoodToSayGoodbye", "Sam", "Smith")
    user2 = auth.auth_register("adele@gmail.com", "1sing_veryW3ll", "Adele", "Singer")
    ch_1 = ch.channels_create(user1['token'], "Soloist", True)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    message1 = "Hello Adele"
    message2 = "hello, Sam Smith!!"
    message21 = "heLLo..... everybody"
    msg.message_send(user1['token'], ch_1['channel_id'], message1)
    msg.message_send(user2['token'], ch_1['channel_id'], message2)
    msg.message_send(user2['token'], ch_1['channel_id'], message21)
    get_message = c.channel_messages(user2['token'], ch_1['channel_id'], 0)
    assert search(user1['token'], "heLLo") == {'messages': [
        {'message_id': get_message['messages'][0]['message_id'],
         'u_id': get_message['messages'][0]['u_id'],
         'message': get_message['messages'][0]['message'],
         'time_created': get_message['messages'][0]['time_created'],
         'reacts': get_message['messages'][0]['reacts'],
         'is_pinned': get_message['messages'][0]['is_pinned']
        }],}
