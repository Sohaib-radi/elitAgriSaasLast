from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models.cost import ProjectCost
from ..serializers.cost import ProjectCostSerializer, ProjectCostCreateUpdateSerializer
from ..services.cost_service import ProjectCostService
from core.viewsets.base import AutoPermissionViewSet

class ProjectCostViewSet(AutoPermissionViewSet):
    permission_module = "crop"
    queryset = ProjectCost.objects.all()
    serializer_class = ProjectCostSerializer
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProjectCostCreateUpdateSerializer
        return ProjectCostSerializer
    
    def get_queryset(self):
        return super().get_queryset().filter(
            farm=self.request.user.active_farm
        ).select_related('project', 'asset')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.farm != request.user.active_farm:
            return Response(
                {'detail': 'Project cost not found or not accessible'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Verify project belongs to farm
        project = serializer.validated_data['project']
        if project.farm != request.user.active_farm:
            return Response(
                {'detail': 'Project not accessible'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Verify asset belongs to farm (if provided)
        if 'asset' in serializer.validated_data and serializer.validated_data['asset']:
            if serializer.validated_data['asset'].farm != request.user.active_farm:
                return Response(
                    {'detail': 'Asset not accessible'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        cost = ProjectCostService.create_cost({
            **serializer.validated_data,
            'farm': request.user.active_farm
        })
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            ProjectCostSerializer(cost, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        if instance.farm != request.user.active_farm:
            return Response(
                {'detail': 'Project cost not found or not accessible'},
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
        
        # Validate project belongs to farm
        if 'project' in serializer.validated_data:
            project = serializer.validated_data['project']
            if project.farm != request.user.active_farm:
                return Response(
                    {'detail': 'Project not accessible'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        # Validate asset belongs to farm (if provided)
        if 'asset' in serializer.validated_data and serializer.validated_data['asset']:
            if serializer.validated_data['asset'].farm != request.user.active_farm:
                return Response(
                    {'detail': 'Asset not accessible'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        updated_cost = ProjectCostService.update_cost(
            instance.pk,
            serializer.validated_data
        )
        
        return Response(
            ProjectCostSerializer(updated_cost, context={'request': request}).data
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.farm != request.user.active_farm:
            return Response(
                {'detail': 'Project cost not found or not accessible'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        ProjectCostService.delete_cost(instance.pk)
        return Response(status=status.HTTP_204_NO_CONTENT)