'''Function to create and listing channel as required'''
from error import AccessError, InputError
from data import data, add_channel, validate_token, decoding_token

def channels_list(token):
    '''List all the channel that the users are in it'''
    #Checking wheter token is valid
    check_token = validate_token(token)
    if check_token is False:
        raise AccessError("Error! Unauthorized Action")

    #Make a new dictionary for every channel that included the user
    #and put a necessary detial into a list
    user_included = {'channels':[]}
    user_id = decoding_token(token)
    for channel in data['channels']:
        if user_id in channel['member_id']:
            list_channel = {}
            list_channel['channel_id'] = channel['id']
            list_channel['name'] = channel['name']
            user_included['channels'].append(list_channel)
    return user_included

def channels_listall(token):
    '''Listing all the channel that are in the system'''
    #Checking wheter token is valid
    check_token = validate_token(token)
    if check_token is False:
        raise AccessError("Error! Unauthorized Action")

    # Make a new directory for every channel with a necessary detail
    all_channel = {
        'channels':[
            ]
        }
    for channel in data['channels']:
        list_channel = {}
        list_channel['channel_id'] = channel['id']
        list_channel['name'] = channel['name']
        all_channel['channels'].append(list_channel)
    return all_channel

def channels_create(token, name, is_public):
    '''Creating a new channel'''
    #Checking wheter token is valid
    check_token = validate_token(token)
    if check_token is False:
        raise AccessError("Error! Unauthorized Action")

    #checking the length of name for the channel
    if len(name) > 20:
        raise InputError("Channel name must be less than 20 character")

    channel_id = add_channel(token, name, is_public)

    return {
        'channel_id': channel_id,
    }
