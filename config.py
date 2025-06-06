ambiente = 'desenvolvimento'

if ambiente == 'desenvolvimento':
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = 'senai'
    DB_NAME = 'ortofix'

elif ambiente == 'producao':
    DB_HOST = ''
    DB_USER = 'GabrielAlves'
    DB_PASSWORD = 'senhaortofix'
    DB_NAME = 'GabrielAlves$ortofix'

# CONFIG CHAVE SECRETA (SESSION)
SECRET_KEY = 'ortofix'

# ACESSO DO ADMIN
MASTER_EMAIL = 'admin@adm'
MASTER_PASSWORD = 'adm'
