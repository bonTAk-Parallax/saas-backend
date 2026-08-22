
from collections import defaultdict


ROLE_MATRIX = {
    ("projects", "read"): {"ADMIN", "MANAGER", "MEMBER"},
    ("projects", "write"): {"ADMIN", "MANAGER"},
    ("projects", "delete"): {"ADMIN"},

    ("tasks", "read"): {"ADMIN", "MANAGER", "MEMBER"},
    ("tasks", "write"): {"ADMIN", "MANAGER", "MEMBER"},
    ("tasks", "delete"): {"ADMIN", "MANAGER"},

    ("exports", "create"): {"ADMIN", "MANAGER"},
}


def _build_role_scopes(matrix):
    scopes = defaultdict(set)

    for (resource, action), roles in matrix.items():
        scope = f"{resource}:{action}"

        for role in roles:
            scopes[role].add(scope)

    return dict(scopes)


ROLE_SCOPES = _build_role_scopes(ROLE_MATRIX)
