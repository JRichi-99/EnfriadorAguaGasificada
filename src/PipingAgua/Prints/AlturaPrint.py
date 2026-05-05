def imprimir_reporte_hidraulico(total_h, friccion, alturas, fittings, datos):
    """
    Imprime un reporte en consola de los cálculos hidráulicos.
    Adaptado para recibir la fricción y los fittings por separado.
    """
    # Encabezado principal
    print("\n" + "="*85)
    print(" REPORTE DE CAÍDA DE PRESIÓN DEL SISTEMA ".center(85, "="))
    print("="*85)
    
    # Encabezado de la tabla
    header = f"| {'Tramo':^5} | {'Dir':^3} | {'L (m)':^7} | {'D (mm)':^7} | {'Vel(m/s)':^8} | {'Reynolds':^9} | {'f / K':^7} | {'h_perd(m)':^9} | {'h_elev(m)':^9} |"
    print(header)
    print("-" * len(header))
    
    # Filas de la tabla
    for i, tramo in enumerate(datos):
        t_dir = tramo['dir'].upper()
        l = tramo['l']
        d_mm = tramo['d'] * 1000  # Convertir a mm para visualización
        v = tramo['velo']
        re = tramo['Re']
        f = tramo['F']
        
        # Tomamos los valores directamente de los arrays
        h_friccion = friccion[i] 
        h_elev = alturas[i]
        
        # 1. Fila de la TUBERÍA (fricción)
        row_tuberia = f"| {i+1:^5} | {t_dir:^3} | {l:>7.2f} | {d_mm:>7.1f} | {v:>8.3f} | {re:>9.0f} | {f:>7.4f} | {h_friccion:>9.3f} | {h_elev:>9.2f} |"
        print(row_tuberia)
        
        # 2. Fila del FITTING (solo si Ks > 0)
        if tramo['ks'] > 0:
            ks_val = tramo['ks']
            h_fitting = fittings[i]
            
            str_k = f"K={ks_val:.1f}"
            row_fit = f"| {'|_':^5} | {'FIT':^3} | {'-':>7} | {'-':>7} | {'-':>8} | {'-':>9} | {str_k:>7} | {h_fitting:>9.3f} | {'-':>9} |"
            print(row_fit)
        
    print("-" * len(header))
    
    # Resumen final
    print("\n" + " RESUMEN GLOBAL ".center(45, "-"))
    
    # Usamos sum() directamente sobre los arrays que pasaste
    print(f"Pérdidas por fricción (tubos) : {sum(friccion):.3f} m")
    print(f"Pérdidas por accesorios (FIT) : {sum(fittings):.3f} m")
    print(f"Diferencia de altura (Ly)     : {sum(alturas):.3f} m")
    
    # Diferencia de energía cinética
    v_in = datos[0]['velo']
    v_out = datos[-1]['velo']
    delta_k = (v_out**2 / (2 * 9.81)) - (v_in**2 / (2 * 9.81))
    
    print(f"Dif. carga velocidad (V_out)  : {delta_k:.3f} m")
    print("-" * 45)
    print(f"CARGA TOTAL DEL SISTEMA (H)   : {total_h:.3f} m\n")