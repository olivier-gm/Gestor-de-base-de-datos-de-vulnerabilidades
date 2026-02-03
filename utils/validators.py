
import re
from urllib.parse import urlparse

def validate_cve_format(cve_id):
    """
    Validar formato CVE-YYYY-NNNNN.
    Ejemplo: CVE-2025-12345
    """
    pattern = r"^CVE-\d{4}-\d{5}$"
    if not re.match(pattern, cve_id):
        return False, "Formato inválido. Debe ser CVE-YYYY-NNNNN (ej: CVE-2025-00001)"
    return True, None

def validate_cvss_score(score):
    """Validar que score esté entre 0.0 y 10.0"""
    try:
        val = float(score)
        if 0.0 <= val <= 10.0:
            return True, None
        return False, "El score debe estar entre 0.0 y 10.0"
    except ValueError:
        return False, "El score debe ser un número válido"

def validate_url(url):
    """Validar formato de URL para referencias"""
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return True, None
        return False, "URL inválida (debe incluir http/https)"
    except:
        return False, "URL mal formada"

def get_user_input_secure(prompt, input_type='text', validator=None, required=True, default=None):
    """
    Obtener entrada del usuario con validación.
    
    Args:
        prompt: Mensaje a mostrar
        input_type: 'text', 'float', 'int'
        validator: Función que recibe el valor y retorna (bool, msg)
        required: Si es True, no permite vacío
        default: Valor por defecto si se deja vacío
    """
    while True:
        try:
            display_prompt = prompt
            if default is not None:
                display_prompt += f" [{default}]"
            display_prompt += ": "
            
            user_input = input(display_prompt).strip()

            if not user_input:
                if default is not None:
                    return default
                if required:
                    print("❌ Este campo es obligatorio.")
                    continue
                return ""

            # Conversión de tipos
            value = user_input
            if input_type == 'float':
                try:
                    value = float(user_input)
                except ValueError:
                    print("❌ Debe ingresar un número decimal.")
                    continue
            elif input_type == 'int':
                try:
                    value = int(user_input)
                except ValueError:
                    print("❌ Debe ingresar un número entero.")
                    continue

            # Validación personalizada
            if validator:
                is_valid, error_msg = validator(value)
                if not is_valid:
                    print(f"❌ {error_msg}")
                    continue
            
            return value

        except KeyboardInterrupt:
            print("\nOperación cancelada.")
            return None
