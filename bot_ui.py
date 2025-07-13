import streamlit as st
import x_api  
from llm_utils import generate_reply  


if "tweets" not in st.session_state:
    st.session_state.tweets = []
if "monitoring" not in st.session_state:
    st.session_state.monitoring = False
if "replies" not in st.session_state:
    st.session_state.replies = {}

st.title("_X_ :green[Mention Tracker] + :blue[Auto Responder]")

query = st.text_input("Enter keyword or @handle to monitor:")
reply_style = st.selectbox("Choose reply style", ["Friendly", "Professional", "Funny"])
st.markdown("---")

if st.button("Start Monitoring"):
    if query:
        st.session_state.tweets = x_api.get_recent_tweets(query)
        st.session_state.monitoring = True
        st.success("Monitoring started.")
    else:
        st.warning("Please enter a keyword or handle.")

if st.button("Stop Monitoring"):
    st.session_state.monitoring = False
    st.info("Monitoring stopped. Tweets will remain displayed.")

if st.button("Reply All"):
    if not st.session_state.tweets:
        st.warning("No tweets to reply to. Start monitoring first.")
    else:
        with st.spinner("Generating replies..."):
            for tweet in st.session_state.tweets:
                if tweet["id"] not in st.session_state.replies:
                    reply = generate_reply(tweet["content"], reply_style)
                    st.session_state.replies[tweet["id"]] = reply
        st.success("Replies generated!")

st.markdown("---")
if st.session_state.tweets:
    st.subheader("Recent Tweets")
    for tweet in st.session_state.tweets:
        with st.container():
            st.markdown(f"**User:** @{tweet['username']} | *{tweet['created_at']}*")
            st.markdown(f"**Tweet:** {tweet['content']}")
            st.markdown(f"[🔗 View Tweet]({tweet['url']})")

            if tweet["id"] in st.session_state.replies:
                st.success(f"💬 AI Reply: {st.session_state.replies[tweet['id']]}")
            st.markdown("---")
