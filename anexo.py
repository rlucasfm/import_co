import requests

class Anexo:
    def __init__(self, 
                 logger,
                 base_url,
                 objAnexo,
                 nuControle, 
                 e_titular, 
                 nuControleDep='', 
                 usuarioIndice=0):
        self.logger = logger
        self.base_url = base_url
        self.objAnexo = objAnexo
        self.nuControle = nuControle
        self.e_titular = e_titular
        self.nuControleDep = nuControleDep
        self.usuarioIndice = usuarioIndice
        
    
    def enviarAnexo(self):
        payload = self.objAnexo
        payload['nuControle'] = self.nuControle
        if(self.e_titular):
            payload['usuarioIndiceVDD'] = 'titular'
        else:
            payload['nuControleDep'] = self.nuControleDep
            payload['usuarioIndiceVDD'] = self.usuarioIndice
        
        r = requests.post(f'{self.base_url}/documentos/enviarAnexo', json=payload)
        res = r.text
        self.logger.log_enviar_anexo(payload, res, self.e_titular)