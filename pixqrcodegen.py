import crcmod
import qrcode
import os
import uuid

class Payload():
    def __init__(self, nome, chavepix, valor, cidade, txtId, diretorio=''):     #txtId seria a informação adicional, não é obrigatório
        self.nome = nome
        self.chavepix = chavepix
        self.valor = valor
        self.cidade = cidade
        self.txtId = txtId
        self.diretorioQrCode = diretorio

        self.nome_tam = len(self.nome)
        self.chavepix_tam = len(self.chavepix)
        self.valor_tam = len(valor)
        self.cidade_tam = len(cidade)
        self.txtId_tam = len(txtId)

        #vamos usar pra definir as variações do tamanho do merchant account - segue a mesma lógica pra todas as partes que variam
        self.merchantAccount_tam = f'0014BR.GOV.BCB.PIX01{self.chavepix_tam}{self.chavepix}'             #começo valor fixo - primeira linha id 01 - receber tamanho chave pix + chavepix

        self.transactionAmount_tam = f'{self.valor_tam}{self.valor}'    #na doc ele pede o tamanho do valor + o valor

        self.addDataField_tam = f'05{self.txtId_tam:02}{self.txtId}'

        self.payloadFormat = '000201'                         #payload format é o início - id - 00 - tam 02 - valor 01
        self.merchantAccount = f'26{len((self.merchantAccount_tam))}{self.merchantAccount_tam}'                             #merchant account information - pix - id 26
        if self.valor_tam <= 9:
            self.transactionAmount_tam = f'0{self.valor_tam}{self.valor}'  #vai receber um 0 a esquerda
        else:
            self.transactionAmount_tam = f'{self.valor_tam}{self.valor}'

        if self.txtId_tam <= 9:
            self.txtId_tam = f'050{self.txtId_tam}{self.txtId}'  #vai receber um 050 a esquerda
        else:
            self.addDataField_tam = f'05{self.txtId_tam}{self.txtId}'  #vai receber somente 05 a esquerda

        if self.nome_tam <= 9:
            self.nome_tam = f'0{self.nome_tam}'  # vai receber um 0 a esquerda

        if self.cidade_tam <= 9:
            self.cidade_tam = f'0{self.cidade_tam}'  # vai receber um 0 a esquerda

        self.merchantCategCode = '52040000'                     #merchant category code - id 52 - tam 04 - valor 0000
        self.transactionCurrency = '5303986'                    #transaction currency - id 53 - tam 03 - valor 986 R$ - equivale ao real
        self.transactionAmount = f'54{self.transactionAmount_tam}' #transaction amount - id 54 - método pra formatar o valor nos ifs
        self.countryCode = '5802BR'                             #country code - id 58 - id 02 - valor BR
        self.merchantName = f'59{self.nome_tam}{self.nome}'     #merchant name - id 59 - método pra formatar nos ifs - precisamos do tamanho do nome + nome
        self.merchantCity = f'60{self.cidade_tam}{self.cidade}'                        #merchant-city - id 60 - depois tem que fazer algo pra receber a cidade
        self.addDataField = f'62{len(self.addDataField_tam)}{self.addDataField_tam}'                        #additional data field - id 62
        self.crc16 = '6304'                             #CRC16-CCITT - id 63 - tam 04

    def gerarPayload(self):
        #todos as variáveis da payload
        self.payload = f'{self.payloadFormat}{self.merchantAccount }{self.merchantCategCode}{self.transactionCurrency}{self.transactionAmount}{self.countryCode}{self.merchantName}{self.merchantCity}{self.addDataField}{self.crc16}'
        print()
        print(self.payload)
        print()

        self.gerarCrc16(self.payload)

    def gerarCrc16(self, payload):
        #Processo de acordo com a documentação
        crc16 = crcmod.mkCrcFun(poly=0x11021, initCrc=0xFFFF, rev=False, xorOut=0x0000)

        self.crc16Code = hex(crc16(str(payload).encode('utf-8')))

        self.crc16Code_formatado = str(self.crc16Code).replace('0x', '').upper().zfill(4)

        self.payload_completa = f'{payload}{self.crc16Code_formatado}'

        self.gerarQrCode(self.payload_completa, self.diretorioQrCode)

    def gerarQrCode(self, payload, diretorio):
        dir = os.path.expanduser(diretorio)

        # Gera um nome de arquivo único usando UUID
        prefixo = 'qrcode'
        nome_arquivo = prefixo + '_' +str(uuid.uuid4()) + '.png'

        # Crie o QR Code
        qrcode_imagem = qrcode.make(payload)

        # Salva o arquivo usando o nome único
        caminho_completo = os.path.join(dir, nome_arquivo)
        qrcode_imagem.save(caminho_completo)

        # Retorna o nome do arquivo gerado
        return nome_arquivo

    def print_variaveis(self):
        print(len(self.merchantAccount_tam))   #sem o len - vai imprimir por exemplo 0014BR.GOV.BCB.PIX0124emailteste2022@gmail.com - 24 é o tamanho da chave + chave pix
        print(self.transactionAmount_tam)      #retorna 0510.00 - tamanho valor(5) + valor(10.00) + 0 a esquerda pois o valor é <= 10





