from django.core.exceptions import ObjectDoesNotExist
from ..models.project import Project
from ..models.cost import ProjectCost
# services/project_service.py
class ProjectService:
    @staticmethod
    def get_all_projects():
        return Project.objects.select_related('farm', 'parent_project')
    
    @staticmethod
    def get_project_by_id(project_id):
        try:
            return Project.objects.select_related('farm').get(id=project_id)
        except Project.DoesNotExist:
            return None
    
    @staticmethod
    def create_project(project_data):
        project = Project(**project_data)
        project.full_clean()
        project.save()
        return project
    
    @staticmethod
    def update_project(project_id, project_data):
        project = ProjectService.get_project_by_id(project_id)
        if project:
            for field, value in project_data.items():
                setattr(project, field, value)
            project.full_clean()
            project.save()
        return project