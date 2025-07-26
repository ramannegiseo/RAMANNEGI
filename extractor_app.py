import streamlit as st
import pandas as pd
import re
from io import BytesIO

# Helper function to extract product name or order id
def extract_product_or_order(text):
    text = str(text)
    patterns = [
        (r'We noticed you (?:left|were checking out) (.+?) on Medansh\.in!', 1),
        (r'We noticed you left (.+?) in your cart!', 1),
        (r'Your purchase of (.+?) could not be completed', 1),
        (r'You left (.+?) in your cart!', 1),
        (r'Your purchase of (.+?) and (.+?) could not be completed', [1, 2]),
        (r'We noticed you left (.+?) in your cart! Complete your purchase now', 1),
        (r'We noticed you were checking out (.+?)\.', 1),
        (r'Your order \*([A-Z0-9]+)\*', 1),
        (r'order \*([A-Z0-9]+)\* from \*Medansh\* is cancelled', 1),
        (r'order \*([A-Z0-9]+)\* has been shipped', 1),
        (r'order \*([A-Z0-9]+)\* has been delivered', 1),
        (r'purchase of (.+?)(?: could not be completed|$)', 1),
        (r'left (.+?) in your cart', 1),
        (r'checking out (.+?)(?: on Medansh\.in|$)', 1),
    ]

    for pattern, group in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            if isinstance(group, list):
                return " and ".join([match.group(g).strip() for g in group])
            return match.group(group).strip()

    return text[:30] + "..."


# Streamlit UI
st.title("📦 Extract Product Name / Order ID from CSV")
st.write("Upload your `tellephant-logs-all_send.csv` file to extract product names or order IDs.")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if 'Text' not in df.columns:
        st.error("❌ Error: 'Text' column not found in the uploaded file.")
    else:
        st.success("✅ File uploaded successfully!")
        st.write("Processing...")
        df['Product Name / Order ID'] = df['Text'].apply(extract_product_or_order)

        st.write("### Preview of Processed Data:")
        st.dataframe(df.head())

        # Convert to downloadable CSV
        output = BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)

        st.download_button(
            label="📥 Download Processed CSV",
            data=output,
            file_name="tellephant-logs-with-product-or-order.csv",
            mime="text/csv"
        )
