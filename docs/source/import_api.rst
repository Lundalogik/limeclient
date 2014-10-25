Import API
==========

.. module:: limeclient

This part of the documentation covers the different classes and methods available in limeclient.

LimeClient
----------

.. autoclass:: LimeClient
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

.. autoclass:: SimpleFieldMapping
   :members:

.. autoclass:: OptionFieldMapping
   :members:
