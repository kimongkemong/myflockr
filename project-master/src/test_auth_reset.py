import pytest
from auth import auth_login, auth_register, auth_logout, auth_passwordreset_request, auth_passwordreset_reset
from error import InputError
from other import clear
#WHITE BOX TESTING
from data import data

# CANNOT TEST THE FUNCTIONALITY OF THESE FUNCTIONS

def test_invalid_email():
    #raise an error if the input email was not registered
    clear()
    # Sample data
    email = 'validemail@gmail.com'
    with pytest.raises(InputError):
        auth_passwordreset_request(email)
    
    # Sample data
    email = 'validemail1@gmail.com'
    password = 'validpassword'
    first_name = 'John'
    last_name = 'Lennon'
    auth_register(email, password, first_name, last_name)

    email = 'invalidemail@gmail.com'
    with pytest.raises(InputError):
        auth_passwordreset_request(email)

def test_invalid_code():
    #raise an error if the code was not valid
    clear()
    with pytest.raises(InputError):
        auth_passwordreset_reset('DUMMYCODE', 'DUMMYPASSWORD')


##############WHITE BOX TESTING###############
#Test the succesful of request and reset
def test_success_reset():
    clear()
    # Sample data
    email = 'validemail1@gmail.com'
    password = 'validpassword'
    first_name = 'John'
    last_name = 'Lennon'
    user = auth_register(email, password, first_name, last_name)
    assert auth_logout(user['token'])['is_success']
    auth_passwordreset_request(email)
    auth_passwordreset_reset(data['reset_code'][0]['code'],'newpassword')
    user = auth_login(email, 'newpassword')
    assert auth_logout(user['token'])['is_success']

def test_short_newpassword():
    clear()
    # Sample data
    email = 'validemail1@gmail.com'
    password = 'validpassword'
    first_name = 'John'
    last_name = 'Lennon'
    user = auth_register(email, password, first_name, last_name)
    assert auth_logout(user['token'])['is_success']
    auth_passwordreset_request(email)
    with pytest.raises(InputError):
        auth_passwordreset_reset(data['reset_code'][0]['code'],'short')
