from datetime import datetime, timezone
import re

import bcrypt
from pymongo.errors import DuplicateKeyError, PyMongoError
import streamlit as st

from database.connection import predictions_collection, users_collection


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def initialize_session():
    """Create login-session values when a user first opens the app."""
    st.session_state.setdefault("authenticated", False)
    st.session_state.setdefault("user_id", "")
    st.session_state.setdefault("user_name", "")
    st.session_state.setdefault("user_email", "")


def clear_authentication():
    """Clear the current user's login session."""
    st.session_state.authenticated = False
    st.session_state.user_id = ""
    st.session_state.user_name = ""
    st.session_state.user_email = ""


def is_authenticated():
    initialize_session()
    return st.session_state.authenticated


def normalize_email(email):
    return email.strip().lower()


def create_account(name, email, password):
    """Create an account without storing a plaintext password."""
    name = name.strip()
    email = normalize_email(email)

    if not name:
        return "Please enter your name."

    if not EMAIL_PATTERN.fullmatch(email):
        return "Please enter a valid email address."

    if len(password) < 8:
        return "Password must contain at least 8 characters."

    if len(password.encode("utf-8")) > 72:
        return "Password is too long."

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    try:
        users_collection.create_index(
            "email",
            unique=True,
            name="unique_user_email"
        )

        users_collection.insert_one({
            "name": name,
            "email": email,
            "password_hash": password_hash,
            "created_at": datetime.now(timezone.utc)
        })

        return None

    except DuplicateKeyError:
        return "An account already exists for this email address."

    except PyMongoError:
        return "Account could not be created. Please try again later."


def login_user(email, password):
    """Verify a login attempt and create the Streamlit session."""
    email = normalize_email(email)

    if not email or not password:
        return False, "Enter your email address and password."

    try:
        user = users_collection.find_one({"email": email})
    except PyMongoError:
        return False, "Login is unavailable right now. Please try again later."

    password_hash = user.get("password_hash", "") if user else ""

    try:
        password_is_valid = (
            user is not None
            and bcrypt.checkpw(
                password.encode("utf-8"),
                password_hash.encode("utf-8")
            )
        )
    except (ValueError, TypeError):
        password_is_valid = False

    if not password_is_valid:
        return False, "Invalid email address or password."

    st.session_state.authenticated = True
    st.session_state.user_id = str(user["_id"])
    st.session_state.user_name = user["name"]
    st.session_state.user_email = user["email"]

    return True, ""


def delete_current_account(password):
    """Delete the signed-in account and all predictions linked to it."""
    user_email = st.session_state.user_email
    user_id = st.session_state.user_id

    try:
        user = users_collection.find_one({"email": user_email})
    except PyMongoError:
        return False, "Account deletion is unavailable right now."

    if not user:
        return False, "Your account could not be found."

    try:
        password_is_valid = bcrypt.checkpw(
            password.encode("utf-8"),
            user["password_hash"].encode("utf-8")
        )
    except (ValueError, TypeError):
        password_is_valid = False

    if not password_is_valid:
        return False, "Incorrect password. Your account was not deleted."

    try:
        deleted_predictions = predictions_collection.delete_many(
            {"user_id": user_id}
        )

        users_collection.delete_one({"_id": user["_id"]})

    except PyMongoError:
        return False, "Account deletion failed. Please try again later."

    clear_authentication()

    return (
        True,
        f"Your account and {deleted_predictions.deleted_count} prediction record(s) were deleted."
    )


def show_authentication_page():
    """Display Login and Create Account tabs on one page."""
    initialize_session()

    deleted_message = st.session_state.pop("account_deleted_message", None)

    st.title("Credit Risk Predictor")
    st.caption("Sign in to use the credit-risk prediction tool.")

    if deleted_message:
        st.success(deleted_message)

    login_tab, signup_tab = st.tabs(["Login", "Create Account"])

    with login_tab:
        with st.form("login_form"):
            email = st.text_input("Email address")
            password = st.text_input("Password", type="password")
            login_submitted = st.form_submit_button("Log in")

        if login_submitted:
            success, message = login_user(email, password)

            if success:
                st.rerun()
            else:
                st.error(message)

    with signup_tab:
        with st.form("signup_form", clear_on_submit=True):
            name = st.text_input("Full name")
            email = st.text_input("Email address")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input(
                "Confirm password",
                type="password"
            )
            signup_submitted = st.form_submit_button("Create account")

        if signup_submitted:
            if password != confirm_password:
                st.error("Passwords do not match.")
            else:
                error = create_account(name, email, password)

                if error:
                    st.error(error)
                else:
                    st.success("Account created. You can now log in.")


def require_login():
    """Prevent unauthenticated users from viewing protected pages."""
    if not is_authenticated():
        show_authentication_page()
        st.stop()


def show_logout_button():
    """Show logout and account-deletion actions in the sidebar."""
    with st.sidebar:
        st.caption(f"Signed in as {st.session_state.user_name}")

        if st.button("Log out"):
            clear_authentication()
            st.rerun()

        st.divider()

        with st.expander("Danger zone"):
            st.warning(
                "Deleting your account permanently removes your account "
                "and all predictions linked to it."
            )

            with st.form("delete_account_form"):
                password = st.text_input(
                    "Enter your password to confirm",
                    type="password"
                )
                confirm_delete = st.checkbox(
                    "I understand this action cannot be undone."
                )
                delete_submitted = st.form_submit_button(
                    "Delete my account"
                )

            if delete_submitted:
                if not confirm_delete:
                    st.error("Please confirm that you understand this action.")
                else:
                    deleted, message = delete_current_account(password)

                    if deleted:
                        st.session_state.account_deleted_message = message
                        st.rerun()
                    else:
                        st.error(message)