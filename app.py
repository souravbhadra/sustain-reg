import os
import streamlit as st
import pyrebase
from password_strength import PasswordPolicy
from dotenv import load_dotenv

from utils import image_management as im
from utils import analyze_form as af


load_dotenv(".env")
# Load env variables
FBASE_CONFIG = {
    'apiKey': os.getenv("FBASE_API_KEY"),
    'authDomain': os.getenv("FBASE_AUTH_DOMAIN"),
    'projectId': os.getenv("FBASE_PROJECT_ID"),
    'storageBucket': os.getenv("FBASE_STORAGE_BUCKET"),
    'messagingSenderId': os.getenv("FBASE_MESSAGING_SENDER_ID"),
    'appId': os.getenv("FBASE_APP_ID"),
    'measurementId': os.getenv("FBASE_MEASUREMENT_ID"),
    'databaseURL': os.getenv("FBASE_DATABASE_URL")
}

# Authenticate firebase and database
firebase = pyrebase.initialize_app(FBASE_CONFIG)
auth = firebase.auth()
db = firebase.database()
    

im.insert_image(
    'images\logo.png',
    sidebar=False,
    margin=(0, 0, 30, 0),
    width='auto'
)


with st.form(key='sign_up_form'):
    col1, col2, col3 = st.columns(3)
    with col1:
        first_name = st.text_input(label='First Name *', placeholder='e.g., John')
    with col2:
        middle_name = st.text_input(label='Middle Name', placeholder='e.g., K.')
    with col3:
        last_name = st.text_input(label='Last Name *', placeholder='e.g., Doe')
    email = st.text_input(
        label='Enter your email *',
        placeholder='e.g., youremail@gmail.com'
    )
    password = st.text_input(
        label='Create a password *',
        type="password",
        placeholder="Password"
    )
    password_check = st.text_input(
        label='Retype password *',
        type="password",
        placeholder="Password again"
    )
    org = st.text_input(
        label='Organization/Company *',
        placeholder="Name of your organization or company"
    )
    col4, col5, col6 = st.columns(3)
    with col4:
        org_type = st.radio(
            label='Occupation*',
            options=[
                'Researcher',
                'Student',
                'Farmer',
                'Policy Developer'
            ]
        )
    with col5:
        industry = st.radio(
            label='Industry Type *',
            options=[
                'University',
                'Private',
                'Government',
                'Non-profit'
            ]
        )
    with col6:
        crop = st.radio(
            label='Which crop do you work with? *',
            options=[
                'Corn/Maize',
                'Sorghum',
                'Both'
            ]
        )
    with st.expander("By signing up, you are agreeing to the following terms and conditions"):
        st.write(
            """The chart above shows some numbers I picked for you.
            I rolled actual dice for these, so they're *guaranteed* to
            be random."""
        )
    submit_button = st.form_submit_button(label='Sign Up')
 

if submit_button:
    
    check_result = af.check_form_inputs(
        first_name,
        last_name,
        email,
        password,
        password_check,
        org
    )
    
    if check_result:
        try:
            # Sign up the user
            user = auth.create_user_with_email_and_password(email, password)
            auth.send_email_verification(user['idToken'])
            
            # Push user information to the database
            table_ref = db.child("user_info")
            new_record = {
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
                "email": email,
                "organization": org,
                "organization_type": org_type,
                "industry": industry,
                "crop": crop
            }
            table_ref.push(new_record)

        except:
            st.error('There is already an account registered using the email')

signin_link = '<a href="https://sustaincrops.net" target="_self">Already have an account? Sign In Instead!</a>'
st.markdown(signin_link, unsafe_allow_html=True)