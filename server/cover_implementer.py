from utils import tsheets
from utils import nexmo_utils

class CoverImplementer(object):

    cover_message = "Need cover for slot {1} - {2}"

    def validate_list_not_empty(self, l, code):
        if l == None or len(l) == 0:
            raise Exception(code)


    def cover_shifts(self, shift_start, shift_end, group_name):
        # find the groups
        group = next(iter(tsheets.get_group(group_name), None)
        self.validate_list_not_empty(group, "no_group")

        group_id = group['id']
        # get all workers who can cover the shift
        group_users = tsheets.get_group_users(group_id)
        self.validate_list_not_empty(group_users, "no_group_users")

        group_user_timesheets = tsheets.get_group_timesheets(group_id)
        if group_user_timesheets == None or len(groups_user_timesheets) == 0:
            #no one in the group is working, we can see if group has users and send to all
            self.notify_users_for_open_slot(shift_start, shift_end, group_users)

        ## get workers with conflicting timesheets
        conflicting_users = {}
        for ts in group_user_timesheets:
            if is_conflicting_timesheet(shift_start, shift_end, ts):
                conflicting_users[ts.user_id] = 1

        ## remove workers who are already doing a shift at that time
        filtered_users = filter(lambda u: conflicting_users.get(u.get('user_id'), 0) == 0, group_users)
            
        self.notify_users_for_open_slot(shift_start, shift_end, filtered_users)
        return "success"

    def notify_users_for_open_slot(start, end, users):
        ## get the phone numbers of remaining workers
        for user in users:
            ## use the nexmo client to send text to these workers
            nexmo-utils.send(user.get('mobile_number'), self.cover_message.format(start, end)) 

        # send notification to all the remaining workers

    def is_conflicting_timesheet(start, end, ts):
        return ((ts.start > start and ts.start < end) or (ts.end > start and ts.end < end))
            
