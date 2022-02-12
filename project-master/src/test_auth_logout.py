from auth import auth_login, auth_register, auth_logout
from other import clear

def test_valid_token():
    clear()

    # Sample data
    email = 'validemail1@gmail.com'
    password = 'validpassword'
    first_name = 'John'
    last_name = 'Lennon'
    user = auth_register(email, password, first_name, last_name)
    assert auth_logout(user['token'])['is_success']

def test_invalid_token():
    clear()

    # Sample data
    email = 'validemail1@gmail.com'
    password = 'validpassword'
    first_name = 'John'
    last_name = 'Lennon'
    auth_register(email, password, first_name, last_name)
    assert not auth_logout(12345)['is_success']

def test_invalidate_token():
    clear()

    # Sample data
    email = 'validemail1@gmail.com'
    password = 'validpassword'
    first_name = 'John'
    last_name = 'Lennon'
    user = auth_register(email, password, first_name, last_name)

    assert auth_logout(user['token'])['is_success']
    #2nd Logout (Expected to fail)
    assert not auth_logout(user['token'])['is_success']

    # One user Login via multiple devices
    user1 = auth_login(email, password)
    user1 = auth_login(email, password)
    assert auth_logout(user1['token'])['is_success']
    assert auth_logout(user1['token'])['is_success']
