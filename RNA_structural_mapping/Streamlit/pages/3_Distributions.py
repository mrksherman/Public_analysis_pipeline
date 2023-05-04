import streamlit as st
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

title='Distribution by Reagent'
st.set_page_config(page_title=title, page_icon="📈", layout='wide')

st.markdown(f"# {title}")
st.sidebar.header(title)
st.write(
    """
    This explorer allows you to view the distribution reactivites of the the shape reagents
    """
)

Big_df = pd.read_csv('../Output/Alldata.csv')


chosen = st.radio(
    'Which analysis would you like to view?',
    ("Raw", "Normalized"))



st.markdown(f'#### {chosen} distribution of SHAPE reagent reactivities')
Q3df_DMSO=Big_df.loc[(Big_df['Compound']=='DMSO')]
Q3df_DMSO_U=Q3df_DMSO.loc[(Q3df_DMSO['Reference_psuedostructure']=='U')]
Q3df_DMSO_T=Q3df_DMSO.loc[(Q3df_DMSO['Reference_psuedostructure']=='T')]
Q3df_DMSO_I=Q3df_DMSO.loc[(Q3df_DMSO['Reference_psuedostructure']=='I')]

Q3df_2A3=Big_df.loc[(Big_df['Compound']=='2A3')]
Q3df_2A3_U=Q3df_2A3.loc[(Q3df_2A3['Reference_psuedostructure']=='U')]
Q3df_2A3_T=Q3df_2A3.loc[(Q3df_2A3['Reference_psuedostructure']=='T')]
Q3df_2A3_I=Q3df_2A3.loc[(Q3df_2A3['Reference_psuedostructure']=='I')]

Q3df_DMS=Big_df.loc[(Big_df['Compound']=='DMS')]
Q3df_DMS_U=Q3df_DMS.loc[(Q3df_DMS['Reference_psuedostructure']=='U')]
Q3df_DMS_T=Q3df_DMS.loc[(Q3df_DMS['Reference_psuedostructure']=='T')]
Q3df_DMS_I=Q3df_DMS.loc[(Q3df_DMS['Reference_psuedostructure']=='I')]

fig, axes = plt.subplots(3,3,figsize = (15,7.25))

#boxplots
axes[0,0].set_title('Unpaired')
axes[0,1].set_title('Terminal')
axes[0,2].set_title('Internal')
axes[0,0].set_ylabel('DMSO')
axes[1,0].set_ylabel('2A3')
axes[2,0].set_ylabel('DMS')
axes[2,1].set_xlabel('Mutation Frequency')

if chosen =='Raw':
    axes[0,0].boxplot(Q3df_DMSO_U['Reactivity'], vert=False, flierprops={'marker': '.', 'markersize': 3})
    axes[0,1].boxplot(Q3df_DMSO_T['Reactivity'], vert=False, flierprops={'marker': '.', 'markersize': 3})
    axes[0,2].boxplot(Q3df_DMSO_I['Reactivity'], vert=False, flierprops={'marker': '.', 'markersize': 3})
    axes[1,0].boxplot(Q3df_2A3_U ['Reactivity'], vert=False, flierprops={'marker': '.', 'markersize': 3})
    axes[1,1].boxplot(Q3df_2A3_T ['Reactivity'], vert=False, flierprops={'marker': '.', 'markersize': 3})
    axes[1,2].boxplot(Q3df_2A3_I ['Reactivity'], vert=False, flierprops={'marker': '.', 'markersize': 3})
    axes[2,0].boxplot(Q3df_DMS_U ['Reactivity'], vert=False, flierprops={'marker': '.', 'markersize': 3})
    axes[2,1].boxplot(Q3df_DMS_T ['Reactivity'], vert=False, flierprops={'marker': '.', 'markersize': 3})
    axes[2,2].boxplot(Q3df_DMS_I ['Reactivity'], vert=False, flierprops={'marker': '.', 'markersize': 3})
elif chosen == 'Normalized':
    axes[1,0].boxplot(Q3df_2A3_U['Normalized_Reactivity'].astype(float).dropna(), vert=False, flierprops={'marker': '.', 'markersize': 3})
    axes[1,1].boxplot(Q3df_2A3_T['Normalized_Reactivity'].astype(float).dropna(), vert=False, flierprops={'marker': '.', 'markersize': 3})
    axes[1,2].boxplot(Q3df_2A3_I['Normalized_Reactivity'].astype(float).dropna(), vert=False, flierprops={'marker': '.', 'markersize': 3})
    axes[2,0].boxplot(Q3df_DMS_U['Normalized_Reactivity'].astype(float).dropna(), vert=False, flierprops={'marker': '.', 'markersize': 3})
    axes[2,1].boxplot(Q3df_DMS_T['Normalized_Reactivity'].astype(float).dropna(), vert=False, flierprops={'marker': '.', 'markersize': 3})
    axes[2,2].boxplot(Q3df_DMS_I['Normalized_Reactivity'].astype(float).dropna(), vert=False, flierprops={'marker': '.', 'markersize': 3})


st.pyplot(fig)





