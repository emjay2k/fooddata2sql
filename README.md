# usda_food_db2sql
This python program converts the USDA FoodData Central Data database into a sql(ite) database.

## Purpose
The [U.S. Department of Agriculture][1] (USDA) has a really useful nutrition information database that is excellent for research purposes. You can [download][2] it for free. While it would technically be allowed to redistribute it, I explicitly choose not to so you will always get the latest data from the original source. Just grab their CSV version for usage with this tool.

## License
The software is licensed under the terms of the GNU General Public License 3. See LICENSE file for details.

## Requirements
* Python3
* [FoodData Central Data][2] database (CSV version)
* If you do not download *All Data Types*, you will also need the *Supporting data*. In this case Just extract both zip files into the same folder and they will end up in the same database.

A minor caveat if you do not download *All Data Types* is the duplicate file *all_downloaded_table_record_counts.csv* present in both zip files, which will not be automatically merged in this case. If you want the content of both *all_downloaded_table_record_counts.csv* files in your database, you need to manually append the one to the other (and remove the second header). But since it only contains the entry count of each table, you will probably not need that information anyway.

## Input
Folder to the CSV files with the aforementioned database.

## Output
By default it will generate an sqlite3 file with the data from the csv files. The following types are auto-detected:

* NULL (no data in column)
* BOOLEAN
* INTEGER
* FLOAT
* DATE (for YYYY-MM-DD)
* TEXT (for anything else)

If you want to import to anything else but sqlite3 you can try to use MysqlImporter or PgsqlImporter instead. I didn't test those, so it might require some bugfixing. 

The script also attempts to find a suitable primary key. If during import the detection of a primary key will fail for a few tables, you will get a warning message. This is harmless in most cases, as there are tables without a proper unique identifier that could serve as a primary key.

## Usage
The program syntax is pretty self-explanatory, just run it like so

    ./usdafood2sql.py -i INPUT -o OUTPUT

Just give the directory to the CSV files you obtained as INPUT and the desired sqlite3 filename for output. There are also some example queries available in usdafoodsearch.py for usage demonstration. If you have to export to some database server, you will need to install the proper driver and tinker with the code a bit (see commented parts in usdafood2sql.py). I haven't tested it at all in such a scenario, so some bugfixing may be required.

## Performance
This program is a thing that in most scenarios will only run once, so it is not optimized for performance. It will take a while so just be patient. To give you an estimation what to expect, here the execution times on a moderately fast 2018 PC (measured using the Linux *time* command):

**Foundation Foods import (31 MB)**

    real    0m35.067s
    user    0m20.258s
    sys     0m0.369s

**FNDDS import (49 MB)**

    real    0m51.243s
    user    0m38.250s
    sys     0m0.456s

**Full Download of All Data Types import (670 MB)**

    real    6m32.103s
    user    5m35.524s
    sys     0m5.598s

Yes, it is a lot of data :-)

## Remark on database sizes
It is highly compressible, so you can reduce size for distribution to between 3 MB (foundation foods with support data) and 64 MB (full data) e.g. by using 7zip.

## Acknowledgement
Nutrition data provided by:

    U.S. Department of Agriculture, Agricultural Research Service. FoodData Central, 2019. fdc.nal.usda.gov.

The [USDA][2] has done a wonderful job by assembling and providing the nutrition data to everyone for free. The database is public domain and a great service to all of mankind. This is how I remember the USA.

[1]: <https://fdc.nal.usda.gov/> "U.S. department of agriculture website"
[2]: <https://fdc.nal.usda.gov/download-datasets.html> "FoodData Central Data website"
