import pandas as pd 
import numpy as np
import re

df = pd.read_csv('customers.csv')

## Step1 - We will remove all the duplicates from the csv if any

df = df.drop_duplicates()

## Step 2 - We will define a function which will check the validity of the emails using regex(regular expression) and will change all the invalid emails with NaN

def is_valid_email(email):
    if pd.isna(email):
        return False
    
    return re.match(r"[^@]+@[^@]+\.[^@]+", str(email)) is not None

df['email'] = df['email'].apply(lambda x: x if is_valid_email(x) else np.nan)

## Step 3: Now we will remove all the issues with age(for example if age is 0 or negative) and replace it with the median age

valid_ages = df['age'].dropna()
valid_ages = valid_ages[valid_ages > 0]
median_age = valid_ages.median()
df['age'] = df['age'].apply(lambda x: median_age if pd.isna(x) or x <= 0 else x)

## Step 4: In this step we will fill the missing name and cities or emails with a fixed name

df['name'] = df['name'].fillna('Tanay')
df['city'] = df['city'].fillna('Pune')
df['email'] = df['email'].fillna('abc@gmail.com')

print(df)

## Step 5: Now we will store this cleaned and processed csv into a new filw using pandas inbuilt function

df.to_csv('customers_cleaned2.csv', index=False)

print("Data cleaning completed. Cleaned data saved to 'customers_cleaned.csv'.")


## Personal Note= Run one step at a time by commenting all the steps below