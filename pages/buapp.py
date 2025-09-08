import requests
from typing import List, Optional, Dict
import json
import openai   
import streamlit as st

# Tentative d'importation de youtube-transcript-api avec gestion d'erreurs
try:
    from youtube_transcript_api import YouTubeTranscriptApi, CouldNotRetrieveTranscript
    TRANSCRIPT_API_AVAILABLE = True
except ImportError as e:
    st.error(f"youtube-transcript-api n'est pas installé. Veuillez exécuter: pip install youtube-transcript-api")
    TRANSCRIPT_API_AVAILABLE = False
    # Créer des classes fictives pour éviter les erreurs
    class YouTubeTranscriptApi:
        @staticmethod
        def get_transcript(*args, **kwargs):
            raise Exception("youtube-transcript-api not installed")
        @staticmethod
        def list_transcripts(*args, **kwargs):
            raise Exception("youtube-transcript-api not installed")
    
    class CouldNotRetrieveTranscript(Exception):
        pass

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
    if not video_description:
        return "No Original Description"
    
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
try:
    with open('yt_category.json', 'r', encoding='utf-8') as f:
        yt_category_data = json.load(f)
except FileNotFoundError:
    st.error("The file YT_CATEGORY.JSON was not found. Please ensure it is in the correct directory.")
    yt_category_data = {}

category_dict = {str(category['id']): category['name'] for category in yt_category_data.get('categories', [])}

def get_top_videos(api_key: str, query: str, language: str, openai_api_key: str, max_results: int = 5) -> Optional[List[dict]]:
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
            optimized_title = generate_optimized_title(openai_api_key, original_title)
            
            original_description = video_data['snippet']['description']
            optimized_description = generate_optimized_description(openai_api_key, original_description)
            
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
        st.error(f"Error fetching videos: {e}")
        return None

def get_search_suggestions(api_key: str, query: str) -> Optional[List[str]]:
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q={query}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        suggestions = response.json()[1]
        return suggestions
    except requests.RequestException as e:
        st.error(f"Error fetching search suggestions: {e}")
        return None

def analyze_video_content(video_id: str, language: str = 'fr') -> str:
    """
    MÉTHODE OPTIMALE pour récupérer les transcriptions YouTube
    Hiérarchie de préférence:
    1. Transcriptions manuelles dans la langue préférée
    2. Transcriptions auto-générées dans la langue préférée  
    3. Transcriptions traduites vers la langue préférée
    4. Toute transcription disponible
    """
    if not TRANSCRIPT_API_AVAILABLE:
        return "❌ youtube-transcript-api non installé. Exécutez: pip install youtube-transcript-api"
    
    try:
        # Utiliser la fonction optimisée
        transcript_data = get_best_transcript(video_id, language)
        
        if transcript_data:
            transcript = transcript_data['transcript']
            text = ' '.join([entry['text'] for entry in transcript])
            
            # Nettoyage et formatage du texte
            text = text.replace('\n', ' ').replace('  ', ' ').strip()
            
            # Statistiques
            word_count = len(text.split())
            char_count = len(text)
            duration_seconds = transcript[-1]['start'] + transcript[-1]['duration'] if transcript else 0
            duration_minutes = int(duration_seconds // 60)
            
            # Limitation pour l'affichage
            words = text.split()
            display_text = text
            if len(words) > 300:
                display_text = ' '.join(words[:300]) + f"\n\n[...{word_count - 300} mots supplémentaires masqués...]"
            
            # Informations sur la transcription
            type_emoji = {
                'manual': '✅',
                'generated': '🤖', 
                'translated_from_en': '🔄',
                'translated_from_fr': '🔄'
            }
            
            emoji = type_emoji.get(transcript_data['type'], '📝')
            type_text = transcript_data['type'].replace('_', ' ').title()
            
            header = f"{emoji} {transcript_data['language_name']} ({type_text})"
            stats = f"📊 {word_count} mots • {char_count} caractères • {duration_minutes}min"
            
            return f"{header}\n{stats}\n\n{display_text}"
            
        else:
            return "❌ Aucune transcription disponible pour cette vidéo"
            
    except Exception as e:
        return f"❌ Erreur: {str(e)[:100]}..."

def get_available_transcripts(video_id: str) -> Dict[str, List[str]]:
    """
    Fonction de diagnostic pour lister toutes les transcriptions disponibles
    """
    available_transcripts = {
        'manual': [],
        'generated': [],
        'translatable': []
    }
    
    if not TRANSCRIPT_API_AVAILABLE:
        return available_transcripts
    
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        for transcript in transcript_list:
            lang_info = f"{transcript.language_code} ({transcript.language})"
            
            if transcript.is_generated:
                available_transcripts['generated'].append(lang_info)
            else:
                available_transcripts['manual'].append(lang_info)
            
            # Vérifier si la transcription peut être traduite
            try:
                translation_languages = transcript.translation_languages
                if translation_languages:
                    available_transcripts['translatable'].append(lang_info)
            except:
                pass
                
    except Exception as e:
        st.warning(f"Erreur lors du diagnostic des transcriptions: {str(e)}")
    
    return available_transcripts

def get_best_transcript(video_id: str, preferred_language: str = 'fr') -> Optional[Dict]:
    """
    Récupère la meilleure transcription disponible selon une hiérarchie de préférence
    Retourne un dictionnaire avec les informations de la transcription
    """
    if not TRANSCRIPT_API_AVAILABLE:
        return None
    
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Hiérarchie de préférence
        language_priority = [preferred_language]
        if preferred_language != 'en':
            language_priority.append('en')
        if preferred_language != 'fr':
            language_priority.append('fr')
        
        # 1. Chercher d'abord les transcriptions manuelles dans l'ordre de préférence
        for lang in language_priority:
            for transcript in transcript_list:
                if transcript.language_code == lang and not transcript.is_generated:
                    return {
                        'transcript': transcript.fetch(),
                        'language': transcript.language_code,
                        'language_name': transcript.language,
                        'type': 'manual',
                        'is_generated': False
                    }
        
        # 2. Ensuite les transcriptions auto-générées dans l'ordre de préférence
        for lang in language_priority:
            for transcript in transcript_list:
                if transcript.language_code == lang and transcript.is_generated:
                    return {
                        'transcript': transcript.fetch(),
                        'language': transcript.language_code,
                        'language_name': transcript.language,
                        'type': 'generated',
                        'is_generated': True
                    }
        
        # 3. Essayer de traduire vers la langue préférée
        if preferred_language in ['fr', 'en']:
            for transcript in transcript_list:
                try:
                    if transcript.language_code != preferred_language:
                        translated = transcript.translate(preferred_language)
                        return {
                            'transcript': translated.fetch(),
                            'language': preferred_language,
                            'language_name': f"Translated to {preferred_language}",
                            'type': f'translated_from_{transcript.language_code}',
                            'is_generated': True,
                            'original_language': transcript.language_code
                        }
                except:
                    continue
        
        # 4. Prendre la première transcription disponible
        for transcript in transcript_list:
            try:
                return {
                    'transcript': transcript.fetch(),
                    'language': transcript.language_code,
                    'language_name': transcript.language,
                    'type': 'generated' if transcript.is_generated else 'manual',
                    'is_generated': transcript.is_generated
                }
            except:
                continue
                
    except Exception as e:
        st.warning(f"Erreur lors de la récupération de la transcription: {str(e)}")
    
    return None

def process_keyword(keyword: str, language: str, youtube_api_key: str, openai_api_key: str, max_results: int) -> None:
    st.write(f"\nFetching top {max_results} videos for '{keyword}' in '{language}' language...")
    
    # Fetch top videos
    top_videos = get_top_videos(youtube_api_key, keyword, language, openai_api_key, max_results)
    if top_videos:
        st.write(f"\nTop {max_results} Related Videos:")
        for i, video in enumerate(top_videos, 1):
            st.write(f"#{i} {video['original_title']} Channel: {video['channel_title']}")
            st.write(f"URL: {video['url']} Category: {category_dict.get(video['category'], 'Unknown')} Views: {video['views']:,} Length: {video['length']} Published at: {video['published_at']} Comments: {video['comments']:,}")
            
            with st.expander("Details"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write("Original Title")
                    st.write(video['original_title'])
                    st.write("Original Description")
                    st.write(video['original_description'])
                with col2:
                    st.write("Optimized Title")
                    st.write(video['optimized_title'])
                    st.write("Optimized Description")
                    st.write(video['optimized_description'])
                with col3:
                    st.write("Transcript")
                    transcript = analyze_video_content(video['url'].split('=')[-1], language)
                    st.write(transcript)

def main():
    st.title("Youtube SEO Assistant")
    
    # Afficher un avertissement si la bibliothèque de transcription n'est pas disponible
    if not TRANSCRIPT_API_AVAILABLE:
        st.warning("⚠️ La bibliothèque youtube-transcript-api n'est pas installée. Les transcriptions ne seront pas disponibles. Pour résoudre ce problème, exécutez: `pip install youtube-transcript-api`")
    
    with st.sidebar:
        youtube_api_key = st.text_input("Enter your YouTube API key:")
        openai_api_key = st.text_input("Enter your OpenAI API key:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        keyword = st.text_input("Enter a keyword to fetch top videos:")
        language = st.selectbox("Enter the language code (e.g., 'en' for English, 'fr' for French):", options=['en', 'fr'], index=1)
        max_results = st.slider("Select the number of top videos to fetch (and the number of transcripts):", 1, 10, 5)
    
    fetch_videos = st.button("Fetch Videos")
    
    if not fetch_videos:
        with col2:
            if keyword:
                st.write(f"Search Suggestions for '{keyword}':")
                suggestions = get_search_suggestions(youtube_api_key, keyword)
                if suggestions:
                    for suggestion in suggestions[:10]:
                        st.write(f"{suggestion}")

    if fetch_videos:
        if not youtube_api_key or not openai_api_key:
            st.error("Please provide both YouTube API key and OpenAI API key.")
        else:
            process_keyword(keyword, language, youtube_api_key, openai_api_key, max_results)

if __name__ == "__main__":
    main()
