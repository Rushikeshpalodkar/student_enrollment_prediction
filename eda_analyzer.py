import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class EDAAnalyzer:
    def __init__(self):
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
    def basic_statistics(self, df):
        """Generate basic statistics about the dataset"""
        print("=== BASIC DATASET STATISTICS ===")
        print(f"Total records: {len(df):,}")
        print(f"Unique students: {df['student_id'].nunique():,}")
        print(f"Unique majors: {df['major'].nunique()}")
        print(f"Unique classes: {df['class_name'].nunique()}")
        print(f"Semesters covered: {df['semester'].min()} to {df['semester'].max()}")
        print(f"Years covered: {df['year'].min()} to {df['year'].max()}")
        
        print("\n=== NUMERICAL FEATURES SUMMARY ===")
        numerical_cols = ['age', 'gpa', 'grade', 'credits']
        print(df[numerical_cols].describe())
        
        print("\n=== MAJOR DISTRIBUTION ===")
        major_counts = df['major'].value_counts()
        print(major_counts)
        
        return {
            'total_records': len(df),
            'unique_students': df['student_id'].nunique(),
            'unique_majors': df['major'].nunique(),
            'unique_classes': df['class_name'].nunique(),
            'major_distribution': major_counts
        }
    
    def plot_major_distribution(self, df, save_path=None):
        """Plot distribution of majors"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Bar plot
        major_counts = df['major'].value_counts()
        ax1.bar(range(len(major_counts)), major_counts.values)
        ax1.set_title('Distribution of Majors')
        ax1.set_xlabel('Major')
        ax1.set_ylabel('Number of Enrollments')
        ax1.set_xticks(range(len(major_counts)))
        ax1.set_xticklabels(major_counts.index, rotation=45, ha='right')
        
        # Pie chart
        ax2.pie(major_counts.values, labels=major_counts.index, autopct='%1.1f%%')
        ax2.set_title('Major Distribution (Percentage)')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_gpa_grade_relationship(self, df, save_path=None):
        """Plot relationship between student GPA and individual grades"""
        plt.figure(figsize=(12, 8))
        
        # Scatter plot with regression line
        sns.scatterplot(data=df, x='gpa', y='grade', hue='major', alpha=0.6)
        sns.regplot(data=df, x='gpa', y='grade', scatter=False, color='red')
        
        plt.title('Relationship between Student GPA and Individual Class Grades')
        plt.xlabel('Student Overall GPA')
        plt.ylabel('Individual Class Grade')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        correlation = df['gpa'].corr(df['grade'])
        plt.text(0.05, 0.95, f'Correlation: {correlation:.3f}', 
                transform=plt.gca().transAxes, fontsize=12, 
                bbox=dict(boxstyle="round", facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_enrollment_trends(self, df, save_path=None):
        """Plot enrollment trends over time"""
        # Enrollment by semester and major
        enrollment_trends = df.groupby(['year', 'semester_type', 'major']).size().reset_index(name='enrollments')
        
        fig = px.line(enrollment_trends, x='year', y='enrollments', 
                     color='major', facet_col='semester_type',
                     title='Enrollment Trends by Major and Semester')
        
        if save_path:
            fig.write_html(save_path)
        fig.show()
    
    def plot_class_popularity(self, df, top_n=20, save_path=None):
        """Plot most popular classes"""
        class_counts = df['class_name'].value_counts().head(top_n)
        
        plt.figure(figsize=(12, 8))
        ax = class_counts.plot(kind='barh')
        plt.title(f'Top {top_n} Most Popular Classes')
        plt.xlabel('Number of Enrollments')
        plt.ylabel('Class Name')
        
        # Add value labels on bars
        for i, v in enumerate(class_counts.values):
            ax.text(v + 10, i, str(v), va='center')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_grade_distribution_by_major(self, df, save_path=None):
        """Plot grade distribution by major"""
        plt.figure(figsize=(14, 8))
        
        # Box plot
        sns.boxplot(data=df, x='major', y='grade')
        plt.title('Grade Distribution by Major')
        plt.xlabel('Major')
        plt.ylabel('Grade')
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_correlation_matrix(self, df, save_path=None):
        """Plot correlation matrix of numerical features"""
        numerical_cols = ['age', 'gpa', 'grade', 'credits', 'semester']
        corr_matrix = df[numerical_cols].corr()
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, fmt='.3f')
        plt.title('Correlation Matrix of Numerical Features')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_interactive_dashboard(self, df, save_path='eda_dashboard.html'):
        """Generate an interactive dashboard with multiple visualizations"""
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Major Distribution', 'GPA vs Grade', 
                          'Enrollment Trends', 'Grade Distribution'),
            specs=[[{"type": "pie"}, {"type": "scatter"}],
                   [{"type": "scatter"}, {"type": "box"}]]
        )
        
        # Major distribution pie chart
        major_counts = df['major'].value_counts()
        fig.add_trace(
            go.Pie(labels=major_counts.index, values=major_counts.values,
                  name="Major Distribution"),
            row=1, col=1
        )
        
        # GPA vs Grade scatter plot
        fig.add_trace(
            go.Scatter(x=df['gpa'], y=df['grade'], mode='markers',
                      text=df['major'], name="GPA vs Grade",
                      marker=dict(opacity=0.6)),
            row=1, col=2
        )
        
        # Enrollment trends
        enrollment_by_semester = df.groupby('semester').size().reset_index(name='count')
        fig.add_trace(
            go.Scatter(x=enrollment_by_semester['semester'], 
                      y=enrollment_by_semester['count'],
                      mode='lines+markers', name="Enrollment Trends"),
            row=2, col=1
        )
        
        # Grade distribution by major (box plot)
        for major in df['major'].unique()[:5]:  # Show top 5 majors
            major_data = df[df['major'] == major]
            fig.add_trace(
                go.Box(y=major_data['grade'], name=major),
                row=2, col=2
            )
        
        fig.update_layout(height=800, showlegend=True,
                         title_text="Student Enrollment Data Analysis Dashboard")
        
        if save_path:
            fig.write_html(save_path)
        fig.show()
        
        return fig
    
    def analyze_major_switching(self, df):
        """Analyze patterns in major switching"""
        # Track major changes per student
        df_sorted = df.sort_values(['student_id', 'semester'])
        df_sorted['major_changed'] = df_sorted.groupby('student_id')['major'].transform(
            lambda x: x != x.shift()
        )
        
        # Students who changed majors
        major_switchers = df_sorted.groupby('student_id')['major_changed'].sum()
        switch_stats = major_switchers.value_counts().sort_index()
        
        print("=== MAJOR SWITCHING ANALYSIS ===")
        print("Number of major changes per student:")
        print(switch_stats)
        
        # Most common major switches
        df_switches = df_sorted[df_sorted['major_changed'] == True].copy()
        df_switches['prev_major'] = df_switches.groupby('student_id')['major'].shift(1)
        df_switches = df_switches.dropna(subset=['prev_major'])
        
        switch_patterns = df_switches.groupby(['prev_major', 'major']).size().reset_index(name='count')
        switch_patterns = switch_patterns.sort_values('count', ascending=False).head(10)
        
        print("\nMost common major switches:")
        print(switch_patterns)
        
        return switch_stats, switch_patterns

if __name__ == "__main__":
    # Test the EDA analyzer
    analyzer = EDAAnalyzer()
    
    # Load sample data
    df = pd.read_csv('student_enrollment_data.csv')
    
    # Run basic statistics
    stats = analyzer.basic_statistics(df)
    
    # Generate plots
    analyzer.plot_major_distribution(df, 'major_distribution.png')
    analyzer.plot_gpa_grade_relationship(df, 'gpa_grade_relationship.png')
    analyzer.plot_class_popularity(df, save_path='class_popularity.png')
    analyzer.plot_grade_distribution_by_major(df, 'grade_by_major.png')
    analyzer.plot_correlation_matrix(df, 'correlation_matrix.png')
    
    # Analyze major switching
    switch_stats, switch_patterns = analyzer.analyze_major_switching(df)
    
    # Generate interactive dashboard
    analyzer.generate_interactive_dashboard(df, 'eda_dashboard.html')