# UCR Library metadata scripts

miscellaneous scripts for digital collections metadata work at UCR Library

* __aspace_digitization_csv.py__: export data from an ArchivesSpace resource record (collection)
    to a spreadsheet for use in digitization workflows.
    * Spreadsheet fields: Box, Folder/Item, Title.
    * Uses [ArchivesSnake](https://github.com/archivesspace-labs/ArchivesSnake) client library.
    * A less sophisticated version of the [Digitization Work Order Plugin](https://github.com/hudmol/digitization_work_order) functionality.