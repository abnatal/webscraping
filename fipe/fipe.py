import requests
"""
FIPE (Fundação Instituto de Pesquisas Econômicas - https://www.fipe.org.br) is a non-profit brazilian organization. One of its goals is to research economic and financial indicators.
This scripts get informations about new/used vehicles prices in brazilian market.
"""
class Fipe:
    def __init__(self):
        self.headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
                         'X-Requested-With': 'XMLHttpRequest' }

    def get_tables(self):
        """
        Get month-based pricing table codes.
        """
        res = requests.Session().post('https://veiculos.fipe.org.br/api/veiculos/ConsultarTabelaDeReferencia', headers = self.headers)
        return res.json()

    def get_brands(self, table_id, vehicle_type):
        """
        All vehicle brands.
        """
        body = {'codigoTabelaReferencia' : table_id, 'codigoTipoVeiculo': vehicle_type }
        res = requests.Session().post('https://veiculos.fipe.org.br/api/veiculos/ConsultarMarcas', data = body, headers = self.headers)
        return res.json()

    def get_models(self, table_id, vehicle_type, brand_id):
        """
        All vehicle models by brand.
        """
        body = {'codigoTabelaReferencia' : table_id, 'codigoTipoVeiculo': vehicle_type, 'codigoMarca' : brand_id }
        res = requests.Session().post('https://veiculos.fipe.org.br/api/veiculos/ConsultarModelos', data = body, headers = self.headers)
        return res.json()

    def get_model_years(self, table_id, vehicle_type, brand_id, model_id):
        """
        Return a dict with models/year pairs.
        """
        body = {'codigoTabelaReferencia' : table_id, 'codigoTipoVeiculo': vehicle_type, 'codigoMarca' : brand_id, 'codigoModelo' : model_id }
        res = requests.Session().post('https://veiculos.fipe.org.br/api/veiculos/ConsultarAnoModelo', data = body, headers = self.headers)
        return res.json()

    def get_model_price(self, table_id, vehicle_type, brand_id, model_id, model_year=32000):
        """
        Get the model price and some other attributes.
        """
        body = {'codigoTabelaReferencia' : table_id, 'codigoTipoVeiculo': vehicle_type, 'codigoMarca' : brand_id, 'codigoModelo' : model_id, 'anoModelo' : model_year, 'tipoConsulta' : 'tradicional', 'codigoTipoCombustivel': 1 }
        res = requests.Session().post('https://veiculos.fipe.org.br/api/veiculos/ConsultarValorComTodosParametros', data = body, headers = self.headers)
        return res.json()

if __name__ == '__main__':

    f = Fipe()
    table_id = f.get_tables()[0]['Codigo']

    # Get information about a 2017 Hiunday (id=26) Creta Prestige (id=7830).
    print(f.get_model_price(table_id=table_id, vehicle_type=1, brand_id=26, model_id=7830, model_year=2017))

    #print(f.get_tables())
    #print(f.get_brands(table_id=table_id, vehicle_type=1) )
    #print(f.get_models(table_id=table_id, vehicle_type=1, brand_id=26))
    #print(f.get_model_years(table_id=table_id, vehicle_type=1, brand_id=26, model_id=7830))
    #print(f.get_model_price(table_id=table_id, vehicle_type=1, brand_id=26, model_id=7830, model_year=2017))
