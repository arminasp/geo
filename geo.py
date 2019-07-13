import csv
from sys import argv
from requests import get
from geograpy import get_place_context

if len(argv) < 2:
    exit('Usage: python %s [inputfile] [outputfile]' % argv[0])

input_file_path = argv[1]
output_file_path = argv[2] if len(argv) > 2 else 'output.csv'
api_url = 'http://92.62.139.201:8080/api/geonames/countries'

print("Opening input file '%s'..." % input_file_path)

with open(input_file_path, 'r', encoding='utf-8') as file:
    text = file.read().replace('\n', ' ')

chunks = [text[i:i + 100000] for i in range(0, len(text), 100000)]
results = []
output = []

print('Searching for geo names...')

for chunk in chunks:
    places = get_place_context(text=chunk).countries

    for place in places:
        if place[0].isupper() and place not in results and place in chunk:
            geo_names = get(api_url, {'name': place}).json()

            if len(geo_names) > 0:
                output += geo_names
                results.append(place)
                print('\t%s' % place)

print('Found %d results...' % len(results))

if len(results) > 0:
    print("Writing results to output file '%s'..." % output_file_path)

    with open(output_file_path, 'w', encoding='utf-8', newline='\n') as file:
        writer = csv.writer(file, delimiter='\t')

        for row in output:
            if row.values():
                writer.writerow(row.values())

print('Exiting...')
