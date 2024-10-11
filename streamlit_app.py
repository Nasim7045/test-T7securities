import streamlit as st
import pyrebase
import firebase_admin
import time
from datetime import datetime, timedelta
from streamlit_cookies_manager import EncryptedCookieManager
from firebase_admin import credentials, auth, firestore

# Firebase Admin SDK credentials
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "t7-securities-database",
    "private_key_id": "29200d5431bdc51b404c298164034aaa5a3a5270",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDa9owU+m8nqLpP\n0bNfBINLsC7L/0Da/hs6OywFDoWGlb7LI/tBaCrxnE3N+dtfo6vwIXaUV3SRUjWk\nNpFdRyIjOJXxAcKGHdHP6TsYR4tD9LFqof7FKz7ykzgv67+oVWKpsPWxWhOnZqO+\ndJ7Qrd2OTxF3I/HeVOnO1QNk7aXQ9dxUtu5BrP+25tPLQXEoijwmi6A5fZveIBd/\nHkLQHWUOdwCxU0PZwbMzn/Js4DnDlWRCwLrESAAe6+8qgvW4kBlZnWsusYwA6wVh\ngqY2sroph8TVmKkI1TvgY5hL442QNVh+pjRWspOdonqoz1SPpGHvwx1moxsxnu3A\n4girhiyvAgMBAAECggEAQNu71bDywPAZM/B9Lb2D+KT4z6NNvjB7ty101hCdm6Z6\ni+ieEZs98TBn2YXTpcow8WGwIrOfCzarPfeN6m/aHE20GF35lUl67xd6UjBK/7eY\n3+mZMiUjsa3K/GLb9AxKu9H3jO+OF81u3kjkDBMcJ/2iwkQq7jz/vqzZIwnDzpeg\nnyEMtZrVQ76H8T4q8MV+CodCiOhVSA4d6Sy3v4W605qIbg8ejlQblkEc/VHzggwW\nXS0uyVi4/Rtuz11fc/pH3ViphXHKgd8Yu+xFUuUB3VREivz0cArdqUn8orks6pfu\nsMs+WTvFLX/m2n9dVI1ckiJw5uKVL3xm8hyZI9VOZQKBgQD4SxsHi8k7qSt7urID\ndrbELl0vS6Jpopnm8eDW8StPKf0kDWT/iZqAcqK8vmN1FzPKgC986Q00ms1Ge7cz\nAgY9tCoqF05nTRDlfxlhkHunosVkfRJ29ro+Nu9i/9Lf7v7CcIrglBrZH6FHJZpN\nPaeLN+5s6HOjVR5JmTV51vCIowKBgQDhwmNm6oot2S7MC0irUD82RQiSnuRW1Dcw\n7HiMSfR2E6s91+NrMK+VT8J2mpux5rHQZFEIY0OSx5ZhsqM8+acQQyNQaec3Mhmd\nIZyVZmdUAq+ZZcptldz2GoAz/tKTuDbJbG4rHe76NBagRSoLuCeC8E/szRRBT5MN\nPQl6vzcQhQKBgG5bq4riFbI/0cTvyTmC5V8zIFXqLyj2jaM5dO70SISqLAp/LZnq\nxlI7IZv0n24mvu1Npk3FpAnymDSwvk+cobuBPZBxxXZiqZTnthdISb3LuiKc+L0J\nkuQeNK5y+H5x0qgHr6J8EabZySw/SWL1eWeGl6Gue99n8MtTnpIl98kzAoGAdq6v\nfQotzD6RqHkCIfWU1Z3jDNl1JuR3g0O9d9rlJjHe4yschlxY4gDFNX6//P1PW0Nx\nihxNCNveBcxYnpSMLDNvXDXgdJbk+kMSQ0RLa9HhqJ3nlkajm8mAvlTnNPsx6iAT\npp0c5fH+NxFFMlYEh4R4L//79v2zS9Fbq2jctNUCgYAKj840NTTyodmwVAKJBm8H\ntXgNHyvQgXr1lBcgHtkaXHEXhIxGavwOoDMp5QMT35JLVk3RjlJFnuySL/lVywHz\nozkHd8AOFbRW+Lda0IanULrjVf9wmzd9F+LIVAgShFrZTj2buw8ASeZW5RWXQoi/\nnei5LNzpJ4RvVCgXth4dFA==\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-ztu4u@t7-securities-database.iam.gserviceaccount.com",
    "client_id": "103402632275992014907",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ztu4u%40t7-securities-database.iam.gserviceaccount.com"
})

# Initialize Firebase Admin SDK only if not already initialized
if not firebase_admin._apps:
    default_app = firebase_admin.initialize_app(cred)

# Pyrebase setup for client-side operations
firebase_config = {
    "apiKey": "AIzaSyB0gbs0qPbl4fZkIVBZ6_UQwZxKV0uPwAk",
    "authDomain": "t7-securities-database.firebaseapp.com",
    "databaseURL": "https://t7-securities-database.firebaseio.com",
    "projectId": "t7-securities-database",
    "storageBucket": "t7-securities-database.appspot.com",
    "messagingSenderId": "278676976057",
    "appId": "1:278676976057:web:182f8c1110d96f9d7f4668",
    "measurementId": "G-DNJN5ZKZEP"
}

# Initialize Pyrebase
firebase = pyrebase.initialize_app(firebase_config)
auth_client = firebase.auth()
db = firestore.client()

# Set page config
st.set_page_config(page_title="Login", page_icon="🔑")

# Cookie manager setup
cookies = EncryptedCookieManager(
    prefix="myapp_",
    password="A very secret password",
)

if not cookies.ready():
    st.stop()

# Constants
TIMEOUT_DURATION = 900  # 15 minutes in seconds

# Authentication functions
def login_user(email, password):
    try:
        user = auth_client.sign_in_with_email_and_password(email, password)
        return user['idToken'], user['email']
    except Exception as e:
        st.error(f"Login failed: {str(e)}")
        return None, None

def register_user(email, password, role):
    try:
        if not email or not password:
            raise ValueError("Email and password cannot be empty.")
        user = auth_client.create_user_with_email_and_password(email, password)
        db.collection('users').document(email).set({"role": role})
        return True
    except Exception as e:
        st.error(f"Registration failed: {str(e)}")
        return False

def reset_password(email):
    try:
        auth_client.send_password_reset_email(email)
        return True
    except Exception as e:
        st.error(f"Password reset failed: {str(e)}")
        return False

def check_session_timeout():
    current_time = time.time()
    if "last_activity" in cookies:
        last_activity = float(cookies["last_activity"])
        if current_time - last_activity > TIMEOUT_DURATION:
            logout_user()
    cookies["last_activity"] = str(current_time)
    cookies.save()

def logout_user():
    st.session_state["logged_in"] = False
    st.session_state["user_email"] = None
    cookies["logged_in"] = "False"
    cookies["user_email"] = ""
    cookies.save()
    st.rerun()

def navigate_to(page):
    st.experimental_set_query_params(page=page)  # Use this for setting query parameters
    st.rerun()

# Page handlers
def admin_login_page():
    st.title("Admin Login")
    with st.form("admin_login_form"):
        email = st.text_input("Admin Email")
        password = st.text_input("Admin Password", type="password")
        submit = st.form_submit_button("Login as Admin")
        
        if submit:
            id_token, user_email = login_user(email, password)
            if id_token:
                user_doc = db.collection('users').document(email).get()
                if user_doc.exists and user_doc.to_dict().get('role') == 'admin':
                    st.session_state["logged_in"] = True
                    st.session_state["user_email"] = user_email
                    cookies["logged_in"] = "True"
                    cookies["user_email"] = user_email
                    cookies["last_activity"] = str(time.time())
                    cookies.save()
                    st.rerun()
                else:
                    st.error("You do not have Admin privileges.")

def user_login_page():
    st.title("User Login")
    with st.form("user_login_form"):
        email = st.text_input("User Email")
        password = st.text_input("User Password", type="password")
        submit = st.form_submit_button("Login as User")
        
        if submit:
            id_token, user_email = login_user(email, password)
            if id_token:
                user_doc = db.collection('users').document(email).get()
                if user_doc.exists and user_doc.to_dict().get('role') == 'user':
                    st.session_state["logged_in"] = True
                    st.session_state["user_email"] = user_email
                    cookies["logged_in"] = "True"
                    cookies["user_email"] = user_email
                    cookies["last_activity"] = str(time.time())
                    cookies.save()
                    st.rerun()
                else:
                    st.error("You do not have User privileges.")

def registration_page():
    st.title("Register a New Account")
    with st.form("registration_form"):
        email = st.text_input("Enter your email")
        password = st.text_input("Enter your password", type="password")
        confirm_password = st.text_input("Confirm your password", type="password")
        role = st.selectbox("Select role", ["user", "admin"])
        submit = st.form_submit_button("Register")
        
        if submit:
            if password == confirm_password:
                if register_user(email, password, role):
                    st.success("Registration successful! You can now log in.")
                    time.sleep(2)  # Give user time to read the success message
                    navigate_to("user")
            else:
                st.error("Passwords do not match.")

def main():
    # Initialize session state variables
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "user_email" not in st.session_state:
        st.session_state["user_email"] = None

    # Check session timeout if logged in
    if st.session_state["logged_in"]:
        check_session_timeout()
        st.write(f"Logged in as: {st.session_state['user_email']}")
        if st.button("Logout"):
            logout_user()
    else:
        # Handle navigation
        page = st.experimental_get_query_params().get("page", ["user"])[0]

        if page == "admin":
            admin_login_page()
        elif page == "register":
            registration_page()
        else:
            user_login_page()

        # Navigation buttons
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if st.button("Admin Login"):
                navigate_to("admin")
        with col2:
            if st.button("User Login"):
                navigate_to("user")
        with col3:
            if st.button("Register"):
                navigate_to("register")

if __name__ == "__main__":
    main()