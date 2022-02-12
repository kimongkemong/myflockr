from other import clear
from auth import auth_register
from error import *
from user import user_profile, user_profile_uploadphoto
import pytest
#Cannot test the functionality of the code since it need flask running behind it

# Check if the token is valid or not
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
        user_profile_uploadphoto(12345, 'https://tinyjpg.com/images/social/website.jpg',0,0,200,200)

# Check if the url is valid or not
def test_invalid_url():
    clear()
    # Initial Data
    email = 'validemail1@gmail.com'
    password = 'validpassword1'
    first_name = 'John'
    last_name = 'Lennon'
    user1 = auth_register(email, password, first_name, last_name)
    
    # Set token with invalid url, Excpected to FAILED
    with pytest.raises(InputError):
        user_profile_uploadphoto(user1['token'], 'https://tinyjpg.com/images/social/.jpg',0,0,200,200)

# Check if the size is valid or not 
def test_invalid_size():
    clear()
    # Initial Data
    email = 'validemail1@gmail.com'
    password = 'validpassword1'
    first_name = 'John'
    last_name = 'Lennon'
    user1 = auth_register(email, password, first_name, last_name)
    b_num = 999999999
    
    # Set sizes with invalid sizes, Excpected to FAILED
    with pytest.raises(InputError):
        user_profile_uploadphoto(user1['token'], 'https://tinyjpg.com/images/social/website.jpg',-1,-1,-100000000,-100000000)
        user_profile_uploadphoto(user1['token'], 'https://tinyjpg.com/images/social/website.jpg',0,0,b_num,b_num)

# Check if the url is a jpg or not
def test_invalid_jpg():
    clear()
    # Initial Data
    email = 'validemail1@gmail.com'
    password = 'validpassword1'
    first_name = 'John'
    last_name = 'Lennon'
    user1 = auth_register(email, password, first_name, last_name)
    
    # Set url with .gif url, Excpected to FAILED
    with pytest.raises(InputError):
        user_profile_uploadphoto(user1['token'], 'https://compote.slate.com/images/697b023b-64a5-49a0-8059-27b963453fb1.gif',0,0,200,200)