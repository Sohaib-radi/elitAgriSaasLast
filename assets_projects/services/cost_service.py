# services/cost_service.py
from assets_projects.models.cost import ProjectCost


class ProjectCostService:
    @staticmethod
    def get_all_costs():
        return ProjectCost.objects.select_related('project', 'asset')
    
    @staticmethod
    def get_costs_by_project(project_id):
        return ProjectCost.objects.filter(project_id=project_id)
    
    @staticmethod 
    def get_cost_by_id(cost_id):
        try:
            return ProjectCost.objects.select_related('project', 'asset').get(id=cost_id)
        except ProjectCost.DoesNotExist:
            return None
    
    @staticmethod
    def create_cost(cost_data):
        cost = ProjectCost(**cost_data)
        cost.full_clean()
        cost.save()
        return cost
    
    @staticmethod
    def update_cost(cost_id, cost_data):
        cost = ProjectCostService.get_cost_by_id(cost_id)
        if cost:
            for field, value in cost_data.items():
                setattr(cost, field, value)
            cost.full_clean()
            cost.save()
        return cost