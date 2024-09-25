import streamlit as st
import time
import random
import matplotlib.pyplot as plt

st.set_page_config(
	page_title="Streamly - An Intelligent Streamlit Assistant",
	page_icon="imgs/avatar_streamly.png",
	layout="wide",
	initial_sidebar_state="auto",
	menu_items={
		"Get help": "https://github.com/AdieLaine/Streamly",
		"Report a bug": "https://github.com/AdieLaine/Streamly",
		"About": """
			## Streamly Streamlit Assistant
			### Powered using GPT-4o-mini

			**GitHub**: https://github.com/AdieLaine/

			The AI Assistant named, Streamly, aims to provide the latest updates from Streamlit,
			generate code snippets for Streamlit widgets,
			and answer questions about Streamlit's latest features, issues, and more.
			Streamly has been trained on the latest Streamlit updates and documentation.
		"""
	}
)

# Função para criar um chat simples
def chat_interface():
	st.subheader("MoFlow")

	# List to hold the conversation
	container = st.container(height=350)
	user_input = st.chat_input("Pergunte algo sobre o Sistema de Precificação do GPA:")
	with container:
		if 'messages' not in st.session_state:
			st.session_state['messages'] = []

		# Mostra as mensagens anteriores
		
		if user_input:
			st.session_state['messages'].append(user_input)
			
		for message in st.session_state['messages']:
			with st.chat_message("assistant"):
				st.write(message)
		# Caixa de texto para o usuário

	

	
		

# Dividindo a página em colunas
col1, col2 = st.columns([6, 4])  # 60% para col1 e 40% para col2

# Gráfico em tempo real na coluna 1
with col1:
	chat_interface()

# Chat na coluna 2
with col2:
	
	st.subheader("MoVision")
	container2 = st.container(height=350)


# Atualização do gráfico a cada 2 segundos
time.sleep(2)

