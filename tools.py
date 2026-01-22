"""
Utility tools for the AI Booking Assistant.

Includes:
1) RAG Tool: runs a retrieval-augmented answer for a user query.
2) Booking Persistence Tool: persists a confirmed booking into SQLite.
3) Email Tool: sends notification emails via SMTP.

All tools handle their own errors and return structured dict responses.
"""

from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from typing import Any, Dict, Iterable, Optional, Union

from database import insert_booking, insert_customer, init_db

from booking_flow import BookingData
from config import (
    SMTP_FROM_EMAIL,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_USE_TLS,
    SMTP_USERNAME,
)
from rag_pipeline import answer_query as rag_answer_query

# Try to import streamlit for secrets, but don't fail if not available
try:
    import streamlit as st
    _HAS_STREAMLIT = True
except ImportError:
    _HAS_STREAMLIT = False


def rag_tool(query: str, chat_history: Optional[Iterable[Dict[str, str]]] = None) -> Dict[str, Any]:
    """
    Run the RAG pipeline for a given query.

    Returns:
        {
            "success": bool,
            "answer": str | None,
            "contexts": list,
            "error": str | None
        }
    """
    try:
        result = rag_answer_query(query=query, chat_history=list(chat_history or []))
        return {
            "success": True,
            "answer": result.get("answer", ""),
            "contexts": result.get("contexts", []),
            "error": None,
        }
    except Exception as exc:  # pragma: no cover - defensive
        return {
            "success": False,
            "answer": None,
            "contexts": [],
            "error": str(exc),
        }


def booking_persistence_tool(booking: Union[BookingData, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Persist a confirmed booking into the SQLite database.

    Expects either a BookingData instance or a dict with keys:
    - name
    - email
    - phone
    - booking_type
    - date
    - time

    Returns:
        {
            "success": bool,
            "booking_id": int | None,
            "customer_id": int | None,
            "error": str | None
        }
    """
    try:
        payload = booking if isinstance(booking, dict) else booking.__dict__

        name = str(payload.get("name", "")).strip()
        email = str(payload.get("email", "")).strip()
        phone = str(payload.get("phone", "")).strip()
        booking_type = str(payload.get("booking_type", "")).strip()
        date = str(payload.get("date", "")).strip()
        time = str(payload.get("time", "")).strip()

        if not all([name, email, phone, booking_type, date, time]):
            return {
                "success": False,
                "booking_id": None,
                "customer_id": None,
                "error": "Missing required booking fields.",
            }

        # Ensure DB schema exists
        init_db()

        customer_id = insert_customer(name=name, email=email, phone=phone)
        if customer_id is None:
            return {
                "success": False,
                "booking_id": None,
                "customer_id": None,
                "error": "Failed to create customer record.",
            }

        booking_id = insert_booking(
            customer_id=customer_id,
            service=booking_type,
            booking_date=date,
            booking_time=time,
            status="confirmed",
            notes=None,
        )

        if booking_id is None:
            return {
                "success": False,
                "booking_id": None,
                "customer_id": customer_id,
                "error": "Failed to create booking record.",
            }

        return {
            "success": True,
            "booking_id": booking_id,
            "customer_id": customer_id,
            "error": None,
        }
    except Exception as exc:  # pragma: no cover - defensive
        return {
            "success": False,
            "booking_id": None,
            "customer_id": None,
            "error": str(exc),
        }


def email_tool(to_email: str, subject: str, body: str) -> Dict[str, Any]:
    """
    Send an email using SMTP settings from Streamlit secrets or configuration.

    Returns:
        {
            "success": bool,
            "error": str | None
        }
    """
    # Try to get SMTP settings from Streamlit secrets first, fallback to config
    smtp_host = SMTP_HOST
    smtp_port = SMTP_PORT
    smtp_username = SMTP_USERNAME
    smtp_password = SMTP_PASSWORD
    smtp_from_email = SMTP_FROM_EMAIL
    smtp_use_tls = SMTP_USE_TLS

    if _HAS_STREAMLIT:
        try:
            # Get secrets if available
            secrets = st.secrets
            smtp_host = secrets.get("SMTP_SERVER", SMTP_HOST)
            smtp_port = int(secrets.get("SMTP_PORT", SMTP_PORT))
            smtp_username = secrets.get("EMAIL_USER", SMTP_USERNAME)
            smtp_password = secrets.get("EMAIL_PASSWORD", SMTP_PASSWORD)
            # Use EMAIL_USER as FROM email if SMTP_FROM_EMAIL is not in secrets
            smtp_from_email = secrets.get("EMAIL_USER", SMTP_FROM_EMAIL)
        except Exception:
            # If secrets are not available, use config defaults
            pass

    # Validate required settings
    if smtp_host == "smtp.example.com" or not smtp_username or not smtp_password:
        return {
            "success": False,
            "error": "SMTP configuration missing. Please set EMAIL_USER, EMAIL_PASSWORD, and SMTP_SERVER in Streamlit secrets.",
        }

    message = EmailMessage()
    message["From"] = smtp_from_email
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
            if smtp_use_tls:
                server.starttls()
            if smtp_username and smtp_password:
                server.login(smtp_username, smtp_password)
            server.send_message(message)
        return {"success": True, "error": None}
    except Exception as exc:  # pragma: no cover - defensive
        return {"success": False, "error": str(exc)}


__all__ = [
    "rag_tool",
    "booking_persistence_tool",
    "email_tool",
]



