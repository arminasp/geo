import csv
from sys import argv

from geograpy import get_place_context
from requests import get

if len(argv) < 3:
    exit('Usage: python %s [isolanguage] [inputfile] [outputfile]' % argv[0])

language_code = argv[1]
input_file_path = argv[2]
output_file_path = argv[3] if len(argv) > 3 else 'output.csv'
api_url = 'http://92.62.139.201:8080/api/geonames/countries'

print("Opening input file '%s'..." % input_file_path)

with open(input_file_path, 'r', encoding='utf-8') as file:
    text = file.read().replace('\n', ' ')

chunks = [text[i:i + 100000] for i in range(0, len(text), 100000)]
output = {}
results = []

print("Searching for geo names in '%s' language ..." % language_code)

for chunk in chunks:
    places = get_place_context(text=chunk).countries
    temp_results = {}

    for place in places:
        if place[0].isupper() and place not in results and place in chunk:
            geo_names = get(api_url, {
                'name': place,
                'isolanguage': language_code
            }).json()

            if len(geo_names) > 0:
                pos = chunk.find(place)
                output[pos] = geo_names
                temp_results[pos] = place
                results.append(place)

    for key in sorted(temp_results.keys()):
        print('\t%s' % temp_results[key])

    temp_results.clear()

print('Found %d results...' % len(results))

if len(results) > 0:
    print("Writing results to output file '%s'..." % output_file_path)

    with open(output_file_path, 'w', encoding='utf-8', newline='\n') as file:
        writer = csv.writer(file, delimiter='\t')

        for key in sorted(output.keys()):
            for row in output[key]:
                if row.values():
                    writer.writerow(row.values())

print('Exiting...')
