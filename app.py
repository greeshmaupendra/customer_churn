import pickle
import pandas as pd
import streamlit as st

MODEL_PATH = "final_model.pkl"
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

with open("normalizer.pkl", "rb") as file:
    normalizer = pickle.load(file)


if __name__ == "__main__":
    st.title("Customer Churn Prediction")
    tenure=st.number_input("Customer Tenure (months)", 0, 1200)
    monthly=st.number_input("Monthly Charges", 0.0, 120.0, step=0.01)
    total=st.number_input("Total Charges", 0.0, step=0.01)
    phoneservice=st.selectbox("Has Phone Service", ["No", "Yes"], index=0)
    contract=st.selectbox(
            "Has Contract",
            ["Month-to-month", "One year", "Two year"],
            index=0,
        )
    paperless_billing = st.selectbox("Has Paperless Billing", ["No", "Yes"], index=0)
    paymentmethod=st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)",
            ],
            index=0,
        ),
    gender=st.selectbox("Gender", ["Male", "Female"], index=0)
    senior=st.selectbox("Senior Citizen", ["No", "Yes"], index=0)
    partner=st.selectbox("Has Partner", ["No", "Yes"], index=0)
    dependents=st.selectbox("Has Dependents", ["No", "Yes"], index=0)
    multilines=st.selectbox(
            "Has Multiple Phone Numbers",
            ["No", "Yes", "No phone service"],
            index=0,
        )
    internet=st.selectbox(
            "Has Internet Service", ["No", "DSL", "Fiber optic"], index=0
        )
    online_sec=st.selectbox(
            "Has Online Security Service",
            ["No", "Yes", "No internet service"],
            index=0,
        )
    backup=st.selectbox(
            "Has Online Backup", ["No", "Yes", "No internet service"], index=0
        )
    protection=st.selectbox(
            "Has Device Protection",
            ["No", "Yes", "No internet service"],
            index=0,
        )
    techsupport=st.selectbox(
            "Has Tech Support Access",
            ["No", "Yes", "No internet service"],
            index=0,
        )
    streamingTV=st.selectbox(
            "Has Streaming TV Subscription", ["No", "Yes", "No internet service"], index=0
        )
    streamingMovie=st.selectbox(
            "Has Streaming Movies Subscription",
            ["No", "Yes", "No internet service"],
            index=0,
        )


    input_df=pd.DataFrame(columns=['tenure', 'PhoneService', 'Contract', 'PaperlessBilling',
       'PaymentMethod', 'MonthlyCharges', 'TotalCharges', 'gender',
       'SeniorCitizen', 'Partner', 'Dependents', 'MultipleLines',
       'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
       'TechSupport', 'StreamingTV', 'StreamingMovies'],dtype=float)

    # Label encoding

    if phoneservice == "Yes":
        phoneservice1=1
    else:
        phoneservice1=0

    if paperless_billing == "Yes":
        paperless_billing1=1
    else:
        paperless_billing1=0

    if senior == "Yes":
        senior1=1
    else:
        senior1=0

    if partner == "Yes":
        partner1=1
    else:
        partner1=0

    if dependents == "Yes":
        dependents1=1
    else:
        dependents1=0

    if gender == "Male":
        gender1=1
    else:
        gender1=0

    if multilines == "No":
        multilines1=0
    elif multilines == "Yes":
        multilines1=1
    else:
        multilines1=2

    if internet == "DSL":
        internet1=0
    elif internet == "Fiber optic":
        internet1=1
    else:
        internet1=2

    if online_sec == "No":
        online_sec1=0
    elif online_sec == "Yes":
        online_sec1=2
    else:
        online_sec1=1

    if backup == "No":
        backup1=0
    elif backup == "Yes":
        backup1=2
    else:
        backup1=1

    if protection == "No":
        protection1=0
    elif protection == "Yes":
        protection1=2
    else:
        protection1=1

    if techsupport == "No":
        techsupport1=0
    elif techsupport == "Yes":
        techsupport1=2
    else:
        techsupport1=1

    if streamingTV == "No":
        streamingTV1=0
    elif streamingTV == "Yes":
        streamingTV1=2
    else:
        streamingTV1=1

    if streamingMovie == "No":
        streamingMovie1=0
    elif streamingMovie == "Yes":
        streamingMovie1=2
    else:
        streamingMovie1=1

    if paymentmethod == "Electronic check":
        paymentmethod1=2
    elif paymentmethod == "Mailed check":
        paymentmethod1=3
    elif paymentmethod == "Bank transfer (automatic)":
        paymentmethod1=0
    else:
        paymentmethod1=1

    if contract == "Month-to-month":
        contract1=0
    elif contract == "Two year":
        contract1=2
    else:
        contract1=1



    data = {'tenure':tenure, 'PhoneService':phoneservice1, 'Contract':contract1, 'PaperlessBilling':paperless_billing1,
       'PaymentMethod':paymentmethod1, 'MonthlyCharges':monthly, 'TotalCharges':total, 'gender':gender1,
       'SeniorCitizen':senior1, 'Partner':partner1, 'Dependents':dependents1, 'MultipleLines':multilines1,
       'InternetService':internet1, 'OnlineSecurity':online_sec1, 'OnlineBackup':backup1, 'DeviceProtection':protection1,
       'TechSupport':techsupport1, 'StreamingTV':streamingTV1, 'StreamingMovies':streamingMovie1}

    new_row = pd.DataFrame(data)

    input_df = pd.concat([input_df, new_row], ignore_index=True)

    #input_df=input_df.append([data],ignore_index=True)
    normalised=input_df[['tenure','MonthlyCharges','TotalCharges']]
    normalised1=normalizer.transform(normalised)
    input_df['tenure']=normalised1[:,0]
    input_df['MonthlyCharges']=normalised1[:,1]
    input_df['TotalCharges']=normalised1[:,2]
    #st.write(input_df)

    if st.button("Predict"):
        if model.predict(input_df)==1:
            st.title("Likely to Churn")
        else:
            st.title("Not Likely to Churn")
