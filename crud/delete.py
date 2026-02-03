
def delete_vulnerability(db, cve_id):
    vuln = db.vulnerabilities.find_one({"cve_id": cve_id})
    if not vuln:
        return {"error": f"No se encontró vulnerabilidad con CVE_ID {cve_id}"}

    result = db.vulnerabilities.delete_one({"cve_id": cve_id})
    if result.deleted_count > 0:
        return {"message": f"Vulnerabilidad {cve_id} eliminada correctamente"}
    else:
        return {"error": "No se pudo eliminar la vulnerabilidad"}


def delete_by_status(db, status):
    """Eliminar todas las vulnerabilidades con cierto estado"""
    result = db.vulnerabilities.delete_many({"status": status})
    if result.deleted_count > 0:
        return {"message": f"Se eliminaron {result.deleted_count} vulnerabilidades con estado {status}"}
    else:
        return {"message": f"No se encontraron vulnerabilidades con estado {status}"}