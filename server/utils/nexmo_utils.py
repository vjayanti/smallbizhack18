import nexmo

def send(to, message):
    client = nexmo.Client(key='ca6e9479', secret='Ik7KwSsU7xw6tBm6')

    client.send_message({
        'from': '15752525166', # rented phone number
        'to': to, 
        'text': message
    })
    return True
