
# import pandas as pd



# data = {
#     'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Evan'],
#     'age': [25, 30, 35, 28, 22],
#     'city': ['NYC', 'LA', 'NYC', 'Chicago', 'LA'],
#     'salary': [70000, 90000, 120000, 85000, 60000]
# }



# df = pd.DataFrame(data)

# print(df[df['salary'] >= 85000])
# print(df.head())

# print(df.shape)

# print(df.info())

# print(df.describe())

# print(df.dtypes)

#print(df['city']) 

#print(df[['name','salary']])

#print(df[df['age'] > 25])

#print(df[(df['age'] > 25) & (df['city'] == 'NYC')])

#print(df[(df['age'] > 25) | (df['city'] == 'NYC')])

#print(df[df['salary'] >= 85000])

# print(df.isnull().sum())



import pandas as pd


data2 = {
    'name': ['Alice', 'Bob', None, 'Diana', 'Evan'],
    'age': [25, None, 35, 28, None],
    'city': ['NYC', 'LA', 'NYC', None, 'LA'],
    'salary': [70000, 90000, None, 85000, 60000]
}

df2 = pd.DataFrame(data2)

print(df2)