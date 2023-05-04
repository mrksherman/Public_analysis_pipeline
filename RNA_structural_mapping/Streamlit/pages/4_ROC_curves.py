
import pandas as pd
import streamlit as st
from PIL import Image

title='ROC Curves'
st.set_page_config(page_title=title, page_icon="📈", layout='wide')

st.markdown(f"# {title}")
st.sidebar.header(title)
st.write(
    """
    This explorer allows you to view the ROC curves for the structural analysis
    """
)

chosen = st.radio(
    'Which analysis would you like to view?',
    ("DMSO", "2A3", "DMS"))


if chosen == 'DMSO':
    image = Image.open('../Output/ROC_of_DMSO.png')
    st.image(image, 'ROC of DMSO')
if chosen == '2A3':
    image = Image.open('../Output/ROC_of_2A3.png')
    st.image(image, 'ROC of 2A3')
if chosen == 'DMS':
    image = Image.open('../Output/ROC_of_DMS.png')
    st.image(image, 'ROC of DMS')