from datetime import datetime

class Logger:
    def __init__(self):
        self.creation_date = datetime.now()
        self.date_str = self.creation_date.strftime("%d/%m/%Y %H:%M:%S")
        self.log_str = f'\n=========== LOG {self.date_str} ===========\n'
        
    def __insert_line(self, str):
        self.log_str += str + "\n"
        
    def log(self):
        date_log = self.creation_date.strftime("%Y-%m-%d")
        f = open(f'logs/log-{date_log}.txt', 'a')
        f.write(self.log_str)
        f.close()
        
    def log_error(self, error):
        self.__insert_line(' *** ERROR ***')
        self.__insert_line(str(error))
        
    def log_gerar_orcamento(self, objOrcamento):
        self.__insert_line('Orçamento Gerado - CPF ' + objOrcamento['cpfTitular'])
        self.__insert_line('cdVendedor: ' + objOrcamento['cdVendedor'])
        self.__insert_line('cdFilial: ' + objOrcamento['cdFilial'])
        self.__insert_line('cdSenha: ' + objOrcamento['cdSenha'])
        self.__insert_line('dtCriacao: ' + objOrcamento['dtCriacao'])
        self.__insert_line('mensagem: ' + objOrcamento['mensagem'])
        self.__insert_line('nuControle: ' + objOrcamento['nuControle'])
        self.__insert_line('nuOrcamento: ' + objOrcamento['nuOrcamento'])
        self.__insert_line('tipo: ' + objOrcamento['tipo'])
        
    def log_enviar_titular(self, objTitular, response):
        self.__insert_line(' === Titular enviado com sucesso! === ')
        self.__insert_line(response)
        
    def log_enviar_dependente(self, objDependente, response):
        self.__insert_line(' === Dependente enviado com sucesso! === ')
        self.__insert_line(response)
        
    def log_enviar_anexo(self, objAnexo, response, titular):
        if(titular):
            self.__insert_line(' === Anexo TITULAR enviado com sucesso! === ')
        else:
            self.__insert_line(' === Anexo DEPENDENTE enviado com sucesso! === ')
        self.__insert_line(response)
        
    def log_condicoes_saude(self, objCondicoes, response):
        self.__insert_line(' === Envio de condicoes de saúde === ')
        self.__insert_line(response)
        
    def log_criticas_get(self, res):
        self.__insert_line(' === Condicoes de saude GET === ')
        self.__insert_line(res)
        
    def log_totalizaPlano(self, payload, res):
        self.__insert_line(' === Envio TotalizaPlano === ')
        self.__insert_line(res)
        
    def log_finalizaProposta(self, payload, res):
        self.__insert_line(' === Envio Finaliza Proposta === ')
        self.__insert_line(res)        
        
    def log_divergenciaNeoway(self, res):
        self.__insert_line(' === Envio de Divergências Neoway === ')
        self.__insert_line(res)
    
    def log_criticas_post(self, res):
        self.__insert_line(' === Envio de Criticas POST === ')
        self.__insert_line(res)            