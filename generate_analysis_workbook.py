"""
================================================================================
DHA Analysis Workbook Generator
================================================================================

PURPOSE:
    Generate separate PDF files: one with analysis questions for students to complete
    using Excel, and one with formula answers for instructors.

PYTHON VERSION REQUIRED:
    Python 3.12

DEPENDENCY INSTALLATION:
    pip install reportlab

HOW TO RUN THE SCRIPT:
    python generate_analysis_workbook.py

OUTPUT:
    Generates two separate PDF files in /output directory:
    - dha_analysis_questions.pdf (questions for students)
    - dha_analysis_answers.pdf (answers and formulas for instructors)

================================================================================
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import os

# Create output directory
OUTPUT_DIR = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_questions_pdf():
    """
    Create a PDF with analysis questions only.
    """
    pdf_path = os.path.join(OUTPUT_DIR, 'dha_analysis_questions.pdf')
    
    print("Creating PDF with questions...")
    
    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=72)
    
    # Container for the 'Flowable' objects
    story = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a237e'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#283593'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor('#3949ab'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    question_style = ParagraphStyle(
        'QuestionStyle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        spaceBefore=8,
        leftIndent=20,
        fontName='Helvetica'
    )
    
    answer_style = ParagraphStyle(
        'AnswerStyle',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        spaceBefore=6,
        leftIndent=30,
        fontName='Courier',
        textColor=colors.HexColor('#2e7d32'),
        backColor=colors.HexColor('#f1f8e9')
    )
    
    # Title Page
    story.append(Paragraph("DHA Data Analytics Workbook", title_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Department of Home Affairs - South Africa", 
                          ParagraphStyle('Subtitle', parent=styles['Normal'], 
                                        fontSize=14, alignment=TA_CENTER)))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Data Quality and Analytics Exercise", 
                          ParagraphStyle('Subtitle', parent=styles['Normal'], 
                                        fontSize=12, alignment=TA_CENTER, 
                                        textColor=colors.grey)))
    story.append(Spacer(1, 0.5*inch))
    
    intro_text = """
    <b>Instructions:</b><br/>
    This workbook contains a series of data analysis questions based on the DHA synthetic datasets.
    Use Microsoft Excel to analyze the provided CSV files and answer each question.
    <br/><br/>
    <b>Datasets:</b><br/>
    • population_registry.csv - Contains citizen registry data<br/>
    • dha_applications.csv - Contains ID and Passport application data<br/>
    <br/>
    <b>Requirements:</b><br/>
    • Use Excel formulas to calculate all answers<br/>
    • Show your work by documenting formulas used<br/>
    • Complete all sections before checking answers<br/>
    """
    story.append(Paragraph(intro_text, styles['Normal']))
    story.append(PageBreak())
    
    # ============================================================================
    # SECTION 1: POPULATION REGISTRY ANALYSIS
    # ============================================================================
    story.append(Paragraph("SECTION 1: POPULATION REGISTRY ANALYSIS", heading_style))
    
    story.append(Paragraph("Question 1.1: Total Population Count", subheading_style))
    story.append(Paragraph(
        "Calculate the total number of records in the population registry dataset.",
        question_style
    ))
    story.append(Paragraph("Your Answer: _________________", question_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Question 1.2: Unique Population", subheading_style))
    story.append(Paragraph(
        "How many unique South African ID numbers are in the population registry? "
        "What does this tell you about data quality?",
        question_style
    ))
    story.append(Paragraph("Unique SA IDs: _________________", question_style))
    story.append(Paragraph("Duplicate SA IDs: _________________", question_style))
    story.append(Paragraph("Data Quality Assessment: _________________", question_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Question 1.3: Gender Distribution", subheading_style))
    story.append(Paragraph(
        "Create a breakdown showing the count and percentage of each gender in the population registry. "
        "Present your results in a table format.",
        question_style
    ))
    story.append(Paragraph("Table:", question_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Your Analysis: _________________", question_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Question 1.4: Birth Year Analysis", subheading_style))
    story.append(Paragraph(
        "How many people in the registry were born after the year 1975? "
        "What percentage of the total population does this represent?",
        question_style
    ))
    story.append(Paragraph("Born After 1975: _________________", question_style))
    story.append(Paragraph("Percentage: _________________%", question_style))
    story.append(Paragraph("Born 1975 or Earlier: _________________", question_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(PageBreak())
    
    # ============================================================================
    # SECTION 2: APPLICATIONS ANALYSIS
    # ============================================================================
    story.append(Paragraph("SECTION 2: DHA APPLICATIONS ANALYSIS", heading_style))
    
    story.append(Paragraph("Question 2.1: Applications by Province", subheading_style))
    story.append(Paragraph(
        "Create a table showing the total number of applications by province. "
        "Include both the count and percentage for each province. "
        "Which province has the most applications?",
        question_style
    ))
    story.append(Paragraph("Province with Most Applications: _________________", question_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Question 2.2: Application Status Distribution", subheading_style))
    story.append(Paragraph(
        "Analyze the distribution of application statuses. "
        "Note: Treat missing/null values as 'Unknown'. "
        "Create a breakdown showing count and percentage for each status.",
        question_style
    ))
    story.append(Paragraph("Status Distribution Table:", question_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Most Common Status: _________________", question_style))
    story.append(Paragraph("Percentage of Unknown Status: _________________%", question_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Question 2.3: Branch Analysis", subheading_style))
    story.append(Paragraph(
        "Identify the top 15 DHA branches by application volume. "
        "Create a ranked list showing branch name, count, and percentage of total applications.",
        question_style
    ))
    story.append(Paragraph("Top 3 Branches:", question_style))
    story.append(Paragraph("1. _________________", question_style))
    story.append(Paragraph("2. _________________", question_style))
    story.append(Paragraph("3. _________________", question_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Question 2.4: Revenue Calculation", subheading_style))
    story.append(Paragraph(
        "Calculate the total revenue generated from all applications. "
        "Note: ID Card applications cost R350 each, and Passport applications cost R650 each.",
        question_style
    ))
    story.append(Paragraph("ID Card Applications: _________________", question_style))
    story.append(Paragraph("ID Card Revenue: R _________________", question_style))
    story.append(Paragraph("Passport Applications: _________________", question_style))
    story.append(Paragraph("Passport Revenue: R _________________", question_style))
    story.append(Paragraph("Total Revenue: R _________________", question_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Question 2.5: Duplicate Applications", subheading_style))
    story.append(Paragraph(
        "Identify duplicate applications (same SA ID number appearing multiple times). "
        "How many duplicate application records exist? "
        "How many unique SA IDs have duplicate applications? "
        "What is the average number of applications per duplicate ID?",
        question_style
    ))
    story.append(Paragraph("Total Duplicate Records: _________________", question_style))
    story.append(Paragraph("Unique SA IDs with Duplicates: _________________", question_style))
    story.append(Paragraph("Average Applications per Duplicate ID: _________________", question_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(PageBreak())
    
    # ============================================================================
    # SECTION 3: DATA QUALITY ANALYSIS
    # ============================================================================
    story.append(Paragraph("SECTION 3: DATA QUALITY ASSESSMENT", heading_style))
    
    story.append(Paragraph("Question 3.1: Missing Values", subheading_style))
    story.append(Paragraph(
        "Identify missing values in the population registry dataset. "
        "Check the following fields: street_address, cell_number, postal_code, and city. "
        "How many missing values exist in each field?",
        question_style
    ))
    story.append(Paragraph("Missing street_address: _________________", question_style))
    story.append(Paragraph("Missing cell_number: _________________", question_style))
    story.append(Paragraph("Missing postal_code: _________________", question_style))
    story.append(Paragraph("Missing city: _________________", question_style))
    story.append(Paragraph("Total Missing Values: _________________", question_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Question 3.2: Application Data Quality", subheading_style))
    story.append(Paragraph(
        "How many applications have missing status values? "
        "What percentage of total applications does this represent?",
        question_style
    ))
    story.append(Paragraph("Missing Status Count: _________________", question_style))
    story.append(Paragraph("Percentage: _________________%", question_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Question 3.3: Data Quality Summary", subheading_style))
    story.append(Paragraph(
        "Create a summary table of all data quality issues found across both datasets. "
        "Include: issue type, dataset affected, count, and impact assessment.",
        question_style
    ))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Data Quality Issues Summary Table:", question_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(PageBreak())
    
    # ============================================================================
    # SECTION 4: ADVANCED ANALYSIS
    # ============================================================================
    story.append(Paragraph("SECTION 4: ADVANCED ANALYSIS QUESTIONS", heading_style))
    
    story.append(Paragraph("Question 4.1: Cross-Dataset Analysis", subheading_style))
    story.append(Paragraph(
        "How many application records reference SA IDs that do NOT exist in the population registry? "
        "These are called 'orphan records'. What might cause this data quality issue?",
        question_style
    ))
    story.append(Paragraph("Orphan Records Count: _________________", question_style))
    story.append(Paragraph("Possible Causes: _________________", question_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Question 4.2: Processing Time Analysis", subheading_style))
    story.append(Paragraph(
        "Analyze the processing_days field in the applications dataset. "
        "Identify any invalid values (negative numbers or extremely high values). "
        "What is the average processing time for valid applications?",
        question_style
    ))
    story.append(Paragraph("Invalid Processing Days: _________________", question_style))
    story.append(Paragraph("Average Valid Processing Days: _________________", question_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Question 4.3: Date Validation", subheading_style))
    story.append(Paragraph(
        "Check for date inconsistencies in the applications dataset. "
        "How many records have a last_updated_date that is earlier than the application_date? "
        "This is a logical data quality issue.",
        question_style
    ))
    story.append(Paragraph("Invalid Date Sequences: _________________", question_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(PageBreak())
    
    # Build questions PDF
    doc.build(story)
    print(f"✓ Questions PDF created: {pdf_path}")


def create_answers_pdf():
    """
    Create a PDF with answers and formulas only.
    """
    pdf_path = os.path.join(OUTPUT_DIR, 'dha_analysis_answers.pdf')
    
    print("Creating PDF with answers and formulas...")
    
    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=72)
    
    # Container for the 'Flowable' objects
    story = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a237e'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#283593'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    question_style_small = ParagraphStyle(
        'QuestionSmall',
        parent=styles['Normal'],
        fontSize=8,
        fontName='Helvetica-Bold',
        leading=10
    )
    
    notes_style = ParagraphStyle(
        'NotesStyle',
        parent=styles['Normal'],
        fontSize=8,
        fontName='Helvetica',
        leading=10
    )
    
    formula_text_style = ParagraphStyle(
        'FormulaText',
        parent=styles['Normal'],
        fontSize=7,
        fontName='Courier',
        leading=9,
        leftIndent=0,
        rightIndent=0,
        alignment=TA_LEFT
    )
    
    # Title Page
    story.append(Paragraph("DHA Data Analytics - Answers", title_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Department of Home Affairs - South Africa", 
                          ParagraphStyle('Subtitle', parent=styles['Normal'], 
                                        fontSize=14, alignment=TA_CENTER)))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Formula Reference Guide", 
                          ParagraphStyle('Subtitle', parent=styles['Normal'], 
                                        fontSize=12, alignment=TA_CENTER, 
                                        textColor=colors.grey)))
    story.append(Spacer(1, 0.5*inch))
    
    intro_text = """
    <b>Instructions for Instructors:</b><br/>
    This document contains the answers and Excel formulas for all questions in the 
    DHA Data Analytics Workbook. Use this as a reference when reviewing student work 
    or providing feedback.
    <br/><br/>
    <b>Note:</b> Adjust table names and cell references based on your Excel setup. 
    Formulas assume Excel Tables are used with structured references.
    """
    story.append(Paragraph(intro_text, styles['Normal']))
    story.append(PageBreak())
    
    # ============================================================================
    # ANSWERS SECTION
    # ============================================================================
    story.append(Paragraph("ANSWERS AND FORMULAS", heading_style))
    story.append(Paragraph(
        "Below are the Excel formulas and methods used to calculate each answer. "
        "Note: Adjust table names and cell references based on your Excel setup.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # Create a style for formula text that wraps
    formula_text_style = ParagraphStyle(
        'FormulaText',
        parent=styles['Normal'],
        fontSize=7,
        fontName='Courier',
        leading=9,
        leftIndent=0,
        rightIndent=0,
        alignment=TA_LEFT
    )
    
    question_style_small = ParagraphStyle(
        'QuestionSmall',
        parent=styles['Normal'],
        fontSize=8,
        fontName='Helvetica-Bold',
        leading=10
    )
    
    notes_style = ParagraphStyle(
        'NotesStyle',
        parent=styles['Normal'],
        fontSize=8,
        fontName='Helvetica',
        leading=10
    )
    
    # Helper function to convert data rows to Paragraph objects
    def make_table_row(q, f, n):
        """Convert row data to Paragraph objects for proper wrapping"""
        if q == '' and f == '' and n == '':
            return ['', '', '']  # Empty row
        return [
            Paragraph(q, question_style_small) if q else '',
            Paragraph(f.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), formula_text_style) if f else '',
            Paragraph(n, notes_style) if n else ''
        ]
    
    # Answers Table - convert formulas to Paragraph objects for proper wrapping
    raw_data = [
        # Section 1 Answers
        ['1.1: Total Population', '=COUNTA(A:A)-1', 'Count all rows minus header'],
        ['1.1: Alternative', '=COUNT(population_registry[sa_id_number])', 'Using Excel table'],
        ['', '', ''],
        ['1.2: Unique SA IDs', '=COUNTA(UNIQUE(population_registry[sa_id_number]))', 'Excel 365/2021'],
        ['1.2: Unique (Older Excel)', '=SUMPRODUCT(1/COUNTIF(population_registry[sa_id_number], population_registry[sa_id_number]))', 'Array formula'],
        ['1.2: Duplicates', '=Total_Population - Unique_SA_IDs', 'Simple subtraction'],
        ['1.2: Duplicate %', '=(Duplicates/Total_Population)*100', 'Percentage calculation'],
        ['', '', ''],
        ['1.3: Gender Count', '=COUNTIF(population_registry[gender],"Male")', 'Count by gender'],
        ['1.3: Gender %', '=Gender_Count/Total_Population*100', 'Calculate percentage'],
        ['1.3: Table Method', 'Use PivotTable: Rows=gender, Values=Count & %', 'Recommended approach'],
        ['', '', ''],
        ['1.4: Born After 1975', '=COUNTIFS(population_registry[date_of_birth],">1975-12-31")', 'Date comparison'],
        ['1.4: Using YEAR', '=SUMPRODUCT(--(YEAR(population_registry[date_of_birth])>1975))', 'Extract year first'],
        ['1.4: Percentage', '=(Born_After_1975/Total_Population)*100', 'Percentage formula'],
        ['', '', ''],
        
        # Section 2 Answers
        ['2.1: Count by Province', '=COUNTIF(dha_applications[province],"Province Name")', 'Count per province'],
        ['2.1: All Provinces', 'Use PivotTable: Rows=province, Values=Count', 'Easiest method'],
        ['2.1: Percentage', '=Province_Count/Total_Applications*100', 'Calculate %'],
        ['2.1: Max Province', '=INDEX(province_list,MATCH(MAX(counts),counts,0))', 'Find maximum'],
        ['', '', ''],
        ['2.2: Status Count', '=COUNTIF(dha_applications[application_status],"Status Name")', 'Count by status'],
        ['2.2: Unknown Status', '=COUNTBLANK(dha_applications[application_status])', 'Count blanks'],
        ['2.2: All Statuses', 'Use PivotTable: Rows=status, Values=Count & %', 'Recommended'],
        ['', '', ''],
        ['2.3: Branch Count', '=COUNTIF(dha_applications[dha_branch_name],"Branch Name")', 'Count per branch'],
        ['2.3: Top 15', 'Use PivotTable, sort descending, show top 15', 'Easiest approach'],
        ['2.3: RANK Function', '=RANK.EQ(branch_count,all_branch_counts,0)', 'Rank branches'],
        ['', '', ''],
        ['2.4: ID Card Count', '=COUNTIF(dha_applications[application_type],"ID Card")', 'Count ID cards'],
        ['2.4: ID Card Revenue', '=ID_Card_Count*350', 'Multiply by unit price'],
        ['2.4: Passport Count', '=COUNTIF(dha_applications[application_type],"Passport")', 'Count passports'],
        ['2.4: Passport Revenue', '=Passport_Count*650', 'Multiply by unit price'],
        ['2.4: Total Revenue', '=SUM(ID_Card_Revenue,Passport_Revenue)', 'Sum both revenues'],
        ['2.4: Alternative', '=SUMPRODUCT((dha_applications[application_type]="ID Card")*350+(dha_applications[application_type]="Passport")*650)', 'Single formula'],
        ['', '', ''],
        ['2.5: Find Duplicates', '=COUNTIF(dha_applications[sa_id_number],sa_id_number)>1', 'Check for duplicates'],
        ['2.5: Duplicate Records', '=SUMPRODUCT(--(COUNTIF(dha_applications[sa_id_number],dha_applications[sa_id_number])>1))', 'Count all duplicates'],
        ['2.5: Unique Duplicate IDs', '=COUNTA(UNIQUE(FILTER(dha_applications[sa_id_number],COUNTIF(dha_applications[sa_id_number],dha_applications[sa_id_number])>1)))', 'Excel 365'],
        ['2.5: Average', '=Total_Duplicate_Records/Unique_Duplicate_IDs', 'Simple division'],
        ['', '', ''],
        
        # Section 3 Answers
        ['3.1: Missing Values', '=COUNTBLANK(population_registry[street_address])', 'Count blanks'],
        ['3.1: All Missing', '=SUM(COUNTBLANK(population_registry[street_address]),COUNTBLANK(population_registry[cell_number]),...)', 'Sum all'],
        ['3.1: Alternative', '=SUMPRODUCT(--(ISBLANK(population_registry[address_fields])))', 'Using ISBLANK'],
        ['', '', ''],
        ['3.2: Missing Status', '=COUNTBLANK(dha_applications[application_status])', 'Count blanks'],
        ['3.2: Percentage', '=(Missing_Status/Total_Applications)*100', 'Calculate %'],
        ['', '', ''],
        
        # Section 4 Answers
        ['4.1: Orphan Records', '=COUNTIFS(dha_applications[sa_id_number],"<>"&population_registry[sa_id_number])', 'Complex lookup'],
        ['4.1: VLOOKUP Method', '=IF(ISNA(VLOOKUP(sa_id,population_table,1,FALSE)),"Orphan","Valid")', 'Check existence'],
        ['4.1: COUNTIF Method', '=SUMPRODUCT(--(ISNA(MATCH(dha_applications[sa_id_number],population_registry[sa_id_number],0))))', 'Match function'],
        ['', '', ''],
        ['4.2: Invalid Processing', '=COUNTIFS(dha_applications[processing_days],"<0")+COUNTIFS(dha_applications[processing_days],">100")', 'Count invalid'],
        ['4.2: Average Valid', '=AVERAGEIFS(dha_applications[processing_days],dha_applications[processing_days],">0",dha_applications[processing_days],"<=100")', 'Conditional average'],
        ['', '', ''],
        ['4.3: Invalid Dates', '=SUMPRODUCT(--(dha_applications[last_updated_date]<dha_applications[application_date]))', 'Date comparison'],
        ['4.3: Alternative', '=COUNTIFS(dha_applications[last_updated_date],"<"&dha_applications[application_date])', 'Using COUNTIFS'],
    ]
    
    # Build answers_data with header and converted rows
    answers_data = [
        [Paragraph('<b>Question</b>', question_style_small), 
         Paragraph('<b>Formula / Method</b>', question_style_small), 
         Paragraph('<b>Notes</b>', question_style_small)]
    ]
    
    # Convert all data rows to Paragraph objects
    for row in raw_data:
        answers_data.append(make_table_row(row[0], row[1], row[2]))
    
    # Create table with better column widths for formulas
    # Adjust widths: Question column smaller, Formula column larger, Notes column medium
    # Total width: 1.5 + 5.0 + 1.5 = 8 inches (fits on A4 with margins)
    answers_table = Table(answers_data, colWidths=[1.5*inch, 5.0*inch, 1.5*inch], repeatRows=1)
    answers_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#283593')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 1), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
        ('SPAN', (0, 0), (0, 0)),  # Ensure proper cell spanning
    ]))
    
    story.append(answers_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Additional Tips
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor('#3949ab'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    story.append(Paragraph("ADDITIONAL EXCEL TIPS", subheading_style))
    tips_text = """
    <b>1. Using Excel Tables:</b><br/>
    Convert your data to Excel Tables (Insert > Table) to use structured references like 
    'population_registry[sa_id_number]' instead of cell ranges.<br/><br/>
    
    <b>2. PivotTables:</b><br/>
    PivotTables are excellent for grouping and counting data. Use them for questions involving 
    counts by category (gender, province, status, etc.).<br/><br/>
    
    <b>3. Array Formulas:</b><br/>
    Some formulas require array entry (Ctrl+Shift+Enter in older Excel) or work automatically 
    in Excel 365. Test your formulas on small datasets first.<br/><br/>
    
    <b>4. Data Validation:</b><br/>
    Use conditional formatting to highlight data quality issues like duplicates, missing values, 
    or invalid dates.<br/><br/>
    
    <b>5. Documentation:</b><br/>
    Always document your formulas and methodology. Create a separate sheet for your calculations 
    and reference cells clearly.
    """
    story.append(Paragraph(tips_text, styles['Normal']))
    
    # Build answers PDF
    doc.build(story)
    print(f"✓ Answers PDF created: {pdf_path}")
    print(f"  Contains comprehensive formula answers for all questions")


def create_workbook_pdf():
    """
    Create both questions and answers PDFs.
    """
    create_questions_pdf()
    create_answers_pdf()
    print("\n✓ Both PDF files created successfully!")
    print(f"  - {os.path.join(OUTPUT_DIR, 'dha_analysis_questions.pdf')}")
    print(f"  - {os.path.join(OUTPUT_DIR, 'dha_analysis_answers.pdf')}")


def main():
    """
    Main function to generate the PDF workbook.
    """
    print("="*70)
    print("DHA ANALYSIS WORKBOOK GENERATOR")
    print("Department of Home Affairs - South Africa")
    print("="*70)
    
    try:
        create_workbook_pdf()
        print("\n✓ Workbook generation completed successfully!")
        print("="*70)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

