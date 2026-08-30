
# import pandas as pd



# data = {
#     'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Evan'],
#     'age': [25, 30, 35, 28, 22],
#     'city': ['NYC', 'LA', 'NYC', 'Chicago', 'LA'],
#     'salary': [70000, 90000, 120000, 85000, 60000]
# }




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

data = {
    'order_id': [1, 2, 3, 4, 5, 6],
    'customer': ['Alice', 'Bob', 'Alice', 'Charlie', 'Bob', 'Alice'],
    'amount': [200, 150, 300, 100, 250, 180],
    'status': ['completed', 'pending', 'completed', 'cancelled', 'completed', 'pending']
}

df = pd.DataFrame(data)

print(df.groupby('customer')['amount'].sum())

print(df.groupby('customer')['order_id'].count().reset_index(name='customer_orders'))

completed = df[df['status'] == 'completed']
print(completed.groupby('customer')['amount'].sum())
