import pandas as pd
import json

"""This is a python file for cleaning the data
It was built to be somewhat readable for non python users
It was not built to be "Optimal", (running the analysis in Python vs Excel
 already gives us a large enough performance boost), 
 this is why alot of print statements have been left.

 
 We used an LLM tool for building this (Claude Code), but it was used for help with syntaxt.
 "Cognetive offload" (where the LLM thinks for you) is extremely dangerous and we wanted to avoid it
 """
input = pd.read_csv("../../../bel20_2026.csv") 


#### 1 Converting the raw data into a more usable format
df_vals = input.set_index('Ticker')

df_vals = df_vals.transpose()

df_vals.index = pd.to_datetime(df_vals.index)

print("############# New data format: #######")
print(df_vals.info())

#### Compouting average geometric returns

#We use a simple (readable) hand built python function for this

print("We see that we are missing 125 entries for SYENS. ") #TODO Write in the paper about this, what do we assume etc

def avg_geo_return(time_series_list : list, test : bool = False):
    """ Takes a list of values, and calculates the 
     average geometric change per unit of time (assuming each entry
     is one unit if time).
      
    See the latex in the prelim report for this logic written out in
     a readable manner for non pyton users """
    starting_value = time_series_list[0]
    ending_value = time_series_list[-1]
    nr_time_period = len(time_series_list) -1 #With N entries there are N -1 time periods
    increase_multiplier = ending_value / starting_value
    avg_geo_change = increase_multiplier**(1/nr_time_period)

    if test == True:
        print("Total increase multiplier")
        print(increase_multiplier)
        print("Average geo change per time period")
        print(avg_geo_change)

    return avg_geo_change

#We test that the function:)
print("####### Testing for APAM ##########")
APAM_list = df_vals['APAM'].tolist()    #List of returns for APAM
avg_geo_return(APAM_list, test = True)  

#### We run a for loop to calculate avg geo return for all tickers
#Which we store in a list afterwards
exp_ret_list = list()

for ticker in df_vals.columns:
    ticker_values = df_vals[ticker].dropna().to_list() 
    #For a given ticker, we drop NA values. See the report for a discussion of the 
    #implications of this
    exp_ret_list.append(avg_geo_return(ticker_values))
#Note that computing it like this gives us the avg geo return over the entire time horizon



#### Computing covariance matrix

""" 
Up until now we have been working with the absolute values of the stocks

For our analysis, this is not an interesting metric. We are interested in the percentage change of the value of 
the stock
"""

df_delta = df_vals.pct_change()

print("############ Testing for pct change transformation #######")
print("Delta")
print(df_delta.head(n=3))
print("Absolute vals")
print(df_vals.head(n=3))
print("Just take a calculator and run the numbers")

print('############ covariance matrix ########')

cov_matrix = df_delta.cov() 
""" This computes the pairvise (sample) conveariance, this excludes all NA values from
#the computation. Which is the behaviour we want. So entries where SYENS = NA is not considered
Since the computations are pairwise the NA values for SYENS do not affecf cov pairs that SYENS is not a part of

The documenation explains this function: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.cov.html#pandas.DataFrame.cov
"""

print(cov_matrix)

test_dict = {"key1" : "value1", "key2" : "value2"}

#### Writing the cleaned data into a json file

data_cleaned = {
    "ticker_list" : df_vals.columns.to_list(),
    "exp_ret_list" : exp_ret_list,
    "cov_nested_list" : cov_matrix.values.tolist()
}

with open("data_cleaned.json", "w") as f:
    json.dump(data_cleaned,f)

