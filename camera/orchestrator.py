import streamlit as st
from . import examples

def show_examples():

    st.write(
        """
        ### 📸 BearKS_Photo Booth
        ---
        take a photo:
        """
    )

    examples.show()

if __name__ == "__main__":
    pass