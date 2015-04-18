import requests, json

class Client:
    def __init__(self, access_token):
        self.access_token = access_token


    def get_activities(self):
        page = 1
        while True:
            # Request page of activities
            activitiesPage = self.makeRequest("activities", {'page': page})

            # If no more, abandon
            if len(activitiesPage) == 0:
                raise StopIteration

            # Yield results
            for activity in activitiesPage:
                yield activity

            # Go to next page
            page += 1


    def makeRequest(self, endpoint, options={}):
        optionsWithAuth = options.copy()
        optionsWithAuth['access_token'] = self.access_token

        r = requests.get("https://www.strava.com/api/v3/" + endpoint, params=optionsWithAuth)
        return r.json()

