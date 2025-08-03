# Blog Content Embeddings & Semantic Search

A Python-based system for creating semantic embeddings from blog posts and content ideas, enabling intelligent search and content discovery through similarity matching.

## Overview

This project combines blog content scraping, embedding generation, and semantic search capabilities to help analyze and discover relevant content from both published articles and content ideas. It uses sentence transformers to create vector embeddings that capture semantic meaning, allowing for sophisticated content matching beyond simple keyword searches.

## Features

- **Blog Content Scraping**: Automatically scrapes blog articles from sitemaps with image downloading
- **Hybrid Embedding Generation**: Creates embeddings for both blog articles and content ideas from CSV
- **Semantic Search**: Query content using natural language with similarity scoring
- **Flexible Filtering**: Search by content type (articles, ideas, or both)
- **Multi-device Support**: Automatic GPU detection with fallback to CPU

## Installation

Ensure you have Python 3.7+ installed, then install the required dependencies:

```bash
pip install sentence-transformers torch pandas requests beautifulsoup4 tqdm
```

## Usage

### 1. Scrape Blog Articles

Extract articles from your website's sitemap:

```bash
python blogscraper.py
```

This creates `articles.json` with structured blog data and downloads associated images to the `images/` directory.

### 2. Generate Embeddings

Create semantic embeddings from blog posts and content ideas:

```bash
python embedhybrid.py [OPTIONS]
```

**Options:**
- `--blog_json`: Path to blog posts JSON file (default: `stepituphr_blog_posts.json`)
- `--ideas_csv`: Path to ideas CSV file (default: `Endless Post Ideas.csv`)
- `--out`: Output JSONL file for embeddings (default: `hybrid_embeddings.jsonl`)

**Example:**
```bash
python embedhybrid.py --blog_json articles.json --ideas_csv "content_ideas.csv" --out embeddings.jsonl
```

### 3. Query Content

Search through embedded content using natural language queries:

```bash
python queryhybrid.py "your search query" [OPTIONS]
```

**Required Arguments:**
- `query`: The search string (natural language)

**Optional Arguments:**
- `-n`: Number of results to return (default: 5)
- `--score`: Minimum similarity score threshold 0.0-1.0 (default: 0.3)
- `--type`: Filter by content type - `idea`, `article`, or `both` (default: both)
- `--device`: Force computation device - `cpu`, `cuda`, or `mps` (auto-detects if not specified)

**Examples:**
```bash
# Basic search
python queryhybrid.py "employee recognition strategies"

# Get top 10 results with higher similarity threshold
python queryhybrid.py "remote work productivity" -n 10 --score 0.5

# Search only article content
python queryhybrid.py "team building activities" --type article

# Force CPU usage
python queryhybrid.py "leadership development" --device cpu
```

## Data Pipeline

1. **Scraping**: `blogscraper.py` → `articles.json` + `images/`
2. **Embedding**: `embedhybrid.py` → `hybrid_embeddings.jsonl`
3. **Search**: `queryhybrid.py` queries the JSONL embeddings file

## File Structure

```
├── blogscraper.py          # Website content scraper
├── embedhybrid.py          # Embedding generation script
├── queryhybrid.py          # Semantic search interface
├── stepituphr_blog_posts.json  # Blog articles data
├── Endless Post Ideas.csv  # Content ideas database
├── hybrid_embeddings.jsonl # Generated embeddings
├── images/                 # Downloaded article images
└── old/                    # Archive of previous versions
```

## Technical Details

- **Embedding Model**: Uses `all-MiniLM-L6-v2` from Sentence Transformers
- **Vector Similarity**: Cosine similarity via dot product scoring
- **Data Format**: JSONL with embedded vectors for efficient loading
- **Device Support**: Automatic detection of CUDA, MPS (Apple Silicon), or CPU

## Output Format

Query results are returned as JSON objects containing:
- `score`: Similarity score (0.0-1.0)
- `type`: Content type ("article" or "idea")
- `title`/`idea`: Content title or idea text
- `url`: Article URL (for articles)
- `published`: Publication date (for articles)
- Additional metadata fields

## Performance Notes

- First run will download the sentence transformer model (~90MB)
- GPU acceleration significantly improves embedding generation speed
- Query performance is near-instantaneous once embeddings are generated
- Memory usage scales with corpus size (embeddings loaded into RAM)
