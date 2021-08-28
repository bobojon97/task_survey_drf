import requests

def client():
    token_h = "Token 826509381128d20de4022678444a978e5a2d9f47"
    # credentials = {"username": "admin", "password": "password"}
    # response = requests.post("http://127.0.0.1:8000/api/rest-auth/login/", data=credentials)
    headers = {"Authorization": token_h}
    response = requests.get("http://127.0.0.1:8000/api/survey/", headers=headers)
    print("Status Code: ", response.status_code)
    response_data = response.json()
    print(response_data)

if __name__ == "__main__":
    client()