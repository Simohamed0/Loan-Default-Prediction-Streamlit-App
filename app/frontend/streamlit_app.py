import streamlit as st
import pandas as pd
import requests
import json

# Title and Introduction
st.title('📊 Loan Default Prediction')
st.markdown("""
Welcome to the **Loan Default Prediction** app! 
Upload your CSV file to predict the likelihood of default for each loan application.
""")

# Step 1: Upload CSV file
st.markdown("### Step 1: Upload Your CSV File")
uploaded_file = st.file_uploader("Upload your input CSV file", type=["csv"])

if uploaded_file is not None:
    # Display the uploaded data
    data = pd.read_csv(uploaded_file)
    st.markdown("### Uploaded Data")
    st.dataframe(data)  # Use st.dataframe for a scrollable table display

    # Step 2: Select Prediction Option
    st.markdown("### Step 2: Choose Prediction Option")
    option = st.selectbox(
        "How would you like to make predictions?",
        ["Select a specific row", "Predict for all rows"]
    )

    if option == "Select a specific row":
        row_index = st.number_input(
            "Select the row index you want to predict (0-based index)", 
            min_value=0, max_value=len(data)-1, step=1
        )
        input_data = data.iloc[[row_index]].to_dict(orient='records')[0]
        input_data = {key: [value] for key, value in input_data.items()}
        st.markdown(f"**Selected Row:** {row_index}")

    elif option == "Predict for all rows":
        input_data = data.to_dict(orient='records')  # Convert entire DataFrame to list of dicts
        st.markdown("**Predicting for all rows**")

    # Step 3: Display the input data
    # st.markdown("### Input Data for Prediction")
    # st.json(input_data)  # Display JSON in a pretty format

    # Step 4: Make prediction
    if st.button("Predict Loan Default"):
        with st.spinner('Making predictions...'):
            response = requests.post('http://backend:8000/predict/', json={"data": input_data})
            st.success("Prediction complete!")
        
        # Display Prediction Results
        st.markdown("### 📈 Prediction Results")
        results = response.json().get("predictions", [])
        if results:
            # Display each prediction in a card-like format
            for i, result in enumerate(results):
                st.markdown(f"#### loan ID {result['id']}")
                st.write(f"**Prediction:** {'Chraged off' if result['predictions'] == 1 else 'Fully Paid'}")
                st.markdown("---")

            # If there are many predictions, provide an option to download the full results
            if len(results) > 5:
                st.download_button(
                    label="Download Full Results",
                    data=pd.DataFrame(results).to_csv(index=False),
                    file_name='prediction_results.csv',
                    mime='text/csv'
                )
        else:
           st.write("No predictions were made. Please check the input data and try again.")
