IMPORTING FILES
===============

The LIME Pro API supports importing simple text files. 

FILE RECOMMENDATIONS
--------------------

The first line of the file should contain names for the columns in the rest of
the file.

The file should preferably be encoded using UTF-8.

CONCEPTS
--------

In order to start an import, we need to define three major components, an
import file, an import configuration, and an import job.

The import file contains not only the contents of the file itself, but also
some additional information, such as what delimiter is used to separate the
columns.

The import configuration contains information about what file to import,
what type of LIME objects we want to import the file to, and how to map what's
in the file to fields on the fields and relation of that LIME type.

Finally, when the import job is created it will start the actual import as
soon as it can. The import job will then contain the status of the import,
and any errors that might have occured during the process.

USING THE API-CLIENT
--------------------
TBD

AUTHENTICATING
--------------
First of all, we need to authenticate ourselves with the LIME Pro server.
If we're using the API-client this done by creating an instance of LimeClient
and logging in:

.. code-block:: python
    from limerest

     client = LimeClient('http://localhost:2134', 'my_database')

     with client.login('user', 'pass') as c:
         # Do stuff here...

This will start a new session in LIME that will automatically be closed when
program is finished.

REST PROTOCOL
-------------
TBD

UPLOADING A FILE
----------------
Once we've authenticated ourselves, we need to begin by asking the server to
create a file for us:

.. code-block:: python
    with client.login('user', 'pass') as c:
        f = ImportFile(c).create('import_my_data.txt')
        f.delimiter(',')
        f.save()

Here we uploaded a file to LIME, which returns with a file object populated
with default values. We then told LIME a little bit more about how it should
interpret the file, and saved the new information on the server.

RETRIEVING THE LIME DATA TYPE
-----------------------------
The second piece of information we need before we can start configuring how to
interpret the content of the file is an object that represents the data type
in LIME. In the LIME API this is called an 'entity'.

If the information in the file contains information about people we might want
to load the 'person' entity type:

.. code-block:: python
    with client.login('user', 'pass') as c:
        f = ImportFile(c).create('import_my_data.txt')
        f.delimiter(',')
        f.save()

        person = EntityTypes(c).get_by_name('person')

CREATING AN IMPORT CONFIGURATION
--------------------------------
With that we have enough information to start configuring our import:

.. code-block:: python
    with client.login('user', 'pass') as c:
        f = ImportFile(c).create('import_my_data.txt')
        f.delimiter(',')
        f.save()

        person = EntityTypes(c).get_by_name('person')

        [TO BE IMPLEMENTED]
        config = ImportConfigs(c).create(entity=person, importfile=f)

BEHAVIOUR
---------
[TO BE IMPLEMENTED]

By setting the behaviour property of the config you can make the import:

**config.behaviour = ImportConfig.CreateAndUpdate**
Update existing objects if they match  what's in the file, and create new
objects if nothing matches

**config.behaviour = ImportConfig.OnlyUpdate**
Only update objects that match what's in the import file. Don't create any new
objects.

**config.behaviour = ImportConfig.OnlyCreate**
Create a new object for each row in the import file. Don't try to match against
existing objects in LIME.

MAPPING
-------
For each row in the file to import, LIME needs to know what to do with the
data. We tell LIME how to accomplish this by telling it how to map each column
to something a field or relation of the data type we're import to.

The LIME API supports three types of mappings: mappings of simple types, such
as strings and numbers, mappings option fields where the value can be one of
several predefined values, and finally relations to other types of entities in
LIME, such as persons being related to companies.

Adding a simple field mapping
-----------------------------
For a simple type, such as a string that represents the e-mail address of a
person, we can add a SimpleFieldMapping to our new config:

.. code-block:: python
    with client.login('user', 'pass') as c:
        # ...

        person = EntityTypes(c).get_by_name('person')

        config = ImportConfigs(c).create(entity=person, importfile=f)

        email = SimpleFieldMapping(field=person.fields['email'],
                                   column='email',
                                   key=True)
        config.add_field_mapping(email)

Here we map the values of the column 'email' to the field 'email' of a person
in LIME.

Setting 'key=True' means that if we find an existing person in LIME with this
email address, we will update that person instead of creating a new one.

We can specify 'key=True' for multiple mappings. In that case all values must
match for the import to consider updating a person in LIME instead of adding a
new.

Adding a mapping to an option field
-----------------------------------

You can map a column in the import file to an option field in LIME by adding
an OptionFieldMapping to your import configuration.

Within the OptionFieldMapping, you specify how a value in a column translates
to one of the possible values of an option field in LIME.

[HOW DO WE WANT TO MAP? ID/KEY? HOW TO FIND?]

.. code:: python
    with client.login('user', 'pass') as c:
        # ...

        field = person.fields['position']
        position = OptionFieldMapping(field=field, column='title')
        position.default = field.option_id_for('VD')
        position.map_value(column_val='IT',
                           field_val=field.option_id_for('IT-chef'))
        config.add_field_mapping(position)

In the example above, we map the column with the header 'title' to the field
'position' of the entity 'person' in LIME.

By setting the default attribute of our new mapping, we're telling the importer
that it should set any values that haven't been explicitly matched to a default value.

[None should mean use default value of field]

