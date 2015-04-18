import argparse, yaml, json, dateutil.parser
from stravaClient import Client

def observe():
    # Parse arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument('--access_token', action='store', help='Strava API access token')
    args = argParser.parse_args()

    # Read config
    config = yaml.load(open('tdoConfig.yaml', 'r'))
    print "Config:", config

    # Create client and authenticate
    access_token = args.access_token
    if access_token == None:
        access_token = open('access_token.txt', 'r').read().strip()
    if access_token == None: raise Exception("Must provide Strava access token.")
    client = Client(access_token)

    # Create local dict for storing data
    stravaDump = {
        'rides': {},
        'stats': {},
    }

    # Get all activities newer than the start date
    for activity in client.get_activities():
        if dateutil.parser.parse(activity['start_date']).date() > config['startDate']:

            # If parameter to be stored in abreviated copy, add to strava dump
            for parameter in config['abreviatedAttributes']:
                stravaDump['rides'].setdefault(activity['start_date'], {})[parameter] = activity[parameter]

        else: break

    # Print for now
    with open(config['outputFilename'], 'w') as outputFile:
        json.dump(stravaDump, outputFile, indent=2)


if __name__ == '__main__':
    observe()