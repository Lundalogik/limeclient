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

Field Types
~~~~~~~~~~~

.. autoclass:: SimpleField
   :members:

.. autoclass:: OptionField
   :members:

.. autoclass:: Option
   :members:

Relations
~~~~~~~~~

.. autoclass:: Relation
   :members:

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
