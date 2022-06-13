__author__ = "Katrin Peikert"

import streamlit as st 
from dgim import Dgim
import pandas as pd




class Drug_database:
    
    def __init__(self, path:str):
        self.data = pd.read_csv(path ,sep ="\t")
        del self.data['Unnamed: 0']
        del self.data['review']
        self.columns = [i for i in self.data.columns]
        
        self.one_hot_encoded = None
        self.one_hot_encoded_columns = None
        return
    
    def one_hot_encoding_col(self, col_name:str) -> pd.array:
        """Applies one hot encoding to chosen column and adds new columns to data array

        Args:
            col_name (str): Name of column we want to one-hot-encode

        Returns:
            pd.array: new array
        """
        if not(col_name in self.columns):
            return "This column does not exist!"
        col = [i for i in self.data[col_name]]
        
        encoding = pd.get_dummies(col)
        self.one_hot_encoded_columns = [i for i in encoding.columns]
        self.one_hot_encoded = self.data.join(encoding)
        del self.one_hot_encoded[col_name]
        return self.one_hot_encoded
    
    def calculate_number_ones(self, col_name:str, N:int):
        """Estimates (with DGIM) and calculates the number of 1's in chosen 
        column and Windowsize N

        Args:
            col_name (str): Name of column we want to estimate the 1's in
            N (int): window size

        Returns:
            _int_, _int_: estimated number, correct number
        """
        if not(col_name in self.one_hot_encoded.columns):
            return "This column does not exist!"
        col = [i for i in self.one_hot_encoded[col_name]]
        window = col[len(col)-N:]
        
        actual_numbers = window.count(1)
        
        dgim = Dgim(N, error_rate= 0.1)
        for i in window:
            dgim.update(bool(i))
        return actual_numbers, dgim.get_count()


database = Drug_database("drugsCom_raw/drugsComTrain_raw.tsv")
with st.sidebar.expander(label='Set Values', expanded=True):
    option = st.selectbox("Column to Hot-Encode:", database.columns)
    database.one_hot_encoding_col(option)
    option_for_dgim = st.selectbox("Column to apply DGIM to:", database.one_hot_encoded_columns)
    option_for_N = st.number_input("Size of Window N", 1, 161296 )

    run_comparison = st.button('RUN!')
  
    
st.title("One-Hot-Encoding & DGIM on DrugReviews")
st.caption("As implemented by Katrin Peikert")


st.subheader("The first five Lines of the Data:")
st.dataframe(database.data.head(5))


st.write("Source: Drug Review Dataset (https://archive-beta.ics.uci.edu/ml/datasets/drug+review+dataset+drugs+com)")
st.header("Result of calculation:")
if run_comparison:   
    actual_number, estimated_number = database.calculate_number_ones(option_for_dgim, option_for_N)
    
    left_column_2, right_column_2 = st.columns(2)
     
    with left_column_2:
        st.write("Chosen Column for One-hot Encoding: " )
        st.write("Calculating the number of 1's on this value: " )
        st.write("Actual Number of 1's in Window of Size",str(option_for_N),": ")
        st.write("Estimated by DGIM:")
        st.write("Percentage between Estimation and actual result:")
        
    with right_column_2:
        st.write( option)
        st.write( option_for_dgim)
        st.write( actual_number)
        st.write( estimated_number)
        st.write( round(estimated_number/actual_number,3))

    
     



        