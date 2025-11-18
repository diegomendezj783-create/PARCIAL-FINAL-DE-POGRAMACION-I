fecha_actual_global = None

def menu():
    print("\n")
    print("-" * 83)
    print("BIENVENIDO A LA BIBLIOTECA VIRTUAL GESTIONATIVA DEL PLUTALCO")
    print("POR FAVOR SELECCIONE LA OPCION DE PREFERENCIA:")
    print("1. NUEVO USUARIO")
    print("2. MODIFICAR FECHA")
    print("3. VER USUARIOS REGISTRADOS")
    print("4. BUSCAR LIBROS EN LA BIBLIOTECA")
    print("5. AÑADIR LIBROS")
    print("6. RESEÑAR LIBROS")
    print("7. VER RESEÑAS DE LIBROS")
    print("8. APARTAR LIBRO")
    print("9. VER PRIVILEGIOS DE USUARIO")
    print("10. VER HISTORIAL DE PRÉSTAMOS")
    print("11. VER MULTAS PENDIENTES")
    print("12. PAGAR MULTAS PENDIENTES")
    print("13. RECOMENDACIONES")
    print("14. DEVOLVER LIBRO")
    print("15. RENOVAR PRÉSTAMO")
    print("16. REPORTES Y ESTADÍSTICAS")
    print("0. Exit")
    print("-" * 83)
    print("\n")

def MENU_REPORTES():
    while True:
        print("\n" + "="*40)
        print("    MÓDULO DE REPORTES Y ESTADÍSTICAS")
        print("="*40)
        print("1. Libros más prestados")
        print("2. Usuarios más activos")
        print("3. Categorías más populares")
        print("4. Tasa de ocupación y libros sin préstamos")
        print("5. Tiempo promedio de préstamo por categoría")
        print("6. Volver al menú principal")
        opc = input("Seleccione una opción (1-6): ")

# --- 1. LIBROS MÁS PRESTADOS ---
        if opc == "1":
            conteo = {} # Diccionario para contar
            for p in prestamos:
                isbn = p.get('ISBN')
                # Usamos .get para sumar 1 al valor actual
                conteo[isbn] = conteo.get(isbn, 0) + 1
            
            # Convertimos a lista de tuplas para ordenar
            lista_ordenada = sorted(conteo.items(), key=lambda x: x[1], reverse=True)
            
            print("\n--- TOP LIBROS MÁS PRESTADOS ---")
            print(f"{'Cant.':<6} | {'Título'}")
            print("-" * 40)
            # Mostramos solo los 5 primeros (o todos si hay menos)
            for isbn, cantidad in lista_ordenada[:5]:
                nombre = obtener_nombre_libro(isbn)
                print(f"{cantidad:<6} | {nombre}")

        # --- 2. USUARIOS MÁS ACTIVOS ---
        elif opc == "2":
            actividad = {}
            for p in prestamos:
                uid = p.get('ID_Usuario')
                actividad[uid] = actividad.get(uid, 0) + 1
            
            lista_users = sorted(actividad.items(), key=lambda x: x[1], reverse=True)
            
            print("\n--- USUARIOS MÁS ACTIVOS ---")
            print(f"{'Prestamos':<10} | {'Usuario'}")
            print("-" * 40)
            for uid, cant in lista_users[:5]:
                nombre = obtener_nombre_usuario(uid)
                print(f"{cant:<10} | {nombre} (ID: {uid})")

        # --- 3. CATEGORÍAS MÁS POPULARES ---
        elif opc == "3":
            cat_conteo = {}
            for p in prestamos:
                isbn_p = p.get('ISBN')
                # Buscar la categoría de ese libro en el inventario
                for l in libros:
                    if l.get('ISBN') == isbn_p:
                        cat = l.get('categoria', 'Sin Categoria')
                        cat_conteo[cat] = cat_conteo.get(cat, 0) + 1
                        break
            
            lista_cat = sorted(cat_conteo.items(), key=lambda x: x[1], reverse=True)
            print("\n--- CATEGORÍAS PREFERIDAS ---")
            for cat, num in lista_cat:
                print(f"{cat}: {num} préstamos")

        # --- 4. TASA DE OCUPACIÓN Y CANDIDATOS A DESCARTE ---
        elif opc == "4":
            total_inventario = 0
            total_prestados = 0
            
            # Calcular ocupación
            for l in libros:
                total_inventario += int(l.get('Copias', 0))
                total_prestados += int(l.get('reservado', 0))
            
            tasa = 0
            if total_inventario > 0:
                tasa = (total_prestados / total_inventario) * 100
                
            print(f"\n--- TASA DE OCUPACIÓN: {tasa:.2f}% ---")
            print(f"Total libros en inventario: {total_inventario}")
            print(f"Total libros prestados hoy: {total_prestados}")

            # Libros nunca prestados (Candidatos a descarte)
            print("\n--- LIBROS NUNCA PRESTADOS (Candidatos a descarte) ---")
            # Crear conjunto de ISBNs que sí han sido prestados
            isbns_prestados = []
            for p in prestamos:
                isbns_prestados.append(p.get('ISBN'))
            
            encontrados = False
            for l in libros:
                if l.get('ISBN') not in isbns_prestados:
                    print(f"- {l.get('Titulo')} ({l.get('ISBN')})")
                    encontrados = True
            
            if not encontrados:
                print("¡Excelente! Todos los libros han sido prestados al menos una vez.")

        # --- 5. TIEMPO PROMEDIO DE PRÉSTAMO Y TENDENCIAS ---
        elif opc == "5":
            # Diccionario: {'Novela': [5, 10, 2], 'Poesía': [3]}
            tiempos_por_cat = {}
            
            for p in prestamos:
                # Solo calculamos si ya fue devuelto para tener fecha real
                if p.get('Devuelto') == True:
                    f_inicio = p.get('Fecha_Prestamo')
                    f_fin = p.get('Fecha_Devolucion_Real')
                    
                    # Usamos tu función fecha_a_dias
                    dias_inicio = fecha_a_dias(f_inicio)
                    dias_fin = fecha_a_dias(f_fin)
                    
                    if dias_inicio and dias_fin:
                        duracion = dias_fin - dias_inicio
                        
                        # Buscar categoría
                        cat_actual = "Desconocida"
                        for l in libros:
                            if l.get('ISBN') == p.get('ISBN'):
                                cat_actual = l.get('categoria')
                                break
                        
                        if cat_actual not in tiempos_por_cat:
                            tiempos_por_cat[cat_actual] = []
                        tiempos_por_cat[cat_actual].append(duracion)

            print("\n--- TIEMPO PROMEDIO DE LECTURA POR CATEGORÍA ---")
            for cat, lista_dias in tiempos_por_cat.items():
                promedio = sum(lista_dias) / len(lista_dias)
                print(f"{cat}: {promedio:.1f} días en promedio")

        # --- SALIR ---
        elif opc == "6":
            break
        else:
            print("Opción no válida.")

# Pide al usuario el día, mes y año actual. 
# Valida si la fecha es correcta (rango de días/meses, años bisiestos) y, si es válida, 
# actualiza la variable global fecha_actual_global.

def FECHA_ACTUAL():
    global fecha_actual_global

    print("-" * 32)
    dia = int(input("\nIngrese el día actual (DD): "))
    mes = int(input("Ingrese el mes actual (MM): "))
    año = int(input("Ingrese el año actual (AAAA): "))

    fecha = (f"{dia}/{mes}/{año}")

    if mes <= 0 or mes > 12:
        print("Mes inválido. Por favor ingrese un mes entre 01 y 12.")
        return FECHA_ACTUAL()
    elif dia<= 0 or dia > 31:
        print("Día inválido. Por favor ingrese un día entre 01 y 31.")
        return FECHA_ACTUAL()
    elif año <= 0:
        print("Año inválido. Por favor ingrese un año válido.")
        return FECHA_ACTUAL()
    elif mes==2:
        if (año % 4 == 0 and año % 100 != 0) or (año % 400 == 0):
            if dia > 29:
                print("Día inválido para febrero en un año bisiesto. Por favor ingrese un día entre 01 y 29.")
                return FECHA_ACTUAL()
        else:
            if dia > 28:
                print("Día inválido para febrero en un año no bisiesto. Por favor ingrese un día entre 01 y 28.")
                return FECHA_ACTUAL()
    else:
        fecha = f"{dia}/{mes}/{año}"
        fecha_actual_global = fecha
        return fecha

def ver_reseñas():
    titulo = input("Ingrese el título o ISBN del libro para ver sus reseñas: ")
    encontrado = None
    for libro in libros:
        if libro['Titulo'].lower() == titulo.lower() or libro['ISBN'] == titulo:
            encontrado = libro
            break
    if encontrado:
        if 'Reseñas' in encontrado and encontrado['Reseñas']:
            print(f"Reseñas para '{encontrado['Titulo']}':")
            print("-" * 40)
            for idx, reseña in enumerate(encontrado['Reseñas'], 1):
                print(f"{idx}. {reseña}")
        else:
            print(f"No hay reseñas disponibles para '{encontrado['Titulo']}'.")
    else:
        print("No se encontró el libro especificado.")

def obtener_privilegios(tipo_usuario):
    """Retorna los privilegios (max_libros, dias_prestamo) del usuario"""
    if tipo_usuario in PRIVILEGIOS:
        return PRIVILEGIOS[tipo_usuario]
    else:
        return (0, 0)

def contar_libros_usuario(id_usuario, prestamos):
    """Cuenta cuántos libros tiene prestados un usuario"""
    # Devolver 0 si no se proporcionó lista de préstamos
    if not prestamos:
        return 0

    contador = 0
    # Contar préstamos activos (no devueltos) del usuario
    for p in prestamos:
        try:
            if p.get('ID_Usuario') == id_usuario and not p.get('Devuelto', False):
                contador += 1
        except Exception:
            # Ignorar entradas inválidas
            continue

    return contador

#Convierte una fecha en formato 'DD/MM/AAAA' a un número entero que representa el total de días
#  transcurridos desde el año 0 (cálculo de días del año, incluyendo bisiestos).
#  Esta función es clave para comparar fechas y calcular diferencias.

def fecha_a_dias(fecha_str):

    try:
        # 1. Encontrar la posición de los separadores '/'
        indice_barra1 = -1
        for i in range(len(fecha_str)):
            if fecha_str[i] == '/':
                indice_barra1 = i
                break
        
        # Encontrar la posición del segundo '/'
        indice_barra2 = -1
        for i in range(indice_barra1 + 1, len(fecha_str)):
            if fecha_str[i] == '/':
                indice_barra2 = i
                break

        # 2. Extracción de día, mes y año usando rebanado de cadenas
        # DD: desde el inicio hasta la primera barra
        dia_str = fecha_str[0:indice_barra1]
        
        # MM: desde la posición después de la primera barra hasta la segunda barra
        mes_str = fecha_str[indice_barra1 + 1:indice_barra2]
        
        # AAAA: desde la posición después de la segunda barra hasta el final
        año_str = fecha_str[indice_barra2 + 1:]

        # 3. Conversión a enteros y validacións.
        if indice_barra1 == -1 or indice_barra2 == -1: return None
        
        dia, mes, año = int(dia_str), int(mes_str), int(año_str)

        # 4. Lógica de cálculo de días
        dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        def es_bisiesto(a):
            return (a % 4 == 0 and a % 100 != 0) or (a % 400 == 0)
        
        total_dias = año * 365
        for a in range(0, año):
            if es_bisiesto(a): total_dias += 1
        
        for m in range(1, mes):
            total_dias += dias_por_mes[m - 1]
            if m == 2 and es_bisiesto(año): total_dias += 1
        
        total_dias += dia
        return total_dias

    except (ValueError, IndexError):
        # Captura errores si la conversión a entero falla o el formato es incorrecto
        return None

def CALCULAR_MORA(fecha_limite_str, fecha_actual_str):
    """Calcula los días de mora: diferencia (fecha_actual - fecha_limite).
    Retorna 0 si no hay mora o si alguna fecha no se puede parsear.
    Formato esperado: 'DD/MM/AAAA'. Usa `fecha_a_dias`.
    """
    try:
        limite = fecha_a_dias(fecha_limite_str)
        actual = fecha_a_dias(fecha_actual_str)
        if limite is None or actual is None:
            return 0
        dias = actual - limite
        return dias if dias > 0 else 0
    except Exception:
        return 0

LIMITE_MULTA_BLOQUEO = 20000
multas_acumuladas = {}

def esta_bloqueado(id_usuario):
    """
    Verifica si la multa acumulada del usuario excede el límite de 20K.
    """
    multa_pendiente = multas_acumuladas.get(id_usuario, 0)
    # Retorna True si la multa es >= 20000
    return multa_pendiente >= LIMITE_MULTA_BLOQUEO

# --- Historial y recomendaciones ---
historial = {}

def registrar_lectura_usuario(id_usuario, isbn):
    if not id_usuario or not isbn:
        return
    if id_usuario not in historial:
        historial[id_usuario] = set()
    historial[id_usuario].add(isbn)

def inicializar_historial_desde_prestamos(prestamos_list):
    for p in prestamos_list:
        uid = p.get('ID_Usuario')
        isbn = p.get('ISBN')
        if uid and isbn:
            if uid not in historial:
                historial[uid] = set()
            historial[uid].add(isbn)

def _parsear_estrellas(reseña_texto):
    if not reseña_texto:
        return None
    return reseña_texto.count('★')

def promedio_calificacion_por_isbn(isbn):
    if not isbn:
        return 0.0
    entradas = RESEÑAS.get(isbn, [])
    total = 0
    cnt = 0
    for r in entradas:
        p = _parsear_estrellas(r)
        if p:
            total += p
            cnt += 1
    return (total / cnt) if cnt > 0 else 0.0

def categorias_mas_leidas(id_usuario, top_n=3):
    if id_usuario not in historial:
        return []
    freq = {}
    for isbn in historial[id_usuario]:
        for lib in libros:
            if lib.get('ISBN') == isbn:
                cat = lib.get('categoria', 'Desconocida')
                freq[cat] = freq.get(cat, 0) + 1
                break
    return sorted(freq.items(), key=lambda x: x[1], reverse=True)[:top_n]

def mejores_en_categoria(categoria, top_n=5):
    candidatos = [lib for lib in libros if lib.get('categoria','').lower() == categoria.lower()]
    scored = []
    for lib in candidatos:
        cal = promedio_calificacion_por_isbn(lib.get('ISBN'))
        scored.append((cal, lib))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [lib for cal, lib in scored[:top_n]]

def usuarios_similares(id_usuario, top_k=3):
    if id_usuario not in historial:
        return []
    target = historial[id_usuario]
    sims = []
    for uid, s in historial.items():
        if uid == id_usuario:
            continue
        inter = len(target & s)
        union = len(target | s)
        jaccard = (inter / union) if union > 0 else 0
        sims.append((jaccard, uid))
    sims.sort(key=lambda x: x[0], reverse=True)
    return [uid for score, uid in sims[:top_k]]

def recomendar_por_similares(id_usuario, top_n=10):
    similares = usuarios_similares(id_usuario, top_k=5)
    recomendaciones = {}
    leidos = historial.get(id_usuario, set())
    for uid in similares:
        for isbn in historial.get(uid, set()):
            if isbn in leidos:
                continue
            recomendaciones[isbn] = recomendaciones.get(isbn, 0) + 1
    ranked = []
    for isbn, freq in recomendaciones.items():
        cal = promedio_calificacion_por_isbn(isbn)
        ranked.append((freq, cal, isbn))
    ranked.sort(key=lambda x: (x[0], x[1]), reverse=True)
    result = []
    for freq, cal, isbn in ranked[:top_n]:
        lib = next((l for l in libros if l.get('ISBN') == isbn), None)
        if lib:
            result.append(lib)
    return result

def recomendar(id_usuario, top_n=10):
    recomendaciones = []
    cats = categorias_mas_leidas(id_usuario, top_n=3)
    for cat, _ in cats:
        mejores = mejores_en_categoria(cat, top_n=3)
        for m in mejores:
            if m not in recomendaciones:
                recomendaciones.append(m)
                if len(recomendaciones) >= top_n:
                    return recomendaciones
    por_sim = recomendar_por_similares(id_usuario, top_n=top_n)
    for p in por_sim:
        if p not in recomendaciones:
            recomendaciones.append(p)
            if len(recomendaciones) >= top_n:
                break
    return recomendaciones

historial = {}

def registrar_lectura_usuario(id_usuario, isbn):
    """Registra un ISBN como leído por el usuario en `historial`."""
    if not id_usuario or not isbn:
        return
    if id_usuario not in historial:
        historial[id_usuario] = set()
    historial[id_usuario].add(isbn)

def inicializar_historial_desde_prestamos(prestamos_list):
    """Llena `historial` usando los préstamos actuales/pasados proporcionados."""
    for p in prestamos_list:
        uid = p.get('ID_Usuario')
        isbn = p.get('ISBN')
        if uid and isbn:
            if uid not in historial:
                historial[uid] = set()
            historial[uid].add(isbn)

def _parsear_estrellas(reseña_texto):
    """Extrae la calificación numérica (1-5) de una reseña que usa '★' al inicio."""
    if not reseña_texto:
        return None
    # contar caracteres '★' en la reseña
    count = reseña_texto.count('★')
    return count if 1 <= count <= 5 else None

def promedio_calificacion_por_isbn(isbn):
    """Calcula la calificación promedio para un ISBN o título (si existen reseñas)."""
    if not isbn:
        return 0.0
    entradas = RESEÑAS.get(isbn, [])
    if not entradas:
        # También buscar por título en minúsculas
        entradas = RESEÑAS.get(isbn, [])
    total = 0
    cnt = 0
    for r in entradas:
        p = _parsear_estrellas(r)
        if p:
            total += p
            cnt += 1
    return (total / cnt) if cnt > 0 else 0.0

def categorias_mas_leidas(id_usuario, top_n=3):
    """Devuelve las categorías más leídas por el usuario (basado en `historial`)."""
    if id_usuario not in historial:
        return []
    freq = {}
    for isbn in historial[id_usuario]:
        for lib in libros:
            if lib.get('ISBN') == isbn:
                cat = lib.get('categoria', 'Desconocida')
                freq[cat] = freq.get(cat, 0) + 1
                break
    return sorted(freq.items(), key=lambda x: x[1], reverse=True)[:top_n]

def mejores_en_categoria(categoria, top_n=5):
    """Devuelve los mejores libros en una categoría según calificación promedio."""
    candidatos = [lib for lib in libros if lib.get('categoria', '').lower() == categoria.lower()]
    scored = []
    for lib in candidatos:
        cal = promedio_calificacion_por_isbn(lib.get('ISBN'))
        scored.append((cal, lib))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [lib for cal, lib in scored[:top_n]]

def usuarios_similares(id_usuario, top_k=3):
    #Encuentra usuarios con gustos similares por Jaccard en `historial`.
    if id_usuario not in historial:
        return []
    target = historial[id_usuario]
    sims = []
    for uid, s in historial.items():
        if uid == id_usuario:
            continue
        inter = len(target & s)
        union = len(target | s)
        jaccard = (inter / union) if union > 0 else 0
        sims.append((jaccard, uid))
    sims.sort(key=lambda x: x[0], reverse=True)
    return [uid for score, uid in sims[:top_k]]

def recomendar_por_similares(id_usuario, top_n=10):
    #Recomendacion libros leídos por usuarios similares que el usuario objetivo no ha leído.
    similares = usuarios_similares(id_usuario, top_k=5)
    recomendaciones = {}
    leidos = historial.get(id_usuario, set())
    for uid in similares:
        for isbn in historial.get(uid, set()):
            if isbn in leidos:
                continue
            recomendaciones[isbn] = recomendaciones.get(isbn, 0) + 1
    # Ordenar por frecuencia y calificación
    ranked = []
    for isbn, freq in recomendaciones.items():
        cal = promedio_calificacion_por_isbn(isbn)
        ranked.append((freq, cal, isbn))
    ranked.sort(key=lambda x: (x[0], x[1]), reverse=True)
    result = []
    for freq, cal, isbn in ranked[:top_n]:
        # buscar libro por isbn
        lib = next((l for l in libros if l.get('ISBN') == isbn), None)
        if lib:
            result.append(lib)
    return result

def recomendar(id_usuario, top_n=10):
    """Combina: categorías favoritas + mejores en esas categorías + sugerencias por usuarios similares."""
    recomendaciones = []
    # 1) Categorías más leídas
    cats = categorias_mas_leidas(id_usuario, top_n=3)
    for cat, _ in cats:
        mejores = mejores_en_categoria(cat, top_n=3)
        for m in mejores:
            if m not in recomendaciones:
                recomendaciones.append(m)
                if len(recomendaciones) >= top_n:
                    return recomendaciones
    # 2) Añadir recomendaciones por similares
    por_sim = recomendar_por_similares(id_usuario, top_n=top_n)
    for p in por_sim:
        if p not in recomendaciones:
            recomendaciones.append(p)
            if len(recomendaciones) >= top_n:
                break
    return recomendaciones

LIMITE_MULTA_BLOQUEO = 20000 
multas_acumuladas = {} 

def agregar_dias_fecha(fecha_str, dias_a_sumar):
    """
    Suma un número de días a una fecha en formato 'DD/MM/AAAA' 
    (Asume 30 días por mes para simplificar sin la librería datetime).
    """
    try:
        # 1. Convertir 'DD/MM/AAAA' a enteros
        # Usamos split('/') ya que tu formato de fecha es DD/MM/AAAA.
        d, m, a = map(int, fecha_str.split('/')) 
    except:
        # Esto ocurre si fecha_actual_global no está en el formato correcto
        print("\nERROR INTERNO: El formato de fecha global no es DD/MM/AAAA.")
        return "Error de Fecha"

    d_total = d + dias_a_sumar
    
    # 2. Manejar el desbordamiento de meses y años (Ciclo manual)
    while d_total > 30: # Usamos 30 como valor constante de días por mes
        d_total -= 30
        m += 1
        # Manejar el desbordamiento de año
        if m > 12:
            m -= 12
            a += 1
            
    # 3. Formatear el resultado (usando f-string para asegurar 0 adelante)
    return f"{d_total:02d}/{m:02d}/{a}"

def APARTAR_LIBRO(id_usuario=None, prestamos=None):
    if prestamos is None:
        prestamos = []
    
    # --- 1. VALIDAR USUARIO Y PRIVILEGIOS ---
    usuario = None
    # Definir privilegios por defecto para usuarios no registrados (tipo "Externo")
    dias_prestamo = 7 
    max_libros = 2    
    
    if id_usuario:
        # Si hay ID, buscar al usuario
        for u in datos:
            if u['ID'] == id_usuario:
                usuario = u
                break
        
        if not usuario:
            print(f"Error: Usuario con ID '{id_usuario}' no encontrado.")
            return

        # --- 2. VERIFICACIÓN DE BLOQUEO POR MULTA (para usuarios registrados) ---
        actualizar_multas_globales() # [cite: 61]

        if esta_bloqueado(id_usuario): # [cite: 61]
            multa_pendiente = multas_acumuladas.get(id_usuario, 0)
            print(f"\n¡USUARIO BLOQUEADO!")
            print(f"Su multa acumulada de ${multa_pendiente:,} excede el límite de ${LIMITE_MULTA_BLOQUEO:,}.")
            print("Debe pagar su deuda (Opción 12) antes de realizar nuevos préstamos/apartados.")
            return

        # --- 3. VERIFICACIÓN DE LÍMITE DE LIBROS (para usuarios registrados) ---
        # Obtener los privilegios correctos
        max_libros, dias_prestamo = obtener_privilegios(usuario['Tipo de Usuario'])
        libros_actuales = contar_libros_usuario(id_usuario, prestamos)
        
        if libros_actuales >= max_libros:
            print(f"Lo siento, ya tiene el máximo de {max_libros} libros prestados.")
            print(f"Tipo de usuario: {usuario['Tipo de Usuario']}")
            return
    
    # --- 4. OBTENER Y BUSCAR LIBRO ---
    identificador = input("Ingrese el ISBN o Título del libro a apartar: ")
    
    libro_encontrado = None
    for libro in libros:
        # Búsqueda por ISBN o Título
        if libro['ISBN'] == identificador or libro['Titulo'].lower() == identificador.lower():
            libro_encontrado = libro
            break

    if not libro_encontrado:
        print(f"ERROR: Libro no encontrado con ISBN/Título '{identificador}'.")
        return

    # --- 5. VERIFICAR DISPONIBILIDAD ---
    # Usamos 'Copias' y 'reservado' como en tu lista 'libros'
    copias_totales = int(libro_encontrado.get('Copias', 0))
    reservados_actuales = int(libro_encontrado.get('reservado', 0))

    if copias_totales <= reservados_actuales: 
        print(f"ERROR: El libro '{libro_encontrado['Titulo']}' no tiene copias disponibles para préstamo.")
        return
        
    # --- 6. CALCULAR FECHA DE DEVOLUCIÓN ---
    # ¡AQUÍ USAMOS 'dias_prestamo' (7, 15 o 30) en lugar de la variable que no existía!
    fecha_devolucion_max = agregar_dias_fecha(fecha_actual_global, dias_prestamo)
    
    # --- 7. CREAR EL REGISTRO DE PRÉSTAMO (LA PARTE QUE FALTABA) ---
    nuevo_prestamo = {
        'ID_Usuario': id_usuario if id_usuario else "Visitante", # Manejar usuario no registrado
        'ISBN': libro_encontrado['ISBN'],
        'Titulo': libro_encontrado['Titulo'],
        'Fecha_Prestamo': fecha_actual_global,
        'Fecha_Devolucion': fecha_devolucion_max, 
        'Devuelto': False,
        'Multa_Monto': 0,
        'Multa_Pagada': True,
        'Renovaciones': 0
    }
    # ¡ESTA ES LA LÍNEA CLAVE QUE FALTABA DENTRO DE LA FUNCIÓN!
    prestamos.append(nuevo_prestamo) 
    
    # --- 8. ACTUALIZAR INVENTARIO Y CONFIRMAR ---
    libro_encontrado['reservado'] += 1 

    print("\n---------------------------------------------------------")
    print(f"✅ ¡PRÉSTAMO APROBADO Y REGISTRADO!")
    print(f"Libro: {libro_encontrado['Titulo']} (ISBN: {libro_encontrado['ISBN']})")
    if usuario:
        print(f"Usuario: {usuario['Nombre']} (ID: {id_usuario})")
    else:
        print("Usuario: Visitante (sin registro)")
    print(f"Fecha de Préstamo: {fecha_actual_global}")
    print(f"Fecha MÁXIMA de Devolución: *{fecha_devolucion_max}* (Plazo: {dias_prestamo} días)")
    print(f"Copias prestadas/reservadas ahora: {libro_encontrado['reservado']}")
    print("---------------------------------------------------------")
    if prestamos is None:
        prestamos = []
    
    IsbnNombre = input("Ingrese el ISBN o título del libro que desea apartar: ")
    
    # Si se da el ID de usuario, validar privilegios Y MULTAS
    if id_usuario:
        usuario = None
        for u in datos:
            if u['ID'] == id_usuario:
                usuario = u
                break
        
        if usuario:
            # --- VERIFICACIÓN DE BLOQUEO POR MULTA ---
            multa_actual, _ = calcular_multa_total_usuario(id_usuario)
            
            if multa_actual > LIMITE_MULTA_BLOQUEO:
                print(f"\n==================== ACCIÓN BLOQUEADA ====================")
                print(f"Usuario: {usuario.get('Nombre', 'N/A')}")
                print(f"Motivo: Multa pendiente superior al límite permitido.")
                print(f"  -> Su multa actual: ${multa_actual:,}")
                print(f"  -> Límite permitido: ${LIMITE_MULTA_BLOQUEO:,}")
                print(f"\nPor favor, pague su multa (Opción 12) para volver a apartar libros.")
                print(f"============================================================")
                return
            # --- FIN DE LA VERIFICACIÓN ---

            # Verificación de límite de libros (lógica existente)
            max_libros, dias_prestamo = obtener_privilegios(usuario['Tipo de Usuario'])
            libros_actuales = contar_libros_usuario(id_usuario, prestamos)
            
            if libros_actuales >= max_libros:
                print(f"Lo siento, ya tiene el máximo de {max_libros} libros prestados.")
                print(f"Tipo de usuario: {usuario['Tipo de Usuario']}")
                print(f"Días de préstamo permitidos: {dias_prestamo}")
                return
    
    # Lógica existente para buscar y apartar el libro
    for libro in libros: 
        if libro['ISBN'] == IsbnNombre or libro['Titulo'].lower() == IsbnNombre.lower():
            if libro['Copias'] > libro['reservado']:
                libro['reservado'] += 1
                print(f"El libro '{libro['Titulo']}' ha sido apartado exitosamente.")
                if usuario:
                    max_libros, dias_prestamo = obtener_privilegios(usuario['Tipo de Usuario'])
                    print(f"Días de préstamo: {dias_prestamo}")
            else:
                print(f"Lo siento, no hay copias disponibles para el libro '{libro['Titulo']}'.")
            return
    print("No se encontró un libro con ese ISBN o título.")

    # --- 2. VERIFICACIÓN DE BLOQUEO POR MULTA ACUMULADA ---
    # PRIMERO: Forzar la acumulación de multas (VITAL para corregir el bug)
    actualizar_multas_globales() 

    if esta_bloqueado(id_usuario): # Asumo que esta_bloqueado ya existe y usa multas_acumuladas
        # Lógica para obtener la multa pendiente sin .get()
        multa_pendiente = 0
        if id_usuario in multas_acumuladas:
            multa_pendiente = multas_acumuladas[id_usuario]

        print(f"\n¡USUARIO BLOQUEADO!")
        print(f"Su multa acumulada de ${multa_pendiente:,} excede el límite de ${LIMITE_MULTA_BLOQUEO:,}.")
        print("Debe pagar su deuda (Opción 12) antes de realizar nuevos préstamos/apartados.")
        return 
    # ------------------------------------------------------

    # 3. Obtener identificador del libro
    identificador = input("Ingrese el ISBN o Título del libro a apartar: ")
    libro_encontrado = None

    # 4. Buscar el libro y verificar disponibilidad
    for libro in libros: # Asumo que la lista de libros se llama 'libros'
        # Búsqueda por ISBN o Título (usando acceso directo [])
        if libro['ISBN'] == identificador or libro['Titulo'] == identificador:
            libro_encontrado = libro
            break

    if not libro_encontrado:
        print(f"ERROR: Libro no encontrado con ISBN/Título '{identificador}'.")
        return

    # Verificar disponibilidad (Cantidad_Disponible vs. reservado)
    if libro_encontrado['Cantidad_Disponible'] <= libro_encontrado['reservado']: 
        print(f"ERROR: El libro '{libro_encontrado['Titulo']}' no tiene copias disponibles para préstamo.")
        return
        
    # 5. Calcular fecha de devolución
    fecha_devolucion_max = agregar_dias_fecha(fecha_actual_global, dias_prestamo)
    
    # 6. Crear el nuevo registro de préstamo
    nuevo_prestamo = {
        'ID_Usuario': id_usuario,
        'ISBN': libro_encontrado['ISBN'],
        'Titulo': libro_encontrado['Titulo'],
        'Fecha_Prestamo': fecha_actual_global,
        'Fecha_Devolucion': fecha_devolucion_max, # Clave usada para el límite de devolución
        'Devuelto': False,
        'Multa_Monto': 0,
        'Multa_Pagada': True 
    }
    prestamos.append(nuevo_prestamo)
    
    # 7. Actualizar el inventario: incrementar el contador de libros prestados
    libro_encontrado['reservado'] += 1

    print("\n---------------------------------------------------------")
    print(f"✅ ¡PRÉSTAMO APROBADO Y REGISTRADO!")
    print(f"Libro: {libro_encontrado['Titulo']} (ISBN: {libro_encontrado['ISBN']})")
    print(f"Fecha de Préstamo: {fecha_actual_global}")
    print(f"Fecha MÁXIMA de Devolución: *{fecha_devolucion_max}* (Plazo: {dias_prestamo} días)")
    print(f"Copias prestadas/reservadas ahora: {libro_encontrado['reservado']}")
    print("---------------------------------------------------------")
    if prestamos is None:
        prestamos = []
    
    # 1. Solicitar el ID de usuario si es necesario
    if not id_usuario:
        id_usuario = input("Ingrese el ID del usuario: ")

    # >>> CAMBIO CLAVE A AÑADIR AQUÍ:
    # Sincronizar multas antes de verificar el bloqueo.
    actualizar_multas_globales()

    # 2. VERIFICAR BLOQUEO POR MULTA ACUMULADA
    if esta_bloqueado(id_usuario): # [cite: 280]
        multa_pendiente = multas_acumuladas.get(id_usuario, 0)
        
        print(f"\n¡USUARIO BLOQUEADO!")
        print(f"Su multa acumulada de ${multa_pendiente:,} excede el límite de ${LIMITE_MULTA_BLOQUEO:,}.") # [cite: 280]
        print("Debe pagar su deuda (Opción 12) antes de realizar nuevos préstamos/apartados.")
        return # Sale de la función antes de cualquier otra lógica

def obtener_nombre_libro(isbn):
    """Busca el nombre del libro usando su ISBN en la lista libros."""
    for l in libros:
        if l.get('ISBN') == isbn:
            return l.get('Titulo')
    return "Desconocido"

def obtener_nombre_usuario(id_u):
    """Busca el nombre del usuario en la lista datos."""
    for u in datos:
        if u.get('ID') == id_u:
            return u.get('Nombre')
    return "Desconocido"

#RENOVAR_PRESTAMO
#Permite al usuario extender el plazo de un préstamo activo si cumple con las reglas
#(no estar bloqueado, no haber excedido el límite de renovaciones, etc.).
#Calcula una nueva fecha de devolución máxima.

def RENOVAR_PRESTAMO(id_usuario):
    global prestamos, fecha_actual_global

    if not fecha_actual_global:
        print("ERROR: Por favor, modifique la fecha actual (Opción 2) antes de continuar.")
        return

    # 1. Chequeo de bloqueo
    actualizar_multas_globales()
    if esta_bloqueado(id_usuario):
        print("\n Renovación CANCELADA: Usuario BLOQUEADO por multas pendientes.")
        print("Pague su deuda (Opción 12) antes de intentar renovar.")
        return

    # 2. Obtener privilegios
    usuario = next((u for u in datos if u['ID'] == id_usuario), None)
    if not usuario:
        print(f"ERROR: Usuario con ID '{id_usuario}' no encontrado.")
        return
        
    max_libros, dias_prestamo = obtener_privilegios(usuario['Tipo de Usuario'])

    isbn_libro = input("Ingrese el ISBN del libro que desea renovar: ")
    
    prestamo_encontrado = None
    for p in prestamos:
        # Buscar préstamo activo
        if p.get('ID_Usuario') == id_usuario and \
            p.get('ISBN') == isbn_libro and \
            p.get('Devuelto', False) == False:
            
            # Chequeo de mora (no se puede renovar un libro en mora)
            dias_mora = CALCULAR_MORA(p.get('Fecha_Devolucion', ''), fecha_actual_global)
            
            if dias_mora > 0:
                print(f"\n Renovación CANCELADA: El libro está en mora ({dias_mora} días).")
                print("Debe devolverlo y pagar la multa (Opción 12) antes de intentar un nuevo préstamo.")
                return
            
            # Chequeo de límite de renovación
            if p.get('Renovaciones', 0) >= 1:
                print("\n Renovación CANCELADA: Este préstamo ya ha sido renovado una vez (LÍMITE ALCANZADO).")
                return

            prestamo_encontrado = p
            break

    if not prestamo_encontrado:
        print("ERROR: No se encontró un préstamo activo para ese libro y usuario.")
        return

    # 3. Realizar la renovación
    fecha_antigua = prestamo_encontrado['Fecha_Devolucion']
    
    # La nueva fecha se calcula a partir de la fecha actual global
    prestamo_encontrado['Fecha_Devolucion'] = agregar_dias_fecha(fecha_actual_global, dias_prestamo)
    prestamo_encontrado['Renovaciones'] = prestamo_encontrado.get('Renovaciones', 0) + 1
    
    print("\n---------------------------------------------------------")
    print("✅ ¡RENOVACIÓN EXITOSA!")
    print(f"Libro: {prestamo_encontrado.get('Titulo', 'N/A')}")
    print(f"Usuario: {id_usuario}")
    print(f"Antigua Fecha de Devolución: {fecha_antigua}")
    print(f"NUEVA Fecha de Devolución: **{prestamo_encontrado['Fecha_Devolucion']}** (Plazo renovado: {dias_prestamo} días)")
    print(f"Renovaciones restantes: {1 - prestamo_encontrado.get('Renovaciones', 1)}")
    print("---------------------------------------------------------")

def esta_bloqueado(id_usuario):
    """Verifica si la multa acumulada del usuario excede el límite de 20K."""
    multa_pendiente = multas_acumuladas.get(id_usuario, 0)
    return multa_pendiente >= LIMITE_MULTA_BLOQUEO

def ver_privilegios_usuario(id_usuario):
    # Muestra los privilegios de un usuario específico
    usuario = None
    for u in datos:
        if u['ID'] == id_usuario:
            usuario = u
            break
    
    if usuario:
        max_libros, dias_prestamo = obtener_privilegios(usuario['Tipo de Usuario'])
        print(f"\n=== PRIVILEGIOS DE {usuario['Nombre'].upper()} ===")
        print(f"Tipo de usuario: {usuario['Tipo de Usuario']}")
        print(f"Máximo de libros permitidos: {max_libros}")
        print(f"Días de préstamo: {dias_prestamo}")
        print(" \n")
    else:
        print("Usuario no encontrado.")

# TARIFA DIARIA DE MULTA (2K = 2000)
TARIFA_MULTA_DIARIA = 2000

#DEVOLVER_LIBRO
#Permite a un usuario devolver un libro prestado.
#Procesa la devolución de un libro: calcula la multa por retraso (si aplica), 
# marca el préstamo como devuelto,
#decrementa el contador 'reservado' del libro y actualiza las multas globales del usuario.


def DEVOLVER_LIBRO():
    global prestamos, libros, fecha_actual_global, TARIFA_MULTA_DIARIA, multas_acumuladas, LIMITE_MULTA_BLOQUEO
    
    # 1. Solicitar datos de devolución
    id_usuario = input("\nIngrese el ID del usuario que devuelve el libro: ")
    # Usamos el ISBN, ya que es más seguro para la búsqueda.
    isbn_libro = input("Ingrese el ISBN del libro a devolver: ")

    if not fecha_actual_global:
        print("ERROR: La fecha actual no está definida. Use la Opción 2 para establecerla.")
        return

    prestamo_encontrado = None
    
    # 2. Buscar el préstamo activo (CORRECCIÓN: Se usa la clave 'ISBN')
    for p in prestamos:
        if p['ID_Usuario'] == id_usuario and \
            p['ISBN'] == isbn_libro and \
            p['Devuelto'] == False: # Asumimos 'Devuelto' existe y es False para préstamos activos
            
            prestamo_encontrado = p
            break

    if prestamo_encontrado:
        
        # 3. Calcular la mora y la multa
        fecha_limite = prestamo_encontrado['Fecha_Devolucion']
        # CALCULAR_MORA ya existe en tu código y funciona con el formato 'DD/MM/AAAA'
        dias_mora = CALCULAR_MORA(fecha_limite, fecha_actual_global)

        monto_multa = 0
        if dias_mora > 0:
            # CORRECCIÓN: Usando la nueva constante TARIFA_MULTA_DIARIA
            monto_multa = dias_mora * TARIFA_MULTA_DIARIA 

            print(f"\n ¡DEVOLUCIÓN CON MORA!")
            print(f"La fecha límite de devolución era: **{fecha_limite}**")
            print(f"Días de retraso: **{dias_mora}** días.")
            print(f"Monto de la multa por este préstamo: ${monto_multa:,}")
        else:
            print(f"\n DEVOLUCIÓN A TIEMPO ({fecha_actual_global}).")


        # 4. Actualizar el estado del préstamo
        prestamo_encontrado['Devuelto'] = True
        prestamo_encontrado['Fecha_Devolucion_Real'] = fecha_actual_global
        prestamo_encontrado['Multa_Monto'] = monto_multa
        prestamo_encontrado['Multa_Pagada'] = (monto_multa == 0) # Si es 0, se considera pagada/nula
        
        # 5. Actualizar el inventario (restar 1 a 'reservado')
        isbn_a_devolver = prestamo_encontrado['ISBN']
        
        for libro in libros:
            if libro['ISBN'] == isbn_a_devolver:
                if libro['reservado'] > 0: 
                    libro['reservado'] -= 1
                    print(f"Stock de '{libro['Titulo']}' actualizado. Copias reservadas restantes: {libro['reservado']}")
                break
        
        # 6. Sincronizar las multas globales (VITAL para el bloqueo)
        # Esto actualizará 'multas_acumuladas' con la nueva deuda (si existe).
        actualizar_multas_globales() 
        
        # Mostrar la multa acumulada y si quedó bloqueado
        multa_total_usuario = multas_acumuladas[id_usuario] if id_usuario in multas_acumuladas else 0
        if multa_total_usuario > 0:
            print(f"**Multa total acumulada PENDIENTE: ${multa_total_usuario:,}**")
            if multa_total_usuario >= LIMITE_MULTA_BLOQUEO:
                 print(f" ¡ADVERTENCIA! Su multa excede los ${LIMITE_MULTA_BLOQUEO:,} y **ha quedado BLOQUEADO** para nuevos préstamos.")

        print(f"\nEl libro '{isbn_libro}' ha sido devuelto exitosamente por el usuario {id_usuario}.")

    else:
        print("\n Error: No se encontró un préstamo activo (no devuelto) para ese usuario y ISBN.")

def calcular_multa_por_retraso(dias_mora):
    """Calcula la multa por retraso en la devolución de un libro
    Args:
        dias_mora: número de días de retraso
    Returns:
        multa_total: cantidad de multa a pagar
    """
    if dias_mora <= 0:
        return 0
    
    multa_total = dias_mora * TARIFA_MULTA_DIARIA
    return multa_total

def calcular_multa_total_usuario(id_usuario):
    """Calcula la multa total de un usuario por todos sus préstamos en mora
        que aún no han sido pagados.
    Args:
        id_usuario: ID del usuario
    Returns:
        multa_total: suma de todas las multas pendientes
        detalles: lista de tuplas (titulo_libro, dias_mora, multa_individual, prestamo_dict)
    """
    prestamos_usuario = [p for p in prestamos if p.get('ID_Usuario') == id_usuario]
    multa_total = 0
    detalles = []
    
    for prestamo in prestamos_usuario:
        
        # CASO 1: Préstamo ACTIVO (No devuelto)
        if not prestamo.get('Devuelto', False):
            # Calcular mora actual
            dias_mora = CALCULAR_MORA(prestamo.get('Fecha_Devolucion', ''), fecha_actual_global)
            
            if dias_mora > 0:
                multa_individual = calcular_multa_por_retraso(dias_mora)
                multa_total += multa_individual
                titulo = prestamo.get('Titulo', 'N/A')
                detalles.append((titulo, dias_mora, multa_individual, prestamo))
        
        # CASO 2: Préstamo DEVUELTO, pero multa NO pagada
        # (Esto ocurre si se usó la Opción 14 pero no la Opción 12)
        elif prestamo.get('Devuelto', True) and not prestamo.get('Multa_Pagada', False):
            multa_individual = prestamo.get('Multa_Monto', 0)
            if multa_individual > 0:
                multa_total += multa_individual
                titulo = prestamo.get('Titulo', 'N/A')
                
                # Calcular los días de mora que tenía cuando se devolvió
                fecha_limite = prestamo.get('Fecha_Devolucion', '')
                fecha_devolucion_real = prestamo.get('Fecha_Devolucion_Real', fecha_limite)
                dias_mora = CALCULAR_MORA(fecha_limite, fecha_devolucion_real)
                
                detalles.append((titulo, dias_mora, multa_individual, prestamo))

    return multa_total, detalles
    """Calcula la multa total de un usuario por todos sus préstamos en mora
        que aún no han sido pagados.
    Args:
        id_usuario: ID del usuario
    Returns:
        multa_total: suma de todas las multas pendientes
        detalles: lista de tuplas (titulo_libro, dias_mora, multa_individual, prestamo_dict)
    """
    prestamos_usuario = [p for p in prestamos if p.get('ID_Usuario') == id_usuario] #  (modificado)
    multa_total = 0
    detalles = []
    
    for prestamo in prestamos_usuario:
        # NUEVA VERIFICACIÓN: Ignorar si la multa ya fue pagada
        if prestamo.get('Multa_Pagada', False):
            continue
            
        dias_mora = CALCULAR_MORA(prestamo.get('Fecha_Devolucion', ''), fecha_actual_global) # 
        
        if dias_mora > 0: # 
            multa_individual = calcular_multa_por_retraso(dias_mora) # 
            multa_total += multa_individual # 
            titulo = prestamo.get('Titulo', 'N/A') # 
            # MODIFICACIÓN: Devolver también el diccionario del préstamo
            detalles.append((titulo, dias_mora, multa_individual, prestamo))
    
    return multa_total, detalles

def actualizar_multas_globales():
    """
    Recalcula la multa total pendiente para cada usuario con préstamos activos 
    y actualiza la variable global `multas_acumuladas`. Esto es crucial para
    que la función `esta_bloqueado` funcione correctamente al cambiar la fecha.
    """
    global multas_acumuladas, prestamos
    # Asegurarse de que `fecha_actual_global` tiene un valor antes de calcular
    if not fecha_actual_global:
        return

    # 1. Obtener todos los IDs de usuarios con préstamos activos (no devueltos)
    # y multas no pagadas.
    usuarios_con_multa_potencial = set(p['ID_Usuario'] for p in prestamos if not p.get('Devuelto') or p.get('Multa_Pagada') == False)
    
    # 2. Reiniciar o limpiar el acumulador global
    nuevas_multas = {}

    # 3. Recalcular y actualizar solo para esos usuarios
    for id_usuario in usuarios_con_multa_potencial:
        # Reutiliza la función que ya tienes para calcular la multa total de un usuario
        multa_total, _ = calcular_multa_total_usuario(id_usuario) 
        if multa_total > 0:
            nuevas_multas[id_usuario] = multa_total
            
    # 4. Reemplazar el diccionario global para que `esta_bloqueado` sea preciso
    multas_acumuladas = nuevas_multas

def ver_historial_prestamos(id_usuario):
    """Muestra el historial de préstamos de un usuario con detalles completos"""
    usuario = None
    for u in datos:
        if u['ID'] == id_usuario:
            usuario = u
            break
    
    if not usuario:
        print("\nUsuario no encontrado.")
        return
    
    # Obtener todos los préstamos del usuario
    prestamos_usuario = [p for p in prestamos if p['ID_Usuario'] == id_usuario]
    
    print(f"\n{'='*120}")
    print(f"HISTORIAL DE PRÉSTAMOS - {usuario['Nombre'].upper()}")
    print(f"ID Usuario: {id_usuario} | Tipo: {usuario['Tipo de Usuario']}")
    print(f"{'='*120}\n")
    
    if not prestamos_usuario:
        print("Este usuario no tiene préstamos registrados.")
        print(" ")
        return
    
    # Mostrar encabezados de tabla
    print(f"{'N°':<4} | {'Título':<30} | {'Autor':<25} | {'ISBN':<20} | {'Fecha Préstamo':<15} | {'Fecha Devolución':<15} | {'Estado':<12} | {'Días Mora':<10}")
    print("-" * 120)
    
    # Mostrar cada préstamo
    for idx, prestamo in enumerate(prestamos_usuario, 1):
        titulo = prestamo.get('Titulo', 'N/A')[:28]
        
        # Buscar autor en la lista de libros
        autor = 'N/A'
        for libro in libros:
            if libro.get('ISBN') == prestamo.get('ISBN'):
                autor = libro.get('Autor', 'N/A')[:23]
                break
        
        isbn = prestamo.get('ISBN', 'N/A')[:18]
        fecha_prestamo = prestamo.get('Fecha_Prestamo', 'N/A')
        fecha_devolucion = prestamo.get('Fecha_Devolucion', 'N/A')
        
        # Calcular días de mora
        dias_mora = CALCULAR_MORA(fecha_devolucion, fecha_actual_global)
        
        # Determinar estado
        if dias_mora > 0:
            estado = "MORA"
        else:
            estado = "Vigente"
        
        print(f"{idx:<4} | {titulo:<30} | {autor:<25} | {isbn:<20} | {fecha_prestamo:<15} | {fecha_devolucion:<15} | {estado:<12} | {dias_mora:<10}")
    
    print("-" * 120)
    
    # Resumen
    total_prestamos = len(prestamos_usuario)
    prestamos_mora = sum(1 for p in prestamos_usuario if CALCULAR_MORA(p.get('Fecha_Devolucion', ''), fecha_actual_global) > 0)
    total_dias_mora = sum(CALCULAR_MORA(p.get('Fecha_Devolucion', ''), fecha_actual_global) for p in prestamos_usuario)
    
    # Calcular multa total
    multa_total, detalles_multa = calcular_multa_total_usuario(id_usuario)
    
    print(f"\nRESUMEN:")
    print(f"  Total de préstamos: {total_prestamos}")
    print(f"  Préstamos con mora: {prestamos_mora}")
    print(f"  Total días de mora: {total_dias_mora}")
    print(f"  Multa total pendiente: ${multa_total:,}")
    
    if prestamos_mora > 0:
        print(f"\n  DETALLES DE MULTAS:")
        for titulo, dias_mora, multa, _ in detalles_multa:
            print(f"    - {titulo:<40} | Días de mora: {dias_mora:<3} | Multa: ${multa:,}")
        print(f"\n   ADVERTENCIA: Tienes {prestamos_mora} libro(s) con mora y una deuda de ${multa_total:,}")
    
    print(" \n")

def PAGAR_MULTAS(id_usuario):
    """Permite al usuario pagar todas las multas pendientes por retraso."""
    
    # Buscar usuario para mostrar su nombre (lógica similar a [cite: 56])
    usuario = next((u for u in datos if u.get('ID') == id_usuario), None)
    if not usuario:
        print(f"\nError: No se encontró un usuario con el ID '{id_usuario}'.")
        return

    # 1. Calcular multa total pendiente (usa la función modificada)
    multa_total, detalles_multa = calcular_multa_total_usuario(id_usuario)

    print(f"\n{'='*50}")
    print(f"OPCIÓN DE PAGO DE MULTAS - Usuario: {usuario['Nombre'].upper()}") # [cite: 102]
    print(f"{'='*50}")

    if multa_total == 0:
        print("Felicidades, no tiene multas pendientes de pago.") # 
        return

    print(f"\nMulta total pendiente: ${multa_total:,}") # [cite: 65, 123]
    print("Detalles de la(s) multa(s) a pagar:")
    for titulo, dias_mora, multa, prestamo in detalles_multa:
        print(f"  - Libro: {titulo:<40} | Días de mora: {dias_mora:<3} | Multa: ${multa:,}") # [cite: 123]

    # 2. Confirmación de pago
    confirmacion = input("\n¿Desea pagar la multa total ahora? (S/N): ").strip().upper()

    if confirmacion == 'S':
        print(f"\n... Procesando pago de ${multa_total:,} ...")

        # 3. Marcar las multas como pagadas en la lista 'prestamos'
        libros_pagados = []
        for titulo, dias_mora, multa, prestamo_dict in detalles_multa:
            # Esta línea modifica el diccionario original en la lista 'prestamos'
            prestamo_dict['Multa_Pagada'] = True 
            libros_pagados.append(titulo)

        print("\n==============================================")
        print("¡PAGO REALIZADO CON ÉXITO!")
        print(f"Se ha(n) pagado la(s) multa(s) por los siguientes libros:")
        for titulo in libros_pagados:
            print(f"- {titulo}")
        print(f"Total pagado: ${multa_total:,}")
        print("==============================================")
        print("\nRecuerde que el préstamo sigue vigente hasta la devolución física del libro.")
        
    else:
        print("\nPago cancelado. La multa sigue pendiente.")
    print(" ")

def ver_multas_pendientes(id_usuario):
    """Muestra un resumen de las multas pendientes de un usuario sin cobrarlas."""
    
    # 1. Buscar al usuario para mostrar su nombre
    usuario = next((u for u in datos if u.get('ID') == id_usuario), None)
    if not usuario:
        print(f"\nError: No se encontró un usuario con el ID '{id_usuario}'.")
        return

    # 2. Usar tu función existente para obtener los detalles de la multa
    multa_total, detalles_multa = calcular_multa_total_usuario(id_usuario)

    # 3. Imprimir el resumen
    print(f"\n{'='*60}")
    print(f" CONSULTA DE MULTAS PENDIENTES - Usuario: {usuario['Nombre'].upper()}")
    print(f"{'='*60}")

    if multa_total == 0:
        print(f"¡Felicidades! El usuario {usuario['Nombre']} no tiene multas pendientes.")
    else:
        print(f"  El usuario tiene una multa total pendiente de: ${multa_total:,}")
        print("\n  Detalles de la(s) multa(s):")
        
        # Iterar sobre los detalles que te da 'calcular_multa_total_usuario'
        for titulo, dias_mora, multa_individual, _ in detalles_multa:
            print(f"    - Libro: {titulo:<40} | Días de mora: {dias_mora:<3} | Multa: ${multa_individual:,}")
    
    print("-" * 60)
    print(" \n")

def remover_tildes(texto):
    tildes = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N'
    }
    resultado = ""
    for ch in texto: #ch = character ("caracter") papaya
        if ch in tildes:
            resultado += tildes[ch]
        else:
            resultado += ch
    return resultado

PRIVILEGIOS = {
    "Estudiante": (3, 15),      # (máximo libros, días préstamo)
    "Profesor": (5, 30),        # (máximo libros, días préstamo)
    "Externo": (2, 7)           # (máximo libros, días préstamo)
}

def filtrar_por_disponibilidad(libros_list):
    #Muestra los libros donde Copias > reservado y calcula las copias disponibles.
    libros_disponibles = []
    
    # 1. Calcular la disponibilidad
    for libro in libros_list:
        try:
            # Intentar obtener y convertir a int, usando 0 como valor predeterminado si falta
            copias = int(libro.get('Copias', 0))
            reservado = int(libro.get('reservado', 0))
            disponibles = copias - reservado
            
            if disponibles > 0:
                libro_con_disponibilidad = libro.copy()
                libro_con_disponibilidad['Disponibles'] = disponibles
                libros_disponibles.append(libro_con_disponibilidad)
        except (TypeError, ValueError):
            # Ignorar libros con datos inválidos si no se pueden convertir a números
            continue

    # 2. Imprimir la salida (la parte que faltaba)
    if libros_disponibles:
        print("\n=== LIBROS DISPONIBLES PARA PRÉSTAMO/APARTADO ===")
        print(f"| {'Título':<37} | {'ISBN':<20} | {'Disponibles':<12} | {'Categoría':<10} |")
        print("|" + "-" * 39 + "|" + "-" * 22 + "|" + "-" * 14 + "|" + "-" * 12 + "|")
        for libro in libros_disponibles:
            print(f"| {libro.get('Titulo', 'N/A'):<37} | {libro.get('ISBN', 'N/A'):<20} | {libro.get('Disponibles', 0):<12} | {libro.get('categoria', 'N/A'):<10} |")
        print("-" * 83)
    else:
        print("\nActualmente no hay libros con copias disponibles.")

prestamos = [
    {"ID_Usuario": "001", "ISBN": "978-84-376-0494-7", "Titulo": "Cien Años de Soledad", "Fecha_Prestamo": "01/11/2025", "Fecha_Devolucion": "16/11/2025", 'Devuelto': False, 'Multa_Monto': 0, 'Multa_Pagada': True},
    {"ID_Usuario": "002", "ISBN": "120-76-659-3450-2", "Titulo": "Don Quijote de la Mancha", "Fecha_Prestamo": "05/11/2025", "Fecha_Devolucion": "05/12/2025", 'Devuelto': False, 'Multa_Monto': 0, 'Multa_Pagada': True},
    {"ID_Usuario": "004", "ISBN": "978-4-08-851-831-5", "Titulo": "El principito", "Fecha_Prestamo": "10/11/2025", "Fecha_Devolucion": "24/11/2025", 'Devuelto': False, 'Multa_Monto': 0, 'Multa_Pagada': True},
]
# Inicializar historial con los préstamos existentes (para recomendaciones)
try:
    inicializar_historial_desde_prestamos(prestamos)
except Exception:
    pass
USUARIOS = []
libros = [
    {"Titulo": "Cien Años de Soledad", "Autor": "Gabriel García Márquez", "Año": 1967, "ISBN": "978-84-376-0494-7", "Copias": 12, "Ubicación": "Estantería A3", "categoria": "Novela", "reservado": 12},
    {"Titulo": "Don Quijote de la Mancha", "Autor": "Miguel de Cervantes", "Año": 1605, "ISBN": "120-76-659-3450-2", "Copias": 12, "Ubicación": "Estantería A3", "categoria": "Novela", "reservado": 4},
    {"Titulo": "El principito", "Autor": "Antoine de Saint-Exupéry", "Año": 1943, "ISBN": "978-4-08-851-831-5", "Copias": 15, "Ubicación": "Estantería C2", "categoria": "Novela", "reservado": 5},
    {"Titulo": "La divina comedia", "Autor": "Dante Alighieri", "Año": 1320, "ISBN": "978-88-04-589-12-3", "Copias": 12, "Ubicación": "Estantería D4", "categoria": "Poesía", "reservado": 3},
    {"Titulo": "Infierno","Autor":"Dante Alighieri","Año":1320,"ISBN":"978-88-04-589-12-3","Copias":9,"Ubicación":"Estantería D4","categoria":"Poesía", "reservado": 0},
    {"Titulo": "Purgatorio","Autor":"Dante Alighieri","Año":1320,"ISBN":"978-88-04-589-12-3","Copias":10,"Ubicación":"Estantería D4","categoria":"Poesía", "reservado": 0},
    {"Titulo": "Paraíso","Autor":"Dante Alighieri","Año":1320,"ISBN":"978-88-04-589-12-3","Copias":6,"Ubicación":"Estantería D4","categoria":"Poesía", "reservado": 1},
    {"Titulo": "El otoño del patriarca", "Autor": "Gabriel García Márquez", "Año": 1975, "ISBN": "978-84-376-0495-4", "Copias": 3, "Ubicación": "Estantería A3", "categoria": "Novela", "reservado": 2},
    {"Titulo": "Crónica de una muerte anunciada", "Autor": "Gabriel García Márquez", "Año": 1981, "ISBN": "978-84-376-0497-8", "Copias": 3, "Ubicación": "Estantería A3", "categoria": "Novela", "reservado": 1},
    {"Titulo": "La Galatea", "Autor": "Miguel de Cervantes", "Año": 1585, "ISBN": "120-76-659-3450-3", "Copias Disponibles": 9, "Ubicación": "Estantería B1", "categoria": "Novela", "reservado": 3},
    {"Titulo": "Maria", "Autor": "Jorge Isaacs", "Año": 1867, "ISBN": "978-84-376-0500-5", "Copias": 7, "Ubicación": "Estantería A4", "categoria": "Romance", "reservado": 1},
    {"Titulo": "Río Moro", "Autor": "Jorge Isaacs", "Año": 1867, "ISBN": "978-84-376-0501-2", "Copias": 5, "Ubicación": "Estantería A4", "categoria": "Romance", "reservado": 0},
    {"Titulo": "A Silvia", "Autor": "Jorge Isaacs", "Año": 1855, "ISBN": "978-88-04-589-15-4", "Copias": 7, "Ubicación": "Estantería D5", "categoria": "Poesía", "reservado": 1},
    {"Titulo": "Los Trabajos de Persiles y Sigismunda", "Autor": "Miguel de Cervantes", "Año": 1617, "ISBN": "120-76-659-3450-4", "Copias": 4, "Ubicación": "Estantería B2", "categoria": "Novela", "reservado": 2},
    {"Titulo": "Dragon ball", "Autor": "Akira Toriyama", "Año": 1984, "ISBN": "978-4-08-851-831-6", "Copias": 12, "Ubicación": "Estantería E1", "categoria": "Comic", "reservado": 2},
    {"Titulo": "Naruto", "Autor": "Masashi Kishimoto", "Año": 1999, "ISBN": "978-4-08-851-831-7", "Copias": 12, "Ubicación": "Estantería E2", "categoria": "Comic", "reservado": 7},
    {"Titulo": "Bleach", "Autor": "Tite Kubo", "Año": 2001, "ISBN": "978-4-08-851-831-8", "Copias": 12, "Ubicación": "Estantería E3", "categoria": "Comic", "reservado": 3},
    {"Titulo": "Death note", "Autor": "Tsugumi Ohba", "Año": 2003, "ISBN": "978-4-08-851-831-9", "Copias": 12, "Ubicación": "Estantería E4", "categoria": "Comic", "reservado": 0},
]

datos = [
    {"ID": "001", "Nombre": "Kamilo Hernadez Perdomo", "Tipo de Usuario": "Estudiante", "Fecha de Inscripcion": "15/03/2023"},
    {"ID": "002", "Nombre": "Esteban Zuluaga Lara", "Tipo de Usuario": "Profesor", "Fecha de Inscripcion": "11/09/2001"},
    {"ID": "003", "Nombre": "Jose Angel Hernandez Montes", "Tipo de Usuario": "Externo", "Fecha de Inscripcion": "05/11/2025"},
    {"ID": "004", "Nombre": "Jesus David Hernadez Contreras", "Tipo de Usuario": "Estudiante", "Fecha de Inscripcion": "30/01/2024"},
    {"ID": "005", "Nombre": "Sergio Ruz Mercado", "Tipo de Usuario": "Profesor", "Fecha de Inscripcion": "12/09/2025"},
    {"ID": "006", "Nombre": "Einer David Paternina Mendez", "Tipo de Usuario": "Externo", "Fecha de Inscripcion": "22/07/2023"},
]

RESEÑAS = {
    # 1. Cien Años de Soledad (Novela)
    "978-84-376-0494-7": [
        "★★★★★ - Un libro que me cambió la vida",
        "★★★★★ - Es la mejor novela que he leído jamás.",
    ],
    "Cien Años de Soledad": [
        "★★★★★ - Un libro que me cambió la vida",
        "★★★★★ - Es la mejor novela que he leído jamás.",
    ],

    # 2. Don Quijote de la Mancha (Novela)
    "120-76-659-3450-2": [
        "★★★★☆ - Un libro que hay que leer más de una vez",
    ],
    "Don Quijote de la Mancha": [
        "★★★★☆ - Un libro que hay que leer más de una vez",
    ],

    # 3. El principito (Novela)
    "978-4-08-851-831-5": [
        "★★★★★ - Hermosa historia, una lección para adultos.",
        "★★★★☆ - Perfecto para releer en cualquier momento.",
    ],
    "El principito": [
        "★★★★★ - Hermosa historia, una lección para adultos.",
        "★★★★☆ - Perfecto para releer en cualquier momento.",
    ],

    # 4. La divina comedia (Poesía)
    "978-88-04-589-12-3": [
        "★★★★☆ - Clásico épico, lectura densa pero gratificante.",
        "★★★☆☆ - No es para todos.",
    ],
    "La divina comedia": [
        "★★★★☆ - Clásico épico, lectura densa pero gratificante.",
        "★★☆☆☆ - No es para todos.",
    ],

    # 5. Infierno (Poesía) - Título y ISBN
    "978-88-04-589-12-3": [
        "★★★★★ - El más impactante de la trilogía.",
    ],
    "Infierno": [
        "★★★★☆ - El más impactante de la trilogía.",
    ],

    # 6. Purgatorio (Poesía) - Título y ISBN
    "978-88-04-589-12-3": [
        "★★★★☆ - Una transición reflexiva e interesante.",
    ],
    "Purgatorio": [
        "★★★★☆ - Una transición reflexiva e interesante.",
    ],

    # 7. Paraíso (Poesía) - Título y ISBN
    "978-88-04-589-12-3": [
        "★☆☆☆☆ - meh."
    ],
    "Paraíso": [
        "★☆☆☆☆ - meh."
    ],

    # 8. El otoño del patriarca (Novela)
    "978-84-376-0495-4": [
        "★★★★☆ - El estilo narrativo es único y complejo.",
        "☆☆☆☆☆ - No me gusto.",
    ],
    "El otoño del patriarca": [
        "★★★★☆ - El estilo narrativo es único y complejo.",
        "☆☆☆☆☆ - No me gusto.",
    ],

    # 9. Crónica de una muerte anunciada (Novela)
    "978-84-376-0497-8": [
        "★★★★★ - Una obra maestra de suspenso y fatalidad.",
    ],
    "Crónica de una muerte anunciada": [
        "★★★★★ - Una obra maestra de suspenso y fatalidad.",
    ],

    # 10. La Galatea (Novela)
    "120-76-659-3450-3": [
        "★★★☆☆ - Un Cervantes pastoril, muy diferente al Quijote.",
        "★★★★☆ - Excelente ejemplo de novela de su época.",
    ],
    "La Galatea": [
        "★★★☆☆ - Un Cervantes pastoril, muy diferente al Quijote.",
        "★★★★☆ - Excelente ejemplo de novela de su época.",
    ],
    
    # 11. Maria (Romance)
    "978-84-376-0500-5": [
        "★★★★★ - El romance más bello de la literatura colombiana.",
        "★★★★☆ - Muy emotiva, aunque un poco trágica.",
    ],
    "Maria": [
        "★★★★★ - El romance más bello de la literatura colombiana.",
        "★★★★☆ - Muy emotiva, aunque un poco trágica.",
    ],
    
    # 12. Río Moro (Romance)
    "978-84-376-0501-2": [
        "★★★☆☆ - Interesante continuación de la obra de Isaacs."
    ],
    "Río Moro": [
        "★★★☆☆ - Interesante continuación de la obra de Isaacs."
    ],
    
    # 13. A Silvia (Poesía)
    "978-88-04-589-15-4": [
        "★★★★☆ - Poesía clásica, llena de sentimiento.",
    ],
    "A Silvia": [
        "★★★★☆ - Poesía clásica, llena de sentimiento.",
    ],
    
    # 14. Los Trabajos de Persiles y Sigismunda (Novela)
    "120-76-659-3450-4": [
        "★★★☆☆ - Una novela bizantina con muchas aventuras.",
    ],
    "Los Trabajos de Persiles y Sigismunda": [
        "★★★☆☆ - Una novela bizantina con muchas aventuras.",
    ],
    
    # 15. Dragon ball (Comic)
    "978-4-08-851-831-6": [
        "★★★★★ - La base de toda la acción y aventura.",
        "★★★★☆ - Un clásico que nunca pasa de moda."
    ],
    "Dragon ball": [
        "★★★★★ - La base de toda la acción y aventura.",
        "★★★★☆ - Un clásico que nunca pasa de moda."
    ],

    # 16. Naruto (Comic)
    "978-4-08-851-831-7": [
        "★★★★★ - Una historia de perseverancia. Muy inspiradora.",
        "★★★★☆ - Excelentes personajes y desarrollo de trama."
    ],
    "Naruto": [
        "★★★★★ - Una historia de perseverancia. Muy inspiradora.",
        "★★★★☆ - Excelentes personajes y desarrollo de trama."
    ],

    # 17. Bleach (Comic)
    "978-4-08-851-831-8": [
        "★★★★☆ - Diseño de personajes impresionante.",
        "★★★☆☆ - Buena acción, aunque la trama se alarga.",
    ],
    "Bleach": [
        "★★★★☆ - Diseño de personajes impresionante.",
        "★★★☆☆ - Buena acción, aunque la trama se alarga.",
    ],

    # 18. Death note (Comic)
    "978-4-08-851-831-9": [
        "★★★★★ - Trama psicológica brillante. Lectura obligatoria.",
        "★★★★★ - Un duelo de intelectos fascinante."
    ],
    "Death note": [
        "★★★★★ - Trama psicológica brillante. Lectura obligatoria.",
        "★★★★★ - Un duelo de intelectos fascinante."
    ],
}  
#poner reseñas en Titulo y ISBN
for libro in libros:
    titulo_libro = libro['Titulo'].lower() if 'Titulo' in libro else ''
    isbn_libro = libro['ISBN'] if 'ISBN' in libro else None
    for clave, lista_reseñas in RESEÑAS.items():
        clave_lower = None
        try:
            clave_lower = clave.lower()
        except Exception:
            clave_lower = None
        if clave == isbn_libro or (clave_lower and clave_lower == titulo_libro):
            if 'Reseñas' not in libro:
                libro['Reseñas'] = []
            for r in lista_reseñas:
                if r not in libro['Reseñas']:
                    libro['Reseñas'].append(r)

fecha_actual_global = FECHA_ACTUAL()
TARIFA_MULTA_DIARIA = 2000  # Tarifa en pesos por día de retraso

while True:
    menu()
    opcion = input("\nSeleccione una opcion: ")

#REGITRAR NUEVO USUARIO
    if opcion == "1":
        highest = 0
        for u in datos:
            try:
                n = int(u["ID"])
            except (KeyError, ValueError, TypeError):
                continue
            if n > highest:
                highest = n
        nuevo_id = f"{highest + 1:03d}"
        print("\n=== REGISTRO DE NUEVO USUARIO ===")
        print("Por favor, ingrese la siguiente información:")
        nombre = input("Ingrese su nombre completo: ")
        tipo_de_usuario_map = {"1": "Estudiante", "2": "Profesor", "3": "Externo"}
        print("\nSeleccione el tipo de usuario:")
        print("1) Estudiante")
        print("2) Profesor")
        print("3) Externo")
        while True:
            num_usuario = input("Ingrese el número correspondiente (1-3): ")
            if num_usuario in tipo_de_usuario_map:
                tipo_de_usuario = tipo_de_usuario_map[num_usuario]
                break
            else:
                print("!!Opción no válida!!")
                print("Intente de nuevo.")
        
        datos.append({
            "ID": nuevo_id,
            "Nombre": nombre,
            "Tipo de Usuario": tipo_de_usuario,
            "Fecha de Inscripcion": fecha_actual_global,
        })
        print("-" * 44)
        print(f"\nUsuario registrado exitosamente con ID: {nuevo_id}")
        print(f"Fecha actual de inscripcion: {fecha_actual_global}\n")
        print("-" * 44)

# MODIFICACION DE FECHA 
    elif opcion == "2":
        FECHA_ACTUAL() # Esto actualiza fecha_actual_global [cite: 242]
        print(f"La fecha ha sido actualizada correctamente")
        
        # >>> CAMBIO CLAVE A AÑADIR AQUÍ:
        actualizar_multas_globales()

# Mostrar usuarios registrados
    elif opcion == "3":
        print("\n=== USUARIOS REGISTRADOS ===\n")
        if not datos:
            print("No hay usuarios registrados aún.")
        else:
            print(f"{'ID':<9} | {'Nombre':<35} | {'Tipo de Usuario':<15} | {'Fecha de Inscripcion':<}")
            print("-" * 88)
            for USUARIOS in datos:
                print(f"ID: {USUARIOS['ID']:<5} | {USUARIOS['Nombre']:<35} | {USUARIOS['Tipo de Usuario']:<15} | {USUARIOS['Fecha de Inscripcion']:<12}")
        print("-" * 88)
        print(" \n")

# Buscar libros
    elif opcion == "4":
        print("=" * 35)
        print("\n¿Cómo desea buscar?")
        print("1) Título")
        print("2) Autor")
        print("3) ISBN")
        print("4) Categoría")
        print("5) Regresar al menu principal")
        print("0) filtrar por disponibilidad")
        print("=" * 35)
        
        opcion = input("Elija una opción: ")
        if opcion == "1":
            titulo = input("Ingrese el título del libro: ")
            titulo_sin_tildes = remover_tildes(titulo.lower())
            encontrados = [libro for libro in libros if remover_tildes(libro['Titulo'].lower()) == titulo_sin_tildes]
            if encontrados:
                for libro in encontrados:
                    print(f"\nTítulo: {libro['Titulo']} | ISBN: {libro['ISBN']} | Autor: {libro['Autor']} | Ubicación: {libro['Ubicación']} | Categoria: {libro['categoria']}")
            else:
                print("No se encontraron libros con ese título.")
        elif opcion == "2":
            autor = input("Ingrese el autor del libro: ")
            autor_sin_tildes = remover_tildes(autor.lower())
            encontrados = [libro for libro in libros if remover_tildes(libro['Autor'].lower()) == autor_sin_tildes]  
            if encontrados:
                for libro in encontrados:
                    print(f"\nTítulo: {libro['Titulo']} | ISBN: {libro['ISBN']} | Autor: {libro['Autor']} | Ubicación: {libro['Ubicación']} | Categoria: {libro['categoria']}")
            else:
                print("No se encontraron libros de ese autor.")
        elif opcion == "3":
            isbn = input("Ingrese el ISBN del libro: ")
            encontrados = [libro for libro in libros if libro['ISBN'] == isbn]
            if encontrados:
                for libro in encontrados:
                    print(f"\nTítulo: {libro['Titulo']} | ISBN: {libro['ISBN']} | Ubicación: {libro['Ubicación']} | Categoria: {libro['categoria']}")
            else:
                print("No se encontró libro con ese ISBN.")
        elif opcion == "4":
            categorias = []
            for libro in libros:
                if libro['categoria'] not in categorias:
                    categorias.append(libro['categoria'])
            print("\nCategorías disponibles:")
            for idx, cat in enumerate(categorias, 1):
                print(f"{idx}. {cat}")
            categoria = input("Ingrese la categoría del libro: ")
            categoria_sin_tildes = remover_tildes(categoria.lower())
            encontrados = [libro for libro in libros if remover_tildes(libro['categoria'].lower()) == categoria_sin_tildes]
            if encontrados:
                for libro in encontrados:
                    print(f"\nTítulo: {libro['Titulo']:<20} | Categoría: {libro['categoria']:<9} | Ubicación: {libro['Ubicación']}")
        elif opcion == "5":
            menu()
        elif opcion == "0":
            filtrar_por_disponibilidad(libros)
            continue
        else:
            print("Opción no válida. Regresando al menú principal.")
            continue

# Añadir libro
    elif opcion == "5":
        titulo = input("Ingrese el título del libro: ")
        autor = input("Ingrese el autor del libro: ")
        año = input("Ingrese el año de publicación del libro: ")
        isbn = input("Ingrese el ISBN del libro: ")
        stock = input("Ingrese el número de copias disponibles: ")
        ubicacion = input("Ingrese la ubicación del libro en la biblioteca: ")
        categoria = input("Ingrese la categoria del libro: ")
        nuevo_libro = {
            "Titulo": titulo,
            "Autor": autor,
            "Año": año,
            "ISBN": isbn,
            "Copias Disponibles": stock,
            "Ubicación": ubicacion,
            "categoria": categoria,
        }
        libros.append(nuevo_libro)
        print(f"Libro '{titulo}' agregado a la biblioteca.")

#AÑADIR RESEÑA A LOS LIBROS
    elif opcion == "6":
        def añadir_reseña():
            titulo_reseña = input("Ingrese el título o ISBN del libro para añadir una reseña: ")
            encontrado = None
            for libro in libros:
                if libro['Titulo'].lower() == titulo_reseña.lower() or libro['ISBN'] == titulo_reseña:
                    encontrado = libro
                    break
            if encontrado:
                try:
                    estrellas = int(input("Ingrese la calificación (1-5 estrellas): "))
                    if estrellas < 1 or estrellas > 5:
                        print("Calificación inválida. Debe ser un número entre 1 y 5.")
                        return
                    comentario = input("Ingrese su reseña: ")
                    reseña = f"{'★' * estrellas}{'☆' * (5 - estrellas)} - {comentario}"
                    if 'Reseñas' not in encontrado:
                        encontrado['Reseñas'] = []
                    encontrado['Reseñas'].append(reseña)
                    print(f"Reseña añadida para '{encontrado['Titulo']}'.")
                except ValueError:
                    print("Calificación inválida. Debe ser un número entre 1 y 5.")
            else:
                print("No se encontró el libro especificado.")

        añadir_reseña()

# VER RESEÑAS DE LOS LIBROS
    elif opcion == "7":
        print("\n=== VER RESEÑAS DE LIBROS ===")
        ver_reseñas()

# APARTAR LIBRO
    elif opcion == "8":
        id_usuario = input("Ingrese su ID de usuario (dejar vacío si no es usuario registrado): ")
        if id_usuario.strip() == "":
            APARTAR_LIBRO(None, prestamos)
        else:
            APARTAR_LIBRO(id_usuario, prestamos)

# VER PRIVILEGIOS DE USUARIO
    elif opcion == "9":
        id_usuario = input("Ingrese el ID del usuario: ")
        ver_privilegios_usuario(id_usuario)

# DEVOLVER LIBRO
    elif opcion == """DESAVILITADA TEMPORALMENTE""":
        id_usuario = input("Ingrese su ID de usuario: ")
        IsbnNombre = input("Ingrese el ISBN o título del libro que desea devolver: ")
        DEVOLVER_LIBRO(id_usuario, IsbnNombre, prestamos)

    #VER HISTORIAL DE PRESTAMOS
    elif opcion == "10":
        id_usuario = input("Ingrese el ID del usuario para ver su historial de préstamos: ")
        ver_historial_prestamos(id_usuario)
    # VER PRESTAMOS ACTUALES
    elif opcion == "11":
        id_usuario = input("Ingrese el ID del usuario para ver sus multas pendientes: ")
        ver_multas_pendientes(id_usuario)

    # PAGAR MULTAS PENDIENTES
    elif opcion == "12":
        id_usuario = input("Ingrese el ID del usuario para pagar sus multas pendientes: ")
        multa_total, detalles_multa = calcular_multa_total_usuario(id_usuario)
        if multa_total == 0:
            print("\nNo hay multas pendientes para este usuario.")
        else:
            print(f"\nMulta total pendiente para el usuario {id_usuario}: ${multa_total:,}")
            confirmar = input("¿Desea pagar esta multa ahora? (s/n): ")
            if confirmar.lower() == 's':
                PAGAR_MULTAS(id_usuario)
                print("Multas pagadas exitosamente.")
                
                # --- ESTA ES LA LÍNEA CLAVE AÑADIDA ---
                actualizar_multas_globales()
                print("El estado de bloqueo del usuario ha sido actualizado.")
                # ----------------------------------------
                
            else:
                print("Pago de multas cancelado.")

    # RECOMENDACIONES
    elif opcion == "13":
        id_usuario = input("Ingrese el ID del usuario para obtener recomendaciones: ")
        # Categorías más leídas
        cats = categorias_mas_leidas(id_usuario, top_n=3)
        if cats:
            print(f"\nCategorías más leídas por {id_usuario}:")
            for cat, cnt in cats:
                print(f"- {cat}: {cnt} libro(s)")
        else:
            print("\nNo hay historial de lecturas para ese usuario.")

        # Usuarios similares
        sims = usuarios_similares(id_usuario, top_k=5)
        if sims:
            print(f"\nUsuarios con gustos similares a {id_usuario}:")
            for uid in sims:
                print(f"- {uid}")
        else:
            print("\nNo se encontraron usuarios similares o no hay suficiente historial.")

        # Recomendaciones combinadas
        recs = recomendar(id_usuario, top_n=10)
        if recs:
            print("-" * 36)
            print(f"\nRecomendaciones para {id_usuario}:")
            print(f"| {'Título':<32} | {'ISBN':<18} | {'Autor':<35} | {'Categoría':<10} | {'Calificación Promedio':<}")
            print("-" * 130)
            for r in recs:
                avg = promedio_calificacion_por_isbn(r.get('ISBN'))
                print(f"| {r.get('Titulo'):<32} | {r.get('ISBN'):<18} | {r.get('Autor'):<35} | {r.get('categoria'):<10} | {avg:.2f}")
        else:
            print("\nNo hay recomendaciones disponibles en este momento.")
    # DEVOLVER LIBRO
    elif opcion == "14": 
        DEVOLVER_LIBRO()
    # RENOVAR PRÉSTAMO
    elif opcion == "15":
        id_usuario = input("Ingrese su ID de usuario: ")
        RENOVAR_PRESTAMO(id_usuario)
# REPORTES
    elif opcion == "16":
        MENU_REPORTES()
# SALIR
    if opcion == "0":
        print("\nGracias por visitar la biblioteca virtual del plutalco, vuelva pronto")
        break