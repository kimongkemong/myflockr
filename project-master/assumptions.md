Assumptions:
General assumption:
1. AccessError will be raised first even if both errors of InputError & AccessError occur

Channel.py
1.  Raise an error if the user join a channel that they already a member.
2.  Once a channel is created, it always has a user already 
3.  Token is regarded as the user_id of the owners of the channel in Iteration 1.
4.  Owner of the channel could be more than one.
5.  Tokens, channel_id and user_id may be given in the wrong format.
6.  Every One can be added as an owner even if he wasn't in the channel before.


Channels.py
1. One user can create more than one channel
2. When user request list all of the channel then it will list all the channel wheter the channel private or public


auth_login
1. The program will not tell the user which inputs are wrong 
2. User can do multiple login
 

auth_register
1. user id will not be randomly generated, instead it will be ordered 
2. User registered with the same first and last name will be allowed
3. password's length does not have a limit 
4. After register, user will automatically Login

 
auth_logout
1. User will not be given an option to log out without log in beforehand

Message.py
1.  Other than the owner, the user who sent the message also can edit the message.
2.  Storing messages - message 'data' (message, time of send, u_id, message id) will be stored within each channel. 
this means that as the message remove function does not have channel_id as an input, the message must be found by looking into the relevant channel 
(and matching the unique message ID).
3. Even if a message has been deleted, its relevant message ID cannot be reused.
4. The time message send time is not changed when it is edited.
5. Calling message_react twice in a row will do nothing, and 2nd is that there will be an input error if a user calls message/unreact without having reacted to it previously

User_profile:
1. If the token is not valid, then will raise AccessError

 User Setname:
1. First and last name can be change with any character even with spaces 
2. user can change their name more than one time

Users_all:
1. Since it’s implicit in Spec, we assume that if the token is invalid then we will raise an AccessError
2. For all valid token, the user has the authorization to view details of all the user.


Other.py
1. search: the messages must match the exact query_string (including Capital letters, lower letters, and characters) 
2. search: Not a single match found, raise error 
3. search: raise error if the user is not part of any channel


Standup.py
standup_start:
1. Length of standup must be > 0 (minimum of 1 second), otherwise raise InputError


User/passwordreset
1. The code given in an email will be a string with unordered uppercase/lowercase char and integer
2. To receive the email, We assume the user has created an account with the registered email
