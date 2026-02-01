def get_vulnerability_by_id(db, cve_id):
    """Obtener vulnerabilidad por CVE_ID"""
    vuln = db.vulnerabilities.find_one({"CVE_ID": cve_id})
    if vuln:
        vuln["_id"] = str(vuln["_id"])  # convertir ObjectId a string
        return vuln
    return {"error": f"No se encontró vulnerabilidad con CVE_ID {cve_id}"}


def list_all_vulnerabilities(db, limit=50):
    """Listar todas las vulnerabilidades con paginación"""
    vulns = db.vulnerabilities.find().limit(limit)
    result = []
    for v in vulns:
        v["_id"] = str(v["_id"])
        result.append(v)
    return result


def find_by_severity(db, severity):
    """Buscar por nivel de severidad"""
    vulns = db.vulnerabilities.find({"severity": severity})
    result = []
    for v in vulns:
        v["_id"] = str(v["_id"])
        result.append(v)
    return result


def find_by_status(db, status):
    """Buscar por estado (Open/Patched/Investigating)"""
    vulns = db.vulnerabilities.find({"status": status})
    result = []
    for v in vulns:
        v["_id"] = str(v["_id"])
        result.append(v)
    return result


def search_by_keyword(db, keyword):
    """Búsqueda de texto en título y descripción"""
    query = {
        "$or": [
            {"title": {"$regex": keyword, "$options": "i"}},
            {"description": {"$regex": keyword, "$options": "i"}}
        ]
    }
    vulns = db.vulnerabilities.find(query)
    result = []
    for v in vulns:
        v["_id"] = str(v["_id"])
        result.append(v)
    return result

