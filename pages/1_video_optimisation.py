import requests
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi, CouldNotRetrieveTranscript
import json
import openai
import streamlit as st

# Configuration de la page Streamlit
st.set_page_config(
    layout="wide",
    page_title="SEO Youtube",
    page_icon="🎥"
)

def GPT35(prompt, systeme, secret_key, temperature=0.7, model="gpt-4o-mini", max_tokens=1200):
    url = "https://api.openai.com/v1/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": systeme},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {secret_key}"
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 401:
        st.error("Unauthorized access to OpenAI API. Please check your API key.")
        return ""
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def generate_optimized_title(api_key: str, video_title: str, transcript: str, video_description: str) -> str:
    prompt = (f"Analyse le titre: {video_title}, la description: {video_description} et le contenu {transcript} suivant d'une vidéo YouTube et génère une version optimisée pour le référencement, en tenant compte des mots-clés, de l'engagement et des bonnes pratiques SEO")
    system_message = (f"Vous êtes un assistant de rédaction compétent et expérimenté, spécialisé dans l'optimisation SEO des contenus, "
    "et particulièrement dans la création de titres optimisés pour YouTube. "
    "Votre mission est de rédiger des titres engageants, informatifs et performants en termes de SEO, adaptés aux attentes de l'audience et aux bonnes pratiques de référencement. "
    "Voici le système à suivre pour rédiger une title YouTube optimisée pour le SEO : "
    "Identifier le sujet principal : Définir le thème ou le sujet de la vidéo et l’objectif principal (informer, expliquer, divertir, vendre). "
    "Prioriser les mots-clés avec un fort volume de recherche et une concurrence modérée/faible. Considérer les variantes spécifiques liées à la niche ou au public cible. "
    "Structure optimale de la title : Placer le mot-clé principal au début pour maximiser sa visibilité. "
    "Ajouter un mot-clé secondaire ou un complément descriptif. Insérer des éléments engageants (chiffres, questions, superlatifs) pour inciter au clic. Utiliser les ? et ! pour impacter. "
    "Utilisation des bonnes pratiques SEO : Respecter une longueur idéale de 50 à 60 caractères pour éviter la coupure dans les résultats de recherche. "
    "Utiliser un langage clair, simple et engageant. Éviter les titres vagues ou génériques."
    "Utiliser 1 ou 2 émojis pertinents pour capter l’attention. Mais ne mets JAMAIS 2 émojis a la suite. Utiliser les majuscules avec parcimonie pour mettre en valeur des mots-clés ou des éléments importants. "
    "Incorporer des éléments attractifs : Ajouter un aspect unique ou une promesse claire (ex. : 'En 5 minutes', 'Sans expérience'). "
    "Mettre en avant une solution ou un avantage spécifique. Poser une question pour capter l’attention ou susciter la curiosité. "
    "Adapter au format vidéo et à l'audience : Pour des tutoriels, utiliser des formats comme 'Comment...', 'Guide pour...', 'Tuto'. "
    "Pour des classements ou listes, utiliser 'Top X', 'Les X meilleurs...'. Pour des actualités ou analyses, inclure des termes comme '2024', 'Tendances', 'Analyse'."
    "Réponds UNIQUEMENT avec la Réponse. Ne mets JAMAIS 'Titre optimisé:' "
    )
    return GPT35(prompt, system_message, api_key)

def generate_optimized_description(api_key: str, video_description: str, transcript: str, video_title:str) -> str:
    if not video_description:
        return "No Original Description"

    prompt = (f"Analyse la description: {video_description}, le contenu :{transcript} et le titre: {video_title} suivante d'une vidéo YouTube et génère une description optimisée pour le référencement")
    system_message = (f"Vous êtes un assistant de rédaction compétent et expérimenté, spécialisé dans l'optimisation SEO des contenus, "
    "et particulièrement dans la création de descriptions optimisées pour YouTube. "
    "Votre mission est de rédiger des descriptions de vidéos engageantes, informatives et performantes en termes de SEO, adaptées aux attentes de l'audience et aux bonnes pratiques de référencement. "
    "Voici le système à suivre pour rédiger une description YouTube optimisée pour le SEO : "
    "Identifier le sujet principal : Définir le thème ou le sujet de la vidéo et l’objectif principal (informer, expliquer, divertir, vendre). "
    "Inclure des mots-clés pertinents liés au contenu de la vidéo. "
    "Ajouter des variantes spécifiques pour maximiser la visibilité et couvrir des requêtes similaires. "
    "Structure optimale de la description : La premiere phrase doit etre une question incitant TRES impactante pour le viewer en lien avec le mot clé principal. Utilise l'emoji 👇 juste apres la question. "
    "Inclure des hashtags pertinents : Ajouter 8 à 10 hashtags stratégiques à la fin de la description pour améliorer la recherche. "
    "Développer un résumé clair et attrayant du contenu de la vidéo dans les premières lignes. "
    "Inclure des phrases contenant des mots-clés secondaires et des compléments pertinents. "
    "Utilisation des bonnes pratiques SEO : Respecter une longueur idéale entre 400 et 500 caractères pour maximiser la visibilité dans les résultats de recherche. "
    "Utiliser un langage clair, simple et engageant. Éviter les descriptions vagues, génériques ou trop répétitives. "
    "Ajouter des éléments attractifs : Mettre en avant un aspect unique de la vidéo, une promesse claire ou un avantage spécifique (ex. : 'Apprenez en 5 minutes', 'Sans expérience'). "
    "Poser une question pour inciter à l’engagement dans les commentaires ou à cliquer sur la vidéo. "
    "Adapter au format vidéo et à l'audience : Pour des tutoriels, commencer par 'Comment...', 'Découvrez...', 'Guide pour...'. "
    "Pour des classements ou listes, utiliser 'Top X', 'Les X meilleurs...'. Pour des analyses ou actualités, inclure des termes comme '2024', 'Tendances', 'Analyse'. "
    "Ajouter des appels à l’action : Inclure des CTA (Call To Action) pour inviter les spectateurs à liker, s’abonner ou visiter un lien spécifique. "
    "Votre priorité est de produire des descriptions engageantes et performantes en termes de SEO, tout en captant l’intérêt des spectateurs."
    "Réponds UNIQUEMENT avec la Réponse.Ne mets JAMAIS 'Description optimisée:'"
    )
    return GPT35(prompt, system_message, api_key)

def get_video_details(api_key: str, video_url: str) -> Optional[dict]:
    try:
        video_id = video_url.split("v=")[-1].split("&")[0]
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id={video_id}&key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        video_data = response.json().get('items', [])[0]

        return {
            'title': video_data['snippet']['title'],
            'description': video_data['snippet']['description'],
            'views': int(video_data['statistics'].get('viewCount', 0)),
            'published_at': video_data['snippet']['publishedAt'],
            'channel_title': video_data['snippet']['channelTitle'],
            'video_id': video_id
        }
    except Exception as e:
        st.error(f"Error fetching video details: {e}")
        return None

def main():
    st.title("YouTube SEO Assistant")

    with st.sidebar:
        youtube_api_key = st.text_input("Enter your YouTube API key:")
        openai_api_key = st.text_input("Enter your OpenAI API key:")

    video_url = st.text_input("Enter the YouTube video URL:")

    if st.button("Optimize SEO"):
        if not youtube_api_key or not openai_api_key:
            st.error("Please provide both YouTube API key and OpenAI API key.")
        elif not video_url:
            st.error("Please provide a valid YouTube video URL.")
        else:
            video_details = get_video_details(youtube_api_key, video_url)
            if video_details:
                st.write("### Original Video Details")
                st.write(f"**Title:** {video_details['title']}")
                st.write(f"**Description:** {video_details['description']}")
                st.write(f"**Channel:** {video_details['channel_title']}")
                st.write(f"**Views:** {video_details['views']:,}")
                st.write(f"**Published At:** {video_details['published_at']}")

                try:
                    transcript = YouTubeTranscriptApi.get_transcript(video_details['video_id'])
                    transcript_text = " ".join([entry['text'] for entry in transcript])
                except CouldNotRetrieveTranscript:
                    st.error("Could not retrieve transcript for the video.")
                    transcript_text = ""

                optimized_title = generate_optimized_title(openai_api_key, video_details['title'], transcript_text, video_details['description'])
                optimized_description = generate_optimized_description(openai_api_key, video_details['description'], transcript_text, video_details['title'])

                st.write("### Optimized Video Details")
                st.write(f"**Optimized Title:** {optimized_title}")
                st.write(f"**Optimized Description:** {optimized_description}")

if __name__ == "__main__":
    main()
