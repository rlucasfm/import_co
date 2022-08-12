import requests
from datetime import date
from Logger import Logger
import re
from dependente import Dependente
from anexo import Anexo

base_url = 'https://api-hapvida.sensedia.com/homologacao/wsvendadireta'

class Orcamento:
    def __init__(self):
        self.cdPlano = ''
        self.nuControle = ''
        self.nuOrcamento = ''
        self.cdFilial = ''
        self.cpfTitularRaw = ''
        self.cdVendedor = ''
        self.cdSenha = ''
        self.cdConcessionaria = ''
        self.dtNascimentoDate = ''
        self.vlMensalidade = ''
        self.vlOdontologia = ''
        
        self.totalizaPlano = {}
                
        self.logger = Logger()
        
    
    def geracaoOrcamento(self, cdVendedor: str, cpfTitularRaw: str):
        try:
            cpfTitular = re.sub("[^0-9]", "", cpfTitularRaw)
            r = requests.post(f'{base_url}/orcamentos?cdVendedor={cdVendedor}&cpfTitular={cpfTitular}', json={})
            res = r.json()
            self.logger.log_gerar_orcamento({
                "cdVendedor": str(cdVendedor),
                "cpfTitular": str(cpfTitular),
                "cdFilial": str(res['cdFilial']),
                "cdSenha": str(res['cdSenha']),
                "dtCriacao": str(res['dtCriacao']),
                "mensagem": str(res['mensagem']),
                "nuControle": str(res['nuControle']),
                "nuOrcamento": str(res['nuOrcamento']),
                "tipo": str(res['tipo']),
            })
        
            self.nuOrcamento = str(res['nuOrcamento'])
            self.nuControle = str(res['nuControle'])
            self.cdFilial = str(res['cdFilial'])
            self.cpfTitularRaw = str(cpfTitularRaw)
            self.cdVendedor = cdVendedor
            self.cdSenha = str(res['cdSenha'])
            
        except Exception as err:
            self.logger.log_error(err)
        
                
        return self
    
    
    def envioTitular(self,  objTitular, anexos):
        try:
            payload = objTitular            
            payload['cdVendedor'] = self.cdVendedor
            payload['nuCpf'] = re.sub("[^0-9]", "", self.cpfTitularRaw)
            payload['nuMatricula'] = self.nuOrcamento
            payload['nuOrcamento'] = self.nuOrcamento
                                    
            r = requests.post(f'{base_url}/beneficiarios/titulares/{self.nuControle}', json=payload)
            res = r.text            
            self.logger.log_enviar_titular(payload, res)
            
            self.cdConcessionaria = objTitular['cdConcessionaria']
            nasc_raw = objTitular['dtNascimento'].split('/')
            self.dtNascimentoDate = date(int(nasc_raw[2]), int(nasc_raw[1]), int(nasc_raw[0]))
            self.cdPlano = objTitular['cdPlano']
            self.vlMensalidade = objTitular['vlMensalidade']
            self.vlOdontologia = str(objTitular['vlOdontologia'])
            
            for anexo in anexos:
                anexo = Anexo(self.logger,
                                base_url,
                                anexo,
                                self.nuControle,
                                True
                                )
                anexo_res = anexo.enviarAnexo()
                
        except Exception as err:
            self.logger.log_error(err)
                            
        return self
    
    
    def envioDependente(self, objDep, nuCpf, anexos, indice):
        dep = Dependente(
                    self.logger,
                    base_url,
                    self.nuControle, 
                    self.nuOrcamento, 
                    self.cdFilial, 
                    re.sub("[^0-9]", "", self.cpfTitularRaw), 
                    self.cdVendedor, 
                    nuCpf)
        
        for anexo in anexos:
            anexo = Anexo(self.logger,
                        base_url,
                        anexo,
                        self.nuControle,
                        False,
                        dep.nuControleDep,
                        indice        
                        )
            anexo_res = anexo.enviarAnexo()
        
        return dep.enviarDependente(objDep)
    
    
    def condicoesSaude(self, objSaude):
        try:
            payload = objSaude
            r = requests.post(f'{base_url}/condicoes/saude', json=payload)
            res = r.json()            
            self.logger.log_condicoes_saude(payload, res['mensagem'])
        except Exception as err:
            self.logger.log_error(err)

    
    def criticasGet(self):
        try:
            r = requests.get(f'{base_url}/criticas/{self.nuControle}')
            res = r.text
            self.logger.log_criticas_get(res)
        except Exception as err:
            self.logger.log_error(err)

    
    def totalizaPlanos(self):
        try:
            payload = {
                "taxaAdesao": "",
                "nuControle": self.nuControle,
                "nuOrcamento": self.nuOrcamento,
                "titular": {
                    "dsSenhaSMS": self.cdSenha,
                    "dtNascimento": self.dtNascimentoDate.strftime("%Y-%m-%d"),
                    "flStatusProcessamento": "11",
                    "nuControle": self.nuControle,
                    "nuMatricula": self.nuOrcamento,
                    "cdPlano": self.cdPlano,
                    "vlMensalidade": self.vlMensalidade,
                    "vlOdontologia": self.vlOdontologia
                }
            }
            
            r = requests.post(f'{base_url}/planos/totalizaPlano/{self.cdConcessionaria}/{self.cdFilial}', json=payload)
            res = r.json()
            self.totalizaPlano = res
            self.logger.log_totalizaPlano(payload, 'Enviado com sucesso')
        except Exception as err:
            self.logger.log_error(err)
    
    
    def finalizaProposta(self):
        try:
            payload = {
                "codigoDesconto": self.totalizaPlano['codigoDesconto'],
                "nuControle": self.nuControle,
                "porcentagemDesconto": self.totalizaPlano['percentagemDesconto'],
                "valorLiquido": self.totalizaPlano['valorLiquidoComDesconto'],
                "vlMensalidade": self.vlMensalidade,
                "vlOdontologia": self.vlOdontologia
            }
            
            r = requests.put(f'{base_url}/orcamentos/finalizaProposta', json=payload)
            res = r.json()            
            self.logger.log_totalizaPlano(payload, res['mensagem'])
        except Exception as err:
            self.logger.log_error(err)    

    
    def divergenciasNeoway(self):
        try:
            r = requests.get(f'{base_url}/criticas/verificaDivergenciaNeoway?nuControle={self.nuControle}&cdProcesso=26')
            res = r.json()            
            self.logger.log_divergenciaNeoway(res['tipo'])
        except Exception as err:
            self.logger.log_error(err)     
    
    
    def criticasPost(self):
        try:
            r = requests.post(f'{base_url}/criticas/{self.nuControle}')
            res = r.json()            
            self.logger.log_criticas_post(res['tipo'])
        except Exception as err:
            self.logger.log_error(err)     
            
    
    
