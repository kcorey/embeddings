# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based embeddings project focused on blog content analysis and semantic search. The system scrapes blog articles, generates embeddings using sentence transformers, and provides hybrid search capabilities across both articles and content ideas.

## Core Architecture

The project consists of three main components:

1. **Data Collection** (`blogscraper.py`): Scrapes blog articles from sitemap XML, downloads associated images, and extracts structured content including title, author, published date, and full text content.

2. **Embedding Generation** (`embedhybrid.py`): Processes blog posts and idea CSV files to generate semantic embeddings using the `all-MiniLM-L6-v2` model. Outputs unified JSONL format with both article and idea data.

3. **Semantic Search** (`queryhybrid.py`): Provides command-line interface for querying the embedded content using similarity search with configurable filters and scoring thresholds.

## Key Commands

### Running the scraper
```bash
python blogscraper.py
```
Outputs: `articles.json` and downloads images to `images/` directory

### Generating embeddings
```bash
python embedhybrid.py --blog_json stepituphr_blog_posts.json --ideas_csv "Endless Post Ideas.csv" --out hybrid_embeddings.jsonl
```

### Querying embeddings
```bash
python queryhybrid.py "your query" -n 10 --score 0.3 --type both --device mps
```

Options:
- `-n`: Number of results (default: 5)
- `--score`: Minimum similarity threshold (default: 0.3)
- `--type`: Filter by "idea", "article", or "both" (default: both)
- `--device`: Force device "cpu", "cuda", or "mps" (auto-detects by default)

## Data Flow

1. Blog articles scraped → `stepituphr_blog_posts.json`
2. Articles + ideas CSV → embedding generation → `hybrid_embeddings.jsonl`
3. Query processing uses the JSONL file for semantic search

## Dependencies

Core Python packages required:
- `sentence-transformers`: For embedding generation and similarity search
- `torch`: PyTorch backend for neural networks
- `pandas`: CSV processing for ideas data
- `requests`: HTTP requests for scraping
- `beautifulsoup4`: HTML parsing
- `tqdm`: Progress bars
- `xml.etree.ElementTree`: XML sitemap parsing

## File Structure

- Main scripts: `blogscraper.py`, `embedhybrid.py`, `queryhybrid.py`
- Data files: `stepituphr_blog_posts.json`, `Endless Post Ideas.csv`, `hybrid_embeddings.jsonl`
- Images: Downloaded to `images/` directory
- Archive: `old/` contains previous iterations and development files