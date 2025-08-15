from rest_framework import serializers
from .models import User, Kudo

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "display_name",
            "organization_id",
            "is_staff",
            "is_superuser",
        ]

class MeSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(source="organization.name", allow_null=True)
    class Meta:
        model = User
        fields = ["id", "username", "display_name", "organization"]

class KudoSerializer(serializers.ModelSerializer):
    from_user = UserSimpleSerializer(read_only=True)
    to_user = UserSimpleSerializer(read_only=True)
    to_user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source="to_user"
    )

    class Meta:
        model = Kudo
        fields = ["id", "from_user", "to_user", "to_user_id", "message", "created_at", "year", "week"]
        read_only_fields = ["id", "from_user", "created_at", "year", "week"]

    def validate(self, attrs):
        req = self.context["request"]
        to_user = attrs["to_user"]
        if req.user.organization_id != to_user.organization_id:
            raise serializers.ValidationError("Can only give kudos within your organization.")
        if req.user.id == to_user.id:
            raise serializers.ValidationError("You cannot give kudos to yourself.")
        return attrs

    def create(self, validated_data):
        req = self.context["request"]
        return Kudo.objects.create(from_user=req.user, **validated_data)
