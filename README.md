# Projeto Python: Gerador de QR-Code Pix
Este é um gerador de QR Code PIX simples e personalizável em Python. Ele permite que você crie um QR Code PIX a partir dos detalhes de pagamento fornecidos.

## Dependências:

- crcmod: Usado para calcular o código de verificação CRC16.
- qrcode: Usado para criar o QR Code.
- os: Usado para operações de sistema de arquivos.
- uuid: Usado para gerar nomes exclusivos de arquivos.

## Como usar:
1. Importe a classe Payload caso esteja em um arquivo externo:
```
from seu_modulo import Payload
```

2. Crie uma instância da classe Payload com os detalhes do pagamento
```
if __name__ == '__main__':
    p = Payload('Joao Silva', '+5544990000009', '0.50', 'Cidade', 'LOJA01')
    p.gerarPayload()
Obs: no nome é obrigatoriamente Nome Sobrenome, não podendo menos ou mais informações.
```

3. O QR-Code ficará salvo na sua pasta com o prefixo qrcode_

## Explicação da lógica do algoritmo baseada na documentação do Banco Central
Link para a documentação: https://www.bcb.gov.br/content/estabilidadefinanceira/spb_docs/ManualBRCode.pdf


Foto da tabela seguida:
![Screenshot_2](https://github.com/leocalheiros/qrcode-pixgen/assets/123272507/e5f676c5-3165-47cd-8fb1-7aa365528434)

- Explicação:
```
- Para usar precisamos definir:
    Nome: Nome Sobrenome
    Chavepix: chavepix
    Valor: 0.00
    Cidade: Cidade
    txtId: txtId

- Explicação da payload de acordo com o código:
    Se a entrada for: ('nome', 'emailteste2022@gmail.com', '10.00', 'cidade', 'LOJA01')
    O código pix gerado será:
    000201 26460014BR.GOV.BCB.PIX0124emailteste2022@gmail.com52040000 5303986 540510.00 5802BR 5904nome 6006cidade 62100506LOJA01 6304

    000201 - payloadFormat fixo

    26460014BR.GOV.BCB.PIX:
    26: id merchant account information fixo
    46 - merchant account information - tamanho da chave pix
    0014BR.GOV.BCB.PIX - valor fixo - id + tam + valor merchant account information

    0124emailteste2022@gmail.com:
    01 - merchant account information - id chave pix
    24 - merchant account information - tamanho da chave pix
    emailteste2022@gmail.com - valor chave pix

    5303986 - transaction currency - valor fixo

    540510.00:
    54 - id transaction amount
    05 - transaction amount - tam valor - valor = 10.00 - len = 5
    10.00 - transaction amount - valor

    5802BR - valor fixo country code

    5904nome:
    59 - id merchant name
    04 - tam merchant name = nome - len = 4
    nome = valor merchant name

    6006cidade:
    60 - id merchant city
    06 - tam merchant city = cidade - len = 6
    cidade - valor merchant city

    62100506LOJA01:
    62 - id additional data field
    10 - soma do tanto de caracteres 0506LOJA01 = 10
    0506LOJA01 - 050 de prefixo do if o 05 é o id da reference label + tam txtId + txtId

    6304 - fixo do CRC16
```
  
