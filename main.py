"""
Streamlit UI entry point for the AI Booking Assistant.

This is the ONLY file responsible for UI concerns (Streamlit widgets, rendering).
All non-UI logic is delegated to app modules (chat, booking flow, RAG, tools, db).
"""

from __future__ import annotations

from typing import Any, Dict, List

import os
import sys

# Ensure project root is on sys.path when running:
#   streamlit run main.py
_PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import streamlit as st
import google.generativeai as genai

from chat_logic import get_message_history, handle_user_message
from rag_pipeline import ingest_pdfs
from tools import booking_persistence_tool, email_tool
from admin_dashboard import render_admin_dashboard
from config import APP_NAME


STATUS_KEY = "status_messages"


def _init_ui_state() -> None:
    if STATUS_KEY not in st.session_state:
        st.session_state[STATUS_KEY] = []  # type: ignore[assignment]


def _push_status(level: str, message: str) -> None:
    """
    Store a status message to display in the UI.
    level: 'success' | 'info' | 'warning' | 'error'
    """
    _init_ui_state()
    st.session_state[STATUS_KEY].append({"level": level, "message": message})
    # Keep last 10 status messages
    st.session_state[STATUS_KEY] = st.session_state[STATUS_KEY][-10:]


def _render_status_messages() -> None:
    _init_ui_state()
    for item in st.session_state[STATUS_KEY]:
        level = item.get("level", "info")
        msg = item.get("message", "")
        if not msg:
            continue
        if level == "success":
            st.success(msg)
        elif level == "warning":
            st.warning(msg)
        elif level == "error":
            st.error(msg)
        else:
            st.info(msg)


def _render_chat_history(messages: List[Dict[str, str]]) -> None:
    for msg in messages:
        role = msg.get("role", "assistant")
        content = msg.get("content", "")
        if not content:
            continue
        with st.chat_message(role):
            st.markdown(content)


def _chat_page() -> None:
    st.title(APP_NAME)
    st.caption("Upload PDFs to enable RAG. Use chat below to ask questions or make a booking.")
    st.info("Using Google Gemini API (Free Tier) for AI responses.")

    with st.sidebar:
        st.subheader("Knowledge Base")
        uploaded = st.file_uploader(
            "Upload PDFs",
            type=["pdf"],
            accept_multiple_files=True,
            help="Uploaded PDFs are ingested for retrieval-augmented answers.",
        )
        if uploaded:
            try:
                added = ingest_pdfs(uploaded)
                _push_status("success", f"Ingested {added} chunks from uploaded PDFs.")
            except Exception as exc:  # defensive
                _push_status("error", f"PDF ingestion failed: {exc}")

    _render_status_messages()

    # Render conversation so far
    history = get_message_history()
    if not history:
        with st.chat_message("assistant"):
            st.markdown(
                "Hi! I can answer questions using your uploaded PDFs, or help you place a booking. "
                "How can I help today?"
            )
    else:
        _render_chat_history(history)

    # Chat input
    user_text = st.chat_input("Type your message…")
    if not user_text:
        return

    # Show the user message immediately (chat_logic also stores it)
    with st.chat_message("user"):
        st.markdown(user_text)

    # Delegate to chat logic
    with st.spinner("Processing..."):
        assistant_reply, booking_payload = handle_user_message(user_text)

    with st.chat_message("assistant"):
        st.markdown(assistant_reply)

    # If booking confirmed, persist + email
    if booking_payload is not None:
        # Show immediate confirmation
        st.success("✅ Booking Confirmed! Processing your booking...")
        persist = booking_persistence_tool(booking_payload)
        if persist.get("success"):
            booking_id = persist.get("booking_id")
            _push_status("success", f"✅ Booking saved successfully! (Booking ID: {booking_id})")

            # Send confirmation email (best-effort)
            email_res = email_tool(
                to_email=booking_payload.email,
                subject=f"Booking Confirmation - ID: {booking_id}",
                body=(
                    "Your booking has been confirmed!\n\n"
                    "Booking Details:\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"Booking ID: {booking_id}\n"
                    f"Name: {booking_payload.name}\n"
                    f"Email: {booking_payload.email}\n"
                    f"Phone: {booking_payload.phone}\n"
                    f"Service Type: {booking_payload.booking_type}\n"
                    f"Date: {booking_payload.date}\n"
                    f"Time: {booking_payload.time}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "Thank you for your booking!\n\n"
                    "If you need to make any changes, please contact us.\n"
                ),
            )
            if email_res.get("success"):
                _push_status("success", f"📧 Confirmation email sent to {booking_payload.email}")
            else:
                error_msg = email_res.get('error', 'Unknown error')
                _push_status("warning", f"⚠️ Booking saved, but email failed: {error_msg}")
                _push_status("info", "💡 Please check your email inbox - the booking is still confirmed in our system.")
        else:
            _push_status("error", f"Booking confirmation received, but DB save failed: {persist.get('error')}")

        st.rerun()


def main() -> None:
    st.set_page_config(page_title=APP_NAME, layout="wide")
    _init_ui_state()

    # Initialize database on startup
    try:
        from database import init_db
        init_db()
    except Exception as e:
        _push_status("warning", f"Database initialization warning: {str(e)}")

    # Configure Gemini API key for downstream modules (no UI code outside main.py)
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        api_key = ""
    if api_key:
        os.environ["GEMINI_API_KEY"] = str(api_key)
        try:
            genai.configure(api_key=str(api_key))
        except Exception as e:
            _push_status("error", f"Failed to configure Gemini API: {str(e)}")
    else:
        _push_status(
            "error",
            "Missing GEMINI_API_KEY. Set it in `.streamlit/secrets.toml` (Streamlit Cloud: Settings → Secrets).",
        )

    with st.sidebar:
        st.header(APP_NAME)
        page = st.radio("Navigate", options=["Chat", "Admin Dashboard"], index=0)

    try:
        if page == "Admin Dashboard":
            render_admin_dashboard()
        else:
            _chat_page()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.exception(e)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Fallback error display if main() fails
        import traceback
        st.error(f"Critical error: {str(e)}")
        st.code(traceback.format_exc())



