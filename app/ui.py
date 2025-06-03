import streamlit as st
from .backend import create_account, fetch_messages

def show_ui():
    st.title("📧 بريد مؤقت")
    st.markdown("خدمة بريد مؤقت آمنة وسريعة - بديل مهمل")

    if st.button("🔁 توليد بريد جديد"):
        email, token = create_account()
        if email:
            st.session_state["email"] = email
            st.session_state["token"] = token
            st.success("✅ تم توليد البريد بنجاح!")
        else:
            st.error("❌ تعذر توليد البريد. حاول مرة أخرى.")

    if "email" in st.session_state and "token" in st.session_state:
        email = st.session_state["email"]
        token = st.session_state["token"]

        st.markdown("### 📨 بريدك المؤقت:")
        st.code(email)

        if st.button("📋 نسخ البريد"):
            st.toast("📋 تم نسخ البريد إلى الحافظة!")

        st.subheader("📥 صندوق الرسائل")
        if st.button("🔄 تحديث الرسائل"):
            st.session_state["refresh"] = True

        fetch_messages(token)
