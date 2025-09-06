import os
import time
import re
from Bio import Entrez
from dotenv import load_dotenv

def setup_entrez(email):
    """
    Set up Entrez with your email. Always tell NCBI who you are.
    This is a requirement for using their API.
    """
    Entrez.email = email

def search_pubmed(query, max_results=10):
    """
    Search PubMed for a given query and return a list of article IDs.
    """
    print(f"Searching PubMed for: '{query}'...")
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results, sort="relevance")
    record = Entrez.read(handle)
    handle.close()
    id_list = record["IdList"]
    print(f"Found {len(id_list)} results.")
    return id_list

def fetch_and_save_articles(id_list, output_dir="data"):
    """
    Fetch article abstracts from PubMed using a list of IDs and save them as text files.
    """
    if not id_list:
        print("No article IDs to fetch.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    print(f"Fetching details for {len(id_list)} articles...")
    # Use rettype='xml' to get structured data
    handle = Entrez.efetch(db="pubmed", id=id_list, rettype="xml", retmode="xml")
    records = Entrez.read(handle)
    handle.close()

    for i, record in enumerate(records['PubmedArticle']):
        try:
            article = record['MedlineCitation']['Article']
            pmid = record['MedlineCitation']['PMID']
            title = article.get('ArticleTitle', 'No Title Available')

            # Abstract can be structured, so we join its parts
            abstract_parts = article.get('Abstract', {}).get('AbstractText', [])
            abstract = "\n".join(abstract_parts)

            if not abstract:
                abstract = "No Abstract Available"

            # Clean title to make it a valid filename
            safe_title = re.sub(r'[^\w\s-]', '', title).strip()
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            filename = f"{pmid}_{safe_title[:50]}.txt"
            filepath = os.path.join(output_dir, filename)

            print(f"Saving article {i+1}/{len(id_list)}: {filepath}")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"Title: {title}\n\n")
                f.write(f"Abstract:\n{abstract}")

        except Exception as e:
            print(f"Could not process record {i+1}. Error: {e}")

        # NCBI's API usage policy: no more than 3 requests per second without an API key.
        # It's good practice to add a small delay.
        time.sleep(0.5)

    print("\nFinished fetching and saving articles for this query.")

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # --- Configuration ---
    # IMPORTANT: Set your email in the .env file (YOUR_EMAIL="your.email@example.com").
    # NCBI uses this to contact you if there's an issue with your queries.
    YOUR_EMAIL = os.getenv("YOUR_EMAIL")

    # Maximum number of articles to download per disease
    MAX_ARTICLES_PER_DISEASE = 25

    # A list of rare diseases to search for.
    # You can expand this list with more diseases.
    RARE_DISEASES = [
        "Fabry disease",
        "Gaucher disease",
        "Cystic fibrosis",
        "Huntington's disease",
        "Duchenne muscular dystrophy",
        "Pompe disease",
        "Amyotrophic lateral sclerosis (ALS)",
        "Spinal muscular atrophy (SMA)",
    ]

    # Base directory to store all data
    BASE_OUTPUT_DIR = "data"

    # --- Execution ---
    if not YOUR_EMAIL or YOUR_EMAIL == "your.email@example.com":
        print("="*80)
        print("!!! IMPORTANT: Please set the YOUR_EMAIL variable in your .env file. !!!")
        print("="*80)
    else:
        setup_entrez(email=YOUR_EMAIL)

        for disease in RARE_DISEASES:
            print(f"\n{'='*20} Processing: {disease} {'='*20}")

            # Construct a detailed query to find relevant information about
            # symptoms, treatments, drugs, and disease management.
            query = (
                f'("{disease}"[Title/Abstract] OR "{disease}"[MeSH Terms]) AND '
                f'("symptoms"[Title/Abstract] OR "treatment"[Title/Abstract] OR '
                f'"therapy"[Title/Abstract] OR "drug"[Title/Abstract] OR '
                f'"management"[Title/Abstract])'
            )

            # Create a specific, safe directory name for the current disease
            disease_dir_name = re.sub(r'[^\w\s-]', '', disease).strip().replace(' ', '_')
            disease_output_dir = os.path.join(BASE_OUTPUT_DIR, disease_dir_name)

            article_ids = search_pubmed(query=query, max_results=MAX_ARTICLES_PER_DISEASE)
            fetch_and_save_articles(id_list=article_ids, output_dir=disease_output_dir)

            # A delay between processing different diseases to be respectful to NCBI servers
            time.sleep(1)

        print("\nAll diseases processed.")
