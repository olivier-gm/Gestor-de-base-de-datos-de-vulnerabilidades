"""
Modelos de datos para el Gestor de Vulnerabilidades.
Define la estructura y validaciones para vulnerabilidades tipo CVE.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any


class VulnerabilityModel:
    """
    Modelo de datos para vulnerabilidades tipo CVE.

    Atributos:
        cve_id: Identificador único tipo CVE (ej: CVE-2025-00001)
        title: Título breve de la vulnerabilidad
        description: Descripción técnica detallada
        severity: Nivel de severidad (Critical/High/Medium/Low)
        cvss_score: Puntuación CVSS (0.0 - 10.0)
        affected_systems: Lista de sistemas/software afectados
        published_date: Fecha de publicación
        last_modified: Fecha de última modificación
        status: Estado actual (Open/Patched/Investigating)
        references: Lista de URLs de referencia
        mitigation: Medidas de mitigación recomendadas
    """

    # Constantes para validación
    VALID_SEVERITIES = ['Critical', 'High', 'Medium', 'Low']
    VALID_STATUSES = ['Open', 'Patched', 'Investigating']

    def __init__(self, data: Dict[str, Any]):
        """
        Inicializa un modelo de vulnerabilidad con validación.

        Args:
            data: Diccionario con los datos de la vulnerabilidad

        Raises:
            ValueError: Si los datos no son válidos
        """
        self.data = self._validate_and_normalize(data)

    def _validate_and_normalize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida y normaliza los datos de entrada.

        Args:
            data: Datos sin validar

        Returns:
            Dict con datos validados y normalizados

        Raises:
            ValueError: Si algún campo no es válido
        """
        validated = {}

        # CVE_ID (requerido)
        if 'cve_id' not in data or not data['cve_id']:
            raise ValueError("El campo 'cve_id' es obligatorio")
        validated['cve_id'] = str(data['cve_id']).strip()

        # Title (requerido)
        if 'title' not in data or not data['title']:
            raise ValueError("El campo 'title' es obligatorio")
        validated['title'] = str(data['title']).strip()

        # Description (requerido)
        if 'description' not in data or not data['description']:
            raise ValueError("El campo 'description' es obligatorio")
        validated['description'] = str(data['description']).strip()

        # Severity (requerido)
        severity = data.get('severity', '').strip()
        if severity not in self.VALID_SEVERITIES:
            raise ValueError(
                f"Severidad inválida. Debe ser una de: {', '.join(self.VALID_SEVERITIES)}"
            )
        validated['severity'] = severity

        # CVSS Score (requerido)
        try:
            cvss_score = float(data.get('cvss_score', 0))
            if not (0.0 <= cvss_score <= 10.0):
                raise ValueError("CVSS score debe estar entre 0.0 y 10.0")
            validated['cvss_score'] = round(cvss_score, 1)
        except (ValueError, TypeError):
            raise ValueError("CVSS score debe ser un número entre 0.0 y 10.0")

        # Affected Systems (requerido)
        affected = data.get('affected_systems', [])
        if not affected or not isinstance(affected, list):
            raise ValueError("'affected_systems' debe ser una lista no vacía")
        validated['affected_systems'] = [str(s).strip() for s in affected if s]

        # Published Date (opcional, usa fecha actual si no se proporciona)
        published_date = data.get('published_date')
        if published_date:
            validated['published_date'] = self._parse_date(published_date)
        else:
            validated['published_date'] = datetime.now().strftime('%Y-%m-%d')

        # Last Modified (opcional, usa fecha actual)
        last_modified = data.get('last_modified')
        if last_modified:
            validated['last_modified'] = self._parse_date(last_modified)
        else:
            validated['last_modified'] = datetime.now().strftime('%Y-%m-%d')

        # Status (opcional, por defecto "Open")
        status = data.get('status', 'Open').strip()
        if status not in self.VALID_STATUSES:
            raise ValueError(
                f"Estado inválido. Debe ser uno de: {', '.join(self.VALID_STATUSES)}"
            )
        validated['status'] = status

        # References (opcional)
        references = data.get('references', [])
        if isinstance(references, list):
            validated['references'] = [str(ref).strip() for ref in references if ref]
        else:
            validated['references'] = []

        # Mitigation (opcional)
        validated['mitigation'] = str(data.get('mitigation', '')).strip()

        return validated

    def _parse_date(self, date_value: Any) -> str:
        """
        Parsea y valida una fecha.

        Args:
            date_value: Fecha en formato string, datetime o timestamp

        Returns:
            Fecha en formato YYYY-MM-DD

        Raises:
            ValueError: Si el formato de fecha es inválido
        """
        if isinstance(date_value, datetime):
            return date_value.strftime('%Y-%m-%d')

        if isinstance(date_value, str):
            try:
                # Intentar parsear varios formatos
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
                    try:
                        dt = datetime.strptime(date_value.strip(), fmt)
                        return dt.strftime('%Y-%m-%d')
                    except ValueError:
                        continue
                raise ValueError()
            except ValueError:
                raise ValueError(
                    f"Formato de fecha inválido: {date_value}. Use YYYY-MM-DD"
                )

        raise ValueError("Fecha debe ser string o datetime")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el modelo a diccionario para MongoDB.

        Returns:
            Diccionario con los datos de la vulnerabilidad
        """
        return self.data.copy()

    def to_display(self) -> str:
        """
        Genera representación en texto legible de la vulnerabilidad.

        Returns:
            String formateado para mostrar en consola
        """
        data = self.data
        output = []

        output.append(f"\n{'=' * 70}")
        output.append(f"🆔 CVE ID: {data['cve_id']}")
        output.append(f"📌 Título: {data['title']}")
        output.append(f"{'=' * 70}")

        output.append(f"\n📄 Descripción:")
        output.append(f"   {data['description']}")

        # Severidad con emoji
        severity_emoji = {
            'Critical': '🔴',
            'High': '🟠',
            'Medium': '🟡',
            'Low': '🟢'
        }
        emoji = severity_emoji.get(data['severity'], '⚪')

        output.append(f"\n{emoji} Severidad: {data['severity']}")
        output.append(f"📊 CVSS Score: {data['cvss_score']}/10.0")

        output.append(f"\n💻 Sistemas Afectados:")
        for system in data['affected_systems']:
            output.append(f"   • {system}")

        output.append(f"\n📅 Publicado: {data['published_date']}")
        output.append(f"🔄 Última modificación: {data['last_modified']}")

        # Estado con emoji
        status_emoji = {
            'Open': '🔓',
            'Patched': '✅',
            'Investigating': '🔍'
        }
        status_icon = status_emoji.get(data['status'], '⚪')
        output.append(f"{status_icon} Estado: {data['status']}")

        if data.get('references'):
            output.append(f"\n🔗 Referencias:")
            for ref in data['references']:
                output.append(f"   • {ref}")

        if data.get('mitigation'):
            output.append(f"\n🛡️  Mitigación:")
            output.append(f"   {data['mitigation']}")

        output.append(f"{'=' * 70}\n")

        return '\n'.join(output)

    @staticmethod
    def get_severity_from_cvss(cvss_score: float) -> str:
        """
        Calcula la severidad basada en el CVSS score según estándares NIST.

        Args:
            cvss_score: Puntuación CVSS (0.0 - 10.0)

        Returns:
            Nivel de severidad correspondiente
        """
        if cvss_score >= 9.0:
            return 'Critical'
        elif cvss_score >= 7.0:
            return 'High'
        elif cvss_score >= 4.0:
            return 'Medium'
        else:
            return 'Low'

    @staticmethod
    def create_empty_template() -> Dict[str, Any]:
        """
        Crea una plantilla vacía para una nueva vulnerabilidad.

        Returns:
            Diccionario con estructura básica
        """
        return {
            'cve_id': '',
            'title': '',
            'description': '',
            'severity': 'Medium',
            'cvss_score': 5.0,
            'affected_systems': [],
            'published_date': datetime.now().strftime('%Y-%m-%d'),
            'last_modified': datetime.now().strftime('%Y-%m-%d'),
            'status': 'Open',
            'references': [],
            'mitigation': ''
        }


# Funciones de utilidad para trabajar con el modelo

def validate_vulnerability(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Valida datos de vulnerabilidad sin crear instancia.

    Args:
        data: Datos a validar

    Returns:
        Tupla (es_valido, mensaje_error)
    """
    try:
        VulnerabilityModel(data)
        return True, None
    except ValueError as e:
        return False, str(e)


def get_collection_stats(db) -> Dict[str, Any]:
    """
    Obtiene estadísticas de la colección de vulnerabilidades.

    Args:
        db: Instancia de la base de datos

    Returns:
        Diccionario con estadísticas
    """
    collection = db['vulnerabilities']

    stats = {
        'total': collection.count_documents({}),
        'by_severity': {},
        'by_status': {}
    }

    # Contar por severidad
    for severity in VulnerabilityModel.VALID_SEVERITIES:
        count = collection.count_documents({'severity': severity})
        stats['by_severity'][severity] = count

    # Contar por estado
    for status in VulnerabilityModel.VALID_STATUSES:
        count = collection.count_documents({'status': status})
        stats['by_status'][status] = count

    return stats


# Ejecutar si se ejecuta directamente este archivo
if __name__ == "__main__":
    print("🔍 Probando modelo de vulnerabilidades...\n")

    # Datos de prueba
    test_data = {
        'cve_id': 'CVE-2025-00001',
        'title': 'Buffer Overflow en Apache HTTP Server',
        'description': 'Vulnerabilidad de desbordamiento de búfer en módulo mod_proxy',
        'severity': 'Critical',
        'cvss_score': 9.8,
        'affected_systems': ['Apache HTTP Server 2.4.x', 'Apache HTTP Server 2.5.0'],
        'status': 'Open',
        'references': ['https://nvd.nist.gov/vuln/detail/CVE-2025-00001'],
        'mitigation': 'Actualizar a versión 2.4.58 o superior'
    }

    try:
        vuln = VulnerabilityModel(test_data)
        print("✅ Modelo validado correctamente")
        print(vuln.to_display())
    except ValueError as e:
        print(f"❌ Error de validación: {e}")
