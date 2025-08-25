"""Advanced ML and statistical validation using free tools."""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import scipy.stats as stats
from typing import Dict, List, Any
import streamlit as st

class AdvancedMLValidator:
    """Advanced ML and statistical validation using free tools."""
    
    def __init__(self):
        # Free ML models
        self.outlier_detector = IsolationForest(
            contamination=0.1, 
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=3, random_state=42)
        
    def analyze_data_quality_advanced(self, data_sources: Dict[str, pd.DataFrame]) -> Dict:
        """Analyze data quality across multiple datasets using advanced ML techniques."""
        quality_analysis = {}
        
        for dataset_name, dataset_df in data_sources.items():
            try:
                # Analyze data quality for this dataset
                dataset_analysis = {
                    'anomalies': self._detect_anomalies_advanced(dataset_df),
                    'distributions': self._analyze_distributions_advanced(dataset_df),
                    'patterns': self._detect_data_patterns(dataset_df),
                    'quality_score': self._calculate_ml_quality_score(dataset_df),
                    'recommendations': []
                }
                
                # Generate ML-based recommendations
                dataset_analysis['recommendations'] = self._generate_ml_recommendations(
                    dataset_analysis, dataset_name
                )
                
                quality_analysis[dataset_name] = dataset_analysis
                
            except Exception as e:
                st.warning(f"⚠️ Could not analyze {dataset_name}: {str(e)}")
                quality_analysis[dataset_name] = {'error': str(e)}
        
        return quality_analysis
    
    def _detect_anomalies_advanced(self, df: pd.DataFrame) -> Dict:
        """Advanced anomaly detection using ML."""
        anomalies = {}
        
        for col in df.select_dtypes(include=[np.number]).columns:
            col_data = df[col].dropna()
            
            if len(col_data) > 10:
                try:
                    # Prepare data for ML
                    data_reshaped = col_data.values.reshape(-1, 1)
                    scaled_data = self.scaler.fit_transform(data_reshaped)
                    
                    # ML-based outlier detection
                    outlier_labels = self.outlier_detector.fit_predict(scaled_data)
                    outlier_indices = np.where(outlier_labels == -1)[0]
                    outlier_count = len(outlier_indices)
                    
                    # Statistical outlier detection (Z-score method)
                    z_scores = np.abs(stats.zscore(col_data))
                    statistical_outliers = np.where(z_scores > 3)[0]
                    statistical_outlier_count = len(statistical_outliers)
                    
                    # IQR method
                    Q1 = col_data.quantile(0.25)
                    Q3 = col_data.quantile(0.75)
                    IQR = Q3 - Q1
                    iqr_outliers = col_data[(col_data < (Q1 - 1.5 * IQR)) | (col_data > (Q3 + 1.5 * IQR))]
                    iqr_outlier_count = len(iqr_outliers)
                    
                    anomalies[col] = {
                        'ml_outliers': {
                            'count': int(outlier_count),
                            'percentage': float(outlier_count / len(col_data)),
                            'indices': [int(i) for i in outlier_indices.tolist()]
                        },
                        'statistical_outliers': {
                            'count': int(statistical_outlier_count),
                            'percentage': float(statistical_outlier_count / len(col_data)),
                            'indices': [int(i) for i in statistical_outliers.tolist()]
                        },
                        'iqr_outliers': {
                            'count': int(iqr_outlier_count),
                            'percentage': float(iqr_outlier_count / len(col_data)),
                            'values': [float(v) if isinstance(v, (np.floating, float)) else int(v) for v in iqr_outliers.tolist()]
                        },
                        'consensus_outliers': self._find_consensus_outliers(
                            outlier_indices, statistical_outliers, iqr_outliers.index.tolist()
                        )
                    }
                    
                except Exception as e:
                    st.warning(f"⚠️ Could not analyze column {col}: {str(e)}")
                    anomalies[col] = {'error': str(e)}
        
        return anomalies
    
    def _find_consensus_outliers(self, ml_outliers, statistical_outliers, iqr_outliers):
        """Find outliers detected by multiple methods (consensus)."""
        # Convert to sets for intersection
        ml_set = set(int(i) for i in ml_outliers)
        stat_set = set(int(i) for i in statistical_outliers)
        iqr_set = set(int(i) for i in iqr_outliers)
        
        # Find consensus outliers (detected by at least 2 methods)
        consensus = (ml_set & stat_set) | (ml_set & iqr_set) | (stat_set & iqr_set)
        
        return {
            'count': int(len(consensus)),
            'percentage': float(len(consensus) / len(ml_outliers) if len(ml_outliers) > 0 else 0),
            'indices': [int(i) for i in list(consensus)]
        }
    
    def _analyze_distributions_advanced(self, df: pd.DataFrame) -> Dict:
        """Advanced distribution analysis using statistical tests."""
        distributions = {}
        
        for col in df.select_dtypes(include=[np.number]).columns:
            col_data = df[col].dropna()
            
            if len(col_data) > 10:
                try:
                    # Statistical tests for normality
                    shapiro_test = stats.shapiro(col_data)
                    kolmogorov_test = stats.kstest(col_data, 'norm')
                    
                    # Distribution characteristics
                    skewness = stats.skew(col_data)
                    kurtosis = stats.kurtosis(col_data)
                    
                    # Quantile analysis
                    percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]
                    quantiles = np.percentile(col_data, percentiles)
                    
                    # Distribution classification
                    distribution_type = self._classify_distribution_advanced(
                        col_data, skewness, kurtosis, shapiro_test.pvalue
                    )
                    
                    distributions[col] = {
                        'distribution_type': distribution_type,
                        'normality_tests': {
                            'shapiro_wilk': {
                                'statistic': float(shapiro_test.statistic),
                                'p_value': float(shapiro_test.pvalue),
                                'is_normal': bool(shapiro_test.pvalue > 0.05)
                            },
                            'kolmogorov_smirnov': {
                                'statistic': float(kolmogorov_test.statistic),
                                'p_value': float(kolmogorov_test.pvalue),
                                'is_normal': bool(kolmogorov_test.pvalue > 0.05)
                            }
                        },
                        'shape_characteristics': {
                            'skewness': float(skewness),
                            'kurtosis': float(kurtosis),
                            'mean': float(col_data.mean()),
                            'median': float(col_data.median()),
                            'std': float(col_data.std())
                        },
                        'quantiles': {int(p): float(q) for p, q in zip(percentiles, quantiles)},
                        'confidence_intervals': self._calculate_confidence_intervals(col_data)
                    }
                    
                except Exception as e:
                    st.warning(f"⚠️ Could not analyze distribution for {col}: {str(e)}")
                    distributions[col] = {'error': str(e)}
        
        return distributions
    
    def _classify_distribution_advanced(self, data, skewness, kurtosis, shapiro_p):
        """Advanced distribution classification."""
        if shapiro_p > 0.05:
            base_type = "normal_like"
        else:
            base_type = "non_normal"
        
        # Classify by shape
        if abs(skewness) < 0.5:
            shape = "symmetric"
        elif skewness > 0.5:
            shape = "right_skewed"
        else:
            shape = "left_skewed"
        
        # Classify by tail behavior
        if kurtosis < -0.5:
            tails = "light_tailed"
        elif kurtosis > 0.5:
            tails = "heavy_tailed"
        else:
            tails = "normal_tailed"
        
        return f"{base_type}_{shape}_{tails}"
    
    def _calculate_confidence_intervals(self, data, confidence=0.95):
        """Calculate confidence intervals for mean and standard deviation."""
        n = len(data)
        mean = float(data.mean())
        std = float(data.std())
        
        # t-distribution for small samples, normal for large samples
        if n < 30:
            t_value = float(stats.t.ppf((1 + confidence) / 2, n - 1))
            margin_error = float(t_value * std / np.sqrt(n))
        else:
            z_value = float(stats.norm.ppf((1 + confidence) / 2))
            margin_error = float(z_value * std / np.sqrt(n))
        
        return {
            'mean_ci': (float(mean - margin_error), float(mean + margin_error)),
            'std_ci': self._bootstrap_std_ci(data, confidence)
        }
    
    def _bootstrap_std_ci(self, data, confidence, n_bootstrap=1000):
        """Bootstrap confidence interval for standard deviation."""
        bootstrap_stds = []
        for _ in range(n_bootstrap):
            bootstrap_sample = np.random.choice(data, size=len(data), replace=True)
            bootstrap_stds.append(float(bootstrap_sample.std()))
        
        lower_percentile = (1 - confidence) / 2 * 100
        upper_percentile = (1 + confidence) / 2 * 100
        
        return (
            float(np.percentile(bootstrap_stds, lower_percentile)),
            float(np.percentile(bootstrap_stds, upper_percentile))
        )
    
    def _detect_data_patterns(self, df: pd.DataFrame) -> Dict:
        """Detect patterns in data using ML techniques."""
        patterns = {}
        
        for col in df.select_dtypes(include=[np.number]).columns:
            col_data = df[col].dropna()
            
            if len(col_data) > 10:
                try:
                    # Detect clusters in the data
                    data_reshaped = col_data.values.reshape(-1, 1)
                    scaled_data = self.scaler.fit_transform(data_reshaped)
                    
                    # K-means clustering
                    cluster_labels = self.kmeans.fit_predict(scaled_data)
                    unique_clusters, cluster_counts = np.unique(cluster_labels, return_counts=True)
                    
                    # Detect periodicity (if applicable)
                    periodicity = self._detect_periodicity(col_data)
                    
                    # Detect trends
                    trend = self._detect_trend(col_data)
                    
                    patterns[col] = {
                        'clustering': {
                            'n_clusters': int(len(unique_clusters)),
                            'cluster_sizes': {int(k): int(v) for k, v in zip(unique_clusters, cluster_counts)},
                            'cluster_centers': [float(c) for c in self.kmeans.cluster_centers_.flatten().tolist()]
                        },
                        'periodicity': periodicity,
                        'trend': trend,
                        'pattern_complexity': self._assess_pattern_complexity(
                            cluster_labels, periodicity, trend
                        )
                    }
                    
                except Exception as e:
                    st.warning(f"⚠️ Could not detect patterns for {col}: {str(e)}")
                    patterns[col] = {'error': str(e)}
        
        return patterns
    
    def _detect_periodicity(self, data):
        """Detect periodicity in time series data."""
        if len(data) < 20:
            return None
        
        try:
            # Simple autocorrelation analysis
            autocorr = np.correlate(data, data, mode='full')
            autocorr = autocorr[len(autocorr)//2:]
            
            # Find peaks in autocorrelation
            from scipy.signal import find_peaks
            peaks, _ = find_peaks(autocorr[:len(autocorr)//2])
            
            if len(peaks) > 0:
                # Estimate period
                period = peaks[0] if peaks[0] > 0 else None
                return {
                    'has_periodicity': True,
                    'estimated_period': period,
                    'autocorrelation_strength': autocorr[peaks[0]] / autocorr[0] if period else 0
                }
            else:
                return {'has_periodicity': False}
                
        except Exception:
            return {'has_periodicity': False}
    
    def _detect_trend(self, data):
        """Detect trends in data."""
        if len(data) < 10:
            return None
        
        try:
            # Linear trend detection
            x = np.arange(len(data))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, data)
            
            # Trend classification
            if abs(slope) < 0.01:
                trend_type = "no_trend"
            elif slope > 0.01:
                trend_type = "increasing"
            else:
                trend_type = "decreasing"
            
            return {
                'trend_type': trend_type,
                'slope': slope,
                'r_squared': r_value**2,
                'p_value': p_value,
                'trend_strength': 'strong' if r_value**2 > 0.7 else 'weak'
            }
            
        except Exception:
            return {'trend_type': 'unknown'}
    
    def _assess_pattern_complexity(self, clusters, periodicity, trend):
        """Assess the complexity of detected patterns."""
        complexity_score = 0
        
        # Clustering complexity
        if clusters is not None:
            complexity_score += len(np.unique(clusters)) * 0.3
        
        # Periodicity complexity
        if periodicity and periodicity.get('has_periodicity'):
            complexity_score += 0.4
        
        # Trend complexity
        if trend and trend.get('trend_type') != 'no_trend':
            complexity_score += 0.3
        
        if complexity_score < 0.3:
            return "simple"
        elif complexity_score < 0.7:
            return "moderate"
        else:
            return "complex"
    
    def _calculate_ml_quality_score(self, df: pd.DataFrame) -> float:
        """Calculate ML-based quality score."""
        try:
            # Get quality metrics
            anomalies = self._detect_anomalies_advanced(df)
            distributions = self._analyze_distributions_advanced(df)
            patterns = self._detect_data_patterns(df)
            
            # Calculate component scores
            anomaly_score = self._calculate_anomaly_score(anomalies)
            distribution_score = self._calculate_distribution_score(distributions)
            pattern_score = self._calculate_pattern_score(patterns)
            
            # Weighted combination
            ml_quality_score = (
                anomaly_score * 0.4 +
                distribution_score * 0.3 +
                pattern_score * 0.3
            )
            
            return ml_quality_score
            
        except Exception as e:
            st.warning(f"⚠️ Could not calculate ML quality score: {str(e)}")
            return 0.5
    
    def _calculate_anomaly_score(self, anomalies):
        """Calculate score based on anomaly analysis."""
        if not anomalies:
            return 0.5
        
        total_outlier_percentage = 0
        valid_columns = 0
        
        for col, analysis in anomalies.items():
            if 'error' not in analysis:
                # Use consensus outliers for scoring
                consensus = analysis.get('consensus_outliers', {})
                outlier_pct = consensus.get('percentage', 0)
                total_outlier_percentage += outlier_pct
                valid_columns += 1
        
        if valid_columns == 0:
            return 0.5
        
        avg_outlier_percentage = total_outlier_percentage / valid_columns
        
        # Lower outlier percentage = higher quality
        return max(0, 1 - avg_outlier_percentage)
    
    def _calculate_distribution_score(self, distributions):
        """Calculate score based on distribution analysis."""
        if not distributions:
            return 0.5
        
        normality_scores = []
        valid_columns = 0
        
        for col, analysis in distributions.items():
            if 'error' not in analysis:
                # Check normality
                shapiro_test = analysis.get('normality_tests', {}).get('shapiro_wilk', {})
                if shapiro_test.get('is_normal', False):
                    normality_scores.append(1.0)
                else:
                    normality_scores.append(0.5)
                valid_columns += 1
        
        if valid_columns == 0:
            return 0.5
        
        return np.mean(normality_scores)
    
    def _calculate_pattern_score(self, patterns):
        """Calculate score based on pattern analysis."""
        if not patterns:
            return 0.5
        
        complexity_scores = []
        valid_columns = 0
        
        for col, analysis in patterns.items():
            if 'error' not in analysis:
                complexity = analysis.get('pattern_complexity', 'moderate')
                if complexity == 'simple':
                    complexity_scores.append(1.0)  # Simple patterns = good quality
                elif complexity == 'moderate':
                    complexity_scores.append(0.7)
                else:
                    complexity_scores.append(0.4)  # Complex patterns = potential issues
                valid_columns += 1
        
        if valid_columns == 0:
            return 0.5
        
        return np.mean(complexity_scores)
    
    def _generate_ml_recommendations(self, analysis: Dict, dataset_name: str) -> List[Dict]:
        """Generate ML-based recommendations."""
        recommendations = []
        
        # Anomaly-based recommendations
        anomalies = analysis.get('anomalies', {})
        for col, anomaly_data in anomalies.items():
            if 'error' not in anomaly_data:
                consensus = anomaly_data.get('consensus_outliers', {})
                outlier_pct = consensus.get('percentage', 0)
                
                if outlier_pct > 0.1:  # More than 10% outliers
                    recommendations.append({
                        'priority': 'High',
                        'title': f'Investigate Outliers in {col}',
                        'description': f'High outlier percentage ({outlier_pct:.1%}) detected by multiple methods',
                        'action': 'Review data collection process and business rules for this column',
                        'impact': 'Outliers can skew analysis and indicate data quality issues'
                    })
        
        # Distribution-based recommendations
        distributions = analysis.get('distributions', {})
        for col, dist_data in distributions.items():
            if 'error' not in dist_data:
                normality = dist_data.get('normality_tests', {}).get('shapiro_wilk', {})
                if not normality.get('is_normal', True):
                    recommendations.append({
                        'priority': 'Medium',
                        'title': f'Non-Normal Distribution in {col}',
                        'description': 'Data does not follow normal distribution',
                        'action': 'Consider using non-parametric statistical methods for analysis',
                        'impact': 'Statistical tests may need adjustment for non-normal data'
                    })
        
        # Pattern-based recommendations
        patterns = analysis.get('patterns', {})
        for col, pattern_data in patterns.items():
            if 'error' not in pattern_data:
                complexity = pattern_data.get('pattern_complexity', 'moderate')
                if complexity == 'complex':
                    recommendations.append({
                        'priority': 'Medium',
                        'title': f'Complex Patterns in {col}',
                        'description': 'Multiple patterns detected (clusters, trends, periodicity)',
                        'action': 'Consider segmenting data or using advanced modeling techniques',
                        'impact': 'Complex patterns may require specialized analysis approaches'
                    })
        
        return recommendations

    def get_anomaly_summary(self, df: pd.DataFrame) -> Dict:
        """Get a comprehensive summary of all anomalies in the dataset."""
        anomalies = self._detect_anomalies_advanced(df)
        
        # Calculate totals
        total_anomalies = 0
        anomaly_details = {}
        anomaly_summary = {
            'total_anomalies': 0,
            'columns_with_anomalies': 0,
            'anomaly_types': {
                'ml_outliers': 0,
                'statistical_outliers': 0,
                'iqr_outliers': 0,
                'consensus_outliers': 0
            },
            'anomaly_details': {},
            'recommendations': []
        }
        
        for col, col_anomalies in anomalies.items():
            if 'error' not in col_anomalies:
                col_total = 0
                col_details = {}
                
                # Count ML outliers
                if 'ml_outliers' in col_anomalies:
                    ml_count = col_anomalies['ml_outliers']['count']
                    col_total += ml_count
                    anomaly_summary['anomaly_types']['ml_outliers'] += ml_count
                    col_details['ml_outliers'] = {
                        'count': ml_count,
                        'percentage': col_anomalies['ml_outliers']['percentage'],
                        'indices': col_anomalies['ml_outliers']['indices'][:10]  # First 10 indices
                    }
                
                # Count statistical outliers
                if 'statistical_outliers' in col_anomalies:
                    stat_count = col_anomalies['statistical_outliers']['count']
                    col_total += stat_count
                    anomaly_summary['anomaly_types']['statistical_outliers'] += stat_count
                    col_details['statistical_outliers'] = {
                        'count': stat_count,
                        'percentage': col_anomalies['statistical_outliers']['percentage'],
                        'indices': col_anomalies['statistical_outliers']['indices'][:10]  # First 10 indices
                    }
                
                # Count IQR outliers
                if 'iqr_outliers' in col_anomalies:
                    iqr_count = col_anomalies['iqr_outliers']['count']
                    col_total += iqr_count
                    anomaly_summary['anomaly_types']['iqr_outliers'] += iqr_count
                    col_details['iqr_outliers'] = {
                        'count': iqr_count,
                        'percentage': col_anomalies['iqr_outliers']['percentage'],
                        'values': col_anomalies['iqr_outliers']['values'][:10]  # First 10 values
                    }
                
                # Count consensus outliers
                if 'consensus_outliers' in col_anomalies:
                    consensus_count = col_anomalies['consensus_outliers']['count']
                    col_total += consensus_count
                    anomaly_summary['anomaly_types']['consensus_outliers'] += consensus_count
                    col_details['consensus_outliers'] = {
                        'count': consensus_count,
                        'percentage': col_anomalies['consensus_outliers']['percentage'],
                        'indices': col_anomalies['consensus_outliers']['indices'][:10]  # First 10 indices
                    }
                
                if col_total > 0:
                    total_anomalies += col_total
                    anomaly_summary['columns_with_anomalies'] += 1
                    anomaly_summary['anomaly_details'][col] = {
                        'total_anomalies': col_total,
                        'details': col_details
                    }
                    
                    # Add recommendations based on anomaly severity
                    if col_total > len(df) * 0.1:  # More than 10% anomalies
                        anomaly_summary['recommendations'].append(f"Column '{col}' has high anomaly rate ({col_total} anomalies, {col_total/len(df)*100:.1f}%) - consider data quality review")
                    elif col_total > len(df) * 0.05:  # More than 5% anomalies
                        anomaly_summary['recommendations'].append(f"Column '{col}' has moderate anomaly rate ({col_total} anomalies, {col_total/len(df)*100:.1f}%) - monitor for data drift")
        
        anomaly_summary['total_anomalies'] = total_anomalies
        anomaly_summary['overall_anomaly_rate'] = total_anomalies / (len(df) * len(df.columns)) if len(df) > 0 and len(df.columns) > 0 else 0
        
        # Add overall recommendations
        if total_anomalies > 0:
            if anomaly_summary['overall_anomaly_rate'] > 0.1:
                anomaly_summary['recommendations'].append("High overall anomaly rate detected - comprehensive data quality review recommended")
            elif anomaly_summary['overall_anomaly_rate'] > 0.05:
                anomaly_summary['recommendations'].append("Moderate overall anomaly rate - implement data quality monitoring")
            else:
                anomaly_summary['recommendations'].append("Low anomaly rate - data quality appears good")
        else:
            anomaly_summary['recommendations'].append("No anomalies detected - excellent data quality")
        
        return anomaly_summary
