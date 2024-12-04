import requests
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
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
    tree = {
        "name": root_keyword,
        "children": [
            {"name": f"{root_keyword} tutorial", "value": 10},
            {"name": f"{root_keyword} tips", "value": 15},
            {"name": f"{root_keyword} guide", "value": 5},
            {"name": f"{root_keyword} 2023", "value": 20}
        ]
    }
    return tree

def display_treemap(tree: dict):
    """Affiche une tree map pour visualiser les relations entre suggestions."""
    fig = go.Figure(go.Treemap(
        labels=[tree["name"]] + [child["name"] for child in tree["children"]],
        parents=[""] + [tree["name"]] * len(tree["children"]),
        values=[0] + [child["value"] for child in tree["children"]],
        marker=dict(colors=px.colors.qualitative.Pastel)
    ))
    fig.update_layout(
        title="Relations des suggestions YouTube",
        margin=dict(t=50, l=25, r=25, b=25)
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
