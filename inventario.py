import json
from datetime import datetime

registro = []
inventario = []

def cargar_datos():
    global registro, inventario
    try:
        with open("producto_registros.json", "r") as f:
            registro = json.load(f)
    except FileNotFoundError:
        registro = []

    try:
        with open("movimientos.json", "r") as f:
            inventario = json.load(f)
    except FileNotFoundError:
        inventario = []

def json_registro():
    with open("producto_registros.json", "w") as archivo:
        json.dump(registro, archivo, indent=4)

def json_movimientos():
    with open("movimientos.json", "w") as archivo:
        json.dump(inventario, archivo, indent=4)

def buscar_producto_por_codigo(codigo):
    for p in registro:
        if p["codigo"] == codigo:
            return p
    return None


def registrar_productos():
    codigo = input("Código: ")
    nombre = input("Nombre: ")
    proveedor = input("Proveedor: ")

    producto = {
        "codigo": codigo,
        "nombre": nombre,
        "proveedor": proveedor,
        "bodegas": {"Norte": 0, "Centro": 0, "Oriente": 0}
    }

    registro.append(producto)
    json_registro()
    print("Producto registrado con éxito.")

def ingresar_producto():
    codigo = input("Código: ")
    producto = buscar_producto_por_codigo(codigo)

    if not producto:
        print("No existe el producto")
        return

    cantidad = int(input("Cantidad a ingresar: "))
    bodega = input("Bodega (Norte, Centro, Oriente): ")

    if bodega not in producto["bodegas"]:
        print("Bodega inválida")
        return

    producto["bodegas"][bodega] += cantidad

    movimiento = {
        "codigo": codigo,
        "tipo": "Entrada",
        "cantidad": cantidad,
        "bodega": bodega,
        "descripcion": input("Descripción: "),
        "fecha": str(datetime.now())
    }

    inventario.append(movimiento)
    json_registro()
    json_movimientos()
    print("Entrada registrada")

def sacar_producto():
    codigo = input("Código: ")
    producto = buscar_producto_por_codigo(codigo)

    if not producto:
        print("No existe el producto")
        return

    cantidad = int(input("Cantidad a sacar: "))
    bodega = input("Bodega: ")

    if bodega not in producto["bodegas"]:
        print("Bodega inválida")
        return

    if producto["bodegas"][bodega] < cantidad:
        print("Stock insuficiente en esa bodega")
        return

    producto["bodegas"][bodega] -= cantidad

    movimiento = {
        "codigo": codigo,
        "tipo": "Salida",
        "cantidad": cantidad,
        "bodega": bodega,
        "descripcion": input("Descripción: "),
        "fecha": str(datetime.now())
    }

    inventario.append(movimiento)
    json_registro()
    json_movimientos()
    print("Salida registrada")

def transferir_productos():
    codigo = input("Digita el código del producto: ")
    producto = buscar_producto_por_codigo(codigo)

    if not producto:
        print("El producto no existe.")
        return

    bodega_origen = input("Bodega de origen (Norte/Centro/Oriente): ")
    if bodega_origen not in producto["bodegas"]:
        print("Bodega de origen no válida.")
        return

    bodega_destino = input("Bodega de destino (Norte/Centro/Oriente): ")
    if bodega_destino not in producto["bodegas"]:
        print("Bodega de destino no válida.")
        return

    if bodega_origen == bodega_destino:
        print("La bodega de origen y destino son la misma.")
        return

    cantidad_pasar = int(input(f"Cantidad a transferir (Disponible {producto['bodegas'][bodega_origen]}): "))

   
    if producto["bodegas"][bodega_origen] < cantidad_pasar:
        print("Cantidad insuficiente en la bodega de origen.")
        return

    producto["bodegas"][bodega_origen] -= cantidad_pasar
    producto["bodegas"][bodega_destino] += cantidad_pasar

    movimiento = {
        "codigo": codigo,
        "tipo": "Transferencia",
        "cantidad": cantidad_pasar,
        "bodega": f"{bodega_origen} -> {bodega_destino}",
        "descripcion": f"Traslado interno de mercancía",
        "fecha": str(datetime.now())
    }
    
    inventario.append(movimiento)
    

    json_registro()
    json_movimientos()
    print(f"Transferencia de {cantidad_pasar} unidades realizada con éxito.")

def buscar_producto():
    codigo = input("Código: ")
    producto = buscar_producto_por_codigo(codigo)
    if producto:
        print(f"\n--- {producto['nombre']} ---")
        for b, c in producto["bodegas"].items():
            print(f"{b}: {c}")
    else:
        print("No encontrado")

def reporte():
    print("REPORTE GENERAL DE INVENTARIO")
    for p in registro:
        total = sum(p["bodegas"].values())
        print(f"{p['nombre']} [{p['codigo']}] | Total: {total}")
        for b, c in p["bodegas"].items():
            print(f"   - {b}: {c}")

def historial():
    codigo = input("Código: ")

    for m in inventario:
        if m["codigo"] == codigo:
            print(f"{m['fecha']} - {m['tipo']} - {m['cantidad']} - {m['bodega']}")

cargar_datos() 
while True:
    print("\n--- SISTEMA DE INVENTARIO ---")
    print("1. Registrar nuevo producto")
    print("2. Ingresar stock (Entrada)")
    print("3. Sacar stock (Salida)")
    print("4. Buscar producto")
    print("5. Ver historial")
    print("6. Reporte total")
    print("7. Transferir entre bodegas")
    print("8. Salir")

    op = input("Seleccione una opción: ")

    if op == "1": registrar_productos()
    elif op == "2": ingresar_producto()
    elif op == "3": sacar_producto()
    elif op == "4": buscar_producto()
    elif op == "5": historial()
    elif op == "6": reporte()
    elif op == "7": transferir_productos()
    elif op == "8": break