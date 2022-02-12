import pytest
from auth import auth_login, auth_register, auth_logout
from error import InputError
from other import clear

def test_successful_login():
    clear()
    # Sample data
    email = 'validemail1@gmail.com'
    password = 'validpassword'
    first_name = 'John'
    last_name = 'Lennon'
    user = auth_register(email, password, first_name, last_name)
    auth_logout(user['token'])
    user = auth_login(email, password)
    assert auth_logout(user['token'])['is_success']

def test_email_not_registered():
    clear()
    
    email = 'validemail1@gmail.com'
    password = 'validpassword'
    # Expected to fail, since none is registered
    with pytest.raises(InputError):
        auth_login(email, password)

    # Sample data
    email = 'validemail1@gmail.com'
    password = 'validpassword'
    first_name = 'John'
    last_name = 'Lennon'
    auth_register(email, password, first_name, last_name)
    
    # Expected to fail, some sample data in the storage, but login with un-registered email
    email = 'unregisteredemail1@gmail.com'
    password = 'validpassword'
    with pytest.raises(InputError):
        auth_login(email, password)

def test_invalid_password():
    clear()

    # Sample data
    email = 'validemail1@gmail.com'
    password = 'validpassword'
    first_name = 'John'
    last_name = 'Lennon'
    auth_register(email, password, first_name, last_name)

    # LOGIN with incorrect password
    password = 'incorrectpassword'
    with pytest.raises(InputError):
        auth_login(email, password)

def test_multiple_login():
    clear()

    # Sample data
    email = 'validemail1@gmail.com'
    password = 'validpassword'
    first_name = 'John'
    last_name = 'Lennon'
    auth_register(email, password, first_name, last_name)

    # 1st Attempt of LOGIN
    auth_login(email, password)
    #2nd attempt of LOGIN (Expected to Success)
    user = auth_login(email, password)
    assert auth_logout(user['token'])['is_success']

def test_invald_email():
    clear()

    # Samples of Invalid Email
    email1 = 'invalidemailsample.com'
    password1 = 'invalidpassword1'

    email2 = '@invalidemailsample.com'
    password2 = 'password2'

    email3 = 'invalid.email@.com'
    password3 = 'password3'

    email4 = 'invalid.email@domain'
    password4 = 'password4'

    with pytest.raises(InputError):
        auth_login(email1, password1)
    with pytest.raises(InputError):
        auth_login(email2, password2)
    with pytest.raises(InputError):
        auth_login(email3, password3)
    with pytest.raises(InputError):
        auth_login(email4, password4)

def test_appeding_token():
    clear()
    # Sample data
    email = 'validemail1@gmail.com'
    password = 'validpassword'
    first_name = 'John'
    last_name = 'Lennon'
    auth_register(email, password, first_name, last_name)
    user1 = auth_login(email, password)
    auth_logout(user1['token'])
    # The same user LOGIN
    user = auth_login(email, password)
    assert auth_logout(user['token'])['is_success']
