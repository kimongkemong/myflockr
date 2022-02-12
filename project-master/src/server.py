import sys
from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from error import InputError
from message import message_send, message_remove, message_react, message_unreact, message_sendlater
from channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner
from user import user_profile_setemail, user_profile_sethandle, user_profile, user_profile_setname, user_profile_uploadphoto
from auth import auth_login, auth_logout, auth_register, auth_passwordreset_request, auth_passwordreset_reset
from message import message_edit, message_pin, message_unpin
from channels import channels_create, channels_list, channels_listall
from other import search, clear, admin_userpermission_change, users_all
from standup import standup_start, standup_send, standup_active

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

########################################### AUTH FEATURES ###############################################
@APP.route("/auth/register", methods=['POST'])
def auth_register_flask():
    payload = request.get_json()
    user1 = auth_register(payload['email'], payload['password'], payload['name_first'], payload['name_last'])
    return dumps({
        'u_id' : user1['u_id'],
        'token' : user1['token'],
    })

@APP.route("/auth/login", methods=['POST'])
def auth_login_flask():
    payload = request.get_json()
    return dumps(auth_login(payload['email'], payload['password']))

@APP.route("/auth/logout", methods=['POST'])
def auth_logout_flask():
    payload = request.get_json()
    return dumps(auth_logout(payload['token']))

@APP.route("/auth/passwordreset/request", methods=['POST'])
def auth_request_flask():
    payload = request.get_json()
    return dumps(auth_passwordreset_request(payload['email']))

@APP.route("/auth/passwordreset/reset", methods=['POST'])
def auth_reset_flask():
    payload = request.get_json()
    return dumps(auth_passwordreset_reset(payload['reset_code'], payload['new_password']))


################################################# USER FEATURES #############################################
@APP.route("/user/profile/sethandle", methods=['PUT'])
def set_handle():
    payload = request.get_json()
    return dumps(user_profile_sethandle(payload['token'], payload['handle_str']))

@APP.route("/user/profile/setemail", methods=['PUT'])
def set_email():
    payload = request.get_json()
    return dumps(user_profile_setemail(payload['token'], payload['email']))

@APP.route("/user/profile", methods=['GET'])
def user_profile_flask():
    data_token = request.args.get('token')
    data_uid = int(request.args.get('u_id'))
    profile_data = user_profile(data_token, data_uid)
    return dumps(profile_data)

@APP.route("/user/profile/setname", methods=['PUT'])
def set_name():
    payload = request.get_json()
    return dumps(user_profile_setname(payload['token'], payload['name_first'], payload['name_last']))
########################################### MESSAGE FEATURES ###############################################

@APP.route("/message/send", methods=['POST'])
def message_send_flask():
    payload = request.get_json()
    return dumps(message_send(payload['token'], int(payload['channel_id']), payload['message']))

@APP.route("/message/remove", methods=['DELETE'])
def message_remove_flask():
    payload = request.get_json()
    return dumps(message_remove(payload['token'], payload['message_id']))


@APP.route("/message/edit", methods=['PUT'])
def message_edit_flask():
    payload = request.get_json()
    msg_edit = message_edit(payload['token'], payload['message_id'], payload['message'])
    return dumps(msg_edit)


@APP.route("/message/react", methods = ['POST'])
def message_react_flask():
    payload = request.get_json()
    return dumps(message_react(payload['token'], payload['message_id'], payload['react_id']))


@APP.route("/message/unreact", methods = ['POST'])
def message_unreact_flask():
    payload = request.get_json()
    return dumps(message_unreact(payload['token'], payload['message_id'], payload['react_id']))

@APP.route("/message/sendlater", methods = ['POST'])
def message_sendlater_flask():
    payload = request.get_json()
    return dumps(message_sendlater(payload['token'], payload['channel_id'], payload['message'], payload['time_sent']))
@APP.route("/message/pin", methods = ['POST'])
def message_pin_flask():
    payload = request.get_json()
    message_pin(payload['token'], payload['message_id'])
    return dumps({})

@APP.route("/message/unpin", methods = ['POST'])
def message_unpin_flask():
    payload = request.get_json()
    message_unpin(payload['token'], payload['message_id'])
    return dumps({})

################################################# OTHER FEATURES ###########################################
@APP.route("/clear", methods=['DELETE'])
def clear_data():
    clear()
    return {}

@APP.route("/admin/userpermission/change", methods=['POST'])
def user_permission_change():
    payload = request.get_json()
    return dumps(admin_userpermission_change(payload['token'], payload['u_id'], payload['permission_id']))

@APP.route("/users/all", methods = ["GET"])
def users_all_flask():
    data_token = request.args.get('token')
    return dumps(users_all(data_token))

@APP.route("/search", methods=['GET'])
def search_flask():
    data_token = request.args.get('token')
    query_string = request.args.get('query_str')
    found = search(data_token,query_string)
    return dumps(found)

############################################## CHANNEL FEATURES #############################################
@APP.route("/channel/invite", methods=['POST'])
def channel_invite_flask():
    payload = request.get_json()
    channel_invite(payload['token'], int(payload['channel_id']), payload['u_id'])
    return {}

@APP.route("/channel/join", methods=['POST'])
def channel_join_flask():
    payload = request.get_json()
    channel_join(payload['token'], int(payload['channel_id']))
    return {}

@APP.route("/channel/leave", methods=['POST'])
def channel_leave_flask():
    payload = request.get_json()
    channel_leave(payload['token'], int(payload['channel_id']))
    return {}

@APP.route("/channel/details", methods=['GET'])
def channel_details_flask():
    data_token = request.args.get('token')
    data_channel_id = int(request.args.get('channel_id'))
    detail_data = channel_details(data_token, data_channel_id)
    return dumps(detail_data)

@APP.route("/channel/addowner", methods = ['POST'])
def channel_addowner_flask():
    payload = request.get_json()
    channel_addowner(payload['token'], int(payload['channel_id']), payload['u_id'])
    return {}

@APP.route("/channel/removeowner", methods = ['POST'])
def channel_removeowner_flask():
    payload = request.get_json()
    channel_removeowner(payload['token'], int(payload['channel_id']), payload['u_id'])
    return {}

@APP.route("/channel/messages", methods=['GET'])
def channel_messages_flask():
    data_token = request.args.get('token')
    data_channel_id = int(request.args.get('channel_id'))
    data_start = int(request.args.get('start'))
    return dumps(channel_messages(data_token, data_channel_id, data_start))


############################################# CHANNELS FEATURES ############################################
@APP.route("/channels/create", methods=['POST'])
def channels_create_flask():
    payload = request.get_json()
    ch_id = channels_create(payload['token'], payload['name'], payload['is_public'])
    return dumps(ch_id)

@APP.route("/channels/listall", methods=['GET'])
def channels_listall_flask():
    data_token = request.args.get('token')
    all_ch = channels_listall(data_token)
    return dumps(all_ch)

@APP.route("/channels/list", methods=['GET'])
def channels_list_flask():
    data_token = request.args.get('token')
    ch_list = channels_list(data_token)
    return dumps(ch_list)

############################################## PROFILE PICTURE FEATURES #############################################

@APP.route("/user/profile/uploadphoto", methods=['POST'])
def user_uploadphoto():
    payload = request.get_json()
    return(user_profile_uploadphoto(payload['token'], payload['img_url'], payload['x_start'], payload['y_start'], payload['x_end'], payload['y_end']))

@APP.route('/static/<path:path>')
def send_picture(path):
    return send_from_directory('/static/', path)

######################################## STANDUP FEATURES #################################################
@APP.route("/standup/start", methods=['POST'])  
def standup_start_flask():
    payload = request.get_json()
    standup = standup_start(payload['token'], payload['channel_id'], payload['length'])
    return dumps(standup)

@APP.route("/standup/send", methods=['POST'])
def standup_send_flask():
    payload = request.get_json()
    standup_send(payload['token'], payload['channel_id'], payload['message'])
    return {}

@APP.route("/standup/active", methods=['GET'])
def standup_active_flask():
    data_token = request.args.get('token')
    data_channel_id = int(request.args.get('channel_id'))
    active = standup_active(data_token, data_channel_id)
    return dumps(active)

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
