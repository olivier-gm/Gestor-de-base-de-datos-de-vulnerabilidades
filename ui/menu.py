
import os
import sys
from colorama import init, Fore, Style
from tabulate import tabulate

# Importaciones de módulos del proyecto
from crud.create import create_vulnerability
from crud.read import (
    get_vulnerability_by_id, list_all_vulnerabilities, 
    find_by_severity, find_by_status, search_by_keyword
)
from crud.update import update_vulnerability, update_status, add_reference
from crud.delete import delete_vulnerability, delete_by_status
from utils.generators import generate_cve_id, generate_random_cve_id
from utils.validators import (
    get_user_input_secure, validate_cvss_score, 
    validate_cve_format, validate_url
)
from utils.reports import (
    generate_summary_report, export_to_json, 
    export_to_csv, display_statistics
)
from database.models import VulnerabilityModel

# Inicializar colorama
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header():
    clear_screen()
    print(Fore.CYAN + Style.BRIGHT + """
    ╔══════════════════════════════════════════════════════════════╗
    ║             GESTOR DE VULNERABILIDADES (CVE)                 ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def show_main_menu():
    print(Fore.YELLOW + "\n=== MENÚ PRINCIPAL ===")
    print("1. " + Fore.WHITE + "Registrar nueva vulnerabilidad")
    print("2. " + Fore.WHITE + "Consultar vulnerabilidad")
    print("3. " + Fore.WHITE + "Listar todas las vulnerabilidades")
    print("4. " + Fore.WHITE + "Buscar vulnerabilidades")
    print("5. " + Fore.WHITE + "Actualizar vulnerabilidad")
    print("6. " + Fore.WHITE + "Eliminar vulnerabilidad")
    print("7. " + Fore.WHITE + "Generar reportes y estadísticas")
    print("8. " + Fore.WHITE + "Salir")

def menu_create_vulnerability(db):
    show_header()
    print(Fore.GREEN + "=== REGISTRAR NUEVA VULNERABILIDAD ===\n")
    
    # Opción de auto-generar CVE ID
    print("¿Desea generar el CVE ID automáticamente? (s/n)")
    if get_user_input_secure("", default="s").lower() == 's':
        cve_id = generate_cve_id(db)
        print(f"🆔 CVE ID asignado: {Fore.CYAN}{cve_id}")
    else:
        cve_id = get_user_input_secure("CVE ID (ej: CVE-2025-00001)", validator=validate_cve_format)

    title = get_user_input_secure("Título")
    description = get_user_input_secure("Descripción")
    
    print("\nSeveridades: Critical, High, Medium, Low")
    severity = get_user_input_secure("Severidad", default="Medium")
    if severity not in VulnerabilityModel.VALID_SEVERITIES:
        print(Fore.RED + "⚠️ Severidad no válida, se asignará 'Medium'")
        severity = "Medium"

    cvss_score = get_user_input_secure("CVSS Score (0.0 - 10.0)", input_type="float", validator=validate_cvss_score)
    
    affected = get_user_input_secure("Sistemas afectados (separados por coma)").split(',')
    affected_systems = [s.strip() for s in affected if s.strip()]

    mitigation = get_user_input_secure("Mitigación", required=False)

    data = {
        "cve_id": cve_id,
        "title": title,
        "description": description,
        "severity": severity,
        "cvss_score": cvss_score,
        "affected_systems": affected_systems,
        "mitigation": mitigation,
        "status": "Open"
    }

    print("\n" + Fore.YELLOW + "Guardando...")
    result = create_vulnerability(db, data)
    
    if "error" in result:
        print(Fore.RED + f"❌ Error: {result['error']}")
    else:
        print(Fore.GREEN + f"✅ Vulnerabilidad creada con éxito. ID Documento: {result['inserted_id']}")
    
    input(Fore.CYAN + "\nPresione Enter para continuar...")

def menu_search_vulnerability(db):
    show_header()
    print(Fore.GREEN + "=== BUSCAR VULNERABILIDADES ===\n")
    print("1. Buscar por ID (CVE)")
    print("2. Buscar por Severidad")
    print("3. Buscar por Estado")
    print("4. Buscar por Palabra Clave")
    
    opcion = get_user_input_secure("Seleccione una opción", input_type="int")
    
    results = []
    
    if opcion == 1:
        cve_id = get_user_input_secure("Ingrese CVE ID")
        res = get_vulnerability_by_id(db, cve_id)
        if "error" not in res:
            results = [res]
        else:
            print(Fore.RED + res["error"])
            
    elif opcion == 2:
        print("Severidades: Critical, High, Medium, Low")
        sev = get_user_input_secure("Ingrese Severidad")
        results = find_by_severity(db, sev)
        
    elif opcion == 3:
        print("Estados: Open, Patched, Investigating")
        stat = get_user_input_secure("Ingrese Estado")
        results = find_by_status(db, stat)
        
    elif opcion == 4:
        keyword = get_user_input_secure("Ingrese palabra clave")
        results = search_by_keyword(db, keyword)
    
    else:
        print(Fore.RED + "Opción inválida")

    if results:
        print(f"\n{Fore.GREEN}Se encontraron {len(results)} resultados:\n")
        table_data = []
        for r in results:
            table_data.append([
                r.get('cve_id'), 
                r.get('severity'), 
                r.get('status'), 
                r.get('title')[:30] + "..."
            ])
        print(tabulate(table_data, headers=["CVE ID", "Severidad", "Estado", "Título"], tablefmt="simple"))
        
        # Opción para ver detalles completos
        if len(results) == 1:
            mostrar_detalle = get_user_input_secure("\n¿Ver detalles completos? (s/n)", default="s")
            if mostrar_detalle.lower() == 's':
                 # Usamos el modelo para formatear, si es posible, o imprimimos directo
                 try:
                     model = VulnerabilityModel(results[0])
                     print(model.to_display())
                 except:
                     print(results[0])
        else:
             ver_id = get_user_input_secure("\nIngrese CVE ID para ver detalles (o Enter para salir)", required=False)
             if ver_id:
                 res = get_vulnerability_by_id(db, ver_id)
                 if "error" not in res:
                     try:
                        model = VulnerabilityModel(res)
                        print(model.to_display())
                     except:
                        print(res)

    input(Fore.CYAN + "\nPresione Enter para continuar...")

def menu_update_vulnerability(db):
    show_header()
    print(Fore.GREEN + "=== ACTUALIZAR VULNERABILIDAD ===\n")
    
    cve_id = get_user_input_secure("Ingrese CVE ID a actualizar")
    vuln = get_vulnerability_by_id(db, cve_id)
    
    if "error" in vuln:
        print(Fore.RED + vuln["error"])
        input("\nPresione Enter para continuar...")
        return

    print(f"Actualizando: {Fore.YELLOW}{vuln.get('title')}")
    print("Deje el campo vacío para mantener el valor actual.\n")
    
    title = get_user_input_secure("Nuevo Título", required=False)
    desc = get_user_input_secure("Nueva Descripción", required=False)
    sev = get_user_input_secure("Nueva Severidad", required=False)
    mitig = get_user_input_secure("Nueva Mitigación", required=False)
    
    update_data = {}
    if title: update_data['title'] = title
    if desc: update_data['description'] = desc
    if sev: update_data['severity'] = sev
    if mitig: update_data['mitigation'] = mitig
    
    if update_data:
        res = update_vulnerability(db, cve_id, update_data)
        if "error" in res:
            print(Fore.RED + f"❌ {res['error']}")
        else:
            print(Fore.GREEN + f"✅ {res['message']}")
    
    # Submenú para estado y referencias
    print("\nOtras acciones:")
    print("1. Cambiar Estado")
    print("2. Agregar Referencia")
    print("3. Terminar")
    
    op = get_user_input_secure("Opción", input_type="int", required=False)
    if op == 1:
        print("Estados: Open, Patched, Investigating")
        st = get_user_input_secure("Nuevo Estado")
        print(update_status(db, cve_id, st).get('message', 'Error'))
    elif op == 2:
        ref = get_user_input_secure("Url Referencia", validator=validate_url)
        print(add_reference(db, cve_id, ref).get('message', 'Error'))
        
    input(Fore.CYAN + "\nPresione Enter para continuar...")

def menu_delete_vulnerability(db):
    show_header()
    print(Fore.RED + "=== ELIMINAR VULNERABILIDAD ===\n")
    
    cve_id = get_user_input_secure("Ingrese CVE ID a eliminar")
    
    check = get_vulnerability_by_id(db, cve_id)
    if "error" in check:
        print(Fore.RED + check["error"])
        input("\nPresione Enter para continuar...")
        return
        
    confirm = get_user_input_secure(f"¿Está SEGURO de eliminar {cve_id}? ESTO NO SE PUEDE DESHACER (s/n)", default="n")
    
    if confirm.lower() == 's':
        res = delete_vulnerability(db, cve_id)
        if "error" in res:
            print(Fore.RED + f"❌ {res['error']}")
        else:
            print(Fore.GREEN + f"✅ {res['message']}")
    else:
        print("Operación cancelada.")
        
    input(Fore.CYAN + "\nPresione Enter para continuar...")

def menu_generate_report(db):
    show_header()
    print(Fore.GREEN + "=== REPORTES Y ESTADÍSTICAS ===\n")
    
    display_statistics(db)
    
    print("\nOpciones de Exportación:")
    print("1. Exportar todo a JSON")
    print("2. Exportar todo a CSV")
    print("3. Volver")
    
    op = get_user_input_secure("Seleccione opción", input_type="int")
    
    if op == 1:
        fname = get_user_input_secure("Nombre archivo JSON", default="vulnerabilidades.json")
        export_to_json(db, fname)
    elif op == 2:
        fname = get_user_input_secure("Nombre archivo CSV", default="vulnerabilidades.csv")
        export_to_csv(db, fname)
        
    input(Fore.CYAN + "\nPresione Enter para continuar...")

def main_loop(db):
    while True:
        show_header()
        show_main_menu()
        
        try:
            choice = input(Fore.YELLOW + "\n>> Seleccione una opción: " + Style.RESET_ALL)
            
            if choice == '1':
                menu_create_vulnerability(db)
            elif choice == '2':
                # Reutilizamos búsqueda por ID
                cve_id = get_user_input_secure("\nIngrese CVE ID")
                res = get_vulnerability_by_id(db, cve_id)
                if "error" in res:
                    print(Fore.RED + res["error"])
                else:
                    try:
                        print(VulnerabilityModel(res).to_display())
                    except:
                        print(res)
                input(Fore.CYAN + "\nPresione Enter para continuar...")
            elif choice == '3':
                vulns = list_all_vulnerabilities(db)
                print(f"\nListando {len(vulns)} vulnerabilidades:\n")
                data = [[v.get('cve_id'), v.get('title')[:40], v.get('severity'), v.get('status')] for v in vulns]
                print(tabulate(data, headers=["CVE ID", "Título", "Severidad", "Estado"], tablefmt="simple"))
                input(Fore.CYAN + "\nPresione Enter para continuar...")
            elif choice == '4':
                menu_search_vulnerability(db)
            elif choice == '5':
                menu_update_vulnerability(db)
            elif choice == '6':
                menu_delete_vulnerability(db)
            elif choice == '7':
                menu_generate_report(db)
            elif choice == '8':
                print(Fore.CYAN + "\n👋 ¡Hasta luego!")
                break
            else:
                print(Fore.RED + "❌ Opción no válida.")
                input("Presione Enter...")
        except KeyboardInterrupt:
            print("\n👋 Salida forzada.")
            break
