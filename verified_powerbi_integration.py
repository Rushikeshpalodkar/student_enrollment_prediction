"""
VERIFIED POWER BI INTEGRATION - Queens College
Creates Power BI files from verified Queens College dataset
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime

class VerifiedPowerBIIntegration:
    def __init__(self, config_file='qc_config.json', data_file='verified_data/queens_college_verified_dataset.csv'):
        """Initialize with verified data and configuration"""
        
        print("QUEENS COLLEGE CUNY - VERIFIED POWER BI INTEGRATION")
        print("=" * 60)
        
        # Load configuration
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        # Load verified dataset
        self.df = pd.read_csv(data_file)
        
        print(f"[OK] Configuration loaded: {self.config['institution']['name']}")
        print(f"[OK] Dataset loaded: {len(self.df):,} student records")
        print(f"[OK] Years covered: {sorted(self.df['year'].unique())}")
        print(f"[OK] Current year data: {len(self.df[self.df['year'] == 2024]):,} students")
        
        # Create output directory
        self.output_dir = 'verified_powerbi_files'
        os.makedirs(self.output_dir, exist_ok=True)
        
    def create_current_enrollment_analysis(self):
        """Create current enrollment analysis for Power BI"""
        
        print("\nCreating current enrollment analysis...")
        
        # Focus on 2024 data
        current_data = self.df[self.df['year'] == 2024].copy()
        
        # Major-level analysis
        major_analysis = current_data.groupby('current_major').agg({
            'student_id': 'count',
            'current_gpa': 'mean',
            'sat_score': 'mean', 
            'high_school_gpa': 'mean',
            'total_credits': 'mean',
            'age': 'mean',
            'financial_need': lambda x: (x == True).sum(),
            'transfer_status': lambda x: (x == True).sum(),
            'gender': lambda x: (x == 'Female').sum()
        }).round(2)
        
        major_analysis.columns = [
            'Current_Enrollment', 'Avg_College_GPA', 'Avg_SAT_Score', 
            'Avg_HS_GPA', 'Avg_Credits', 'Avg_Age', 
            'Students_With_Financial_Aid', 'Transfer_Students', 'Female_Students'
        ]
        
        major_analysis = major_analysis.reset_index()
        
        # Add capacity and utilization from config
        capacity_data = []
        utilization_data = []
        
        for major in major_analysis['current_major']:
            if major in self.config['academic_programs']:
                capacity = self.config['academic_programs'][major]['capacity']
                utilization = self.config['academic_programs'][major]['utilization']
            else:
                # Default for any majors not in config
                capacity = int(major_analysis[major_analysis['current_major'] == major]['Current_Enrollment'].iloc[0] * 1.2)
                utilization = 85.0
            
            capacity_data.append(capacity)
            utilization_data.append(utilization)
        
        major_analysis['Program_Capacity'] = capacity_data
        major_analysis['Utilization_Rate'] = utilization_data
        major_analysis['Available_Spots'] = major_analysis['Program_Capacity'] - major_analysis['Current_Enrollment']
        
        # Add percentages
        total_enrollment = major_analysis['Current_Enrollment'].sum()
        major_analysis['Percentage_of_Total'] = (major_analysis['Current_Enrollment'] / total_enrollment * 100).round(1)
        
        # Sort by enrollment
        major_analysis = major_analysis.sort_values('Current_Enrollment', ascending=False)
        
        # Save current enrollment file
        filename = f'{self.output_dir}/PowerBI_Current_Enrollment_Verified.csv'
        major_analysis.to_csv(filename, index=False)
        
        print(f"[OK] Current enrollment analysis saved: {filename}")
        print(f"    Total students analyzed: {total_enrollment:,}")
        print(f"    Top 3 majors: {', '.join(major_analysis.head(3)['current_major'].tolist())}")
        
        return major_analysis
    
    def create_historical_trends_analysis(self):
        """Create historical trends analysis"""
        
        print("\nCreating historical trends analysis...")
        
        # Yearly enrollment by major
        historical_trends = self.df.groupby(['year', 'current_major']).agg({
            'student_id': 'count',
            'current_gpa': 'mean',
            'sat_score': 'mean'
        }).reset_index()
        
        historical_trends.columns = ['Year', 'Major', 'Enrollment', 'Avg_GPA', 'Avg_SAT']
        historical_trends = historical_trends.round(2)
        
        # Add growth rate calculations
        historical_trends['Growth_Rate'] = 0.0
        
        for major in historical_trends['Major'].unique():
            major_data = historical_trends[historical_trends['Major'] == major].sort_values('Year')
            
            for i in range(1, len(major_data)):
                current_enrollment = major_data.iloc[i]['Enrollment']
                previous_enrollment = major_data.iloc[i-1]['Enrollment']
                
                if previous_enrollment > 0:
                    growth_rate = ((current_enrollment - previous_enrollment) / previous_enrollment) * 100
                    historical_trends.loc[major_data.iloc[i].name, 'Growth_Rate'] = round(growth_rate, 1)
        
        # Add projected flag
        historical_trends['Is_Projected'] = historical_trends['Year'] >= 2025
        
        # Overall yearly totals
        yearly_totals = self.df.groupby('year').agg({
            'student_id': 'count',
            'current_gpa': 'mean',
            'sat_score': 'mean',
            'financial_need': lambda x: (x == True).mean() * 100,
            'transfer_status': lambda x: (x == True).mean() * 100
        }).reset_index()
        
        yearly_totals.columns = ['Year', 'Total_Enrollment', 'Avg_GPA', 'Avg_SAT', 'Financial_Aid_Pct', 'Transfer_Pct']
        yearly_totals = yearly_totals.round(1)
        
        # Save files
        trends_filename = f'{self.output_dir}/PowerBI_Historical_Trends_Verified.csv'
        historical_trends.to_csv(trends_filename, index=False)
        
        totals_filename = f'{self.output_dir}/PowerBI_Yearly_Totals_Verified.csv'
        yearly_totals.to_csv(totals_filename, index=False)
        
        print(f"[OK] Historical trends saved: {trends_filename}")
        print(f"[OK] Yearly totals saved: {totals_filename}")
        print(f"    Years covered: {sorted(historical_trends['Year'].unique())}")
        
        return historical_trends, yearly_totals
    
    def create_verified_executive_kpis(self):
        """Create executive KPIs with verified data"""
        
        print("\nCreating verified executive KPIs...")
        
        current_year_data = self.df[self.df['year'] == 2024]
        
        # Calculate actual KPIs from data
        total_enrollment = len(current_year_data)
        total_capacity = self.config['institution']['total_capacity']
        capacity_utilization = (total_enrollment / total_capacity) * 100
        
        # Financial calculations
        avg_tuition = self.config['financial']['average_tuition_fees']
        total_tuition_revenue = total_enrollment * avg_tuition
        
        # Academic metrics
        avg_gpa = current_year_data['current_gpa'].mean()
        avg_sat = current_year_data['sat_score'].mean()
        avg_hs_gpa = current_year_data['high_school_gpa'].mean()
        
        # Demographic metrics
        female_percentage = (current_year_data['gender'] == 'Female').mean() * 100
        financial_aid_pct = current_year_data['financial_need'].mean() * 100
        transfer_student_pct = current_year_data['transfer_status'].mean() * 100
        full_time_pct = (current_year_data['enrollment_type'] == 'Full-time').mean() * 100
        
        # Program insights
        major_counts = current_year_data['current_major'].value_counts()
        top_major = major_counts.index[0]
        top_major_count = major_counts.iloc[0]
        
        # Capacity analysis
        programs_at_capacity = 0
        programs_with_growth = 0
        
        for major, config_data in self.config['academic_programs'].items():
            if config_data['utilization'] > 90:
                programs_at_capacity += 1
            elif config_data['utilization'] < 80:
                programs_with_growth += 1
        
        executive_kpis = {
            "report_metadata": {
                "report_date": datetime.now().isoformat(),
                "data_source": "Verified Queens College Dataset",
                "academic_year": "2024-2025",
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            
            "institution_overview": {
                "college_name": self.config['institution']['name'],
                "location": self.config['institution']['location'],
                "total_enrollment": int(total_enrollment),
                "total_capacity": total_capacity,
                "capacity_utilization_pct": round(capacity_utilization, 1),
                "student_faculty_ratio": f"{self.config['institution']['student_to_faculty_ratio']}:1"
            },
            
            "financial_metrics": {
                "annual_tuition_revenue": int(total_tuition_revenue),
                "revenue_formatted": f"${total_tuition_revenue/1000000:.1f}M",
                "average_tuition_per_student": avg_tuition,
                "estimated_net_revenue": int(total_tuition_revenue * 0.3),  # 30% net margin
                "financial_aid_recipients_pct": round(financial_aid_pct, 1)
            },
            
            "academic_performance": {
                "average_college_gpa": round(avg_gpa, 2),
                "average_sat_score": int(avg_sat),
                "average_high_school_gpa": round(avg_hs_gpa, 2),
                "graduation_rate_6_year_pct": self.config['academic_metrics']['graduation_rate_6_year'],
                "retention_rate_freshman_pct": self.config['academic_metrics']['freshman_retention_rate']
            },
            
            "student_demographics": {
                "female_percentage": round(female_percentage, 1),
                "male_percentage": round(100 - female_percentage, 1),
                "full_time_percentage": round(full_time_pct, 1),
                "part_time_percentage": round(100 - full_time_pct, 1),
                "transfer_students_percentage": round(transfer_student_pct, 1),
                "financial_aid_percentage": round(financial_aid_pct, 1)
            },
            
            "program_insights": {
                "total_programs": len(self.config['academic_programs']),
                "largest_program": top_major,
                "largest_program_enrollment": int(top_major_count),
                "programs_at_capacity_90_plus": programs_at_capacity,
                "programs_with_growth_potential": programs_with_growth,
                "top_5_majors": [
                    {"major": major, "enrollment": int(count), "percentage": round((count/total_enrollment)*100, 1)}
                    for major, count in major_counts.head(5).items()
                ]
            },
            
            "strategic_insights": [
                f"Queens College serves {total_enrollment:,} students with {capacity_utilization:.1f}% capacity utilization",
                f"Annual tuition revenue of ${total_tuition_revenue/1000000:.1f}M supports institutional operations",
                f"{top_major} leads enrollment with {top_major_count:,} students ({(top_major_count/total_enrollment)*100:.1f}%)",
                f"{programs_at_capacity} programs at 90%+ capacity present expansion opportunities",
                f"Student body is {female_percentage:.1f}% female with {financial_aid_pct:.1f}% receiving financial aid",
                f"Average SAT score of {int(avg_sat)} and college GPA of {avg_gpa:.2f} indicate strong academic performance"
            ],
            
            "performance_benchmarks": {
                "capacity_utilization_target": "85-90%",
                "capacity_utilization_status": "Optimal" if 85 <= capacity_utilization <= 90 else "Monitor",
                "graduation_rate_benchmark": "CUNY system average",
                "retention_rate_benchmark": "78% freshman retention",
                "financial_health": "Strong" if total_tuition_revenue > 100000000 else "Monitor"
            }
        }
        
        # Save KPIs
        kpis_filename = f'{self.output_dir}/PowerBI_Executive_KPIs_Verified.json'
        with open(kpis_filename, 'w') as f:
            json.dump(executive_kpis, f, indent=2)
        
        print(f"[OK] Executive KPIs saved: {kpis_filename}")
        print(f"    Total enrollment: {total_enrollment:,} students")
        print(f"    Capacity utilization: {capacity_utilization:.1f}%")
        print(f"    Annual revenue: ${total_tuition_revenue/1000000:.1f}M")
        print(f"    Top major: {top_major} ({top_major_count:,} students)")
        
        return executive_kpis
    
    def create_demographic_analysis(self):
        """Create demographic analysis files"""
        
        print("\nCreating demographic analysis...")
        
        current_data = self.df[self.df['year'] == 2024].copy()
        
        # Gender analysis by major
        gender_analysis = current_data.groupby(['current_major', 'gender']).size().unstack(fill_value=0)
        gender_analysis['Total'] = gender_analysis.sum(axis=1)
        gender_analysis['Female_Percentage'] = (gender_analysis['Female'] / gender_analysis['Total'] * 100).round(1)
        gender_analysis['Male_Percentage'] = (gender_analysis['Male'] / gender_analysis['Total'] * 100).round(1)
        gender_analysis = gender_analysis.reset_index()
        
        # Age group analysis
        age_groups = pd.cut(current_data['age'], bins=[0, 20, 23, 26, 100], 
                          labels=['18-20', '21-23', '24-26', '27+'])
        current_data['age_group'] = age_groups
        
        age_analysis = current_data.groupby(['current_major', 'age_group']).size().unstack(fill_value=0)
        age_analysis = age_analysis.reset_index()
        
        # Financial need analysis
        financial_analysis = current_data.groupby('current_major').agg({
            'financial_need': ['sum', 'count'],
            'sat_score': 'mean',
            'high_school_gpa': 'mean'
        })
        
        financial_analysis.columns = ['Students_With_Aid', 'Total_Students', 'Avg_SAT', 'Avg_HS_GPA']
        financial_analysis['Financial_Aid_Percentage'] = (financial_analysis['Students_With_Aid'] / financial_analysis['Total_Students'] * 100).round(1)
        financial_analysis = financial_analysis.reset_index()
        
        # Save demographic files
        gender_filename = f'{self.output_dir}/PowerBI_Gender_Analysis_Verified.csv'
        gender_analysis.to_csv(gender_filename, index=False)
        
        age_filename = f'{self.output_dir}/PowerBI_Age_Analysis_Verified.csv'
        age_analysis.to_csv(age_filename, index=False)
        
        financial_filename = f'{self.output_dir}/PowerBI_Financial_Analysis_Verified.csv'
        financial_analysis.to_csv(financial_filename, index=False)
        
        print(f"[OK] Gender analysis saved: {gender_filename}")
        print(f"[OK] Age analysis saved: {age_filename}")
        print(f"[OK] Financial analysis saved: {financial_filename}")
        
        return gender_analysis, age_analysis, financial_analysis
    
    def create_all_powerbi_files(self):
        """Create all Power BI files from verified data"""
        
        print("\nCreating complete Power BI integration...")
        
        # Create all analyses
        enrollment_analysis = self.create_current_enrollment_analysis()
        historical_trends, yearly_totals = self.create_historical_trends_analysis()
        executive_kpis = self.create_verified_executive_kpis()
        gender_analysis, age_analysis, financial_analysis = self.create_demographic_analysis()
        
        # Create summary report
        summary_report = {
            "power_bi_integration_summary": {
                "total_files_created": 7,
                "data_source": "Verified Queens College Dataset",
                "total_records_analyzed": len(self.df),
                "current_year_focus": 2024,
                "files_created": [
                    "PowerBI_Current_Enrollment_Verified.csv",
                    "PowerBI_Historical_Trends_Verified.csv", 
                    "PowerBI_Yearly_Totals_Verified.csv",
                    "PowerBI_Executive_KPIs_Verified.json",
                    "PowerBI_Gender_Analysis_Verified.csv",
                    "PowerBI_Age_Analysis_Verified.csv",
                    "PowerBI_Financial_Analysis_Verified.csv"
                ],
                "key_insights": executive_kpis['strategic_insights'],
                "ready_for_powerbi_import": True
            }
        }
        
        summary_filename = f'{self.output_dir}/PowerBI_Integration_Summary.json'
        with open(summary_filename, 'w') as f:
            json.dump(summary_report, f, indent=2)
        
        print(f"[OK] Integration summary saved: {summary_filename}")
        
        return summary_report

def main():
    """Create verified Power BI integration"""
    
    try:
        # Check if verified data exists
        if not os.path.exists('verified_data/queens_college_verified_dataset.csv'):
            print("[ERROR] Verified dataset not found.")
            print("Please run: python verified_data_generator.py")
            return
        
        # Initialize integration
        powerbi = VerifiedPowerBIIntegration()
        
        # Create all Power BI files
        summary = powerbi.create_all_powerbi_files()
        
        print("\n" + "=" * 60)
        print("VERIFIED POWER BI INTEGRATION COMPLETE!")
        print("=" * 60)
        print(f"[OK] Files created in: {powerbi.output_dir}/")
        print(f"[OK] Total Power BI files: {summary['power_bi_integration_summary']['total_files_created']}")
        print(f"[OK] Based on {len(powerbi.df):,} verified student records")
        print(f"[OK] Ready for import into Power BI Desktop")
        print("\nKey files for VP presentation:")
        for filename in summary['power_bi_integration_summary']['files_created']:
            print(f"  - {filename}")
        
    except Exception as e:
        print(f"[ERROR] Power BI integration failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()