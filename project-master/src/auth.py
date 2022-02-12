import re
from datetime import datetime
from data import data, encoding_token, email_validation, encoding_password, get_user
from error import InputError
import smtplib, ssl
import random
import string

def auth_login(email, password):
    # Email Validation
    if not email_validation(email):
        raise InputError("Error, email is invalid")
    success_flag = False
    # Check if the email exits
    for user in data['users']:
        if (user['email'] == email) and (user['password'] == encoding_password(password)):
            success_flag = True
            current_user = user
            break
    if not success_flag:
        raise InputError("Error, email does not exist")
    # Storing the token
    token = encoding_token(current_user['u_id'])
    data['active_tokens'].append(token)
    return {
        'u_id': current_user['u_id'],
        'token': encoding_token(current_user['u_id']),
    }

def auth_logout(token):
    if token in data['active_tokens']:
        # Invalidate the token
        data['active_tokens'].remove(token)
        return {'is_success' : True}
    return {'is_success' : False}

def auth_register(email, password, name_first, name_last):
    # Creating a dcitionoary to append to the data
    new_account = {}
    # Email Validation
    if not email_validation(email):
        raise InputError("Error, email is invalid")
    # Check if the email is taken by another account
    duplicate_flag = True
    for user in data['users']:
        if user['email'] == email:
            duplicate_flag = False
            break
    if not duplicate_flag:
        raise InputError("Error, email has been taken ")
    new_account['email'] = email

    # Password Validation
    # Password has to be more than or equal to 6 characters
    if len(password) < 6:
        raise InputError("Error, password need to be more than 5 characters")
    new_account['password'] = encoding_password(password)
    # First and Last Name Validation
    # Names should be between 1 and 50 characters
    if (1 <= len(name_first) <= 50) and (1 <= len(name_last) <= 50):
        new_account['name_first'] = name_first
        new_account['name_last'] = name_last
    else:
        raise InputError("Error, name should be betwwen 1 and 50 characters")

    # Generating the ID
    user_id = 1
    for user in data['users']:
        user_id += 1
    new_account['u_id'] = user_id

    # Generating a handle
    handle = name_first + name_last
    if len(handle) > 20:
        handle = handle[0:20]
    # If a handle is already taken, to make it unique use date and time
    handle_duplicate = False
    for user in data['users']:
        if user['handle_str'] == handle:
            handle_duplicate = True
            break
    if handle_duplicate:
        handle = handle[0:8]
        dt_string = datetime.now().strftime("%d%m%y%H%M%S")
        handle = handle + dt_string
    new_account['handle_str'] = handle

    # Defaukt permission
    if new_account['u_id'] == 1:
        new_account['permission'] = 1
    else:
        new_account['permission'] = 2

    # Appending the new user to the data
    data['users'].append(new_account)

    # Generating, Storing, Encoding the Token
    token = encoding_token(user_id)
    data['active_tokens'].append(token)
    return {
        'u_id': user_id,
        'token': token,
    }

def auth_passwordreset_request(email):
    #Check if the email has been registered
    valid_email = False
    for user in data['users']:
        if user['email'] == email:
            current_user = user
            valid_email = True
            break
    if valid_email == False:
        raise InputError("Email do not exits")

    #Generate the code with 6 characters
    len_code = 6
    code = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k = len_code))
    data['reset_code'].append({'code': code, 'u_id': current_user['u_id']})

    #Initialixing the server + sending the email
    port = 465  # For SSL
    sender_email = "flockgrape1@gmail.com" # dummy email
    receiver_email = email  
    password = 'flockgrape1best'
    message = f"""\
    Subject: Password Reset Request

    To reset your paswword, please enter the number below
    {code}
    """
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    return {}

def auth_passwordreset_reset(reset_code, new_password):
    #Check if the code is valid
    valid_code = False
    for code_dict in data['reset_code']:
        if code_dict['code'] == reset_code:
            user = get_user(code_dict['u_id'])
            data['reset_code'].remove(code_dict)
            valid_code = True
            break
    if valid_code == False:
        raise InputError("Code is invalid")
    # Padssword validation
    # Password has to be more than or equal to 6 characters
    if len(new_password) < 6:
        raise InputError("Error, password need to be more than 5 characters")
    user['password'] = encoding_password(new_password)
    return {}