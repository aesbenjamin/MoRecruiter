system = [
	"""
					Você é o clone do Alex Benjamin, um Líder em modernização de ambientes de TI legados e especialista em Inteligência Artificial. Vai receber perguntas de recrutadores sobre 
					capacitações ou curiosidades suas. Não responda sem conhecimento prévio pelo contexto, apenas trabalhe com o 
					contexto e pergunta passadas.
	""",
	"""
	You are the clone of Alex Benjamin, a leader in modernizing legacy IT environments and an expert in Artificial Intelligence. You will receive questions from recruiters about your skills or curiosities. Do not respond without prior knowledge of the context; only work with the context and questions provided.
	"""
]

ini = ['Recrutador: ', 'Recruiter: ']

txt=["Histórico de conversa com o clone do Alex Benjamin", "Conversation history with the clone of Alex Benjamin"]
sub_txt = ["Clone do Alex Benjamin", "Alex Benjamin's Clone"]
input_txt = ["Pergunte algo sobre mim:", "Ask me something about myself:"]
txt_pdf = ["Gerar PDF","Generate PDF"]
txt_baixar_pdf = ["Baixar PDF", "Download PDF"]
init_msg = ["""
				Olá, eu sou o clone do Alex Benjamin. Fique à vontade para fazer perguntas 
				profissionais, ou até mesmo pessoais, como curiosidades, ou hobbies :D\n
				Se você preferir, pode utilizar a análise de conformidade, do lado direito desse chat,
				uma maneira simples e fácil de analisar se eu sou o candidato ideal para a sua vaga.								

				""",
				"""
			Hello, I am the clone of Alex Benjamin. Feel free to ask professional or even personal questions, 
			such as curiosities or hobbies\n

			If you prefer, you can use the compliance analysis on the right side of this chat, a simple and easy way to assess if I am the ideal candidate for your position.
			"""]
txt_multi = [
	"Escolha palavras-chave para analisar o índice de alinhamento das capacitações do Alex com a vaga proposta:",
	"Choose keywords to analyze the alignment index of Alex's skills with the proposed position."]
txt_descr = ["Ou se preferir, cole aqui a descrição da vaga:", "Or if you prefer, paste the job description here:"]			


def get_analise(title:str, options:str):
		
	analise = [f"""
						Analise se o Alex tem as capacitações abaixo:
						\n
						Descrição da vaga e palavras-chave:
						{title}
						\n
						{options}
						\n
						Ao final, gere um relatório e um índice de conformidade, que representa um percentual
						de capacitação do Alex em relação as palavras-chave e a descrição da vaga.
						""",
						f"""
						Analyze if Alex has the skills listed below:
						\n
						Job description and keywords: 
						\n 
						{title}
						\n  
						{options}
						\n
						At the end, generate a report and a compliance index, which represents a percentage of Alex's skills in relation to the keywords and the job description.
						"""
						]
	return analise
txt_vis=['Visualização do PDF:',"PDF Preview:"]
sidebar_txt1 = ["""
			Alex Benjamin
			\n
			Líder em Modernização de Sistemas Legados, especialista em 
			Inteligência Artificial Generativa e Engenheiro de Software há mais de 18 anos.
			\n
			Utilize o chat ao lado para conhecer um pouco de mim e minhas qualificações.	
			""",
			"""
			Alex Benjamin
			\n
			Leader in Legacy Systems Modernization, specialist in Generative Artificial Intelligence and Software Engineer for over 18 years.
			\n
			Use the chat next to learn a bit about me and my qualifications.	
			"""]

sidebar_txt2 = ["Este site foi construído com Python e Streamlit, e seu backend com o motor MoMapping.\nAcesse o site e saiba mais:",
	"This site was built with Python and Streamlit, and its backend with the MoMapping engine.\nVisit the site to learn more:"
]
tab_list = [["Chat", "Galeria", "Video", "Currículo", "Contato"],["Chat", "Gallery", "Video",  "Resume", "Contact"]]

txt_anterior = ["◀️ Anterior", "◀️ Previous"]
txt_proximo = ["Próximo ▶️", "Next ▶️"]
txt_analisar = ["Analisar","Analyze"]
txt_conformidade = ["Análise de Conformidade", "Compliance Analysis"]
txt_em_breve =["Em breve", "Coming soon"]
txt_cv = ["Curriculum Alex Benjamin", "Alex Benjamin's Resume"]
pdf_file_path = ["./curriculum_alex_benjamin.pdf", "./curriculum_alex_benjamin_v17_english.pdf"]
pdf_html_name = ["curriculum_alex_benjamin.html", "curriculum_alex_benjamin_v17_english.html"]