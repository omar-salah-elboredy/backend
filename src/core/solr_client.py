import pysolr
import os

SOLR_URL = os.getenv("SOLR_URL", "http://localhost:8983/solr/story_core")
solr = pysolr.Solr(SOLR_URL, always_commit=True)

def index_story_node(story_id: int, node_id: int, prompt: str, content: str):
    """
    Indexes an AI-generated story node into Solr for full-text searching.
    """
    doc = {
        "id": f"node_{node_id}",
        "type_s": "story_node",
        "story_id_i": story_id,
        "prompt_t": prompt,
        "content_t": content,
        "timestamp_dt": "NOW"
    }
    solr.add([doc])

def search_stories(query_text: str):
    """
    Searches across all generated stories using Solr's full-text matching.
    """
    results = solr.search(f"content_t:{query_text} OR prompt_t:{query_text}")
    return [hit for hit in results]
