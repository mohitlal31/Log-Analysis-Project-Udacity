# Log Analysis Project

A simple reporting tool to present important details about a newspaper website
 
The project uses python code to read the postgreSQL databases 
and presents answers to 3 important questions about the data.

### Required Libraries and Dependencies
The project uses the python library [Tabulate](https://pypi.org/project/tabulate/) to present the analysis
in a neat tabular grid.
To Install Tabulate, from the command line in your virtual box, run 

`pip install tabulate`

Refer [Tabulate Installation](https://pypi.org/project/tabulate/) for more information.

### Create Views

Before running the python program, you need to create the pre-requisite postgreSQL database views which are used by the python code.
From the vagrant directory in your virtual box, run

`psql -d news`

Then run the following postgreSQL queries from the command line in the same order 

`create view top_paths as select path, count(*) as num from log where log.status = '200 OK' group by path order by num desc;`
`create view top_articles as select articles.author, articles.title, top_paths.num from articles, top_paths where top_paths.path like '%' || articles.slug || '%';`
`create view top_authors as select top_articles.author, sum(top_articles.num) as num_views from authors, top_articles group by top_articles.author order by num_views desc;`
`create view failed_views as select time::timestamp::date, count(*) as num from log where status != '200 OK' group by time::timestamp::date order by time::timestamp::date;`
`create view total_views as select time::timestamp::date, count(*) as num from log group by time::timestamp::date order by time::timestamp::date;`

### How To Run Project

Download the project zip file to you computer and unzip the file. Or clone this repository.
Place the project file inside the vagrant directory in your system alongside the newsdata.sql file.
if you haven't installed virtual box and vagrant, please refer to the udacity course for more details.

Navigate to the vagrant directory in your virtual box and type in the following command:

`python log_analysis.py`

Your command line should display a neat tabular grid of the analysis performed.
