import json
from datetime import datetime
registro = []
inventario = []
def cargar_datos():
    global registro, inventario
    try:
        with open("producto_registros.json", "r") as f:
            registro = json.load(f)
    except:
        registro = []

    try:
        with open("movimientos.json", "r") as f:
            inventario = json.load(f)
    except:
        inventario = []

def json_registro():
    with open("producto_registros.json", "w") as archivo:
        json.dump(registro, archivo)

def json_movimientos():
    with open("movimientos.json", "w") as archivo:
        json.dump(inventario, archivo)

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
    print("Producto registrado")

def buscar_producto_por_codigo(codigo):
    for p in registro:
        if p["codigo"] == codigo:
            return p
    return None

def ingresar_producto():
    codigo = input("Código: ")
    producto = buscar_producto_por_codigo(codigo)

    if not producto:
        print("No existe el producto")
        return

    cantidad = int(input("Cantidad: "))
    bodega = input("Bodega: Norte,Centro,Oriente ")
    descripcion = input("Descripción: ")

    if bodega not in producto["bodegas"]:
        print("Bodega inválida")
        return

    producto["bodegas"][bodega] += cantidad

    movimiento = {
        "codigo": codigo,
        "tipo": "Entrada",
        "cantidad": cantidad,
        "bodega": bodega,
        "descripcion": descripcion,
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

    cantidad = int(input("Cantidad: "))
    bodega = input("Bodega: ")
    descripcion = input("Descripción: ")

    if bodega not in producto["bodegas"]:
        print("Bodega inválida")
        return

    if producto["bodegas"][bodega] < cantidad:
        print("Stock insuficiente")
        return

    producto["bodegas"][bodega] -= cantidad

    movimiento = {
        "codigo": codigo,
        "tipo": "Salida",
        "cantidad": cantidad,
        "bodega": bodega,
        "descripcion": descripcion,
        "fecha": str(datetime.now())
    }

    inventario.append(movimiento)

    json_registro()
    json_movimientos()

    print("Salida registrada")

def buscar_producto():
    codigo = input("Código: ")
    producto = buscar_producto_por_codigo(codigo)

    if not producto:
        print("No existe")
        return

    print("\nProducto:")
    print(producto["nombre"])
    print("Stock:")
    for b, c in producto["bodegas"].items():
        print(f"{b}: {c}")

def historial():
    codigo = input("Código: ")

    for m in inventario:
        if m["codigo"] == codigo:
            print(f"{m['fecha']} - {m['tipo']} - {m['cantidad']} - {m['bodega']}")

def reporte():
    for p in registro:
        total = sum(p["bodegas"].values())
        print(f"\n{p['nombre']} ({p['codigo']})")
        for b, c in p["bodegas"].items():
            print(f"{b}: {c}")
        print("Total:", total)

cargar_datos()

while True:
    print("\n1. Registrar")
    print("2. Ingresar")
    print("3. Sacar")
    print("4. Buscar")
    print("5. Historial")
    print("6. Reporte")
    print("7. Salir")

    op = input("Opción: ")

    if op == "1": registrar_productos()
    elif op == "2": ingresar_producto()
    elif op == "3": sacar_producto()
    elif op == "4": buscar_producto()
    elif op == "5": historial()
    elif op == "6": reporte()
    elif op == "7": 
        print("Hasta luego")
        break