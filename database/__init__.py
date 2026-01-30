"""
Módulo de base de datos para el Gestor de Vulnerabilidades.
Proporciona conexión y modelos para MongoDB.
"""

from .connection import get_database, close_connection
from .models import VulnerabilityModel

__all__ = ['get_database', 'close_connection', 'VulnerabilityModel']
