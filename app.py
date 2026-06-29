import streamlit as st
from translator import translate_text

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Translator",
    page_icon="🌍",
    layout="wide"
)

# =====================================================
# SESSION STATE
# =====================================================

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

if "history" not in st.session_state:
    st.session_state.history = []

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

.stApp{
background:#0F172A;
}

/* Banner */

.banner{
background:linear-gradient(135deg,#2563EB,#7C3AED);
padding:30px;
border-radius:18px;
text-align:center;
margin-bottom:30px;
}

.banner h1{
color:white;
font-size:50px;
margin:0;
}

.banner p{
color:white;
font-size:18px;
margin-top:8px;
}

/* Headings */

h2,h3,h4,label,p{
color:white !important;
}

/* Text Area */

textarea{
background:#111827 !important;
color:white !important;
border-radius:12px !important;
font-size:18px !important;
}

/* Output Text */

.stTextArea textarea{
color:white !important;
opacity:1 !important;
-webkit-text-fill-color:white !important;
}

/* Select Box */

div[data-baseweb="select"]{
border-radius:12px;
}

/* Buttons */

.stButton>button{
width:100%;
height:52px;
background:linear-gradient(90deg,#2563EB,#1D4ED8);
color:white;
font-size:17px;
font-weight:bold;
border:none;
border-radius:12px;
}

.stButton>button:hover{
background:linear-gradient(90deg,#1D4ED8,#1E40AF);
}

/* Download */

.stDownloadButton>button{
width:100%;
height:52px;
background:#16A34A;
color:white;
font-size:17px;
font-weight:bold;
border:none;
border-radius:12px;
}

.stDownloadButton>button:hover{
background:#15803D;
}

[data-testid="stMetricValue"]{
color:white;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="banner">

<h1>🌍 AI Translator</h1>

<p>
Translate text instantly across multiple languages
</p>

</div>
""", unsafe_allow_html=True)
# =====================================================
# LANGUAGES
# =====================================================

languages = {
    "English": "en",
    "Hindi": "hi",
    "Kannada": "kn",
    "Tamil": "ta",
    "Telugu": "te",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Bengali": "bn",
    "Urdu": "ur",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh-CN",
    "Arabic": "ar",
    "Russian": "ru"
}

# =====================================================
# TWO COLUMNS
# =====================================================

left, right = st.columns([1.2, 1], gap="large")

# =====================================================
# INPUT PANEL
# =====================================================

with left:

    st.markdown("## 📝 Input")

    source_language = st.selectbox(
        "Source Language",
        list(languages.keys()),
        index=0
    )

    target_language = st.selectbox(
        "Target Language",
        list(languages.keys()),
        index=2
    )

    text = st.text_area(
        "Enter Text",
        height=260,
        placeholder="Type or paste your text here..."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Characters", len(text))

    with col2:
        st.metric("Words", len(text.split()))

    translate = st.button(
        "🚀 Translate",
        use_container_width=True
    )
    # =====================================================
# TRANSLATION
# =====================================================

if translate:

    if text.strip() == "":

        st.warning("Please enter some text.")

    elif source_language == target_language:

        st.warning("Source and Target languages cannot be the same.")

    else:

        with st.spinner("Translating..."):

            translated = translate_text(
                text=text,
                source_lang=languages[source_language],
                target_lang=languages[target_language]
            )

        # Save latest translation
        st.session_state.translated_text = translated

        # Save history
        st.session_state.history.insert(
            0,
            {
                "source": source_language,
                "target": target_language,
                "input": text,
                "output": translated
            }
        )

        # Keep only last 10 translations
        st.session_state.history = st.session_state.history[:10]
        # =====================================================
# OUTPUT PANEL
# =====================================================

with right:

    st.markdown("## 🌐 Translation Result")

    if st.session_state.translated_text:

        st.success("✅ Translation Completed Successfully")

        st.text_area(
            label="Translated Text",
            value=st.session_state.translated_text,
            height=260,
            disabled=True
        )

        st.download_button(
            label="📥 Download Translation",
            data=st.session_state.translated_text,
            file_name="translated_text.txt",
            mime="text/plain",
            use_container_width=True
        )

    else:

        st.info("Translate some text to see the result here.")
        # =====================================================
# TRANSLATION HISTORY
# =====================================================

st.divider()

col1, col2 = st.columns([5, 1])

with col1:
    st.subheader("🕘 Translation History")

with col2:
    if st.button("🗑 Clear History"):
        st.session_state.history.clear()
        st.session_state.translated_text = ""
        st.rerun()

if len(st.session_state.history) == 0:

    st.info("No translations yet.")

else:

    for item in st.session_state.history:

        with st.expander(
            f"{item['source']} ➜ {item['target']}"
        ):

            st.markdown("**📝 Original Text**")
            st.write(item["input"])

            st.markdown("**🌍 Translated Text**")
            st.code(item["output"], language=None)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown("""
<div style="text-align:center;padding:20px;color:#94A3B8;">

<h3 style="color:white;margin-bottom:8px;">
🌍 AI Translator
</h3>

<p style="font-size:16px;">
Translate text instantly across multiple languages.
</p>

<p style="font-size:15px;">
Built with ❤️ using <b>Python</b>, <b>Streamlit</b> and <b>Deep Translator</b>
</p>

<hr style="border:1px solid #334155;width:70%;margin:auto;margin-top:15px;margin-bottom:15px;">

<p style="font-size:14px;">
</p>

</div>
""", unsafe_allow_html=True)