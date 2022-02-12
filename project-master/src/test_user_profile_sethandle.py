from other import clear
from auth import auth_register
from error import *
from user import user_profile, user_profile_sethandle
import pytest


def test_successful_sethandle():
    clear()
    # Initial Data
    email1 = 'validemail1@gmail.com'
    password1 = 'validpassword1'
    first_name1 = 'John'
    last_name1 = 'Lennon'
    user1 = auth_register(email1, password1, first_name1, last_name1)
    email2 = 'validemail2@gmail.com'
    password2 = 'validpassword2'
    first_name2 = 'Bill'
    last_name2 = 'Gates'
    user2 = auth_register(email2, password2, first_name2, last_name2)
    # Set handle for user1
    user_profile_sethandle(user1['token'], 'JohnLennon2')
    profile1 = user_profile(user1['token'], user1['u_id'])
    assert profile1['user']['handle_str'] == 'JohnLennon2'
    # Set handle for user2
    user_profile_sethandle(user2['token'], 'BillGatess2')
    profile2 = user_profile(user2['token'], user2['u_id'])
    assert profile2['user']['handle_str'] == 'BillGatess2'
    # Check to see that user1'handle did not change
    assert profile1['user']['handle_str'] == 'JohnLennon2'

def test_short_handle():
    clear()
    # Initial Data
    email1 = 'validemail1@gmail.com'
    password1 = 'validpassword1'
    first_name1 = 'John'
    last_name1 = 'Lennon'
    user1 = auth_register(email1, password1, first_name1, last_name1)
    # Set handle for user1, Expected to FAILED
    with pytest.raises(InputError):
        user_profile_sethandle(user1['token'], 'ab')
    with pytest.raises(InputError):
        user_profile_sethandle(user1['token'], '1')
    with pytest.raises(InputError):
        user_profile_sethandle(user1['token'], 'a1')

def test_long_handle():
    clear()
    # Initial Data
    email1 = 'validemail1@gmail.com'
    password1 = 'validpassword1'
    first_name1 = 'John'
    last_name1 = 'Lennon'
    user1 = auth_register(email1, password1, first_name1, last_name1)
    # Set handle for user1, Expected to FAILED
    with pytest.raises(InputError):
        user_profile_sethandle(user1['token'], 'a' * 21)
    with pytest.raises(InputError):
        user_profile_sethandle(user1['token'], '1' * 50)

def test_same_handle():
    clear()
    # Initial Data
    email1 = 'validemail1@gmail.com'
    password1 = 'validpassword1'
    first_name1 = 'John'
    last_name1 = 'Lennon'
    user1 = auth_register(email1, password1, first_name1, last_name1)
    email2 = 'validemail2@gmail.com'
    password2 = 'validpassword2'
    first_name2 = 'Bill'
    last_name2 = 'Gates'
    user2 = auth_register(email2, password2, first_name2, last_name2)
    # Set handle for user1
    user_profile_sethandle(user1['token'], 'JohnLennon2')
    # Set handle for user2 to user1'handle, Expected to FAILED
    with pytest.raises(InputError):
        user_profile_sethandle(user2['token'], 'JohnLennon2')

def test_invalid_token():
    clear()
    # Initial Data
    email1 = 'validemail1@gmail.com'
    password1 = 'validpassword1'
    first_name1 = 'John'
    last_name1 = 'Lennon'
    auth_register(email1, password1, first_name1, last_name1)
    
    # Set handle for user1 with invalid token, Expected to failed
    with pytest.raises(AccessError):
        user_profile_sethandle(12345, 'JohnLennon2')
   