CREATE TABLE marcas (
    id_marca INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE laptops (
    id_laptop INTEGER PRIMARY KEY,
    modelo TEXT NOT NULL,
    precio REAL NOT NULL,
    ram INTEGER NOT NULL,
    ssd INTEGER NOT NULL,
    procesador TEXT NOT NULL,
    sistema_operativo TEXT NOT NULL,
    id_marca INTEGER NOT NULL,
    FOREIGN KEY (id_marca) REFERENCES marcas(id_marca)
);
