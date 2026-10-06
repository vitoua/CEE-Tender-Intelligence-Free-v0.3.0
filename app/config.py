from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
 secret_key:str='change-me';admin_email:str='admin@example.com';admin_password:str='ChangeMe123!';app_language:str='uk';cache_limit:int=800
 model_config=SettingsConfigDict(env_file='.env',extra='ignore')
settings=Settings()
