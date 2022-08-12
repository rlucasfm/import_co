import requests

class Dependente:
    def __init__(self,
                 Logger,
                 base_url,
                 nuControle, 
                 nuOrcamento, 
                 cdFilial, 
                 cpfTitular, 
                 cdVendedor, 
                 nuCpfDep):
        self.logger = Logger
        self.base_url = base_url
        self.nuControle = nuControle
        self.nuOrcamento = nuOrcamento
        self.cdFilial = cdFilial
        self.cpfTitular = cpfTitular
        self.cdVendedor = cdVendedor
        self.nuCpfDep = nuCpfDep
        self.nuControleDep = ''  
    
    def enviarDependente(self, objDep):
        try:
            payload = objDep            
            payload['cdVendedor'] = self.cdVendedor
            payload['nuCpf'] = self.nuCpfDep
            payload['nuCpfTitular'] = self.cpfTitular
            payload['nuMatricula'] = self.nuOrcamento
            payload['nuOrcamento'] = self.nuOrcamento
            payload['cdFilial'] = self.cdFilial
                                    
            r = requests.post(f'{self.base_url}/beneficiarios/titulares/{self.nuControle}/dependente', json=payload)
            res = r.text
            self.nuControleDep = res
            self.logger.log_enviar_dependente(payload, res)
        except Exception as err:
            print(err)
            self.logger.log_error(err)
                            
        return self
    