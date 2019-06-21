> run probabilisticDatabase.py on command line as follows:
       probabilisticDatabase.py --query query.txt --table table1.txt --table table2.txt --table table3.txt
    where:
        query.txt contains the input query in first order logic
        table1.txt, table2.txt and table3.txt... contains probabilistic databases

OUTPUT FORMAT:
> If the input query is safe, then the program will print the probability of the query using lifted inference. It will also compute the probability of query using Monte Carlo, Gibbs and Mentropolis-Hastings separately and plot the error of the sampling techniques against the value obtained from lifted inference for validation. 
> If the input query is hard, then the program will give the probability of the query by running three different sampling methods separately: Monte Carlo, Gibbs and Metropolis-Hastings        