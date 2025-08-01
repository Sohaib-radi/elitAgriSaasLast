from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models.asset import Asset
from ..serializers.asset import AssetSerializer, AssetCreateUpdateSerializer
from ..services.asset_service import AssetService
from core.viewsets.base import AutoPermissionViewSet

class AssetViewSet(AutoPermissionViewSet):
    permission_module = "crop"
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AssetCreateUpdateSerializer
        return AssetSerializer
    
    def get_queryset(self):
        return super().get_queryset().filter(
            farm=self.request.user.active_farm
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.farm != request.user.active_farm:
            return Response(
                {'detail': 'Asset not found or not accessible'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        asset = AssetService.create_asset({
            **serializer.validated_data,
            'farm': request.user.active_farm
        })
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            AssetSerializer(asset, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.farm != request.user.active_farm:
            return Response(
                {'detail': 'Asset not found or not accessible'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)

        # ✅ REMOVE 'farm' manually before the check
        serializer.validated_data.pop('farm', None)

        if 'farm' in serializer.validated_data:
            return Response(
                {'detail': 'Cannot change farm association'},
                status=status.HTTP_403_FORBIDDEN
            )

        updated_asset = AssetService.update_asset(
            instance.pk,
            serializer.validated_data
        )

        return Response(
            AssetSerializer(updated_asset, context={'request': request}).data
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.farm != request.user.active_farm:
            return Response(
                {'detail': 'Asset not found or not accessible'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        AssetService.delete_asset(instance.pk)
        return Response(status=status.HTTP_204_NO_CONTENT)