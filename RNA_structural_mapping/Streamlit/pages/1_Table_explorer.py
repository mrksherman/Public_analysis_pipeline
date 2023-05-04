import streamlit as st
import time
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


st.set_page_config(page_title="Table explorer", page_icon="📈", layout= 'wide')

st.markdown("# Table Explorer")
st.sidebar.header("Table Explorer")
st.write(
    """
    This explorer allows you to modify the analysis of DMSMaPSeq data depending on user preferences
    """
)

Big_df = pd.read_csv('../Output/Alldata.csv')
st.write(Big_df)

Q3df_DMSO=Big_df.loc[(Big_df['Compound']=='DMSO')]
Q3df_2A3=Big_df.loc[(Big_df['Compound']=='2A3')]
Q3df_DMS=Big_df.loc[(Big_df['Compound']=='DMS')]

st.write('\n')
st.markdown("### Disribution of base mutations by compound")
fig, axes = plt.subplots(2,3,figsize = (12,6))

#boxplots
axes[0,0].set_title('DMSO')
axes[0,1].set_title('2A3')
axes[0,2].set_title('DMS')
axes[0,0].set_ylabel('Box plots\n')

axes[0,0].boxplot(Q3df_DMSO['Reactivity'], vert=False, flierprops={'marker': '.', 'markersize': 3})
axes[0,1].boxplot(Q3df_2A3['Reactivity'], vert=False, flierprops={'marker': '.', 'markersize': 3})
axes[0,2].boxplot(Q3df_DMS['Reactivity'], vert=False, flierprops={'marker': '.', 'markersize': 3})



#histograms
axes[1,0].set_yscale('log')
axes[1,0].hist(Q3df_DMSO['Reactivity'])
axes[1,1].hist(Q3df_2A3['Reactivity'])
axes[1,2].hist(Q3df_DMS['Reactivity'])
axes[1,0].set_ylabel('Histograms\nLog(Count)')
axes[1,1].set_xlabel('Mutation Frequency')

st.pyplot(fig)

