schema = {
    "lugar_compra": {"type": "string", "minlength": 1},
    "productos": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "categoria": {"type": "string", "minlength": 1},
                "nombre": {"type": "string", "minlength": 1},
                "cantidad": {"type": "integer", "min": 1},
                "unidad": {"type": "string", "minlength": 1},
                "precio_unitario": {"type": "float", "min": 0.01},
                "precio_total_unidad": {"type": "float", "min": 0.01}
            }
        }
    }
}
