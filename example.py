#!/usr/bin/env python
import sys
import time
import argparse
from limerest import (RestClient,
                      SimpleFieldMapping,
                      OptionFieldMapping,
                      RelationMapping,
                      ImportConfigs,
                      ImportJobs,
                      Entities,
                      ImportFiles)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--user', required=True)
    p.add_argument('--password', required=True)
    return p.parse_args()

def main():
    args = parse_args()

    client = RestClient(host='http://localhost:5000',
                        database='lime_basic_v4_1')

    with client.login(user=args.user, password=args.password) as c:
        f = ImportFiles(c).create('import_person.txt')
        f.delimiter = ';'
        f.save()

        person = Entities(c).get_by_name('person')

        config = ImportConfigs(c).create()
        config.entity = person
        config.importfile = f

        email = SimpleFieldMapping(field=person.fields['email'],
                                   column='email',
                                   key=True)
        config.add_field_mapping(email)

        firstname = SimpleFieldMapping(field=person.fields['firstname'],
                                       column='first name',
                                       key=False)
        config.add_field_mapping(firstname)

        field = person.fields['position']
        position = OptionFieldMapping(field=field, column='title')
        position.default = field.option_id_for('VD')
        position.map_value(column_val='IT',
                           field_val=field.option_id_for('IT-chef'))
        config.add_field_mapping(position)

        relation = person.relations['company']
        company = relation.related
        relation_mapping = RelationMapping(column='company', relation=relation,
                                           key_field=company.fields['name'])
        config.add_relation_mapping(relation_mapping)

        config.save()

        job = ImportJobs(c).create(config)

        for i in range(10):
            time.sleep(1)
            job = job.refresh()
            print(job.status)
            print(job.errors.errors[:10])

if __name__ == '__main__':
    sys.exit(main())
