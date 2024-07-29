import streamlit as st
import spacy
from spacy import displacy
import re
from spacy.tokenizer import Tokenizer

nlp = spacy.load('en_core_web_sm')

def custom_tokenizer(nlp):
    infix_re = re.compile(r'''[-~]''')
    prefix_re = re.compile(r'''^[\[\("']''')
    suffix_re = re.compile(r'''[]\)"']$''')
    return Tokenizer(nlp.vocab, prefix_search=prefix_re.search,
                     suffix_search=suffix_re.search,
                     infix_finditer=infix_re.finditer,
                     token_match=None)

nlp.tokenizer = custom_tokenizer(nlp)

ruler = nlp.add_pipe("entity_ruler", after="ner")

HTML_WRAPPER = """<div style="overflow-x:auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin:5px;>{}</div>"""

patterns = [
    {"label": "CLASS NAME", "pattern": [{"LOWER": "_"}]},
    {"label": "CLASS NAME", "pattern": [{"LOWER": {"REGEX": r"(_\d+\.?\d*.?\d*)"}}]},
    {"label": "CLASS NAME", "pattern": [{"LOWER": "_"}, {"TEXT": {"REGEX": r"(_\d+\.?\d*.?\d*)"}}]},
    {"label": "CLASS NAME", "pattern": [{"TEXT": {"REGEX": r"^[A-Z][a-zA-Z0-9]*$"}}]},
    {"label": "CLASS NAME", "pattern": [{"TEXT": {"REGEX": r"^[A-Z][a-zA-Z0-9]*\.[A-Z][a-zA-Z0-9]*$"}}]},
    {"label": "CLASS NAME", "pattern": [{"TEXT": {"REGEX": r"^[A-Za-z]+\<[A-Za-z]+\>$"}}]}
]

colors = {
    'CLASS NAME': "#508D4E", 
    "CLASS NAME": "#77E4C8",
    "CLASS NAME": "#ffcc00",
    "CLASS NAME": "#ff6666"
}
options = {"ents": ['CLASS NAME', 'CLASS NAME', 'CLASS NAME', 'CLASS NAME'], "colors": colors}

ruler.add_patterns(patterns)


@st.cache_data 
def render_entities(rawtext):
    docx = nlp(rawtext)
    html = displacy.render(docx, style='ent', options=options)
    html = html.replace("\n\n","\n")
    result = HTML_WRAPPER.format(html)
    return result

def get_entities(text):
    with nlp.disable_pipes('ner'):
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

    st.title("Ajudante de Documentação")

    st.subheader("Documentação")
    rawtext = st.text_area("Enter Text", "Type Here")
  
    if st.button("Submit"):
        entities = get_entities(rawtext)
        explanations = [(entity, label, explain_entity(entity, label)) for entity, label in entities]
        st.subheader("Extração de dados")
        st.write(render_entities(rawtext), unsafe_allow_html=True)
        st.divider()
        st.subheader("Explanation")
        st.write(explanations)
            
    
if __name__ == '__main__':
    main()