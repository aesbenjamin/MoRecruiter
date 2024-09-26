import streamlit as st

from PIL import Image
import os
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import  Settings
from llama_index.core import StorageContext, load_index_from_storage
import logging
import sys
from llama_index.core.retrievers import TreeSelectLeafEmbeddingRetriever, TreeAllLeafRetriever, TreeSelectLeafRetriever, TreeRootRetriever
from fpdf import FPDF
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from io import BytesIO
import keyword_list
import base64

os.environ["OPENAI_API_KEY"] = "sk-MDwTK2Wq87oN3qR25-ElhN2XuIU00s_EyGG6QwTqr6T3BlbkFJQXFecaGZq73YsgSeJNVu8EgcDDhB3AVHMFpvp7XDAA"

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
system = """
					Você é o clone do Alex Benjamin, um Líder em modernização de ambientes de TI legados e especialista em Inteligência Artificial. Vai receber perguntas de recrutadores sobre 
					capacitações ou curiosidades suas. Não responda sem conhecimento prévio pelo contexto, apenas trabalhe com o 
					contexto e pergunta passadas.
		"""

llm = OpenAI(temperature=0, model="gpt-4o-mini", system_prompt=system)
Settings.llm = llm
Settings.embed_model = OpenAIEmbedding(model_name="text-embedding-3-small")

if 'index' not in st.session_state:
	index_tr = load_index_from_storage(StorageContext.from_defaults(persist_dir="./vecCv"))
	st.session_state['index'] = index_tr
	chat_engine = st.session_state.index.as_chat_engine(chat_mode="condense_plus_context",system_prompt=system, similarity_top_k=10)
	chat_engine2 = st.session_state.index.as_chat_engine(chat_mode="condense_plus_context",system_prompt=system, similarity_top_k=30)
	st.session_state['chat'] = chat_engine
	st.session_state['chat_analise'] = chat_engine2

chat = st.session_state['chat']
chat_analise = st.session_state['chat_analise']
st.set_page_config(
	page_title="Alex Benjamin - Conheça este Profissional de TI",
	page_icon=":trophy:",
	layout="wide",
	initial_sidebar_state="expanded",
)

def get_pdf2():
	# Criar um buffer em memória
	str1 = ""
	
	buffer = BytesIO()

	# Criar o documento PDF
	doc = SimpleDocTemplate(buffer, pagesize=letter)
	
	# Estilos de texto (para parágrafos)
	styles = getSampleStyleSheet()

	# Criar um parágrafo a partir do texto
	elementos = []

	paragraph_titulo = Paragraph( "MoRecruiter - Alex Benjamin", styles["Title"]) 
	caminho_imagem = "./image3.jpg"  
	imagem = Image(caminho_imagem, 200, 300)


	elementos.append(paragraph_titulo)
	elementos.append(Spacer(1, 12))
	elementos.append(Spacer(1, 12))
	elementos.append(imagem)
	elementos.append(Spacer(1, 12))

	if 'messages' in st.session_state:
		for message in st.session_state['messages']:
				ini = ""
				if message['role'] == 'assistant':
					ini = 'Alex Benjamin: '
				if message['role'] == 'user':
					ini = 'Recrutador: '
				msg = ini + message['content']
				texto_com_html = '<br />'.join(msg.splitlines())
				paragrafo = Paragraph( texto_com_html, styles["BodyText"]) 
				elementos.append(paragrafo)
				elementos.append(Spacer(1, 12))

	# Criar o PDF com os elementos
	doc.build(elementos)
	# Mover o cursor do buffer para o início
	buffer.seek(0)
	# O conteúdo binário do PDF está agora no buffer
	return buffer.getvalue()

def get_pdf():
	pdf = FPDF()
	pdf.add_page()
	pdf.set_font("Arial", size=12)
	pdf.cell(200, 10, txt="Histórico de conversa com o clone do Alex Benjamin", ln=True, align="C")
	if 'messages' in st.session_state:
		str1 = ""
		for message in st.session_state['messages']:
				str1 = str1 + message['content'] + '\n'
		pdf.multi_cell(0, 10, str1)
	pdf_content = pdf.output(dest='S').encode('utf-8')
	return pdf_content

# Função para criar um chat simples
def chat_interface():
	ph = st.empty()
	col1, col2 = st.columns([5, 2])
	with col1:
		st.subheader("Clone do Alex Benjamin")

		# List to hold the conversation
		container = st.container(height=250)
		colA, colB,colC = st.columns([5,1,1])
		with colA:
			user_input = st.chat_input("Pergunte algo sobre mim:")
		with colB:
			if st.button("Gerar PDF"):
				with colC:
					st.download_button("Baixar PDF", get_pdf2(), file_name= "historico.pdf")
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
	
			for message in st.session_state['messages']:
				with st.chat_message( message['role']):
					st.write(message['content'])

			if user_input:
				st.session_state['messages'].append({'role':'user', 'content': user_input})
				with st.chat_message("user"):
					st.write(user_input)
				res = chat.stream_chat(f"{user_input}")
				with st.chat_message("assistant"):
						st.write_stream(res.response_gen)
				st.session_state['messages'].append({'role':'assistant', 'content': res.response})
	with col2:
		st.subheader("Análise de Conformidade")
		options = st.multiselect(
				"Escolha palavras-chave para analisar o índice de alinhamento das capacitações do Alex com a vaga proposta:",
				keyword_list.key_list,
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
					res = chat_analise.stream_chat(analise)
					with st.chat_message("assistant"):
							st.write_stream(res.response_gen)
					st.session_state['messages'].append({'role':'assistant', 'content': res.response})

def print_images():
	#placeholder = st.sidebar.empty()  # Espaço reservado para as imagens
	image_paths =  ["image1.jpg", "image2.jpg"]
	for image_path in image_paths:
			img = Image.open(image_path)
			st.sidebar.image(img, use_column_width=True)
			
	
# Inicializar a lista de imagens
images = [
	"./image1.jpg",
	"./image2.jpg",
	"./image4.jpg",
	"./image5.jpg",
	"./image6.jpg",
]

# Inicializa o estado da sessão para o índice da imagem atual
if 'current_image_index' not in st.session_state:
	st.session_state['current_image_index'] = 0
# Função para avançar no carrossel
def next_image():
	st.session_state['current_image_index'] += 1
	if st.session_state['current_image_index'] >= len(images):
		st.session_state['current_image_index'] = 0
	#photo_ph.image(images[st.session_state['current_image_index']])

# Função para retroceder no carrossel
def prev_image():
	st.session_state['current_image_index'] -= 1
	if st.session_state['current_image_index'] < 0:
		st.session_state['current_image_index'] = len(images) - 1

def sidebar():
	st.sidebar.image('./image3.jpg')
	cont = st.sidebar.container()
	cont.write("""
			Alex Benjamin
			\n
			Líder em Modernização de Sistemas Legados, especialista em 
			Inteligência Artifical Generativa e Engenheiro de Software há mais 18 anos.
			\n
			Utilize o chat ao lado para conhecer um pouco de mim e minhas qualificações.	
			""")
	cont.write("""
			Este site foi construído com Python e Streamlit, e seu backend com o motor MoMapping. \n
			Acesse o site e saiba mais: 
			""")
	cont.link_button("MoMapping", "https://site.momapping.com.br")

st.subheader("MoRecruiter")
tab_chat, tab_galeria, tab_video, tab_cv, tab_contato = st.tabs(["Chat", "Galeria", "Video", "Currículo", "Contato"])
# Mostrar a imagem atual

with tab_chat:
	chat_interface()


# Botões de navegação

with tab_galeria:
	col1, col2, col3, col4, col5 = st.columns([1, 1, 3, 1,1])
	with col1:
		if st.button("◀️ Anterior"):
			prev_image()

	with col5:
		if st.button("Próxima ▶️"):
			next_image()

	with col3:
		st.image(images[st.session_state['current_image_index']])

with tab_video:
	col1, col2, col3 = st.columns([1,4,1])
	with col2:
		h = 300
		container_style = f"""
		<style>
		.centered-container {{
			display: flex;
			justify-content: center;
			align-items: center;
			height: {h}px;  /* Definindo a altura do container explicitamente */
			border: 1px solid red;
		}}
		</style>
		"""

		# Aplica o estilo CSS
		st.markdown(container_style, unsafe_allow_html=True)

		# Adiciona o container com o texto centralizado
		st.markdown('<div class="centered-container"><p>Em breve</p></div>', unsafe_allow_html=True)
with tab_cv:
	col1, col2, col3 = st.columns([1,4,1])
	with col2:
		st.title("Curriculum Alex Benjamin")
		pdf_file_path = "./curriculum_alex_benjamin.pdf"
		pdf_data = ""
		with open(pdf_file_path, "rb") as f:
			pdf_data = f.read()
		st.download_button(
			label="Baixar PDF",
			data=pdf_data,
			file_name="curriculum_alex_benjamin.pdf",
			mime="application/pdf"
		)
		base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
		pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
		st.write('Visuzalição do PDF (Apenas para desktop):')
		st.markdown(pdf_display, unsafe_allow_html=True)		

with tab_contato:
	col1,col2,col3,col4 = st.columns([1,1,3,3])
	with col1:
		st.image(image="./whatsapp.png")
		st.link_button(label="WhatsApp",url="https://wa.me/5511965590645?text=Ol%C3%A1,%20gostaria%20de%20saber%20um%20pouco%20mais%20sobre%20o%20seu%20perfil!")
	with col2:
		st.image(image="./linkedin.png")
		st.link_button(label="Linkedin",url="http://www.linkedin.com/in/alex-benjamin-43b1b438")


sidebar()