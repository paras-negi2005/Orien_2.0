import pandas as pd
import os
import toml

# Load values from secrets.toml
secrets = toml.load(".streamlit/secrets.toml")

# Get admin values from secrets
ADMIN_USERNAME = secrets["ADMIN_USERNAME"]
ADMIN_PASSWORD = secrets["ADMIN_PASSWORD"]
ADMIN_EMAIL = secrets["ADMIN_EMAIL"]

USER_FILE = "users.csv"
LOGIN_HISTORY_FILE = "login_history.csv"

def init_user_data():  # For creating new columns of username, password, email and adding admin info to the df and csv file
    if not os.path.exists(USER_FILE):
        df = pd.DataFrame(columns=["username", "password", "email"])
        df.to_csv(USER_FILE, index=False)  # telling pandas NOT to write the index column of the DataFrame into the CSV file
    else:
        df = pd.read_csv(USER_FILE)
        if ADMIN_USERNAME not in df["username"].values:
            new_admin = pd.DataFrame([{"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD, "email": ADMIN_EMAIL}])
            df = pd.concat([df, new_admin], ignore_index=True)  # Appends the new admin row to the existing DataFrame (df)
            df.to_csv(USER_FILE, index=False)  # Saves the updated DataFrame back to the CSV file

def register_user(username, password, email):  # Function to add new user data to the csv file or check if the same data exists
    df = pd.read_csv(USER_FILE)
    if username in df["username"].values or email in df["email"].values:  # Checks if the username or email is already taken
        return False
    new_user_data = pd.DataFrame([{"username": username, "password": password, "email": email}])
    df = pd.concat([df, new_user_data], ignore_index=True)
    df.to_csv(USER_FILE, index=False)
    return True

def login_user(username, password):  # This function filters the DataFrame to find a row that matches username and password
    df = pd.read_csv(USER_FILE)
    user = df[(df["username"] == username) & (df["password"] == password)]
    return not user.empty

def get_email_by_username(username):  # Function for getting the registered email id
    df = pd.read_csv(USER_FILE)
    user = df[df["username"] == username]
    return user["email"].values[0] if not user.empty else None

def update_password(username, new_password):  # Function for updating the password
    df = pd.read_csv(USER_FILE)
    df.loc[df["username"] == username, "password"] = new_password
    df.to_csv(USER_FILE, index=False)

def log_login(username):  # Function for adding login details in csv file like time and device
    from datetime import datetime
    import platform
    login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    device_info = platform.system() + " " + platform.release()
    if not os.path.exists(LOGIN_HISTORY_FILE):
        df = pd.DataFrame(columns=["username", "login_time", "device_info"])
        df.to_csv(LOGIN_HISTORY_FILE, index=False)
    df = pd.read_csv(LOGIN_HISTORY_FILE)
    new_log = pd.DataFrame([{"username": username, "login_time": login_time, "device_info": device_info}])
    df = pd.concat([df, new_log], ignore_index=True)
    df.to_csv(LOGIN_HISTORY_FILE, index=False)

def get_all_users():
    return pd.read_csv(USER_FILE) if os.path.exists(USER_FILE) else pd.DataFrame()

def get_login_history():  # Attempts to read the login history data from a CSV file; returns empty DataFrame if file doesn't exist
    return pd.read_csv(LOGIN_HISTORY_FILE) if os.path.exists(LOGIN_HISTORY_FILE) else pd.DataFrame()
