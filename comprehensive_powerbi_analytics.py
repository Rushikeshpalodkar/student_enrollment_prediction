"""
Comprehensive Power BI Analytics System
- Historical trends (5-8 years)
- Enrollment patterns by demographics
- Miss/match analysis for capacity planning
- Gender ratio analysis
- Major selection trends
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

print("=" * 70)
print("COMPREHENSIVE POWER BI ANALYTICS SYSTEM")
print("Historical Trends & Enrollment Analysis")
print("=" * 70)
print()

# Set random seed for reproducible data
np.random.seed(42)

# 1. Generate Historical Data (2018-2025)
print("1. GENERATING HISTORICAL ENROLLMENT DATA (2018-2025)...")
print("-" * 50)

historical_data = []
years = list(range(2018, 2026))  # 8 years of data
semesters = ['Fall', 'Spring', 'Summer']
majors = ['Computer Science', 'Business Administration', 'Engineering', 
          'Psychology', 'Biology', 'Mathematics', 'English Literature', 
          'Economics', 'Nursing', 'Art & Design']
genders = ['Male', 'Female', 'Other']
ethnicities = ['White', 'Asian', 'Hispanic', 'Black', 'Other']
schools = ['School of Engineering', 'Business School', 'Liberal Arts', 
           'Sciences', 'Nursing School']

student_id_counter = 1

for year in years:
    for semester in semesters:
        # Simulate enrollment growth/decline trends
        if year <= 2020:  # Pre-pandemic
            base_enrollment = 4500 + (year - 2018) * 200
        elif year <= 2022:  # Pandemic impact
            base_enrollment = 4200 - (year - 2020) * 300
        else:  # Recovery
            base_enrollment = 3600 + (year - 2022) * 400
        
        # Summer has lower enrollment
        if semester == 'Summer':
            base_enrollment = int(base_enrollment * 0.6)
        elif semester == 'Spring':
            base_enrollment = int(base_enrollment * 0.95)
        
        # Generate students for this semester
        num_students = int(np.random.normal(base_enrollment, base_enrollment * 0.1))
        
        for i in range(num_students):
            # Generate realistic demographic distributions
            gender = np.random.choice(genders, p=[0.45, 0.52, 0.03])
            
            # Major trends over time
            if year >= 2020:  # CS and Engineering growth
                major_probs = [0.25, 0.20, 0.18, 0.08, 0.07, 0.06, 0.04, 0.05, 0.05, 0.02]
            else:  # Earlier distribution
                major_probs = [0.15, 0.25, 0.15, 0.10, 0.08, 0.08, 0.06, 0.06, 0.05, 0.02]
            
            major = np.random.choice(majors, p=major_probs)
            
            # Gender bias in majors (realistic)
            if major in ['Engineering', 'Computer Science'] and gender == 'Female':
                if np.random.random() < 0.3:  # 30% chance to switch
                    major = np.random.choice(['Psychology', 'Biology', 'Business Administration'])
            elif major == 'Nursing' and gender == 'Male':
                if np.random.random() < 0.7:  # 70% chance to switch
                    major = np.random.choice(['Biology', 'Psychology', 'Business Administration'])
            
            # Map major to school
            school_mapping = {
                'Computer Science': 'School of Engineering',
                'Engineering': 'School of Engineering',
                'Business Administration': 'Business School',
                'Economics': 'Business School',
                'Psychology': 'Liberal Arts',
                'English Literature': 'Liberal Arts',
                'Biology': 'Sciences',
                'Mathematics': 'Sciences',
                'Nursing': 'Nursing School',
                'Art & Design': 'Liberal Arts'
            }
            school = school_mapping.get(major, 'Liberal Arts')
            
            age = int(np.random.normal(20, 2))
            age = max(17, min(30, age))  # Clamp age
            
            gpa = np.random.normal(3.2, 0.5)
            gpa = max(2.0, min(4.0, gpa))  # Clamp GPA
            
            ethnicity = np.random.choice(ethnicities, p=[0.40, 0.25, 0.20, 0.10, 0.05])
            
            # Financial aid (higher for certain demographics)
            financial_aid = False
            if ethnicity in ['Hispanic', 'Black'] or gpa > 3.5:
                financial_aid = np.random.random() < 0.6
            else:
                financial_aid = np.random.random() < 0.3
            
            student_record = {
                'student_id': f'STU{student_id_counter:06d}',
                'year': year,
                'semester': semester,
                'academic_year': f'{year}-{year+1}',
                'major': major,
                'school': school,
                'gender': gender,
                'age': age,
                'ethnicity': ethnicity,
                'gpa': round(gpa, 2),
                'financial_aid': financial_aid,
                'enrollment_status': 'Active',
                'credits_enrolled': np.random.choice([12, 15, 18], p=[0.2, 0.6, 0.2]),
                'residency': np.random.choice(['In-State', 'Out-of-State', 'International'], p=[0.7, 0.25, 0.05])
            }
            
            historical_data.append(student_record)
            student_id_counter += 1

df_historical = pd.DataFrame(historical_data)
print(f"   Generated {len(df_historical):,} historical student records")
print(f"   Years covered: {df_historical['year'].min()} - {df_historical['year'].max()}")
print(f"   Total unique students: {df_historical['student_id'].nunique():,}")
print()

# 2. Current Year Analysis (2025)
print("2. CURRENT YEAR (2025) ENROLLMENT ANALYSIS...")
print("-" * 50)

current_year = df_historical[df_historical['year'] == 2025].copy()
print(f"   Current year students: {len(current_year):,}")
print()

print("   Major Distribution (2025):")
major_dist_2025 = current_year['major'].value_counts()
for major, count in major_dist_2025.items():
    percentage = (count / len(current_year)) * 100
    print(f"   • {major}: {count:,} students ({percentage:.1f}%)")
print()

print("   Gender Distribution (2025):")
gender_dist_2025 = current_year['gender'].value_counts()
for gender, count in gender_dist_2025.items():
    percentage = (count / len(current_year)) * 100
    print(f"   • {gender}: {count:,} students ({percentage:.1f}%)")
print()

print("   School Distribution (2025):")
school_dist_2025 = current_year['school'].value_counts()
for school, count in school_dist_2025.items():
    percentage = (count / len(current_year)) * 100
    print(f"   • {school}: {count:,} students ({percentage:.1f}%)")
print()

# 3. Historical Trends Analysis
print("3. HISTORICAL TRENDS ANALYSIS (2018-2025)...")
print("-" * 50)

# Yearly enrollment trends
yearly_trends = df_historical.groupby('year').agg({
    'student_id': 'count',
    'gpa': 'mean',
    'age': 'mean'
}).round(2)
yearly_trends.columns = ['Total_Enrollment', 'Average_GPA', 'Average_Age']

print("   Yearly Enrollment Trends:")
for year, row in yearly_trends.iterrows():
    print(f"   • {year}: {row['Total_Enrollment']:,} students (Avg GPA: {row['Average_GPA']:.2f})")
print()

# Major trends over time
major_trends = df_historical.groupby(['year', 'major']).size().reset_index(name='enrollment')
print("   Top Growing Majors (2018 vs 2025):")
major_2018 = df_historical[df_historical['year'] == 2018]['major'].value_counts()
major_2025 = df_historical[df_historical['year'] == 2025]['major'].value_counts()

for major in majors:
    count_2018 = major_2018.get(major, 0)
    count_2025 = major_2025.get(major, 0)
    if count_2018 > 0:
        growth = ((count_2025 - count_2018) / count_2018) * 100
        print(f"   • {major}: {growth:+.1f}% growth ({count_2018} → {count_2025})")
print()

# 4. Miss/Match Capacity Analysis
print("4. CAPACITY MISS/MATCH ANALYSIS...")
print("-" * 50)

# Define capacity for each major/school
capacity_data = {
    'Computer Science': {'capacity': 800, 'current': 0, 'faculty': 25},
    'Business Administration': {'capacity': 1200, 'current': 0, 'faculty': 35},
    'Engineering': {'capacity': 700, 'current': 0, 'faculty': 30},
    'Psychology': {'capacity': 400, 'current': 0, 'faculty': 15},
    'Biology': {'capacity': 350, 'current': 0, 'faculty': 20},
    'Mathematics': {'capacity': 300, 'current': 0, 'faculty': 12},
    'English Literature': {'capacity': 250, 'current': 0, 'faculty': 10},
    'Economics': {'capacity': 300, 'current': 0, 'faculty': 12},
    'Nursing': {'capacity': 200, 'current': 0, 'faculty': 18},
    'Art & Design': {'capacity': 150, 'current': 0, 'faculty': 8}
}

# Calculate current enrollment vs capacity
current_enrollment = current_year['major'].value_counts()
capacity_analysis = []

print("   Capacity Analysis (2025):")
for major, data in capacity_data.items():
    current = current_enrollment.get(major, 0)
    capacity = data['capacity']
    utilization = (current / capacity) * 100
    shortage = max(0, current - capacity)
    surplus = max(0, capacity - current)
    
    status = "OVER CAPACITY" if current > capacity else "UNDER CAPACITY" if utilization < 80 else "OPTIMAL"
    
    capacity_analysis.append({
        'major': major,
        'capacity': capacity,
        'current_enrollment': current,
        'utilization_rate': utilization,
        'shortage': shortage,
        'surplus': surplus,
        'status': status,
        'faculty': data['faculty'],
        'student_faculty_ratio': round(current / data['faculty'], 1) if data['faculty'] > 0 else 0
    })
    
    print(f"   • {major}:")
    print(f"     - Capacity: {capacity}, Current: {current} ({utilization:.1f}% utilization)")
    print(f"     - Status: {status}")
    if shortage > 0:
        print(f"     - Shortage: {shortage} students")
    elif surplus > 0:
        print(f"     - Available spots: {surplus}")
    print(f"     - Student-Faculty Ratio: {current / data['faculty']:.1f}:1")
print()

# 5. Gender Analysis by Major
print("5. GENDER RATIO ANALYSIS BY MAJOR...")
print("-" * 50)

gender_by_major = current_year.groupby(['major', 'gender']).size().unstack(fill_value=0)
gender_analysis = []

print("   Gender Distribution by Major (2025):")
for major in majors:
    major_data = current_year[current_year['major'] == major]
    if len(major_data) > 0:
        male_count = len(major_data[major_data['gender'] == 'Male'])
        female_count = len(major_data[major_data['gender'] == 'Female'])
        other_count = len(major_data[major_data['gender'] == 'Other'])
        total = male_count + female_count + other_count
        
        male_pct = (male_count / total) * 100 if total > 0 else 0
        female_pct = (female_count / total) * 100 if total > 0 else 0
        
        gender_analysis.append({
            'major': major,
            'male_count': male_count,
            'female_count': female_count,
            'other_count': other_count,
            'male_percentage': male_pct,
            'female_percentage': female_pct,
            'gender_ratio': f"{male_count}:{female_count}" if female_count > 0 else f"{male_count}:0"
        })
        
        print(f"   • {major}: {male_count}M/{female_count}F ({male_pct:.1f}%M/{female_pct:.1f}%F)")

print()

# 6. Save all data for Power BI
print("6. GENERATING POWER BI DATASETS...")
print("-" * 50)

# Historical enrollment data
df_historical.to_csv('powerbi_historical_enrollment.csv', index=False)
print("   ✓ Saved: powerbi_historical_enrollment.csv")

# Current year analysis
current_year.to_csv('powerbi_current_year_2025.csv', index=False)
print("   ✓ Saved: powerbi_current_year_2025.csv")

# Capacity analysis
pd.DataFrame(capacity_analysis).to_csv('powerbi_capacity_analysis.csv', index=False)
print("   ✓ Saved: powerbi_capacity_analysis.csv")

# Gender analysis
pd.DataFrame(gender_analysis).to_csv('powerbi_gender_analysis.csv', index=False)
print("   ✓ Saved: powerbi_gender_analysis.csv")

# Yearly trends summary
yearly_trends.to_csv('powerbi_yearly_trends.csv', index=True)
print("   ✓ Saved: powerbi_yearly_trends.csv")

# Major trends over time
major_trends.to_csv('powerbi_major_trends_timeline.csv', index=False)
print("   ✓ Saved: powerbi_major_trends_timeline.csv")

print()

# 7. Executive Summary Metrics
print("7. EXECUTIVE SUMMARY METRICS...")
print("-" * 50)

executive_metrics = {
    'total_students_2025': len(current_year),
    'total_historical_records': len(df_historical),
    'years_of_data': len(years),
    'growth_rate_2024_2025': ((len(df_historical[df_historical['year'] == 2025]) - 
                               len(df_historical[df_historical['year'] == 2024])) / 
                              len(df_historical[df_historical['year'] == 2024])) * 100,
    'average_gpa_2025': current_year['gpa'].mean(),
    'gender_diversity_index': min(gender_dist_2025) / max(gender_dist_2025),  # Closer to 1 is more diverse
    'majors_over_capacity': sum(1 for ca in capacity_analysis if ca['status'] == 'OVER CAPACITY'),
    'majors_under_capacity': sum(1 for ca in capacity_analysis if ca['status'] == 'UNDER CAPACITY'),
    'total_capacity_shortage': sum(ca['shortage'] for ca in capacity_analysis),
    'fastest_growing_major': major_2025.index[0],
    'male_percentage': (gender_dist_2025.get('Male', 0) / len(current_year)) * 100,
    'female_percentage': (gender_dist_2025.get('Female', 0) / len(current_year)) * 100
}

print("   KEY EXECUTIVE METRICS (2025):")
print(f"   • Total Current Students: {executive_metrics['total_students_2025']:,}")
print(f"   • Year-over-Year Growth: {executive_metrics['growth_rate_2024_2025']:+.1f}%")
print(f"   • Average GPA: {executive_metrics['average_gpa_2025']:.2f}")
print(f"   • Gender Split: {executive_metrics['female_percentage']:.1f}%F / {executive_metrics['male_percentage']:.1f}%M")
print(f"   • Majors Over Capacity: {executive_metrics['majors_over_capacity']}")
print(f"   • Total Capacity Shortage: {executive_metrics['total_capacity_shortage']} students")
print(f"   • Fastest Growing Major: {executive_metrics['fastest_growing_major']}")

# Save executive metrics
with open('powerbi_executive_metrics.json', 'w') as f:
    json.dump(executive_metrics, f, indent=2)
print("   ✓ Saved: powerbi_executive_metrics.json")

print()
print("=" * 70)
print("POWER BI ANALYTICS GENERATION COMPLETED!")
print("=" * 70)
print()
print("📊 Generated Datasets:")
print("• powerbi_historical_enrollment.csv - 8 years of student data")
print("• powerbi_current_year_2025.csv - Current year detailed analysis")
print("• powerbi_capacity_analysis.csv - Miss/match capacity planning")
print("• powerbi_gender_analysis.csv - Gender ratios by major")
print("• powerbi_yearly_trends.csv - Historical trends summary")
print("• powerbi_major_trends_timeline.csv - Major popularity over time")
print("• powerbi_executive_metrics.json - Key performance indicators")
print()
print("🎯 Key Insights:")
print(f"• {len(df_historical):,} total student records across 8 years")
print(f"• {executive_metrics['majors_over_capacity']} majors are over capacity")
print(f"• {executive_metrics['total_capacity_shortage']} student shortage overall")
print(f"• Gender ratio: {executive_metrics['female_percentage']:.1f}%F / {executive_metrics['male_percentage']:.1f}%M")
print(f"• {executive_metrics['fastest_growing_major']} is the fastest growing major")
print()
print("✅ Ready for Power BI import and dashboard creation!")
print("✅ All requested analytics completed: trends, demographics, capacity analysis")