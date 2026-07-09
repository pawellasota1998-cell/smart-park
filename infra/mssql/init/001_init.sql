:setvar DatabaseName "euro_park"
:setvar AppLogin "euro_park_app"


IF DB_ID(N'$(DatabaseName)') IS NULL
BEGIN
    PRINT N'Creating database [$(DatabaseName)]...';

    CREATE DATABASE [$(DatabaseName)];
END;
GO


IF NOT EXISTS (
    SELECT 1
    FROM sys.server_principals
    WHERE [name] = N'$(AppLogin)'
)
BEGIN
    PRINT N'Creating login [$(AppLogin)]...';

    CREATE LOGIN [$(AppLogin)]
        WITH PASSWORD = '$(APP_DB_PASSWORD)',
             CHECK_POLICY = ON;
END
ELSE
BEGIN
    PRINT N'Updating login password [$(AppLogin)]...';

    ALTER LOGIN [$(AppLogin)]
        WITH PASSWORD = '$(APP_DB_PASSWORD)';
END;
GO


USE [$(DatabaseName)];
GO


IF NOT EXISTS (
    SELECT 1
    FROM sys.database_principals
    WHERE [name] = N'$(AppLogin)'
)
BEGIN
    PRINT N'Creating database user [$(AppLogin)]...';

    CREATE USER [$(AppLogin)]
        FOR LOGIN [$(AppLogin)];
END;
GO


IF NOT EXISTS (
    SELECT 1
    FROM sys.database_role_members AS drm
    INNER JOIN sys.database_principals AS role_principal
        ON role_principal.principal_id = drm.role_principal_id
    INNER JOIN sys.database_principals AS member_principal
        ON member_principal.principal_id = drm.member_principal_id
    WHERE role_principal.[name] = N'db_datareader'
      AND member_principal.[name] = N'$(AppLogin)'
)
BEGIN
    ALTER ROLE [db_datareader]
        ADD MEMBER [$(AppLogin)];
END;
GO


IF NOT EXISTS (
    SELECT 1
    FROM sys.database_role_members AS drm
    INNER JOIN sys.database_principals AS role_principal
        ON role_principal.principal_id = drm.role_principal_id
    INNER JOIN sys.database_principals AS member_principal
        ON member_principal.principal_id = drm.member_principal_id
    WHERE role_principal.[name] = N'db_datawriter'
      AND member_principal.[name] = N'$(AppLogin)'
)
BEGIN
    ALTER ROLE [db_datawriter]
        ADD MEMBER [$(AppLogin)];
END;
GO


IF NOT EXISTS (
    SELECT 1
    FROM sys.database_role_members AS drm
    INNER JOIN sys.database_principals AS role_principal
        ON role_principal.principal_id = drm.role_principal_id
    INNER JOIN sys.database_principals AS member_principal
        ON member_principal.principal_id = drm.member_principal_id
    WHERE role_principal.[name] = N'db_ddladmin'
      AND member_principal.[name] = N'$(AppLogin)'
)
BEGIN
    ALTER ROLE [db_ddladmin]
        ADD MEMBER [$(AppLogin)];
END;
GO


PRINT N'SQL Server initialization completed successfully.';
GO