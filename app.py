import requests
from typing import List, Optional, Dict
from youtube_transcript_api import YouTubeTranscriptApi, CouldNotRetrieveTranscript
import json
import openai   
import streamlit as st

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
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def generate_optimized_title(api_key: str, video_title: str) -> str:
    prompt = (f"Analyse le titre suivant d'une vidéo YouTube et génère une version optimisée pour le référencement, en tenant compte des mots-clés, de l'engagement et des bonnes pratiques SEO : {video_title}")
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
    "Utiliser 1 ou 2 émojis pertinents pour capter l’attention. Utiliser les majuscules avec parcimonie pour mettre en valeur des mots-clés ou des éléments importants. "
    "Incorporer des éléments attractifs : Ajouter un aspect unique ou une promesse claire (ex. : 'En 5 minutes', 'Sans expérience'). "
    "Mettre en avant une solution ou un avantage spécifique. Poser une question pour capter l’attention ou susciter la curiosité. "
    "Adapter au format vidéo et à l'audience : Pour des tutoriels, utiliser des formats comme 'Comment...', 'Guide pour...', 'Tuto'. "
    "Pour des classements ou listes, utiliser 'Top X', 'Les X meilleurs...'. Pour des actualités ou analyses, inclure des termes comme '2024', 'Tendances', 'Analyse'."
    "Réponds UNIQUEMENT avec la Réponse."
)

    optimized_title = GPT35(prompt, system_message, api_key)
    return optimized_title

def generate_optimized_description(api_key: str, video_description: str) -> str:
    prompt = (f"Analyse la description suivante d'une vidéo YouTube et génère une version optimisée pour le référencement, en tenant compte des mots-clés, de l'engagement et des bonnes pratiques SEO : {video_description}")
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
    "Réponds UNIQUEMENT avec la Réponse."

)

    optimized_description = GPT35(prompt, system_message, api_key)
    return optimized_description

# Load category data from JSON file
with open('YT_CATEGORY.JSON', 'r', encoding='utf-8') as f:
    category_data = json.load(f)
    category_dict = {str(category['id']): category['name'] for category in category_data['categories']}

def get_top_videos(api_key: str, query: str, language: str, max_results: int = 5) -> Optional[List[dict]]: #Quelles est le nombre de video a scrapper ? 
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults={max_results}&relevanceLanguage={language}&key={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        video_items = response.json().get('items', [])
        
        video_details = []
        for item in video_items:
            video_id = item['id']['videoId']
            video_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id={video_id}&key={api_key}"
            video_response = requests.get(video_url)
            video_response.raise_for_status()
            video_data = video_response.json().get('items', [])[0]
            
            original_title = video_data['snippet']['title']
            optimized_title = generate_optimized_title(openAI_API_KEY, original_title)
            
            original_description = video_data['snippet']['description']
            optimized_description = generate_optimized_description(openAI_API_KEY, original_description)
            
            video_details.append({
                'original_title': original_title,
                'optimized_title': optimized_title,
                'original_description': original_description,
                'optimized_description': optimized_description,
                'views': int(video_data['statistics'].get('viewCount', 0)),
                'length': video_data['contentDetails']['duration'],
                'published_at': video_data['snippet']['publishedAt'],
                'comments': int(video_data['statistics'].get('commentCount', 0)),
                'url': f"https://www.youtube.com/watch?v={video_id}",
                'category': video_data['snippet'].get('categoryId', 'N/A'),  # Category ID
                'channel_title': video_data['snippet']['channelTitle']
            })
        
        return video_details
    except requests.RequestException as e:
        print(f"Error fetching videos: {e}")
        return None

def get_search_suggestions(api_key: str, query: str) -> Optional[List[str]]:
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q={query}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        suggestions = response.json()[1]
        return suggestions
    except requests.RequestException as e:
        print(f"Error fetching search suggestions: {e}")
        return None

def analyze_video_content(video_id, language):
    # Placeholder function for analyzing video content
    return "Sample transcript"

def fetch_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except CouldNotRetrieveTranscript:
        print("No Transcript")

def process_keyword(keyword, language, youtube_api_key, openai_api_key):
    # Placeholder for fetching videos based on keyword
    videos = [
        {'url': 'https://www.youtube.com/watch?v=sample1', 'category': 1, 'channel_title': 'Channel 1'},
        {'url': 'https://www.youtube.com/watch?v=sample2', 'category': 2, 'channel_title': 'Channel 2'},
        # Add more sample videos as needed
    ]
    category_dict = {1: 'Category 1', 2: 'Category 2'}

    for i, video in enumerate(videos):
        st.write(f"URL: {video['url']}")
        category_id = video['category']
        category_name = category_dict.get(category_id, 'Unknown')
        st.write(f"Category: {category_id} ({category_name})")
        st.write(f"Channel: {video['channel_title']}")

        if i <= 5:
            try:
                transcript = analyze_video_content(video['url'].split('=')[-1], language)
                st.write(f"Transcript: {transcript}")
            except Exception as e:
                st.write(f"Error fetching transcript: {e}")

def main():
    st.title("YouTube Video Fetcher")
    
    youtube_api_key = st.text_input("Enter your YouTube API key:")
    openai_api_key = st.text_input("Enter your OpenAI API key:")
    
    keyword = st.text_input("Enter a keyword to fetch top 5 videos:")
    language = st.text_input("Enter the language code (e.g., 'en' for English, 'fr' for French):")

    if st.button("Fetch Videos"):
        if not youtube_api_key or not openai_api_key:
            st.error("Please provide both YouTube API key and OpenAI API key.")
        else:
            process_keyword(keyword, language, youtube_api_key, openai_api_key)

if __name__ == "__main__":
    main()
