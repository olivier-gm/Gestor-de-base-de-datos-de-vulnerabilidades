def update_vulnerability(db, cve_id, update_data):
    vuln = db.vulnerabilities.find_one({"CVE_ID": cve_id})
    if not vuln:
        return {"error": f"No se encontró vulnerabilidad con CVE_ID {cve_id}"}

    try:
        # Validar datos combinando lo existente con lo nuevo
        merged_data = {**vuln, **update_data}
        vulnerability = VulnerabilityModel(**merged_data)

        # Actualizar campo last_modified
        update_data["last_modified"] = datetime.utcnow()

        result = db.vulnerabilities.update_one(
            {"CVE_ID": cve_id},
            {"$set": update_data}
        )

        if result.modified_count > 0:
            return {"message": "Vulnerabilidad actualizada correctamente"}
        else:
            return {"message": "No se realizaron cambios"}

    except ValidationError as ve:
        return {"error": f"Datos inválidos: {ve}"}
    except Exception as e:
        return {"error": f"Error inesperado: {e}"}


def update_status(db, cve_id, new_status):
    """Cambiar estado de vulnerabilidad"""
    valid_status = ["Open", "Patched", "Investigating"]
    if new_status not in valid_status:
        return {"error": f"Estado inválido. Debe ser uno de {valid_status}"}

    result = db.vulnerabilities.update_one(
        {"CVE_ID": cve_id},
        {"$set": {"status": new_status, "last_modified": datetime.utcnow()}}
    )

    if result.matched_count == 0:
        return {"error": f"No se encontró vulnerabilidad con CVE_ID {cve_id}"}
    return {"message": f"Estado actualizado a {new_status}"}


def add_reference(db, cve_id, reference_url):
    """Agregar URL de referencia"""
    result = db.vulnerabilities.update_one(
        {"CVE_ID": cve_id},
        {"$addToSet": {"references": reference_url},  # evita duplicados
         "$set": {"last_modified": datetime.utcnow()}}
    )

    if result.matched_count == 0:
        return {"error": f"No se encontró vulnerabilidad con CVE_ID {cve_id}"}
    return {"message": "Referencia agregada correctamente"}
