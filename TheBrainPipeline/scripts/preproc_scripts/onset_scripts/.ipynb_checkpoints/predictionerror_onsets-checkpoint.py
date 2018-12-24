
# coding: utf-8

# In[67]:


import pandas as pd
import glob



print("___________________________________________________________________")
print("STARTING PROGRAM..................................................")
handles = []


f = glob.glob('*.log')
for l in f:
    handles.append(open(l))
for l in f: 
    data = pd.read_table(l, header=None)

with open('subject_conversion.txt', 'r') as file:
    contents = file.readlines()
data.describe()


# In[68]:


def get_subject():
    for handle in range(0, len(handles)):
        global subject_name
        global sub_num 
        subject_name = handles[handle].name.split('-')[0]
        match = [s for s in contents if subject_name in s]
        print(type(match))
        for s in match:
            sub_num = s.split(" ")[2]
            sub_num = sub_num.strip("\n")
        
            
     
print("GETTING SUBJECTS..................................................")            

print("SUBJECT NAME.................................................."+subject_name)
print("SUBJECT NUMBER.................................................."+sub_num)


# In[69]:


data.dtypes


# In[70]:


data.columns = ['Onset', 'Type','Keypress']
data.head()


# In[71]:


print("___________________________________________________________________")
print("PREDICTION ERROR IMAGES.................................................")
predictionerror = data[data['Type'].str.contains("Level image=tasty.jpg")==True].copy()
predictionerror


# In[73]:


temp_df = pd.DataFrame()

for index,row in predictionerror.iterrows():
    if "image" in row['Type']:
        # make a test case & keep track of index
        temp_index = index 
        for i in range(1,3):
            temp_row = data.loc[temp_index+i]
            img = row
            condition_case = data.loc[temp_index+i, "Type"]
            if "2" in condition_case:
                
                temp_df = temp_df.append(pd.Series(img, index=predictionerror.columns))
                temp_df = temp_df.append(pd.Series(temp_row, index=predictionerror.columns))
                
print("PREDICTION ERROR ONSETS..................................................")
            
temp_df.sort_values('Onset')
cols = temp_df.columns.tolist()
cols = cols[1::] + cols[0:1]
temp_df = temp_df[cols]
temp_df


# In[74]:


print("WRITING TO FILE..................................................")
temp_df.to_csv(sub_num+'_task-predictionerror_events.tsv', sep='\t', index=False)
print("___________________________________________________________________")


# In[75]:


print("NORMAL IMAGES.................................................")
normalevents=data[data['Type'].str.contains("Level image=not_tasty")==True].copy()
normalevents


# In[77]:


for index,row in normalevents.iterrows():
    if "image" in row['Type']:
        # make a test case & keep track of index
        temp_index = index 
        for i in range(1,3):
            temp_row = data.loc[temp_index+i]
            
            condition_case = data.loc[temp_index+i, "Type"]
            if "Level injecting" in condition_case:
                img = row
                normalevents= normalevents.append(pd.Series(temp_row, index=normalevents.columns))

print("NORMAL ONSETS..................................................")
            
normalevents.sort_values('Onset')


# In[80]:


print("WRITING TO FILE..................................................")
normalevents.to_csv(sub_num+'_task-normal_events.tsv', sep='\t', index=False)
print("..................................................FINISHED PROGRAM")
print("___________________________________________________________________")

