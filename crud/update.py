from datetime import datetime
from database.models import VulnerabilityModel

def update_vulnerability(db, cve_id, update_data):
    vuln = db.vulnerabilities.find_one({"cve_id": cve_id})
    if not vuln:
        return {"error": f"No se encontró vulnerabilidad con CVE_ID {cve_id}"}

    try:
        # Validar datos combinando lo existente con lo nuevo
        # Nota: VulnerabilityModel espera un dict completo para validación estricta? 
        # Si update_data es parcial, necesitamos fusionar con cuidado.
        # Asumiremos que fusionamos con el existente.
        merged_data = {**vuln, **update_data}
        # Eliminar _id del dict merged para que no falle validación si el modelo no lo espera
        if '_id' in merged_data:
            del merged_data['_id']
            
        vulnerability = VulnerabilityModel(merged_data)

        # Actualizar campo last_modified
        final_update_data = update_data.copy()
        final_update_data["last_modified"] = datetime.now().strftime('%Y-%m-%d')
        # Asegurar que se guarden los campos validados, pero update_one usa $set
        # Podríamos usar vulnerability.to_dict() pero eso sobrescribe todo.
        # Mejor confiamos en que update_data es lo que queremos cambiar, 
        # pero usamos validación de merged_data para asegurar integridad.

        result = db.vulnerabilities.update_one(
            {"cve_id": cve_id},
            {"$set": final_update_data}
        )

        if result.modified_count > 0:
            return {"message": "Vulnerabilidad actualizada correctamente"}
        else:
            return {"message": "No se realizaron cambios"}

    except ValueError as ve:
        return {"error": f"Datos inválidos: {ve}"}
    except Exception as e:
        return {"error": f"Error inesperado: {e}"}


def update_status(db, cve_id, new_status):
    """Cambiar estado de vulnerabilidad"""
    valid_status = ["Open", "Patched", "Investigating"]
    if new_status not in valid_status:
        return {"error": f"Estado inválido. Debe ser uno de {valid_status}"}

    result = db.vulnerabilities.update_one(
        {"cve_id": cve_id},
        {"$set": {"status": new_status, "last_modified": datetime.now().strftime('%Y-%m-%d')}}
    )

    if result.matched_count == 0:
        return {"error": f"No se encontró vulnerabilidad con CVE_ID {cve_id}"}
    return {"message": f"Estado actualizado a {new_status}"}


def add_reference(db, cve_id, reference_url):
    """Agregar URL de referencia"""
    result = db.vulnerabilities.update_one(
        {"cve_id": cve_id},
        {"$addToSet": {"references": reference_url},  # evita duplicados
         "$set": {"last_modified": datetime.now().strftime('%Y-%m-%d')}}
    )

    if result.matched_count == 0:
        return {"error": f"No se encontró vulnerabilidad con CVE_ID {cve_id}"}
    return {"message": "Referencia agregada correctamente"}
