import streamlit as st
from user_data import (
    register_user, login_user, get_email_by_username,
    update_password, log_login, get_all_users, get_login_history
)
from email_utils import send_otp

def login_page():
    # Title for the login page
    st.title("Login / Sign Up")

    # Default menu items for regular users
    menu = ["Login", "Sign Up", "Forgot Password", "Change Password"]
    
    # If the user is authenticated as "parasadmin", add admin-only options to the menu
    if st.session_state.get("authenticated") and st.session_state.get("username") == "parasadmin":
        menu.extend(["View Users", "Login History"])  # Admin options only visible to "parasadmin"

    # Display the menu options in the sidebar
    choice = st.sidebar.selectbox("Menu", menu)

    # Show post-login success message
    if st.session_state.get("login_success"):
        st.success(st.session_state.pop("login_success"))

    # Show post-signup success message
    if st.session_state.get("signup_success"):
        st.success(st.session_state.pop("signup_success"))

    # Login Flow
    if choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            # Attempt to login with the provided username and password
            if login_user(username, password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.session_state["login_success"] = f"Welcome {username}!"
                log_login(username)
                st.write(f"Session state after login: {st.session_state}")  # Log session state for debugging
                st.rerun()  # Rerun the app to refresh the UI
            else:
                st.error("Invalid credentials")

    # Signup Flow
    elif choice == "Sign Up":
        st.subheader("Sign Up")
        username = st.text_input("New Username")
        password = st.text_input("New Password", type="password")
        email = st.text_input("Email")
        if st.button("Send OTP"):
            st.session_state["otp"] = send_otp(email)  # Send OTP for verification
            st.session_state["temp_user"] = {"username": username, "password": password, "email": email}
        if "otp" in st.session_state:
            user_otp = st.text_input("Enter OTP")
            if st.button("Verify OTP"):
                if user_otp == st.session_state["otp"]:  # Verify the entered OTP
                    temp = st.session_state["temp_user"]
                    # Register the user if OTP is correct
                    if register_user(temp["username"], temp["password"], temp["email"]):
                        st.session_state["signup_success"] = "Account created!"
                        del st.session_state["otp"]
                        del st.session_state["temp_user"]
                        st.rerun()
                    else:
                        st.error("User already exists")

    # Forgot Password Flow
    elif choice == "Forgot Password":
        st.subheader("Forgot Password")
        username = st.text_input("Username")
        if st.button("Send OTP to Email"):
            email = get_email_by_username(username)
            if email:
                st.session_state["otp"] = send_otp(email)  # Send OTP to the user's email
                st.session_state["username"] = username
        if "otp" in st.session_state:
            user_otp = st.text_input("Enter OTP")
            new_password = st.text_input("New Password", type="password")
            if st.button("Reset Password"):
                if user_otp == st.session_state["otp"]:  # Verify OTP and reset the password
                    update_password(st.session_state["username"], new_password)
                    st.success("Password updated!")
                    st.session_state.clear()
                else:
                    st.error("Incorrect OTP")

    # Change Password Flow
    elif choice == "Change Password":
        st.subheader("Change Password")
        username = st.text_input("Username")
        old_password = st.text_input("Old Password", type="password")
        new_password = st.text_input("New Password", type="password")
        if st.button("Change"):
            if login_user(username, old_password):  # Verify old password before updating
                update_password(username, new_password)
                st.success("Password changed successfully!")
            else:
                st.error("Incorrect username or old password")

    # Admin Views (Only visible to admins)
    elif choice == "View Users":
        st.subheader("All Registered Users")
        st.dataframe(get_all_users())  # Display all registered users

    elif choice == "Login History":
        st.subheader("Login History")
        st.dataframe(get_login_history())  # Display login history of users
