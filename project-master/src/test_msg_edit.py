'''
    Test for message_edit
'''
import pytest
import channel as c
import channels as ch
import auth
import error
import message as msg
from other import clear

##############################################################################################
################################---TEST MESSAGE EDIT---#######################################

def test_message_edit_normal():
    '''
    test message_edit with its normal behaviour
    '''
    clear()
    user1 = auth.auth_register("samsmith@gmail.com", "TooGoodToSayGoodbye", "Sam", "Smith")
    user2 = auth.auth_register("adele@gmail.com", "1sing_veryW3ll", "Adele", "Singer")
    ch_1 = ch.channels_create(user1['token'], "Soloist", True)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    message1 = "Hello Adele"
    msg1 = msg.message_send(user1['token'], ch_1['channel_id'], message1)
    msg.message_edit(user1['token'], msg1['message_id'], "GoodMorning Adele")
    get_message = c.channel_messages(user1['token'], ch_1['channel_id'], 0)
    assert get_message['messages'][0]['message'] == "GoodMorning Adele"

def test_msg_edit_twice():
    '''
    test message_edit 2 times in 1 channel
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
    msg.message_send(user1['token'], ch_1['channel_id'], message1)
    msg2 = msg.message_send(user2['token'], ch_1['channel_id'], message2)
    msg3 = msg.message_send(user3['token'], ch_1['channel_id'], message3)
    msg.message_edit(user1['token'], msg2['message_id'], "Ron Weasley is the best")
    msg.message_edit(user1['token'], msg3['message_id'], "I'm hermione, Nice to meet u")
    get_message = c.channel_messages(user1['token'], ch_1['channel_id'], 0)
    assert get_message['messages'][1]['message'] == "Ron Weasley is the best"
    assert get_message['messages'][0]['message'] == "I'm hermione, Nice to meet u"

def test_msg_edit_multiple_ch():
    '''
    #test message_edit with multiple edit on multiple channel
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
    msg11 = msg.message_send(user3['token'], ch_1['channel_id'], "Good morning")
    msg.message_send(user1['token'], ch_1['channel_id'], "R you okay?")
    msg13 = msg.message_send(user2['token'], ch_1['channel_id'], "I'm fine thanks")
    msg21 = msg.message_send(user3['token'], ch_2['channel_id'], "U coming?")
    msg.message_send(user4['token'], ch_2['channel_id'], "Not sure")
    msg.message_send(user5['token'], ch_3['channel_id'], "Happy Birtday")
    msg.message_send(user6['token'], ch_3['channel_id'], "Thank you!")
    msg33 = msg.message_send(user6['token'], ch_3['channel_id'], "<3 <3")
    msg.message_edit(user1['token'], msg11['message_id'], "Good Evening!")
    msg.message_edit(user1['token'], msg13['message_id'], "I'm great thanks!")
    msg.message_edit(user3['token'], msg21['message_id'], "Bro, u coming?")
    msg.message_edit(user6['token'], msg33['message_id'], "love ya!")
    get_message1 = c.channel_messages(user1['token'], ch_1['channel_id'], 0)
    get_message2 = c.channel_messages(user3['token'], ch_2['channel_id'], 0)
    get_message3 = c.channel_messages(user6['token'], ch_3['channel_id'], 0)
    assert get_message1['messages'][2]['message'] == "Good Evening!"
    assert get_message1['messages'][0]['message'] == "I'm great thanks!"
    assert get_message2['messages'][1]['message'] == "Bro, u coming?"
    assert get_message3['messages'][0]['message'] == "love ya!"

def test_msg_edit_owner():
    '''
    #test message_edit which message edited by owner & sender
    '''
    clear()
    user1 = auth.auth_register("kenclark@gmail.com", "Ihate_cryptonite", "Kent", "Clark")
    user2 = auth.auth_register("karasupergirl@gmail.com", "MissingMonel123", "Kara", "Zor-el")
    user3 = auth.auth_register("iambatman@gmail.com", "who_is_wonderWoman", "Bruce", "Wayne")
    ch_1 = ch.channels_create(user3['token'], "Just League", True)
    c.channel_join(user1['token'], ch_1['channel_id'])
    c.channel_join(user2['token'], ch_1['channel_id'])
    message1 = "Have you heard this?"
    message2 = "Whose album is that?"
    msg1 = msg.message_send(user1['token'], ch_1['channel_id'], message1)
    msg2 = msg.message_send(user2['token'], ch_1['channel_id'], message2)
    msg.message_edit(user1['token'], msg1['message_id'], "This album is very nice")
    msg.message_edit(user3['token'], msg2['message_id'], "Is that ed sheeran's?")
    get_message = c.channel_messages(user1['token'], ch_1['channel_id'], 0)
    assert get_message['messages'][1]['message'] == "This album is very nice"
    assert get_message['messages'][0]['message'] == "Is that ed sheeran's?"


def test_msg_edit_unauth():
    '''
    #test message_edit with unauthorized user
    '''
    clear()
    user1 = auth.auth_register("harrypotter@gmail.com", "Dobbyis_Afree_elf", "Harry", "Potter")
    user2 = auth.auth_register("hermione_granger12@gmail.com", "Wingardium_leviosa",
                               "Hermione", "Granger")
    user3 = auth.auth_register("ronweasley@gmail.com", "ginny_lil_sis", "Ron", "Weasley")
    ch_1 = ch.channels_create(user1['token'], "hogwards", False)
    c.channel_invite(user1['token'], ch_1['channel_id'], user3['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    message1 = "How R u?"
    message2 = "Awesome..."
    msg1 = msg.message_send(user1['token'], ch_1['channel_id'], message1)
    msg.message_send(user2['token'], ch_1['channel_id'], message2)
    with pytest.raises(error.AccessError):
        msg.message_edit(user3['token'], msg1['message_id'], "How are you??")

def test_msg_edit_nomsg_id():
    '''
    #test message_edit with the wrong message id
    '''
    clear()
    user1 = auth.auth_register("harrypotter@gmail.com", "Dobbyis_Afree_elf", "Harry", "Potter")
    user2 = auth.auth_register("hermione_granger12@gmail.com", "Wingardium_leviosa",
                               "Hermione", "Granger")
    user3 = auth.auth_register("ronweasley@gmail.com", "ginny_lil_sis", "Ron", "Weasley")
    ch_1 = ch.channels_create(user1['token'], "hogwards", False)
    c.channel_invite(user1['token'], ch_1['channel_id'], user3['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    message1 = "How R u?"
    msg.message_send(user1['token'], ch_1['channel_id'], message1)
    with pytest.raises(error.InputError):
        msg.message_edit(user1['token'], 15, "Sunday morning")

def test_msg_edit_empty():
    '''
    #test message_edit with the wrong message id
    '''
    clear()
    user1 = auth.auth_register("harrypotter@gmail.com", "Dobbyis_Afree_elf", "Harry", "Potter")
    user2 = auth.auth_register("hermione_granger12@gmail.com", "Wingardium_leviosa",
                               "Hermione", "Granger")
    user3 = auth.auth_register("ronweasley@gmail.com", "ginny_lil_sis", "Ron", "Weasley")
    ch_1 = ch.channels_create(user1['token'], "hogwards", False)
    c.channel_invite(user1['token'], ch_1['channel_id'], user3['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    message1 = "How R u?"
    msg1 = msg.message_send(user1['token'], ch_1['channel_id'], message1)
    msg.message_edit(user1['token'], msg1['message_id'], "")
    get_message = c.channel_messages(user1['token'], ch_1['channel_id'], 0)
    assert get_message['end'] == -1

def test_msg_edit_invalid_token():
    '''
    #test message_edit with invalid token
    '''
    clear()
    user1 = auth.auth_register("harrypotter@gmail.com", "Dobbyis_Afree_elf", "Harry", "Potter")
    user2 = auth.auth_register("hermione_granger12@gmail.com", "Wingardium_leviosa",
                               "Hermione", "Granger")
    ch_1 = ch.channels_create(user1['token'], "hogwards", False)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    message1 = "How R u?"
    msg.message_send(user1['token'], ch_1['channel_id'], message1)
    with pytest.raises(error.AccessError):
        msg.message_edit(123123, 15, "Sunday morning")
