import requests
import json
from urllib import urlencode
import dateutil.parser as parser
from dateutil.relativedelta import relativedelta

TSHEETS_URL = 'https://rest.tsheets.com/api/v1'
TSHEETS_KEY = 'S.7__451415bf1afd3d22321e4eeaee72c3c37d398063'

def get_users():
    headers = {
        'Authorization': "Bearer "+TSHEETS_KEY,
    }
    response = requests.request("GET", TSHEETS_URL+'/users', headers=headers)
    resDict = json.loads(response)[0]
    return resDict['results']['users']

def build_swap_url(endpoint, user_id, start_date):
    start = parser.parse(start_date)
    end = start+relativedelta(days=1)
    start = start.isoformat() + '+00:00'
    end = end.isoformat() + '+00:00'
    return (TSHEETS_URL+'/'+endpoint+'?'+
        urlencode({'user_ids': str(user_id),
                   'schedule_calendar_ids':'83765',
                   'active': 'yes',
                   'start': start,
                   'end': end})
            )

def verify_schedules(old_time, new_time, requester_id, requested_id):
    return True

    headers = {
        'Authorization': "Bearer "+TSHEETS_KEY,
    }
    requester_schedule = json.loads(requests.request("GET", build_swap_url('schedule_events', requester_id, old_time), headers=headers).content)
    requester_new_schedule = json.loads(requests.request("GET", build_swap_url('schedule_events', requester_id, new_time), headers=headers).content)
    requested_schedule = json.loads(requests.request("GET", build_swap_url('schedule_events', requested_id, new_time), headers=headers).content)
    requested_new_schedule = json.loads(requests.request("GET", build_swap_url('schedule_events', requested_id, old_time), headers=headers).content)
    requester_is_ready = len(requester_schedule['results']['schedule_events'].keys()) > 0 and len(requester_new_schedule['results'].keys()) == 0
    requested_is_ready = len(requested_schedule['results']['schedule_events'].keys()) == 0 and len(requested_new_schedule['results'].keys()) > 0
    if requester_is_ready and requested_is_ready:
        return True
    return False

def get_group(id):
    headers = {
        'Authorization': "Bearer "+TSHEETS_KEY,
    }
    response = requests.request("GET", TSHEETS_URL+'/groups?ids=' + str(id), headers=headers)
    resDict = dict(json.loads(response.text))
    return resDict.get('results', {}).get('groups', {})

def get_group_users(id):
    headers = {
        'Authorization': "Bearer "+TSHEETS_KEY,
    }
    response = requests.request("GET", TSHEETS_URL+'/users?group_ids=' + str(id), headers=headers)
    resDict = dict(json.loads(response.text))
    return resDict.get('results', {}).get('users', {})

def get_group_timesheets(id):
    tsheets = requests.get(TSHEETS_URL).content
    headers = {
        'Authorization': "Bearer "+TSHEETS_KEY,
    }
    response = requests.request("GET", TSHEETS_URL+'/timesheets?group_ids=' + str(id), headers=headers)
    resDict = dict(json.loads(response.text))
    return resDict.get('results', {}).get('timesheets', {})


