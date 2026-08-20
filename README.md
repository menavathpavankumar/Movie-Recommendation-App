#  Movie Recommendation System

> A content-based movie recommendation web application that recommends movies similar to a user's selected movie using **TF-IDF vectorization** and **cosine similarity**. The application is built with **Python and Streamlit** and integrates the **OMDb API** to display movie posters, IMDb ratings, release years, and plot summaries.

<p align="center">
  <a href="https://mainpy-k3rcgvkxzpuaaocmvccgrc.streamlit.app/">
    <strong> Live Demo</strong>
  </a>
</p>

---

##  Project Overview

Finding a good movie to watch can be difficult when there are thousands of choices available.

This project solves that problem by building a **content-based movie recommendation system**. Instead of relying on user ratings or information from other users, the system analyzes the **content of movies** such as:

*  Genres
*  Keywords
*  Movie overview

The textual information is processed using Natural Language Processing (NLP), converted into numerical representations using **TF-IDF**, and compared using **cosine similarity**.

When a user selects a movie, the system identifies the movies whose content is most similar and returns the **Top 5 recommendations**.

The Streamlit application then enriches these recommendations using the **OMDb API**, displaying useful information such as posters, IMDb ratings, release years, and plot summaries.

---

##  Live Application

Try the deployed application:

**[ Open Movie Recommendation App](https://mainpy-k3rcgvkxzpuaaocmvccgrc.streamlit.app/)**

### How it works

1. Select a movie from the dropdown.
2. Click **"Recommend Movies"**.
3. The recommendation engine calculates the most similar movies.
4. The application displays the top 5 recommendations.
5. Movie metadata such as poster, IMDb rating, release year, and plot is retrieved from OMDb.

---

##  Features

*  Movie selection through an interactive Streamlit interface
*  Content-based movie recommendations
*  NLP-based text preprocessing
*  TF-IDF feature extraction
*  Cosine similarity for measuring movie similarity
*  Top 5 similar movie recommendations
*  Movie poster retrieval
*  IMDb rating display
*  Release year display
*  Movie plot/overview display
*  Precomputed similarity matrix for faster recommendations
*  Logging for preprocessing and recommendation operations
*  Deployed as a live Streamlit application

---

#  Recommendation Approach

This project uses a **content-based filtering** approach.

The core idea is simple:

> If two movies have similar textual content, they are likely to be similar in terms of genre, themes, keywords, or story.

For every movie, relevant textual fields are combined into a single document:

```text
genres + keywords + overview
```

For example:

```text
Action Adventure superhero
A billionaire builds advanced technology and becomes a superhero...
```

This combined text becomes the basis for calculating similarity between movies.

---

#  End-to-End System Pipeline

```text
                    Movie Dataset
                         │
                         ▼
              Select Relevant Columns
                         │
                         ▼
              Combine Movie Information
             genres + keywords + overview
                         │
                         ▼
                Text Preprocessing
                         │
          ┌──────────────┴──────────────┐
          │                             │
      Lowercasing                 Remove special chars
          │                             │
          └──────────────┬──────────────┘
                         ▼
                  Tokenization
                         │
                         ▼
                Stopword Removal
                         │
                         ▼
                 Cleaned Movie Text
                         │
                         ▼
                  TF-IDF Vectorization
                         │
                         ▼
                 TF-IDF Matrix
                         │
                         ▼
                Cosine Similarity
                         │
                         ▼
             Movie-to-Movie Similarity
                         │
                         ▼
              Top 5 Similar Movies
                         │
                         ▼
                  OMDb API Lookup
                         │
                         ▼
          Posters + Ratings + Year + Plot
                         │
                         ▼
                 Streamlit Interface
```

---

#  Machine Learning / NLP Methodology

## 1. Data Preparation

The application uses a movie dataset stored in:

```text
src/movies.csv
```

The recommendation pipeline uses the following columns:

```text
genres
keywords
overview
title
```

The preprocessing script selects these columns and removes rows containing missing values.

---

## 2. Creating the Movie Representation

Three content fields are combined:

```python
df['combined'] = (
    df['genres'] +
    ' ' +
    df['keywords'] +
    ' ' +
    df['overview']
)
```

This creates a single textual representation for each movie.

The purpose is to give the recommendation system more information than simply comparing movie titles.

---

## 3. Text Preprocessing

The project uses **NLTK** for basic Natural Language Processing.

The preprocessing pipeline includes:

### Lowercasing

All text is converted to lowercase so that words such as:

```text
Action
action
ACTION
```

are treated consistently.

### Removing non-alphabetic characters

Special characters and numbers are removed from the text.

### Tokenization

The text is split into individual words.

For example:

```text
"An amazing action movie"
```

becomes:

```text
["an", "amazing", "action", "movie"]
```

### Stopword Removal

Common English words that provide little information are removed using NLTK stopwords.

The result is cleaner text that focuses more on meaningful movie-related terms.

---

#  TF-IDF Vectorization

After preprocessing, the movie descriptions are converted into numerical vectors using **TF-IDF (Term Frequency-Inverse Document Frequency)**.

TF-IDF measures how important a word is to a particular movie relative to the entire movie collection.

A simplified representation is:

```text
TF-IDF = Term Frequency × Inverse Document Frequency
```

A word that appears frequently in one movie but not across many movies receives a higher importance score.

The project limits the vocabulary to:

```text
5000 features
```

This is implemented using:

```python
TfidfVectorizer(max_features=5000)
```

The output is a **TF-IDF matrix**, where each movie is represented as a numerical vector.

---

# 📐 Cosine Similarity

Once every movie has been converted into a TF-IDF vector, the system needs a way to measure how similar two movies are.

This project uses **cosine similarity**.

The similarity between two vectors is calculated conceptually as:

```text
cosine similarity = (A · B) / (||A|| × ||B||)
```

The value is generally interpreted as:

```text
1.0  → highly similar
0.0  → very different
```

The project calculates the pairwise similarity between all movies and stores the resulting matrix.

```python
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
```

This allows the application to quickly retrieve similar movies when a user makes a selection.

---

#  Recommendation Logic

When a user selects a movie, the system:

### Step 1 — Find the selected movie

The movie title is matched against the dataset.

### Step 2 — Retrieve its similarity scores

The corresponding row from the cosine similarity matrix is retrieved.

### Step 3 — Rank movies

The similarity scores are sorted in descending order.

### Step 4 — Remove the selected movie

The first result is the movie itself, so it is excluded.

### Step 5 — Select the Top 5

The five highest-scoring remaining movies are returned.

Conceptually:

```text
Selected Movie
      │
      ▼
Similarity Scores
      │
      ▼
Sort Descending
      │
      ▼
Remove Selected Movie
      │
      ▼
Top 5 Similar Movies
```

The recommendation logic is implemented in:

```text
src/recommend.py
```

---

#  Streamlit Application

The user interface is built using **Streamlit**.

The main application:

```text
src/main.py
```

provides an interactive interface where users can select a movie and request recommendations.

The application:

* Loads the movie dataset
* Loads the precomputed cosine similarity matrix
* Displays a movie selection dropdown
* Generates recommendations
* Fetches additional movie information
* Displays the results in a user-friendly layout

---

#  OMDb API Integration

The recommendation engine determines **which movies are similar**.

However, a recommendation is more useful when the user can also see information about the recommended movie.

For this reason, the application integrates the **OMDb API**.

For each recommended movie, the application attempts to retrieve:

* 🎬 Movie title
* 🖼️ Poster
* ⭐ IMDb rating
* 📅 Release year
* 📝 Plot

The API integration is implemented in:

```text
src/omdb_utils.py
```

The application also includes fallback handling when movie information or a poster cannot be retrieved.

---

#  Precomputed ML Artifacts

To avoid performing expensive NLP and similarity calculations every time the application starts, the project stores processed artifacts using **Joblib**.

Important files include:

```text
src/tfidf_matrix.pkl
src/cosine_sim.pkl
```

The preprocessing pipeline generates these artifacts before the application is used.

This separates the project into two stages:

### Offline processing

```text
Dataset
   ↓
Cleaning
   ↓
TF-IDF
   ↓
Cosine Similarity
   ↓
Save artifacts
```

### Online recommendation

```text
User selects movie
        ↓
Load precomputed similarity matrix
        ↓
Retrieve similarity scores
        ↓
Return Top 5
        ↓
Fetch movie details
        ↓
Display results
```

This design avoids repeating the expensive preprocessing and similarity calculation for every user request.

---

#  Project Structure

```text
Movie-Recommendation-App/
│
├── src/
│   ├── main.py
│   ├── preprocess.py
│   ├── recommend.py
│   ├── omdb_utils.py
│   ├── movies.csv
│   ├── tfidf_matrix.pkl
│   ├── cosine_sim.pkl
│   ├── config.json
│   └── start_app.txt
│
├── Movie_recommendation_system.ipynb
├── requirements.txt
├── runtime.text
├── .gitignore
├── .gitattributes
├── LICENSE
└── README.md
```

### File responsibilities

| File                                | Purpose                                                            |
| ----------------------------------- | ------------------------------------------------------------------ |
| `src/main.py`                       | Streamlit web application                                          |
| `src/preprocess.py`                 | Data cleaning, NLP preprocessing, TF-IDF and similarity generation |
| `src/recommend.py`                  | Loads data and returns similar movies                              |
| `src/omdb_utils.py`                 | Retrieves movie details from OMDb API                              |
| `src/movies.csv`                    | Movie dataset used by the recommender                              |
| `src/tfidf_matrix.pkl`              | Precomputed TF-IDF representation                                  |
| `src/cosine_sim.pkl`                | Precomputed movie similarity matrix                                |
| `src/config.json`                   | Application/API configuration                                      |
| `Movie_recommendation_system.ipynb` | Exploratory development and recommendation-system experimentation  |
| `requirements.txt`                  | Python dependencies                                                |

---

# 🛠️ Tech Stack

## Programming Language

* **Python**

## Machine Learning / NLP

* **Scikit-learn**

  * TF-IDF Vectorizer
  * Cosine Similarity
* **NLTK**

  * Tokenization
  * Stopword removal

## Data Processing

* **Pandas**
* **NumPy**

## Serialization

* **Joblib**

## Web Application

* **Streamlit**

## External API

* **OMDb API**

## Deployment

* **Streamlit Community Cloud**

---

#  Installation

## 1. Clone the repository

```bash
git clone https://github.com/menavathpavankumar/Movie-Recommendation-App.git
```

Move into the project directory:

```bash
cd Movie-Recommendation-App
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

The project currently uses dependencies including:

```text
streamlit
numpy
pandas
scikit-learn
nltk
joblib
requests
```

---

#  OMDb API Configuration

The application uses the OMDb API to retrieve movie metadata.

Create an OMDb API key and configure it in:

```text
src/config.json
```

Example:

```json
{
    "OMDB_API_KEY": "YOUR_API_KEY"
}
```

> **Security note:** Do not commit real API keys or other secrets to a public GitHub repository. Prefer environment variables or Streamlit secrets for production deployments.

---

#  Running the Application Locally

From the project root:

```bash
streamlit run src/main.py
```

Streamlit will start the application locally.

Open the URL shown in the terminal, usually:

```text
http://localhost:8501
```

---

#  Rebuilding the Recommendation Model

If the movie dataset is changed or updated, regenerate the preprocessing artifacts.

Run:

```bash
python src/preprocess.py
```

The preprocessing script will:

1. Load the movie dataset
2. Select the required columns
3. Remove missing records
4. Combine genres, keywords, and overview
5. Clean and tokenize the text
6. Remove stopwords
7. Generate TF-IDF vectors
8. Calculate cosine similarity
9. Save the generated artifacts

The resulting files include:

```text
tfidf_matrix.pkl
cosine_sim.pkl
```

---

#  Recommendation Performance

The current implementation uses a **precomputed cosine similarity matrix**.

This means the computationally expensive similarity calculation is performed during preprocessing rather than every time a user requests a recommendation.

At application runtime, the system mainly performs:

```text
Movie lookup
     ↓
Similarity vector retrieval
     ↓
Sorting
     ↓
Top-N selection
```

This makes the deployed Streamlit application considerably simpler and faster than recalculating the complete similarity matrix for every request.

---

#  Design Decisions

## Why Content-Based Filtering?

A content-based approach was chosen because recommendations can be generated using movie metadata without requiring individual user histories.

This makes the system suitable for a simple standalone recommendation application.

### Advantages

* No user-rating history required
* No collaborative user data required
* Recommendations are based on movie content
* Easy to understand and explain
* Works for new users immediately

### Limitation

Because the system is content-based, it does not learn individual user preferences.

For example, two users selecting the same movie will receive the same recommendations.

---

#  Current Limitations

This project intentionally uses a relatively simple recommendation architecture, which leaves several opportunities for improvement.

### 1. Content-only recommendations

The system considers movie content rather than user behavior.

A future version could combine:

```text
Content similarity
+
User ratings
+
Watch history
+
Popularity
```

to create a hybrid recommender.

### 2. Limited semantic understanding

TF-IDF is based primarily on word importance and does not understand deeper semantic relationships between words.

For example, it may not fully understand that:

```text
"car"
```

and

```text
"automobile"
```

are semantically related.

A future version could use sentence embeddings or transformer-based models.

### 3. Cold-start for new movies

A newly added movie requires suitable metadata before the content-based system can recommend it effectively.

### 4. External API dependency

Posters, ratings, and plot information depend on the availability of the OMDb API.

If the API request fails, the application falls back to unavailable/default values.

---

# Future Improvements

Potential improvements include:

* [ ] Replace TF-IDF with sentence embeddings
* [ ] Experiment with transformer-based embeddings
* [ ] Build a hybrid recommendation system
* [ ] Add user ratings and feedback
* [ ] Add movie genre filtering
* [ ] Add language/year filters
* [ ] Add recommendation similarity scores to the UI
* [ ] Add movie search instead of only a dropdown
* [ ] Add recommendation explanations such as "Recommended because of similar genres and keywords"
* [ ] Add caching for external API requests
* [ ] Move API secrets to Streamlit Secrets
* [ ] Add automated testing
* [ ] Add CI/CD with GitHub Actions
* [ ] Improve monitoring and logging
* [ ] Add evaluation metrics for recommendation quality

---

# Learning Outcomes

This project helped demonstrate practical experience with:

### Machine Learning

* Building a content-based recommendation system
* Feature extraction using TF-IDF
* Similarity-based ranking
* Precomputing ML artifacts

### Natural Language Processing

* Text cleaning
* Tokenization
* Stopword removal
* Converting text into numerical features

### Python Development

* Modular project structure
* Data processing with Pandas
* Serialization with Joblib
* Logging and error handling
* API integration

### Application Development

* Building an interactive Streamlit application
* Connecting an ML pipeline to a user interface
* Integrating external APIs
* Deploying a Python application to the cloud

---

# Project Workflow

The project can be understood as three major components:

## 1. Recommendation Engine

Responsible for transforming movie content into numerical representations and finding similar movies.

```text
Movie Data
   ↓
NLP Preprocessing
   ↓
TF-IDF
   ↓
Cosine Similarity
   ↓
Top-N Recommendations
```

## 2. Application Layer

Responsible for interacting with the user.

```text
Streamlit UI
   ↓
Movie Selection
   ↓
Recommendation Function
   ↓
Display Results
```

## 3. Metadata Layer

Responsible for enriching the recommendations.

```text
Recommended Movie
       ↓
    OMDb API
       ↓
Poster / Rating / Year / Plot
```

---

#  What This Project Demonstrates

This project is more than a simple movie recommendation script.

It demonstrates an end-to-end workflow:

```text
Raw Data
   ↓
Data Cleaning
   ↓
NLP Processing
   ↓
Feature Engineering
   ↓
Machine Learning
   ↓
Similarity-Based Ranking
   ↓
Model Artifact Storage
   ↓
Application Development
   ↓
External API Integration
   ↓
Cloud Deployment
```

The project therefore combines **data science, NLP, machine learning, Python development, API integration, and deployment** into a single working application.

---

# Notebook

The repository also contains:

```text
Movie_recommendation_system.ipynb
```

The notebook documents the experimentation and development process behind the recommendation system.

It can be useful for understanding the data-processing and recommendation methodology before looking at the production-oriented files under `src/`.

---

# Contributing

Contributions, suggestions, and improvements are welcome.

To contribute:

```bash
git clone https://github.com/menavathpavankumar/Movie-Recommendation-App.git
cd Movie-Recommendation-App
```

Create a new branch:

```bash
git checkout -b feature/improvement
```

Make your changes, commit them, and open a pull request.

---

#  License

This project is licensed under the **MIT License**.

See the `LICENSE` file for more information.

---

#  Author

**Pavan Kumar**

If you found this project interesting, feel free to explore the repository and try the live application.

---

## ⭐ If you like this project

Consider giving the repository a ⭐ on GitHub and trying the live application:

**[🚀 Movie Recommendation App](https://mainpy-k3rcgvkxzpuaaocmvccgrc.streamlit.app/)**

