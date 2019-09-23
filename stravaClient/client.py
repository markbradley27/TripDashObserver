import requests, json, time

class Client:
    def __init__(self, client_id, client_secret, token_path):
        self._client_id = client_id
        self._client_secret = client_secret
        self._token_path = token_path


    def get_activities(self):
        page = 1
        while True:
            # Request page of activities
            activitiesPage = self.makeRequest("activities", {'page': page})
            print("activitiesPage:", activitiesPage)

            # If no more, abandon
            if len(activitiesPage) == 0:
                raise StopIteration

            # Yield results
            for activity in activitiesPage:
                yield activity

            # Go to next page
            page += 1

    def refreshAccessToken(self, old_token_data):
        r = requests.post(
                "https://www.strava.com/oauth/token",
                params={
                    'client_id': self._client_id,
                    'client_secret': self._client_secret,
                    'grant_type': 'refresh_token',
                    'refresh_token': old_token_data['refresh_token']
                    }
                )
        new_token_data = r.json()
        with open(self._token_path, 'w') as token_file:
            json.dump(new_token_data, token_file)
        return new_token_data

    def getAccessToken(self):
        with open(self._token_path) as token_file:
            token_data = json.load(token_file)
        if token_data['expires_at'] - time.time() < 3600:
            token_data = self.refreshAccessToken(token_data)
        return token_data['access_token']

    def makeRequest(self, endpoint, options={}):
        optionsWithAuth = options.copy()
        optionsWithAuth['access_token'] = self.getAccessToken()
        print("optionsWithAuth:", optionsWithAuth)

        r = requests.get("https://www.strava.com/api/v3/" + endpoint, params=optionsWithAuth)
        return r.json()

