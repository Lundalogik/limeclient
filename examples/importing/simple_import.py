#!/usr/bin/env python
import sys
import time
import argparse
from os.path import join, abspath, dirname
from limeclient import (LimeClient,
                        SimpleFieldMapping,
                        OptionFieldMapping,
                        RelationMapping,
                        ImportConfigs,
                        ImportConfig,
                        ImportJobs,
                        EntityTypes,
                        ImportFiles)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--user', required=True)
    p.add_argument('--password', required=True)
    return p.parse_args()

def main():
    args = parse_args()

    client = LimeClient(host='http://localhost:5000',
                        database='lime_basic_v4_1',
                        debug=True)

    with client.login(user=args.user, password=args.password) as c:
        print('Uploading file...')
        path = join(script_dir(), 'import_person.txt')
        with open(path, 'r', encoding='utf-8') as content:
            f = ImportFiles(c).create(filename='import_person.txt',
                                      content=content)
            f.delimiter = ';'
            f.save()

        print('Getting person entity type info...')
        person = EntityTypes(c).get_by_name('person')

        print('Creating import config...')
        config = ImportConfigs(c).create(entity=person, importfile=f)
        config.behaviour = ImportConfig.CreateAndUpdate

        print('Adding simple mapping for email...')
        email = SimpleFieldMapping(field=person.fields['email'],
                                   column='email',
                                   key=True)
        config.add_mapping(email)

        print('Adding simple mapping for first name...')
        firstname = SimpleFieldMapping(field=person.fields['firstname'],
                                       column='first name',
                                       key=False)
        config.add_mapping(firstname)

        print('Adding option mapping for position...')
        field = person.fields['position']
        position = OptionFieldMapping(field=field, column='title')
        position.default = field.option_by_localname('VD')
        position.map_option(column_val='IT',
                           option=field.option_by_localname('IT-chef'))
        config.add_mapping(position)

        print('Adding a relation to company...')
        relation = person.relations['company']
        company = relation.related
        relation_mapping = RelationMapping(column='company', relation=relation,
                                           key_field=company.fields['name'])
        config.add_mapping(relation_mapping)

        print('Saving configuration...')
        config.save()

        config_status = config.validate()
        print(config_status.valid)
        print(config_status.errors)

        print('Starting import job...')
        job = ImportJobs(c).create(config)

        for i in range(10):
            time.sleep(1)
            job = job.refresh()
            print('Current job status: {}'.format(job.status))
            if job.has_errors:
                print('Oh noes! Errors!')
                print(job.errors.errors[:10])
            if job.status != 'pending' and job.status != 'running':
                break

def script_dir():
    return abspath(dirname(__file__))

if __name__ == '__main__':
    sys.exit(main())
