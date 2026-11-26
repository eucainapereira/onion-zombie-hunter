"""Onion Zombie Hunter — AWS Lambda Entrypoint Re-export.

Garante compatibilidade total com invocações configuradas para lambda_function.lambda_handler
ou handler.lambda_handler.
"""

from handler import lambda_handler

__all__ = ["lambda_handler"]
