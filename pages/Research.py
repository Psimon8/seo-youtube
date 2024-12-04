import streamlit as st
import requests
import plotly.graph_objects as go

# Fonction pour récupérer les suggestions YouTube
def get_youtube_suggestions(keyword, language, max_suggestions):
    url = f"https://suggestqueries.google.com/complete/search?client=youtube&hl={language}&q={keyword}"
    response = requests.get(url)
    try:
        response_json = response.json()
        suggestions = response_json[1][:max_suggestions]
        return suggestions
    except ValueError:
        st.error("Erreur lors de la récupération des suggestions YouTube.")
        return []

# Fonction pour récupérer les volumes de recherche des suggestions
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
    try:
        return response.json()
    except ValueError:
        st.error("Erreur lors de la récupération des volumes de recherche. Veuillez vérifier votre clé API et réessayer.")
        return {}

# Fonction pour construire l'arbre des suggestions
def build_suggestion_tree(root_keyword, language, max_suggestions):
    tree = {"name": root_keyword, "children": []}
    suggestions = get_youtube_suggestions(root_keyword, language, max_suggestions)
    for suggestion in suggestions:
        child_suggestions = get_youtube_suggestions(suggestion, language, max_suggestions)
        tree["children"].append({"name": suggestion, "children": [{"name": cs} for cs in child_suggestions]})
    return tree

# Fonction pour afficher la visualisation en arbre
def display_treemap(tree):
    labels = [tree["name"]]
    parents = [""]
    values = [0]
    for child in tree["children"]:
        labels.append(child["name"])
        parents.append(tree["name"])
        values.append(1)
        for grandchild in child["children"]:
            labels.append(grandchild["name"])
            parents.append(child["name"])
            values.append(1)
    fig = go.Figure(go.Treemap(labels=labels, parents=parents, values=values))
    fig.update_layout(title="Relations des suggestions YouTube", margin=dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(fig, use_container_width=True)

# Interface utilisateur Streamlit
def main():
    st.title("🔍 YouTube Suggest Explorer")
    st.write("Entrez un mot-clé pour explorer les suggestions de recherche YouTube et leurs relations sous forme de tree map.")
    
    with st.sidebar:
        max_suggestions = st.slider("Nombre de suggestions à récupérer", 1, 10, 2)
        language = st.text_input("Langue de recherche (code)", value="en")
        api_key = st.text_input("Clé API Keyword Everywhere")
    
    root_keyword = st.text_input("Entrez un mot-clé :", placeholder="Exemple : SEO YouTube")
    
    if st.button("Explorer les suggestions"):
        if not root_keyword.strip():
            st.error("Veuillez entrer un mot-clé valide.")
        else:
            st.info("Recherche des suggestions en cours...")
            tree = build_suggestion_tree(root_keyword, language, max_suggestions)
            if tree:
                st.success("Suggestions récupérées avec succès.")
                display_treemap(tree)
                keywords = [child["name"] for child in tree["children"]]
                volumes = get_keyword_volumes(keywords, api_key)
                if volumes:
                    st.write("Volumes de recherche des suggestions :")
                    st.table(volumes)
            else:
                st.warning("Aucune suggestion trouvée.")

if __name__ == "__main__":
    main()
