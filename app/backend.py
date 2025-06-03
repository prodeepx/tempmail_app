import requests
import streamlit as st
import uuid

def create_account():
    try:
        domain_resp = requests.get("https://api.mail.tm/domains")
        domain = domain_resp.json()["hydra:member"][0]["domain"]

        username = f"user_{uuid.uuid4().hex[:8]}"
        email = f"{username}@{domain}"
        password = uuid.uuid4().hex

        account_data = {"address": email, "password": password}
        create = requests.post("https://api.mail.tm/accounts", json=account_data)

        if create.status_code == 201:
            token_resp = requests.post("https://api.mail.tm/token", json=account_data)
            token = token_resp.json()["token"]
            return email, token
    except:
        pass
    return None, None

def fetch_messages(token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        inbox = requests.get("https://api.mail.tm/messages", headers=headers).json()

        if inbox["hydra:member"]:
            for msg in inbox["hydra:member"]:
                msg_detail = requests.get(
                    f"https://api.mail.tm/messages/{msg['id']}", headers=headers
                ).json()

                message_text = msg_detail.get("text") or msg_detail.get("html") or "📭 لا يوجد محتوى"

                st.markdown(
                    f"""
                    <div class='msg-card'>
                        <strong>✉️ من:</strong> {msg['from']['address']}<br>
                        <strong>📝 الموضوع:</strong> {msg['subject']}<br>
                        <strong>📅 التاريخ:</strong> {msg['createdAt']}<hr>
                        <div class='msg-content'>{message_text}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("📭 لا توجد رسائل حالياً.")
    except Exception as e:
        st.error(f"❌ فشل في جلب الرسائل: {e}")
