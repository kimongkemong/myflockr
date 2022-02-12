'''Containing a global function'''
from data import validate_token, decoding_token, encoding_token, data, get_user
from user import user_profile
import channel as c
import channels as ch
from error import AccessError, InputError

def clear():
    '''
    function to clear global data
    '''
    global data
    global user_counter
    global channel_counter
    global message_counter
    user_counter = 1
    channel_counter = 1
    message_counter = 1
    data['users'] = []
    data['channels'] = []
    data['active_tokens'] = []


def users_all(token):
    '''
    Returns a list of all users and their associated details
    '''

    #If the token is invalid, then raise an AccessError
    if not validate_token(token):
        raise AccessError("Invalid token")

    #Create a list to store all the user profiles
    all_user = []

    #Loop to call user_profile for all users, and store them in all_user.
    for i in data['users']:
        u_p = user_profile(token, i['u_id'])['user']
        all_user.append(u_p)
    return {'users': all_user}

def admin_userpermission_change(token, u_id, permission_id):
    '''Changing user permission'''

    #checking token
    check_token = validate_token(token)
    if check_token is False:
        raise AccessError("Error! Unauthorized Action")

    curr_user = decoding_token(token)
    #check if the user is the owner
    for user in data['users']:
        if curr_user == user['u_id']:
            if user['permission'] == 1:
                break
            elif user['permission'] == 2:
                raise AccessError("Error! User is not an owner")

    #check if u_id is a valid user
    '''
    u_id_token = encoding_token(u_id)
    check_u_id = validate_token(u_id_token)
    if check_u_id is False:
        raise InputError("Error! u_id is not a valid user")
    '''
    if get_user(u_id)['u_id'] == -1:
        raise InputError("Error! u_id is not a valid user")

    #check the value of permission_id
    if permission_id < 0 or permission_id > 2:
        raise InputError("Error! Invalid permission_id")

    #change the target user to the realted permission
    for target_user in data['users']:
        if u_id == target_user['u_id']:
            target_user['permission'] = permission_id
    return {}

def search(token, query_str):
    '''
    Given a query string, return a collection of messages in all of the channels 
    that the user has joined that match the query
    '''
    #validate token
    if validate_token(token) is False:
        raise AccessError("Invalid token")
    message_found = []
    #find the user is a member from which channnel
    ch_list = ch.channels_list(token)
    if ch_list == {'channels': []}:
        raise AccessError("User is not a member of any channel")

    #for each channel the user is in, find the matching string
    for curr_channel in ch_list['channels']:
        ch_message = c.channel_messages(token, curr_channel['channel_id'], 0)
        #find the matching string in the list of messages
        for curr_message in ch_message['messages']:
            if curr_message['message'].find(query_str) != -1:
                message_found.append(curr_message)

    if message_found == []:
        raise InputError("No message found")
    return {'messages': message_found}
