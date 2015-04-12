import argparse
from stravalib.client import Client

def observe():
    # Parse arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument('--access_token', action='store', help='Strava API access token')
    args = argParser.parse_args()

    # Create client and authenticate
    client = Client()
    client.access_token = args.access_token
    if (client.access_token == None):
        client.access_token = open('access_token.txt', 'r').read().strip()
    if (client.access_token == None): raise Exception('Must provide Strava access token.')

    # Test
    print "Current athlete:"
    print client.get_athlete()

if __name__ == "__main__":
    observe()