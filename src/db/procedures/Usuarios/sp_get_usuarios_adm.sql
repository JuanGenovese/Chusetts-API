CREATE OR REPLACE FUNCTION sp_get_usuarios_adm() 
RETURNS table (
    id INT,
    nombre VARCHAR,
    apellido VARCHAR,
    dni VARCHAR,
    rol_adm_id INT,
    activo BOOLEAN
) 
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY 
    SELECT
        ua."id",
        ua."nombre",
        ua."apellido", 
        ua."dni", 
        ua."rol_adm_id", 
        ua."activo"
    FROM public."USUARIOS_ADM" ua;
END;
$$;
