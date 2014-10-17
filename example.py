#!/usr/bin/env python
import sys
import time
from limerest import (RestClient,
                      SimpleFieldMapping,
                      OptionFieldMapping,
                      RelationMapping,
                      ImportConfigs,
                      ImportJobs,
                      Entities,
                      ImportFiles)


def main():
    client = RestClient(host='http://localhost:5000',
                        database='my_db')

    with client.login(user='admin', password='') as c:
        f = ImportFiles(c).create('import_person.txt')
        f.delimiter = ';'
        f.save()

        person = Entities(c).get_by_name('person')

        config = ImportConfigs(c).create()
        config.entity = person
        config.importfile = f

        email_mapping = SimpleFieldMapping(column='email', key=True)
        config.add_field_mapping(field=person.fields['email'],
                                 mapping=email_mapping)

        firstname_mapping = SimpleFieldMapping(column='firstname', key=False)
        config.add_field_mapping(field=person.fields['firstname'],
                                 mapping=email_mapping)

        position_mapping = OptionFieldMapping(column='title')
        position_mapping.default = 'ceo'
        position_mapping.map_value(column_val='IT', field_val='supersupport')
        config.add_field_mapping(field=person.fields['position'],
                                 mapping=position_mapping)

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
