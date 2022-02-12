import data as d
import imghdr
import urllib.request
# from PIL import Image
from error import InputError, AccessError
import urllib.request
import requests
import imghdr
from PIL import Image
import flask

#return the details of the user
def user_profile(token, u_id):

    #if token is invalid, then the func raise an AccessError
    if not d.validate_token(token):
        raise AccessError ("invalid token!")

    else:

        #user the helper func in data.py to get user info
        user = d.get_user(u_id)

        #create an empty dictionary
        profile = dict()

        #If the user can't be found, raise InputError
        if user['u_id'] == -1:
            raise InputError ("invalid u_id!")

        else:

            #match each attributes between profile and user
            profile['u_id'] = user['u_id']
            profile['email'] = user['email']
            profile['name_first'] = user['name_first']
            profile['name_last'] = user['name_last']
            profile['handle_str'] = user['handle_str']

            #If the user has uploaded an image, then we add it
            if 'profile_img_url' in user.keys():
                profile['profile_img_url'] = user['profile_img_url']

            #Otherwise just set its url to be empty.
            else:
                profile['profile_img_url'] = ""
            return {'user':profile}

def user_profile_setname(token, name_first, name_last):
    '''Changing first and last name of authorised'''
    #Checking token
    check_token = d.validate_token(token)
    if check_token is False:
        raise AccessError("Error! Unauthorized Action")

    #Checking for the length of the name
    if len(name_first) == 0 or len(name_last) == 0:
        raise InputError("Name cannot be empty!") 
    if len(name_first) > 50 or len(name_last) > 50:
        raise InputError("Name cannot exceed 50 characters!")

    #GO through the dictionary to find the authorised user
    user_id = d.decoding_token(token)
    for user in d.data['users']:
        if user_id == user['u_id']:
            user['name_first'] = name_first
            user['name_last'] = name_last

    return {}

def user_profile_setemail(token, email):
    # Token Validation
    if d.validate_token(token):
        # Email Validation
        if not d.email_validation(email):
            raise InputError("Error, email is invalid")
        # Check if the email is taken by another account
        duplicate_flag = False
        for user in d.data['users']:
            if user['u_id'] != d.decoding_token(token) and user['email'] == email:
                duplicate_flag = True
                break
        if duplicate_flag:
            raise InputError("Error, email has been taken ")

        # Decoding the token to user_id
        user_id = d.decoding_token(token)

        # Modifying the Handle
        for user in d.data['users']:
            if user_id == user['u_id']:
                user['email'] = email
        return {}
    else:
        raise AccessError ("invalid token!")

def user_profile_sethandle(token, handle_str):
    # Token Validation
    if d.validate_token(token):
        # Handle Validation
        length_flag = False
        duplicate_flag = False
        if 3 <= len(handle_str) <= 20:
            length_flag == True
        else:
            raise InputError("Error, handle should be betwwen 3 and 20 characters")
        for user in d.data['users']:
            if user['u_id'] != d.decoding_token(token) and user['handle_str'] == handle_str:
                duplicate_flag == True
                raise InputError("Error, handle is taken")

        # Decoding the token to user_id
        user_id = d.decoding_token(token)

        # Modifying the Handle
        for user in d.data['users']:
            if user_id == user['u_id']:
                user['handle_str'] = handle_str

        return {}
    else:
        raise AccessError ("invalid token!")

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    #Checking token
    check_token = d.validate_token(token)
    if check_token is False:
        raise AccessError("Error! Unauthorized Action, Invalid Token")

    user_id = d.decoding_token(token)
    
    #Check if the HTTP return codes other than 200
    respond = requests.get(img_url)
    status = respond.status_code
    if status != 200:
        raise InputError("Error in Image Url")
    # Take the pic
    urllib.request.urlretrieve(img_url, "src/static/profilepic.jpg")
    jpg_extension = ['jpg', 'jpeg']
    
    #Check if the image is in .jpg extensions file
    type_file = imghdr.what("src/static/profilepic.jpg")
    if type_file not in jpg_extension:
        raise InputError("Error! Image must be .jpg extentions file")

    #Check if the coordinate is within the dimension
    image = Image.open("src/static/profilepic.jpg")
    width, height = image.size
    if x_start not in range(0,width) or x_end not in range(0,width):
        raise InputError("Error! Size extend the dimension of image")
    if y_start not in range(0,height) or y_end not in range(0,height):
        raise InputError("Error! Size extend the dimension of image")

    #Cropping the image
    cropped_image = image.crop((x_start, y_start, x_end, y_end))
    cropped_image.save(f"src/static/cropped{user_id}.jpg")

    #Set the profile_url
    for user in d.data['users']:
        if user_id == user['u_id']:
            user['profile_img_url'] = flask.request.host_url+f"static/cropped{user_id}.jpg"
    return {}
