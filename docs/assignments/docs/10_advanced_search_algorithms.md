---
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

![bg left:40% 80%](https://oppkey.com/static/logo.jpg)

# **Advanced Search Algorithms Assignment**
## Beyond Cosine Similarity

**Implement and compare multiple similarity algorithms for better search results**

---

# Assignment Overview

## What You'll Build

A comprehensive search algorithm system that implements:
- **Multiple similarity measures** - Cosine, Jaccard, Euclidean, and more
- **Semantic search** - BERT, RoBERTa, and transformer-based embeddings
- **Hybrid search** - Combine multiple algorithms for better results
- **Learning-to-rank** - ML-based ranking optimization
- **Graph-based search** - Network analysis and recommendations
- **Performance comparison** - Benchmark different algorithms

---

# Problem Statement

## Limitations of Basic Search

The current FastOpp system uses basic cosine similarity, which has limitations:
- **Semantic understanding** - Can't understand meaning and context
- **Language variations** - Struggles with synonyms and paraphrasing
- **Multi-modal search** - Can't handle different content types effectively
- **Personalization** - No user-specific ranking or preferences
- **Scalability** - Performance degrades with large datasets
- **Relevance tuning** - Hard to optimize for specific use cases

---

# Your Solution

## Advanced Search System

Create a comprehensive search system that addresses these limitations:

1. **Multiple Algorithms** - Implement various similarity measures
2. **Semantic Understanding** - Use transformer models for better context
3. **Hybrid Approaches** - Combine multiple algorithms for optimal results
4. **Machine Learning** - Use ML for ranking and personalization
5. **Graph Analysis** - Leverage network relationships for recommendations
6. **Performance Optimization** - Efficient algorithms for large datasets

---

# Technical Requirements

## Tech Stack

- **Python 3.8+** with type hints
- **NumPy & SciPy** - Numerical computations
- **Scikit-learn** - Machine learning algorithms
- **Transformers** - Hugging Face transformer models
- **FAISS** - Efficient similarity search
- **NetworkX** - Graph analysis
- **Pandas** - Data manipulation
- **Matplotlib/Seaborn** - Visualization

---

# Project Structure

## Recommended Architecture

```
advanced_search/
├── src/
│   ├── algorithms/
│   │   ├── similarity.py
│   │   ├── semantic.py
│   │   ├── hybrid.py
│   │   └── learning_to_rank.py
│   ├── embeddings/
│   │   ├── text_embeddings.py
│   │   ├── image_embeddings.py
│   │   └── multimodal.py
│   ├── ranking/
│   │   ├── rankers.py
│   │   ├── personalization.py
│   │   └── optimization.py
│   ├── evaluation/
│   │   ├── metrics.py
│   │   ├── benchmarks.py
│   │   └── visualization.py
│   └── utils/
│       ├── preprocessing.py
│       └── performance.py
├── data/
│   ├── test_datasets/
│   └── embeddings/
├── experiments/
│   ├── algorithm_comparison.py
│   └── hyperparameter_tuning.py
└── tests/
    ├── test_algorithms.py
    └── test_evaluation.py
```

---

# Core Components

## 1. Similarity Algorithms

```python
# src/algorithms/similarity.py
import numpy as np
from scipy.spatial.distance import cosine, euclidean, jaccard
from scipy.stats import pearsonr
from sklearn.metrics.pairwise import cosine_similarity, manhattan_distances
from typing import List, Tuple, Dict, Any
import math

class SimilarityAlgorithms:
    def __init__(self):
        self.algorithms = {
            'cosine': self.cosine_similarity,
            'euclidean': self.euclidean_similarity,
            'manhattan': self.manhattan_similarity,
            'jaccard': self.jaccard_similarity,
            'pearson': self.pearson_similarity,
            'jensen_shannon': self.jensen_shannon_similarity,
            'bray_curtis': self.bray_curtis_similarity,
            'canberra': self.canberra_similarity
        }
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
            return 0.0
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    def euclidean_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate Euclidean distance similarity (1 - normalized distance)"""
        distance = euclidean(vec1, vec2)
        max_distance = math.sqrt(len(vec1))  # Maximum possible distance
        return 1 - (distance / max_distance)
    
    def manhattan_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate Manhattan distance similarity"""
        distance = manhattan_distances([vec1], [vec2])[0][0]
        max_distance = np.sum(np.abs(vec1)) + np.sum(np.abs(vec2))
        return 1 - (distance / max_distance) if max_distance > 0 else 0
    
    def jaccard_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate Jaccard similarity for binary vectors"""
        # Convert to binary if needed
        vec1_binary = (vec1 > 0).astype(int)
        vec2_binary = (vec2 > 0).astype(int)
        
        intersection = np.sum(vec1_binary & vec2_binary)
        union = np.sum(vec1_binary | vec2_binary)
        
        return intersection / union if union > 0 else 0
    
    def pearson_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate Pearson correlation coefficient"""
        if len(vec1) != len(vec2) or len(vec1) < 2:
            return 0.0
        
        correlation, _ = pearsonr(vec1, vec2)
        return correlation if not np.isnan(correlation) else 0.0
    
    def jensen_shannon_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate Jensen-Shannon divergence similarity"""
        # Normalize vectors to probability distributions
        p = vec1 / np.sum(vec1) if np.sum(vec1) > 0 else vec1
        q = vec2 / np.sum(vec2) if np.sum(vec2) > 0 else vec2
        
        # Calculate KL divergence
        def kl_divergence(p, q):
            return np.sum(p * np.log(p / q + 1e-10))
        
        # Jensen-Shannon divergence
        m = 0.5 * (p + q)
        js_div = 0.5 * kl_divergence(p, m) + 0.5 * kl_divergence(q, m)
        
        # Convert to similarity (1 - JS divergence)
        return 1 - js_div
    
    def bray_curtis_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate Bray-Curtis similarity"""
        numerator = np.sum(np.abs(vec1 - vec2))
        denominator = np.sum(vec1 + vec2)
        return 1 - (numerator / denominator) if denominator > 0 else 0
    
    def canberra_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate Canberra similarity"""
        numerator = np.sum(np.abs(vec1 - vec2))
        denominator = np.sum(np.abs(vec1) + np.abs(vec2))
        return 1 - (numerator / denominator) if denominator > 0 else 0
    
    def calculate_similarity(self, vec1: np.ndarray, vec2: np.ndarray, 
                           algorithm: str = 'cosine') -> float:
        """Calculate similarity using specified algorithm"""
        if algorithm not in self.algorithms:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        
        return self.algorithms[algorithm](vec1, vec2)
    
    def batch_similarity(self, query_vec: np.ndarray, 
                        candidate_vecs: np.ndarray, 
                        algorithm: str = 'cosine') -> np.ndarray:
        """Calculate similarity between query and multiple candidates"""
        similarities = []
        for candidate_vec in candidate_vecs:
            sim = self.calculate_similarity(query_vec, candidate_vec, algorithm)
            similarities.append(sim)
        return np.array(similarities)
```

---

# Core Components

## 2. Semantic Search

```python
# src/algorithms/semantic.py
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
from typing import List, Dict, Any, Optional
import faiss
from sentence_transformers import SentenceTransformer

class SemanticSearch:
    def __init__(self, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
        self.embeddings = None
    
    def encode_text(self, texts: List[str]) -> np.ndarray:
        """Encode texts to embeddings"""
        embeddings = self.model.encode(texts, convert_to_tensor=False)
        return embeddings
    
    def build_index(self, documents: List[Dict[str, Any]], 
                   index_type: str = 'flat') -> None:
        """Build FAISS index for efficient similarity search"""
        self.documents = documents
        texts = [doc.get('content', '') for doc in documents]
        
        # Encode documents
        self.embeddings = self.encode_text(texts)
        
        # Create FAISS index
        dimension = self.embeddings.shape[1]
        
        if index_type == 'flat':
            self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        elif index_type == 'ivf':
            quantizer = faiss.IndexFlatIP(dimension)
            self.index = faiss.IndexIVFFlat(quantizer, dimension, 100)
        elif index_type == 'hnsw':
            self.index = faiss.IndexHNSWFlat(dimension, 32)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(self.embeddings)
        self.index.add(self.embeddings.astype('float32'))
    
    def search(self, query: str, top_k: int = 10, 
              threshold: float = 0.0) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        if self.index is None:
            raise ValueError("Index not built. Call build_index() first.")
        
        # Encode query
        query_embedding = self.encode_text([query])
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:  # Invalid index
                continue
            
            if score >= threshold:
                result = {
                    'document': self.documents[idx],
                    'score': float(score),
                    'index': int(idx)
                }
                results.append(result)
        
        return results
    
    def search_with_filters(self, query: str, filters: Dict[str, Any], 
                           top_k: int = 10) -> List[Dict[str, Any]]:
        """Search with additional filters"""
        # Get all results first
        all_results = self.search(query, top_k * 2)  # Get more results for filtering
        
        # Apply filters
        filtered_results = []
        for result in all_results:
            doc = result['document']
            matches_filter = True
            
            for key, value in filters.items():
                if key in doc:
                    if isinstance(value, list):
                        if doc[key] not in value:
                            matches_filter = False
                            break
                    else:
                        if doc[key] != value:
                            matches_filter = False
                            break
                else:
                    matches_filter = False
                    break
            
            if matches_filter:
                filtered_results.append(result)
                if len(filtered_results) >= top_k:
                    break
        
        return filtered_results[:top_k]

class MultiModelSemanticSearch:
    def __init__(self, models: List[str] = None):
        self.models = models or [
            'sentence-transformers/all-MiniLM-L6-v2',
            'sentence-transformers/all-mpnet-base-v2',
            'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
        ]
        self.searchers = {}
        
        for model_name in self.models:
            self.searchers[model_name] = SemanticSearch(model_name)
    
    def build_indexes(self, documents: List[Dict[str, Any]]) -> None:
        """Build indexes for all models"""
        for searcher in self.searchers.values():
            searcher.build_index(documents)
    
    def ensemble_search(self, query: str, top_k: int = 10, 
                       weights: Dict[str, float] = None) -> List[Dict[str, Any]]:
        """Perform ensemble search across multiple models"""
        if weights is None:
            weights = {model: 1.0 for model in self.models}
        
        all_results = {}
        
        # Get results from each model
        for model_name, searcher in self.searchers.items():
            results = searcher.search(query, top_k * 2)
            for result in results:
                doc_id = result['index']
                if doc_id not in all_results:
                    all_results[doc_id] = {
                        'document': result['document'],
                        'scores': {},
                        'index': doc_id
                    }
                all_results[doc_id]['scores'][model_name] = result['score']
        
        # Calculate ensemble scores
        ensemble_results = []
        for doc_id, result in all_results.items():
            ensemble_score = 0
            total_weight = 0
            
            for model_name, score in result['scores'].items():
                weight = weights.get(model_name, 1.0)
                ensemble_score += score * weight
                total_weight += weight
            
            if total_weight > 0:
                ensemble_score /= total_weight
                result['ensemble_score'] = ensemble_score
                ensemble_results.append(result)
        
        # Sort by ensemble score
        ensemble_results.sort(key=lambda x: x['ensemble_score'], reverse=True)
        
        return ensemble_results[:top_k]
```

---

# Core Components

## 3. Hybrid Search

```python
# src/algorithms/hybrid.py
import numpy as np
from typing import List, Dict, Any, Tuple
from .similarity import SimilarityAlgorithms
from .semantic import SemanticSearch
import pandas as pd

class HybridSearch:
    def __init__(self, semantic_model: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        self.similarity_algorithms = SimilarityAlgorithms()
        self.semantic_search = SemanticSearch(semantic_model)
        self.documents = []
        self.tfidf_vectors = None
        self.bm25_vectors = None
    
    def build_index(self, documents: List[Dict[str, Any]], 
                   use_tfidf: bool = True, use_bm25: bool = True) -> None:
        """Build multiple indexes for hybrid search"""
        self.documents = documents
        
        # Build semantic index
        self.semantic_search.build_index(documents)
        
        # Build TF-IDF index
        if use_tfidf:
            self._build_tfidf_index(documents)
        
        # Build BM25 index
        if use_bm25:
            self._build_bm25_index(documents)
    
    def _build_tfidf_index(self, documents: List[Dict[str, Any]]) -> None:
        """Build TF-IDF index"""
        from sklearn.feature_extraction.text import TfidfVectorizer
        
        texts = [doc.get('content', '') for doc in documents]
        vectorizer = TfidfVectorizer(
            max_features=10000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        self.tfidf_vectors = vectorizer.fit_transform(texts)
        self.tfidf_vectorizer = vectorizer
    
    def _build_bm25_index(self, documents: List[Dict[str, Any]]) -> None:
        """Build BM25 index"""
        from rank_bm25 import BM25Okapi
        
        texts = [doc.get('content', '').split() for doc in documents]
        self.bm25 = BM25Okapi(texts)
    
    def search(self, query: str, top_k: int = 10, 
              weights: Dict[str, float] = None) -> List[Dict[str, Any]]:
        """Perform hybrid search combining multiple algorithms"""
        if weights is None:
            weights = {
                'semantic': 0.4,
                'tfidf': 0.3,
                'bm25': 0.3
            }
        
        results = {}
        
        # Semantic search
        if 'semantic' in weights and weights['semantic'] > 0:
            semantic_results = self.semantic_search.search(query, top_k * 2)
            for result in semantic_results:
                doc_id = result['index']
                if doc_id not in results:
                    results[doc_id] = {
                        'document': result['document'],
                        'scores': {},
                        'index': doc_id
                    }
                results[doc_id]['scores']['semantic'] = result['score']
        
        # TF-IDF search
        if 'tfidf' in weights and weights['tfidf'] > 0 and self.tfidf_vectors is not None:
            query_vector = self.tfidf_vectorizer.transform([query])
            tfidf_scores = cosine_similarity(query_vector, self.tfidf_vectors).flatten()
            
            top_indices = np.argsort(tfidf_scores)[::-1][:top_k * 2]
            for idx in top_indices:
                if idx not in results:
                    results[idx] = {
                        'document': self.documents[idx],
                        'scores': {},
                        'index': idx
                    }
                results[idx]['scores']['tfidf'] = float(tfidf_scores[idx])
        
        # BM25 search
        if 'bm25' in weights and weights['bm25'] > 0 and self.bm25 is not None:
            bm25_scores = self.bm25.get_scores(query.split())
            top_indices = np.argsort(bm25_scores)[::-1][:top_k * 2]
            
            for idx in top_indices:
                if idx not in results:
                    results[idx] = {
                        'document': self.documents[idx],
                        'scores': {},
                        'index': idx
                    }
                results[idx]['scores']['bm25'] = float(bm25_scores[idx])
        
        # Calculate hybrid scores
        hybrid_results = []
        for doc_id, result in results.items():
            hybrid_score = 0
            total_weight = 0
            
            for algorithm, score in result['scores'].items():
                weight = weights.get(algorithm, 0)
                hybrid_score += score * weight
                total_weight += weight
            
            if total_weight > 0:
                hybrid_score /= total_weight
                result['hybrid_score'] = hybrid_score
                hybrid_results.append(result)
        
        # Sort by hybrid score
        hybrid_results.sort(key=lambda x: x['hybrid_score'], reverse=True)
        
        return hybrid_results[:top_k]

class AdaptiveHybridSearch:
    def __init__(self, semantic_model: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        self.hybrid_search = HybridSearch(semantic_model)
        self.query_classifier = None
        self.performance_history = []
    
    def build_index(self, documents: List[Dict[str, Any]]) -> None:
        """Build indexes and train query classifier"""
        self.hybrid_search.build_index(documents)
        self._train_query_classifier(documents)
    
    def _train_query_classifier(self, documents: List[Dict[str, Any]]) -> None:
        """Train a classifier to determine optimal weights for different query types"""
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.ensemble import RandomForestClassifier
        
        # Generate training data with different query types
        training_queries = []
        training_labels = []
        
        # Short queries (favor BM25)
        short_queries = ["python", "machine learning", "data science"]
        for query in short_queries:
            training_queries.append(query)
            training_labels.append('short')
        
        # Long queries (favor semantic)
        long_queries = [
            "How to implement machine learning algorithms in Python",
            "Best practices for data preprocessing and feature engineering",
            "Understanding deep learning architectures and their applications"
        ]
        for query in long_queries:
            training_queries.append(query)
            training_labels.append('long')
        
        # Technical queries (favor TF-IDF)
        tech_queries = ["API documentation", "error handling", "performance optimization"]
        for query in tech_queries:
            training_queries.append(query)
            training_labels.append('technical')
        
        # Train classifier
        vectorizer = TfidfVectorizer(max_features=1000)
        X = vectorizer.fit_transform(training_queries)
        
        self.query_classifier = RandomForestClassifier(n_estimators=100)
        self.query_classifier.fit(X, vectorizer)
        self.query_vectorizer = vectorizer
    
    def classify_query(self, query: str) -> str:
        """Classify query type to determine optimal weights"""
        if self.query_classifier is None:
            return 'default'
        
        query_vector = self.query_vectorizer.transform([query])
        prediction = self.query_classifier.predict(query_vector)[0]
        return prediction
    
    def get_adaptive_weights(self, query: str) -> Dict[str, float]:
        """Get adaptive weights based on query classification"""
        query_type = self.classify_query(query)
        
        weight_configs = {
            'short': {'semantic': 0.2, 'tfidf': 0.3, 'bm25': 0.5},
            'long': {'semantic': 0.6, 'tfidf': 0.2, 'bm25': 0.2},
            'technical': {'semantic': 0.3, 'tfidf': 0.5, 'bm25': 0.2},
            'default': {'semantic': 0.4, 'tfidf': 0.3, 'bm25': 0.3}
        }
        
        return weight_configs.get(query_type, weight_configs['default'])
    
    def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Perform adaptive hybrid search"""
        weights = self.get_adaptive_weights(query)
        return self.hybrid_search.search(query, top_k, weights)
    
    def update_performance(self, query: str, results: List[Dict[str, Any]], 
                          user_feedback: Dict[int, float]) -> None:
        """Update performance based on user feedback"""
        # Store performance data for future optimization
        performance_data = {
            'query': query,
            'weights': self.get_adaptive_weights(query),
            'results': results,
            'feedback': user_feedback,
            'timestamp': pd.Timestamp.now()
        }
        self.performance_history.append(performance_data)
        
        # Retrain classifier if we have enough data
        if len(self.performance_history) > 100:
            self._retrain_classifier()
    
    def _retrain_classifier(self) -> None:
        """Retrain query classifier based on performance history"""
        # Implementation would analyze performance history
        # and retrain the classifier for better weight prediction
        pass
```

---

# Core Components

## 4. Learning to Rank

```python
# src/algorithms/learning_to_rank.py
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import ndcg_score
import xgboost as xgb

class LearningToRank:
    def __init__(self, model_type: str = 'xgboost'):
        self.model_type = model_type
        self.model = None
        self.feature_names = []
        self.training_data = []
    
    def extract_features(self, query: str, documents: List[Dict[str, Any]], 
                        algorithm_scores: Dict[str, List[float]]) -> np.ndarray:
        """Extract features for learning to rank"""
        features = []
        
        for i, doc in enumerate(documents):
            doc_features = []
            
            # Query features
            query_length = len(query.split())
            doc_features.append(query_length)
            
            # Document features
            content_length = len(doc.get('content', '').split())
            doc_features.append(content_length)
            
            # Title features
            title_length = len(doc.get('title', '').split())
            doc_features.append(title_length)
            
            # Algorithm scores
            for algorithm, scores in algorithm_scores.items():
                if i < len(scores):
                    doc_features.append(scores[i])
                else:
                    doc_features.append(0.0)
            
            # Text similarity features
            query_words = set(query.lower().split())
            content_words = set(doc.get('content', '').lower().split())
            title_words = set(doc.get('title', '').lower().split())
            
            # Word overlap
            content_overlap = len(query_words.intersection(content_words)) / len(query_words) if query_words else 0
            title_overlap = len(query_words.intersection(title_words)) / len(query_words) if query_words else 0
            
            doc_features.extend([content_overlap, title_overlap])
            
            # Position features
            doc_features.append(i)  # Original position
            
            # Recency features
            if 'created_at' in doc:
                days_old = (pd.Timestamp.now() - pd.to_datetime(doc['created_at'])).days
                doc_features.append(days_old)
            else:
                doc_features.append(0)
            
            # Engagement features
            if 'engagement' in doc:
                engagement = doc['engagement']
                total_engagement = sum(engagement.values()) if isinstance(engagement, dict) else engagement
                doc_features.append(total_engagement)
            else:
                doc_features.append(0)
            
            features.append(doc_features)
        
        return np.array(features)
    
    def train(self, training_queries: List[Dict[str, Any]]) -> None:
        """Train the learning to rank model"""
        X = []
        y = []
        
        for query_data in training_queries:
            query = query_data['query']
            documents = query_data['documents']
            relevance_scores = query_data['relevance_scores']
            algorithm_scores = query_data['algorithm_scores']
            
            # Extract features
            features = self.extract_features(query, documents, algorithm_scores)
            X.append(features)
            y.append(relevance_scores)
        
        # Combine all features
        X = np.vstack(X)
        y = np.concatenate(y)
        
        # Train model
        if self.model_type == 'xgboost':
            self.model = xgb.XGBRanker(
                objective='rank:pairwise',
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1
            )
            # XGBoost requires group information
            groups = [len(query_data['documents']) for query_data in training_queries]
            self.model.fit(X, y, group=groups)
        
        elif self.model_type == 'random_forest':
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.model.fit(X, y)
        
        elif self.model_type == 'gradient_boosting':
            self.model = GradientBoostingRegressor(n_estimators=100, random_state=42)
            self.model.fit(X, y)
        
        elif self.model_type == 'linear':
            self.model = LinearRegression()
            self.model.fit(X, y)
    
    def predict_ranking(self, query: str, documents: List[Dict[str, Any]], 
                       algorithm_scores: Dict[str, List[float]]) -> List[float]:
        """Predict ranking scores for documents"""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        features = self.extract_features(query, documents, algorithm_scores)
        scores = self.model.predict(features)
        return scores.tolist()
    
    def rank_documents(self, query: str, documents: List[Dict[str, Any]], 
                      algorithm_scores: Dict[str, List[float]]) -> List[Dict[str, Any]]:
        """Rank documents using the trained model"""
        scores = self.predict_ranking(query, documents, algorithm_scores)
        
        # Create results with ranking scores
        ranked_docs = []
        for i, (doc, score) in enumerate(zip(documents, scores)):
            ranked_doc = doc.copy()
            ranked_doc['ranking_score'] = score
            ranked_doc['original_position'] = i
            ranked_docs.append(ranked_doc)
        
        # Sort by ranking score
        ranked_docs.sort(key=lambda x: x['ranking_score'], reverse=True)
        
        return ranked_docs
    
    def evaluate(self, test_queries: List[Dict[str, Any]]) -> Dict[str, float]:
        """Evaluate the model on test data"""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        ndcg_scores = []
        mrr_scores = []
        
        for query_data in test_queries:
            query = query_data['query']
            documents = query_data['documents']
            relevance_scores = query_data['relevance_scores']
            algorithm_scores = query_data['algorithm_scores']
            
            # Get predicted scores
            predicted_scores = self.predict_ranking(query, documents, algorithm_scores)
            
            # Calculate NDCG
            ndcg = ndcg_score([relevance_scores], [predicted_scores])
            ndcg_scores.append(ndcg)
            
            # Calculate MRR
            sorted_indices = np.argsort(predicted_scores)[::-1]
            mrr = 0
            for i, idx in enumerate(sorted_indices):
                if relevance_scores[idx] > 0:
                    mrr = 1.0 / (i + 1)
                    break
            mrr_scores.append(mrr)
        
        return {
            'ndcg_mean': np.mean(ndcg_scores),
            'ndcg_std': np.std(ndcg_scores),
            'mrr_mean': np.mean(mrr_scores),
            'mrr_std': np.std(mrr_scores)
        }

class PersonalizedLearningToRank(LearningToRank):
    def __init__(self, model_type: str = 'xgboost'):
        super().__init__(model_type)
        self.user_models = {}
        self.global_model = None
    
    def train_user_model(self, user_id: str, training_queries: List[Dict[str, Any]]) -> None:
        """Train a personalized model for a specific user"""
        user_ltor = LearningToRank(self.model_type)
        user_ltor.train(training_queries)
        self.user_models[user_id] = user_ltor
    
    def train_global_model(self, training_queries: List[Dict[str, Any]]) -> None:
        """Train a global model using all user data"""
        super().train(training_queries)
        self.global_model = self.model
    
    def rank_documents_personalized(self, user_id: str, query: str, 
                                   documents: List[Dict[str, Any]], 
                                   algorithm_scores: Dict[str, List[float]]) -> List[Dict[str, Any]]:
        """Rank documents using personalized model if available, otherwise global model"""
        if user_id in self.user_models:
            return self.user_models[user_id].rank_documents(query, documents, algorithm_scores)
        elif self.global_model is not None:
            return self.rank_documents(query, documents, algorithm_scores)
        else:
            raise ValueError("No model available for ranking")
```

---

# Evaluation

## Performance Metrics

```python
# src/evaluation/metrics.py
import numpy as np
from typing import List, Dict, Any
from sklearn.metrics import ndcg_score, precision_score, recall_score
import pandas as pd

class SearchEvaluator:
    def __init__(self):
        self.metrics = {}
    
    def calculate_ndcg(self, relevance_scores: List[float], 
                      predicted_scores: List[float], k: int = 10) -> float:
        """Calculate Normalized Discounted Cumulative Gain"""
        if len(relevance_scores) != len(predicted_scores):
            raise ValueError("Relevance and predicted scores must have same length")
        
        # Sort by predicted scores
        sorted_indices = np.argsort(predicted_scores)[::-1]
        sorted_relevance = [relevance_scores[i] for i in sorted_indices[:k]]
        
        # Calculate DCG
        dcg = 0
        for i, rel in enumerate(sorted_relevance):
            dcg += rel / np.log2(i + 2)
        
        # Calculate IDCG (ideal DCG)
        ideal_relevance = sorted(relevance_scores, reverse=True)[:k]
        idcg = 0
        for i, rel in enumerate(ideal_relevance):
            idcg += rel / np.log2(i + 2)
        
        return dcg / idcg if idcg > 0 else 0
    
    def calculate_mrr(self, relevance_scores: List[float], 
                     predicted_scores: List[float]) -> float:
        """Calculate Mean Reciprocal Rank"""
        sorted_indices = np.argsort(predicted_scores)[::-1]
        
        for i, idx in enumerate(sorted_indices):
            if relevance_scores[idx] > 0:
                return 1.0 / (i + 1)
        
        return 0
    
    def calculate_precision_at_k(self, relevance_scores: List[float], 
                                predicted_scores: List[float], k: int = 10) -> float:
        """Calculate Precision@K"""
        sorted_indices = np.argsort(predicted_scores)[::-1]
        top_k_indices = sorted_indices[:k]
        
        relevant_count = sum(1 for idx in top_k_indices if relevance_scores[idx] > 0)
        return relevant_count / k
    
    def calculate_recall_at_k(self, relevance_scores: List[float], 
                             predicted_scores: List[float], k: int = 10) -> float:
        """Calculate Recall@K"""
        total_relevant = sum(1 for score in relevance_scores if score > 0)
        if total_relevant == 0:
            return 0
        
        sorted_indices = np.argsort(predicted_scores)[::-1]
        top_k_indices = sorted_indices[:k]
        
        relevant_retrieved = sum(1 for idx in top_k_indices if relevance_scores[idx] > 0)
        return relevant_retrieved / total_relevant
    
    def calculate_map(self, relevance_scores: List[float], 
                     predicted_scores: List[float]) -> float:
        """Calculate Mean Average Precision"""
        sorted_indices = np.argsort(predicted_scores)[::-1]
        
        precision_sum = 0
        relevant_count = 0
        
        for i, idx in enumerate(sorted_indices):
            if relevance_scores[idx] > 0:
                relevant_count += 1
                precision_at_i = relevant_count / (i + 1)
                precision_sum += precision_at_i
        
        return precision_sum / relevant_count if relevant_count > 0 else 0
    
    def evaluate_algorithm(self, algorithm_name: str, 
                          test_queries: List[Dict[str, Any]]) -> Dict[str, float]:
        """Evaluate a specific algorithm on test queries"""
        ndcg_scores = []
        mrr_scores = []
        precision_scores = []
        recall_scores = []
        map_scores = []
        
        for query_data in test_queries:
            relevance_scores = query_data['relevance_scores']
            predicted_scores = query_data['algorithm_scores'][algorithm_name]
            
            ndcg_scores.append(self.calculate_ndcg(relevance_scores, predicted_scores))
            mrr_scores.append(self.calculate_mrr(relevance_scores, predicted_scores))
            precision_scores.append(self.calculate_precision_at_k(relevance_scores, predicted_scores))
            recall_scores.append(self.calculate_recall_at_k(relevance_scores, predicted_scores))
            map_scores.append(self.calculate_map(relevance_scores, predicted_scores))
        
        return {
            'ndcg_mean': np.mean(ndcg_scores),
            'ndcg_std': np.std(ndcg_scores),
            'mrr_mean': np.mean(mrr_scores),
            'mrr_std': np.std(mrr_scores),
            'precision_mean': np.mean(precision_scores),
            'precision_std': np.std(precision_scores),
            'recall_mean': np.mean(recall_scores),
            'recall_std': np.std(recall_scores),
            'map_mean': np.mean(map_scores),
            'map_std': np.std(map_scores)
        }
    
    def compare_algorithms(self, algorithm_results: Dict[str, List[Dict[str, Any]]]) -> pd.DataFrame:
        """Compare multiple algorithms"""
        comparison_data = []
        
        for algorithm_name, test_queries in algorithm_results.items():
            metrics = self.evaluate_algorithm(algorithm_name, test_queries)
            metrics['algorithm'] = algorithm_name
            comparison_data.append(metrics)
        
        return pd.DataFrame(comparison_data)
    
    def generate_report(self, comparison_df: pd.DataFrame) -> str:
        """Generate a comprehensive evaluation report"""
        report = "# Algorithm Comparison Report\n\n"
        
        # Summary table
        report += "## Summary\n\n"
        report += comparison_df.to_string(index=False)
        report += "\n\n"
        
        # Best performing algorithm
        best_ndcg = comparison_df.loc[comparison_df['ndcg_mean'].idxmax()]
        report += f"## Best Performing Algorithm (NDCG)\n\n"
        report += f"**{best_ndcg['algorithm']}** with NDCG: {best_ndcg['ndcg_mean']:.4f}\n\n"
        
        # Detailed analysis
        report += "## Detailed Analysis\n\n"
        for metric in ['ndcg_mean', 'mrr_mean', 'precision_mean', 'recall_mean', 'map_mean']:
            best_algorithm = comparison_df.loc[comparison_df[metric].idxmax()]
            report += f"- **{metric.replace('_', ' ').title()}**: {best_algorithm['algorithm']} ({best_algorithm[metric]:.4f})\n"
        
        return report
```

---

# Success Criteria

## Must-Have Features

- [ ] **Multiple Similarity Algorithms** - Implement at least 5 different similarity measures
- [ ] **Semantic Search** - Use transformer models for semantic understanding
- [ ] **Hybrid Search** - Combine multiple algorithms for better results
- [ ] **Learning to Rank** - Implement ML-based ranking optimization
- [ ] **Performance Evaluation** - Comprehensive metrics and benchmarking
- [ ] **Algorithm Comparison** - Compare different approaches objectively
- [ ] **Documentation** - Clear documentation of algorithms and results
- [ ] **Testing** - Unit tests and integration tests

---

# Bonus Challenges

## Advanced Features

- [ ] **Graph-based Search** - Use network analysis for recommendations
- [ ] **Multi-modal Search** - Handle text, images, and other content types
- [ ] **Real-time Learning** - Update models based on user feedback
- [ ] **A/B Testing** - Compare different algorithms in production
- [ ] **Personalization** - User-specific ranking and recommendations
- [ ] **Federated Search** - Search across multiple data sources
- [ ] **Query Expansion** - Improve search with related terms
- [ ] **Result Diversification** - Ensure diverse and relevant results

---

# Getting Started

## Setup Instructions

1. **Set up environment** - Install required packages and dependencies
2. **Prepare test data** - Create or obtain test datasets for evaluation
3. **Implement basic algorithms** - Start with simple similarity measures
4. **Add semantic search** - Integrate transformer models
5. **Build hybrid system** - Combine multiple approaches
6. **Implement learning to rank** - Add ML-based ranking
7. **Create evaluation framework** - Build comprehensive testing system
8. **Compare and optimize** - Benchmark different approaches

---

# Dependencies

## requirements.txt

```txt
numpy>=1.24.0
scipy>=1.10.0
scikit-learn>=1.3.0
transformers>=4.30.0
sentence-transformers>=2.2.0
faiss-cpu>=1.7.4
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
xgboost>=1.7.0
rank-bm25>=0.2.2
networkx>=3.1.0
pytest>=7.0.0
```

---

# Resources

## Helpful Links

- **Scikit-learn** - https://scikit-learn.org/
- **Transformers** - https://huggingface.co/transformers/
- **FAISS** - https://github.com/facebookresearch/faiss
- **Learning to Rank** - https://en.wikipedia.org/wiki/Learning_to_rank
- **NDCG** - https://en.wikipedia.org/wiki/Discounted_cumulative_gain
- **BM25** - https://en.wikipedia.org/wiki/Okapi_BM25

---

# Let's Build Advanced Search!

## Ready to Start?

**This assignment will teach you:**
- Advanced similarity algorithms and their applications
- Semantic search and transformer models
- Hybrid search and ensemble methods
- Machine learning for ranking optimization
- Performance evaluation and benchmarking
- Algorithm comparison and optimization

**Start with basic similarity algorithms and build up to a comprehensive search system!**

---

# Next Steps

## After Completing This Assignment

1. **Benchmark your results** - Compare with existing search systems
2. **Optimize performance** - Improve speed and accuracy
3. **Share your findings** - Document your results and insights
4. **Contribute to open source** - Share your implementations
5. **Move to the next track** - Try database exploration or machine learning pipelines next!

**Happy algorithm development! 🚀**
