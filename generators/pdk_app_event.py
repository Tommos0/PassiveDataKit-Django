import calendar
import csv
import json
import tempfile

from ..models import DataPoint, install_supports_jsonfield

def extract_secondary_identifier(properties):
    if 'event_name' in properties:
        return properties['event_name']

    return None

def compile_report(generator, sources):
    filename = tempfile.gettempdir() + '/pdk_' + generator + '.txt'

    with open(filename, 'w') as outfile:
        writer = csv.writer(outfile, delimiter='\t')

        writer.writerow([
            'Source',
            'Created Timestamp',
            'Created Date',
            'Event Name',
            'Event Properties'
        ])

        for source in sources:
            points = DataPoint.objects.filter(source=source, generator_identifier=generator).order_by('created') # pylint: disable=no-member,line-too-long

            index = 0
            count = points.count()

            while index < count:
                for point in points[index:(index + 5000)]:
                    row = []

                    row.append(point.source)
                    row.append(calendar.timegm(point.created.utctimetuple()))
                    row.append(point.created.isoformat())

                    properties = {}

                    if install_supports_jsonfield():
                        properties = point.properties
                    else:
                        properties = json.loads(point.properties)

                    row.append(properties['event_name'])
                    row.append(json.dumps(properties['event_details']))

                    writer.writerow(row)

                index += 5000

    return filename