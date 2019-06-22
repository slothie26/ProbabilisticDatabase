#Probabilistic Database System
The system takes as input a fully quantified
query in first-order logic and efficiently computes
the probability of the input query. Our probabilistic
database system is capable of evaluating both safe
queries as well as hard queries. The project is based on the lifted inference algorithm shared and uses as reference [1].

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Python 3.7.1
Numpy 1.14.6
Scipy 1.1.0
Matplotlib 2.2.4

### Setup

The following files need to be created before the code can be successfully run.
query.txt - holds the query string that needs to be evaluated
table1.txt ... tablen.txt will hold each of the 'n' tables
The format of each of the files is disucussed [here](###Formating the Input Files).
A sample set of hese files is already created and shared in the repository.

###Formating the Input Files

####query.txt

The query needs to be a UCQ: Union of quantified conjunctive queries. Each conjunctive query is seperated with '||'. Within each conjunctive query, every clause is seperated with ','.  Table names are denoted wih capital letters and represent a single clause. Every table has comma seperated variables as arguments. Variables are denoted with strings of letters starting with a lower case letter. Ultimately, the query file will contain a single query rule

####table.txt
Each table file represents a single table. The first line in the table file denotes the table name(Capital letter).  The file is organised similar to a CSV. Every line in the table represents a single tuple. Each column of each tuple is seperated with a comma. The last comumn of each tuple represents the probability that the tuple is in the database.

## Running the code

The example provided can be run as follows.
```probabilisticDatabase.py --query query.txt --table table1.txt --table table2.txt --table table3.txt```

The number of tables included depend on the query that is being tested.
### Expected output

If the input query is safe, then the program will print the probability of the query using lifted inference. It will also compute the probability of query using Monte Carlo, Gibbs and Mentropolis-Hastings separately and plot the error of the sampling techniques against the value obtained from lifted inference for validation. 

If the input query is hard, then the program will give the probability of the query by running three different sampling methods separately: Monte Carlo, Gibbs and Metropolis-Hastings

### Sample Queries
Some sample queries and their results have been shared in queries_tested.txt



## Contributors

Vidhu Malik (Author)
Vishwa Karia
Zeel Doshi
Vaishnavi Pendse

##References
[1]: Van den Broeck, Guy and Suciu, Dan. Query Processing on Probabilistic Data: A Survey. Foundations
and Trends in Databases. Now Publishers, 2017. doi: 10.1561/1900000052
        