
class TenantAwareMixin:
    """
    Provides automatic organization-level isolation for tenant-scoped views.

    get_queryset():
        Restricts all queries to records belonging to the authenticated
        user's organization. If the user has no profile, returns an empty
        queryset for safety.

    perform_create():
        Automatically assigns the user's organization to root tenant models.
        For models with indirect tenant relationships, the organization is
        derived through the validated related object.
    """
    def get_queryset(self):
        qs = super().get_queryset()
        profile = getattr(self.request.user, "profile", None)
        if profile is None:
            return qs.none()
        return qs.filter(**qs.model.tenant_lookup(profile.organization))

    def perform_create(self, serializer):
        model = serializer.Meta.model
        if model.is_root_tenant_field():
            serializer.save(organization=self.request.user.profile.organization)
        else:
            serializer.save()  
            