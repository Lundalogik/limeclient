Importing Files
===============

The LIME Pro API supports importing simple text files. 

File Recommendations
--------------------

The first line of the file should contain names for the columns in the rest of
the file.

The file should preferably be encoded using UTF-8.

Concepts
--------

In order to start an import, we need to define three major components, an
import file, an import configuration, and an import job.

**The import file** contains not only the contents of the file itself, but also
some additional information, such as what delimiter is used to separate the
columns.

**The import configuration** contains information about what file to import,
what type of LIME objects we want to import the file to, and how to map what's
in the file to fields on the fields and relation of that LIME type.

Finally, when **the import job** is created it will start the actual import as
soon as it can. The import job will then contain the status of the import,
and any errors that might have occured during the process.

Importing a file
----------------
Let's say we have the following file containing information about people we want to add to LIME:

::

    name;e-mail;ship;rank
    Ripley;ellen@nostromo.com;Nostromo;Warrant Officer
    Dallas;dallas@weyland.com;Nostromo;Captain
    Ash;ash@weyland.com;Nostromo;Science Officer
    ...

We have a LIME database that contains information about employees and ships, and we've been tasked with importing this file in to LIME.

We install the latest version of limeclient, create a module called weyland.py.

Authenticating
--------------
First of all, we need to authenticate ourselves with the LIME Pro server.
If we're using the API-client this done by creating an instance of :class:`~limeclient.LimeClient`
and logging in:

.. code-block:: python

    from limeclient import LimeClient

     client = LimeClient('https://myserver:2134', 'weyland_db')
     with client.login('user', 'pass') as c:
         # Do stuff here...

This will start a new session in LIME that will automatically be closed when
program is finished.

If you're importing data to a hosted LIME installation, you should not pass
the database name argument.

Uploading a file
----------------
Once we've authenticated ourselves, it's time for us to tell LIME about the
file we want to import.


.. code-block:: python

    with client.login('user', 'pass') as c:
        with open('nostromo_crew.txt') as content:
            f = ImportFiles(c).create(filename='nostromo_crew.txt',
                                      content=content)
            f.delimiter = ';'
            f.save()

Here we uploaded a file to LIME, which returns with a file object populated
with default values. We then told LIME a little bit more about how it should
interpret the file, and saved the new information on the server.

Retrieving the LIME data type
-----------------------------
The second piece of information we need before we can start configuring how to
interpret the content of the file is an object that represents the data type
in LIME.

If the information in the file contains information about people we might want
to load the 'crew' :class:`~limeclient.LimeTypes`:

.. code-block:: python

    with client.login('user', 'pass') as c:
        with open('nostromo_crew.txt') as content:
            f = ImportFiles(c).create(filename='nostromo_crew.txt',
                                     content=content)
            f.delimiter(';')
            f.save()

        crew = LimeTypes(c).get_by_name('crew')

Creating an import configuration
--------------------------------
With that we have enough information to start configuring our import:

.. code-block:: python

    with client.login('user', 'pass') as c:
        with open('nostromo_crew.txt') as content:
            f = ImportFiles(c).create(filename='nostromo_crew.txt',
                                     content=content)
            f.delimiter(';')
            f.save()

        crew = LimeTypes(c).get_by_name('crew')

        config = ImportConfigs(c).create(lime_type=crew, importfile=f)

Behavior
---------
We can tell LIME what it should do for each row it finds in our import file.

**config.behavior = ImportConfig.CreateAndUpdate**
Update existing objects if they match  what's in the file, and create new
objects if nothing matches. This is the default value for a new
:class:`~limeclient.ImportConfig`

**config.behavior = ImportConfig.OnlyUpdate**
Only update objects that match what's in the import file. Don't create any new
objects.

**config.behavior = ImportConfig.OnlyCreate**
Create a new object for each row in the import file. Don't try to match against
existing objects in LIME.

Mapping
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
In our example, the name and e-mail of the crew members are simple types, so we
add simple field mappings for those. We also mark the name field as a key
field, meaning that we will use this when determining if this row matches an
existing object in LIME.

.. code-block:: python

    with client.login('user', 'pass') as c:
        # ...

        crew = LimeTypes(c).get_by_name('crew')

        config = ImportConfigs(c).create(lime_type=crew, importfile=f)

        name = SimpleFieldMapping(field=crew.fields['name'],
                                   column='name',
                                   key=False)
        config.add_mapping(name)

        email = SimpleFieldMapping(field=crew.fields['email'],
                                   column='e-mail',
                                   key=True)
        config.add_mapping(email)


We can specify 'key=True' for multiple mappings. In that case all values must
match for the import to consider updating a person in LIME instead of adding a
new.

Adding a mapping to an option field
-----------------------------------

You can map a column in the import file to an option field in LIME by adding
an :class:`~limeclient.OptionFieldMapping`  to your import configuration.

Within the :class:`~limeclient.OptionFieldMapping`, you specify how a value in a column translates
to one of the possible values of an option field in LIME.

.. code:: python

    with client.login('user', 'pass') as c:
        # ...

        field = crew.fields['rank']
        position = OptionFieldMapping(field=field, column='rank')
        position.default = field.option_by_key('Engineer')
        position.map_option(column_val='Captain',
                            option=field.option_by_key('Captain'))
        position.map_option(column_val='Warrant Officer',
                            option=field.option_by_key('Warrant Officer'))
        config.add_mapping(position)

In the example above we first say that any values for the 'rank' column that
haven't been explicitly mapped, we should assume that the crew member is
engineer.

We then proceed to explicitly map the values for captain and warrant officer.

Mapping relations
-----------------

Finally, we need to import the ship of each crew member in the file. 'Ship'
is a separate table in the LIME database and we need to tell the import about
this:

.. code:: python

    with client.login('user', 'pass') as c:
        # ...

        crew = LimeTypes(c).get_by_name('crew')

        # ...

        relation = crew.relations['ship']
        ship = relation.related
        relation_mapping = RelationMapping(column='ship', relation=relation,
                                           key_field=ship.fields['name'])
        config.add_mapping(relation_mapping)

        config.save()

We ask the lime type for the relation to the ship type, we use that to get a
hold of the actual ship type. We then tell the importer that the 'ship' column
contains names of ships.

Now, we can save the import configuration and are ready to start the import.

Starting an import job
----------------------

We can now start the import job:

.. code-block:: python

   with client.login(user=args.user, password=args.password) as c:
       # ...

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

This tells LIME to put the import job on a queue. We then proceed to poll the
status of the job. If something goes wrong, the ten first errors will be
printed to the console.

