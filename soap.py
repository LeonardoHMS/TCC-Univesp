import requests
import json

# Inadimplência - Total
def get_data_totals(serial_code: str, format_data: str, initial_date: str, end_date: str, file_name: str):
    URL_API_TOTALS = "https://api.bcb.gov.br/dados/serie/bcdata.sgs"
    url_api_totals_finish = f'{URL_API_TOTALS}.{serial_code}/dados?formato={format_data}&dataInicial={initial_date}&dataFinal={end_date}'
    json_data = requests.get(url_api_totals_finish).json()
    print(json_data)

    with open(f'data/{file_name}.json', 'w') as f:
        json.dump(json_data, f, indent=4)

if __name__ == "__main__":
    with open('estados.json', 'r', encoding='utf-8') as f:
        estados = json.load(f)
    for estado in estados['Estados'].values():
        print(estado)
        serial_code = estado
        format_data = 'json'
        initial_date = '01/01/2010'
        end_date = '31/12/2025'
        file_name = f'data_{estado}'
        get_data_totals(serial_code, format_data, initial_date, end_date, file_name)