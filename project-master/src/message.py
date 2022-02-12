import data
from error import InputError
from error import AccessError
import datetime
from datetime import timezone

def message_send(token, channel_id, message):
    '''
    Send a message from authorised_user to the channel specified by channel_id
    '''
    #Checking wheter token is valid
    check_token = data.validate_token(token)
    if check_token is False:
        raise AccessError("Invalid token")

    if len(message) > 1000:
        raise InputError("Message must be shorter than 1000 characters!")

    if not data.is_authorized(token, channel_id, "member"):
        raise AccessError("You are not a member of this channel!")

    now = datetime.datetime.now(timezone.utc)
    now_timestamp = int(now.replace(tzinfo=timezone.utc).timestamp())

    send_later = False
    message_id = data.add_message(token, channel_id, message, now_timestamp, send_later)

    return {'message_id': message_id}

def message_remove(token, message_id):
    '''
    with the given message_id for a message, removed the message from channel
    '''
    check_token = data.validate_token(token)
    if check_token is False:
        raise AccessError("Invalid token")

    c_id = data.get_message_channel(message_id)

    # Input error if the message does not exist
    if (c_id == -1):
        raise InputError("Message does not exist!")

    

    curr_channel = data.get_channel(c_id)
    message_to_remove = data.get_msg_info(message_id, c_id)
    
    if message_to_remove['u_id'] == data.decoding_token(token) or (data.is_authorized(token, c_id, "owner") or data.is_authorized(token, c_id, "global")):
        curr_channel['messages'].remove(message_to_remove)
        return {}
    else:
        raise AccessError("You are not authorised to remove this message")


def message_edit(token, message_id, message):
    '''
    update it's text with new text. If the new message is an empty string, the message is deleted.
    '''
    if data.validate_token(token) is False:
        raise AccessError("Invalid token")

    if message == "":
        message_remove(token, message_id)
        return {}
    else:
        ch_id = data.get_message_channel(message_id)

        if (ch_id == -1):
            raise InputError("Message does not exist!")

        curr_msg = data.get_msg_info(message_id, ch_id)
        if curr_msg['u_id'] == data.decoding_token(token) or (data.is_authorized(token, ch_id, "owner") or data.is_authorized(token, ch_id, "global")):
            curr_msg['message'] = message
            return {}
        else:
            raise AccessError("You are not authorised to edit this message")


def message_react(token, message_id, react_id):
    '''
    add a "react" to that particular message with that particular message_id
    '''
    check_token = data.validate_token(token)
    if check_token is False:
        raise AccessError("Invalid token")

    # For the purposes of this assignment, the only valid react_id is 1.
    # The following 2 lines could be easily altered if there were more valid react_ids added.
    if (react_id != 1):
        raise InputError("Invalid react_id")

    c_id = data.get_message_channel(message_id)

    # Input error if the message does not exist
    if (c_id == -1):
        raise InputError("Message does not exist!")

    # Can only react to messages in a channel the user is a member of
    if not data.is_authorized(token, c_id, "member"):
        raise InputError("This message_id is not in a channel that you are a member of")

    data.add_react(token, message_id, c_id, react_id)

    return {}

def message_unreact(token, message_id, react_id):
    '''
    remove a "react" to that particular message with that particular message_id
    '''
    check_token = data.validate_token(token)
    if check_token is False:
        raise AccessError("Invalid token")

    # For the purposes of this assignment, the only valid react_id is 1.
    # The following 2 lines could be easily altered if there were more valid react_ids added.
    if (react_id != 1):
        raise InputError("Invalid react_id")

    c_id = data.get_message_channel(message_id)

    # Input error if the message does not exist
    if (c_id == -1):
        raise InputError("Message does not exist!")

    # Can only react to messages in a channel the user is a member of
    if not data.is_authorized(token, c_id, "member"):
        raise InputError("This message_id is not in a channel that you are a member of")

    curr_message = data.get_msg_info(message_id, c_id)

    valid_react = False
    for react in curr_message['reacts']:
        if react['react_id'] == react_id:
            curr_react = react
            valid_react = True
            break

    if not valid_react:
        raise InputError("This react_id is not active")
    u_id = data.decoding_token(token)

    user_reacted = False
    if u_id in curr_react['u_ids']:
        react['u_ids'].remove(u_id)
        user_reacted = True

    if not user_reacted:
        raise InputError("You never reacted to this message in the first place")
    return {}

def message_sendlater(token, channel_id, message, time_sent):
    '''
    Send a message from user to the channel specified by channel_id
    automatically at a specified time in the future
    '''
    check_token = data.validate_token(token)
    if check_token is False:
        raise AccessError("Invalid token")

    if len(message) > 1000:
        raise InputError("Message must be shorter than 1000 characters!")

    channel_validate = data.get_channel(channel_id)

    if channel_validate['id'] == -1:
        raise InputError("Channel ID is not valid")

    if not data.is_authorized(token, channel_id, "member"):
        raise AccessError("You are not a member of this channel!")

    now = datetime.datetime.now(timezone.utc)
    now_timestamp = int(now.replace(tzinfo=timezone.utc).timestamp())

    difference = time_sent - now_timestamp
    if int(difference) < 0:
        raise InputError("You cannot send a message to a time in the past!")

    send_later = True
    message_id = data.add_message(token, channel_id, message, time_sent, send_later)

    return {'message_id': message_id}


def message_pin(token, message_id):
    '''
    #Pin the given message
    '''
    #First we check if the token is valid, if not, raise an AccessError
    if not data.validate_token(token):
        raise AccessError("Unauthorised action!")

    #Get the channel_id in which the message was sent by using helper func in data.py
    ch_id = data.get_message_channel(message_id)

    #If we can't find the channel, then raise an InputError
    if (ch_id == -1):
        raise InputError("Message does not exist!")

    #If token is from a user who is not a member of the channel or global owner, raise AccessError
    if not data.is_authorized(token, ch_id, "member") and not data.is_authorized(token, ch_id, "global"):
        raise AccessError("The user has no authorization!")

    #Get the msg info by helper func in data.py
    msg = data.get_msg_info(message_id, ch_id)

    #If the msg is already pinned , raise an InputError
    if msg['is_pinned'] is True:
        raise InputError("The message is already pinned!")

    #Else pin the msg.
    msg['is_pinned'] = True

def message_unpin(token, message_id):
    '''
    remove a pin from a particular message
    '''
    #First we check if the token is valid, if not, raise an AccessError
    if not data.validate_token(token):
        raise AccessError("Unauthorised action!")

    #Get the channel_id in which the message was sent by using helper func in data.py
    ch_id = data.get_message_channel(message_id)

    #If we can't find the channel, then raise an InputError
    if (ch_id == -1):
        raise InputError("Message does not exist!")

    #If token is from a user who is not a member of the channel or global owner, raise AccessError
    if not data.is_authorized(token, ch_id, "member") and not data.is_authorized(token, ch_id, "global"):
        raise AccessError("The user has no authorization!")

    #Get the msg info by helper func in data.py
    msg = data.get_msg_info(message_id, ch_id)

    #If the msg is already unpinned, then raise an InputError
    if msg['is_pinned'] is False:
        raise InputError("The message is already unpinned!")

    #Else unpin the msg.
    msg['is_pinned'] = False
