import pytest
from auth import auth_register, auth_logout
from other import clear
from error import InputError

def test_success_register():
    clear()

    # Sample data
    email = 'validemail1@gmail.com'
    password = 'validpassword'
    first_name = 'John'
    last_name = 'Lennon'

    # Expected to Success
    user = auth_register(email, password, first_name, last_name)
    assert auth_logout(user['token'])['is_success']

def test_unique_token_or_id():
    clear()

    # Sample data
    email = 'validemail1@gmail.com'
    password = 'validpassword'
    first_name = 'John'
    last_name = 'Lennon'
    email2 = 'validemail2@gmail.com'
    password2 = 'validpassword2'
    first_name2 = 'John'
    last_name2 = 'Lennon'

    user1 = auth_register(email, password, first_name, last_name)
    user2 = auth_register(email2, password2, first_name2, last_name2)

    # Testing to check if the tokens given are unique
    assert user1['token'] != user2['token']

def test_invalid_email():
    clear()
    first_name = 'John'
    last_name = 'Lennon'

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
        auth_register(email1, password1, first_name, last_name)
    with pytest.raises(InputError):
        auth_register(email2, password2, first_name, last_name)
    with pytest.raises(InputError):
        auth_register(email3, password3, first_name, last_name)
    with pytest.raises(InputError):
        auth_register(email4, password4, first_name, last_name)

def test_same_email():
    clear()

    # Initial data
    email = 'validemail1@gmail.com'
    password = 'validpassword'
    first_name = 'John'
    last_name = 'Lennon'
    auth_register(email, password, first_name, last_name)

    #Registering with the same email (same data)
    email1 = 'validemail1@gmail.com'
    password1 = 'validpassword'
    first_name1 = 'John'
    last_name1 = 'Lennon'

    with pytest.raises(InputError):
        auth_register(email1, password1, first_name1, last_name1)

def test_short_password():
    clear()

    # Less than 6 letters of password
    email = 'validemail1@gmail.com'
    password = 'short'
    first_name = '12345'
    last_name = 'Lennon'

    with pytest.raises(InputError):
        auth_register(email, password, first_name, last_name)


def test_long_first_name():
    clear()

    # Maximum length of first name
    email = 'validemail1@gmail.com'
    password = 'validpassword'
    first_name = 'J' * 50
    last_name = 'Lennon'

    # Should be succesfull
    auth_register(email, password, first_name, last_name)

    clear()

    # Exceeding the maximum length of first name
    email = 'validemail1@gmail.com'
    password = 'validpassword'
    first_name = 'J' * 51
    last_name = 'Lennon'

    # Should raise an exception
    with pytest.raises(InputError):
        auth_register(email, password, first_name, last_name)


def test_long_last_name():
    clear()

    # Maximum length of last name
    email = 'validemail1@gmail.com'
    password = 'validpassword'
    first_name = 'John'
    last_name = 'L' * 50

    # Should return the user_id as well as token
    auth_register(email, password, first_name, last_name)

    clear()

    # Exceeding the maximum length of last name
    email = 'validemail1@gmail.com'
    password = 'validpassword'
    first_name = 'John'
    last_name = 'L' * 51

    # Should raise an exception
    with pytest.raises(InputError):
        auth_register(email, password, first_name, last_name)
