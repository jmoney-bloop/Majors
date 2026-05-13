import streamlit as st
from utils import get_df
st.title("Semi-Annual Brian Finishes Last Event")

df = get_df()

st.dataframe(df, hide_index=True)