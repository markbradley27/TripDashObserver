import os, argparse, yaml, json, dateutil.parser, logging, sys
from stravaClient import Client


def observe():
    # Parse arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument('--token_path', action='store', help='Strava API token path')
    argParser.add_argument('--client_creds_path', action='store', help='Strava API client creds path')
    args = argParser.parse_args()

    # Read config
    scriptPath = os.path.dirname(os.path.realpath(__file__))
    config = yaml.load(open(scriptPath + '/config.yaml', 'r'))

    # Set up logger
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    # Create client and authenticate
    client_id = None
    client_secret = None
    with open(args.client_creds_path) as client_creds_file:
        client_creds_data = json.load(client_creds_file)
        client_id = client_creds_data['client_id']
        client_secret = client_creds_data['client_secret']
    client = Client(client_id, client_secret, args.token_path)

    # Create local dict for storing data
    stravaDump = {'rides': {}, 'stats': {}}

    # Get all activities newer than the start date
    for activity in client.get_activities():
        print("Activity:", activity)
        if dateutil.parser.parse(activity['start_date']).date() > config['startDate']:

            # Skip blacklisted activities
            if config['activityBlacklist'] is not None and activity['id'] in config['activityBlacklist']:
                logging.info("Skipping:" + activity['start_date'] + '-' + activity['name'])
                continue

            logging.info("Observing:" + activity['start_date'] + '-' + activity['name'])

            # If parameter to be stored in abreviated copy, add to strava dump
            for parameter in config['abreviatedAttributes']:
                stravaDump['rides'].setdefault(activity['start_date'], {})[parameter] = activity[parameter]

        else: break

    # Compute statistics
    for statistic in config['statisticize']:
        stravaDump['stats'].setdefault(statistic['attribute'], {})[statistic['statistic']] = \
          computeStatistic(stravaDump, statistic['attribute'], statistic['statistic'])

    # Save json dump
    with open(scriptPath + '/' + config['outputFilename'], 'w') as outputFile:
        json.dump(stravaDump, outputFile, indent=2)


def computeStatistic(dump, attribute, statistic):
    result = 0;

    # Grand total
    if statistic == 'total':
        for rideDate, ride in dump['rides'].items():
            result += ride[attribute]
        return result

    # Daily average
    elif statistic == 'dailyAverage':
        dailyTotals = {}
        for rideDate, ride in dump['rides'].items():
            rideDate = dateutil.parser.parse(rideDate).date()
            if rideDate not in dailyTotals: dailyTotals[rideDate] = 0
            dailyTotals[rideDate] += ride[attribute]
        days = 0
        for date, total in dailyTotals.items():
            days += 1
            result += total
        return result / days


if __name__ == '__main__':
    observe()
