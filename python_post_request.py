import requests

r = requests.post(
    "http://0.0.0.0:80/invocations",
    json={
        "id": 1001,
        "accommodates": 4,
        "room_type": "Entire home/apt",
        "beds": 2,
        "bedrooms": 1,
        "bathrooms": 2,
        "neighbourhood": "Brooklyn",
        "tv": 1,
        "elevator": 1,
        "internet": 0,
        "latitude": 40.71383,
        "longitude": -73.9658,
    }
)
print (r.text)

r = requests.get("http://0.0.0.0:80/ping")

print(r.reason)
