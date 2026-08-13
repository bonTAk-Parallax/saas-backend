
from rest_framework import serializers
from apps.core.models.base import TenantScopedModel


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            for field_name in exclude:
                self.fields.pop(field_name, None)


class TenantAwareModelSerializer(DynamicFieldsModelSerializer):
    """
    Two layers of defense, both generic — no per-field validate_* methods needed:
      1. __init__  -> scopes each related field's queryset to the user's org
                      (bad references never even validate as "exists")
      2. validate() -> explicit resolve_tenant() check on whatever survived #1
                      (catches anything #1's queryset filter didn't reach,
                       e.g. fields with a custom/overridden queryset)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        profile = getattr(getattr(request, "user", None), "profile", None) if request else None
        if profile is None:
            return

        org = profile.organization
        for field in self.fields.values():
            related_model = getattr(getattr(field, "queryset", None), "model", None)
            if related_model and issubclass(related_model, TenantScopedModel):
                field.queryset = field.queryset.filter(**related_model.tenant_lookup(org))

    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get("request")
        profile = getattr(getattr(request, "user", None), "profile", None) if request else None
        if profile is None:
            return attrs

        org = profile.organization
        for field_name, field in self.fields.items():
            if field.read_only or field_name not in attrs:
                continue
            value = attrs[field_name]
            if value is None:
                continue
            candidates = value if isinstance(value, (list, tuple)) else [value]
            for candidate in candidates:
                if isinstance(candidate, TenantScopedModel) and candidate.resolve_tenant() != org:
                    raise serializers.ValidationError(
                        {field_name: "This value does not belong to your organization."}
                    )
        return attrs
                