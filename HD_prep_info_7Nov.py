#!/usr/bin/env python
# coding: utf-8

# In[233]:


# 08/2025
# Load distance matrices, generate isomap/Umap
# Join the above generated shape info with Database-specific infomation
#     add function_info to make complete_info
# Verifications
# Save the csv file if needed


# In[1]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# In[ ]:





# In[2]:


curProject = 'HD'
curRegion = 'CS'  # CSSyl or CSpreCS
curRoot = 'C'  # 'C' or 'D'


# In[3]:


#######################################  load distances  #####################################

##  reading from the basic analysis  ##
distance_path_min = rf'{curRoot}:\B_projWIP\proj_{curProject}\WINHD_MOTOHD_HDTRACK\{curRegion}\Isomap\minDist{curRegion}.txt'
distance_path_max = rf'{curRoot}:\B_projWIP\proj_{curProject}\WINHD_MOTOHD_HDTRACK\{curRegion}\Isomap\maxDist{curRegion}.txt'

try:
    minDist = pd.read_csv(distance_path_min, index_col=0, header=0)
    maxDist = pd.read_csv(distance_path_max, index_col=0, header=0)    
except FileNotFoundError as e:
    print(f"Error: {e}")

rows, cols = minDist.shape
print(f"Number of rows: {rows}")
print(f"Number of columns: {cols}")


# In[ ]:





# In[13]:


################################    generation of Isomap    ##################################
# generation of isomaps using minDist and maxDist, all subjects, NO selection
# Define: outNameMin/Max, outFileNameMin/Max

from sklearn.manifold import Isomap
numDim = 3
numNeig = 10
genIsomap = False  ## !!!!!!!!!!!!!  default to False, True only after varification  !!!!!!!!!!!!!

outNameMin = 'isomapCmds'+curRegion+'k'+str(numNeig)+'d'+str(numDim)+'distmin'+'.txt'
outNameMax = 'isomapCmds'+curRegion+'k'+str(numNeig)+'d'+str(numDim)+'distmax'+'.txt'

outFileNameMin = rf'{curRoot}:\B_projWIP\proj_{curProject}\Analysis_2025\form_measure\isomap\{outNameMin}'
outFileNameMax = rf'{curRoot}:\B_projWIP\proj_{curProject}\Analysis_2025\form_measure\isomap\{outNameMax}'

subjNames = minDist.index
dimNames = np.arange(1,numDim+1)
iso_min = Isomap(n_neighbors=numNeig,n_components=numDim,metric='precomputed').fit_transform(minDist.values)
iso_min_DF = pd.DataFrame(iso_min,index=subjNames,columns=dimNames)
iso_max = Isomap(n_neighbors=numNeig,n_components=numDim,metric='precomputed').fit_transform(maxDist.values)
iso_max_DF = pd.DataFrame(iso_max,index=subjNames,columns=dimNames)

# SAVE Isomaps as csv
print(outFileNameMin)
print(outFileNameMax)
if genIsomap:
    iso_min_DF.to_csv(outFileNameMin,index_label='subjName')
    iso_max_DF.to_csv(outFileNameMax,index_label='subjName')


# In[31]:


###############################   generation of UMAP   ################################
# UMAP for the original distance WITHOUT selection of subjects
import umap
import random

# to ensure that the results are always the same
SEED = 42
np.random.seed(SEED)
random.seed(SEED)

writeUMAP = False     # default to False, True only after varification            ###   CHANGE   ###

typeDist = 'min'   # using minimum or maximum distance matrix                     ###   CHANGE   ###
n_comp = 1         # Change this to the desired number of dimensions: 1 or 2      ###   CHANGE   ###
n_neighbors = 5    # Change this to the desired number of neighbors: 5 or 30      ###   CHANGE   ###
min_dist = 0.2     # Change this to the desired minimum distance
# define df for UMAP generation
if (typeDist == 'min'):
    df = minDist    
if (typeDist == 'max'):
    df = maxDist        
    
###############################  define output file name  ############################
outName = 'dim'+str(n_comp)+'_'+typeDist+'_neig'+str(n_neighbors)+'_dist'+str(min_dist)+'.txt'
###############################  define output file path  ############################   

curTypeAnalysis = 'main_piece_analysis' # 'basic_analysis'  ##  !!!!!!!!   CHANGE  !!!!!!!!
outFileName = rf'{curRoot}:\B_projWIP\proj_{curProject}\Analysis_2025\form_measure\umap_{curRegion}\{outName}'
##############################################################################################################################
# perform UMAP
reducer = umap.UMAP(metric='precomputed', n_components=n_comp,n_neighbors=n_neighbors,min_dist=min_dist,random_state=SEED)
embedding = reducer.fit_transform(df)

# Create a DataFrame for the embedding
if n_comp == 1:
    embedding_df = pd.DataFrame(embedding, columns=['UMAP1']) 
if n_comp == 2:
    embedding_df = pd.DataFrame(embedding, columns=['UMAP1', 'UMAP2'])
if n_comp == 3:
    embedding_df = pd.DataFrame(embedding, columns=['UMAP1', 'UMAP2', 'UMAP3'])
embedding_df.index = df.index

print(embedding_df)
print(outFileName)
# Save as csv
if writeUMAP:
    embedding_df.to_csv(outFileName,index_label='subjName')


# In[ ]:





# In[ ]:





# In[ ]:





# In[33]:


##########################  Load shape measures, if generated and written above  #############################
curDistType = 'min'                                         ##############   CHANGE  ###############
curTypeAnalysis = 'form_measure'                            ##############   CHANGE  ###############
#curTypeAnalysis = 'main_piece_analysis' 

shape_path = rf'{curRoot}:\B_projWIP\proj_{curProject}\Analysis_2025\{curTypeAnalysis}\isomap\isomapCmds{curRegion}k10d3dist{curDistType}.txt'
shapeU_1_path = rf'{curRoot}:\B_projWIP\proj_{curProject}\Analysis_2025\{curTypeAnalysis}\umap_{curRegion}\dim1_{curDistType}_neig5_dist0.2.txt'
shapeU_2_path = rf'{curRoot}:\B_projWIP\proj_{curProject}\Analysis_2025\{curTypeAnalysis}\umap_{curRegion}\dim1_{curDistType}_neig30_dist0.2.txt'
shapeU_3_path = rf'{curRoot}:\B_projWIP\proj_{curProject}\Analysis_2025\{curTypeAnalysis}\umap_{curRegion}\dim2_{curDistType}_neig5_dist0.2.txt'
shapeU_4_path = rf'{curRoot}:\B_projWIP\proj_{curProject}\Analysis_2025\{curTypeAnalysis}\umap_{curRegion}\dim2_{curDistType}_neig30_dist0.2.txt'


# In[35]:


#######################  Load shape information  #######################
shape = shapeU_1 = shapeU_2 = shapeU_3 = shapeU_4 = None
try:
    shape = pd.read_csv(shape_path, index_col=0, header=0)
    #print(shape.head())
    shapeU_1 = pd.read_csv(shapeU_1_path, index_col=0, header=0)
    shapeU_2 = pd.read_csv(shapeU_2_path, index_col=0, header=0)
    shapeU_3 = pd.read_csv(shapeU_3_path, index_col=0, header=0)
    shapeU_4 = pd.read_csv(shapeU_4_path, index_col=0, header=0)

    shape.rename(columns={'1':'iso1'}, inplace=True)
    shape.rename(columns={'2':'iso2'}, inplace=True)
    shape.rename(columns={'3':'iso3'}, inplace=True)    
    shapeU_1.rename(columns={'UMAP1': 'UMAP1_U1'}, inplace=True)
    shapeU_2.rename(columns={'UMAP1': 'UMAP1_U2'}, inplace=True)
    shapeU_3.rename(columns={'UMAP1': 'UMAP1_U3', 'UMAP2': 'UMAP2_U3'}, inplace=True)
    shapeU_4.rename(columns={'UMAP1': 'UMAP1_U4', 'UMAP2': 'UMAP2_U4'}, inplace=True)
    #shapeU_4.rename(columns={'UMAP1': 'UMAP1_U4', 'UMAP2': 'UMAP2_U4','UMAP3': 'UMAP3_U4'}, inplace=True)
except FileNotFoundError as e:
    print(f"Error: {e}")

if all(df is not None for df in [shape, shapeU_1, shapeU_2, shapeU_3, shapeU_4]):
    shape_joined = shape.join([shapeU_1, shapeU_2, shapeU_3, shapeU_4])
    shape = shape_joined
    print(shape.head())
    print(shape.index)
else:
    print("One or more input files were missing — join was not performed.")
    


# In[37]:


###############################  Proecssing the shape file  ################################
# Add a 'SubjID' column, based on index, removing L, filp_R as prefix
# Add a 'Hemisphere' column (Left if index starts with L or Right if index starts with flip)

# Create SubjID from index, removing pre_fix and post_fix
shape['SubjID'] = (
    shape.index
    .to_series()  # convert index to a Series so we can use string operations
    .astype(str)   # convert index values to strings
    .str.replace(r'^(L|flip-R)', '', regex=True)   # remove 'L' or 'flip-R' at start
)
shape['SubjID'] = shape['SubjID'].astype(str) # Make sure SubjID is string
shape['Study'] = 'MOTOHD' # Default Study = MOTOHD
shape.loc[shape['SubjID'].str.startswith('v'), 'Study'] = 'HDTRACK' # Assign HDTRACT where SubjID starts with 'v'
shape.loc[shape['SubjID'].str.startswith('W'), 'Study'] = 'WINHD' # Assign HDTRACT where SubjID starts with 'v'

# Create 'Hemisphere' based on index prefix
#shape['Hemisphere'] = shape.index.to_series().apply(
#shape['Hemisphere'] = shape[subjName].apply(
#    lambda x: 'Left' if x.startswith('L') else 'Right' if x.startswith('flip-R') else None
#)
shape['Hemisphere'] = shape.index.to_series().astype(str).apply(
    lambda x: 'Left' if x.startswith('L') else 'Right' if x.startswith('flip-R') else None
)

shape = shape.reset_index()

#print(shape.head())
print(shape.columns)
print(shape)


# In[ ]:





# In[ ]:





# In[ ]:





# In[93]:


##################################### Prepare Database-specific infomation ####################################
# Load anatomical and functional info 
HDTRACK_info_path = rf'{curRoot}:\B_projWIP\proj_{curProject}\{curProject}_INFO_result\HD_Track_cleaned_filled.csv'
WINHD_info_path = rf'{curRoot}:\B_projWIP\proj_{curProject}\{curProject}_INFO_result\WIN_HD.csv'
MOTOHD_info_path = rf'{curRoot}:\B_projWIP\proj_{curProject}\{curProject}_INFO_result\MOTO_HD_cleaned.csv'

HDTRACK_info, WINHD_info, MOTOHD_info = None, None, None

try:
    WINHD_info = pd.read_csv(WINHD_info_path, index_col=0, header=0, sep=';', encoding='latin1')
    MOTOHD_info = pd.read_csv(MOTOHD_info_path, index_col=0, header=0, sep=';', encoding='latin1')
    HDTRACK_info = pd.read_csv(HDTRACK_info_path, index_col=0, header=0, sep=';', encoding='latin1')
except FileNotFoundError as e:
    print(f"Error: {e}")

if WINHD_info is not None:  
    WINHD_info.index.name = 'Subject'                     # rename index from the original 'File Name' to 'Subject'
    WINHD_info = WINHD_info.reset_index()                 # set the index as a col
    WINHD_info = WINHD_info.drop(columns=['Unnamed: 1'])  # remove col created by trailing ';' in CSV file
    WINHD_info.drop(['DDN','Date IRM','UHDRS'], axis=1, inplace=True)   
    WINHD_info = WINHD_info.rename(columns={"Age à l'IRM": "Age","Sexe":"Sex"})
    WINHD_info['Diag'] = WINHD_info['Diag'].replace('MH','MH_premanifest')
if MOTOHD_info is not None:
    MOTOHD_info.index.name = 'Subject'
    MOTOHD_info = MOTOHD_info.reset_index()
    MOTOHD_info.drop(['DDN','Date IRM'], axis=1, inplace=True)
    MOTOHD_info = MOTOHD_info.rename(columns={"Age at IRM":"Age","Sexe":"Sex"})
    MOTOHD_info['Diag'] = np.where(MOTOHD_info['UHDRS'] >= 5, 'MH', 'MH_premanifest')  # create Diag col, set value <5 as MH_premanifest
if HDTRACK_info is not None:
    HDTRACK_info.index.name = 'Subject'
    HDTRACK_info = HDTRACK_info.reset_index()
    HDTRACK_info.drop(['DDN','Date IRM'],axis=1, inplace=True)
    HDTRACK_info = HDTRACK_info.rename(columns={"Age at IRM":"Age","Sexe":"Sex","Allèle muté":"CAG"," Allele normal":"CAG_normalAllele"})
    #HDTRACK_info = HDTRACK_info.fillna({'CAG': 19, 'CAG_normalAllele': 19})  # verified that all NA are controls, 18-20 repeats on average
else:
    print("Info could not be loaded. Aborting further steps.")
"""
print(len(WINHD_info))
print(WINHD_info.columns)
print(WINHD_info.index.name)
print(WINHD_info.head())
print("Original data types:\n", WINHD_info.dtypes)

print(len(MOTOHD_info))
print(MOTOHD_info.columns)
print(MOTOHD_info.index.name)
print(MOTOHD_info.head())
print("Original data types:\n", MOTOHD_info.dtypes)
"""
print(len(HDTRACK_info))
print(HDTRACK_info.columns)
print(HDTRACK_info.index.name)
print(HDTRACK_info.head())
print("Original data types:\n", HDTRACK_info.dtypes)


# In[ ]:





# In[ ]:





# In[ ]:





# In[242]:


##################  Merging the ori shape_info with the function_info to make complete_info  ###################

#complete_info = shape_info.merge(function_info,on=['Group', 'Group_num'],left_index=True,right_index=True,how='left')
complete_info = shape_info.merge(function_info, on=['SubjID', 'Group','Group_num'], how='left')
complete_info = complete_info.reset_index()   # make 'SubjID' a column
complete_info['Study'] = complete_info['Study'].fillna(1)

"""
# Move the subjID (function_info) column next to SubjID (shape_info) for visual inspection
cols = list(complete_info.columns)               # current column order
cols.remove('subjID')                    # take out colB
insert_pos = cols.index('SubjID') + 1    # position right after colA
cols.insert(insert_pos, 'subjID')        # insert colB in the right place
complete_info = complete_info[cols]                          # reorder DataFrame

# Rename subjID (function_info) to SubjID_function, SubjID (amputee_info) to SubjID_amputeeS
complete_info.rename(columns={'subjID': 'SubjID_function'}, inplace=True)
complete_info.rename(columns={'SubjID': 'SubjID_amputee'}, inplace=True)
"""
print(complete_info.columns)
#print(complete_info.head())
#print("Original data types:\n", complete_info.dtypes)
print(len(complete_info))
#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#    print(complete_info)
#    print(shape)


# In[243]:


##########################  Merging shape (Isomap/Umap) and complete_info  ###########################
merged_info = shape.merge(complete_info, on=['SubjID','Study'], how='left')  # left join, keep all the rows
merged_info.set_index('subjName', inplace=True)
#print(merged_info.head())
print(merged_info.columns)
print(len(merged_info))


# In[244]:


#########################  Adding missing_hem column to the final complete_info  ##########################

# Default all to 'None'
merged_info['missing_hem'] = 'None'

# Set 'R' where AmpSide is 'L'
merged_info.loc[merged_info['AmpSide'] == 'L', 'missing_hem'] = 'R'

# Set 'L' where AmpSide is 'R'
merged_info.loc[merged_info['AmpSide'] == 'R', 'missing_hem'] = 'L'


# In[ ]:





# In[ ]:





# In[ ]:





# In[245]:


###########################################  Verifications  ###########################################


# In[246]:


print(merged_info.columns)


# In[247]:


ctl_counts = shape_info['Group_num'].value_counts()
print(ctl_counts)
ctl_counts = function_info['Group_num'].value_counts()
print(ctl_counts)
ctl_counts = merged_info['Group_num'].value_counts()
print(ctl_counts)


# In[248]:


####################  Display the values of a specific column  ####################
print("Values in the 'iso1' column:")
print(merged_info['iso1'])

####################  Display the rows with a specific column value  ####################
cer = merged_info[merged_info['Group'] == 1]
#print(cer['Category'])

####################  Get a summary of statistics  ####################
summary_stats = merged_info['iso1'].describe()
print("\nSummary statistics for the 'isomap1' column:")
print(summary_stats)

####################  Detect null values in a specific column  ###################
null_values = merged_info['Group'].isnull()
#print(null_values)

####################  Filter rows where the specified column has null values  #####################
null_rows = merged_info[merged_info['iso1'].isnull()]
#print(null_rows['1'])

####################  Count the number of null values in a specific column  ######################
null_count = merged_info['iso1'].isnull().sum()
print(f"Number of null values in selected column: {null_count}")


# In[ ]:





# In[ ]:





# In[282]:


################################  Saving csv files if needed  #################################
file_path = rf'{curRoot}:\B_projWIP\proj_{curProject}\Analysis_2025\{curRegion}_combined_{curDistType}.csv'
print(file_path)

# Write the DataFrame to a CSV file
#merged_info.to_csv(file_path, index=True)

################################  Test read the CSV file back into a DataFrame  ################################
#df_loaded = pd.read_csv(file_path)
#print(len(df_loaded))
#print("Data types:\n", df_loaded.dtypes)


# In[ ]:




