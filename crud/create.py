def create_vulnerability(db, vuln_data):
    try:
        # 1. Validar datos con el modelo
        vulnerability = VulnerabilityModel(**vuln_data)

        # 2. Verificar unicidad de CVE_ID
        existing = db.vulnerabilities.find_one({"CVE_ID": vulnerability.CVE_ID})
        if existing:
            return {"error": f"La vulnerabilidad con CVE_ID {vulnerability.CVE_ID} ya existe."}

        # 3. Insertar en la colección
        result = db.vulnerabilities.insert_one(vulnerability.dict())

        # 4. Retornar el ID insertado
        return {"inserted_id": str(result.inserted_id)}

    except ValidationError as ve:
        return {"error": f"Datos inválidos: {ve}"}
    except DuplicateKeyError:
        return {"error": f"CVE_ID {vuln_data.get('CVE_ID')} ya existe en la base de datos."}
    except Exception as e:
        return {"error": f"Error inesperado: {e}"}
