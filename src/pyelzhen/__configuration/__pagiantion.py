from pydantic import BaseSettings


class PaginationBaseSettings(BaseSettings):
    """
        In this class, we set the variables needed for pagination or use the values used in the ".env" file.
    """
    PAGE_SIZE_DEFAULT: int = 25
    PAGE_NUMBER_DEFAULT: int = 1
    FILTERS_DEFAULT: dict = {}
    ORDERINGS_DEFAULT: list = ['-id']

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


pagination_base_settings = PaginationBaseSettings()
