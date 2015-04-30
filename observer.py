import argparse, yaml, json, dateutil.parser
from stravaClient import Client


def observe():
    # Parse arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument('--access_token', action='store', help='Strava API access token')
    args = argParser.parse_args()

    # Read config
    config = yaml.load(open('config.yaml', 'r'))

    # Create client and authenticate
    access_token = args.access_token
    if access_token == None:
	try:
        	access_token = open('access_token.txt', 'r').read().strip()
	except:
		pass
    if access_token == None: raise Exception("Must provide Strava access token.")
    client = Client(access_token)

    # Create local dict for storing data
    stravaDump = {'rides': {}, 'stats': {}}

    # Get all activities newer than the start date
    for activity in client.get_activities():
        if dateutil.parser.parse(activity['start_date']).date() > config['startDate']:

            # If parameter to be stored in abreviated copy, add to strava dump
            for parameter in config['abreviatedAttributes']:
                stravaDump['rides'].setdefault(activity['start_date'], {})[parameter] = activity[parameter]

        else: break

    # Compute statistics
    for statistic in config['statisticize']:
        stravaDump['stats'].setdefault(statistic['attribute'], {})[statistic['statistic']] = \
          computeStatistic(stravaDump, statistic['attribute'], statistic['statistic'])

    # Save json dump
    with open(config['outputFilename'], 'w') as outputFile:
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
