## Overview

This project implements a search engine for Persian text documents, designed to retrieve and rank news articles from Persian websites. The system leverages classroom concepts and techniques to process, index, and retrieve documents based on user queries.

## Project Structure

The project is divided into two main phases:

### Phase 1: Document Indexing

1. **Dataset**: Utilizes news articles from Persian websites, focusing on the "content" field and using news IDs as document identifiers.
2. **Preprocessing**:
   - Tokenization
   - Normalization
   - Stopword Removal
   - Stemming
3. **Index Creation**: Constructs an inverted index to track word occurrences across documents.
4. **Query Processing**:
   - Implements Boolean operators (AND, OR, NOT) and phrase searches.
   - Ranks results based on word occurrences.

### Phase 2: Document Retrieval and Ranking

1. **Document Modeling**: Uses Term Frequency-Inverse Document Frequency (TF-IDF) to weight document terms.
2. **Query Execution**: Processes user queries and ranks documents based on relevance.
3. **Evaluation**: Tests the system with various query types, including:
   - Simple queries
   - Negated queries
   - Phrase-based queries
   - Complex queries
