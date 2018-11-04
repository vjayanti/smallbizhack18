from utils.tsheets import verify_schedules
from utils import nexmo_utils

class SwitchImplementer(object):
    def swap_shifts(self, old_time, new_time, from_person, to_person):
        # connect to tsheets
        # verify that both workers are available for said dates
        verified = verify_schedules(old_time, new_time, from_person, to_person)
        if verified:
            # send notification to worker from nexmo
            self.send_swap_request(old_time, new_time, from_person, to_person)
        else:
            self.fail_request(from_person)

    def send_swap_request(self, old_time, new_time, swap_from, swap_to):
        # get acknowledgement
        message = swap_from + ' is requesting a swap with ' + swap_to + ' from ' + old_time + ' to ' + new_time
        print('sending message')
        nexmo_utils.send('15105857152', message)
        return 'sent message'

    def handle_response(self, swap_agreed=True):
        if swap_agreed:
            # send notification to manager from nexmo for approval
            self.manager_confirmation()
        else:
            self.fail_request()

    def notify_status(self, status, *people_to_notify):
        for user in people_to_notify:
            #TODO: send api to people to notify
            #nexmorequest(user, status)
            pass
        pass

    def manager_confirmation(self, ):
        # once approved, make the swap
        #nexmo

        pass

    def handle_manager_response(self, old_time, new_time, from_person, to_person, swap_agreed=True):
        manager = 'jykim@gmail.com'
        if swap_agreed:
            self.tsheets_swap_shifts(old_time, new_time, from_person, to_person)
            self.notify_status(True, old_time, new_time, manager)
        else:
            self.notify_status(False, old_time, new_time, manager)

    def tsheets_swap_shifts(self):
        #Tsheets api
        pass

    def fail_request(self):
        return 'failed'
