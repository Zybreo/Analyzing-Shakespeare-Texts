import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import glob,nltk,os,re
from nltk.corpus import stopwords
import nltk
import string
nltk.download('stopwords')
nltk.download('punkt')


st.markdown('''
# Analyzing Shakespeare Texts
''')

books = {"": "", "A Mid Summer Night's Dream": "summer.txt", "The Merchant of Venice": "merchant.txt", "Romeo and Juliet": "romeo.txt"}

st.sidebar.header("Word Cloud Settings")
max_word = st.sidebar.slider("Max Words", min_value=10, max_value=200, value=100)
max_font_size = st.sidebar.slider("Size of largest Word", min_value=50, max_value=350, value=200)
image_width = st.sidebar.slider("Image Width", min_value=100, max_value=800, value=400)
random_state = st.sidebar.slider("Random States", min_value=20, max_value=100, value=42)
remove_stop_words = st.sidebar.checkbox("Remove Stop Words?", value=True)

st.sidebar.header("Word Count Settings")
min_word_count = st.sidebar.slider("Minimum count of words", min_value=5, max_value=100, value=20)


image = st.selectbox('Choose a text file', list(books.keys()))
image = books.get(image)

if image != "":
    stop_words = []
    raw_text = open(image, "r").read().lower()
    nltk_stop_words = stopwords.words('english')

    if remove_stop_words:
        stop_words = set(nltk_stop_words)
        stop_words.update(['us', 'one', 'thouth', 'will', 'said', 'now', 'well', 'man', 'may',
                           'little', 'say', 'must', 'way', 'long', 'yet', 'mean',
                           'put', 'seem', 'asked', 'made', 'half', 'much',
                           'certainly', 'might', 'came', 'thou'])

    tokens = nltk.word_tokenize(raw_text)
else:
    raw_text = ""

tab1, tab2, tab3 = st.tabs(['Word Cloud', 'Bar chart', 'View text'])

with tab1:
    if image != "":
        wc = WordCloud(stopwords=stop_words, max_words=max_word, background_color="white", max_font_size=max_font_size, width=image_width, random_state=random_state).generate(raw_text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(plt.gcf())
    else:
        st.warning("Please choose a text file.")

with tab2:
    if image != "":
        # Remove punctuation
        tokens_no_punct = [word for word in tokens if word not in string.punctuation]
        
        # Remove stop words and non-alphanumeric words
        filtered_words = [word for word in tokens_no_punct if word not in stop_words and word.isalnum()]
        
        # Calculate word frequency
        word_freq = nltk.FreqDist(filtered_words)
        df = pd.DataFrame(word_freq.most_common(), columns=["Word", "Frequency"])

        # Filter words based on the minimum count
        df_filtered = df[df["Frequency"] >= min_word_count]

        if not df_filtered.empty:
            # Create bar chart
            fig, ax = plt.subplots()
            ax.barh(df_filtered["Word"], df_filtered["Frequency"])
            ax.invert_yaxis()
            ax.set_xlabel("Frequency")
            ax.set_title("Word Frequency Bar Chart")
            st.pyplot(fig)
        else:
            st.warning("No words match the minimum count criteria.")
    else:
        st.warning("Please choose a text file.")

with tab3:
    if image != "":
        st.write("All Text")
        st.write(raw_text)
    else:
        st.warning("Please choose a text file.")