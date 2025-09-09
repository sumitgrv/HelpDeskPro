import os, requests, json, streamlit as st

st.set_page_config(page_title="HelpDeskPro (RAG)", layout="wide")
st.title("HelpDeskPro — Knowledge-Centered Support (GenAI + RAG)")

API = os.getenv("API_URL", "http://backend:8000")

with st.sidebar:
    st.header("Upload Document")
    up = st.file_uploader("PDF / DOCX / MD", type=["pdf","docx","md","txt"])
    owner = st.text_input("Owner ID", value="agent-1")
    if st.button("Upload") and up is not None:
        files = {"file": (up.name, up.getvalue(), "application/octet-stream")}
        data = {"owner_id": owner}
        r = requests.post(f"{API}/v1/documents", files=files, data=data)
        st.success(r.text)

st.header("Chat")
if "thread_id" not in st.session_state:
    st.session_state.thread_id = ""

question = st.text_input("Ask a question")
if st.button("Send") and question:
    payload = {"question": question, "thread_id": st.session_state.thread_id}
    r = requests.post(f"{API}/v1/chat/query", json=payload, timeout=60)
    if r.ok:
        resp = r.json()
        st.session_state.thread_id = resp["thread_id"]
        st.subheader("Answer")
        st.write(resp["answer"])
        st.caption(f"Sources: {[ (s['chunk_id'], round(s['score'],3)) for s in resp.get('sources', []) ]}")
        st.session_state.last_answer_id = resp["answer_id"]

st.header("Feedback")
rating = st.selectbox("Was this helpful?", ["HELPFUL", "NOT_HELPFUL"])
notes = st.text_area("Notes (optional)")
if st.button("Submit Feedback") and st.session_state.get("last_answer_id"):
    p = {"answer_id": st.session_state["last_answer_id"], "rating": rating, "notes": notes}
    r = requests.post(f"{API}/v1/feedback", json=p)
    st.success(r.text)
