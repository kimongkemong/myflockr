'''
    Test for channel_invite, channel_leave, channel_join
'''
import pytest
import channel as c
import channels as ch
import auth
import error
from other import clear

##############################################################################################
#############---- TEST INVITE -----###########################################################
def test_invite_invalid_token():
    '''
    test channel_invite with invalid token
    '''
    clear()
    user1 = auth.auth_register("samsmith@gmail.com", "TooGoodToSayGoodbye", "Sam", "Smith")
    user2 = auth.auth_register("adele@gmail.com", "1sing_veryW3ll", "Adele", "Singer")
    ch_1 = ch.channels_create(user1['token'], "Soloist", True)
    with pytest.raises(error. AccessError):
        c.channel_invite(1234567, ch_1['channel_id'], user2['u_id']) 
    assert c.channel_details(user1['token'], ch_1['channel_id']) == {
        'name' :  'Soloist',
        'owner_members' : [{'u_id': user1['u_id'], 'name_first': 'Sam', 'name_last': 'Smith','profile_img_url' : "",}],
        'all_members' : [{'u_id': user1['u_id'], 'name_first': 'Sam', 'name_last': 'Smith','profile_img_url' : "",}]
    }

def test_invite_normal():
    '''
    hallo hallo test test 
    '''
    '''
    test channel_invite with simple normal behaviour
    '''
    clear()
    user1 = auth.auth_register("samsmith@gmail.com", "TooGoodToSayGoodbye", "Sam", "Smith")
    user2 = auth.auth_register("adele@gmail.com", "1sing_veryW3ll", "Adele", "Singer")
    ch_1 = ch.channels_create(user1['token'], "Soloist", True)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    assert c.channel_details(user1['token'], ch_1['channel_id']) == {
        'name' :  'Soloist',
        'owner_members' : [{'u_id': user1['u_id'], 'name_first': 'Sam', 'name_last': 'Smith','profile_img_url' : "",}],
        'all_members' : [{'u_id': user1['u_id'], 'name_first': 'Sam', 'name_last': 'Smith','profile_img_url' : "",},
                         {'u_id': user2['u_id'], 'name_first': 'Adele', 'name_last': 'Singer','profile_img_url' : "",}]
    }

def test_invite_twice():
    '''
    #test channel_invite 2 new members into 1 channel
    '''
    clear()
    user1 = auth.auth_register("harrypotter@gmail.com", "Dobbyis_Afree_elf", "Harry", "Potter")
    user2 = auth.auth_register("hermione_granger12@gmail.com", "Wingardium_leviosa",
                               "Hermione", "Granger")
    user3 = auth.auth_register("ronweasley@gmail.com", "ginny_lil_sis", "Ron", "Weasley")
    ch_1 = ch.channels_create(user1['token'], "hogwards", False)
    c.channel_invite(user1['token'], ch_1['channel_id'], user3['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    assert c.channel_details(user1['token'], ch_1['channel_id']) == {
        'name' : 'hogwards',
        'owner_members' : [{'u_id': user1['u_id'], 'name_first': 'Harry', 'name_last': 'Potter','profile_img_url' : "",}],
        'all_members' : [{'u_id': user1['u_id'], 'name_first': 'Harry', 'name_last': 'Potter','profile_img_url' : "",},
                         {'u_id': user3['u_id'], 'name_first': 'Ron', 'name_last': 'Weasley','profile_img_url' : "",},
                         {'u_id': user2['u_id'], 'name_first': 'Hermione', 'name_last': 'Granger','profile_img_url' : "",}]
    }

def test_invite_multiple_ch():
    '''
    #test channel_invite many new members into multiple different channels
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
    assert c.channel_details(user1['token'], ch_1['channel_id']) == {
        'name' : 'Avengers',
        'owner_members' : [{'u_id': user1['u_id'], 'name_first': 'Steve', 'name_last': 'Roger','profile_img_url' : "",}],
        'all_members' : [{'u_id': user1['u_id'], 'name_first': 'Steve', 'name_last': 'Roger','profile_img_url' : "",},
                         {'u_id': user2['u_id'], 'name_first': 'Tony', 'name_last': 'Stark','profile_img_url' : "",},
                         {'u_id': user4['u_id'], 'name_first': 'Hope', 'name_last': 'Pym','profile_img_url' : "",},
                         {'u_id': user3['u_id'], 'name_first': 'Scott', 'name_last': 'Lang','profile_img_url' : "",},
                         {'u_id': user7['u_id'], 'name_first': 'Star', 'name_last': 'Lord','profile_img_url' : "",},
                         {'u_id': user5['u_id'], 'name_first': 'Peter', 'name_last': 'Parker','profile_img_url' : "",},
                         {'u_id': user6['u_id'], 'name_first': 'Thor', 'name_last': 'God','profile_img_url' : "",}]
    }
    assert c.channel_details(user3['token'], ch_2['channel_id']) == {
        'name' : 'Tiny Hero',
        'owner_members' : [{'u_id': user3['u_id'], 'name_first': 'Scott', 'name_last': 'Lang','profile_img_url' : "",}],
        'all_members' : [{'u_id': user3['u_id'], 'name_first': 'Scott', 'name_last': 'Lang','profile_img_url' : "",},
                         {'u_id': user4['u_id'], 'name_first': 'Hope', 'name_last': 'Pym','profile_img_url' : "",}]
    }
    assert c.channel_details(user6['token'], ch_3['channel_id']) == {
        'name' : 'Space Hero',
        'owner_members' : [{'u_id': user6['u_id'], 'name_first': 'Thor', 'name_last': 'God','profile_img_url' : "",}],
        'all_members' : [{'u_id': user6['u_id'], 'name_first': 'Thor', 'name_last': 'God','profile_img_url' : "",},
                         {'u_id': user5['u_id'], 'name_first': 'Peter', 'name_last': 'Parker','profile_img_url' : "",},
                         {'u_id': user7['u_id'], 'name_first': 'Star', 'name_last': 'Lord','profile_img_url' : "",}]
    }

def test_invite_unauth_ch():
    '''
    test channel_invite with unauthorized channel_id
    '''
    clear()
    user1 = auth.auth_register("kenclark@gmail.com", "Ihate_cryptonite", "Kent", "Clark")
    user2 = auth.auth_register("karasupergirl@gmail.com", "MissingMonel123", "Kara", "Zor-el")
    user3 = auth.auth_register("iambatman@gmail.com", "who_is_wonderWoman", "Bruce", "Wayne")
    ch_1 = ch.channels_create(user3['token'], "Just League", True)
    with pytest.raises(error. InputError):
        c.channel_invite(user3['token'], 15, user1['u_id'])
    #assert c.channel_invite(3, 15, 1) == "Input Error! Invalid Channel or User"
    c.channel_invite(user3['token'], ch_1['channel_id'], user2['u_id'])
    assert c.channel_details(user3['token'], ch_1['channel_id']) == {
        'name' : 'Just League',
        'owner_members' : [{'u_id': user3['u_id'], 'name_first': 'Bruce', 'name_last': 'Wayne','profile_img_url' : "",}],
        'all_members' : [{'u_id': user3['u_id'], 'name_first': 'Bruce', 'name_last': 'Wayne','profile_img_url' : "",},
                         {'u_id': user2['u_id'], 'name_first': 'Kara', 'name_last': 'Zor-el','profile_img_url' : "",}]
    }

def test_invite_user_error():
    '''
    test channel_invite with invalid user_id
    '''
    clear()
    user3 = auth.auth_register("iambatman@gmail.com", "who_is_wonderWoman", "Bruce", "Wayne")
    ch_1 = ch.channels_create(user3['token'], "Just League", True)
    with pytest.raises(error.InputError):
        c.channel_invite(user3['token'], ch_1['channel_id'], 16)
    #assert c.channel_invite(3, 1, 16) == "Input Error! Invalid Channel or User"
    assert c.channel_details(user3['token'], ch_1['channel_id']) == {
        'name' : 'Just League',
        'owner_members' : [{'u_id': user3['u_id'], 'name_first': 'Bruce', 'name_last': 'Wayne','profile_img_url' : "",}],
        'all_members' : [{'u_id': user3['u_id'], 'name_first': 'Bruce', 'name_last': 'Wayne','profile_img_url' : "",}]
    }

def test_invite_already_a_member():
    '''
    test channel_invite to add new member that is already a member of the channel
    '''
    clear()
    user2 = auth.auth_register("karasupergirl@gmail.com", "MissingMonel123", "Kara", "Zor-el")
    user3 = auth.auth_register("iambatman@gmail.com", "who_is_wonderWoman", "Bruce", "Wayne")
    user4 = auth.auth_register("luthorevil@gmail.com", "LenaLuthoramazing", "Lena", "Luthor")
    ch_1 = ch.channels_create(user3['token'], "Just League", True)
    c.channel_invite(user3['token'], ch_1['channel_id'], user2['u_id'])
    c.channel_invite(user3['token'], ch_1['channel_id'], user4['u_id'])
    with pytest.raises(error.AccessError):
        c.channel_invite(user3['token'], ch_1['channel_id'], user2['u_id'])
    #assert c.channel_invite(3, 1, 2) == "Access Error! User is already a member"
    assert c.channel_details(user3['token'], ch_1['channel_id']) == {
        'name' : 'Just League',
        'owner_members' : [{'u_id': user3['u_id'], 'name_first': 'Bruce', 'name_last': 'Wayne','profile_img_url' : "",}],
        'all_members' : [{'u_id': user3['u_id'], 'name_first': 'Bruce', 'name_last': 'Wayne','profile_img_url' : "",},
                         {'u_id': user2['u_id'], 'name_first': 'Kara', 'name_last': 'Zor-el','profile_img_url' : "",},
                         {'u_id': user4['u_id'], 'name_first': 'Lena', 'name_last': 'Luthor','profile_img_url' : "",}]
    }

################################################################################################
###################------------------ TEST LEAVE ------------------#############################

def test_leave_invalid_token():
    '''
    test channel_leave with invalid token
    '''
    clear()
    user1 = auth.auth_register("samsmith@gmail.com", "TooGoodToSayGoodbye", "Sam", "Smith")
    user2 = auth.auth_register("adele@gmail.com", "1sing_veryW3ll", "Adele", "Singer")
    ch_1 = ch.channels_create(user1['token'], "Soloist", True)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id']) 
    with pytest.raises(error. AccessError):
        c.channel_leave(1234556, ch_1['channel_id'])
    assert c.channel_details(user1['token'], ch_1['channel_id']) == {
        'name' :  'Soloist',
        'owner_members' : [{'u_id': user1['u_id'], 'name_first': 'Sam', 'name_last': 'Smith','profile_img_url' : "",}],
        'all_members' : [{'u_id': user1['u_id'], 'name_first': 'Sam', 'name_last': 'Smith','profile_img_url' : "",},
                         {'u_id': user2['u_id'], 'name_first': 'Adele', 'name_last': 'Singer','profile_img_url' : "",}]
    }

def test_leave_normal():
    '''
    test channel_leave with simple normal behaviour
    '''
    clear()
    user1 = auth.auth_register("spongebobsquarepants@gmail.com", "garry_is_lovely",
                               "Spongebob", "Squarepants")
    user2 = auth.auth_register("patrickstar@gmail.com", "nothing_todo", "Patrick", "Star")
    user3 = auth.auth_register("plankton@gmail.com", "i_WANT_the_RECIPE", "Plankton", "Evil")
    user4 = auth.auth_register("karen_computer@gmail.com", "i_wannabe_alive", "Karen", "Computer")
    ch_1 = ch.channels_create(user1['token'], "bikini bottom", True)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user3['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user4['u_id'])
    c.channel_leave(user2['token'], ch_1['channel_id'])
    assert c.channel_details(user1['token'], ch_1['channel_id']) == {
        'name' : 'bikini bottom',
        'owner_members' : [{'u_id': user1['u_id'], 'name_first': 'Spongebob',
                            'name_last': 'Squarepants','profile_img_url' : "",}],
        'all_members' : [{'u_id': user1['u_id'], 'name_first': 'Spongebob',
                          'name_last': 'Squarepants','profile_img_url' : "",},
                         {'u_id': user3['u_id'], 'name_first': 'Plankton', 'name_last': 'Evil','profile_img_url' : "",},
                         {'u_id': user4['u_id'], 'name_first': 'Karen', 'name_last': 'Computer','profile_img_url' : "",}]
    }

def test_leave_multiple_ch():
    '''
    test channel_leave on multiple members and multiple channels
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
    ch_2 = ch.channels_create(user3['token'], "Tiny Hero", False)
    ch_3 = ch.channels_create(user6['token'], "Space Hero", True)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user4['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user3['u_id'])
    c.channel_invite(user3['token'], ch_2['channel_id'], user4['u_id'])
    c.channel_invite(user6['token'], ch_3['channel_id'], user5['u_id'])
    c.channel_invite(user6['token'], ch_3['channel_id'], user4['u_id'])
    c.channel_invite(user6['token'], ch_3['channel_id'], user7['u_id'])
    c.channel_leave(user4['token'], ch_3['channel_id'])
    c.channel_leave(user4['token'], ch_1['channel_id'])
    assert c.channel_details(user1['token'], ch_1['channel_id']) == {
        'name' : 'Avengers',
        'owner_members' : [{'u_id': user1['u_id'], 'name_first': 'Steve', 'name_last': 'Roger','profile_img_url' : "",}],
        'all_members' : [{'u_id': user1['u_id'], 'name_first': 'Steve', 'name_last': 'Roger','profile_img_url' : "",},
                         {'u_id': user2['u_id'], 'name_first': 'Tony', 'name_last': 'Stark','profile_img_url' : "",},
                         {'u_id': user3['u_id'], 'name_first': 'Scott', 'name_last': 'Lang','profile_img_url' : "",}]
    }
    assert c.channel_details(user3['token'], ch_2['channel_id']) == {
        'name' : 'Tiny Hero',
        'owner_members' : [{'u_id': user3['u_id'], 'name_first': 'Scott', 'name_last': 'Lang','profile_img_url' : "",}],
        'all_members' : [{'u_id': user3['u_id'], 'name_first': 'Scott', 'name_last': 'Lang','profile_img_url' : "",},
                         {'u_id': user4['u_id'], 'name_first': 'Hope', 'name_last': 'Pym','profile_img_url' : "",}]
    }
    assert c.channel_details(user6['token'], ch_3['channel_id']) == {
        'name' : 'Space Hero',
        'owner_members' : [{'u_id': user6['u_id'], 'name_first': 'Thor', 'name_last': 'God','profile_img_url' : "",}],
        'all_members' : [{'u_id': user6['u_id'], 'name_first': 'Thor', 'name_last': 'God','profile_img_url' : "",},
                         {'u_id': user5['u_id'], 'name_first': 'Peter', 'name_last': 'Parker','profile_img_url' : "",},
                         {'u_id': user7['u_id'], 'name_first': 'Star', 'name_last': 'Lord','profile_img_url' : "",}]
    }

def test_leave_unauth():
    '''
    test channel_invite with unauthorized channel_id
    '''
    clear()
    user1 = auth.auth_register("harrypotter@gmail.com", "Dobbyis_Afree_elf",
                               "Harry", "Potter")
    user2 = auth.auth_register("hermione_granger12@gmail.com", "Wingardium_leviosa",
                               "Hermione", "Granger")
    user3 = auth.auth_register("ronweasley@gmail.com", "ginny_lil_sis", "Ron", "Weasley")
    ch_1 = ch.channels_create(user1['token'], "hogwards", False)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    c.channel_invite(user1['token'], ch_1['channel_id'], user3['u_id'])
    with pytest.raises(error.InputError):
        c.channel_leave(user3['token'], 17)
    #assert c.channel_leave(3, 17) == "Input Error! Invalid Channel"
    assert c.channel_details(user1['token'], ch_1['channel_id']) == {
        'name' : 'hogwards',
        'owner_members' : [{'u_id': user1['u_id'], 'name_first': 'Harry', 'name_last': 'Potter','profile_img_url' : "",}],
        'all_members' : [{'u_id': user1['u_id'], 'name_first': 'Harry', 'name_last': 'Potter','profile_img_url' : "",},
                         {'u_id': user2['u_id'], 'name_first': 'Hermione', 'name_last': 'Granger','profile_img_url' : "",},
                         {'u_id': user3['u_id'], 'name_first': 'Ron', 'name_last': 'Weasley','profile_img_url' : "",}]
    }

def test_leave_not_member():
    '''
    test channel_leave but the user is not a member
    '''
    clear()
    user1 = auth.auth_register("harrypotter@gmail.com", "Dobbyis_Afree_elf", "Harry", "Potter")
    user2 = auth.auth_register("hermione_granger12@gmail.com", "Wingardium_leviosa",
                               "Hermione", "Granger")
    user3 = auth.auth_register("ronweasley@gmail.com", "ginny_lil_sis", "Ron", "Weasley")
    ch_1 = ch.channels_create(user1['token'], "hogwards", False)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    with pytest.raises(error.AccessError):
        c.channel_leave(user3['token'], ch_1['channel_id'])
    #assert c.channel_leave(3, 1) == "Access Error! User is not a member"
    assert c.channel_details(user1['token'], ch_1['channel_id']) == {
        'name' : 'hogwards',
        'owner_members' : [{'u_id': user1['u_id'], 'name_first': 'Harry', 'name_last': 'Potter','profile_img_url' : "",}],
        'all_members' : [{'u_id': user1['u_id'], 'name_first': 'Harry', 'name_last': 'Potter','profile_img_url' : "",},
                         {'u_id': user2['u_id'], 'name_first': 'Hermione', 'name_last': 'Granger','profile_img_url' : "",}]
    }
##################################################################################################
##############################------------ TEST JOIN ------------------###########################

def test_join_global_owner():
    '''
    test channel_join with a global owner joining the channel
    '''
    clear()
    user1 = auth.auth_register("spongebobsquarepants@gmail.com", "garry_is_lovely",
                               "Spongebob", "Squarepants")
    user2 = auth.auth_register("patrickstar@gmail.com", "nothing_todo", "Patrick", "Star")
    ch_1 = ch.channels_create(user2['token'], "bikini bottom", False)
    c.channel_join(user1['token'], ch_1['channel_id'])
    print(c.channel_details(user2['token'], ch_1['channel_id']))
    assert c.channel_details(user2['token'], ch_1['channel_id']) == {
        'name' : 'bikini bottom',
        'owner_members' : [{'u_id': user2['u_id'], 'name_first': 'Patrick',
                            'name_last': 'Star','profile_img_url' : ""}],
        'all_members' : [{'u_id': user2['u_id'], 'name_first': 'Patrick',
                          'name_last': 'Star','profile_img_url' : ""},
                         {'u_id': user1['u_id'], 'name_first': 'Spongebob', 'name_last': 'Squarepants','profile_img_url' : ""}]
    }

def test_join_invalid_token():
    '''
    test channel_join with invalid token
    '''
    clear()
    user1 = auth.auth_register("samsmith@gmail.com", "TooGoodToSayGoodbye", "Sam", "Smith")
    auth.auth_register("adele@gmail.com", "1sing_veryW3ll", "Adele", "Singer")
    ch_1 = ch.channels_create(user1['token'], "Soloist", True)
    with pytest.raises(error. AccessError):
        c.channel_join(1234567, ch_1['channel_id'])
    assert c.channel_details(user1['token'], ch_1['channel_id']) == {
        'name' :  'Soloist',
        'owner_members' : [{'u_id': user1['u_id'], 'name_first': 'Sam', 'name_last': 'Smith','profile_img_url' : "",}],
        'all_members' : [{'u_id': user1['u_id'], 'name_first': 'Sam', 'name_last': 'Smith','profile_img_url' : "",}]
    }

def test_join_normal():
    '''
    test channel_join with simple normal behaviour
    '''
    clear()
    user1 = auth.auth_register("samsmith@gmail.com", "TooGoodToSayGoodbye", "Sam", "Smith")
    user2 = auth.auth_register("adele@gmail.com", "1sing_veryW3ll", "Adele", "Singer")
    user3 = auth.auth_register("ed_sheeran@gmail.com", "guitar_mylife", "Ed", "Sheeran")
    ch_1 = ch.channels_create(user1['token'], "Soloist", True)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    c.channel_join(user3['token'], ch_1['channel_id'])
    assert c.channel_details(user1['token'], ch_1['channel_id']) == {
        'name' : 'Soloist',
        'owner_members' : [{'u_id': user1['u_id'], 'name_first': 'Sam', 'name_last': 'Smith','profile_img_url' : "",}],
        'all_members' : [{'u_id': user1['u_id'], 'name_first': 'Sam', 'name_last': 'Smith','profile_img_url' : "",},
                         {'u_id': user2['u_id'], 'name_first': 'Adele', 'name_last': 'Singer','profile_img_url' : "",},
                         {'u_id': user3['u_id'], 'name_first': 'Ed', 'name_last': 'Sheeran','profile_img_url' : "",}]
    }

def test_join_multiple():
    '''
    test channel_join on multiple members and multiple channels
    '''
    clear()
    user1 = auth.auth_register("spongebobsquarepants@gmail.com", "garry_is_lovely",
                               "Spongebob", "Squarepants")
    user2 = auth.auth_register("patrickstar@gmail.com", "nothing_todo", "Patrick", "Star")
    user3 = auth.auth_register("plankton@gmail.com", "i_WANT_the_RECIPE", "Plankton", "Evil")
    user4 = auth.auth_register("karen_computer@gmail.com", "i_wannabe_alive", "Karen", "Computer")
    user5 = auth.auth_register("mr_krab@gmail.com", "pearl_mysunshine", "Mister", "Krab")
    ch_1 = ch.channels_create(user1['token'], "KrustyKrab", True)
    ch_2 = ch.channels_create(user3['token'], "Chum Bucket", False)
    ch_3 = ch.channels_create(user5['token'], "bikini bottom", True)
    c.channel_join(user2['token'], ch_1['channel_id'])
    c.channel_join(user2['token'], ch_3['channel_id'])
    c.channel_join(user5['token'], ch_1['channel_id'])
    c.channel_join(user4['token'], ch_3['channel_id'])
    assert c.channel_details(user1['token'], ch_1['channel_id']) == {
        'name' : 'KrustyKrab',
        'owner_members' : [{'u_id': user1['u_id'], 'name_first': 'Spongebob',
                            'name_last': 'Squarepants','profile_img_url' : "",}],
        'all_members' : [{'u_id': user1['u_id'], 'name_first': 'Spongebob',
                          'name_last': 'Squarepants','profile_img_url' : "",},
                         {'u_id': user2['u_id'], 'name_first': 'Patrick', 'name_last': 'Star','profile_img_url' : "",},
                         {'u_id': user5['u_id'], 'name_first': 'Mister', 'name_last': 'Krab','profile_img_url' : "",}]
    }
    assert c.channel_details(user3['token'], ch_2['channel_id']) == {
        'name' : 'Chum Bucket',
        'owner_members' : [{'u_id': user3['u_id'], 'name_first': 'Plankton', 'name_last': 'Evil','profile_img_url' : "",}],
        'all_members' : [{'u_id': user3['u_id'], 'name_first': 'Plankton', 'name_last': 'Evil', 'profile_img_url' : "",}]
    }
    assert c.channel_details(user5['token'], ch_3['channel_id']) == {
        'name' : 'bikini bottom',
        'owner_members' : [{'u_id': user5['u_id'], 'name_first': 'Mister', 'name_last': 'Krab', 'profile_img_url' : "",}],
        'all_members' : [{'u_id': user5['u_id'], 'name_first': 'Mister', 'name_last': 'Krab', 'profile_img_url' : "",},
                         {'u_id': user2['u_id'], 'name_first': 'Patrick', 'name_last': 'Star', 'profile_img_url' : "",},
                         {'u_id': user4['u_id'], 'name_first': 'Karen', 'name_last': 'Computer', 'profile_img_url' : "",}]
    }

def test_join_unauth():
    '''
    test channel_join with unauthorized channel_id
    '''
    clear()
    user1 = auth.auth_register("spongebobsquarepants@gmail.com", "garry_is_lovely",
                               "Spongebob", "Squarepants")
    user3 = auth.auth_register("plankton@gmail.com", "i_WANT_the_RECIPE", "Plankton", "Evil")
    ch_1 = ch.channels_create(user1['token'], "KrustyKrab", True)
    with pytest.raises(error.InputError):
        c.channel_join(user3['token'], 13)
    #assert c.channel_join(3, 13) == "Input Error! Invalid Channel"
    assert c.channel_details(user1['token'], ch_1['channel_id']) == {
        'name' : 'KrustyKrab',
        'owner_members' : [{'u_id': user1['u_id'], 'name_first': 'Spongebob',
                            'name_last': 'Squarepants', 'profile_img_url' : "",}],
        'all_members' : [{'u_id': user1['u_id'], 'name_first': 'Spongebob',
                          'name_last': 'Squarepants','profile_img_url' : "",}]
    }

def test_join_private():
    '''
    test channel_join to join a private channel
    '''
    clear()
    user1 = auth.auth_register("spongebobsquarepants@gmail.com", "garry_is_lovely",
                               "Spongebob", "Squarepants")
    user3 = auth.auth_register("plankton@gmail.com", "i_WANT_the_RECIPE", "Plankton", "Evil")
    user4 = auth.auth_register("karen_computer@gmail.com", "i_wannabe_alive", "Karen", "Computer")
    ch_1 = ch.channels_create(user1['token'], "KrustyKrab", True)
    ch_2 = ch.channels_create(user3['token'], "Chum Bucket", False)
    with pytest.raises(error.AccessError):
        c.channel_join(user4['token'], ch_2['channel_id'])
    #assert c.channel_join(4, 2) == "Access Error! Channel is private or User already a member"
    assert c.channel_details(user1['token'], ch_1['channel_id']) == {
        'name' : 'KrustyKrab',
        'owner_members' : [{'u_id': user1['u_id'], 'name_first': 'Spongebob',
                            'name_last': 'Squarepants','profile_img_url' : "",}],
        'all_members' : [{'u_id': user1['u_id'], 'name_first': 'Spongebob',
                          'name_last': 'Squarepants','profile_img_url' : "",}]
    }
    assert c.channel_details(user3['token'], ch_2['channel_id']) == {
        'name' : 'Chum Bucket',
        'owner_members' : [{'u_id': user3['u_id'], 'name_first': 'Plankton', 'name_last': 'Evil','profile_img_url' : "",}],
        'all_members' : [{'u_id': user3['u_id'], 'name_first': 'Plankton', 'name_last': 'Evil','profile_img_url' : "",}]
    }

def test_join_already_a_member():
    '''
    test channel_join but the user is already a member
    '''
    clear()
    user1 = auth.auth_register("spongebobsquarepants@gmail.com", "garry_is_lovely",
                               "Spongebob", "Squarepants")
    user2 = auth.auth_register("patrickstar@gmail.com", "nothing_todo", "Patrick", "Star")
    ch_1 = ch.channels_create(user1['token'], "KrustyKrab", True)
    c.channel_invite(user1['token'], ch_1['channel_id'], user2['u_id'])
    with pytest.raises(error.AccessError):
        c.channel_join(user2['token'], ch_1['channel_id'])
    #assert c.channel_join(2, 1) == "Access Error! Channel is private or User already a member"
    assert c.channel_details(user1['token'], ch_1['channel_id']) == {
        'name' : 'KrustyKrab',
        'owner_members' : [{'u_id': user1['u_id'], 'name_first': 'Spongebob',
                            'name_last': 'Squarepants','profile_img_url' : "",}],
        'all_members' : [{'u_id': user1['u_id'], 'name_first': 'Spongebob', 'name_last':
                          'Squarepants','profile_img_url' : "",},
                         {'u_id': user2['u_id'], 'name_first': 'Patrick', 'name_last': 'Star','profile_img_url' : "",}]
    }
