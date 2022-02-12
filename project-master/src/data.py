'''A collection of helper function for the project'''
import datetime
from datetime import timezone
import re
import hashlib
import jwt
import threading

user_counter = 1
message_counter = 1

data = {'users':[], 'channels':[], 'active_tokens':[], 'reset_code':[]}

#get all the info of a user. If the id doesn't exist, return its id as -1
def get_user(u_id):
    global data
    for user in data['users']:
        if u_id == user['u_id']:
            return user

    return {'u_id':-1}

#add(create) new channel information to the database
def add_channel(token, name, is_public):
    global data
    channel = {}
    channel['id'] = len(data['channels']) + 1
    channel['name'] = name
    channel['owner_id'] = [decoding_token(token)]
    channel['member_id'] = [decoding_token(token)]
    channel['messages'] = []
    channel['is_public'] = is_public
    data['channels'].append(channel)
    return channel['id']


#get all the info of a channel. If the id doesn't exist, return its id as -1
def get_channel(c_id):
    global data
    for channel in data['channels']:
        if c_id == channel['id']:
            return channel

    return {'id':-1}


######################Helper function for channel.py##########################
###############################################################################
#helper function for channel_details, if user not found then return its u_id as -1.
def search_user(u_id):
    user_info = {}
    user = get_user(u_id)

    if user['u_id'] == -1:
        return {'u_id': -1}

    user_info['u_id'] = user['u_id']
    user_info['name_first'] = user['name_first']
    user_info['name_last'] = user['name_last']
    if 'profile_img_url' in user.keys():
        user_info['profile_img_url'] = user['profile_img_url']
    else:
        user_info['profile_img_url'] = ""
    return user_info


#helper function to use token, check if the user has authorization to give command.
#Now we always assume channel exists
def is_authorized(token, channel_id, role= "member"):
    channel = get_channel(channel_id)
    assert channel['id'] != -1

    if not validate_token(token):
        return False

    if role == 'member':
        if decoding_token(token) in channel['member_id']:
            return True

    if role == 'owner':
        if decoding_token(token) in channel['owner_id']:
            return True

    if role == 'global':
        user = get_user(decoding_token(token))
        if user['permission'] == 1:
            return True

    return False

#################################### HELPER FUNCTIONS FOR TOKENS ###################################################

# Encoding The user_id -> token
def encoding_token(user_id):
    SECRET = 'grape01'
    encoded_token = jwt.encode({'id': user_id}, SECRET, algorithm='HS256').decode('utf-8')
    return encoded_token

# Decoding the Token -> user_id
def decoding_token(token):
    SECRET = 'grape01'
    decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
    return decoded_token['id']

# Validating Token
def validate_token(token):
    if token in data['active_tokens']:
        return True
    else:
        return False

##########################################################################
##                  Helper functions for message.py                     ##
##########################################################################
def add_message(token, channel_id, message, message_time, send_later):
    '''
    This function adds a message to the list of messages in a given channel.
    '''
    global data
    global message_counter

    new_message = {}
    new_message['message'] = message

    sender_id = decoding_token(token)
    new_message['u_id'] = sender_id

    new_message['message_id'] = message_counter
    message_counter += 1
    channel = get_channel(channel_id)

    new_message['reacts'] = []

    new_message['is_pinned'] = False
    new_message['time_created'] = message_time

    if not send_later:
        channel['messages'].insert(0, new_message)

    if send_later:
        # Get current time Unix timestamp to figure out the timer wait time.
        now = datetime.datetime.now(timezone.utc)
        now_timestamp = int(now.replace(tzinfo=timezone.utc).timestamp())

        wait = message_time - now_timestamp
        t = threading.Timer(wait, add_message_later, [new_message, channel_id])
        t.start()

    return new_message['message_id']

def add_message_later(new_message, channel_id):
    '''
    This function is called only if a message is to be sent later than the current time.
    When called it add the message to the channel.
    '''
    global data
    channel = get_channel(channel_id)
    channel['messages'].insert(0, new_message)


def get_message_channel(message_id):
    '''
    When given a message_id, this function will return the relevant channel_id that the message is in.
    If the message does not exist/ no longer exists, then the function will return -1.
    '''
    for channel in data['channels']:
        for message in channel['messages']:
            if (message['message_id'] == message_id):
                return channel['id']
    return -1


def add_react(token, message_id, channel_id, react_id):
    '''
    This function adds a react from a certain user to a given message.
    '''
    global data

    curr_message = get_msg_info(message_id, channel_id)

    added_react = False
    for react in curr_message['reacts']:
        if react['react_id'] == react_id:
            # don't want to add the same user_id twice
            if decoding_token(token) in react['u_ids']:
                added_react = True
                break
            else:
                react['u_ids'].append(decoding_token(token))
                added_react = True
                break

    if not added_react:
        new_react = {'react_id': react_id, 'u_ids': [decoding_token(token)]}
        curr_message['reacts'].append(new_react)

    return

#only be used when channel and message is assured to exist
def get_msg_info(message_id, channel_id):

    channel = get_channel(channel_id)

    for msg in channel['messages']:
        if msg['message_id'] == message_id:
            return msg

#################################### HELPER FUNCTIONS FOR PASSWORD AND EMAILS ###################################################

def email_validation(email):
    # Module to check if an email is valid or not
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, email):
        return True
    else:
        return False

# Encoding The password(str) -> encrypted_form(str)
def encoding_password(password):
    encoded_password = hashlib.sha256(password.encode()).hexdigest()
    return encoded_password
