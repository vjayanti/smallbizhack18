import nexmo
client = nexmo.Client(key='ca6e9479', secret='Ik7KwSsU7xw6tBm6')

def send(to, message):

    client.send_message({
        'from': '15752525166', # rented phone number
        'to': '1'+to,
        'text': message
    })
    return True
