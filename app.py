import streamlit as st
import os 


import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_sm')

HTML_WRAPPER = """<div style="overflow-x:auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem;>{}</div>"""


def sanitize_names(text):
    docx = nlp(text)
    redacted_sentence = []
    with docx.retokenize() as retokenizer:
        for ent in docx.ents:
           retokenizer.merge(ent)
           print(ent.label_,ent, sep="\t")
        for token in docx:
            if token.ent_type_ == "PERSON":
                redacted_sentence.append("[NOME]")
            else:
                redacted_sentence.append(token.text)
    return " ".join(redacted_sentence)

def sanitize_places(text):
    docx = nlp(text)
    redacted_sentence = []
    with docx.retokenize() as retokenizer:
        for ent in docx.ents:
            retokenizer.merge(ent)
        for token in docx:
            if token.ent_type_ == 'GPE':
                redacted_sentence.append("[LUGAR]")
            else:
                redacted_sentence.append(token.text)
    return " ".join(redacted_sentence)

def sanitize_org(text):
    docx = nlp(text)
    redacted_sentence = []
    with docx.retokenize() as retokenizer:
        for ent in docx.ents:
            retokenizer.merge(ent)
        for token in docx:
            if token.ent_type_ == 'ORG':
                redacted_sentence.append("[LINK]")
            else:
                redacted_sentence.append(token.text)
    return " ".join(redacted_sentence)

def sanitize_dates(text):
    docx = nlp(text)
    redacted_sentence = []
    with docx.retokenize() as retokenizer:
        for ent in docx.ents:
            retokenizer.merge(ent)
        for token in docx:
            if token.ent_type_ == 'DATE':
                redacted_sentence.append("[DATA]")
            else:
                redacted_sentence.append(token.text)
    return " ".join(redacted_sentence)


@st.cache_data 
def render_entities(rawtext):
    docx = nlp(rawtext)
    html = displacy.render(docx, style='ent')
    html = html.replace("\n\n","\n")
    result = HTML_WRAPPER.format(html)
    return result

def get_entities(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))
    return entities


def explain_entity(entity, label):
    explanations = {
        "PERSON": "Esta entidade foi identificada como uma pessoa porque é um nome próprio geralmente associado a indivíduos.",
        "GPE": "Esta entidade foi identificada como um lugar porque é um nome próprio geralmente associado a locais geográficos.",
        "ORG": "Esta entidade foi identificada como uma organização porque é um nome próprio geralmente associado a grupos ou empresas.",
        "DATE": "Esta entidade foi identificada como uma data porque segue um padrão de datas comuns."
    }
    return explanations.get(label, "Entidade desconhecida.")

 


def main():

    st.title("Document Redactor App")
    st.text("Built with Streamlit and SpaCy") 


    st.subheader("Redaction of Terms")
    rawtext = st.text_area("Enter Text", "Type Here")
  
 
    if st.button("Submit"):
        entities = get_entities(rawtext)
        explanations = [(entity, label, explain_entity(entity, label)) for entity, label in entities]
        st.subheader("Original Text")
        st.write(render_entities(rawtext), unsafe_allow_html=True)
        st.divider()
        st.subheader("Explanation")
        st.write(explanations)
            
    

if __name__ == '__main__':
    main()