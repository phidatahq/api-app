from dataclasses import dataclass


@dataclass
class ApiEndpoints:
    PING: str = "/ping"
    USERS: str = "/users"


endpoints = ApiEndpoints()
