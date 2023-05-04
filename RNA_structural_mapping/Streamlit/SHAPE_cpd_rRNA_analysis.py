import streamlit as st

st.set_page_config(
    page_title="SHAPE v DMS Comparison",
    page_icon="👋",
    layout="wide",
)

st.write("# SHAPE v DMS Comparison")

st.sidebar.success("Select an analysis")

st.markdown(
    """

    ### Source data was downloaded from the following sources

    |Treatment|SRR record|Description|Source|
    |:-:|:-:|:-:|:-:|
    |DMSO| SRR12235529| GSM4673448: DMSO, E. coli, in vivo (SSII)| https://trace.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=SRR12235529&display=download|
    |2A3|SRR12235536|GSM4673455: 2A3, E. coli, in vivo (SSII)|https://trace.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=SRR12235536&display=download|
    |DMS|SRR6848182|GSM3045709: DMS-MaPseq on E. coli (Total RNA)|https://trace.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=SRR6848182&display=download|
    |||E. coli 16S rRNA FASTA|https://rnacentral.org/api/v1/rna/URS000039D89A.fasta|
    |||E. coli 23S rRNA FASTA|https://rnacentral.org/api/v1/rna/URS00019ABAEF.fasta|
    |||E. coli 16S Dot-bracket| https://rnacentral.org/rna/URS000039D89A/511145|
    |||E. coli 23S Dot-bracket| https://rnacentral.org/rna/URS00019ABAEF/511145|


    ### Select tha appropriate analysis from the sidebar
    - Table explore
        - A, U, C, G
        - Base Plots
        - Distributions
    - Curves
        - ROC
    - Tools
        - Hairpin analysis
"""
)