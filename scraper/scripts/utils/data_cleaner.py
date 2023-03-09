import re

class DataCleaner:

    @staticmethod
    def clean_data(data):
        
        # Remove all the new line characters
        data = data.replace('\n', '')

        # Remove all the white spaces at the beginning and at the end of the data
        data = data.strip()

        # Remove all special characters
        data = data.replace('é', 'e')
        data = data.replace('è', 'e')
        data = data.replace('ê', 'e')
        data = data.replace('à', 'a')
        data = data.replace('â', 'a')
        data = data.replace('ô', 'o')
        data = data.replace('î', 'i')
        data = data.replace('ï', 'i')
        data = data.replace('ç', 'c')
        data = data.replace('ù', 'u')
        data = data.replace('û', 'u')
        data = data.replace('ä', 'a')
        data = data.replace('\n', '')

        return data