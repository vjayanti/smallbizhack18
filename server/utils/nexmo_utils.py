import nexmo
client = nexmo.Client(key='ca6e9479', secret='lk7KwSsU7xw6tBm6')

def send(to, message):
    response = client.send_message({'from': '15752525166', 'to': '1' + to, 'text': message})
    print(response)
