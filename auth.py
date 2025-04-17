import streamlit as st
from user_data import (
    register_user, login_user, get_email_by_username,
    update_password, log_login, get_all_users, get_login_history
)
from email_utils import send_otp

def login_page():
    st.title("Login / Sign Up")
    menu = ["Login", "Sign Up", "Forgot Password", "Change Password"]
    if st.session_state.get("authenticated") and st.session_state.get("username") == "parasadmin":
        menu.extend(["View Users", "Login History"])
    choice = st.sidebar.selectbox("Menu", menu)

    # Show post-login success message
    if st.session_state.get("login_success"):
        st.success(st.session_state.pop("login_success"))

    # Show post-signup success message
    if st.session_state.get("signup_success"):
        st.success(st.session_state.pop("signup_success"))

    if choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_user(username, password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.session_state["login_success"] = f"Welcome {username}!"
                log_login(username)
                st.rerun()
            else:
                st.error("Invalid credentials")

    elif choice == "Sign Up":
        st.subheader("Sign Up")
        username = st.text_input("New Username")
        password = st.text_input("New Password", type="password")
        email = st.text_input("Email")
        if st.button("Send OTP"):
            st.session_state["otp"] = send_otp(email)
            st.session_state["temp_user"] = {"username": username, "password": password, "email": email}
        if "otp" in st.session_state:
            user_otp = st.text_input("Enter OTP")
            if st.button("Verify OTP"):
                if user_otp == st.session_state["otp"]:
                    temp = st.session_state["temp_user"]
                    if register_user(temp["username"], temp["password"], temp["email"]):
                        st.session_state["signup_success"] = "Account created!"
                        del st.session_state["otp"]
                        del st.session_state["temp_user"]
                        st.rerun()
                    else:
                        st.error("User already exists")

    elif choice == "Forgot Password":
        st.subheader("Forgot Password")
        username = st.text_input("Username")
        if st.button("Send OTP to Email"):
            email = get_email_by_username(username)
            if email:
                st.session_state["otp"] = send_otp(email)
                st.session_state["username"] = username
        if "otp" in st.session_state:
            user_otp = st.text_input("Enter OTP")
            new_password = st.text_input("New Password", type="password")
            if st.button("Reset Password"):
                if user_otp == st.session_state["otp"]:
                    update_password(st.session_state["username"], new_password)
                    st.success("Password updated!")
                    st.session_state.clear()
                else:
                    st.error("Incorrect OTP")

    elif choice == "Change Password":
        st.subheader("Change Password")
        username = st.text_input("Username")
        old_password = st.text_input("Old Password", type="password")
        new_password = st.text_input("New Password", type="password")
        if st.button("Change"):
            if login_user(username, old_password):
                update_password(username, new_password)
                st.success("Password changed successfully!")
            else:
                st.error("Incorrect username or old password")

    elif choice == "View Users":
        st.subheader("All Registered Users")
        st.dataframe(get_all_users())

    elif choice == "Login History":
        st.subheader("Login History")
        st.dataframe(get_login_history())
