import streamlit as st
import requests
from gtts import gTTS
from io import BytesIO


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Translation Studio",
    page_icon="🌐",
    layout="wide"
)


# ---------------- LANGUAGES ----------------

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Malayalam": "ml",
    "Kannada": "kn",
    "Tamil": "ta",
    "Telugu": "te",
    "Bengali": "bn",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Urdu": "ur",
    "Arabic": "ar",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Portuguese": "pt",
    "Italian": "it",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh-CN"
}


# ---------------- SESSION STATE ----------------

if "translation" not in st.session_state:
    st.session_state.translation = ""

if "history" not in st.session_state:
    st.session_state.history = []


# ---------------- TRANSLATION FUNCTION ----------------

def translate_text(text, source, target):

    url = "https://api.mymemory.translated.net/get"

    params = {
        "q": text,
        "langpair": f"{source}|{target}",
        "mt": "1"
    }

    response = requests.get(
        url,
        params=params,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    translated = data.get(
        "responseData",
        {}
    ).get(
        "translatedText",
        ""
    )

    if not translated:
        raise Exception("No translation returned.")

    return translated


# ---------------- HEADER ----------------

st.title("🌐 AI Translation Studio")

st.write(
    "Translate text between multiple languages using "
    "a REST-based machine translation service."
)

st.divider()


# ---------------- LANGUAGE SELECTION ----------------

col1, col2 = st.columns(2)


with col1:

    source_language = st.selectbox(
        "Source Language",
        ["Auto Detect"] + list(LANGUAGES.keys())
    )


with col2:

    target_language = st.selectbox(
        "Target Language",
        list(LANGUAGES.keys()),
        index=1
    )


# ---------------- TEXT INPUT ----------------

st.subheader("✍️ Enter Text")

text = st.text_area(
    "Text to translate",
    height=180,
    placeholder="Type or paste your text here..."
)


if text:

    st.caption(
        f"Words: {len(text.split())} | "
        f"Characters: {len(text)}"
    )


# ---------------- TRANSLATE BUTTON ----------------

if st.button(
    "🚀 Translate",
    type="primary",
    use_container_width=True
):

    if not text.strip():

        st.warning(
            "Please enter some text first."
        )

    elif source_language == target_language:

        st.warning(
            "Source and target languages "
            "cannot be the same."
        )

    else:

        try:

            target_code = LANGUAGES[target_language]


            # MyMemory does not provide reliable
            # automatic language detection here.
            # We use English as the fallback source.

            if source_language == "Auto Detect":

                source_code = "en"

            else:

                source_code = LANGUAGES[source_language]


            translated_text = translate_text(
                text,
                source_code,
                target_code
            )


            st.session_state.translation = (
                translated_text
            )


            # Save history

            st.session_state.history.insert(
                0,
                {
                    "source": source_language,
                    "target": target_language,
                    "original": text,
                    "translation": translated_text
                }
            )


            # Keep latest 10 translations

            st.session_state.history = (
                st.session_state.history[:10]
            )


        except requests.exceptions.RequestException:

            st.error(
                "Unable to connect to the translation "
                "service. Please check your internet connection."
            )


        except Exception as error:

            st.error(
                f"Translation failed: {error}"
            )


# ---------------- RESULT ----------------

if st.session_state.translation:

    st.divider()

    st.subheader("✅ Translation Result")

    st.success(
        st.session_state.translation
    )


    # Download

    st.download_button(
        "📥 Download Translation",
        data=st.session_state.translation,
        file_name="translation.txt",
        mime="text/plain",
        use_container_width=True
    )


    # ---------------- TEXT TO SPEECH ----------------

    st.subheader("🔊 Text-to-Speech")

    if st.button(
        "🎧 Generate Audio",
        use_container_width=True
    ):

        try:

            audio = BytesIO()

            speech = gTTS(
                text=st.session_state.translation,
                lang=LANGUAGES[target_language]
            )

            speech.write_to_fp(audio)

            audio.seek(0)

            st.audio(
                audio,
                format="audio/mp3"
            )

        except Exception:

            st.warning(
                "Text-to-speech is not available "
                "for this language."
            )


# ---------------- HISTORY ----------------

st.divider()

st.subheader("🕘 Translation History")


if st.session_state.history:

    for item in st.session_state.history:

        with st.expander(
            f"{item['source']} → {item['target']}"
        ):

            st.write("**Original:**")

            st.write(
                item["original"]
            )

            st.write("**Translation:**")

            st.write(
                item["translation"]
            )

else:

    st.info(
        "Your recent translations will appear here."
    )


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "AI Translation Studio • NLP • REST API • "
    "Machine Translation • Python • Streamlit"
)