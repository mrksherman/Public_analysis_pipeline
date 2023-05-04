import streamlit as st
import time
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="Base analysis", page_icon="📈", layout='wide')

st.markdown("# Base Analysis")
st.sidebar.header("Base Analysis")
st.write(
    """
    This explorer allows you to view the distribution of bases across the datasets
    """
)

Big_df = pd.read_csv('../Output/Alldata.csv')


chosen = st.radio(
    'Which analysis would you like to view?',
    ("Raw", "Normalized"))

sns.set(rc={'figure.figsize':(11.7,5.27)})
f, axes = plt.subplots(1, 3)

if chosen == 'Raw':
    Q3df_DMSO=Big_df.loc[(Big_df['Compound']=='DMSO')]
    Q3df_2A3=Big_df.loc[(Big_df['Compound']=='2A3')]
    Q3df_DMS=Big_df.loc[(Big_df['Compound']=='DMS')]
    boxDMSO=sns.boxplot( y=Q3df_DMSO['Reactivity'], x= Q3df_DMSO['Reference_sequence'].replace('T','U'),  orient='v' , ax=axes[0])
    box2A3=sns.boxplot(  y=Q3df_2A3['Reactivity'], x= Q3df_2A3['Reference_sequence'].replace('T','U'),  orient='v' , ax=axes[1]).set_title('2A3')
    boxDMS=sns.boxplot(  y=Q3df_DMS['Reactivity'], x= Q3df_DMS['Reference_sequence'].replace('T','U'),  orient='v' , ax=axes[2]).set_title('DMS')
elif chosen == 'Normalized':
    Q3df_DMSO=Big_df.loc[(Big_df['Compound']=='DMSO')]
    Q3df_DMSO.dropna()
    Q3df_2A3=Big_df.loc[(Big_df['Compound']=='2A3')]
    Q3df_2A3.dropna()
    Q3df_DMS=Big_df.loc[(Big_df['Compound']=='DMS')]
    Q3df_DMS.dropna()
    box2A3=sns.boxplot(  y=Q3df_2A3['Normalized_Reactivity'].astype(float), x= Q3df_2A3['Reference_sequence'].replace('T','U'),  orient='v' , ax=axes[1]).set_title('2A3')
    boxDMS=sns.boxplot(  y=Q3df_DMS['Normalized_Reactivity'].astype(float), x= Q3df_DMS['Reference_sequence'].replace('T','U'),  orient='v' , ax=axes[2]).set_title('DMS')


st.write(f'{chosen} Individual distribution of mutation frequencies across nucleotides')
st.pyplot(f)