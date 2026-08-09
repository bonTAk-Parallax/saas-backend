
class TenantAwareMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        org = self.request.user.profile.organization
        model = queryset.model

        if hasattr(model, 'organization') and model._meta.get_field('organization').related_model.__name__ == 'Organization':
            return queryset.filter(organization=org)
        if hasattr(model, 'project'):
            return queryset.filter(project__organization=org)
        if hasattr(model, 'task'):
            return queryset.filter(task__project__organization=org)
        return queryset

    def perform_create(self, serializer):
        if hasattr(serializer.Meta.model, 'organization'):
            serializer.save(organization=self.request.user.profile.organization)
        else:
            serializer.save()
            