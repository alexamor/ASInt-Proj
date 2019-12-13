import requests

#rooms
r = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/2448131360897")
print(r.status_code)
data = r.json()
print(data)