import requests

# Send get request to specifieed web address
response = requests.get('https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-zip-code-latitude-and-longitude&rows=624&facet=state&refine.state=MD')

data = response.json()
zipCodes = open('zip_codes.csv', 'w')

# Writes all Maryland zip codes along with their correesponding latitude and longitude
# to a comma separated values file, 'zip_codes.csv'
for area in data['records']:
    zipList = [area['fields']['zip'], str(area['fields']['latitude']), str(area['fields']['longitude'])]
    zipCodes.write(",".join(zipList) + '\n')

zipCodes.close()
