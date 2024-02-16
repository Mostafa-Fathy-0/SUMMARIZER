import streamlit as st
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Function to handle whitespace and newline characters
def clean_text(text):
    return re.sub(r'\s+', ' ', re.sub(r'\n+', ' ', text.strip()))

# Main function to generate the summary
def generate_summary(article_text, model_name, max_summary_length=84, num_beams=4):
    # Clean the input text
    cleaned_text = clean_text(article_text)

    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # Tokenize the cleaned text
    input_ids = tokenizer(
        [cleaned_text],
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=512
    )["input_ids"]

    # Generate the summary
    output_ids = model.generate(
        input_ids=input_ids,
        max_length=max_summary_length,
        no_repeat_ngram_size=2,
        num_beams=num_beams
    )[0]

    # Decode the summary tokens into text
    summary = tokenizer.decode(
        output_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False
    )

    return summary

def main():
    st.title('Text Summarizer')
    st.write('Enter the article text below:')
    article_text = st.text_area('Input Article Text', height=300)
    if st.button('Generate Summary'):
        model_name = "csebuetnlp/mT5_multilingual_XLSum"
        summary = generate_summary(article_text, model_name)
        st.subheader('Summary:')
        st.write(summary)

if __name__ == "__main__":
    main()
