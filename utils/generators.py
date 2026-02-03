
import random
from datetime import datetime

def generate_cve_id(db):
    """
    Generar ID único tipo CVE-YYYY-NNNNN.
    Autoincremental basado en el último registrado del año actual.
    """
    current_year = datetime.now().year
    prefix_pattern = f"CVE-{current_year}-"
    
    # Buscar el último CVE del año actual
    # Ordenamos descendente por cve_id y limitamos a 1
    # Filtramos por regex para asegurar que siga el patrón del año
    query = {"cve_id": {"$regex": f"^{prefix_pattern}"}}
    last_vuln = db.vulnerabilities.find(query).sort("cve_id", -1).limit(1)
    
    last_id = None
    for v in last_vuln:
        last_id = v.get('cve_id')
    
    if last_id:
        try:
            # Extraer número: CVE-2025-00001 -> 00001
            parts = last_id.split('-')
            if len(parts) == 3:
                sequence = int(parts[2])
                new_sequence = sequence + 1
            else:
                new_sequence = 1
        except ValueError:
            new_sequence = 1
    else:
        new_sequence = 1
        
    return f"CVE-{current_year}-{new_sequence:05d}"

def generate_random_cve_id():
    """Generar ID aleatorio para testing."""
    year = datetime.now().year
    number = random.randint(1, 99999)
    return f"CVE-{year}-{number:05d}"
