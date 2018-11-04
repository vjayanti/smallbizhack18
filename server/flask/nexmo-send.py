import nexmo

client = nexmo.Client(key='###', secret='###')

client.send_message({
    'from': '15752525166',
    'to': '15752525166', # rented phone number
    'text': 'Hello from Nexmo',
})