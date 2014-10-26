Import API
==========

.. module:: limeclient

This part of the documentation covers the different classes and methods available in limeclient.

LimeClient
----------

.. autoclass:: LimeClient
   :members:

EntityTypes
-----------

.. autoclass:: EntityTypes
   :members:

.. autoclass:: EntityType
   :members:

   .. attribute:: name

   Name of entity type.

   .. attribute:: is_system

   `True` if this is a system type.

 
Field Types
~~~~~~~~~~~

.. autoclass:: SimpleField
   :members:

   .. attribute:: label

   .. attribute:: length

   .. attribute:: localname

   .. attribute:: name

   .. attribute:: readonly

   .. attribute:: required

   .. attribute:: type

.. autoclass:: OptionField
   :members:

   .. attribute:: label

   .. attribute:: localname

   .. attribute:: name

   .. attribute:: readonly

   .. attribute:: required

   .. attribute:: type

.. autoclass:: Option
   :members:

Relations
~~~~~~~~~

.. autoclass:: Relation
   :members:

   .. attribute:: localname

   .. attribute:: name


ImportFiles
-----------

.. autoclass:: ImportFiles
   :members:

.. autoclass:: ImportFile
   :members:

   .. attribute:: delimiter

   Use this to set the delimiter used in the file so LIME knows how to parse it.

   .. attribute:: filename

   The name of the file.

   .. attribute:: headers

   Returns the headers (:class:`ImportFileHeaders`) of the file.

   .. method:: save()

   Save the file information in LIME.

.. autoclass:: ImportFileHeaders
   :members:

   .. attribute:: headers

   A list of the header names in the file

Import Configuration
--------------------

.. autoclass:: ImportConfigs
   :members:

.. autoclass:: ImportConfig
   :members:

   .. attribute:: behaviour

   Determines how the import handles existing objects in LIME Pro. Can be one of the following:

   - `ImportConfig.CreateAndUpdate`
   - `ImportConfig.UpdateOnly`
   - `ImportConfig.CreateOnly`

Mapping
~~~~~~~

The following types can be passed to :meth:`ImportConfig.add_mapping` to
define how columns in the import file should be mapped to fields in LIME Pro:

.. autoclass:: SimpleFieldMapping
   :members:

.. autoclass:: OptionFieldMapping
   :members:

.. autoclass:: RelationMapping
   :members:

Import Jobs
===========

.. autoclass:: ImportJobs
   :members:

.. autoclass:: ImportJob
   :members:

.. autoclass:: ImportJobErrors
   :members:
