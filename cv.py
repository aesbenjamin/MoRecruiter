import streamlit as st
from PIL import Image
import time
from llama_index.core.indices.property_graph import PropertyGraphIndex
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.core import Document
import os
import openai
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.neo4jvector import Neo4jVectorStore
from llama_index.core import SimpleDirectoryReader, KnowledgeGraphIndex, PropertyGraphIndex, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.graph_stores.neo4j import Neo4jGraphStore
from llama_index.core.graph_stores import SimpleGraphStore
#from llama_index.core.chat_engine import 
import logging
import nest_asyncio
import sys
from llama_index.core.schema import TextNode
from llama_index.core import DocumentSummaryIndex
from llama_index.core.retrievers import TreeSelectLeafEmbeddingRetriever, TreeAllLeafRetriever, TreeSelectLeafRetriever, TreeRootRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
import re

os.environ["OPENAI_API_KEY"] = "sk-MDwTK2Wq87oN3qR25-ElhN2XuIU00s_EyGG6QwTqr6T3BlbkFJQXFecaGZq73YsgSeJNVu8EgcDDhB3AVHMFpvp7XDAA"

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
system = """
					Você é o clone do Alex Benjamin, um Líder em modernização de ambientes de TI legados e especialista em Inteligência Artificial. Vai receber perguntas de recrutadores sobre 
					capacitações ou curiosidades suas. Não responda sem conhecimento prévio pelo contexto, apenas trabalhe com o 
					contexto e pergunta passadas.
		"""
helper_prompt = """
A pergunta a seguir é sobre a vida profissional de Alex Benjamin, como cargo, empresas, curiosidades:\n
Não utilize conhecimento prévio, apenas o do contexto:
"""
llm = OpenAI(temperature=0, model="gpt-4o-mini", system_prompt=system)
Settings.llm = llm
Settings.embed_model = OpenAIEmbedding(model_name="text-embedding-3-small")

if 'index' not in st.session_state:
	index_tr = load_index_from_storage(StorageContext.from_defaults(persist_dir="./cv"))
	st.session_state['index'] = index_tr
	chat_engine = st.session_state.index.as_chat_engine(chat_mode="condense_plus_context",system_prompt=system)
	st.session_state['chat'] = chat_engine

chat = st.session_state['chat']

st.set_page_config(
	page_title="Alex Benjamin - Conheça este Profissional de TI",
	page_icon=":trophy:",
	layout="wide",
	initial_sidebar_state="auto",
	#menu_items={
	#	"Conectar Alex no WhatsApp": "https://github.com/AdieLaine/Streamly",
	#	
	#}
)

# Função para criar um chat simples
def chat_interface():
	col1, col2 = st.columns([5, 2])
	with col1:
		st.subheader("Clone do Alex Benjamin")

		# List to hold the conversation
		container = st.container(height=300)
		user_input = st.chat_input("Pergunte algo sobre mim:")
		with container:
			if 'messages' not in st.session_state:
				st.session_state['messages'] = []
				init_msg = """
				Olá, eu sou o clone do Alex Benjamin. Fique à vontade para fazer perguntas 
				profissionais, ou até mesmo pessoais, como curiosidades, ou hobbies :D\n
				Se você preferir, pode utilizar a análise de conformidade, do lado direito desse chat,
				uma maneira simples e fácil de analisar se eu sou o candidato ideal para a sua vaga.								

				"""

				st.session_state['messages'].append({'role':'assistant', 'content': init_msg })
				#system = """
				#	Você é o clone do Alex Benjamin. Vai receber perguntas de recrutadores sobre 
				##	capacitações ou curiosidades suas. Não invente nada, apenas trabalhe com o 
				#	contexto e pergunta passadas.  Quando perguntarem quem é você, responda que é o Alex Benjamin.
				#"""
				#r = chat.chat("quem é você", prompt=system)
				#st.write(r.response)
			
			# Mostra as mensagens anteriores
				
			for message in st.session_state['messages']:
				with st.chat_message( message['role']):
					st.write(message['content'])

			if user_input:
				st.session_state['messages'].append({'role':'user', 'content': user_input})
				with st.chat_message("user"):
					st.write(user_input)
				res = chat.stream_chat(f"{helper_prompt} {user_input}")
				with st.chat_message("assistant"):
						st.write_stream(res.response_gen)
				st.session_state['messages'].append({'role':'assistant', 'content': res.response})
	with col2:
		st.subheader("Analise de Conformidade")
		options = st.multiselect(
				"Escolha palavras-chave para analisar o índice de alinhamento das capacitações do Alex com a vaga proposta:",
				["COBOL", "Natural", "Adabas", "Devops"],
				[],
			)
		title = st.text_area("Ou se preferir, cole aqui a descrição da vaga:", "")
		if st.button("Analisar"):
			with col1:
				with container:
					analise = f"""
					Analise se o Alex tem as capacitações abaixo:
					\n
					Descrição da vaga e palavras-chave:
					{title}
					\n
					{options}

					\n
					


					Ao final, gere um relatório e um índice de conformidade, que representa um percentual
					de capacitação do Alex em relação as palavras-chave.
					"""
					#st.session_state['messages'].append({'role':'user', 'content': analise})
					#with st.chat_message("user"):
					#	st.write(analise)
					res = chat.stream_chat(analise)
					with st.chat_message("assistant"):
							st.write_stream(res.response_gen)
					st.session_state['messages'].append({'role':'assistant', 'content': res.response})



			

			
			# Caixa de texto para o usuário

def print_images():
	#placeholder = st.sidebar.empty()  # Espaço reservado para as imagens
	image_paths =  ["image1.jpg", "image2.jpg"]
	for image_path in image_paths:
			img = Image.open(image_path)
			
			# Exibe a imagem no espaço reservado (atualiza no mesmo lugar)
			st.sidebar.image(img, use_column_width=True)
			
			# Aguardar o tempo de transição
			
	
# Inicializar a lista de imagens
images = [
	"./image1.jpg",
	"./image2.jpg",
]

# Inicializa o estado da sessão para o índice da imagem atual
if 'current_image_index' not in st.session_state:
	st.session_state['current_image_index'] = 0

# Função para avançar no carrossel
def next_image():
	st.session_state['current_image_index'] += 1
	if st.session_state['current_image_index'] >= len(images):
		st.session_state['current_image_index'] = 0

# Função para retroceder no carrossel
def prev_image():
	st.session_state['current_image_index'] -= 1
	if st.session_state['current_image_index'] < 0:
		st.session_state['current_image_index'] = len(images) - 1

tab1, tab2 = st.tabs(["Chat", "Galeria"])
# Mostrar a imagem atual

with tab1:
	chat_interface()

with tab2:
	st.image(images[st.session_state['current_image_index']])

# Botões de navegação

with tab2:
	col1, col2, col3 = st.columns([1, 4, 1])
	with col1:
		if st.button("◀️ Anterior"):
			prev_image()

	with col3:
		if st.button("Próxima ▶️"):
			next_image()

