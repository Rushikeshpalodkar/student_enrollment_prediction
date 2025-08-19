# CUNY First Database Integration Guide
## Replace Sample Data with Real CUNY First Data

### 🎯 **Overview**
This guide shows you exactly how to replace the sample data with your actual CUNY First databases to get real enrollment predictions and analytics.

---

## 📊 **Current Sample Data vs CUNY First Data**

### **Sample Data Generated:**
- **PowerBI_Historical_Enrollment_2018-2025.csv** (35,937 records)
- **PowerBI_Current_Year_2025_Detailed.csv** (5,490 records) 
- **PowerBI_Capacity_Analysis.csv**
- **PowerBI_Gender_Analysis_by_Major.csv**

### **CUNY First Tables You Need:**
- **Student enrollment data** (historical)
- **Student demographics** (gender, ethnicity, age)
- **Course enrollment** (majors, schools, classes)
- **Capacity/limits** (program caps, course limits)

---

## 🔄 **Step-by-Step Data Replacement**

### **Step 1: Export CUNY First Data**
Export the following data from CUNY First:

#### **A. Historical Enrollment (2018-2025)**
```sql
-- Example query structure (adapt to your CUNY First schema)
SELECT 
    student_id,
    academic_year,
    semester,
    major_code,
    major_name,
    school_code,
    school_name,
    gender,
    age,
    ethnicity,
    gpa,
    total_credits,
    residency_status,
    financial_aid_flag
FROM student_enrollment 
WHERE academic_year BETWEEN '2018' AND '2025'
```

#### **B. Current Year Details (2025)**
```sql
-- Current semester enrollment
SELECT 
    student_id,
    semester,
    credits_enrolled,
    class_standing,
    major_name,
    school_name,
    gender,
    age,
    gpa,
    ethnicity,
    residency_status
FROM current_enrollment 
WHERE academic_year = '2025'
```

#### **C. Program Capacity Limits**
```sql
-- Program capacity data
SELECT 
    major_name,
    max_enrollment_capacity,
    current_enrollment_count,
    faculty_count
FROM program_capacity
```

### **Step 2: Format Data to Match Our Structure**

#### **A. Replace PowerBI_Historical_Enrollment_2018-2025.csv**
Your CUNY data should have these columns:
```
Year,Major,School,Gender,Age,GPA,Ethnicity,Residency,Financial_Aid
2018,Computer Science,Engineering,Female,19,3.45,Hispanic,In-State,True
2019,Business Administration,Business,Male,20,3.12,White,Out-of-State,False
...
```

#### **B. Replace PowerBI_Current_Year_2025_Detailed.csv**
```
Year,Major,School,Gender,Age,GPA,Ethnicity,Residency,Financial_Aid,Semester,Credits_Enrolled,Class_Standing
2025,Computer Science,Engineering,Female,21,3.67,Asian,In-State,True,Fall,15,Junior
...
```

#### **C. Replace PowerBI_Capacity_Analysis.csv**
```
Major,Current_Enrollment,Max_Capacity,Utilization_Rate,Shortage,Surplus,Status,Recommended_Action
Computer Science,850,800,106.3,50,0,Over Capacity,Expand Program
...
```

### **Step 3: Update Data Generation Scripts**

#### **A. Modify `create_powerbi_data.py`**
Replace the sample data generation section with CUNY First data loading:

```python
# REPLACE THIS SECTION (lines 20-100)
# Instead of generating sample data, load from CUNY First exports

# Load historical data from CUNY First export
df_historical = pd.read_csv('cuny_first_historical_export.csv')

# Load current year data
current_year = pd.read_csv('cuny_first_current_year.csv')

# Load capacity data  
capacity_data = pd.read_csv('cuny_first_capacity_limits.csv')
```

#### **B. Update Field Mappings**
Map CUNY First field names to our format:
```python
# CUNY First to our format mapping
field_mapping = {
    'STUDENT_ID': 'student_id',
    'ACAD_YEAR': 'Year', 
    'MAJOR_DESC': 'Major',
    'SCHOOL_DESC': 'School',
    'GENDER_CODE': 'Gender',
    'STUDENT_AGE': 'Age',
    'CUM_GPA': 'GPA',
    'ETHNIC_DESC': 'Ethnicity',
    'RESIDENCY': 'Residency',
    'FIN_AID_FLAG': 'Financial_Aid'
}

# Rename columns to match our format
df_historical = df_historical.rename(columns=field_mapping)
```

---

## 🔧 **Automated Integration Scripts**

### **Script 1: CUNY Data Processor**
```python
# cuny_data_processor.py
import pandas as pd
import numpy as np

def process_cuny_first_data():
    """Process CUNY First exports into Power BI format"""
    
    print("Processing CUNY First data...")
    
    # Load your CUNY First exports
    historical = pd.read_csv('cuny_exports/historical_enrollment.csv')
    current = pd.read_csv('cuny_exports/current_enrollment.csv') 
    capacity = pd.read_csv('cuny_exports/program_capacity.csv')
    
    # Process historical data
    historical_processed = process_historical_data(historical)
    historical_processed.to_csv('PowerBI_Historical_Enrollment_2018-2025.csv', index=False)
    
    # Process current year
    current_processed = process_current_year_data(current)
    current_processed.to_csv('PowerBI_Current_Year_2025_Detailed.csv', index=False)
    
    # Process capacity analysis
    capacity_processed = process_capacity_data(capacity, current)
    capacity_processed.to_csv('PowerBI_Capacity_Analysis.csv', index=False)
    
    print("CUNY First data processing completed!")

def process_historical_data(df):
    """Clean and format historical CUNY data"""
    # Add your CUNY-specific data cleaning here
    # Handle CUNY First specific codes, formats, etc.
    return df

def process_current_year_data(df):
    """Process current year CUNY data"""
    # Add current year specific processing
    return df

def process_capacity_data(capacity_df, current_df):
    """Calculate capacity utilization from CUNY data"""
    # Calculate actual utilization rates
    # Compare with CUNY program limits
    return capacity_analysis

if __name__ == "__main__":
    process_cuny_first_data()
```

### **Script 2: CUNY Field Mapper**
```python
# cuny_field_mapper.py
def map_cuny_fields(df, data_type='historical'):
    """Map CUNY First fields to our standard format"""
    
    if data_type == 'historical':
        field_mapping = {
            # Map your CUNY First column names here
            'STU_ID': 'student_id',
            'TERM_CODE': 'semester', 
            'MAJOR_CODE': 'major_code',
            'MAJOR_DESC': 'Major',
            'COLL_CODE': 'school_code',
            'COLL_DESC': 'School',
            'GENDER': 'Gender',
            'AGE': 'Age',
            'ETHNICITY': 'Ethnicity',
            'CUM_GPA': 'GPA',
            'RESIDENCY': 'Residency',
            'AID_FLAG': 'Financial_Aid'
        }
    
    # Apply mapping
    df_mapped = df.rename(columns=field_mapping)
    
    # Clean CUNY-specific codes
    df_mapped = clean_cuny_codes(df_mapped)
    
    return df_mapped

def clean_cuny_codes(df):
    """Clean CUNY First specific codes and formats"""
    
    # Example: Convert CUNY gender codes
    gender_mapping = {
        'M': 'Male',
        'F': 'Female', 
        'X': 'Other'
    }
    if 'Gender' in df.columns:
        df['Gender'] = df['Gender'].map(gender_mapping)
    
    # Example: Convert CUNY school codes
    school_mapping = {
        'ENG': 'Engineering',
        'BUS': 'Business',
        'LIB': 'Liberal Arts',
        'SCI': 'Sciences',
        'NUR': 'Nursing'
    }
    if 'School' in df.columns:
        df['School'] = df['School'].map(school_mapping).fillna(df['School'])
    
    return df
```

---

## 📋 **Integration Checklist**

### **Before Integration:**
- [ ] Export historical enrollment data from CUNY First (2018-2025)
- [ ] Export current year detailed enrollment data
- [ ] Export program capacity and limits data
- [ ] Export demographic data (gender, ethnicity, etc.)
- [ ] Identify CUNY First field names and codes

### **During Integration:**
- [ ] Create `cuny_exports/` folder for your data files
- [ ] Run `cuny_data_processor.py` to process your exports
- [ ] Verify data formats match our Power BI structure
- [ ] Test with a small sample first
- [ ] Validate data quality and completeness

### **After Integration:**
- [ ] Run `create_powerbi_data.py` with real data
- [ ] Verify all Power BI files are generated correctly
- [ ] Test the web dashboard with real data
- [ ] Update capacity limits with actual CUNY program caps
- [ ] Validate all analytics and trends

### **Quality Assurance:**
- [ ] Compare sample vs real data structure
- [ ] Verify historical trends make sense
- [ ] Check gender ratios match expectations  
- [ ] Validate capacity analysis against known limits
- [ ] Test Power BI dashboard with real data

---

## 🎯 **Key Differences to Expect**

### **Sample Data vs CUNY First:**
- **Sample**: Generated trends and patterns
- **CUNY**: Real historical trends and actual patterns
- **Sample**: Simulated capacity limits  
- **CUNY**: Actual program enrollment caps
- **Sample**: Fictional demographics
- **CUNY**: Real student demographic distributions

### **What Will Stay the Same:**
- ✅ All Power BI dashboard structures
- ✅ All visualization templates
- ✅ Executive reporting formats
- ✅ API endpoints and functionality
- ✅ Analysis methodologies

### **What Will Be More Accurate:**
- 📊 Real historical enrollment trends
- 🎯 Actual capacity shortages/surpluses  
- 👥 True demographic distributions
- 📈 Genuine growth/decline patterns
- 💼 Accurate strategic insights

---

## 🚀 **Quick Start with Your CUNY Data**

1. **Export your CUNY First data** using the SQL examples above
2. **Save exports** in `cuny_exports/` folder
3. **Run the processor**: `python cuny_data_processor.py`
4. **Generate Power BI files**: `python create_powerbi_data.py`
5. **Import to Power BI** using the existing integration guide
6. **Present to leadership** with real CUNY data insights!

---

**🎯 Result: Your complete Student Enrollment Prediction System now runs on real CUNY First data instead of sample data, providing accurate insights for strategic decision-making!**