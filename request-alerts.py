import sys
import requests
from requests.exceptions import HTTPError
import argparse

argparser = argparse.ArgumentParser()
alertcountint = 0

argparser.add_argument('-s', '--state')
argparser.add_argument('-t', '--type')
#argparser.add_argument('-h', '--help')
argvar = argparser.parse_args()
print(sys.argv)

# Does some fun stuff to check if it has an alert type.
if len(sys.argv)>4:
    url = 'https://api.weather.gov/alerts/active?&area=' + argvar.state + '&event=' + argvar.type + '&limit=100'     

elif len(sys.argv)>0:
    try:
        url = 'https://api.weather.gov/alerts/active?&area=' + argvar.state + '&limit=100'
    except:
        url = 'https://api.weather.gov/alerts/active?&event=' + argvar.type + '&limit=100'

#url = 'https://api.weather.gov/alerts/active?&area=' + argvar.state

# Main function pulls from the API, parses it, and formats it so it's readable.
for url in [url]:
    try:
        response = requests.get(url)

        # If the response was successful, no exception will be raised.
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Success!')
        # Parses the b l o b of JSON and turns it into into a nice data dump.
        for alert in response.json()['features']:
            print('------------------------------' + alert['properties']['event'] + '-----------------------------')
            print(alert['properties']['headline'])
            print(alert['properties']['description'])
            print('\n')
            print('Nerd Info:')
            print('Certainty: ' + alert['properties']['certainty'])
            print('Urgency: ' + alert['properties']['urgency'])
            print('Severity: ' + alert['properties']['severity'])
            print('\n')
            alertcountint += 1
        # Prints URL for debugging purposes.
        alertcount = str(alertcountint)
        print(alertcount + ' Alerts total.')
        print('\n')
        print(url)