import streamlit as st

col1, col2 = st.columns(2)

col1.write("oi")
with col2:
	messages = col2.container(height=300)
	if prompt := col2.chat_input("Say something"):
		messages.chat_message("user").write(prompt)
		messages.chat_message("assistant").write(f"Echo: {prompt}")