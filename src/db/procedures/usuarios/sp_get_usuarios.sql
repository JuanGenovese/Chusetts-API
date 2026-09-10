CREATE OR REPLACE FUNCTION sp_get_usuarios() 
RETURNS table (
    id INT,
    nombre VARCHAR,
    apellido VARCHAR,
    dni VARCHAR,
    rol_id INT,
    activo BOOLEAN
) 
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY 
    SELECT
        u."id",
        u."nombre",
        u."apellido", 
        u."dni", 
        u."rol_id", 
        u."activo"
    FROM public."USUARIOS" u;
END;
$$;
