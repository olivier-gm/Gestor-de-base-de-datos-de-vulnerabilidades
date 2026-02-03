
import json
import csv
import os
from datetime import datetime
from tabulate import tabulate
from database.models import get_collection_stats

def generate_summary_report(db):
    """
    Generar e imprimir reporte de resumen en consola.
    """
    stats = get_collection_stats(db)
    
    print("\n📊 REPORTE DE RESUMEN DE VULNERABILIDADES")
    print(f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    print(f"\n📝 Total de Vulnerabilidades: {stats.get('total', 0)}")
    
    # Tabla por Severidad
    print("\n🔴 Por Severidad:")
    sev_data = [[k, v] for k, v in stats.get('by_severity', {}).items()]
    print(tabulate(sev_data, headers=["Severidad", "Cantidad"], tablefmt="simple"))
    
    # Tabla por Estado
    print("\n🔄 Por Estado:")
    status_data = [[k, v] for k, v in stats.get('by_status', {}).items()]
    print(tabulate(status_data, headers=["Estado", "Cantidad"], tablefmt="simple"))
    
    # Últimas 10 vulnerabilidades
    print("\n🗓️  Últimas 10 Vulnerabilidades Registradas:")
    recent = db.vulnerabilities.find({}, {"cve_id": 1, "title": 1, "published_date": 1, "severity": 1}).sort("published_date", -1).limit(10)
    
    recent_data = []
    for v in recent:
        recent_data.append([
            v.get('cve_id'),
            v.get('published_date'),
            v.get('severity'),
            v.get('title')[:40] + "..." if len(v.get('title', '')) > 40 else v.get('title')
        ])
    
    print(tabulate(recent_data, headers=["CVE ID", "Fecha", "Severidad", "Título"], tablefmt="grid"))
    print("\n" + "=" * 50)

def export_to_json(db, filename):
    """Exportar vulnerabilidades a JSON"""
    try:
        cursor = db.vulnerabilities.find()
        data = []
        for doc in cursor:
            doc['_id'] = str(doc['_id']) # Convertir ObjectId
            data.append(doc)
            
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        print(f"✅ Exportación exitosa a: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error al exportar a JSON: {e}")
        return False

def export_to_csv(db, filename):
    """Exportar vulnerabilidades a CSV"""
    try:
        cursor = db.vulnerabilities.find()
        # Obtener primer documento para cabeceras, o definir fijas
        # Definimos cabeceras fijas para orden y consistencia
        fieldnames = ['cve_id', 'title', 'description', 'severity', 'cvss_score', 
                      'status', 'published_date', 'last_modified', 'mitigation', 
                      'affected_systems', 'references']
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            
            for doc in cursor:
                # Procesar listas para que quepan en CSV
                row = doc.copy()
                if isinstance(row.get('affected_systems'), list):
                    row['affected_systems'] = "; ".join(row['affected_systems'])
                if isinstance(row.get('references'), list):
                    row['references'] = "; ".join(row['references'])
                
                writer.writerow(row)
                
        print(f"✅ Exportación exitosa a: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error al exportar a CSV: {e}")
        return False

def display_statistics(db):
    """Mostrar estadísticas en consola (similar al resumen)"""
    # Reutilizamos generate_summary_report o hacemos uno específico
    generate_summary_report(db)
