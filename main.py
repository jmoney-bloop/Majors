import streamlit as st
from utils import get_df
import pandas as pd

st.title("PGA Championship")

if st.button(label="Refresh"):
    st.cache_data.clear()

df = get_df()
st.dataframe(df, hide_index=True)