import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

st.title("Pandas DataFrame insert() Function Explorer")

# Create example dataframe
@st.cache_data
def create_sample_data():
    return pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [10, 20, 30, 40, 50],
        'C': [100, 200, 300, 400, 500]
    })

df = create_sample_data()

# Create a sidebar for function parameters
with st.sidebar:
    st.header("Function Parameters")
    
    st.markdown("""
    ```python
    DataFrame.insert(loc, column, value, allow_duplicates=False)
    ```
    """)
    
    loc = st.number_input("loc (position to insert at)", 
                          min_value=0, 
                          max_value=len(df.columns), 
                          value=1, 
                          help="Integer that indicates the position to insert the column(s)")

    column_name = st.text_input("column (name of new column)", 
                               value="New_Column", 
                               help="Label for the new column")

    value_type = st.selectbox("Type of value to insert", 
                              options=["Single Value", "List/Array", "Series", "Function/Expression"],
                              help="Choose what type of value to insert")

    if value_type == "Single Value":
        value = st.number_input("value (constant)", value=99)
    elif value_type == "List/Array":
        value_input = st.text_input("value (comma separated values)", 
                                   value="99, 88, 77, 66, 55",
                                   help="Enter comma-separated values")
        try:
            value = [float(x.strip()) for x in value_input.split(",")]
        except:
            st.error("Please enter valid comma-separated numbers")
            value = [99, 88, 77, 66, 55]
    elif value_type == "Series":
        column_to_use = st.selectbox("Base on column", df.columns.tolist())
        operation = st.selectbox("Operation", ["Multiply by", "Add", "Subtract", "Square", "Square Root"])
        operation_value = st.number_input("Operation value", value=2.0) if operation in ["Multiply by", "Add", "Subtract"] else None
        
        if operation == "Multiply by":
            value = df[column_to_use] * operation_value
        elif operation == "Add":
            value = df[column_to_use] + operation_value
        elif operation == "Subtract":
            value = df[column_to_use] - operation_value
        elif operation == "Square":
            value = df[column_to_use] ** 2
        elif operation == "Square Root":
            value = np.sqrt(df[column_to_use])
    elif value_type == "Function/Expression":
        expr = st.text_input("Python expression (use df for dataframe)", 
                             value="df['A'] + df['B']",
                             help="Enter a Python expression using 'df' as the dataframe")
        try:
            value = eval(expr)
        except:
            st.error("Invalid expression. Using default expression.")
            value = df['A'] + df['B']

    allow_duplicates = st.checkbox("allow_duplicates", 
                                  value=False, 
                                  help="Allow duplicate column names")

    st.markdown("---")
    st.markdown("""
    #### Visual Settings
    """)
    highlight_color = st.color_picker("Highlight color for new column", value="#ffff00")
    highlight_opacity = st.slider("Highlight opacity", min_value=0.1, max_value=1.0, value=0.3, step=0.1)

# Function to style the dataframes 
def highlight_new_column(df_styled, column_name):
    # Convert hex color to rgba
    hex_color = highlight_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    rgba = f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {highlight_opacity})"
    
    return df_styled.style.set_properties(
        subset=[column_name],
        **{'background-color': rgba, 'font-weight': 'bold'}
    )

# Add visual borders to distinguish dataframes
original_container_style = """
<style>
div[data-testid="stDataFrame"] {
    border: 2px solid #ccc;
    border-radius: 5px;
    padding: 5px;
}
div.stDataFrame > div {
    margin-bottom: 0;
}
</style>
"""

modified_container_style = """
<style>
div[data-testid="stDataFrame"] {
    border: 2px solid #4e8df5;
    border-radius: 5px;
    padding: 5px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
div.stDataFrame > div {
    margin-bottom: 0;
}
</style>
"""

# Main content area - split into two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Original DataFrame")
    st.markdown(original_container_style, unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

# Create and display modified dataframe
try:
    modified_df = df.copy()
    modified_df.insert(loc=loc, column=column_name, value=value, allow_duplicates=allow_duplicates)
    
    with col2:
        st.subheader("Modified DataFrame")
        st.markdown(modified_container_style, unsafe_allow_html=True)
        
        # Apply styling to highlight the new column
        styled_df = highlight_new_column(modified_df, column_name)
        st.dataframe(styled_df, use_container_width=True)
    
    
    # Show code example
    st.subheader("Code")
    
    if value_type == "Single Value":
        code_value = str(value)
    elif value_type == "List/Array":
        code_value = str(value)
    elif value_type == "Series":
        if operation == "Multiply by":
            code_value = f"df['{column_to_use}'] * {operation_value}"
        elif operation == "Add":
            code_value = f"df['{column_to_use}'] + {operation_value}"
        elif operation == "Subtract":
            code_value = f"df['{column_to_use}'] - {operation_value}"
        elif operation == "Square":
            code_value = f"df['{column_to_use}'] ** 2"
        elif operation == "Square Root":
            code_value = f"np.sqrt(df['{column_to_use}'])"
    elif value_type == "Function/Expression":
        code_value = expr
    
    code = f"""
# Original DataFrame
{df.to_string()}

# Insert new column
df.insert(loc={loc}, column="{column_name}", value={code_value}, allow_duplicates={allow_duplicates})

# Modified DataFrame
{modified_df.to_string()}
    """
    st.code(code, language="python")
    
except Exception as e:
    with col2:
        st.error(f"Error: {str(e)}")
        st.warning("Common errors include:")
        st.markdown("""
        - Inserting a column with a name that already exists (without allow_duplicates=True)
        - Providing a value of incorrect length
        """)
