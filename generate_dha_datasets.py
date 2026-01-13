"""
================================================================================
DHA Synthetic Dataset Generator
================================================================================

PURPOSE:
    Generate realistic synthetic datasets for Department of Home Affairs
    (South Africa) data analytics and data quality workshops. The script
    intentionally includes controlled data quality issues to support validation
    and cleaning exercises.

PYTHON VERSION REQUIRED:
    Python 3.12

DEPENDENCY INSTALLATION:
    pip install pandas faker openpyxl

HOW TO CHANGE DATASET SIZE AND ERROR RATES:
    Modify the configuration parameters at the top of the main() function:
    - BIG_DATA_MODE: Set to True for datasets with over 1 million records
    - POPULATION_ROWS: Number of population registry records
    - APPLICATION_ROWS: Number of application records
    - DUPLICATE_RATE: Percentage of duplicate records (0.02 = 2%)
    - MISSING_VALUE_RATE: Percentage of missing values (0.03 = 3%)
    - INVALID_VALUE_RATE: Percentage of invalid values (0.01 = 1%)
    
    When BIG_DATA_MODE is True, output files will have "big_data_" prefix.

HOW TO RUN THE SCRIPT:
    python generate_dha_datasets.py

OUTPUT:
    The script generates CSV and XLSX files in the /data directory:
    - population_registry.csv (or big_data_population_registry.csv in big data mode)
    - population_registry.xlsx (or big_data_population_registry.xlsx in big data mode)
    - dha_applications.csv (or big_data_dha_applications.csv in big data mode)
    - dha_applications.xlsx (or big_data_dha_applications.xlsx in big data mode)

================================================================================
"""

import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os
from typing import List, Dict, Tuple

# Initialize Faker (using en_GB as en_ZA is not available in Faker)
# Note: We manually specify South African provinces, cities, and formats
fake = Faker('en_GB')
Faker.seed(42)
random.seed(42)

# South African provinces
SA_PROVINCES = [
    'Eastern Cape', 'Free State', 'Gauteng', 'KwaZulu-Natal',
    'Limpopo', 'Mpumalanga', 'Northern Cape', 'North West', 'Western Cape'
]

# DHA Branch names by province (simplified mapping)
DHA_BRANCHES = {
    'Eastern Cape': ['Port Elizabeth', 'East London', 'Mthatha'],
    'Free State': ['Bloemfontein', 'Welkom'],
    'Gauteng': ['Johannesburg', 'Pretoria', 'Soweto', 'Sandton', 'Midrand'],
    'KwaZulu-Natal': ['Durban', 'Pietermaritzburg', 'Newcastle'],
    'Limpopo': ['Polokwane', 'Tzaneen'],
    'Mpumalanga': ['Nelspruit', 'Witbank'],
    'Northern Cape': ['Kimberley', 'Upington'],
    'North West': ['Mahikeng', 'Rustenburg'],
    'Western Cape': ['Cape Town', 'Stellenbosch', 'George']
}

# Application types and statuses
APPLICATION_TYPES = ['ID Card', 'Passport']
APPLICATION_STATUSES = ['Pending', 'In Progress', 'Approved', 'Rejected', 'Completed']
SUBMISSION_CHANNELS = ['Branch', 'Online', 'Mobile Unit']


def calculate_luhn_checksum(number: str) -> int:
    """
    Calculate Luhn checksum digit for South African ID number.
    
    Args:
        number: 12-digit string (without checksum)
    
    Returns:
        Checksum digit (0-9)
    """
    digits = [int(d) for d in number]
    # Double every second digit from right
    for i in range(len(digits) - 1, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    total = sum(digits)
    return (10 - (total % 10)) % 10


def generate_sa_id_number(date_of_birth: datetime, gender: str) -> str:
    """
    Generate a valid South African ID number.
    Format: YYMMDDSSSSCAZ (13 digits)
    - YYMMDD: Date of birth
    - SSSS: Sequence number (0000-9999)
    - C: Citizenship (0 for SA citizen)
    - A: Race/age indicator (0-8)
    - Z: Checksum digit (Luhn algorithm)
    
    Args:
        date_of_birth: Date of birth datetime object
        gender: 'Male' or 'Female'
    
    Returns:
        13-digit SA ID number string
    """
    # Extract date components
    yy = date_of_birth.year % 100
    mm = date_of_birth.month
    dd = date_of_birth.day
    
    # Format as YYMMDD
    date_part = f"{yy:02d}{mm:02d}{dd:02d}"
    
    # Generate sequence number (0000-9999)
    sequence = random.randint(0, 9999)
    sequence_part = f"{sequence:04d}"
    
    # Citizenship digit (0 for SA citizen)
    citizenship = '0'
    
    # Race/age indicator (simplified: random 0-8)
    age_indicator = random.randint(0, 8)
    
    # Construct 12-digit number (without checksum)
    id_without_checksum = date_part + sequence_part + citizenship + str(age_indicator)
    
    # Calculate Luhn checksum
    checksum = calculate_luhn_checksum(id_without_checksum)
    
    # Return complete 13-digit ID
    return id_without_checksum + str(checksum)


def generate_population_data(num_rows: int, show_progress: bool = True,
                             duplicate_rate: float = 0.0, missing_rate: float = 0.0,
                             invalid_rate: float = 0.0) -> Tuple[pd.DataFrame, Dict]:
    """
    Generate synthetic population registry data with inline data quality issue injection.
    
    Args:
        num_rows: Number of records to generate
        show_progress: If True, show progress updates for large datasets
        duplicate_rate: Percentage of duplicate SA ID numbers (0.02 = 2%)
        missing_rate: Percentage of missing values (0.03 = 3%)
        invalid_rate: Percentage of invalid values (0.01 = 1%)
    
    Returns:
        Tuple of (DataFrame with population registry data, issue statistics dictionary)
    """
    data = []
    id_numbers = set()  # Track generated IDs to avoid duplicates initially
    id_list = []  # Track IDs for duplicate injection
    issues = {
        'duplicates': 0,
        'missing_values': 0,
        'invalid_postal_codes': 0,
        'future_dates': 0,
        'inconsistent_formatting': 0
    }
    
    # Pre-calculate which records will have which issues (much faster than random checks)
    num_duplicates = int(num_rows * duplicate_rate)
    num_missing = int(num_rows * missing_rate)
    num_invalid_postal = int(num_rows * invalid_rate)
    num_future_dates = int(num_rows * invalid_rate)
    num_formatting = int(num_rows * invalid_rate * 2)
    
    # Pre-select indices for each issue type (using sets for O(1) lookup)
    duplicate_indices = set(random.sample(range(num_rows), min(num_duplicates, num_rows))) if num_duplicates > 0 else set()
    missing_indices = set(random.sample(range(num_rows), min(num_missing, num_rows))) if num_missing > 0 else set()
    invalid_postal_indices = set(random.sample(range(num_rows), min(num_invalid_postal, num_rows))) if num_invalid_postal > 0 else set()
    future_date_indices = set(random.sample(range(num_rows), min(num_future_dates, num_rows))) if num_future_dates > 0 else set()
    formatting_indices = set(random.sample(range(num_rows), min(num_formatting, num_rows))) if num_formatting > 0 else set()
    
    # Pre-determine issue types for formatting issues
    formatting_types = {}
    fields_to_make_missing = ['street_address', 'cell_number', 'postal_code', 'city']
    for idx in formatting_indices:
        formatting_types[idx] = random.choice(['name_case', 'phone_format'])
    
    # Pre-determine which fields to make missing
    missing_fields = {}
    for idx in missing_indices:
        missing_fields[idx] = random.choice(fields_to_make_missing)
    
    # Progress indicator for large datasets
    progress_interval = max(1, num_rows // 20) if show_progress else num_rows + 1
    
    for i in range(num_rows):
        # Show progress for large datasets
        if show_progress and (i + 1) % progress_interval == 0:
            progress = ((i + 1) / num_rows) * 100
            print(f"  Progress: {i+1:,}/{num_rows:,} ({progress:.1f}%)", end='\r')
        # Generate date of birth (between 18 and 80 years ago)
        birth_year = random.randint(1944, 2006)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)  # Use 28 to avoid month-end issues
        date_of_birth = datetime(birth_year, birth_month, birth_day)
        
        # Generate gender
        gender = random.choice(['Male', 'Female'])
        
        # Generate SA ID number
        sa_id = generate_sa_id_number(date_of_birth, gender)
        # Ensure unique ID (in normal case)
        while sa_id in id_numbers:
            sa_id = generate_sa_id_number(date_of_birth, gender)
        id_numbers.add(sa_id)
        
        # Generate name (using Faker with SA locale)
        first_name = fake.first_name()
        last_name = fake.last_name()
        
        # Apply inconsistent name formatting if needed (during generation)
        if i in formatting_indices and formatting_types.get(i) == 'name_case':
            if random.random() < 0.5:
                first_name = first_name.upper()
            else:
                first_name = first_name.lower()
            issues['inconsistent_formatting'] += 1
        
        # Citizenship status
        citizenship_status = 'South African'
        
        # Generate province and city
        province = random.choice(SA_PROVINCES)
        city = fake.city() if i not in missing_indices or missing_fields.get(i) != 'city' else None
        
        # Generate address
        street_address = fake.street_address() if i not in missing_indices or missing_fields.get(i) != 'street_address' else None
        
        # Generate postal code (with potential invalid format)
        if i in invalid_postal_indices:
            postal_code = random.choice([
                str(random.randint(100, 999)),  # 3 digits
                str(random.randint(10000, 99999)),  # 5 digits
                'ABCD',  # Letters
                ''  # Empty string
            ])
            issues['invalid_postal_codes'] += 1
        else:
            postal_code = fake.postcode()
        
        # Apply missing postal code if needed
        if i in missing_indices and missing_fields.get(i) == 'postal_code':
            postal_code = None
        
        # Count missing values (count once per record that has missing values)
        if i in missing_indices:
            issues['missing_values'] += 1
        
        # Generate cell number (South African format) - optimized
        # Format: +27 or 0 followed by 9 digits
        cell_prefix = random.choice(['+27', '0'])
        # More efficient: generate 9 random digits at once
        cell_suffix = f"{random.randint(100000000, 999999999)}"
        cell_number = cell_prefix + cell_suffix
        
        # Apply inconsistent phone formatting if needed (during generation)
        if i in formatting_indices and formatting_types.get(i) == 'phone_format':
            if cell_number.startswith('+27'):
                cell_number = '0' + cell_number[3:]  # Remove +27, add 0
            elif cell_number.startswith('0'):
                cell_number = '+27' + cell_number[1:]  # Add +27, remove 0
            issues['inconsistent_formatting'] += 1
        
        # Apply missing cell number if needed
        if i in missing_indices and missing_fields.get(i) == 'cell_number':
            cell_number = None
        
        # Record created date (within last 5 years, but after date of birth)
        min_created_date = date_of_birth + timedelta(days=365)  # At least 1 year after birth
        max_created_date = datetime.now()
        days_diff = (max_created_date - min_created_date).days
        
        # Apply future date if needed
        if i in future_date_indices:
            record_created_date = datetime.now() + timedelta(days=random.randint(1, 30))
            issues['future_dates'] += 1
        else:
            record_created_date = min_created_date + timedelta(days=random.randint(0, days_diff))
        
        # Track ID for potential duplication
        if i in duplicate_indices:
            id_list.append((i, sa_id))
        
        data.append({
            'sa_id_number': sa_id,
            'first_name': first_name,
            'last_name': last_name,
            'date_of_birth': date_of_birth.strftime('%Y-%m-%d'),
            'gender': gender,
            'citizenship_status': citizenship_status,
            'province': province,
            'city': city,
            'street_address': street_address,
            'postal_code': postal_code,
            'cell_number': cell_number,
            'record_created_date': record_created_date.strftime('%Y-%m-%d')
        })
    
    # Apply duplicates efficiently (copy IDs from random records)
    if duplicate_indices:
        all_indices = list(range(num_rows))
        for dup_idx, _ in id_list:
            # Pick a random source index (not the duplicate index itself)
            source_idx = random.choice([idx for idx in all_indices if idx != dup_idx])
            data[dup_idx]['sa_id_number'] = data[source_idx]['sa_id_number']
            issues['duplicates'] += 1
    
    if show_progress:
        print(f"  Progress: {num_rows:,}/{num_rows:,} (100.0%)")
    
    return pd.DataFrame(data), issues


def inject_population_quality_issues(df: pd.DataFrame, duplicate_rate: float,
                                     missing_rate: float, invalid_rate: float) -> Tuple[pd.DataFrame, Dict]:
    """
    Inject controlled data quality issues into population registry data.
    
    Args:
        df: Population registry DataFrame
        duplicate_rate: Percentage of duplicate SA ID numbers (0.02 = 2%)
        missing_rate: Percentage of missing values (0.03 = 3%)
        invalid_rate: Percentage of invalid values (0.01 = 1%)
    
    Returns:
        Tuple of (modified DataFrame, issue statistics dictionary)
    """
    df = df.copy()
    issues = {
        'duplicates': 0,
        'missing_values': 0,
        'invalid_postal_codes': 0,
        'future_dates': 0,
        'inconsistent_formatting': 0
    }
    
    num_rows = len(df)
    
    # 1. DUPLICATE SA ID NUMBERS (1-3%)
    # Intentional issue: Some citizens have duplicate ID numbers in the system
    num_duplicates = int(num_rows * duplicate_rate)
    if num_duplicates > 0:
        # Select random rows to duplicate
        duplicate_indices = random.sample(range(num_rows), min(num_duplicates, num_rows))
        for idx in duplicate_indices:
            # Copy the SA ID from another random record
            source_idx = random.choice([i for i in range(num_rows) if i != idx])
            df.at[idx, 'sa_id_number'] = df.at[source_idx, 'sa_id_number']
            issues['duplicates'] += 1
    
    # 2. MISSING VALUES in non-critical fields
    # Intentional issue: Missing address, phone, or postal code data
    fields_to_make_missing = ['street_address', 'cell_number', 'postal_code', 'city']
    num_missing = int(num_rows * missing_rate)
    for _ in range(num_missing):
        idx = random.randint(0, num_rows - 1)
        field = random.choice(fields_to_make_missing)
        if pd.notna(df.at[idx, field]):
            df.at[idx, field] = None
            issues['missing_values'] += 1
    
    # 3. INCONSISTENT FORMATTING
    # Intentional issue: Mixed case names, inconsistent phone formats
    num_formatting = int(num_rows * invalid_rate * 2)  # More common issue
    for _ in range(num_formatting):
        idx = random.randint(0, num_rows - 1)
        issue_type = random.choice(['name_case', 'phone_format'])
        
        if issue_type == 'name_case':
            # Randomly capitalize names inconsistently
            if random.random() < 0.5:
                df.at[idx, 'first_name'] = df.at[idx, 'first_name'].upper()
            else:
                df.at[idx, 'first_name'] = df.at[idx, 'first_name'].lower()
            issues['inconsistent_formatting'] += 1
        
        elif issue_type == 'phone_format':
            # Remove country code or add inconsistent formatting
            cell = str(df.at[idx, 'cell_number'])
            if cell.startswith('+27'):
                df.at[idx, 'cell_number'] = '0' + cell[3:]  # Remove +27, add 0
            elif cell.startswith('0'):
                df.at[idx, 'cell_number'] = '+27' + cell[1:]  # Add +27, remove 0
            issues['inconsistent_formatting'] += 1
    
    # 4. INVALID POSTAL CODES
    # Intentional issue: Some postal codes don't match SA format (should be 4 digits)
    num_invalid_postal = int(num_rows * invalid_rate)
    for _ in range(num_invalid_postal):
        idx = random.randint(0, num_rows - 1)
        if pd.notna(df.at[idx, 'postal_code']):
            # Generate invalid postal code (wrong length or format)
            invalid_code = random.choice([
                str(random.randint(100, 999)),  # 3 digits
                str(random.randint(10000, 99999)),  # 5 digits
                'ABCD',  # Letters
                ''  # Empty string
            ])
            df.at[idx, 'postal_code'] = invalid_code
            issues['invalid_postal_codes'] += 1
    
    # 5. FUTURE RECORD CREATED DATES
    # Intentional issue: Some records have creation dates in the future
    num_future_dates = int(num_rows * invalid_rate)
    for _ in range(num_future_dates):
        idx = random.randint(0, num_rows - 1)
        # Set date to 1-30 days in the future
        future_date = datetime.now() + timedelta(days=random.randint(1, 30))
        df.at[idx, 'record_created_date'] = future_date.strftime('%Y-%m-%d')
        issues['future_dates'] += 1
    
    return df, issues


def generate_application_data(num_rows: int, population_df: pd.DataFrame, show_progress: bool = True) -> pd.DataFrame:
    """
    Generate synthetic DHA application data.
    
    Args:
        num_rows: Number of application records to generate
        population_df: Population registry DataFrame for referential integrity
        show_progress: If True, show progress updates for large datasets
    
    Returns:
        DataFrame with application data
    """
    data = []
    population_ids = population_df['sa_id_number'].tolist()
    
    # OPTIMIZATION: Create dictionary lookup for ID -> province (much faster than DataFrame filtering)
    id_to_province = dict(zip(population_df['sa_id_number'], population_df['province']))
    
    # Generate branch codes (3-4 digit codes)
    branch_codes = {}
    for province, branches in DHA_BRANCHES.items():
        for branch in branches:
            branch_codes[branch] = f"{random.randint(100, 9999):04d}"
    
    # Progress indicator for large datasets
    progress_interval = max(1, num_rows // 20) if show_progress else num_rows + 1
    
    for i in range(num_rows):
        # Show progress for large datasets
        if show_progress and (i + 1) % progress_interval == 0:
            progress = ((i + 1) / num_rows) * 100
            print(f"  Progress: {i+1:,}/{num_rows:,} ({progress:.1f}%)", end='\r')
        
        # Application ID (unique identifier)
        application_id = f"APP{random.randint(100000, 999999)}"
        
        # Link to population registry (most records)
        # Small percentage will be orphan records (intentional data quality issue)
        if random.random() < 0.95:  # 95% valid references
            sa_id_number = random.choice(population_ids)
            # OPTIMIZATION: Use dictionary lookup instead of DataFrame filtering
            province = id_to_province.get(sa_id_number, random.choice(SA_PROVINCES))
        else:
            # Orphan record: ID not in population registry
            sa_id_number = generate_sa_id_number(
                datetime(random.randint(1980, 2000), random.randint(1, 12), random.randint(1, 28)),
                random.choice(['Male', 'Female'])
            )
            province = random.choice(SA_PROVINCES)
        
        # Application type
        application_type = random.choice(APPLICATION_TYPES)
        
        # Application date (within last 3 years)
        app_date = datetime.now() - timedelta(days=random.randint(0, 1095))
        application_date = app_date.strftime('%Y-%m-%d')
        
        # Application status (some missing - intentional issue)
        application_status = random.choice(APPLICATION_STATUSES + [None])
        
        # DHA branch (should match province, but sometimes won't - intentional issue)
        if province in DHA_BRANCHES:
            # 90% match province, 10% don't (intentional mismatch)
            if random.random() < 0.9:
                branch_name = random.choice(DHA_BRANCHES[province])
            else:
                # Mismatch: branch from different province
                other_provinces = [p for p in SA_PROVINCES if p != province]
                other_province = random.choice(other_provinces)
                branch_name = random.choice(DHA_BRANCHES[other_province])
        else:
            branch_name = random.choice(DHA_BRANCHES[random.choice(SA_PROVINCES)])
        
        branch_code = branch_codes.get(branch_name, f"{random.randint(1000, 9999):04d}")
        
        # Submission channel
        submission_channel = random.choice(SUBMISSION_CHANNELS)
        
        # Processing days (normally 5-30 days, but some invalid - intentional issue)
        if random.random() < 0.95:
            processing_days = random.randint(5, 30)
        else:
            # Invalid: negative or extreme values
            processing_days = random.choice([
                random.randint(-10, -1),  # Negative
                random.randint(1000, 5000)  # Extreme
            ])
        
        # Last updated date (should be >= application date, but sometimes not - intentional issue)
        if random.random() < 0.95:
            # Valid: after application date
            days_after_app = random.randint(0, processing_days if processing_days > 0 else 30)
            last_updated = app_date + timedelta(days=days_after_app)
        else:
            # Invalid: before application date
            last_updated = app_date - timedelta(days=random.randint(1, 30))
        
        last_updated_date = last_updated.strftime('%Y-%m-%d')
        
        data.append({
            'application_id': application_id,
            'sa_id_number': sa_id_number,
            'application_type': application_type,
            'application_date': application_date,
            'application_status': application_status,
            'province': province,
            'dha_branch_name': branch_name,
            'branch_code': branch_code,
            'submission_channel': submission_channel,
            'processing_days': processing_days,
            'last_updated_date': last_updated_date
        })
    
    if show_progress:
        print(f"  Progress: {num_rows:,}/{num_rows:,} (100.0%)")
    
    return pd.DataFrame(data)


def inject_application_quality_issues(df: pd.DataFrame, duplicate_rate: float,
                                      missing_rate: float, invalid_rate: float) -> Tuple[pd.DataFrame, Dict]:
    """
    Inject additional controlled data quality issues into application data.
    
    Args:
        df: Application DataFrame
        duplicate_rate: Percentage of duplicate applications (0.02 = 2%)
        missing_rate: Percentage of missing values (0.03 = 3%)
        invalid_rate: Percentage of invalid values (0.01 = 1%)
    
    Returns:
        Tuple of (modified DataFrame, issue statistics dictionary)
    """
    df = df.copy()
    issues = {
        'duplicate_applications': 0,
        'missing_status': 0,
        'province_mismatches': 0,
        'invalid_processing_days': 0,
        'invalid_dates': 0
    }
    
    num_rows = len(df)
    
    # Additional duplicate applications (same ID, different application_id)
    num_duplicates = int(num_rows * duplicate_rate)
    if num_duplicates > 0:
        duplicate_indices = random.sample(range(num_rows), min(num_duplicates, num_rows))
        for idx in duplicate_indices:
            # Find another application with same SA ID
            sa_id = df.at[idx, 'sa_id_number']
            matching_indices = df[df['sa_id_number'] == sa_id].index.tolist()
            if len(matching_indices) > 1:
                issues['duplicate_applications'] += 1
    
    # Missing application_status (additional to what's already in generation)
    num_missing_status = int(num_rows * missing_rate)
    status_indices = df[df['application_status'].notna()].index.tolist()
    if len(status_indices) > 0:
        missing_indices = random.sample(status_indices, min(num_missing_status, len(status_indices)))
        for idx in missing_indices:
            df.at[idx, 'application_status'] = None
            issues['missing_status'] += 1
    
    # Province vs branch mismatches (additional)
    num_mismatches = int(num_rows * invalid_rate)
    for _ in range(num_mismatches):
        idx = random.randint(0, num_rows - 1)
        province = df.at[idx, 'province']
        branch = df.at[idx, 'dha_branch_name']
        
        # Check if branch belongs to province
        if province in DHA_BRANCHES and branch not in DHA_BRANCHES[province]:
            issues['province_mismatches'] += 1
        else:
            # Force a mismatch
            other_provinces = [p for p in SA_PROVINCES if p != province]
            if other_provinces:
                other_province = random.choice(other_provinces)
                df.at[idx, 'dha_branch_name'] = random.choice(DHA_BRANCHES[other_province])
                issues['province_mismatches'] += 1
    
    # Invalid processing days (negative or extreme) - count existing ones
    invalid_days = df[(df['processing_days'] < 0) | (df['processing_days'] > 100)]
    issues['invalid_processing_days'] = len(invalid_days)
    
    # Invalid dates (last_updated < application_date) - count existing ones
    df['app_date'] = pd.to_datetime(df['application_date'])
    df['updated_date'] = pd.to_datetime(df['last_updated_date'])
    invalid_dates = df[df['updated_date'] < df['app_date']]
    issues['invalid_dates'] = len(invalid_dates)
    df = df.drop(columns=['app_date', 'updated_date'])
    
    return df, issues


def save_population_dataset(population_df: pd.DataFrame, output_dir: str = 'data', 
                            big_data: bool = False, save_xlsx: bool = True) -> list:
    """
    Save population registry dataset to CSV and optionally XLSX formats.
    
    Args:
        population_df: Population registry DataFrame
        output_dir: Output directory path
        big_data: If True, adds "big_data" to output filenames
        save_xlsx: If False, skip XLSX generation (much faster for big data)
    
    Returns:
        List of saved file paths
    """
    # Excel row limit: 1,048,576 rows per sheet
    EXCEL_MAX_ROWS = 1048576
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Determine filename prefix
    prefix = 'big_data_' if big_data else ''
    
    saved_files = []
    
    # Save population registry CSV
    population_csv = os.path.join(output_dir, f'{prefix}population_registry.csv')
    print(f"  Saving population registry CSV ({len(population_df):,} rows)...")
    population_df.to_csv(population_csv, index=False)
    saved_files.append(population_csv)
    
    # Save population registry XLSX (skip for big data by default - very slow)
    if save_xlsx:
        num_rows = len(population_df)
        
        if num_rows > EXCEL_MAX_ROWS:
            # Dataset exceeds Excel row limit - split into multiple sheets
            print(f"  ⚠️  Dataset exceeds Excel row limit ({EXCEL_MAX_ROWS:,} rows)")
            print(f"  Splitting into multiple sheets...")
            
            population_xlsx = os.path.join(output_dir, f'{prefix}population_registry.xlsx')
            num_sheets = (num_rows // EXCEL_MAX_ROWS) + (1 if num_rows % EXCEL_MAX_ROWS > 0 else 0)
            
            with pd.ExcelWriter(population_xlsx, engine='openpyxl') as writer:
                for sheet_num in range(num_sheets):
                    start_idx = sheet_num * EXCEL_MAX_ROWS
                    end_idx = min((sheet_num + 1) * EXCEL_MAX_ROWS, num_rows)
                    sheet_df = population_df.iloc[start_idx:end_idx]
                    sheet_name = f'Sheet{sheet_num + 1}' if num_sheets > 1 else 'Population Registry'
                    print(f"    Writing sheet {sheet_num + 1}/{num_sheets} ({len(sheet_df):,} rows)...")
                    sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            saved_files.append(population_xlsx)
            print(f"  ✓ Saved to {num_sheets} sheet(s) in XLSX file")
        else:
            # Dataset fits in single sheet
            population_xlsx = os.path.join(output_dir, f'{prefix}population_registry.xlsx')
            print(f"  Saving population registry XLSX ({num_rows:,} rows)...")
            population_df.to_excel(population_xlsx, index=False, engine='openpyxl')
            saved_files.append(population_xlsx)
    
    print(f"✓ Population registry files saved:")
    for file in saved_files:
        print(f"  - {file}")
    if not save_xlsx:
        print(f"  (XLSX skipped for performance)")
    
    return saved_files


def save_application_dataset(application_df: pd.DataFrame, output_dir: str = 'data',
                             big_data: bool = False, save_xlsx: bool = True) -> list:
    """
    Save applications dataset to CSV and optionally XLSX formats.
    
    Args:
        application_df: Application DataFrame
        output_dir: Output directory path
        big_data: If True, adds "big_data" to output filenames
        save_xlsx: If False, skip XLSX generation (much faster for big data)
    
    Returns:
        List of saved file paths
    """
    # Excel row limit: 1,048,576 rows per sheet
    EXCEL_MAX_ROWS = 1048576
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Determine filename prefix
    prefix = 'big_data_' if big_data else ''
    
    saved_files = []
    
    # Save applications CSV
    application_csv = os.path.join(output_dir, f'{prefix}dha_applications.csv')
    print(f"  Saving applications CSV ({len(application_df):,} rows)...")
    application_df.to_csv(application_csv, index=False)
    saved_files.append(application_csv)
    
    # Save applications XLSX (skip for big data by default - very slow)
    if save_xlsx:
        num_rows = len(application_df)
        
        if num_rows > EXCEL_MAX_ROWS:
            # Dataset exceeds Excel row limit - split into multiple sheets
            print(f"  ⚠️  Dataset exceeds Excel row limit ({EXCEL_MAX_ROWS:,} rows)")
            print(f"  Splitting into multiple sheets...")
            
            application_xlsx = os.path.join(output_dir, f'{prefix}dha_applications.xlsx')
            num_sheets = (num_rows // EXCEL_MAX_ROWS) + (1 if num_rows % EXCEL_MAX_ROWS > 0 else 0)
            
            with pd.ExcelWriter(application_xlsx, engine='openpyxl') as writer:
                for sheet_num in range(num_sheets):
                    start_idx = sheet_num * EXCEL_MAX_ROWS
                    end_idx = min((sheet_num + 1) * EXCEL_MAX_ROWS, num_rows)
                    sheet_df = application_df.iloc[start_idx:end_idx]
                    sheet_name = f'Sheet{sheet_num + 1}' if num_sheets > 1 else 'Applications'
                    print(f"    Writing sheet {sheet_num + 1}/{num_sheets} ({len(sheet_df):,} rows)...")
                    sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            saved_files.append(application_xlsx)
            print(f"  ✓ Saved to {num_sheets} sheet(s) in XLSX file")
        else:
            # Dataset fits in single sheet
            application_xlsx = os.path.join(output_dir, f'{prefix}dha_applications.xlsx')
            print(f"  Saving applications XLSX ({num_rows:,} rows)...")
            application_df.to_excel(application_xlsx, index=False, engine='openpyxl')
            saved_files.append(application_xlsx)
    
    print(f"✓ Application files saved:")
    for file in saved_files:
        print(f"  - {file}")
    if not save_xlsx:
        print(f"  (XLSX skipped for performance)")
    
    return saved_files


def save_datasets(population_df: pd.DataFrame, application_df: pd.DataFrame, 
                  output_dir: str = 'data', big_data: bool = False, save_xlsx: bool = True):
    """
    Save both datasets to CSV and XLSX formats (legacy function for backward compatibility).
    
    Args:
        population_df: Population registry DataFrame
        application_df: Application DataFrame
        output_dir: Output directory path
        big_data: If True, adds "big_data" to output filenames
        save_xlsx: If False, skip XLSX generation (much faster for big data)
    """
    save_population_dataset(population_df, output_dir, big_data, save_xlsx)
    save_application_dataset(application_df, output_dir, big_data, save_xlsx)


def print_summary_statistics(population_df: pd.DataFrame, application_df: pd.DataFrame,
                             pop_issues: Dict, app_issues: Dict):
    """
    Print summary statistics and data quality issue counts.
    
    Args:
        population_df: Population registry DataFrame
        application_df: Application DataFrame
        pop_issues: Population data quality issues dictionary
        app_issues: Application data quality issues dictionary
    """
    print("\n" + "="*70)
    print("DATASET GENERATION SUMMARY")
    print("="*70)
    
    print(f"\n📊 POPULATION REGISTRY DATASET")
    print(f"   Total Records: {len(population_df):,}")
    print(f"   Columns: {len(population_df.columns)}")
    print(f"\n   Data Quality Issues Injected:")
    print(f"   - Duplicate SA ID Numbers: {pop_issues['duplicates']:,}")
    print(f"   - Missing Values: {pop_issues['missing_values']:,}")
    print(f"   - Invalid Postal Codes: {pop_issues['invalid_postal_codes']:,}")
    print(f"   - Future Record Dates: {pop_issues['future_dates']:,}")
    print(f"   - Inconsistent Formatting: {pop_issues['inconsistent_formatting']:,}")
    
    print(f"\n📋 DHA APPLICATIONS DATASET")
    print(f"   Total Records: {len(application_df):,}")
    print(f"   Columns: {len(application_df.columns)}")
    print(f"\n   Data Quality Issues Injected:")
    print(f"   - Duplicate Applications: {app_issues['duplicate_applications']:,}")
    print(f"   - Missing Application Status: {app_issues['missing_status']:,}")
    print(f"   - Province/Branch Mismatches: {app_issues['province_mismatches']:,}")
    print(f"   - Invalid Processing Days: {app_issues['invalid_processing_days']:,}")
    print(f"   - Invalid Date Sequences: {app_issues['invalid_dates']:,}")
    
    # Count orphan records (SA IDs in applications not in population)
    pop_ids = set(population_df['sa_id_number'].unique())
    app_ids = set(application_df['sa_id_number'].unique())
    orphan_count = len(app_ids - pop_ids)
    print(f"   - Orphan Records (IDs not in population): {orphan_count:,}")
    
    print("\n" + "="*70)
    print("✓ Dataset generation completed successfully!")
    print("="*70 + "\n")


def main():
    """
    Main function to generate DHA synthetic datasets.
    """
    # ============================================================================
    # CONFIGURATION PARAMETERS
    # ============================================================================
    # Adjust these values to change dataset sizes and error injection rates
    
    # Set BIG_DATA_MODE = True to generate datasets with over 1 million records
    BIG_DATA_MODE = True
    
    # PERFORMANCE OPTIMIZATION: Skip XLSX for big data (saves 10-20 minutes)
    # Set to True if you need XLSX files, but CSV is usually sufficient
    SAVE_XLSX_FOR_BIG_DATA = True
    
    if BIG_DATA_MODE:
        # Big data configuration (over 1 million records)
        POPULATION_ROWS = 1500000   # 1.5 million population registry records
        APPLICATION_ROWS = 800000   # 800 thousand application records
    else:
        # Standard configuration
        POPULATION_ROWS = 10000     # Number of population registry records
        APPLICATION_ROWS = 5000     # Number of application records
    
    # Data quality issue rates (as decimals: 0.02 = 2%, 0.03 = 3%, etc.)
    DUPLICATE_RATE = 0.02        # 2% duplicate records
    MISSING_VALUE_RATE = 0.03    # 3% missing values
    INVALID_VALUE_RATE = 0.01    # 1% invalid values
    
    # ============================================================================
    
    mode_label = "BIG DATA MODE" if BIG_DATA_MODE else "STANDARD MODE"
    print("="*70)
    print("DHA SYNTHETIC DATASET GENERATOR")
    print("Department of Home Affairs - South Africa")
    print(f"{mode_label}")
    print("="*70)
    print(f"\nGenerating datasets with the following configuration:")
    print(f"  Population Registry: {POPULATION_ROWS:,} records")
    print(f"  Applications: {APPLICATION_ROWS:,} records")
    print(f"  Duplicate Rate: {DUPLICATE_RATE*100:.1f}%")
    print(f"  Missing Value Rate: {MISSING_VALUE_RATE*100:.1f}%")
    print(f"  Invalid Value Rate: {INVALID_VALUE_RATE*100:.1f}%")
    if BIG_DATA_MODE:
        print(f"\n⚠️  WARNING: Big data mode enabled. This may take significant time and memory.")
        print(f"   Estimated time: 5-15 minutes (CSV only) or 15-30 minutes (with XLSX)")
        if not SAVE_XLSX_FOR_BIG_DATA:
            print(f"   ⚡ Performance: XLSX generation skipped (set SAVE_XLSX_FOR_BIG_DATA=True to enable)")
    print("\nGenerating data...")
    
    # Step 1: Generate population registry data with inline data quality issues
    print("\n[1/4] Generating population registry data with data quality issues...")
    population_df, pop_issues = generate_population_data(
        POPULATION_ROWS, 
        show_progress=BIG_DATA_MODE,
        duplicate_rate=DUPLICATE_RATE,
        missing_rate=MISSING_VALUE_RATE,
        invalid_rate=INVALID_VALUE_RATE
    )
    
    # Step 2: Save population registry immediately (don't wait for applications)
    print("\n[2/4] Saving population registry files...")
    save_xlsx = SAVE_XLSX_FOR_BIG_DATA if BIG_DATA_MODE else True
    save_population_dataset(population_df, big_data=BIG_DATA_MODE, save_xlsx=save_xlsx)
    print("  ✓ Population registry files are ready and available for use!\n")
    
    # Step 3: Generate application data
    print("[3/4] Generating DHA application data...")
    application_df = generate_application_data(APPLICATION_ROWS, population_df, show_progress=BIG_DATA_MODE)
    
    # Step 4: Inject data quality issues into application data (still separate for now)
    print("\n[4/4] Injecting data quality issues into application data...")
    application_df, app_issues = inject_application_quality_issues(
        application_df, DUPLICATE_RATE, MISSING_VALUE_RATE, INVALID_VALUE_RATE
    )
    
    # Step 5: Save applications immediately
    print("\nSaving application files...")
    save_application_dataset(application_df, big_data=BIG_DATA_MODE, save_xlsx=save_xlsx)
    print("  ✓ Application files are ready and available for use!\n")
    
    # Step 6: Print summary statistics
    print_summary_statistics(population_df, application_df, pop_issues, app_issues)


if __name__ == "__main__":
    main()

