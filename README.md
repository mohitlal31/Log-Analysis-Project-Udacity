# Log Analysis Project

A simple reporting tool to present important details about a newspaper website
 
The project uses python code to read the postgreSQL databases 
and presents answers to 3 important questions about the news data.

### Required Libraries, Softwares and Dependencies

#### 1. Virtual Box and Vagrant
Refer the [installation](https://classroom.udacity.com/courses/ud197/lessons/3423258756/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0) details

#### 2. Tabulate
The project uses the python library [Tabulate](https://pypi.org/project/tabulate/) to present the analysis
in a neat tabular grid.
To Install Tabulate, from the command line in your virtual box, run `pip install tabulate`

Refer [Tabulate Installation](https://pypi.org/project/tabulate/) for more information.

#### 3. News database
[Download the data here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). You will need to unzip this file after downloading it. The file inside is called newsdata.sql. Put this file into the vagrant directory, which is shared with your virtual machine.

To build the reporting tool, you'll need to load the site's data into your local database.
To load the data, cd into the vagrant directory and use the command `psql -d news -f newsdata.sql`.

Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, 
creating tables and populating them with data. 

#### 4. Create Views
Before running the python program, you need to create the pre-requisite postgreSQL database views which are used by the python code.
From the vagrant directory in your virtual box, run the following postgreSQL queries from the command line in the same order 

`create view top_paths as select path, count(*) as num from log where log.status = '200 OK' group by path order by num desc;`

`create view top_articles as select articles.author, articles.title, top_paths.num from articles, top_paths where top_paths.path like '%' || articles.slug || '%';`

`create view top_authors as select top_articles.author, sum(top_articles.num) as num_views from authors, top_articles group by top_articles.author order by num_views desc;`

`create view failed_views as select time::timestamp::date, count(*) as num from log where status != '200 OK' group by time::timestamp::date order by time::timestamp::date;`

`create view total_views as select time::timestamp::date, count(*) as num from log group by time::timestamp::date order by time::timestamp::date;`

### How To Run Project

Download the project zip file to you computer and unzip the file. Or clone this repository.
Place the project file inside the vagrant directory in your system alongside the newsdata.sql file.

Navigate to the vagrant directory in your virtual box and type in the following command:

`python log_analysis.py`

Your command line should display a neat tabular grid of the analysis performed.
