import pandas as pd
import twint
import numpy as np
import os
import time

# directory to store files
to_path = "data/lex_all_tweets/"

# query
query = '(lex AND fridman) OR (lexfridman)'

# latest date wanted
last_date = "2021-10-01"

print(query)
attempts = 0

# 3 attempts because it errors often
while attempts<3:
    print("attempts",attempts)
    error = 0
    
    # again, errors often, 5 attempts
    while error<5:
        try:
            print(error,"trying with",to_path+last_date+".csv")
            c = twint.Config()
            c.Until = last_date
            c.Search = query
            c.Output = to_path+last_date+".csv"
            c.Store_csv = True
            c.Hide_output = True
            twint.run.Search(c)
            time.sleep(1)
            break

        except Exception as e:
            print(e)
            error+=1
            time.sleep(1)

    
    # gets used if errors. finds last date in csv, and starts again from there
    if os.path.isfile(to_path+last_date+".csv"):
        print("file was created")
        check_df = pd.read_csv(to_path+last_date+".csv")
        old_last_date = last_date
        last_date = check_df.iloc[-1]["date"]

        print(old_last_date)
        print(last_date)
        print()
        
        # if its just repeating same date, program finished 
        if last_date==old_last_date:
            print("adding attempt")
            attempts+=1

    else:
        break