query_creacion_edades = '''
CREATE TABLE IF NOT EXISTS edades (
    id_grupo_edad INT PRIMARY KEY,
    grupo_edad VARCHAR
);
'''

query_insercion_edades = '''
    insert into edades (id_grupo_edad, grupo_edad)
    values
    (%s, %s)''' 


query_creacion_ramas = '''
CREATE TABLE IF NOT EXISTS ramas (
    id_rama INT PRIMARY KEY,
    nombre VARCHAR
);
'''

query_insercion_ramas = '''
    insert into ramas (id_rama, nombre)
    values
    (%s, %s)''' 


query_creacion_comunidades = '''
CREATE TABLE IF NOT EXISTS ccaa (
    id_ccaa INT PRIMARY KEY,
    nombre_ccaa VARCHAR
);
'''

query_insercion_comunidades = '''
    insert into ccaa (id_ccaa, nombre_ccaa)
    values
    (%s, %s)''' 


query_creacion_provincias = '''
CREATE TABLE IF NOT EXISTS provincias (
    id_provincia INT PRIMARY KEY,
    nombre_provincia VARCHAR,
    id_ccaa INT REFERENCES ccaa(id_ccaa) ON UPDATE CASCADE ON DELETE RESTRICT
);
'''

query_insercion_provincias = '''
    insert into provincias (id_provincia, nombre_provincia, id_ccaa)
    values
    (%s, %s, %s)''' 


query_creacion_pib_total = '''
CREATE TABLE IF NOT EXISTS pib_total (
    id_pib_total SERIAL PRIMARY KEY,
    id_provincia INT REFERENCES provincias(id_provincia) ON UPDATE CASCADE ON DELETE RESTRICT,
    acumulado VARCHAR,
    anio INT,
    total FLOAT
);
'''

query_insercion_pib_total = '''
    insert into pib_total (id_provincia, acumulado, anio, total)
    values
    (%s, %s, %s, %s)''' 


query_creacion_poblacion = '''
CREATE TABLE IF NOT EXISTS poblacion (
    id_poblacion SERIAL PRIMARY KEY,
    id_provincia INT REFERENCES provincias(id_provincia) ON UPDATE CASCADE ON DELETE RESTRICT,
    grupo_edad VARCHAR,
    nacionalidad VARCHAR,
    sexo VARCHAR,
    anio INT,
    total INT
);
'''

query_insercion_poblacion = '''
    insert into poblacion (id_provincia, grupo_edad, nacionalidad, sexo, anio, total)
    values
    (%s, %s, %s, %s, %s, %s)''' 


query_creacion_pib = '''
CREATE TABLE IF NOT EXISTS pib (
    id_pib SERIAL PRIMARY KEY,
    id_provincia INT REFERENCES provincias(id_provincia) ON UPDATE CASCADE ON DELETE RESTRICT,
    rama VARCHAR,
    anio INT,
    total FLOAT
);
'''

query_insercion_pib = '''
    insert into pib (id_provincia, rama, anio, total)
    values
    (%s, %s, %s, %s)''' 


query_creacion_tipo_energia = '''
CREATE TABLE IF NOT EXISTS tipo_energia (
    id_tipo_energia INT PRIMARY KEY,
    nombre VARCHAR
);
'''

query_insercion_tipo_energia = '''
    insert into tipo_energia (id_tipo_energia, nombre)
    values
    (%s, %s)''' 


query_creacion_demanda = '''
CREATE TABLE IF NOT EXISTS demanda (
    id_demanda SERIAL PRIMARY KEY,
    id_ccaa INT REFERENCES ccaa(id_ccaa) ON UPDATE CASCADE ON DELETE RESTRICT,
    anio INT,
    mes INT,
    valor FLOAT
);
'''

query_insercion_demanda = '''
    insert into demanda (anio, mes, id_ccaa, valor)
    values
    (%s, %s, %s, %s)''' 


query_creacion_generacion = '''
CREATE TABLE IF NOT EXISTS generacion (
    id_generacion SERIAL PRIMARY KEY,
    id_tipo_energia INT REFERENCES tipo_energia(id_tipo_energia) ON UPDATE CASCADE ON DELETE RESTRICT,
    id_ccaa INT REFERENCES ccaa(id_ccaa) ON UPDATE CASCADE ON DELETE RESTRICT,
    mes INT,
    anio INT,
    valor FLOAT,
    porcentaje FLOAT
);
'''

query_insercion_generacion = '''
    insert into generacion (id_tipo_energia, id_ccaa, mes, anio, valor, porcentaje)
    values
    (%s, %s, %s, %s, %s, %s)''' 