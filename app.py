import streamlit as st
import re
from collections import Counter

# --- CONFIGURAÇÃO DA INTERFACE STREAMLIT ---
# (Esta linha DEVE vir antes de qualquer outro comando do Streamlit, incluindo @st.cache_resource)
st.set_page_config(page_title="NLP Lab - Aula 8", page_icon="🧠", layout="wide")

# Importando as bibliotecas obrigatórias de PLN
import nltk
import spacy

# Configuração e download seguro de recursos do NLTK
@st.cache_resource
def iniciar_recursos_nltk():
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    try:
        # Apenas um fallback pro safety run no Render
        nltk.download('punkt_tab', quiet=True)
    except: pass
    from nltk.corpus import stopwords
    return set(stopwords.words('portuguese'))

try:
    STOPWORDS_NLTK = iniciar_recursos_nltk()
except Exception as e:
    STOPWORDS_NLTK = {"de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "é", "com", "não", "uma"}

# Carregamento seguro do modelo spaCy em Português
@st.cache_resource
def iniciar_spacy():
    try:
        return spacy.load("pt_core_news_sm")
    except OSError:
        from spacy.cli import download
        download("pt_core_news_sm")
        return spacy.load("pt_core_news_sm")

try:
    nlp = iniciar_spacy()
except Exception as e:
    nlp = spacy.blank("pt")

# Estilização
st.markdown("""
    <style>
    .main-title { font-size: 38px; font-weight: bold; color: #1E3A8A; margin-bottom: 10px; }
    .subtitle { font-size: 18px; color: #4B5563; margin-bottom: 30px; }
    .problematic-box { background-color: #FEF3C7; padding: 15px; border-left: 5px solid #D97706; border-radius: 4px; margin-bottom: 10px; }
    .task-box { background-color: #E0F2FE; padding: 15px; border-left: 5px solid #0284C7; border-radius: 4px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🧠 Laboratório Avançado de PLN — Solução Integrada (Aula 8)</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Aplicação fullstack interativa desenvolvida com Streamlit, NLTK e spaCy.</div>', unsafe_allow_html=True)

tabs = st.tabs([f"Exercício {i}" for i in range(1, 11)])

# ATIVIDADE 1
with tabs[0]:
    st.subheader("Atividade 1: Análise de Sentimentos por Palavras-Chave")
    st.markdown('<div class="problematic-box"><b>⚠️ Problemática:</b> Uma empresa de marketing precisa identificar rapidamente se comentários de clientes são positivos ou negativos.</div>', unsafe_allow_html=True)
    st.markdown('<div class="task-box"><b>🎯 Tarefa:</b> Crie um sistema simples de análise de sentimentos baseado em palavras-chave.</div>', unsafe_allow_html=True)

    txt_1 = st.text_area("Comentário do cliente:", "Amei o produto! Foi sensacional.", key="act1")
    if st.button("Analisar Sentimento", key="btn1"):
        if not txt_1.strip():
            st.warning("⚠️ Por favor, insira o comentário do cliente no campo acima antes de analisar.")
        else:
            tokens = nltk.word_tokenize(txt_1.lower())
            pos_words = {"amei", "bom", "excelente", "ótimo", "sensacional"}
            neg_words = {"ruim", "péssimo", "atrasou", "odiei"}
            
            c_pos = sum(1 for w in tokens if w in pos_words)
            c_neg = sum(1 for w in tokens if w in neg_words)
            score = c_pos - c_neg
            
            if score > 0: 
                st.success("🟢 Sentimento: POSITIVO")
            elif score < 0: 
                st.error("🔴 Sentimento: NEGATIVO")
            else: 
                if c_pos == 0 e c_neg == 0:
                    st.info("⚪ Sentimento: NEUTRO (Nenhuma palavra-chave de sentimento mapeada foi encontrada no texto).")
                else:
                    st.warning("🟡 Sentimento: NEUTRO (Empate entre palavras positivas e negativas).")

# ATIVIDADE 2
with tabs[1]:
    st.subheader("Atividade 2: Tokenização Avançada")
    st.markdown('<div class="problematic-box"><b>⚠️ Problemática:</b> Um e-commerce recebe milhares de avaliações e precisa separar palavras importantes para análise.</div>', unsafe_allow_html=True)
    st.markdown('<div class="task-box"><b>🎯 Tarefa:</b> Use tokenização para quebrar avaliações em palavras.</div>', unsafe_allow_html=True)

    txt_2 = st.text_area("Avaliação:", "O celular chegou perfeito, mas a tela está arranhada.", key="act2")
    if st.button("Executar Tokenização", key="btn2"):
        if not txt_2.strip():
            st.warning("⚠️ O campo de texto está vazio. Digite uma avaliação para tokenizar.")
        else:
            tokens_list = nltk.word_tokenize(txt_2)
            st.json(tokens_list)

# ATIVIDADE 3
with tabs[2]:
    st.subheader("Atividade 3: Classificador Temático (Banco Digital)")
    st.markdown('<div class="problematic-box"><b>⚠️ Problemática:</b> Um banco digital precisa identificar solicitações como “bloquear cartão” ou “segunda via de boleto”.</div>', unsafe_allow_html=True)
    st.markdown('<div class="task-box"><b>🎯 Tarefa:</b> Crie um classificador simples baseado em palavras-chave.</div>', unsafe_allow_html=True)

    txt_3 = st.text_input("Mensagem:", "Preciso da segunda via do meu boleto.", key="act3")
    if st.button("Classificar Atendimento", key="btn3"):
        if not txt_3.strip():
            st.warning("⚠️ Insira a mensagem do cliente para realizar o roteamento.")
        else:
            cartao_kw = ["bloquear", "cartão", "perdi"]
            boleto_kw = ["segunda via", "boleto", "fatura"]
            
            if any(kw in txt_3.lower() for kw in cartao_kw): 
                st.success("💳 Setor: Cartões")
            elif any(kw in txt_3.lower() for kw in boleto_kw): 
                st.info("🧾 Setor: Boletos e Faturamento")
            else: 
                st.warning("❓ Setor: Atendimento Geral (Não identificamos palavras-chave de setores específicos).")

# ATIVIDADE 4
with tabs[3]:
    st.subheader("Atividade 4: Remoção de Stopwords (NLTK)")
    st.markdown('<div class="problematic-box"><b>⚠️ Problemática:</b> Uma empresa quer remover palavras irrelevantes de textos para melhorar análise de dados.</div>', unsafe_allow_html=True)
    st.markdown('<div class="task-box"><b>🎯 Tarefa:</b> Remova stopwords de um texto usando NLTK.</div>', unsafe_allow_html=True)

    txt_4 = st.text_area("Texto:", "O gerente da loja falou para o cliente que o prazo era de vinte dias.", key="act4")
    if st.button("Remover Stopwords", key="btn4"):
        if not txt_4.strip():
            st.warning("⚠️ Insira o texto bruto para remover as stopwords.")
        else:
            tokens = nltk.word_tokenize(txt_4)
            filtrados = [w for w in tokens if w.lower() not in STOPWORDS_NLTK]
            if len(tokens) == len(filtrados):
                st.info("ℹ️ Nenhuma stopword foi encontrada ou removida do texto original.")
            st.code(" ".join(filtrados), language="text")

# ATIVIDADE 5
with tabs[4]:
    st.subheader("Atividade 5: Detector de Reclamações")
    st.markdown('<div class="problematic-box"><b>⚠️ Problemática:</b> Uma equipe de suporte quer identificar reclamações automaticamente em mensagens de clientes.</div>', unsafe_allow_html=True)
    st.markdown('<div class="task-box"><b>🎯 Tarefa:</b> Detecte palavras negativas como “ruim”, “erro”, “péssimo”.</div>', unsafe_allow_html=True)

    txt_5 = st.text_area("Mensagem:", "O sistema deu um erro muito ruim hoje.", key="act5")
    if st.button("Escanear Mensagem", key="btn5"):
        if not txt_5.strip():
            st.warning("⚠️ Digite uma mensagem do suporte para escanear.")
        else:
            doc = nlp(txt_5.lower())
            negativas = {"ruim", "erro", "péssimo", "horrível"}
            encontrados = [t.text for t in doc if t.text in negativas]
            if encontrados:
                st.error(f"⚠️ Reclamação detectada! Termos críticos: {list(set(encontrados))}")
            else:
                st.success("✅ Mensagem analisada e classificada como normal (Nenhum termo de reclamação mapeado foi identificado).")

# ATIVIDADE 6
with tabs[5]:
    st.subheader("Atividade 6: Simulação de NER (spaCy)")
    st.markdown('<div class="problematic-box"><b>⚠️ Problemática:</b> Um sistema precisa identificar nomes de pessoas e empresas em documentos automaticamente.</div>', unsafe_allow_html=True)
    st.markdown('<div class="task-box"><b>🎯 Tarefa:</b> Simule extração de entidades (NER) usando spaCy.</div>', unsafe_allow_html=True)

    txt_6 = st.text_area("Texto corporativo:", "Carlos Silva assinou o contrato com a Google Brasil em São Paulo.", key="act6")
    if st.button("Extrair Entidades", key="btn6"):
        if not txt_6.strip():
            st.warning("⚠️ O campo está vazio. Forneça um texto para que a IA possa extrair entidades.")
        else:
            doc = nlp(txt_6)
            if doc.ents:
                st.table([{"Entidade": ent.text, "Tipo": ent.label_} for ent in doc.ents])
            else:
                st.info("🔍 Análise concluída: Nenhuma entidade (Pessoa, Organização ou Local) foi reconhecida no texto pelo modelo.")

# ATIVIDADE 7
with tabs[6]:
    st.subheader("Atividade 7: Frequência de Palavras")
    st.markdown('<div class="problematic-box"><b>⚠️ Problemática:</b> Uma rede social quer entender quais palavras aparecem mais em comentários de uma postagem viral.</div>', unsafe_allow_html=True)
    st.markdown('<div class="task-box"><b>🎯 Tarefa:</b> Calcule frequência de palavras em um texto.</div>', unsafe_allow_html=True)

    txt_7 = st.text_area("Postagem viral:", "Muito bom o vídeo! O vídeo é incrível, muito bom mesmo.", key="act7")
    if st.button("Calcular Frequência", key="btn7"):
        if not txt_7.strip():
            st.warning("⚠️ Por favor, insira o conteúdo da postagem viral.")
        else:
            tokens = nltk.word_tokenize(re.sub(r'[^\w\s]', '', txt_7.lower()))
            uteis = [w for w in tokens if w not in STOPWORDS_NLTK]
            ranking = Counter(uteis).most_common()
            
            if ranking:
                st.table([{"Palavra": p, "Frequência": c} for p, c in ranking])
            else:
                st.info("ℹ️ Não sobraram palavras úteis para contar após a limpeza de stopwords e pontuação.")

# ATIVIDADE 8
with tabs[7]:
    st.subheader("Atividade 8: Intent Parser para Chatbot")
    st.markdown('<div class="problematic-box"><b>⚠️ Problemática:</b> Um chatbot precisa identificar intenção do usuário em mensagens.</div>', unsafe_allow_html=True)
    st.markdown('<div class="task-box"><b>🎯 Tarefa:</b> Crie regras para identificar intenções como “cancelar”, “comprar”, “suporte”.</div>', unsafe_allow_html=True)

    txt_8 = st.text_input("Mensagem para o Chatbot:", "Eu quero cancelar o meu plano.", key="act8")
    if st.button("Processar Intenção", key="btn8"):
        if not txt_8.strip():
            st.warning("⚠️ Digite a mensagem que o usuário enviou ao chatbot.")
        else:
            t = txt_8.lower()
            if any(w in t for w in ["cancelar", "cancelamento"]): 
                st.error("❌ Intenção: CANCELAR")
            elif any(w in t for w in ["comprar", "preço", "adquirir"]): 
                st.success("🛒 Intenção: COMPRAR")
            elif any(w in t for w in ["suporte", "erro", "ajuda", "problema"]): 
                st.warning("🛠️ Intenção: SUPORTE")
            else: 
                st.info("❓ Intenção Desconhecida: A IA não conseguiu mapear o objetivo da frase baseado nas regras atuais.")

# ATIVIDADE 9
with tabs[8]:
    st.subheader("Atividade 9: Normalização de Textos")
    st.markdown('<div class="problematic-box"><b>⚠️ Problemática:</b> Uma empresa quer limpar textos retirando pontuação e padronizando letras.</div>', unsafe_allow_html=True)
    st.markdown('<div class="task-box"><b>🎯 Tarefa:</b> Normalize textos (minúsculas e sem pontuação).</div>', unsafe_allow_html=True)

    txt_9 = st.text_area("Texto bruto:", "Atenção!!! Você viu isso??? Sim, claro.", key="act9")
    if st.button("Higienizar", key="btn9"):
        if not txt_9.strip():
            st.warning("⚠️ Insira um texto bruto para realizar a normalização.")
        else:
            resultado = re.sub(r'[^\w\s]', '', txt_9.lower())
            st.code(resultado)

# ATIVIDADE 10
with tabs[9]:
    st.subheader("Atividade 10: Classificação Simples (Positivo, Negativo, Neutro)")
    st.markdown('<div class="problematic-box"><b>⚠️ Problemática:</b> Uma empresa quer analisar feedbacks e classificar automaticamente mensagens em três categorias: positivo, negativo ou neutro.</div>', unsafe_allow_html=True)
    st.markdown('<div class="task-box"><b>🎯 Tarefa:</b> Combine tokenização + regras condicionais para classificação simples.</div>', unsafe_allow_html=True)

    txt_10 = st.text_area("Feedback:", "A loja física foi ok, o atendimento foi regular.", key="act10")
    if st.button("Classificar Feedback", key="btn10"):
        if not txt_10.strip():
            st.warning("⚠️ O campo de feedback está vazio.")
        else:
            tokens = nltk.word_tokenize(txt_10.lower())
            pos = {"excelente", "ótimo", "bom", "gostei"}
            neg = {"ruim", "péssimo", "horrível", "lento"}
            
            c_pos = sum(1 for t in tokens if t in pos)
            c_neg = sum(1 for t in tokens if t in neg)
            
            if c_pos > c_neg: 
                st.success("🟢 Feedback: POSITIVO")
            elif c_neg > c_pos: 
                st.error("🔴 Feedback: NEGATIVO")
            else: 
                st.warning("🟡 Feedback: NEUTRO (Informação: O sistema não detectou uma prevalência clara de palavras emocionais cadastradas no dicionário).")
