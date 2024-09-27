import streamlit as st
import streamlit.components.v1 as components
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
import translate
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
os.environ["OPENAI_API_KEY"] = st.secrets['secrets']['OPENAI_API_KEY']
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

if 'language' not in st.session_state:
	st.session_state['language'] = 0

language = st.session_state['language']

system = translate.system[language]

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
	page_title="Alex Benjamin - Meet this IT Profissional",
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
					ini = translate.ini[language]
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
	pdf.cell(200, 10, txt=translate.txt[language], ln=True, align="C")
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
		sub_txt = translate.sub_txt[language]
		st.subheader(sub_txt)

		# List to hold the conversation
		container = st.container(height=250)
		colA, colB,colC = st.columns([5,1,1])
		with colA:
			input_txt = translate.input_txt[language]
			user_input = st.chat_input(input_txt)
		with colB:
			txt_pdf = translate.txt_pdf[language]
			if st.button(txt_pdf):
				with colC:
					txt_baixar_pdf = translate.txt_baixar_pdf[language]
					st.download_button(txt_baixar_pdf, get_pdf2(), file_name= "MoRecruiter_Alex_history.pdf")
		with container:
			if 'messages' not in st.session_state:
				st.session_state['messages'] = []
				
				init_msg = translate.init_msg[language]

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
		txt_conformidade = translate.txt_conformidade[language]
		st.subheader(txt_conformidade)
		txt_multi = translate.txt_multi[language]
		options = st.multiselect(
				txt_multi,
				keyword_list.key_list,
				[],
			)
		txt_descr = translate.txt_descr[language]
		title = st.text_area(txt_descr, "")
		txt_analisar = translate.txt_analisar[language]
		if st.button(txt_analisar):
			with col1:
				with container:
					analise_tmp = translate.get_analise(title,options)
					analise = analise_tmp[language]
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
	sidebar_txt1 = translate.sidebar_txt1[language]
	cont.write(sidebar_txt1)
	sidebar_txt2 = translate.sidebar_txt2[language]
	cont.write(sidebar_txt2)
	cont.link_button("MoMapping", "https://site.momapping.com.br")

col1, col2, col3, col4 = st.columns([2,1,1,4])
with col1:
	st.subheader("MoRecruiter")
with col2: 
	if st.button("Português"):
		st.session_state['language'] = 0
		del st.session_state['messages']
		st.rerun()

with col3:
	if st.button("English"):
		st.session_state['language'] = 1
		del st.session_state['messages']
		st.rerun()

tab_list = translate.tab_list[language]
tab_chat, tab_galeria, tab_video, tab_cv, tab_contato = st.tabs(tab_list)
# Mostrar a imagem atual

with tab_chat:
	
	chat_interface()


# Botões de navegação

with tab_galeria:
	col1, col2, col3, col4, col5 = st.columns([1, 1, 3, 1,1])
	with col1:
		txt_anterior = translate.txt_anterior[language]
		if st.button(txt_anterior):
			prev_image()

	with col5:
		txt_proximo = translate.txt_proximo[language]
		if st.button(txt_proximo):
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
		txt_em_breve = translate.txt_em_breve[language]
		st.markdown(f'<div class="centered-container"><p>{txt_em_breve}</p></div>', unsafe_allow_html=True)
with tab_cv:
	col1, col2, col3 = st.columns([1,4,1])
	with col2:
		txt_cv = translate.txt_cv[language]
		st.title(txt_cv)
		pdf_file_path = translate.pdf_file_path[language]
		pdf_data = ""
		with open(pdf_file_path, "rb") as f:
			pdf_data = f.read()
		txt_baixar_pdf = translate.txt_baixar_pdf[language]
		st.download_button(
			label=txt_baixar_pdf,
			data=pdf_data,
			file_name="curriculum_alex_benjamin.pdf",
			mime="application/pdf"
		)
		base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
		#pdf_display = f'<object data="data:application/pdf;base64,{base64_pdf}" type="application/pdf" width="700" height="1000"></object>'
		#pdf_display = f'<iframe src="{pdf_file_path}" type="application/pdf" width="700" height="1000"></iframe>'
		pdf_display =  f"""<embed
			class="pdfobject"
			type="application/pdf"
			title="Embedded PDF"
			src="data:application/pdf;base64,{base64_pdf}"
			style="overflow: auto; width: 700px; height: 1000px;">"""
		txt_vis = translate.txt_vis[language]
		st.write(txt_vis)
		#st.markdown(pdf_display, unsafe_allow_html=True)	
		pdf_html_name = translate.pdf_html_name
		with open(pdf_html_name, "r", encoding="utf-8") as f:
			html_content = f.read()
		components.html(html_content, height=700)
with tab_contato:
	col1,col2,col3,col4 = st.columns([3,1,1,3])
	with col2:
		st.image(image="./whatsapp.png")
		st.link_button(label="WhatsApp",url="https://wa.me/5511965590645?text=Ol%C3%A1,%20gostaria%20de%20saber%20um%20pouco%20mais%20sobre%20o%20seu%20perfil!")
	with col3:
		st.image(image="./linkedin.png")
		st.link_button(label="Linkedin",url="http://www.linkedin.com/in/alex-benjamin-43b1b438")


sidebar()
