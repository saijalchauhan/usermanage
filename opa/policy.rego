package usermanage.authz

default allow = false

allow {
    input.role = "admin"
    input.action = "create"
}

allow {
    input.role = "admin"
    input.action = "read"
}

allow {
    input.role = "user"
    input.action = "read"
}
