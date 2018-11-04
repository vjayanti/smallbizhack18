import requests
TSHEETS_URL = 'https://rest.tsheets.com/api/v1'
TSHEETS_KEY = 'S.7__451415bf1afd3d22321e4eeaee72c3c37d398063'

def get_users():
    headers = {
        'Authorization': "Bearer "+TSHEETS_KEY,
    }
    response = requests.request("GET", TSHEETS_URL+'/users', headers=headers)
    print(response.text)
    return response.text

def verify_schedules(old_time, new_time, requester_id, requested_id, time):
    headers = {
        'Authorization': "Bearer "+TSHEETS_KEY,
    }
    requester_schedule = requests.request("GET", TSHEETS_URL+'/timesheets?user_ids='+ str(requester_id) + 'start_date' + str(old_time), headers=headers)
    requester_new_schedule = requests.request("GET", TSHEETS_URL+'/timesheets?user_ids='+ str(requester_id) + 'start_date' + str(new_time), headers=headers)
    requested_schedule = requests.request("GET", TSHEETS_URL+'/timesheets?user_ids='+ str(requested_id) + 'start_date' + str(new_time), headers=headers)
    requested_new_schedule = requests.request("GET", TSHEETS_URL+'/timesheets?user_ids='+ str(requested_id) + 'start_date' + str(old_time), headers=headers)
    requester_is_ready = len(requester_schedule['results'].keys()) > 0 and len(requester_new_schedule['results'].keys()) == 0
    requested_is_ready = len(requested_schedule['results'].keys()) == 0 and len(requested_new_schedule['results'].keys()) > 0
    if requester_is_ready and requested_is_ready:
        return True
    return False

def get_group(id):
    headers = {
        'Authorization': "Bearer "+TSHEETS_KEY,
    }
    response = requests.request("GET", TSHEETS_URL+'/groups?ids=' + str(id), headers=headers)
    print(response.text)
    return response['results']['groups']

def get_group_users(id):
    headers = {
        'Authorization': "Bearer "+TSHEETS_KEY,
    }
    response = requests.request("GET", TSHEETS_URL+'/users?group_ids=' + str(id), headers=headers)
    print(response.text)
    return response['results']

def get_group_timesheet(id):
    headers = {
        'Authorization': "Bearer "+TSHEETS_KEY,
    }
    response = requests.request("GET", TSHEETS_URL+'/timesheets?group_ids=' + str(id), headers=headers)
    print(response.text)
    return response['results']


