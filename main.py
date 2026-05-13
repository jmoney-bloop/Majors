import streamlit as st
from utils import get_df
st.title("Semi-Annual Brian Finishes Last Event")



if st.button(label="Refresh"):
    st.cache_data.clear()

df = get_df()
st.dataframe(df, hide_index=True)