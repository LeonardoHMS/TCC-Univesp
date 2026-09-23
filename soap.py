import requests
import json

# Inadimplência - Total
def get_data_totals(serial_code: str, format_data: str, initial_date: str, end_date: str, file_name: str):
    URL_API_TOTALS = "https://api.bcb.gov.br/dados/serie/bcdata.sgs"
    url_api_totals_finish = f'{URL_API_TOTALS}.{serial_code}/dados?formato={format_data}&dataInicial={initial_date}&dataFinal={end_date}'
    json_data = requests.get(url_api_totals_finish).json()

    with open(f'{file_name}.json', 'w') as f:
        json.dump(json_data, f, indent=4)

if __name__ == "__main__":
    get_data_totals("21082", "json", "01/01/2023", "01/07/2026", "inadimplencia_credito_total")
    get_data_totals("21084", "json", "01/01/2023", "01/07/2026", "inadimplencia_credito_total_pf")
    get_data_totals("21119", "json", "01/01/2023", "01/07/2026", "inadimplencia_credito_total_livres")
