from django.db.models import Sum, Count
from ..models.cost import ProjectCost
from ..models.project import Project

class ReportingService:
    @staticmethod
    def get_project_cost_summary(project_id):
        return ProjectCost.objects.filter(
            project_id=project_id
        ).aggregate(
            total_cost=Sum('amount'),
            cost_count=Count('id'),
            average_cost=Sum('amount') / Count('id')
        )
    
    @staticmethod
    def get_project_with_costs(project_id):
        try:
            project = Project.objects.prefetch_related('costs').get(id=project_id)
            costs = project.costs.all()
            total_cost = sum(cost.amount for cost in costs)
            
            return {
                'project': project,
                'costs': costs,
                'total_cost': total_cost,
                'cost_count': len(costs),
                'average_cost': total_cost / len(costs) if costs else 0
            }
        except Project.DoesNotExist:
            return None

    @staticmethod
    def generate_cost_report(project_id):
        data = ReportingService.get_project_with_costs(project_id)
        if not data:
            return None
            
        report = {
            'project_name': data['project'].name,
            'project_description': data['project'].description,
            'total_cost': data['total_cost'],
            'cost_count': data['cost_count'],
            'average_cost': data['average_cost'],
            'costs': []
        }
        
        for cost in data['costs']:
            report['costs'].append({
                'name': cost.name,
                'amount': cost.amount,
                'description': cost.description,
                'asset': cost.asset.name if cost.asset else None,
                'created_at': cost.created_at
            })
            
        return report