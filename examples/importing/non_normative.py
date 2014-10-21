#!/usr/bin/env python
import sys
import time
import tempfile
import argparse
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


NORMALIZED_HEADERS = 'first name;last name;company;email;phone;title'


def normalize(infile, outfile):
    outfile.write(NORMALIZED_HEADERS + '\r\n')
    for line, content in enumerate(infile):
        if line > 0:
            row = content.split(';')
            name = row.pop(0)
            first, last = name.split()
            row.insert(0, last)
            row.insert(0, first)
            outfile.write(';'.join(row) + '\r\n')
    outfile.seek(0)

def main():
    args = parse_args()

    client = LimeClient(host='http://localhost:5000',
                        database='lime_basic_v4_1',
                        debug=False)

    with client.login(user=args.user, password=args.password) as c:
        print('Uploading file...')

        with open('non-normative.txt', 'r', encoding='utf-8') as raw:
            with tempfile.TemporaryFile('w+', encoding='utf-8') as fixed:
                normalize(raw, fixed)
                f = ImportFiles(c).create(filename='non-normative.txt',
                                          content=fixed)
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

        print('Adding simple mapping for last name...')
        lastname = SimpleFieldMapping(field=person.fields['lastname'],
                                       column='last name',
                                       key=False)
        config.add_mapping(lastname)

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

        print('Starting import job...')
        job = ImportJobs(c).create(config)

        for i in range(30):
            time.sleep(1)
            job = job.refresh()
            print('Current job status: {}'.format(job.status))
            if job.has_errors:
                print('Oh noes! Errors!')
                print(job.errors.errors[:10])
            if job.status != 'pending' and job.status != 'running':
                break

if __name__ == '__main__':
    sys.exit(main())

