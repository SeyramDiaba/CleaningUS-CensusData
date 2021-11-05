import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import codecademylib3_seaborn
import glob



files = glob.glob('states*.csv')

temp = []
for file in files:
  data = pd.read_csv(file)
  temp.append(data)

us_census = pd.concat(temp)
# print(us_census.columns)
# print(us_census.dtypes)
print(us_census.head())
# remove dollar prefix sign from Income column
us_census['Income'] = us_census.Income.replace(['\$'],'',regex= True)

# Splitting gender column into separate columns of 'male' and 'female'.
print(us_census.GenderPop)
split_gender = us_census['GenderPop'].str.split('_',expand=True)
us_census['Male']= split_gender[0].str.split('(\d+)', expand = True)[1]
us_census['Female']= split_gender[1].str.split('(\d+)', expand = True)[1]

us_census['Male'] = pd.to_numeric(us_census['Male'])
us_census['Female'] = pd.to_numeric(us_census['Female'])
print(us_census.head())

plt.scatter(us_census['Female'],us_census['Income'])
plt.show()
plt.clf()
print(us_census.Female)

# Removing Non/nan Values
us_census['Female'] = us_census['Female'].fillna(us_census.TotalPop - us_census.Male)
print(us_census.Female)

# Checking for census duplicates
us_census_check= us_census.duplicated()
print(us_census_check)
# Drop duplicates
us_census= us_census.drop_duplicates()
print(us_census.head(10))
plt.scatter(us_census['Female'],us_census['Income'])
plt.show()
plt.clf()

print(us_census.columns)


# function to Clean races columns and strip %
def cleaner(df, column, character):
  df[column]=df[column].str.strip(character)
  df[column]=pd.to_numeric(df[column])
  #filling all NaN values with the average of the column
  df[column] = df[column].fillna(df[column].mean())
  return df[column]
  

# cleaner function call
us_census['Hispanic'] = cleaner(us_census,'Hispanic', '%') 
us_census['White'] = cleaner(us_census,'White', '%') 
us_census['Black'] = cleaner(us_census,'Black', '%')
us_census['Native'] = cleaner(us_census,'Native', '%')  
us_census['Asian'] = cleaner(us_census,'Asian', '%') 
us_census['Pacific'] = cleaner(us_census,'Pacific', '%')

# take out duplicates
us_census = us_census[['State','TotalPop','Hispanic','White','Black','Native','Asian','Pacific','Income','GenderPop','Male','Female']].drop_duplicates()
print(us_census)

# function to plot histogram
def plt_hist(df,column):
  plt.hist(df[column])
  plt.title(column)
  plt.show()
  plt.clf()

us_census['Hispanic'] = plt_hist(us_census, 'Hispanic')
us_census['White'] = plt_hist(us_census, 'White')
us_census['Black'] = plt_hist(us_census, 'Black')
us_census['Native'] = plt_hist(us_census, 'Native')
us_census['Asian'] = plt_hist(us_census, 'Asian')
us_census['Pacific'] = plt_hist(us_census, 'Pacific')

