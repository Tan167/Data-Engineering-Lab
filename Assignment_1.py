import pandas as pd
import numpy as np
import re


## Step 1: We will first Load the csv file using pandas in variable name df

df = pd.read_csv('sorted_employee_data.csv')

## Step 2: In this step we will try to remove all the duplicates using drop_duplicate() in built function

df = df.drop_duplicates()


## Step 3: In this step we will check the validity using the the regex(regular expression) and for invalid emails we will convert it into NaN using Lambda Function

def is_valid_email(email):
    if pd.isna(email):
        return False
    return re.match(r"[^@]+@[^@]+\.[^@]+", str(email)) is not None

df['email'] = df['email'].apply(lambda x: x if is_valid_email(x) else np.nan)


## Step 4: In this step we will first convert the dates given into standard format 

df['joining_date'] = pd.to_datetime(df['joining_date'], dayfirst=True)


## Step 5: In this step we will replace the empty cell in date column with the with a fixed date so we can make sure which date was missing but also ensure the cell is filled so it does not disturb during analysis

fixed_date = pd.Timestamp('2000-01-01')
df['joining_date'].fillna(fixed_date, inplace=True)


## Step 6: In this step we will assign each employee and uniques employee_id as in this case 2 employees is having the same emp_id by reassigning all the employees emp_id sequentially

df['emp_id'] = range(101, 101 + len(df))


## Step 7: In this step we will first convert the salary into numneric form(in case someone has entered string in the cell) the drop the invalid values and replace them with the meidan salary

df['salary'] = pd.to_numeric(df['salary'])
valid_salaries = df['salary'].dropna()
valid_salaries = valid_salaries[valid_salaries > 0]
median_salary = valid_salaries.median()
df['salary'] = df['salary'].apply(lambda x: median_salary if pd.isna(x) or x <= 0 else x)

## Step 8: In this step we will fill the empty values in name,email and department columns (if any) with a fixed name,email and department

df['email'] = df['email'].fillna('Random@gmail.com')
df['name'] = df['name'].fillna('Tanay')
df['department'] = df['department'].fillna('Customer Support')


## Step 9: In this we can see in department column there are different name for same department (in this case IT and HR have issues HR is also written as hr and Human resourses which means the same thing) so we need to fix that

df['department'] = df['department'].str.strip().str.lower() # this helps to make all the names in lower case

df['department'] = df['department'].replace({
    'hr': 'Human Resources',
    'human resources': 'Human Resources',
    'it': 'Information Technology',
    'information technology': 'Information Technology',
    'finance' : 'Finance'
})



## Step 10: In this step we will export the cleaned file to a new file and save it to our folder and print the end statement

df.to_csv('employee_cleaned2.csv', index=False)
print("Data cleaning completed. Cleaned data saved to 'employee_cleaned.csv'.")
print(df)
