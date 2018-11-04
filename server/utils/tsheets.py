import requests
TSHEETS_URL = 'https://rest.tsheets.com/api/v1'
TSHEETS_KEY = 'S.7__451415bf1afd3d22321e4eeaee72c3c37d398063'

def get_users():
    tsheets = requests.get(TSHEETS_URL).content
    headers = {
        'Authorization': "Bearer "+TSHEETS_KEY,
    }
    response = requests.request("GET", TSHEETS_URL+'/users', headers=headers)
    print(response.text)
    return response.text

def verify_schedules(requester_id, requested_id, time):
    tsheets = requests.get(TSHEETS_URL).content
    headers = {
        'Authorization': "Bearer "+TSHEETS_KEY,
    }
    requester_schedule = requests.request("GET", TSHEETS_URL+'/timesheets?user_ids='+ str(requester_id) + 'start_date' + str(time), headers=headers)
    requested_schedule = requests.request("GET", TSHEETS_URL+'/timesheets?user_ids='+ str(requested_id) + 'start_date' + str(time), headers=headers)
    requester_has_timesheet = len(requester_schedule['results'].keys()) > 0
    requested_has_timesheet_available = len(requested_schedule['results'].keys()) == 0
    if requester_has_timesheet and requested_has_timesheet_available:
        return True
    return False

def get_group(id):
    tsheets = requests.get(TSHEETS_URL).content
    headers = {
        'Authorization': "Bearer "+TSHEETS_KEY,
    }
    response = requests.request("GET", TSHEETS_URL+'/groups?ids=' + str(id), headers=headers)
    print(response.text)
    return response['results']['groups']

def get_group_users(id):
    tsheets = requests.get(TSHEETS_URL).content
    headers = {
        'Authorization': "Bearer "+TSHEETS_KEY,
    }
    response = requests.request("GET", TSHEETS_URL+'/users?group_ids=' + str(id), headers=headers)
    print(response.text)
    return response['results']

def get_group_timesheet(id):
    tsheets = requests.get(TSHEETS_URL).content
    headers = {
        'Authorization': "Bearer "+TSHEETS_KEY,
    }
    response = requests.request("GET", TSHEETS_URL+'/timesheets?group_ids=' + str(id), headers=headers)
    print(response.text)
    return response['results']


