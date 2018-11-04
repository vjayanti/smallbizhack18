from server.utils.tsheets import verify_schedules

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
        # TODO: send api to swap_to
        
        pass

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
