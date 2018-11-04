import requests
import json
import urllib
from datetime import datetime
import pytz

TSHEETS_URL = 'https://rest.tsheets.com/api/v1'
TSHEETS_KEY = 'S.7__451415bf1afd3d22321e4eeaee72c3c37d398063'

def get_users():
    tsheets = requests.get(TSHEETS_URL).content
    headers = {
        'Authorization': "Bearer "+TSHEETS_KEY,
    }
    response = requests.request("GET", TSHEETS_URL+'/users', headers=headers)
    resDict = json.loads(response)[0]
    return resDict['results']['users']

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
    resDict = dict(json.loads(response.text))
    return resDict.get('results', {}).get('groups', {})

def get_group_users(id):
    tsheets = requests.get(TSHEETS_URL).content
    headers = {
        'Authorization': "Bearer "+TSHEETS_KEY,
    }
    response = requests.request("GET", TSHEETS_URL+'/users?group_ids=' + str(id), headers=headers)
    resDict = dict(json.loads(response.text))
    return resDict.get('results', {}).get('users', {})

def get_group_schedule_events(start_ts, ids):
    tsheets = requests.get(TSHEETS_URL).content
    headers = {
        'Authorization': "Bearer "+TSHEETS_KEY,
    }
    tz = pytz.timezone('America/Los_Angeles')
    start_date = datetime.fromtimestamp(start_ts, tz).isoformat()
    calendar_id = 83765
    params = urllib.urlencode({"start": start_date, "schedule_calendar_ids": calendar_id}) + "&user_ids={}".format(ids)+"&active=yes"
    #params = urllib.quote_plus("start={}&schedule_calendar_ids={}&ids={}".format(start_date, calendar_id, ids))
    print params
    response = requests.request("GET", TSHEETS_URL+'/schedule_events?' + params, headers=headers)
    #return response
    resDict = dict(json.loads(response.text))
    return resDict.get('results', {}).get('schedule_events', {})

