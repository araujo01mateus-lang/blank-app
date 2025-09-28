import streamlit as st
import os
import json
import pandas as pd

# --- Configurações ---
ADMIN_USER = "flex"
ADMIN_PASS = "290924"
WHATSAPP_ADMIN = "558899111888"
CADASTRO_FILE = "os_meno_quentao.json"

# --- Inicializa estados ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_type" not in st.session_state:
    st.session_state.user_type = None
if "username" not in st.session_state:
    st.session_state.username = None

# Inicializa contadores de download
for key in ["pc_count", "pc_medio_count", "mobile_count"]:
    if key not in st.session_state:
        st.session_state[key] = 0

# --- Inicializa cadastro JSON ---
if not os.path.exists(CADASTRO_FILE):
    with open(CADASTRO_FILE, "w") as f:
        json.dump([], f)

# --- Funções ---
def load_cadastros():
    with open(CADASTRO_FILE, "r") as f:
        return json.load(f)

def save_cadastros(cadastros):
    with open(CADASTRO_FILE, "w") as f:
        json.dump(cadastros, f, indent=2)

def adicionar_cadastro(nome, nick, server, whatsapp):
    cadastros = load_cadastros()
    cadastros.append({
        "nome": nome,
        "nick": nick,
        "server": server,
        "whatsapp": whatsapp,
        "aprovado": False
    })
    save_cadastros(cadastros)
    msg = f"Novo cadastro: {nome}, {nick}, {server}, {whatsapp}"
    st.markdown(f"[💌 Notificar no WhatsApp](https://wa.me/{WHATSAPP_ADMIN}?text={msg.replace(' ', '%20')})")

def aprovar_cadastro(index):
    cadastros = load_cadastros()
    cadastros[index]["aprovado"] = True
    save_cadastros(cadastros)

# --- Estilos CSS ---
st.markdown("""
<style>
.download-btn {
    padding: 15px 25px;
    font-size: 18px;
    font-weight: bold;
    border: none;
    border-radius: 12px;
    margin: 5px;
    cursor: pointer;
    transition: all 0.3s ease;
}
.download-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
.btn-pc { background-color: #ff2b2b; color: white; }
.btn-pc-medio { background-color: #ff7f50; color: white; }
.btn-mobile { background-color: #1e90ff; color: white; }
</style>
""", unsafe_allow_html=True)

# --- Tela inicial ---
st.title("🌐 Plataforma de Cadastro / Login com Aprovação")

if not st.session_state.logged_in:
    option = st.radio("Entrar como:", ["Admin", "Player"])
    if option == "Admin":
        st.subheader("🔒 Login Admin")
        user = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        if st.button("Entrar como Admin"):
            if user == ADMIN_USER and password == ADMIN_PASS:
                st.session_state.logged_in = True
                st.session_state.user_type = "admin"
                st.success("✅ Login Admin bem-sucedido!")
            else:
                st.error("❌ Usuário ou senha incorretos")
    else:
        st.subheader("📝 Cadastro de Player")
        nick = st.text_input("Nick do jogo")
        server = st.radio("Escolha seu servidor:", ["sv1","sv2","sv3","sv4"])
        whatsapp = st.text_input("Seu WhatsApp")
        aceito = st.checkbox("✅ Concordo com os termos")
        if st.button("Cadastrar"):
            if not aceito:
                st.warning("Você precisa concordar com os termos!")
            elif not nome or not nick or not whatsapp:
                st.warning("Preencha todos os campos!")
            else:
                adicionar_cadastro(nome, nick, server, whatsapp)
                st.success("✅ Cadastro enviado! Aguarde aprovação do admin.")
                st.session_state.username = nick

else:
    st.success(f"✅ Logado como {st.session_state.user_type.upper()}")
    cadastros = load_cadastros()

    # --- Admin vê cadastros pendentes ---
    if st.session_state.user_type == "admin":
        st.subheader("📝 Cadastros Pendentes")
        for i, c in enumerate(cadastros):
            if not c["aprovado"]:
                st.write(f"Nome: {c['nome']}, Nick: {c['nick']}, Server: {c['server']}, WhatsApp: {c['whatsapp']}")
                if st.button(f"Aprovar {c['nick']}", key=f"aprovar_{i}"):
                    aprovar_cadastro(i)
                    st.success(f"✅ {c['nick']} aprovado!")

    # --- Verificar se player está aprovado ---
    if st.session_state.user_type == "player":
        aprovado = any(c["nick"] == st.session_state.username and c["aprovado"] for c in cadastros)
        if not aprovado:
            st.info("⏳ Aguarde aprovação do admin para ver os downloads.")
        else:
            st.success("✅ Você foi aprovado! Downloads disponíveis:")

    # --- Botões de download ---
    downloads_visiveis = st.session_state.user_type == "admin" or \
                         (st.session_state.user_type == "player" and \
                          any(c["nick"] == st.session_state.username and c["aprovado"] for c in cadastros))

    if downloads_visiveis:
        links = [
            ("📥 A DATA DUS MENÓ", "https://download2261.mediafire.com/sg4j65iwme0goucTZvtYK1LYxKFH6SPzIicSmetCaciXE0NxTpULMWey4p-_FNCSERRt5TMkpKMmB7FTK8OF3ZOyBnu1jee47WVNUei99ET0R7NuRiZhRFXnOKidkCqHMLTlHYns-T3Fw7sjkPsdNTG474pRZ9r75Yol1Odaw-boluk/izwrx53brqyvq0r/Ant+Lag+By+Ninja+V5.rar", "btn-pc", "pc_count"),
            ("📥 A DATA DUS MENÓ (PC MÉDIO)", "https://download850.mediafire.com/9lj8n0qmsr0gUcxt6WBFsT1wpL6QSHdRtKzUSO4OvKP5Dymm5UQ8Xg1DazdgWmfRsEED6GhcS5AfGo1xu0CF9ztc-EokGzy12C7Z0druTCKTPcuwhS7dQlj2IfOLUmKPrBi20hNiIvSaT3ODMqWYsnmvjnvRfOj_J-WaqkKbwzyH4Q/1ma1yg9fwl7q1fe/By+Lobo+Rlk+%28+privada+%29.rar", "btn-pc-medio", "pc_medio_count"),
            ("📱 A DATA DUS MENÓ (MOBILE)", "https://www.mediafire.com/file/gf068rxq9te7fi7/ro.alyn_sampmobile.game.7z/file", "btn-mobile", "mobile_count")
        ]
        for text, link, cls, counter in links:
            col1, col2 = st.columns([4,1])
            with col1:
                st.markdown(f'<a href="{link}" target="_blank"><button class="download-btn {cls}">{text}</button></a>', unsafe_allow_html=True)
            with col2:
                st.write(f"📊 {st.session_state[counter]}")

    # --- Tabela completa de players para admin ---
    if st.session_state.user_type == "admin":
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("📋 Lista de Players")
        if cadastros:
            df = pd.DataFrame(cadastros)
            df["aprovado"] = df["aprovado"].apply(lambda x: "Sim" if x else "Não")
            servidor_filtro = st.selectbox("Filtrar por servidor", ["Todos","sv1","sv2","sv3","sv4"])
            if servidor_filtro != "Todos":
                df = df[df["server"] == servidor_filtro]
            st.dataframe(df, use_container_width=True)
        else:
            st.write("Nenhum player cadastrado ainda.")
