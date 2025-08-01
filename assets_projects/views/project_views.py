from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models.project import Project
from ..serializers.project import ProjectDetailSerializer, ProjectSerializer, ProjectCreateUpdateSerializer, ProjectWithAssetsAndCostsSerializer
from ..services.project_service import ProjectService
from core.viewsets.base import AutoPermissionViewSet
from rest_framework.decorators import action

class ProjectViewSet(AutoPermissionViewSet):
    permission_module = "crop"
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def get_serializer_class(self):
        if self.action == 'create' and (
            'assets' in self.request.data or 'costs' in self.request.data
        ):
            print("ProjectWithAssetsAndCostsSerializer Used")
            return ProjectWithAssetsAndCostsSerializer
        elif self.action == 'retrieve':
            print("ProjectDetailSerializer Used")
            return ProjectDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            print("ProjectCreateUpdateSerializer Used")
            return ProjectCreateUpdateSerializer
        print("ProjectSerializer Used") 
        return ProjectSerializer
    
    def get_queryset(self):
        return super().get_queryset().filter(
            farm=self.request.user.active_farm
        ).select_related('parent_project')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.farm != request.user.active_farm:
            return Response(
                {'detail': 'Project not found or not accessible'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if isinstance(serializer, ProjectWithAssetsAndCostsSerializer):
            result = serializer.save()
            project = result["project"]
            serialized = ProjectSerializer(project, context={'request': request}).data
            return Response(
                serialized,
                status=status.HTTP_201_CREATED,
                headers=self.get_success_headers(serialized)
            )
        else:
            # Handle standard creation
            project = ProjectService.create_project({
                **serializer.validated_data,
                'farm': request.user.active_farm
            })
            return Response(
                ProjectSerializer(project, context={'request': request}).data,
                status=status.HTTP_201_CREATED,
                headers=self.get_success_headers(serializer.data)
            )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        if instance.farm != request.user.active_farm:
            return Response(
                {'detail': 'Project not found or not accessible'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(
            instance, 
            data=request.data, 
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        
        # Prevent farm modification
        if 'farm' in serializer.validated_data:
            return Response(
                {'detail': 'Cannot change farm association'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Validate parent project belongs to same farm
        if 'parent_project' in serializer.validated_data:
            parent = serializer.validated_data['parent_project']
            if parent and parent.farm != request.user.active_farm:
                return Response(
                    {'detail': 'Parent project not accessible'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        updated_project = ProjectService.update_project(
            instance.pk,
            serializer.validated_data
        )
        
        return Response(
            ProjectSerializer(updated_project, context={'request': request}).data
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.farm != request.user.active_farm:
            return Response(
                {'detail': 'Project not found or not accessible'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        ProjectService.delete_project(instance.pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'])
    def costs(self, request, pk=None):
        """Custom action to get project costs"""
        project = self.get_object()
        if project.farm != request.user.active_farm:
            return Response(
                {'detail': 'Project not found or not accessible'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        from ..serializers.cost import ProjectCostSerializer
        costs = project.costs.all()
        serializer = ProjectCostSerializer(
            costs, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
    


class SimpleProjectViewSet(AutoPermissionViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return super().get_queryset().filter(farm=self.request.user.active_farm)