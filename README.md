# Rare Disease Information Agent

This project aims to build an intelligent agent capable of answering questions about rare diseases. It begins by systematically gathering up-to-date medical literature from PubMed, creating a specialized knowledge base for various rare conditions.

The ultimate goal is to develop a Retrieval-Augmented Generation (RAG) agent that can leverage this curated data to provide accurate and context-aware answers to complex queries about symptoms, treatments, and drugs related to rare diseases.

## Features

- **Automated Data Collection**: Fetches scientific article abstracts from PubMed for a predefined list of rare diseases.
- **Organized Data Storage**: Organizes downloaded data into separate, clearly-named directories for each disease within the `data/` folder.
- **Targeted Queries**: Constructs detailed search queries to find relevant information on symptoms, treatments, drugs, and disease management.
- **Secure Configuration**: Manages sensitive information like email addresses and API keys securely using a `.env` file.

## Setup and Installation

Follow these steps to get the project set up on your local machine.

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Hrutik-Pisal/Rare-Disease-Agent.git
    cd Rare-Disease-Agent
    ```

2.  **Create and Activate a Virtual Environment**
    - On Windows:
      ```bash
      python -m venv venv
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables**
    Create a file named `.env` in the root of the project directory and add your email address. This is required by the NCBI API.

    ```env
    # .env
    YOUR_EMAIL="your.email@example.com"
    ```

## Usage

The primary script for data collection is `data.py`. To run it, simply execute the following command from the project's root directory:

```bash
python data.py
```

The script will iterate through the list of diseases defined in `RARE_DISEASES`, search PubMed for relevant articles, and save them in the `data/` directory. Each disease will have its own sub-directory.

> **Note**: The `data/` directory is included in the `.gitignore` file, so the downloaded articles will not be committed to the repository.

## Project Roadmap

- [ ] **Develop a RAG Agent**: Implement a Retrieval-Augmented Generation (RAG) model to process and understand the collected data.
- [ ] **Build an Interactive UI**: Create a user-friendly interface using Streamlit to allow users to ask questions and get answers from the agent.
- [ ] **Expand Data Sources**: Integrate other medical and genetic databases (e.g., MeSH, Gene, OMIM) to enrich the knowledge base.
- [ ] **Advanced Information Extraction**: Implement techniques to parse the text files and extract structured data (symptoms, drugs, etc.) into a more queryable format.

---
