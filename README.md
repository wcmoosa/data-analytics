# DHA Data Analytics Workshop Toolkit

A comprehensive Python toolkit for generating realistic synthetic datasets for Department of Home Affairs (South Africa) data analytics and data quality workshops. This toolkit includes dataset generation, analysis, visualization, and educational materials.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Core Scripts](#core-scripts)
- [Quick Start Guide](#quick-start-guide)
- [Configuration](#configuration)
- [Output Files](#output-files)
- [Workflow Examples](#workflow-examples)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This toolkit is designed for data analytics and data quality training workshops. It generates realistic synthetic South African DHA datasets with intentional data quality issues, enabling hands-on exercises in:

- Data validation and cleaning
- Data quality assessment
- Data analytics and visualization
- Excel formula practice
- Data governance principles

## ✨ Features

- **Realistic Data Generation**: South African ID numbers with Luhn checksum validation
- **Controlled Data Quality Issues**: Configurable duplicate rates, missing values, and invalid data
- **Scalable**: Supports both standard (10K records) and big data (1.5M+ records) modes
- **Comprehensive Analysis**: Automated analysis with charts and visualizations
- **Educational Materials**: PDF workbooks with questions and answers
- **Data Stories**: Interactive HTML dashboard with insights
- **Excel Support**: Automatic sheet splitting for datasets exceeding Excel limits

## 📦 Installation

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)

### Step 1: Clone or Download Repository

```bash
git clone <repository-url>
cd data-analytics
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `pandas` - Data manipulation and analysis
- `faker` - Synthetic data generation
- `openpyxl` - Excel file handling
- `matplotlib` - Chart generation
- `seaborn` - Statistical visualizations
- `reportlab` - PDF generation

### Step 3: Verify Installation

```bash
python --version  # Should show Python 3.12+
```

## 📚 Core Scripts

### 1. `generate_dha_datasets.py`

**Purpose**: Generates synthetic DHA datasets (population registry and applications)

**What it does**:
- Creates realistic South African citizen data
- Generates ID/Passport application records
- Injects controlled data quality issues
- Saves data in CSV and XLSX formats

**Usage**:
```bash
# Standard mode (10K population, 5K applications)
python generate_dha_datasets.py

# Big data mode (1.5M population, 800K applications)
# Edit the script and set BIG_DATA_MODE = True
python generate_dha_datasets.py
```

**Configuration** (in script):
```python
BIG_DATA_MODE = False  # Set to True for big data
POPULATION_ROWS = 10000
APPLICATION_ROWS = 5000
DUPLICATE_RATE = 0.02      # 2%
MISSING_VALUE_RATE = 0.03  # 3%
INVALID_VALUE_RATE = 0.01  # 1%
```

**Output**:
- `data/population_registry.csv` and `.xlsx`
- `data/dha_applications.csv` and `.xlsx`
- (With `big_data_` prefix in big data mode)

**Key Features**:
- ✅ SA ID numbers with Luhn checksum validation
- ✅ Inline data quality issue injection (fast)
- ✅ Automatic Excel sheet splitting for large datasets
- ✅ Progress indicators for big data generation
- ✅ Separate file saving (population ready before applications)

---

### 2. `analyze_dha_datasets.py`

**Purpose**: Analyzes generated datasets and creates visualizations

**What it does**:
- Performs statistical analysis on both datasets
- Generates charts and visualizations (PNG images)
- Creates comprehensive Excel analysis report with formulas
- Detects and reports data quality issues

**Usage**:
```bash
# Analyze standard datasets
python analyze_dha_datasets.py

# Analyze big data datasets
python analyze_dha_datasets.py --big-data
# OR
python analyze_dha_datasets.py -b
```

**Output**:
- Chart images in `output/` directory:
  - `population_gender_distribution.png`
  - `population_birth_year_distribution.png`
  - `applications_by_province.png`
  - `applications_by_status.png`
  - `applications_by_branch.png`
  - `applications_cost_breakdown.png`
  - `applications_duplicates.png`
- Excel report: `output/dha_analysis_report.xlsx` (9 sheets with formulas)

**Analysis Includes**:
- Population statistics (total, unique, duplicates)
- Gender distribution
- Birth year analysis (born after 1975)
- Applications by province, status, and branch
- Revenue calculations (ID Cards × R350, Passports × R650)
- Duplicate detection
- Data quality issue summary

---

### 3. `generate_analysis_workbook.py`

**Purpose**: Creates PDF workbooks for students and instructors

**What it does**:
- Generates question workbook for students
- Creates answer key with Excel formulas for instructors
- Includes comprehensive formula documentation

**Usage**:
```bash
python generate_analysis_workbook.py
```

**Output**:
- `output/dha_analysis_questions.pdf` - Questions for students
- `output/dha_analysis_answers.pdf` - Answers and formulas for instructors

**Content**:
- 15+ analysis questions across 4 sections
- 40+ Excel formulas with explanations
- Tips and best practices
- Professional formatting

---

### 4. `generate_data_story_html.py`

**Purpose**: Creates an interactive HTML one-pager with data stories

**What it does**:
- Builds a responsive HTML dashboard
- Tells data stories using generated charts
- Provides insights and recommendations
- Creates a shareable web page

**Usage**:
```bash
# Standard datasets
python generate_data_story_html.py

# Big data datasets
python generate_data_story_html.py --big-data
```

**Output**:
- `output/dha_data_story.html` - Interactive HTML dashboard

**Features**:
- Responsive design (works on mobile)
- Data stories and insights
- Embedded chart visualizations
- Key findings and recommendations
- Professional styling

**Note**: Run `analyze_dha_datasets.py` first to generate the chart images.

---

## 🚀 Quick Start Guide

### Complete Workflow Example

```bash
# Step 1: Generate datasets
python generate_dha_datasets.py

# Step 2: Analyze datasets and create charts
python analyze_dha_datasets.py

# Step 3: Generate educational workbooks
python generate_analysis_workbook.py

# Step 4: Create HTML data story
python generate_data_story_html.py
```

### Big Data Workflow

```bash
# Step 1: Edit generate_dha_datasets.py
# Set BIG_DATA_MODE = True

# Step 2: Generate big data datasets (takes 15-30 minutes)
python generate_dha_datasets.py

# Step 3: Analyze big data (use --big-data flag)
python analyze_dha_datasets.py --big-data

# Step 4: Generate HTML story for big data
python generate_data_story_html.py --big-data
```

## ⚙️ Configuration

### Dataset Size Configuration

Edit `generate_dha_datasets.py`:

```python
# Standard Mode
BIG_DATA_MODE = False
POPULATION_ROWS = 10000
APPLICATION_ROWS = 5000

# Big Data Mode
BIG_DATA_MODE = True
POPULATION_ROWS = 1500000
APPLICATION_ROWS = 800000
```

### Data Quality Issue Rates

```python
DUPLICATE_RATE = 0.02        # 2% duplicate records
MISSING_VALUE_RATE = 0.03    # 3% missing values
INVALID_VALUE_RATE = 0.01    # 1% invalid values
```

### Performance Settings

```python
# Skip XLSX for big data (saves 10-20 minutes)
SAVE_XLSX_FOR_BIG_DATA = False  # Set to True if you need XLSX
```

## 📁 Output Files

### Data Files (`/data` directory)

**Standard Mode**:
- `population_registry.csv` / `.xlsx`
- `dha_applications.csv` / `.xlsx`

**Big Data Mode**:
- `big_data_population_registry.csv` / `.xlsx` (may have multiple sheets)
- `big_data_dha_applications.csv` / `.xlsx`

### Analysis Files (`/output` directory)

**Charts** (PNG images):
- `population_gender_distribution.png`
- `population_birth_year_distribution.png`
- `applications_by_province.png`
- `applications_by_status.png`
- `applications_by_branch.png`
- `applications_cost_breakdown.png`
- `applications_duplicates.png`

**Reports**:
- `dha_analysis_report.xlsx` - Comprehensive analysis with formulas (9 sheets)
- `dha_analysis_questions.pdf` - Student workbook
- `dha_analysis_answers.pdf` - Instructor answer key
- `dha_data_story.html` - Interactive HTML dashboard

## 🔄 Workflow Examples

### Example 1: Standard Workshop Setup

```bash
# 1. Generate standard datasets (fast, ~30 seconds)
python generate_dha_datasets.py

# 2. Analyze and create visualizations (~10 seconds)
python analyze_dha_datasets.py

# 3. Create educational materials (~5 seconds)
python generate_analysis_workbook.py

# 4. Generate HTML story (~2 seconds)
python generate_data_story_html.py
```

**Result**: Complete workshop package ready for distribution

### Example 2: Big Data Analysis

```bash
# 1. Configure for big data (edit script: BIG_DATA_MODE = True)
# 2. Generate big data (15-30 minutes)
python generate_dha_datasets.py

# 3. Analyze big data
python analyze_dha_datasets.py --big-data

# 4. Create HTML story
python generate_data_story_html.py --big-data
```

**Result**: Large-scale dataset analysis for advanced workshops

### Example 3: Quick Data Generation Only

```bash
# Generate and save immediately (no analysis)
python generate_dha_datasets.py
# Files are saved as soon as each dataset is ready
```

## 🐛 Troubleshooting

### Common Issues

#### 1. "File not found" errors

**Problem**: Scripts can't find data files

**Solution**:
```bash
# Ensure you run generate_dha_datasets.py first
python generate_dha_datasets.py

# Then run analysis
python analyze_dha_datasets.py
```

#### 2. Excel row limit error

**Problem**: "This sheet is too large!" error

**Solution**: Already fixed! The script automatically splits large datasets into multiple sheets.

#### 3. Missing chart images in HTML

**Problem**: HTML shows broken images

**Solution**:
```bash
# Run analysis first to generate charts
python analyze_dha_datasets.py

# Then generate HTML
python generate_data_story_html.py
```

#### 4. Slow performance with big data

**Problem**: Generation takes too long

**Solutions**:
- Set `SAVE_XLSX_FOR_BIG_DATA = False` (saves 10-20 minutes)
- Close other applications to free up memory
- Use SSD storage for faster file I/O
- Consider reducing dataset size for testing

#### 5. Memory errors

**Problem**: "Out of Memory" errors

**Solution**:
- Reduce dataset sizes
- Close other applications
- See `MEMORY_REQUIREMENTS.md` for details
- Minimum 2GB RAM required, 4GB recommended

#### 6. Import errors

**Problem**: "Module not found" errors

**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install individually
pip install pandas faker openpyxl matplotlib seaborn reportlab
```

## 📊 Dataset Schemas

### Population Registry Schema

| Column | Type | Description |
|--------|------|-------------|
| `sa_id_number` | String | 13-digit SA ID (with Luhn checksum) |
| `first_name` | String | First name |
| `last_name` | String | Last name |
| `date_of_birth` | Date | Birth date (YYYY-MM-DD) |
| `gender` | String | Male or Female |
| `citizenship_status` | String | South African |
| `province` | String | One of 9 SA provinces |
| `city` | String | City name |
| `street_address` | String | Street address |
| `postal_code` | String | 4-digit postal code |
| `cell_number` | String | Phone number (+27 or 0 format) |
| `record_created_date` | Date | Record creation date |

### Applications Schema

| Column | Type | Description |
|--------|------|-------------|
| `application_id` | String | Unique application ID (APP######) |
| `sa_id_number` | String | Reference to population registry |
| `application_type` | String | ID Card or Passport |
| `application_date` | Date | Application submission date |
| `application_status` | String | Pending, In Progress, Approved, Rejected, Completed, or null |
| `province` | String | Province of application |
| `dha_branch_name` | String | DHA branch name |
| `branch_code` | String | 4-digit branch code |
| `submission_channel` | String | Branch, Online, or Mobile Unit |
| `processing_days` | Integer | Days to process (may be invalid) |
| `last_updated_date` | Date | Last status update date |

## 🎓 Educational Use Cases

### Workshop Scenarios

1. **Data Quality Workshop**
   - Use generated datasets with intentional issues
   - Students identify and fix data quality problems
   - Practice data validation techniques

2. **Excel Analytics Training**
   - Use PDF workbooks for guided exercises
   - Practice Excel formulas and functions
   - Learn PivotTables and data analysis

3. **Data Visualization**
   - Analyze generated charts
   - Create custom visualizations
   - Practice storytelling with data

4. **Big Data Analytics**
   - Work with 1.5M+ record datasets
   - Practice performance optimization
   - Learn scalable analysis techniques

## 📝 Notes

- **Data is Synthetic**: All data is generated and does not represent real individuals
- **Reproducible**: Uses fixed random seeds for consistent results
- **Educational Purpose**: Designed for training and workshops
- **Excel Limits**: Large datasets automatically split into multiple sheets

## 🔗 Additional Resources

- `MEMORY_REQUIREMENTS.md` - Memory requirements for big data generation
- `PERFORMANCE_OPTIMIZATIONS.md` - Performance tips and optimizations
- `requirements.txt` - Python package dependencies

## 📄 License

This toolkit is designed for educational and training purposes.

## 🤝 Contributing

When contributing, please ensure:
- Code follows Python best practices
- Documentation is updated
- Scripts are tested with both standard and big data modes
- Output files are properly formatted

## 📧 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review script documentation headers
3. Verify all dependencies are installed
4. Check that data files exist before running analysis

---

**Happy Data Analyzing! 📊**

