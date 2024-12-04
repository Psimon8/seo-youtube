import requests
import streamlit as st
import plotly.express as px
from collections import defaultdict

# Configuration de la page Streamlit
st.set_page_config(
    layout="wide",
    page_title="YouTube Suggest Explorer",
    page_icon="🔍"
)

def fetch_suggestions(query: str) -> list:
    """Récupère les suggestions de recherche YouTube pour un mot-clé donné."""
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q={query}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        suggestions = response.json()[1]
        return suggestions
    except requests.RequestException as e:
        st.error(f"Erreur lors de la récupération des suggestions : {e}")
        return []

def build_suggestion_tree(root_keyword: str) -> dict:
    """
    Construit un arbre de suggestions.
    - Les 10 premières suggestions du mot-clé de départ.
    - Pour chaque suggestion, récupère les suggestions associées.
    """
    tree = defaultdict(list)
    root_suggestions = fetch_suggestions(root_keyword)[:10]  # 10 premières suggestions pour le mot-clé de départ
    for suggestion in root_suggestions:
        tree[root_keyword].append(suggestion)
        # Récupère les suggestions associées pour chaque suggestion
        associated_suggestions = fetch_suggestions(suggestion)[:10]
        tree[suggestion].extend(associated_suggestions)
    return tree

def display_treemap(tree: dict):
    """Affiche une tree map pour visualiser les relations entre suggestions."""
    data = []
    for parent, children in tree.items():
        for child in children:
            data.append({"Parent": parent, "Child": child})

    # Conversion en DataFrame pour Plotly
    import pandas as pd
    df = pd.DataFrame(data)

    # Générer la tree map
    fig = px.treemap(
        df,
        path=["Parent", "Child"],
        values=None,  # Pas de valeur spécifique, juste pour la structure
        title="Relations des suggestions YouTube",
        color_discrete_sequence=px.colors.qualitative.Pastel  # Palette de couleurs
    )
    st.plotly_chart(fig, use_container_width=True)

# Interface utilisateur Streamlit
def main():
    st.title("🔍 YouTube Suggest Explorer")
    st.write("Entrez un mot-clé pour explorer les suggestions de recherche YouTube et leurs relations sous forme de tree map.")
    
    # Champ pour saisir le mot-clé
    root_keyword = st.text_input("Entrez un mot-clé :", placeholder="Exemple : SEO YouTube")
    
    # Bouton pour lancer l'exploration
    if st.button("Explorer les suggestions"):
        if not root_keyword.strip():
            st.error("Veuillez entrer un mot-clé valide.")
        else:
            st.info("Recherche des suggestions en cours...")
            tree = build_suggestion_tree(root_keyword)
            if tree:
                st.success("Suggestions récupérées avec succès.")
                display_treemap(tree)
            else:
                st.warning("Aucune suggestion trouvée.")

if __name__ == "__main__":
    main()
