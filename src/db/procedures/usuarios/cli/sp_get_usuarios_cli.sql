CREATE OR REPLACE FUNCTION sp_get_usuarios_cli() 
RETURNS table (
    id INT,
    nombre VARCHAR,
    apellido VARCHAR,
    dni VARCHAR,
    email VARCHAR,
    telefono VARCHAR,
    fecha_nac DATE,
    rol_cli_id INT,
    activo BOOLEAN
) 
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY 
    SELECT
        uc."id",
        uc."nombre",
        uc."apellido", 
        uc."dni", 
        uc."email",
        uc."telefono",
        uc."fecha_nac",
        uc."rol_cli_id", 
        uc."activo"
    FROM public."USUARIOS_CLI" uc;
END;
$$;
