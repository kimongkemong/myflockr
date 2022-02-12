'''
File consist of channel_invite, channel_details, channel_messages,
channel_leave, channel_join, channel_removeowner, channel_addowner
'''
import data as d
from error import InputError
from error import AccessError

def channel_invite(token, channel_id, u_id):
    '''
    Invites a user to join a channel with ID channel_id.
    '''
    if d.validate_token(token) is False:
        raise AccessError("Unauthorized action")
    #checks if channel_id is valid
    if d.get_channel(channel_id)['id'] == -1:
        raise InputError("Input Error! Invalid Channel or User")
    #checks if u_id is valid
    #valid_user = d.search_user(u_id)
    valid_user = d.get_user(u_id)
    if valid_user['u_id'] == -1:
        raise InputError("Access Error! User is not registered")
    new_user_token = d.encoding_token(u_id)
    ###############################################
    if d.is_authorized(new_user_token, channel_id, "member") == True:
        raise AccessError("Access Error! User is already a member")
    ###############################################
    #remove a user -> delete the user from the channel member in channel_details
    channel = d.get_channel(channel_id)
    ###############################################
    channel['member_id'].append(u_id)
    ###############################################

#return the details of the given channel

def channel_details(token, channel_id):
    
    #used to storing certain data
    details = {}
    owners = []
    members = []

    #if the user isn't the member of the channel or the user haven't logged in, raise AccessError
    if not d.validate_token(token):
        raise AccessError ("No authorization. Invalid Access")

    #if the channel id does not exist in data, raise InputError  
    if d.get_channel(channel_id)['id'] == -1:
        raise InputError ("No such channel")

    if not d.is_authorized(token, channel_id, "member"):
        raise AccessError ("No authorization. Invalid Access")

    #Get the address of the channel
    channel = d.get_channel(channel_id)

    #assign names
    details['name'] = channel['name']

    #assign owner members
    for owner_id in channel['owner_id']:
        owner = d.search_user(owner_id)
        if owner['u_id'] != -1:
            owners.append(owner)
    details['owner_members'] = owners


    #assign all members
    for member_id in channel['member_id']:
        member = d.search_user(member_id)
        if member['u_id'] != -1:
            members.append(member)

    details['all_members'] = members
    return details

def channel_messages(token, channel_id, start):
    '''
    Given a Channel with ID channel_id that the authorised user is part of,
    return up to 50 messages.
    Returns InputError when Channel ID is not a valid channel and start is 
    greater than the total number of messages in the channel.
    AccessError when authorised user is not a member of channel with channel_id.
    '''
    return_messages = []

    if not d.validate_token(token):
        raise AccessError("Unauthorized action")

    #If channel does not exist, return InputError
    if d.get_channel(channel_id) == {'id': -1}:
        raise InputError("Input Error! Invalid Channel")

    #If the user is not a member of the channel, return AccessError
    if d.is_authorized(token, channel_id, "member") == 0:
        raise AccessError("Access Error! User is not a member")

    channel = d.get_channel(channel_id)
    num_messages = len(channel['messages'])

    #Input error if start position given is greater than the total number of messages in the channel
    if start > num_messages:
        raise InputError("Input Error! There are not enough messages in the channel")

    i = 0
    num_messages = 0
    end = start + 50
    for message in channel['messages']:
        if start <= i < end:
            return_messages.append(message.copy())
            num_messages += 1
        i += 1

    # If given user has reacted to the message then reflect this
    for message in return_messages:
        for react in message['reacts']:
            if d.decoding_token(token) in react['u_ids']:
                react['is_this_user_reacted'] = True
            else:
                react['is_this_user_reacted'] = False

    #Return -1 if the oldest message in the channel has been returned and
    #there are no more messages after it
    if len(channel['messages']) == start + num_messages:
        end = -1

    result = {'messages':return_messages, 'start': start, 'end': end}
    return result

def channel_leave(token, channel_id):
    '''
    Given a channel ID, the user removed as a member of this channel
    '''
    if d.validate_token(token) is False:
        raise AccessError("Unauthorized action")
    #checks if channel_id is valid
    if d.get_channel(channel_id)['id'] == -1:
        raise InputError("Input Error! Invalid Channel")
    if d.is_authorized(token, channel_id, "member") == 0:
        raise AccessError("Access Error! User is not a member")

    #remove a user -> delete the user from the channel member in channel_details
    for channel in d.data['channels']:
        if channel_id == channel['id']:
        ###############################################
            channel['member_id'].remove(d.decoding_token(token))
        ###############################################


def channel_join(token, channel_id):
    '''
    Given a channel_id of a channel that the authorised user can join,
    adds them to that channel
    '''
    if d.validate_token(token) is False:
        raise AccessError("Unauthorized action")
    #checks if channel_id is valid
    if d.get_channel(channel_id)['id'] == -1:
        raise InputError("Input Error! Invalid Channel")
    if d.is_authorized(token, channel_id, "member") != 0:
        raise AccessError("Access Error! User already a member")
    #checks if channel_id refers to private channel
    u_id = d.decoding_token(token)
    channel = d.get_channel(channel_id)
    if channel['is_public'] is False:
        user = d.get_user(u_id)['permission']
        #if the user is a global owner
        if user == 1:
            channel['member_id'].append(u_id)
        else:
            raise AccessError("Access Error! Channel is private")
    else:
    #join a user -> put u_id into channel member in channel_details
    ###############################################
        channel['member_id'].append(u_id)
    ###############################################

#if the arguments provided are valid, add the user as an owner
def channel_addowner(token, channel_id, u_id):

    #if the user isn't the owner of the channel or the user haven't logged in, raise an AccessError
    if not d.validate_token(token):
        raise AccessError ("Unauthorized action!")

    #if the channel id does not exist in data, raise InputError  
    if d.get_channel(channel_id)['id'] == -1:
        raise InputError ("No such channel")

    if (not d.is_authorized(token, channel_id, "owner")) and (not d.is_authorized(token, channel_id, "global")):
        raise AccessError ("Unauthorized action!")

    #get the address of the certain channel
    channel = d.get_channel(channel_id)

    #if the user is not already in the owner list, add the user as an owner
    if u_id not in channel['owner_id']:
        channel['owner_id'].append(u_id)

    #if the user is already one of the owners, raise an InputError    
    else:
        raise InputError ("The user already exists in the owner list!")

    #if the user wasn't even an member before, we should also add him as a member
    if u_id not in channel['member_id']:
        channel['member_id'].append(u_id)



#if the arguments provided are valid, remove the owner chosen
def channel_removeowner(token, channel_id, u_id):
    
    #if the user isn't the owner of the channel or the user haven't logged in, raise an AccessError
    if not d.validate_token(token):
        raise AccessError ("Unauthorized action!")

    #if the channel id does not exist in data, raise InputError  
    if d.get_channel(channel_id)['id'] == -1:
        raise InputError ("No such channel")

    if (not d.is_authorized(token, channel_id, "owner")) and (not d.is_authorized(token, channel_id, "global")):
        raise AccessError ("Unauthorized action!")

    #get the address of the channel
    channel = d.get_channel(channel_id)

    #if the only owner of the channel want to remove himself, raise an InputError
    if len(channel['owner_id']) <= 1 and u_id in channel['owner_id']:
        raise InputError ('You are the only owner of the channel!!')

    #if not and the user_id given is in owner list, then we remove the owner chosen
    if u_id in channel['owner_id']:
        channel['owner_id'].remove(u_id)
    
    #if the user_id given isn't even in the owner list, raise an InputError
    else:
        raise InputError ("The user doesn't exist in the owner list!")

            
