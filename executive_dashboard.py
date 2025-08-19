import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime, timedelta
import json

class ExecutiveDashboard:
    def __init__(self):
        self.colors = {
            'primary': '#1f77b4',
            'success': '#2ca02c', 
            'warning': '#ff7f0e',
            'danger': '#d62728',
            'info': '#17becf',
            'secondary': '#7f7f7f'
        }
        
    def create_executive_dashboard(self):
        """Create a comprehensive executive dashboard"""
        print("Creating Executive Dashboard for Leadership...")
        
        # Create the main dashboard with multiple sections
        fig = make_subplots(
            rows=4, cols=3,
            subplot_titles=[
                'Enrollment Forecast Overview', 'Budget Impact Analysis', 'Student Success Metrics',
                'Department Performance', 'Risk Assessment', 'ROI Projections',
                'Resource Utilization', 'Trend Analysis', 'Capacity Planning',
                'Key Performance Indicators', 'Competitive Positioning', 'Strategic Recommendations'
            ],
            specs=[
                [{"type": "indicator"}, {"type": "bar"}, {"type": "scatter"}],
                [{"type": "pie"}, {"type": "indicator"}, {"type": "bar"}],
                [{"type": "scatter"}, {"type": "scatter"}, {"type": "bar"}],
                [{"colspan": 3}, None, None]
            ],
            vertical_spacing=0.08,
            horizontal_spacing=0.1
        )
        
        # Generate sample executive data
        exec_data = self.generate_executive_data()
        
        # 1. Enrollment Forecast Overview (KPI Card)
        fig.add_trace(go.Indicator(
            mode="number+delta+gauge",
            value=exec_data['total_predicted_enrollment'],
            delta={'reference': exec_data['last_year_enrollment'], 'relative': True},
            title={'text': "Total Predicted Enrollment"},
            gauge={'axis': {'range': [3000, 6000]},
                   'bar': {'color': self.colors['primary']},
                   'steps': [{'range': [3000, 4000], 'color': "lightgray"},
                            {'range': [4000, 5000], 'color': "gray"}],
                   'threshold': {'line': {'color': "red", 'width': 4},
                               'thickness': 0.75, 'value': 5500}}
        ), row=1, col=1)
        
        # 2. Budget Impact Analysis
        budget_data = exec_data['budget_impact']
        fig.add_trace(go.Bar(
            x=list(budget_data.keys()),
            y=list(budget_data.values()),
            marker_color=[self.colors['success'] if v > 0 else self.colors['danger'] for v in budget_data.values()],
            name="Budget Changes"
        ), row=1, col=2)
        
        # 3. Student Success Metrics
        success_data = exec_data['success_metrics']
        fig.add_trace(go.Scatter(
            x=list(success_data.keys()),
            y=[v['retention_rate'] for v in success_data.values()],
            mode='markers+lines',
            marker=dict(size=[v['student_count']/10 for v in success_data.values()]),
            name="Retention Rate by Major"
        ), row=1, col=3)
        
        # 4. Department Performance (Pie Chart)
        dept_performance = exec_data['department_performance']
        fig.add_trace(go.Pie(
            labels=list(dept_performance.keys()),
            values=list(dept_performance.values()),
            name="Department Enrollment Share"
        ), row=2, col=1)
        
        # 5. Risk Assessment (KPI)
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=exec_data['risk_score'],
            title={'text': "Overall Risk Score"},
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': self.colors['warning']},
                   'steps': [{'range': [0, 30], 'color': self.colors['success']},
                            {'range': [30, 70], 'color': self.colors['warning']},
                            {'range': [70, 100], 'color': self.colors['danger']}]}
        ), row=2, col=2)
        
        # 6. ROI Projections
        roi_data = exec_data['roi_projections']
        fig.add_trace(go.Bar(
            x=list(roi_data.keys()),
            y=list(roi_data.values()),
            marker_color=self.colors['success'],
            name="ROI by Initiative"
        ), row=2, col=3)
        
        # 7. Resource Utilization
        utilization = exec_data['resource_utilization']
        fig.add_trace(go.Scatter(
            x=list(utilization.keys()),
            y=[v['current'] for v in utilization.values()],
            mode='markers',
            marker=dict(size=15, color=self.colors['primary']),
            name="Current Utilization"
        ), row=3, col=1)
        
        # 8. Trend Analysis
        trends = exec_data['enrollment_trends']
        fig.add_trace(go.Scatter(
            x=list(trends.keys()),
            y=list(trends.values()),
            mode='lines+markers',
            line=dict(color=self.colors['info']),
            name="5-Year Enrollment Trend"
        ), row=3, col=2)
        
        # 9. Capacity Planning
        capacity = exec_data['capacity_analysis']
        fig.add_trace(go.Bar(
            x=list(capacity.keys()),
            y=[v['shortage'] for v in capacity.values()],
            marker_color=self.colors['warning'],
            name="Capacity Shortage"
        ), row=3, col=3)
        
        # 10. Strategic KPIs Table (Bottom section)
        kpi_table = self.create_kpi_table(exec_data['strategic_kpis'])
        fig.add_trace(go.Table(
            header=dict(values=['KPI', 'Current', 'Target', 'Status', 'Trend'],
                       fill_color=self.colors['primary'],
                       font=dict(color='white', size=12)),
            cells=dict(values=[kpi_table[col] for col in kpi_table.columns],
                      fill_color='lightgray',
                      align="center")
        ), row=4, col=1)
        
        # Update layout
        fig.update_layout(
            height=1400,
            title={
                'text': "Student Enrollment Prediction System - Executive Dashboard",
                'x': 0.5,
                'font': {'size': 24, 'color': self.colors['primary']}
            },
            showlegend=False,
            font=dict(size=10)
        )
        
        # Save dashboard
        fig.write_html('executive_dashboard.html')
        print("Executive dashboard saved as 'executive_dashboard.html'")
        
        return fig
    
    def generate_executive_data(self):
        """Generate realistic executive-level data"""
        return {
            'total_predicted_enrollment': 4750,
            'last_year_enrollment': 4520,
            'budget_impact': {
                'Computer Science': 250000,
                'Engineering': 180000,
                'Business': 75000,
                'Liberal Arts': -50000,
                'Sciences': 100000
            },
            'success_metrics': {
                'Computer Science': {'retention_rate': 88, 'student_count': 850},
                'Engineering': {'retention_rate': 82, 'student_count': 720},
                'Business': {'retention_rate': 91, 'student_count': 1200},
                'Psychology': {'retention_rate': 85, 'student_count': 650},
                'Biology': {'retention_rate': 79, 'student_count': 480}
            },
            'department_performance': {
                'Computer Science': 28,
                'Business': 32,
                'Engineering': 22,
                'Liberal Arts': 12,
                'Sciences': 6
            },
            'risk_score': 35,
            'roi_projections': {
                'Capacity Optimization': 340000,
                'Retention Programs': 890000,
                'Resource Allocation': 520000,
                'Faculty Planning': 230000
            },
            'resource_utilization': {
                'Classrooms': {'current': 78, 'optimal': 85},
                'Faculty': {'current': 92, 'optimal': 88},
                'Labs': {'current': 65, 'optimal': 80},
                'Study Spaces': {'current': 88, 'optimal': 85}
            },
            'enrollment_trends': {
                2020: 4200,
                2021: 4350,
                2022: 4420,
                2023: 4520,
                2024: 4750
            },
            'capacity_analysis': {
                'Computer Science': {'shortage': 45},
                'Engineering': {'shortage': 32},
                'Business': {'shortage': 12},
                'Liberal Arts': {'shortage': -8},
                'Sciences': {'shortage': 18}
            },
            'strategic_kpis': {
                'Student Retention Rate': {'current': '84.2%', 'target': '87%', 'status': 'On Track', 'trend': '↗'},
                'Prediction Accuracy': {'current': '91.5%', 'target': '95%', 'status': 'Good', 'trend': '↗'},
                'Resource Efficiency': {'current': '78%', 'target': '85%', 'status': 'Needs Attention', 'trend': '→'},
                'Cost per Student': {'current': '$12,450', 'target': '$11,800', 'status': 'Monitor', 'trend': '↘'},
                'Faculty Utilization': {'current': '89%', 'target': '85%', 'status': 'Excellent', 'trend': '↗'}
            }
        }
    
    def create_kpi_table(self, kpi_data):
        """Create a formatted KPI table"""
        data = []
        for kpi, values in kpi_data.items():
            data.append([
                kpi,
                values['current'],
                values['target'],
                values['status'],
                values['trend']
            ])
        
        return pd.DataFrame(data, columns=['KPI', 'Current', 'Target', 'Status', 'Trend'])
    
    def create_financial_impact_report(self):
        """Create a detailed financial impact visualization"""
        print("Creating Financial Impact Report...")
        
        # Financial data
        financial_data = {
            'cost_savings': {
                'Optimized Faculty Allocation': 450000,
                'Efficient Space Utilization': 280000,
                'Reduced Administrative Overhead': 120000,
                'Better Resource Planning': 180000
            },
            'revenue_gains': {
                'Improved Retention': 890000,
                'Increased Enrollment': 650000,
                'Program Optimization': 340000,
                'Strategic Partnerships': 120000
            },
            'investment_required': {
                'System Development': 150000,
                'Training and Implementation': 75000,
                'Ongoing Maintenance': 50000,
                'Data Infrastructure': 25000
            }
        }
        
        # Create financial dashboard
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[
                'Cost Savings Breakdown',
                'Revenue Enhancement',
                'Investment Requirements',
                'Net ROI Analysis'
            ],
            specs=[[{"type": "pie"}, {"type": "bar"}],
                   [{"type": "pie"}, {"type": "waterfall"}]]
        )
        
        # Cost savings pie chart
        fig.add_trace(go.Pie(
            labels=list(financial_data['cost_savings'].keys()),
            values=list(financial_data['cost_savings'].values()),
            name="Cost Savings",
            marker_colors=['#2ca02c', '#17becf', '#ff7f0e', '#9467bd']
        ), row=1, col=1)
        
        # Revenue gains bar chart
        fig.add_trace(go.Bar(
            x=list(financial_data['revenue_gains'].keys()),
            y=list(financial_data['revenue_gains'].values()),
            marker_color='#1f77b4',
            name="Revenue Gains"
        ), row=1, col=2)
        
        # Investment pie chart
        fig.add_trace(go.Pie(
            labels=list(financial_data['investment_required'].keys()),
            values=list(financial_data['investment_required'].values()),
            name="Investment",
            marker_colors=['#d62728', '#ff7f0e', '#bcbd22', '#e377c2']
        ), row=2, col=1)
        
        # ROI waterfall chart
        total_savings = sum(financial_data['cost_savings'].values())
        total_revenue = sum(financial_data['revenue_gains'].values())
        total_investment = sum(financial_data['investment_required'].values())
        net_benefit = total_savings + total_revenue - total_investment
        
        fig.add_trace(go.Waterfall(
            name="ROI Analysis",
            orientation="v",
            measure=["relative", "relative", "relative", "total"],
            x=["Cost Savings", "Revenue Gains", "Investment", "Net Benefit"],
            y=[total_savings, total_revenue, -total_investment, net_benefit],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ), row=2, col=2)
        
        fig.update_layout(
            height=800,
            title="Financial Impact Analysis - Student Enrollment Prediction System",
            showlegend=True
        )
        
        fig.write_html('financial_impact_report.html')
        print("Financial impact report saved as 'financial_impact_report.html'")
        
        return fig
    
    def generate_executive_briefing(self):
        """Generate an automated executive briefing document"""
        briefing = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'summary': {
                'total_enrollment_prediction': 4750,
                'growth_rate': '+5.1%',
                'confidence_level': '91.5%',
                'departments_at_capacity': 3,
                'budget_optimization_potential': '$1.2M'
            },
            'key_insights': [
                'Computer Science enrollment expected to grow 18% next semester',
                'Liberal Arts showing declining trend, intervention recommended',
                'Classroom capacity shortage identified in STEM departments',
                'Student retention programs showing 2.3% improvement',
                'Budget allocation accuracy improved by 35%'
            ],
            'action_items': [
                'Allocate additional faculty to Computer Science department',
                'Implement retention programs for Liberal Arts students',
                'Plan for additional STEM classroom capacity',
                'Review resource allocation for declining programs',
                'Continue monitoring prediction accuracy'
            ],
            'risks': [
                'Potential faculty shortage in high-demand departments',
                'Infrastructure strain from enrollment growth',
                'Budget constraints for expansion programs'
            ],
            'opportunities': [
                'Expand popular programs to capture market demand',
                'Optimize underutilized resources',
                'Develop new programs based on trend analysis'
            ]
        }
        
        # Save as JSON for API consumption
        with open('executive_briefing.json', 'w') as f:
            json.dump(briefing, f, indent=2)
        
        # Create markdown report
        markdown_report = f"""# Executive Briefing - Student Enrollment Prediction System
## Date: {briefing['date']}

### Executive Summary
- **Total Predicted Enrollment**: {briefing['summary']['total_enrollment_prediction']} students
- **Growth Rate**: {briefing['summary']['growth_rate']} from previous year
- **Prediction Confidence**: {briefing['summary']['confidence_level']}
- **Departments at Capacity**: {briefing['summary']['departments_at_capacity']}
- **Budget Optimization Potential**: {briefing['summary']['budget_optimization_potential']}

### Key Insights
"""
        for insight in briefing['key_insights']:
            markdown_report += f"- {insight}\n"
        
        markdown_report += "\n### Immediate Action Items\n"
        for item in briefing['action_items']:
            markdown_report += f"- [ ] {item}\n"
        
        markdown_report += "\n### Risk Assessment\n"
        for risk in briefing['risks']:
            markdown_report += f"- ⚠️ {risk}\n"
        
        markdown_report += "\n### Strategic Opportunities\n"
        for opportunity in briefing['opportunities']:
            markdown_report += f"- 💡 {opportunity}\n"
        
        with open('executive_briefing.md', 'w') as f:
            f.write(markdown_report)
        
        print("Executive briefing generated:")
        print("- executive_briefing.json (API format)")
        print("- executive_briefing.md (readable format)")
        
        return briefing

if __name__ == "__main__":
    dashboard = ExecutiveDashboard()
    
    # Create all executive reports
    print("=== GENERATING EXECUTIVE REPORTS ===\n")
    
    # Main dashboard
    dashboard.create_executive_dashboard()
    
    # Financial impact
    dashboard.create_financial_impact_report()
    
    # Executive briefing
    dashboard.generate_executive_briefing()
    
    print("\n=== EXECUTIVE REPORTING COMPLETE ===")
    print("Files generated for leadership:")
    print("- executive_dashboard.html (Interactive dashboard)")
    print("- financial_impact_report.html (ROI analysis)")
    print("- executive_briefing.md (Summary report)")
    print("- executive_briefing.json (API data)")