from other import clear
from auth import auth_register
from error import *
from user import user_profile, user_profile_setemail
import pytest


def test_successful_setemail():
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
    # Set email for user1
    user_profile_setemail(user1['token'], 'newvalidemail1@gmail.com')
    profile1 = user_profile(user1['token'], user1['u_id'])
    assert profile1['user']['email'] == 'newvalidemail1@gmail.com'
    # Set email for user2
    user_profile_setemail(user2['token'], 'newvalidemail2@gmail.com')
    profile2 = user_profile(user2['token'], user2['u_id'])
    assert profile2['user']['email'] == 'newvalidemail2@gmail.com'
    # Check to see that user1'email did not change
    assert profile1['user']['email'] == 'newvalidemail1@gmail.com'

def test_invalid_email():
    clear()
    # Initial Data
    email = 'validemail1@gmail.com'
    password = 'validpassword1'
    first_name = 'John'
    last_name = 'Lennon'
    user1 = auth_register(email, password, first_name, last_name)
    # Samples of Invalid Email
    email1 = 'invalidemailsample.com'
    email2 = '@invalidemailsample.com'
    email3 = 'invalid.email@.com'
    email4 = 'invalid.email@domain'
    # Set email with invalid emails, Excpected to FAILED
    with pytest.raises(InputError):
        user_profile_setemail(user1['token'], email1)
    with pytest.raises(InputError):
        user_profile_setemail(user1['token'], email2)
    with pytest.raises(InputError):
        user_profile_setemail(user1['token'], email3)
    with pytest.raises(InputError):
        user_profile_setemail(user1['token'], email4)

def test_same_email():
    clear()
    # Initial Data
    email1 = 'validemail1@gmail.com'
    password1 = 'validpassword1'
    first_name1 = 'John'
    last_name1 = 'Lennon'
    auth_register(email1, password1, first_name1, last_name1)
    email2 = 'validemail2@gmail.com'
    password2 = 'validpassword2'
    first_name2 = 'Bill'
    last_name2 = 'Gates'
    user2 = auth_register(email2, password2, first_name2, last_name2)
    # Set email for user2 to user1's email, expected to FAILED
    with pytest.raises(InputError):
        user_profile_setemail(user2['token'], email1)
   
def test_invalid_token():
    clear()
    # Initial Data
    email = 'validemail1@gmail.com'
    password = 'validpassword1'
    first_name = 'John'
    last_name = 'Lennon'
    auth_register(email, password, first_name, last_name)
    
    # Set token with invalid token, Excpected to FAILED
    with pytest.raises(AccessError):
        user_profile_setemail(12345, 'validemail2@gmail.com')