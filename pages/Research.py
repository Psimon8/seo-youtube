import requests
import streamlit as st
import networkx as nx
from pyvis.network import Network
from collections import defaultdict
import json
import streamlit.components.v1 as components

# Configuration de la page Streamlit
st.set_page_config(
    layout="wide",
    page_title="YouTube Suggest Explorer",
    page_icon="🔍"
)

def fetch_suggestions(query: str, language: str) -> list:
    """Récupère les suggestions de recherche YouTube pour un mot-clé donné."""
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl={language}&q={query}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        suggestions = response.json()[1]
        return suggestions
    except requests.RequestException as e:
        st.error(f"Erreur lors de la récupération des suggestions : {e}")
        return []

def build_suggestion_tree(root_keyword: str, language: str, max_suggestions: int) -> dict:
    """
    Construit un arbre de suggestions.
    - Les suggestions du mot-clé de départ.
    - Pour chaque suggestion, récupère les suggestions associées.
    """
    tree = defaultdict(list)
    root_suggestions = fetch_suggestions(root_keyword, language)[:max_suggestions]
    for suggestion in root_suggestions:
        tree[root_keyword].append(suggestion)
        associated_suggestions = fetch_suggestions(suggestion, language)[:max_suggestions]
        tree[suggestion].extend(associated_suggestions)
    return tree

def display_mind_map(tree: dict):
    """Affiche un mind map pour visualiser les relations entre suggestions."""
    G = nx.Graph()
    for parent, children in tree.items():
        for child in children:
            G.add_edge(parent, child)

    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
    net.from_nx(G)
    html = net.generate_html(notebook=True)
    components.html(html, height=750)

def display_suggestions_table(suggestions: list):
    """Affiche les suggestions dans un tableau."""
    st.table(suggestions)

# Interface utilisateur Streamlit
def main():
    st.title("🔍 YouTube Suggest Explorer")
    st.write("Entrez un mot-clé pour explorer les suggestions de recherche YouTube et leurs relations sous forme de mind map.")
    
    with st.sidebar:
        max_suggestions = st.slider("Nombre de suggestions à récupérer", 1, 10, 2)
        language = st.text_input("Langue de recherche (code)", value="en")
        api_key = st.text_input("Clé API Keyword Everywhere", type="password")
    
    root_keyword = st.text_input("Entrez un mot-clé :", placeholder="Exemple : SEO YouTube")
    
    if st.button("Explorer les suggestions"):
        if not root_keyword.strip():
            st.error("Veuillez entrer un mot-clé valide.")
        else:
            st.info("Recherche des suggestions en cours...")
            tree = build_suggestion_tree(root_keyword, language, max_suggestions)
            if tree:
                st.success("Suggestions récupérées avec succès.")
                display_mind_map(tree)
                keywords = [child for children in tree.values() for child in children]
                display_suggestions_table(keywords)
                volumes = get_keyword_volumes(keywords, api_key)
                if volumes:
                    st.write("Volumes de recherche des suggestions :")
                    st.table(volumes)
            else:
                st.warning("Aucune suggestion trouvée.")

def get_keyword_volumes(keywords, api_key):
    url = 'https://api.keywordseverywhere.com/v1/get_keyword_data'
    my_data = {
        'country': 'fr',
        'currency': 'EUR',
        'dataSource': 'gkp',
        'kw[]': keywords
    }
    my_headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.post(url, data=my_data, headers=my_headers)
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            st.error("Erreur lors de la récupération des volumes de recherche. Veuillez vérifier votre clé API et réessayer.")
            return {}
    else:
        st.error(f"Erreur lors de la récupération des volumes de recherche : {response.status_code}")
        return {}

if __name__ == "__main__":
    main()
