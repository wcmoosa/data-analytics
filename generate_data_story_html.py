"""
================================================================================
DHA Data Story HTML Generator
================================================================================

PURPOSE:
    Generate an HTML one-pager website that tells data stories using the
    charts and visualizations from analyze_dha_datasets.py

PYTHON VERSION REQUIRED:
    Python 3.12

DEPENDENCY INSTALLATION:
    No additional dependencies required (uses standard library)

HOW TO RUN THE SCRIPT:
    python generate_data_story_html.py
    
    For big data outputs:
    python generate_data_story_html.py --big-data

OUTPUT:
    Generates an HTML file:
    - dha_data_story.html (in /output directory)

================================================================================
"""

import os
import argparse
from datetime import datetime

# Create output directory
OUTPUT_DIR = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_html_story(big_data: bool = False):
    """
    Create an HTML one-pager with data stories.
    
    Args:
        big_data: If True, uses big_data_ prefixed image files
    """
    prefix = 'big_data_' if big_data else ''
    html_path = os.path.join(OUTPUT_DIR, f'{prefix}dha_data_story.html')
    
    print(f"Creating HTML data story page...")
    
    # Check which images exist
    image_files = [
        f'{prefix}population_gender_distribution.png',
        f'{prefix}population_birth_year_distribution.png',
        f'{prefix}applications_by_province.png',
        f'{prefix}applications_by_status.png',
        f'{prefix}applications_by_branch.png',
        f'{prefix}applications_cost_breakdown.png',
        f'{prefix}applications_duplicates.png'
    ]
    
    existing_images = []
    for img in image_files:
        img_path = os.path.join(OUTPUT_DIR, img)
        if os.path.exists(img_path):
            existing_images.append(img)
        else:
            print(f"  Warning: Image not found: {img}")
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DHA Data Analytics Story - South Africa</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: white;
            box-shadow: 0 0 30px rgba(0,0,0,0.3);
        }}
        
        header {{
            background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
            margin: -20px -20px 30px -20px;
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .intro {{
            background: #f5f5f5;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 40px;
            border-left: 5px solid #283593;
        }}
        
        .intro h2 {{
            color: #283593;
            margin-bottom: 15px;
            font-size: 1.8em;
        }}
        
        .story-section {{
            margin-bottom: 50px;
            padding: 30px;
            background: #fafafa;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .story-section h2 {{
            color: #283593;
            font-size: 2em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #283593;
        }}
        
        .story-section h3 {{
            color: #3949ab;
            font-size: 1.4em;
            margin-top: 25px;
            margin-bottom: 15px;
        }}
        
        .chart-container {{
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 5px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .chart-caption {{
            margin-top: 15px;
            font-style: italic;
            color: #666;
            font-size: 0.9em;
        }}
        
        .insight-box {{
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 5px solid #2196f3;
        }}
        
        .insight-box h4 {{
            color: #1976d2;
            margin-bottom: 10px;
            font-size: 1.2em;
        }}
        
        .stat-highlight {{
            display: inline-block;
            background: #283593;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            margin: 5px;
        }}
        
        .two-column {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin: 30px 0;
        }}
        
        @media (max-width: 768px) {{
            .two-column {{
                grid-template-columns: 1fr;
            }}
            
            header h1 {{
                font-size: 1.8em;
            }}
        }}
        
        footer {{
            text-align: center;
            padding: 30px;
            background: #f5f5f5;
            margin-top: 50px;
            border-radius: 10px;
            color: #666;
        }}
        
        .key-findings {{
            background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
            padding: 25px;
            border-radius: 10px;
            margin: 30px 0;
            border-left: 5px solid #ff9800;
        }}
        
        .key-findings h3 {{
            color: #e65100;
            margin-bottom: 15px;
        }}
        
        .key-findings ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .key-findings li {{
            padding: 10px;
            margin: 5px 0;
            background: white;
            border-radius: 5px;
            border-left: 3px solid #ff9800;
        }}
        
        .data-quality-alert {{
            background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 5px solid #f44336;
        }}
        
        .data-quality-alert h4 {{
            color: #c62828;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 DHA Data Analytics Story</h1>
            <p>Department of Home Affairs - South Africa</p>
            <p style="font-size: 0.9em; margin-top: 10px; opacity: 0.8;">
                Insights from Population Registry and Application Data Analysis
            </p>
        </header>
        
        <div class="intro">
            <h2>Welcome to the Data Story</h2>
            <p>
                This interactive dashboard presents key insights from the Department of Home Affairs 
                synthetic datasets. Through comprehensive data analysis, we uncover patterns, trends, 
                and data quality issues that inform decision-making and operational improvements.
            </p>
            <p style="margin-top: 15px;">
                <strong>Dataset Overview:</strong> Our analysis covers population registry records and 
                DHA application data, revealing demographic patterns, application trends, revenue insights, 
                and critical data quality metrics.
            </p>
        </div>
        
        <!-- Population Insights -->
        <div class="story-section">
            <h2>👥 Population Registry Insights</h2>
            
            <h3>Gender Distribution: A Balanced Perspective</h3>
            <p>
                Understanding the gender composition of our population registry is fundamental to 
                ensuring equitable service delivery. The distribution reveals important demographic 
                patterns that inform resource allocation and policy development.
            </p>
"""
    
    # Add gender distribution chart if it exists
    if f'{prefix}population_gender_distribution.png' in existing_images:
        html_content += f"""
            <div class="chart-container">
                <img src="{prefix}population_gender_distribution.png" alt="Gender Distribution">
                <p class="chart-caption">Gender distribution across the population registry</p>
            </div>
"""
    
    html_content += """
            <div class="insight-box">
                <h4>💡 Key Insight</h4>
                <p>
                    A balanced gender distribution ensures that DHA services are accessible and 
                    relevant to all citizens. This data helps identify any potential gaps in 
                    service delivery or registration patterns that may require attention.
                </p>
            </div>
            
            <h3>Generational Patterns: Birth Year Analysis</h3>
            <p>
                Analyzing birth years provides crucial insights into the age structure of our 
                registered population. Understanding generational distribution helps predict 
                future service demands, particularly for ID card renewals and passport applications.
            </p>
"""
    
    # Add birth year chart if it exists
    if f'{prefix}population_birth_year_distribution.png' in existing_images:
        html_content += f"""
            <div class="chart-container">
                <img src="{prefix}population_birth_year_distribution.png" alt="Birth Year Distribution">
                <p class="chart-caption">Distribution of birth years in the population registry</p>
            </div>
"""
    
    html_content += """
            <div class="insight-box">
                <h4>📈 Strategic Planning Insight</h4>
                <p>
                    The 1975 cutoff analysis helps identify citizens who may be approaching 
                    milestones requiring updated documentation. This enables proactive service 
                    planning and resource allocation for peak application periods.
                </p>
            </div>
        </div>
        
        <!-- Application Insights -->
        <div class="story-section">
            <h2>📋 DHA Applications: Trends and Patterns</h2>
            
            <h3>Geographic Distribution: Where Are Applications Coming From?</h3>
            <p>
                Understanding provincial application patterns is essential for optimizing branch 
                locations, staffing levels, and service delivery. Geographic analysis reveals 
                regional demand and helps identify areas requiring additional resources.
            </p>
"""
    
    # Add province chart if it exists
    if f'{prefix}applications_by_province.png' in existing_images:
        html_content += f"""
            <div class="chart-container">
                <img src="{prefix}applications_by_province.png" alt="Applications by Province">
                <p class="chart-caption">Total number of applications received by province</p>
            </div>
"""
    
    html_content += """
            <div class="insight-box">
                <h4>🗺️ Geographic Intelligence</h4>
                <p>
                    Provincial application volumes directly inform infrastructure planning. 
                    High-volume provinces may require additional branches, extended hours, or 
                    enhanced online services to meet citizen demand effectively.
                </p>
            </div>
            
            <h3>Application Status: Tracking the Journey</h3>
            <p>
                Monitoring application statuses provides visibility into processing efficiency 
                and helps identify bottlenecks in the workflow. Understanding status distribution 
                enables targeted improvements to reduce processing times.
            </p>
"""
    
    # Add status chart if it exists
    if f'{prefix}applications_by_status.png' in existing_images:
        html_content += f"""
            <div class="chart-container">
                <img src="{prefix}applications_by_status.png" alt="Application Status Distribution">
                <p class="chart-caption">Distribution of application statuses across all applications</p>
            </div>
"""
    
    html_content += """
            <div class="insight-box">
                <h4>⚡ Operational Efficiency</h4>
                <p>
                    Status distribution analysis helps identify process improvements. High 
                    percentages of "Pending" or "In Progress" statuses may indicate capacity 
                    constraints, while "Unknown" statuses highlight data quality issues requiring 
                    attention.
                </p>
            </div>
            
            <h3>Branch Performance: Top Performers</h3>
            <p>
                Identifying high-performing branches provides opportunities for best practice 
                sharing and capacity planning. Understanding branch-level volumes helps optimize 
                resource allocation and service delivery models.
            </p>
"""
    
    # Add branch chart if it exists
    if f'{prefix}applications_by_branch.png' in existing_images:
        html_content += f"""
            <div class="chart-container">
                <img src="{prefix}applications_by_branch.png" alt="Top Branches">
                <p class="chart-caption">Top 15 DHA branches by application volume</p>
            </div>
"""
    
    html_content += """
            <div class="insight-box">
                <h4>🏆 Performance Benchmarking</h4>
                <p>
                    Top-performing branches can serve as models for operational excellence. 
                    Analyzing their practices, staffing models, and service delivery approaches 
                    can inform improvements across the entire branch network.
                </p>
            </div>
        </div>
        
        <!-- Financial Insights -->
        <div class="story-section">
            <h2>💰 Revenue Analysis: Financial Impact</h2>
            
            <h3>Revenue Breakdown: ID Cards vs Passports</h3>
            <p>
                Understanding revenue streams from different application types is crucial for 
                financial planning and resource allocation. The cost breakdown reveals the 
                economic impact of DHA services and helps inform pricing strategies.
            </p>
"""
    
    # Add cost breakdown chart if it exists
    if f'{prefix}applications_cost_breakdown.png' in existing_images:
        html_content += f"""
            <div class="chart-container">
                <img src="{prefix}applications_cost_breakdown.png" alt="Cost Breakdown">
                <p class="chart-caption">Revenue analysis: ID Card applications (R350) vs Passport applications (R650)</p>
            </div>
"""
    
    html_content += """
            <div class="insight-box">
                <h4>💵 Financial Intelligence</h4>
                <p>
                    Revenue analysis demonstrates the significant financial contribution of 
                    DHA services. ID cards, while lower in individual value, may represent 
                    higher volume, while passports contribute substantial revenue per application. 
                    This balance informs strategic service delivery decisions.
                </p>
            </div>
            
            <div class="key-findings">
                <h3>💡 Key Financial Findings</h3>
                <ul>
                    <li><strong>ID Card Revenue:</strong> Lower per-unit value but potentially higher volume</li>
                    <li><strong>Passport Revenue:</strong> Higher per-unit value, significant total contribution</li>
                    <li><strong>Total Revenue Impact:</strong> Demonstrates the economic value of efficient service delivery</li>
                </ul>
            </div>
        </div>
        
        <!-- Data Quality Insights -->
        <div class="story-section">
            <h2>🔍 Data Quality: Ensuring Data Integrity</h2>
            
            <h3>Duplicate Applications: Identifying Data Quality Issues</h3>
            <p>
                Data quality is fundamental to effective decision-making. Identifying duplicate 
                applications helps ensure accurate reporting, prevents processing errors, and 
                maintains the integrity of our citizen records.
            </p>
"""
    
    # Add duplicates chart if it exists
    if f'{prefix}applications_duplicates.png' in existing_images:
        html_content += f"""
            <div class="chart-container">
                <img src="{prefix}applications_duplicates.png" alt="Duplicate Applications">
                <p class="chart-caption">Analysis of duplicate application records</p>
            </div>
"""
    
    html_content += """
            <div class="data-quality-alert">
                <h4>⚠️ Data Quality Alert</h4>
                <p>
                    Duplicate applications represent a critical data quality issue that requires 
                    attention. These duplicates can lead to:
                </p>
                <ul style="margin-top: 10px; padding-left: 20px;">
                    <li>Inaccurate reporting and analytics</li>
                    <li>Resource waste in processing</li>
                    <li>Potential service delivery delays</li>
                    <li>Compliance and audit concerns</li>
                </ul>
            </div>
            
            <div class="insight-box">
                <h4>🛠️ Remediation Strategy</h4>
                <p>
                    Identifying duplicate patterns enables targeted data cleaning initiatives. 
                    Implementing automated duplicate detection during application submission can 
                    prevent future occurrences and improve overall data quality.
                </p>
            </div>
        </div>
        
        <!-- Key Takeaways -->
        <div class="story-section">
            <h2>🎯 Key Takeaways and Recommendations</h2>
            
            <div class="two-column">
                <div>
                    <h3>Operational Recommendations</h3>
                    <ul style="list-style: none; padding-left: 0;">
                        <li style="padding: 10px; margin: 5px 0; background: #e3f2fd; border-radius: 5px;">
                            <strong>📍 Geographic Optimization:</strong> Allocate resources based on provincial demand patterns
                        </li>
                        <li style="padding: 10px; margin: 5px 0; background: #e3f2fd; border-radius: 5px;">
                            <strong>⚙️ Process Improvement:</strong> Address bottlenecks identified in status distribution
                        </li>
                        <li style="padding: 10px; margin: 5px 0; background: #e3f2fd; border-radius: 5px;">
                            <strong>🏢 Branch Excellence:</strong> Leverage top-performing branch practices across the network
                        </li>
                    </ul>
                </div>
                
                <div>
                    <h3>Data Quality Actions</h3>
                    <ul style="list-style: none; padding-left: 0;">
                        <li style="padding: 10px; margin: 5px 0; background: #fff3e0; border-radius: 5px;">
                            <strong>🔧 Duplicate Resolution:</strong> Implement automated duplicate detection systems
                        </li>
                        <li style="padding: 10px; margin: 5px 0; background: #fff3e0; border-radius: 5px;">
                            <strong>✅ Data Validation:</strong> Enhance validation rules during data entry
                        </li>
                        <li style="padding: 10px; margin: 5px 0; background: #fff3e0; border-radius: 5px;">
                            <strong>📊 Monitoring:</strong> Establish ongoing data quality monitoring processes
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        
        <footer>
            <p><strong>DHA Data Analytics Dashboard</strong></p>
            <p>Generated on """ + datetime.now().strftime("%B %d, %Y at %I:%M %p") + """</p>
            <p style="margin-top: 15px; font-size: 0.9em; color: #999;">
                This dashboard presents insights from synthetic DHA datasets created for 
                data analytics and data quality training purposes.
            </p>
        </footer>
    </div>
</body>
</html>
"""
    
    # Write HTML file
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ HTML data story created: {html_path}")
    print(f"  Includes {len(existing_images)} chart images")
    if len(existing_images) < len(image_files):
        print(f"  Warning: {len(image_files) - len(existing_images)} images not found")
        print(f"  Run analyze_dha_datasets.py first to generate all charts")


def main():
    """
    Main function to generate the HTML data story.
    """
    parser = argparse.ArgumentParser(
        description='Generate HTML one-pager with data stories',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '-b', '--big-data',
        action='store_true',
        help='Use big data chart images (big_data_* files)'
    )
    args = parser.parse_args()
    
    print("="*70)
    print("DHA DATA STORY HTML GENERATOR")
    print("Department of Home Affairs - South Africa")
    print("="*70)
    
    try:
        create_html_story(big_data=args.big_data)
        print("\n✓ HTML generation completed successfully!")
        print("="*70)
        print(f"\nOpen the HTML file in your browser to view the data story:")
        if args.big_data:
            print(f"  file://{os.path.abspath(os.path.join(OUTPUT_DIR, 'big_data_dha_data_story.html'))}")
        else:
            print(f"  file://{os.path.abspath(os.path.join(OUTPUT_DIR, 'dha_data_story.html'))}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

