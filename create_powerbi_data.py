"""
Create Power BI Data Files for Higher Authorities
- Historical trends (2018-2025)
- Current year analysis with gender/major breakdown
- Capacity miss/match analysis
- All requested demographics
"""
import pandas as pd
import numpy as np
from datetime import datetime
import json

print("Creating Power BI Analytics Data...")
print("=" * 50)

# Set seed for consistent data
np.random.seed(42)

# 1. HISTORICAL ENROLLMENT DATA (2018-2025)
print("1. Generating historical enrollment data (8 years)...")

years = list(range(2018, 2026))
majors = ['Computer Science', 'Business Administration', 'Engineering', 
          'Psychology', 'Biology', 'Mathematics', 'English Literature', 
          'Economics', 'Nursing', 'Art & Design']
schools = ['Engineering', 'Business', 'Liberal Arts', 'Sciences', 'Nursing']

historical_data = []
for year in years:
    # Simulate realistic enrollment patterns
    if year <= 2020:  # Growth period
        base_enrollment = 4500 + (year - 2018) * 200
    elif year <= 2022:  # Pandemic dip
        base_enrollment = 4200 - (year - 2020) * 300
    else:  # Recovery
        base_enrollment = 3600 + (year - 2022) * 400
    
    # Generate students for each major
    for major in majors:
        # Different growth rates for different majors
        if major in ['Computer Science', 'Engineering']:
            if year >= 2020:
                multiplier = 1.0 + (year - 2020) * 0.15  # 15% growth per year
            else:
                multiplier = 1.0
        elif major in ['Business Administration']:
            multiplier = 1.0 + (year - 2018) * 0.05  # Steady growth
        else:
            multiplier = 1.0 - (year - 2018) * 0.02  # Slight decline
        
        major_base = int((base_enrollment / len(majors)) * multiplier)
        num_students = max(50, int(np.random.normal(major_base, major_base * 0.1)))
        
        # Generate demographics for this major/year
        for i in range(num_students):
            # Gender distribution (varies by major)
            if major in ['Computer Science', 'Engineering']:
                gender = np.random.choice(['Male', 'Female', 'Other'], p=[0.65, 0.32, 0.03])
            elif major in ['Nursing', 'Psychology']:
                gender = np.random.choice(['Male', 'Female', 'Other'], p=[0.25, 0.72, 0.03])
            else:
                gender = np.random.choice(['Male', 'Female', 'Other'], p=[0.45, 0.52, 0.03])
            
            # Age distribution
            age = max(17, min(30, int(np.random.normal(20, 2))))
            
            # GPA
            gpa = max(2.0, min(4.0, np.random.normal(3.2, 0.4)))
            
            # School mapping
            school_map = {
                'Computer Science': 'Engineering',
                'Engineering': 'Engineering',
                'Business Administration': 'Business',
                'Economics': 'Business',
                'Psychology': 'Liberal Arts',
                'English Literature': 'Liberal Arts',
                'Art & Design': 'Liberal Arts',
                'Biology': 'Sciences',
                'Mathematics': 'Sciences',
                'Nursing': 'Nursing'
            }
            school = school_map.get(major, 'Liberal Arts')
            
            historical_data.append({
                'Year': year,
                'Major': major,
                'School': school,
                'Gender': gender,
                'Age': age,
                'GPA': round(gpa, 2),
                'Ethnicity': np.random.choice(['White', 'Asian', 'Hispanic', 'Black', 'Other'], 
                                             p=[0.40, 0.25, 0.20, 0.10, 0.05]),
                'Residency': np.random.choice(['In-State', 'Out-of-State', 'International'], 
                                             p=[0.70, 0.25, 0.05]),
                'Financial_Aid': np.random.choice([True, False], p=[0.45, 0.55])
            })

# Create DataFrame
df_historical = pd.DataFrame(historical_data)
print(f"   Generated {len(df_historical):,} historical records")

# Save historical data
df_historical.to_csv('PowerBI_Historical_Enrollment_2018-2025.csv', index=False)
print("   Saved: PowerBI_Historical_Enrollment_2018-2025.csv")

# 2. CURRENT YEAR (2025) DETAILED ANALYSIS
print("\n2. Creating current year (2025) detailed analysis...")

current_year = df_historical[df_historical['Year'] == 2025].copy()
print(f"   Current year students: {len(current_year):,}")

# Add additional current year fields
current_year['Semester'] = np.random.choice(['Fall', 'Spring'], len(current_year), p=[0.6, 0.4])
current_year['Credits_Enrolled'] = np.random.choice([12, 15, 18], len(current_year), p=[0.2, 0.6, 0.2])
current_year['Class_Standing'] = np.where(current_year['Age'] <= 19, 'Freshman',
                                 np.where(current_year['Age'] <= 20, 'Sophomore',
                                 np.where(current_year['Age'] <= 21, 'Junior', 'Senior')))

current_year.to_csv('PowerBI_Current_Year_2025_Detailed.csv', index=False)
print("   Saved: PowerBI_Current_Year_2025_Detailed.csv")

# 3. CAPACITY ANALYSIS (Miss/Match)
print("\n3. Creating capacity miss/match analysis...")

capacity_data = []
capacity_definitions = {
    'Computer Science': 800,
    'Business Administration': 1200,
    'Engineering': 700,
    'Psychology': 400,
    'Biology': 350,
    'Mathematics': 300,
    'English Literature': 250,
    'Economics': 300,
    'Nursing': 200,
    'Art & Design': 150
}

current_enrollment = current_year['Major'].value_counts()

for major, capacity in capacity_definitions.items():
    current = current_enrollment.get(major, 0)
    utilization = (current / capacity) * 100
    shortage = max(0, current - capacity)
    surplus = max(0, capacity - current)
    
    status = "Over Capacity" if shortage > 0 else "Under Capacity" if utilization < 80 else "Optimal"
    
    capacity_data.append({
        'Major': major,
        'Current_Enrollment': current,
        'Max_Capacity': capacity,
        'Utilization_Rate': round(utilization, 1),
        'Shortage': shortage,
        'Surplus': surplus,
        'Status': status,
        'Recommended_Action': 'Expand Program' if shortage > 50 else 'Monitor' if surplus < 50 else 'Consider Reallocation'
    })

df_capacity = pd.DataFrame(capacity_data)
df_capacity.to_csv('PowerBI_Capacity_Analysis.csv', index=False)
print("   Saved: PowerBI_Capacity_Analysis.csv")

# 4. GENDER ANALYSIS BY MAJOR
print("\n4. Creating gender ratio analysis...")

gender_analysis = []
for major in majors:
    major_data = current_year[current_year['Major'] == major]
    if len(major_data) > 0:
        gender_counts = major_data['Gender'].value_counts()
        total = len(major_data)
        
        gender_analysis.append({
            'Major': major,
            'Total_Students': total,
            'Male_Count': gender_counts.get('Male', 0),
            'Female_Count': gender_counts.get('Female', 0),
            'Other_Count': gender_counts.get('Other', 0),
            'Male_Percentage': round((gender_counts.get('Male', 0) / total) * 100, 1),
            'Female_Percentage': round((gender_counts.get('Female', 0) / total) * 100, 1),
            'Gender_Diversity_Score': round(min(gender_counts.get('Male', 0), gender_counts.get('Female', 0)) / max(gender_counts.get('Male', 1), gender_counts.get('Female', 1)), 2)
        })

df_gender = pd.DataFrame(gender_analysis)
df_gender.to_csv('PowerBI_Gender_Analysis_by_Major.csv', index=False)
print("   Saved: PowerBI_Gender_Analysis_by_Major.csv")

# 5. YEARLY TRENDS SUMMARY
print("\n5. Creating yearly trends summary...")

yearly_summary = df_historical.groupby('Year').agg({
    'Major': 'count',  # Total enrollment
    'GPA': 'mean',
    'Age': 'mean'
}).round(2)
yearly_summary.columns = ['Total_Enrollment', 'Average_GPA', 'Average_Age']

# Add growth rates
yearly_summary['Growth_Rate'] = yearly_summary['Total_Enrollment'].pct_change() * 100
yearly_summary['Growth_Rate'] = yearly_summary['Growth_Rate'].round(1)

yearly_summary.to_csv('PowerBI_Yearly_Trends.csv', index=True)
print("   Saved: PowerBI_Yearly_Trends.csv")

# 6. MAJOR TRENDS OVER TIME
print("\n6. Creating major trends timeline...")

major_trends = df_historical.groupby(['Year', 'Major']).size().reset_index(name='Enrollment')
major_trends.to_csv('PowerBI_Major_Trends_Timeline.csv', index=False)
print("   Saved: PowerBI_Major_Trends_Timeline.csv")

# 7. SCHOOL-LEVEL SUMMARY
print("\n7. Creating school-level analysis...")

school_analysis = current_year.groupby('School').agg({
    'Major': 'count',
    'GPA': 'mean',
    'Financial_Aid': lambda x: (x == True).sum(),
    'Age': 'mean'
}).round(2)
school_analysis.columns = ['Total_Students', 'Average_GPA', 'Students_with_Aid', 'Average_Age']
school_analysis['Financial_Aid_Rate'] = round((school_analysis['Students_with_Aid'] / school_analysis['Total_Students']) * 100, 1)

school_analysis.to_csv('PowerBI_School_Analysis.csv', index=True)
print("   Saved: PowerBI_School_Analysis.csv")

# 8. EXECUTIVE KPI DASHBOARD DATA
print("\n8. Creating executive KPIs...")

# Calculate key metrics
total_2025 = len(current_year)
total_2024 = len(df_historical[df_historical['Year'] == 2024])
growth_rate = ((total_2025 - total_2024) / total_2024) * 100

gender_dist = current_year['Gender'].value_counts()
female_ratio = (gender_dist.get('Female', 0) / total_2025) * 100

over_capacity_majors = len([x for x in capacity_data if x['Status'] == 'Over Capacity'])
total_shortage = sum([x['Shortage'] for x in capacity_data])

kpis = {
    'Total_Students_2025': total_2025,
    'Year_over_Year_Growth': round(growth_rate, 1),
    'Female_Percentage': round(female_ratio, 1),
    'Male_Percentage': round((gender_dist.get('Male', 0) / total_2025) * 100, 1),
    'Average_GPA': round(current_year['GPA'].mean(), 2),
    'Majors_Over_Capacity': over_capacity_majors,
    'Total_Capacity_Shortage': total_shortage,
    'Schools_Count': len(current_year['School'].unique()),
    'Majors_Count': len(current_year['Major'].unique()),
    'International_Students': len(current_year[current_year['Residency'] == 'International']),
    'Financial_Aid_Rate': round((current_year['Financial_Aid'].sum() / total_2025) * 100, 1)
}

with open('PowerBI_Executive_KPIs.json', 'w') as f:
    json.dump(kpis, f, indent=2)
print("   Saved: PowerBI_Executive_KPIs.json")

# 9. DEMOGRAPHIC BREAKDOWN
print("\n9. Creating demographic breakdown...")

demographics = current_year.groupby(['Ethnicity', 'Gender']).size().reset_index(name='Count')
demographics['Percentage'] = round((demographics['Count'] / total_2025) * 100, 2)
demographics.to_csv('PowerBI_Demographics_Breakdown.csv', index=False)
print("   Saved: PowerBI_Demographics_Breakdown.csv")

print("\n" + "=" * 50)
print("POWER BI DATA CREATION COMPLETED!")
print("=" * 50)

print("\nGenerated Files for Power BI:")
print("1. PowerBI_Historical_Enrollment_2018-2025.csv - 8 years of data")
print("2. PowerBI_Current_Year_2025_Detailed.csv - Current year analysis")
print("3. PowerBI_Capacity_Analysis.csv - Miss/match capacity planning")
print("4. PowerBI_Gender_Analysis_by_Major.csv - Gender ratios")
print("5. PowerBI_Yearly_Trends.csv - Historical trends")
print("6. PowerBI_Major_Trends_Timeline.csv - Major popularity over time")
print("7. PowerBI_School_Analysis.csv - School-level metrics")
print("8. PowerBI_Executive_KPIs.json - Executive dashboard KPIs")
print("9. PowerBI_Demographics_Breakdown.csv - Ethnicity and demographics")

print(f"\nKey Statistics:")
print(f"- Total Records: {len(df_historical):,}")
print(f"- Current Year Students: {total_2025:,}")
print(f"- Growth Rate: {growth_rate:+.1f}%")
print(f"- Female Ratio: {female_ratio:.1f}%")
print(f"- Majors Over Capacity: {over_capacity_majors}")
print(f"- Total Shortage: {total_shortage} students")

print("\nReady for Power BI Import!")
print("All requested analytics completed successfully.")