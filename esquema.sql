CREATE TABLE marcas (
    id_marca INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE laptops (
    id_laptop INTEGER PRIMARY KEY,
    modelo TEXT NOT NULL,
    precio REAL NOT NULL CHECK (precio > 0),
    ram INTEGER NOT NULL CHECK (ram > 0),
    ssd INTEGER NOT NULL CHECK (ssd > 0),
    procesador TEXT NOT NULL,
    sistema_operativo TEXT NOT NULL,
    id_marca INTEGER NOT NULL,
    FOREIGN KEY (id_marca) REFERENCES marcas(id_marca)
);
