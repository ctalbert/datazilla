import os
import json

from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from datazilla.model import DatazillaModel

class Command(BaseCommand):

    help = "Transfer data from one project to another."

    option_list = BaseCommand.option_list + (
        make_option('--source',
                    action='store',
                    dest='source',
                    default=False,
                    help='Source project to pull data from: talos, ' +
                         'b2g, stoneridge, test etc...'),
        make_option('--target',
                    action='store',
                    dest='target',
                    default=False,
                    help='Target project to push data to: talos, ' +
                         'b2g, stoneridge, test etc...'),
        make_option('--records',
                    action='store',
                    dest='records',
                    default=10,
                    help='Total number of records to transfer. Defaults to 10.'),
        make_option('--start',
                    action='store',
                    dest='start',
                    default=0,
                    help='Database id to start from.  Defaults to 0.'),
        make_option('--debug',
                    action='store_true',
                    dest='debug',
                    default=None,
                    help='Write the json structures that will be transfered to stdout ' +
                         'but do not write them to the database.'),
        make_option('--show',
                    action='store_true',
                    dest='show',
                    default=None,
                    help='Write the json structures that will be transfered to stdout ' +
                         'and write them to the database.'),)

    def handle(self, *args, **options):

        source = options.get('source')
        target = options.get('target')
        records = int( options.get('records') )
        start = int( options.get('start') )

        dm_source = DatazillaModel(source)
        dm_target = DatazillaModel(target)

        data_iter = dm_source.getAllTestData(start)

        iterations = 0

        for d in data_iter:
            for data in d:
                deserialized_data = json.loads( data['data'] )

                if options['debug']:
                    self.stdout.write(data['data'] + "\n")
                else:
                    if options['show']:
                        self.stdout.write(data['data'] + "\n")
                    dm_target.loadTestData(deserialized_data, data['data'])

                iterations += 1

                if iterations == records:

                    dm_source.disconnect()
                    dm_target.disconnect()

                    return


