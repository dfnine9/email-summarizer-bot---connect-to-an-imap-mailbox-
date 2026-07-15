```python
"""
Financial Data Visualization Generator

This module creates comprehensive spending analysis visualizations including:
- Spending breakdown pie charts
- Monthly trend line graphs  
- Category comparison bar charts

Features customizable date ranges and export options for financial data analysis.
Requires matplotlib for visualization capabilities.
"""

import json
import datetime
from typing import Dict, List, Tuple, Optional
import random

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.figure import Figure
except ImportError:
    print("Error: matplotlib is required but not installed")
    print("Install with: pip install matplotlib")
    exit(1)

class FinancialVisualizationGenerator:
    """Generator for financial spending visualizations with customizable options."""
    
    def __init__(self):
        """Initialize the visualization generator."""
        self.data = {}
        self.date_range = None
        
    def generate_sample_data(self, start_date: datetime.date, end_date: datetime.date) -> Dict:
        """Generate sample financial data for demonstration purposes."""
        categories = ['Food & Dining', 'Transportation', 'Shopping', 'Entertainment', 
                     'Bills & Utilities', 'Healthcare', 'Travel', 'Education']
        
        data = {}
        current_date = start_date
        
        while current_date <= end_date:
            month_key = current_date.strftime('%Y-%m')
            if month_key not in data:
                data[month_key] = {}
                
            for category in categories:
                # Generate realistic spending amounts
                base_amount = random.uniform(200, 1500)
                seasonal_factor = 1.0
                
                # Add seasonal variations
                if category == 'Travel' and current_date.month in [6, 7, 12]:
                    seasonal_factor = 1.8
                elif category == 'Bills & Utilities' and current_date.month in [12, 1, 2]:
                    seasonal_factor = 1.3
                    
                amount = base_amount * seasonal_factor * random.uniform(0.7, 1.3)
                data[month_key][category] = round(amount, 2)
                
            current_date = current_date.replace(day=28) + datetime.timedelta(days=4)
            current_date = current_date.replace(day=1)
            
        return data
    
    def create_pie_chart(self, data: Dict, title: str = "Spending Breakdown") -> Figure:
        """Create a pie chart showing spending breakdown by category."""
        try:
            # Aggregate data across all months in range
            category_totals = {}
            for month_data in data.values():
                for category, amount in month_data.items():
                    category_totals[category] = category_totals.get(category, 0) + amount
            
            if not category_totals:
                raise ValueError("No data available for pie chart")
            
            # Create pie chart
            fig, ax = plt.subplots(figsize=(10, 8))
            
            categories = list(category_totals.keys())
            amounts = list(category_totals.values())
            colors = plt.cm.Set3(range(len(categories)))
            
            wedges, texts, autotexts = ax.pie(amounts, labels=categories, autopct='%1.1f%%',
                                            colors=colors, startangle=90)
            
            # Enhance appearance
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            
            # Add legend with amounts
            legend_labels = [f'{cat}: ${amt:,.0f}' for cat, amt in category_totals.items()]
            ax.legend(wedges, legend_labels, title="Categories", loc="center left", 
                     bbox_to_anchor=(1, 0, 0.5, 1))
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            print(f"Error creating pie chart: {e}")
            raise
    
    def create_trend_chart(self, data: Dict, title: str = "Monthly Spending Trends") -> Figure:
        """Create a line chart showing monthly spending trends."""
        try:
            if not data:
                raise ValueError("No data available for trend chart")
            
            # Prepare data for plotting
            months = sorted(data.keys())
            categories = set()
            for month_data in data.values():
                categories.update(month_data.keys())
            categories = sorted(list(categories))
            
            # Convert month strings to datetime objects for plotting
            month_dates = [datetime.datetime.strptime(month, '%Y-%m') for month in months]
            
            fig, ax = plt.subplots(figsize=(12, 8))
            
            colors = plt.cm.tab10(range(len(categories)))
            
            for i, category in enumerate(categories):
                amounts = []
                for month in months:
                    amount = data[month].get(category, 0)
                    amounts.append(amount)
                
                ax.plot(month_dates, amounts, marker='o', linewidth=2, 
                       label=category, color=colors[i])
            
            # Format x-axis
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
            
            # Enhance appearance
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Month', fontweight='bold')
            ax.set_ylabel('Amount ($)', fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            
            # Format y-axis to show currency
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            print(f"Error creating trend chart: {e}")
            raise
    
    def create_comparison_chart(self, data: Dict, title: str = "Category Comparison") -> Figure:
        """Create a bar chart comparing spending across categories."""
        try:
            # Calculate monthly averages for each category
            category_totals = {}
            month_count = len(data)
            
            if month_count == 0:
                raise ValueError("No data available for comparison chart")
            
            for month_data in data.values():
                for category, amount in month_data.items():
                    category_totals[category] = category_totals.get(category, 0) + amount
            
            # Calculate averages
            category_averages = {cat: total/month_count for cat, total in category_totals.items()}
            
            # Sort by amount for better visualization
            sorted_categories = sorted(category_averages.items(), key=lambda x: x[1], reverse=True)
            
            fig, ax = plt.subplots(figsize=(12, 8))
            
            categories = [item[0] for item in sorted_categories]
            amounts = [item[1] for item in sorted_categories]
            colors = plt.cm.viridis(range(len(categories)))
            
            bars = ax.bar(categories, amounts, color=colors)
            
            # Add value labels on bars
            for bar, amount in zip(bars, amounts):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'${amount:,.0f}', ha='center', va='bottom', fontweight='bold')
            
            # Enhance appearance
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Category', fontweight='bold')
            ax.set_ylabel('Average Monthly Amount ($)',