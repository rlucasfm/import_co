from orcamento import *
import json

if __name__ == "__main__":
    orcamento = Orcamento()
    # Gerar orçamento
    orcamento.geracaoOrcamento('1818546', '066.232.290-86')
    
    #  Envio do titular
    payload_titular = json.load(open('json/json_titular.json'))
    # Carregamendo de anexos do titular
    anexos_titular = []
    anexos_titular.append(json.load(open('json/anexos/titular/anexo1.json')))
    anexos_titular.append(json.load(open('json/anexos/titular/anexo2.json')))
    anexos_titular.append(json.load(open('json/anexos/titular/anexo3.json')))
    anexos_titular.append(json.load(open('json/anexos/titular/anexo4.json')))
    anexos_titular.append(json.load(open('json/anexos/titular/anexo5.json')))
    anexos_titular.append(json.load(open('json/anexos/titular/anexo6.json')))
    orcamento.envioTitular(payload_titular, anexos_titular)
    
    # Envio dos dependentes
    payload_dependente = json.load(open('json/json_dependente.json'))
    # Carregamento de anexos dependente
    anexos_dependente = []
    anexos_dependente.append(json.load(open('json/anexos/dependente/anexo1.json')))
    anexos_dependente.append(json.load(open('json/anexos/dependente/anexo2.json')))
    orcamento.envioDependente(payload_dependente, '83643016085', anexos_dependente, 0)
    
    # Envio de condições de saude
    payload_condicoes = json.load(open('json/condicoes_saude.json'))
    orcamento.condicoesSaude(payload_condicoes)
    
    # Envio criticas GET
    orcamento.criticasGet()
    
    # Totaliza planos
    orcamento.totalizaPlanos()
    
    # Finaliza Proposta
    orcamento.finalizaProposta()
    
    # Enviar Divergencias Neoway
    orcamento.divergenciasNeoway()
    
    # Enviar Criticas POST
    orcamento.criticasPost()
    
    orcamento.logger.log()