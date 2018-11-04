from utils import tsheets
from utils import nexmo_utils
from datetime import datetime
import time
import dateutil.parser as dp

class CoverImplementer(object):

    cover_message = "Hey {}, need cover from {} on {} to {} on {}. Can you take the time?"

    def validate_list_not_empty(self, d, code):
        if d == None or len(d) == 0:
            raise Exception(code)


    def cover_shifts(self, start, end, group_name):
        shift_start = time.mktime(datetime.strptime(start, "%m/%d/%Y %H:%M").timetuple())
        shift_end = time.mktime(datetime.strptime(end, "%m/%d/%Y %H:%M").timetuple())
        # find the groups
        groups = tsheets.get_group(0)
        self.validate_list_not_empty(groups, "no_group")

        #print(groups)
        group = None
        for (gid,g) in groups.items():
            #print(gid)
            if g.get('name') == group_name:
                group = g
                break
        #print(group)
        group_id = group['id']
        # get all workers who can cover the shift
        group_users = tsheets.get_group_users(group_id)
        self.validate_list_not_empty(group_users, "no_group_users")

        group_user_ids_concat = ','.join([u for u in group_users.keys()])
        start_ts = time.mktime(datetime.strptime(datetime.fromtimestamp(shift_start - 1).strftime('%m-%d-%Y'), '%m-%d-%Y').timetuple())
        group_user_schedule_events = tsheets.get_group_schedule_events(start_ts, group_user_ids_concat)
        if group_user_schedule_events == None or len(group_user_schedule_events) == 0:
            #no one in the group is working, we can see if group has users and send to all
            print("no scheduled events for groups members")
            self.notify_users_for_open_slot(shift_start, shift_end, group_users)
            return "success"

        ## get workers with conflicting timesheets
        conflicting_users = {}
        for se_id in group_user_schedule_events:
            se = group_user_schedule_events[se_id]
            if self.is_conflicting_schedule(shift_start, shift_end, se):
                conflicting_users[str(se['user_id'])] = 1

        ## remove workers who are already doing a shift at that time
        filtered_users = {}
        for id in group_users:
            if conflicting_users.get(id, None) == None:
                filtered_users[id] = group_users[id]
            
        self.notify_users_for_open_slot(shift_start, shift_end, filtered_users)
        return "success"

    def notify_users_for_open_slot(self, start, end, users):
        ## get the phone numbers of remaining workers
        for user_id in users:
            user = users.get(user_id)
            ## use the nexmo client to send text to these workers
            to_ph = user.get('mobile_number')
            to_name = ' '.join([user.get('first_name'), user.get('last_name')])
            #print("User id {}".format(user_id))
            print("Sending text to {} at {}".format(to_name, to_ph))
            start_date = datetime.fromtimestamp(start).strftime('%m-%d-%Y')
            start_time = datetime.fromtimestamp(start).strftime('%H:%M')
            end_date = datetime.fromtimestamp(end).strftime('%m-%d-%Y')
            end_time = datetime.fromtimestamp(end).strftime('%H:%M')
            nexmo_utils.send(to_ph, self.cover_message.format(to_name, start_time, start_date, end_time, end_date)) 

        # send notification to all the remaining workers

    def is_conflicting_schedule(self, start, end, se):
        se_start_parsed = dp.parse(se['start']) 
        se_start = int(se_start_parsed.strftime('%s'))
        se_end_parsed = dp.parse(se['end']) 
        se_end = int(se_end_parsed.strftime('%s'))
        return ((se_start > start and se_start < end) or (se_end > start and se_end < end) or (start > se_start and start < se_end) or (end > se_start and end < se_end))
