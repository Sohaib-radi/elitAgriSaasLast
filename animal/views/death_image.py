from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from animal.models.death import AnimalDeath, AnimalDeathImage
from animal.serializers.death import AnimalDeathImageSerializer


class UploadDeathImageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        death_record = get_object_or_404(AnimalDeath, pk=pk, animal__farm=request.user.active_farm)

        images = request.FILES.getlist("images")
        created_images = []

        for image in images:
            img_obj = AnimalDeathImage.objects.create(death=death_record, image=image)
            created_images.append(img_obj)

        serializer = AnimalDeathImageSerializer(created_images, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
