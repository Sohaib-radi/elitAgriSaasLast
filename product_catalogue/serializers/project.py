from rest_framework import serializers
from product_catalogue.models.project import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "end_date",
           
            
        ]
        read_only_fields = ["id", "created_at"]
