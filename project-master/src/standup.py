'''
    The file consist of standup_start, standup_send, standup_active
'''
import threading
from datetime import datetime
import data as d
from error import InputError
from error import AccessError

STANDUP = {}
ACTIVE = {}

def standup_start(token, channel_id, length):
    '''
    start the standup period whereby for the next "length" seconds
    '''
    #validate token
    if d.validate_token(token) is False:
        raise AccessError("Invalid token")
    #check for valid channel
    channel = d.get_channel(channel_id)
    if channel['id'] == -1:
        raise InputError("Input Error! Invalid Channel!")

    if not d.is_authorized(token, channel_id, "member"):
        raise AccessError("Unauthorized user")


    #check for active standup
    active = standup_active(token, channel_id)['is_active']
    if active is True:
        raise InputError("Input Error! An active standup is currently running on this channel.")
    if length < 1:
        raise InputError("Input Error! Stand up must be atleast of 1 second")
    now = datetime.now()
    now_timestamp = int(now.replace().timestamp())
    time_finish = now_timestamp + length
    global ACTIVE
    ACTIVE[channel_id] = time_finish
    STANDUP[channel_id] = []
    thread = threading.Timer(length, standup_message_send_and_activeclear, kwargs={'token': token, 'channel_id': channel_id})
    thread.start()
    return time_finish

def standup_send(token, channel_id, message):
    '''
    Sending a message to get buffered in the standup queue
    '''
    #validate token
    if d.validate_token(token) is False:
        raise AccessError("Invalid token")
    #check for active standup
    active = standup_active(token, channel_id)['is_active']
    if active is False:
        raise InputError("Input Error! An active standup is not currently running on this channel.")

    #check for valid channel
    channel = d.get_channel(channel_id)
    if channel['id'] == -1:
        raise InputError("Input Error! Invalid Channel!")

    if not d.is_authorized(token, channel_id, "member"):
        raise AccessError("Unauthorized user")

    if len(message) > 1000:
        raise InputError("Message must be shorter than 1000 characters!")


    global STANDUP
    user = d.get_user(d.decoding_token(token))['handle_str']
    msg_data = f"{user}: {message}"
    for c_id in STANDUP:
        if channel_id == c_id:
            STANDUP[channel_id].append(msg_data)

def standup_active(token, channel_id):
    '''
    Check weather there is an active standup
    '''
    #validate token
    if d.validate_token(token) is False:
        raise AccessError("Invalid token")
    #check for valid channel
    channel = d.get_channel(channel_id)
    if channel['id'] == -1:
        raise InputError("Input Error! Invalid Channel!")

    if not d.is_authorized(token, channel_id, "member"):
        raise AccessError("Unauthorized user")


    #check if there is an active thread
    global ACTIVE
    if_active = False
    time_finish = None
    for c_id in ACTIVE:
        if channel['id'] == c_id:
            if ACTIVE[channel_id] is None:
                if_active = False
            else:
                if_active = True
                time_finish = ACTIVE[channel_id]
    return {
        'is_active' : if_active,
        'time_finish' : time_finish
    }

################ HELPER FUNCTION FOR STANDUP'S MESSAGES #####################################
def standup_message_send_and_activeclear(token, channel_id):
    '''
    To send the buffered message from standup as a single message
    '''
    global ACTIVE
    for c_id in ACTIVE:
        if channel_id == c_id:
            ACTIVE[channel_id] = None

    #check standup active
    active = standup_active(token, channel_id)['is_active']
    if active is True:
        raise AccessError("A standup is currently active. Can't send standup as a message yet.")
    global STANDUP
    str_send = ""
    #concatinate the message into a one single string
    for string in STANDUP[channel_id]:
        str_send += string
        str_send += '\n'

    message_time = int(datetime.utcnow().timestamp())
    send_later = False
    d.add_message(token, channel_id, str(str_send), message_time, send_later)
    STANDUP[channel_id] = {}
