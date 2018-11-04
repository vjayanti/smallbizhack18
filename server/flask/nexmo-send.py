import nexmo

client = nexmo.Client(key='ca6e9479', secret='lk7KwSsU7xw6tBm6')

response = client.send_message({
    'from': '15752525166',
    'to': '15105857152', # rented phone number
    'text': 'Hello from Nexmo',
})

print(response['messages'][0])
print(response['messages'][0]['status'])
print(response)