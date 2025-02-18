import streamlit as st
import pandas as pd


def main():
    st.title("API Demo: REST, GraphQL, and gRPC")
    st.write(
        "This Streamlit app lets you try 3 different APIs which access the same data."
    )

    endpoint_option = st.selectbox("Choose an API", ["REST", "GraphQL", "gRPC"])

    if st.button("Get stats"):
        rows = 10
        st.text(f"Total rows: {rows}")

    if st.button("Get Metadata"):
        data = {"Columns": ["Price", "Bedrooms"], "Max": [10, 3], "Min": [1, 1]}
        df = pd.DataFrame(data)
        df.set_index("Columns", inplace=True)
        st.bar_chart(df, stack=False)


if __name__ == "__main__":
    main()
