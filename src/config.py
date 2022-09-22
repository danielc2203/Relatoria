# Clase de llave privada
class Config:
    SECRET_KEY = 'B!1HGtyu34567(ghjk?)K+lk'
    

# Clase para iniciar el servidor en modo DEBU
class DevelopmentConfig(Config):
    DEBUG = True 
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'relatoria'
    MYSQL_PASSWORD = 'relatoria'
    MYSQL_DB = 'relatoria'
    
    
config = {
    'development': DevelopmentConfig
}