# Log Analysis Project
A small reporting script to analyze a dummy news dataset to answer the following questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Contents:
1. Source Code: `log_analysis.py`
2. Sample Output: `log_analysis_output.txt`

## Requirements
1. `FSND-Virtual-Machine.zip`
2. `newsdata.sql`

## Usage example for (macOS):
1. Unzip the contents in `FSND-Virtual-Machine.zip`
2. Using your terminal cd into the vagrant directory inside fullstack-nanodegree-vm directory
3. Start virtual machine `vagrant up` & ssh into it `vagrant ssh` 
4. Place newsdata.sql and log_analysis.py in vagrant directory on your local (file will be accessible on virtual)
5. In vagrant virtual cd to the `/vagrant` directory and run `psql -d news -f newsdata.sql` to load the data
6. Execute the log_analysis.py using `python3 log_analysis.py` to view the output

## License:
MIT
