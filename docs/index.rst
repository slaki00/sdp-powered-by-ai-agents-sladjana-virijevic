BankOCR Documentation
=====================

BankOCR reads scanned account numbers from a text file, validates them with
the checksum, corrects ERR and ILL entries when exactly one alternative passes,
and writes the result file. It runs as a CLI in Docker.

.. toctree::
   :maxdepth: 2
   :caption: Overview:

   README

.. toctree::
   :maxdepth: 2
   :caption: Architecture:

   architecture/01-introduction-and-goals
   architecture/02-constraints
   architecture/03-context-and-scope
   architecture/04-solution-strategy
   architecture/05-building-block-view
   architecture/06-runtime-view
   architecture/07-deployment-view
   architecture/08-cross-cutting-concepts
   architecture/09-architecture-decisions
   architecture/10-quality-requirements
   architecture/11-risks-and-technical-debts
   architecture/12-glossary
   arc42-summary

.. toctree::
   :maxdepth: 2
   :caption: User Stories:

   user-stories/README
   user-stories/recognition
   user-stories/validation
   user-stories/reporting

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
