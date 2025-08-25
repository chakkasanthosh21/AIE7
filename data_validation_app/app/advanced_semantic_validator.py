"""Advanced semantic validation using free RAG and vector database tools."""

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from typing import Dict, List, Tuple, Any
import streamlit as st

class AdvancedSemanticValidator:
    """Advanced semantic validation using embeddings and vector search."""
    
    def __init__(self):
        # Free embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Free vector database - using new ChromaDB client format
        try:
            # Try new client format first
            self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        except Exception:
            try:
                # Fallback to old format
                self.chroma_client = chromadb.Client(
                    chromadb.config.Settings(
                        chroma_db_impl="duckdb+parquet",
                        persist_directory="./chroma_db"
                    )
                )
            except Exception as e:
                st.warning(f"⚠️ Could not initialize ChromaDB: {str(e)}")
                self.chroma_client = None
        
        # Create or get collection for column embeddings
        if self.chroma_client:
            try:
                self.column_collection = self.chroma_client.get_or_create_collection(
                    name="column_embeddings",
                    metadata={"description": "Column semantic embeddings for validation"}
                )
            except Exception as e:
                st.warning(f"⚠️ Could not create collection: {str(e)}")
                self.column_collection = None
        else:
            self.column_collection = None
    
    def analyze_column_semantics_advanced(self, data_sources: Dict[str, pd.DataFrame]) -> Dict:
        """Advanced semantic analysis using embeddings and vector search."""
        st.info("🔍 Running advanced semantic analysis with embeddings...")
        
        if not self.column_collection:
            st.error("❌ ChromaDB not available. Using fallback semantic analysis.")
            return self._fallback_semantic_analysis(data_sources)
        
        semantic_analysis = {}
        all_embeddings = {}
        
        # Generate embeddings for all columns with context
        for dataset_name, dataset_df in data_sources.items():
            semantic_analysis[dataset_name] = {}
            
            for col in dataset_df.columns:
                # Create rich context for better semantic understanding
                context = self._create_column_context(dataset_df, col, dataset_name)
                embedding = self.embedding_model.encode(context)
                
                # Store embedding with metadata
                embedding_id = f"{dataset_name}_{col}"
                all_embeddings[embedding_id] = {
                    'embedding': embedding,
                    'dataset': dataset_name,
                    'column': col,
                    'context': context,
                    'dtype': str(dataset_df[col].dtype),
                    'sample_values': dataset_df[col].dropna().head(5).tolist()
                }
        
        # Store embeddings in ChromaDB
        self._store_embeddings(all_embeddings)
        
        # Find semantic relationships
        semantic_relationships = self._find_semantic_relationships(all_embeddings)
        
        # Generate semantic mapping recommendations
        mapping_recommendations = self._generate_semantic_mappings(semantic_relationships)
        
        return {
            'semantic_relationships': semantic_relationships,
            'mapping_recommendations': mapping_recommendations,
            'embedding_metadata': all_embeddings
        }
    
    def analyze_cross_dataset_semantics(self, data_sources: Dict[str, pd.DataFrame]) -> Dict:
        """Analyze semantic relationships between similar columns across different datasets."""
        if len(data_sources) < 2:
            return {"message": "Need at least 2 datasets for cross-dataset analysis"}
        
        cross_dataset_insights = {}
        
        # Get all column names from all datasets
        all_columns = {}
        for dataset_name, dataset_df in data_sources.items():
            all_columns[dataset_name] = list(dataset_df.columns)
        
        # Find common columns across datasets
        common_columns = set.intersection(*[set(cols) for cols in all_columns.values()])
        
        if not common_columns:
            return {"message": "No common columns found across datasets"}
        
        for common_col in common_columns:
            col_analysis = {}
            
            # Analyze each dataset's column data
            for dataset_name, dataset_df in data_sources.items():
                if common_col in dataset_df.columns:
                    col_data = dataset_df[common_col].dropna()
                    if len(col_data) > 0:
                        # Get sample values and basic stats
                        sample_values = col_data.head(5).tolist()
                        unique_count = col_data.nunique()
                        null_count = col_data.isnull().sum()
                        
                        col_analysis[dataset_name] = {
                            'sample_values': sample_values,
                            'unique_count': int(unique_count),
                            'null_count': int(null_count),
                            'data_type': str(col_data.dtype),
                            'total_rows': int(len(col_data))
                        }
            
            # Compare common columns across datasets
            if len(col_analysis) > 1:
                cross_dataset_insights[common_col] = {
                    'datasets': col_analysis,
                    'comparison': self._compare_common_columns(common_col, col_analysis)
                }
        
        return cross_dataset_insights
    
    def _compare_common_columns(self, column_name: str, col_analysis: Dict) -> Dict:
        """Compare common columns across datasets and identify differences."""
        dataset_names = list(col_analysis.keys())
        
        if len(dataset_names) < 2:
            return {"message": "Need at least 2 datasets for comparison"}
        
        comparison = {
            'data_type_consistency': {},
            'value_overlap': {},
            'sample_differences': {},
            'recommendations': []
        }
        
        # Check data type consistency
        data_types = {name: info['data_type'] for name, info in col_analysis.items()}
        unique_types = set(data_types.values())
        
        if len(unique_types) > 1:
            comparison['data_type_consistency'] = {
                'status': 'inconsistent',
                'types': data_types,
                'issue': f"Column '{column_name}' has different data types across datasets"
            }
            comparison['recommendations'].append(f"Standardize data type for '{column_name}' across all datasets")
        else:
            comparison['data_type_consistency'] = {
                'status': 'consistent',
                'type': list(unique_types)[0]
            }
        
        # Find sample differences (1-2 examples)
        sample_values = {name: info['sample_values'] for name, info in col_analysis.items()}
        
        # Get unique values from all samples
        all_samples = []
        for samples in sample_values.values():
            all_samples.extend(samples)
        
        unique_samples = list(set(all_samples))
        
        if len(unique_samples) > 1:
            # Find examples of differences
            differences = []
            for i, dataset1 in enumerate(dataset_names):
                for j, dataset2 in enumerate(dataset_names[i+1:], i+1):
                    samples1 = set(sample_values[dataset1])
                    samples2 = set(sample_values[dataset2])
                    
                    # Find values unique to each dataset
                    unique_to_1 = samples1 - samples2
                    unique_to_2 = samples2 - samples1
                    
                    if unique_to_1 or unique_to_2:
                        diff_example = {
                            'datasets': [dataset1, dataset2],
                            'unique_to_first': list(unique_to_1)[:2],  # Max 2 examples
                            'unique_to_second': list(unique_to_2)[:2]  # Max 2 examples
                        }
                        differences.append(diff_example)
            
            if differences:
                comparison['sample_differences'] = {
                    'status': 'differences_found',
                    'examples': differences[:2]  # Max 2 difference examples
                }
                comparison['recommendations'].append(f"Review data consistency for '{column_name}' - found differences in sample values")
            else:
                comparison['sample_differences'] = {
                    'status': 'consistent',
                    'message': 'Sample values are consistent across datasets'
                }
        
        # Check for very common differences (null handling, value ranges)
        null_counts = {name: info['null_count'] for name, info in col_analysis.items()}
        unique_counts = {name: info['unique_count'] for name, info in col_analysis.items()}
        
        # Check for significant differences in null counts
        null_values = list(null_counts.values())
        if max(null_values) - min(null_values) > 0:
            comparison['recommendations'].append(f"Column '{column_name}' has inconsistent null handling across datasets")
        
        # Check for significant differences in unique counts
        unique_values = list(unique_counts.values())
        if max(unique_values) - min(unique_values) > 0:
            comparison['recommendations'].append(f"Column '{column_name}' has different cardinality across datasets")
        
        return comparison
    
    def _fallback_semantic_analysis(self, data_sources: Dict[str, pd.DataFrame]) -> Dict:
        """Fallback semantic analysis when ChromaDB is not available."""
        st.info("🔄 Using fallback semantic analysis...")
        
        semantic_analysis = {}
        semantic_relationships = {}
        mapping_recommendations = []
        
        # Simple string similarity analysis
        for dataset_name, dataset_df in data_sources.items():
            semantic_analysis[dataset_name] = {}
            
            for col in dataset_df.columns:
                # Basic semantic analysis
                semantic_type = self._classify_column_semantic_type(dataset_df[col])
                semantic_analysis[dataset_name][col] = {
                    'semantic_type': semantic_type,
                    'context': f"Column: {col}, Type: {dataset_df[col].dtype}, Dataset: {dataset_name}"
                }
        
        # Find relationships between datasets
        if len(data_sources) >= 2:
            dataset_names = list(data_sources.keys())
            base_dataset = dataset_names[0]
            compare_dataset = dataset_names[1]
            
            base_cols = list(data_sources[base_dataset].columns)
            compare_cols = list(data_sources[compare_dataset].columns)
            
            # Simple column matching
            for base_col in base_cols:
                for compare_col in compare_cols:
                    similarity = self._calculate_string_similarity(base_col, compare_col)
                    if similarity > 0.6:  # High similarity threshold
                        pair_key = f"{base_col} ↔ {compare_col}"
                        semantic_relationships[pair_key] = {
                            'similarity_score': similarity,
                            'dataset1': base_dataset,
                            'column1': base_col,
                            'dataset2': compare_dataset,
                            'column2': compare_col,
                            'relationship_type': 'high_similarity' if similarity > 0.8 else 'moderate_similarity'
                        }
                        
                        # Generate recommendation
                        mapping_recommendations.append({
                            'priority': 'High' if similarity > 0.8 else 'Medium',
                            'title': f'Map Columns: {base_col} ↔ {compare_col}',
                            'description': f'High semantic similarity ({similarity:.1%}) detected between columns',
                            'action': f'Create mapping rule: {base_col} = {compare_col}',
                            'impact': f'Will improve data consistency between {base_dataset} and {compare_dataset}',
                            'similarity_score': similarity,
                            'relationship_type': semantic_relationships[pair_key]['relationship_type']
                        })
        
        return {
            'semantic_relationships': semantic_relationships,
            'mapping_recommendations': mapping_recommendations,
            'embedding_metadata': {},
            'fallback_mode': True
        }
    
    def _classify_column_semantic_type(self, col_data):
        """Classify column semantic type based on data patterns."""
        if col_data.dtype in ['int64', 'float64']:
            if col_data.min() >= 0 and col_data.max() <= 100:
                return "percentage_like"
            elif col_data.min() >= 1900 and col_data.max() <= 2100:
                return "year_like"
            elif col_data.min() >= 1 and col_data.max() <= 31:
                return "day_like"
            else:
                return "numeric"
        else:
            # Text column analysis
            sample_values = col_data.dropna().head(10).astype(str)
            if sample_values.str.contains('@').any():
                return "email_like"
            elif sample_values.str.contains(r'\d{4}-\d{2}-\d{2}').any():
                return "date_like"
            elif sample_values.str.len().mean() < 3:
                return "code_like"
            else:
                return "text"
    
    def _calculate_string_similarity(self, str1: str, str2: str) -> float:
        """Calculate string similarity using simple algorithm."""
        # Remove common words and special characters
        common_words = {'id', 'name', 'date', 'time', 'value', 'amount', 'count', 'total'}
        
        words1 = set(str1.lower().replace('_', ' ').replace('-', ' ').split()) - common_words
        words2 = set(str2.lower().replace('_', ' ').replace('-', ' ').split()) - common_words
        
        if not words1 or not words2:
            return 0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0
    
    def _create_column_context(self, df: pd.DataFrame, col: str, dataset_name: str) -> str:
        """Create rich context for column semantic analysis."""
        col_data = df[col].dropna()
        
        # Basic column info
        context_parts = [
            f"column_name: {col}",
            f"dataset: {dataset_name}",
            f"data_type: {df[col].dtype}",
            f"total_rows: {len(df)}",
            f"non_null_rows: {len(col_data)}"
        ]
        
        # Sample data patterns
        if len(col_data) > 0:
            if df[col].dtype in ['int64', 'float64']:
                context_parts.extend([
                    f"min_value: {col_data.min()}",
                    f"max_value: {col_data.max()}",
                    f"mean_value: {col_data.mean():.2f}",
                    f"std_dev: {col_data.std():.2f}"
                ])
            else:
                # Text patterns
                sample_values = col_data.head(10).astype(str)
                avg_length = sample_values.str.len().mean()
                unique_ratio = col_data.nunique() / len(col_data)
                
                context_parts.extend([
                    f"average_length: {avg_length:.1f}",
                    f"uniqueness: {unique_ratio:.2f}",
                    f"sample_values: {', '.join(sample_values.head(3).tolist())}"
                ])
        
        return " | ".join(context_parts)
    
    def _store_embeddings(self, embeddings: Dict[str, Dict]):
        """Store embeddings in ChromaDB."""
        if not self.column_collection:
            st.warning("⚠️ ChromaDB not initialized, skipping embedding storage.")
            return

        try:
            # Prepare data for ChromaDB
            ids = list(embeddings.keys())
            embeddings_list = [emb['embedding'].tolist() for emb in embeddings.values()]
            metadatas = [
                {
                    'dataset': emb['dataset'],
                    'column': emb['column'],
                    'dtype': emb['dtype'],
                    'context': emb['context']
                }
                for emb in embeddings.values()
            ]
            
            # Add to collection
            self.column_collection.add(
                embeddings=embeddings_list,
                metadatas=metadatas,
                ids=ids
            )
            
            st.success(f"✅ Stored {len(embeddings)} column embeddings in vector database")
            
        except Exception as e:
            st.warning(f"⚠️ Could not store embeddings: {str(e)}")
    
    def _find_semantic_relationships(self, embeddings: Dict[str, Dict]) -> Dict:
        """Find semantic relationships between columns using vector similarity."""
        if not self.column_collection:
            st.warning("⚠️ ChromaDB not initialized, skipping semantic relationship search.")
            return {}

        relationships = {}
        
        # Convert embeddings to numpy arrays for similarity calculation
        embedding_ids = list(embeddings.keys())
        embedding_vectors = np.array([emb['embedding'] for emb in embeddings.values()])
        
        # Calculate cosine similarity matrix
        similarity_matrix = self._cosine_similarity_matrix(embedding_vectors)
        
        # Find high-similarity pairs
        for i, id1 in enumerate(embedding_ids):
            for j, id2 in enumerate(embedding_ids):
                if i < j:  # Avoid duplicate pairs
                    similarity = similarity_matrix[i, j]
                    
                    if similarity > 0.7:  # High similarity threshold
                        pair_key = f"{id1} ↔ {id2}"
                        relationships[pair_key] = {
                            'similarity_score': similarity,
                            'dataset1': embeddings[id1]['dataset'],
                            'column1': embeddings[id1]['column'],
                            'dataset2': embeddings[id2]['dataset'],
                            'column2': embeddings[id2]['column'],
                            'relationship_type': self._classify_relationship_type(
                                embeddings[id1], embeddings[id2], similarity
                            )
                        }
        
        return relationships
    
    def _cosine_similarity_matrix(self, embeddings: np.ndarray) -> np.ndarray:
        """Calculate cosine similarity matrix between embeddings."""
        # Normalize embeddings
        normalized = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        # Calculate cosine similarity
        similarity_matrix = np.dot(normalized, normalized.T)
        
        return similarity_matrix
    
    def _classify_relationship_type(self, emb1: Dict, emb2: Dict, similarity: float) -> str:
        """Classify the type of relationship between columns."""
        if similarity > 0.9:
            return "exact_match"
        elif similarity > 0.8:
            return "high_similarity"
        elif similarity > 0.7:
            return "moderate_similarity"
        else:
            return "low_similarity"
    
    def _generate_semantic_mappings(self, relationships: Dict) -> List[Dict]:
        """Generate semantic mapping recommendations."""
        recommendations = []
        
        for pair_key, rel in relationships.items():
            if rel['similarity_score'] > 0.7:
                recommendation = {
                    'priority': 'High' if rel['similarity_score'] > 0.8 else 'Medium',
                    'title': f"Map Columns: {rel['column1']} ↔ {rel['column2']}",
                    'description': f"High semantic similarity ({rel['similarity_score']:.1%}) detected between columns",
                    'action': f"Create mapping rule: {rel['column1']} = {rel['column2']}",
                    'impact': f"Will improve data consistency between {rel['dataset1']} and {rel['dataset2']}",
                    'similarity_score': rel['similarity_score'],
                    'relationship_type': rel['relationship_type']
                }
                recommendations.append(recommendation)
        
        # Sort by similarity score
        recommendations.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return recommendations
    
    def search_similar_columns(self, query_column: str, query_context: str, top_k: int = 5) -> List[Dict]:
        """Search for semantically similar columns using vector similarity."""
        if not self.column_collection:
            st.warning("⚠️ ChromaDB not initialized, skipping similar column search.")
            return []

        # Encode query
        query_embedding = self.embedding_model.encode(query_context)
        
        # Search in ChromaDB
        results = self.column_collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )
        
        # Format results
        similar_columns = []
        for i in range(len(results['ids'][0])):
            similar_columns.append({
                'column_id': results['ids'][0][i],
                'similarity_score': results['distances'][0][i],
                'metadata': results['metadatas'][0][i]
            })
        
        return similar_columns
    
    def get_column_insights(self, dataset_name: str, column_name: str) -> Dict:
        """Get detailed insights about a specific column."""
        if not self.column_collection:
            st.warning("⚠️ ChromaDB not initialized, skipping column insights.")
            return {}

        column_id = f"{dataset_name}_{column_name}"
        
        # Search for this column
        results = self.column_collection.get(
            ids=[column_id]
        )
        
        if results['ids']:
            metadata = results['metadatas'][0]
            
            # Find similar columns
            similar_columns = self.search_similar_columns(
                column_name, 
                metadata['context'],
                top_k=3
            )
            
            return {
                'column_info': metadata,
                'similar_columns': similar_columns,
                'semantic_context': metadata['context']
            }
        
        return {}
