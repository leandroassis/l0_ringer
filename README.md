# ringer-L0


## Premissas do desenvolvimento em Hardware

A entrada da energia é feita em MeV (não confirmado), dessa forma, o range de energia é de 0 a 500 000 MeV (500 Gev). Ou seja, necessitamos de 19 bits para representar esse intervalo.

Para representar as casas decimais, trabalharemos com 6 casas decimais de precisão. Ou seja, os valores devem estar no range de 0 a 999999. Dessa forma, necessitamos de 20 bits para representar esse intervalo.

Assim, a representação em em fixed-point é de 41 bits (1 de sinal).


Os valores de eta, phi, deta e dphi também seguem essa notação. Entretando no caso deles, muito mais precisão pode ser adicionada (mais bits decimais)

### Representação de valores em Fixed Point

Energia: (-524288,000000 -> 524288,4857) MeV
``` s     integer part       decimal part   ```
    0 0000000000000000000 0000000000000000000

Eta, Phi, dEta, dPhi: (-4,000000000000 -> 4,037438953473) unid.
``` s integer part decimal part (37 bits)   ```
    0     000           00000...0000  

### Operações em Fixed Point
As operações em fixed point são feitas considerando as partes da stream de bits que representa a parte inteira e a parte decimal.

#### Soma e subtração
A soma e subtração são feitas de forma direta, considerando que a parte inteira e a parte decimal são somadas/subtraídas separadamente.
Ex:
    Suponha as seguintes entradas de energia:
    14,567543 + (-2,345678) = (aprox) 12,221876

    Em bits (duas somas/substrações seguindo regra de complemento de 2):

    Parte inteira                  Parte decimal
  o 0 0000000000000001110 | o s 10001010100011110111
  o 1 1111111111111111101 | o s 10101011100110110001
    ----------------------| ------------------------
  1 0 0000000000000001011 | 1 0 00110110001010101000

    Como houve overflow na parte decimal, é necessário somar 1 na parte inteira. O Overflow da parte inteira é descartado (regra de soma e subtração em complemento de 2). O bit de sinal não precisa ser replicado na parte decimal, apenas ligado via wire.

    Logo o resultado é 0 000000000000000101100110110001010101000 (12,221864). Erro introduzido: 0,000012

#### Multiplicação
A multiplicação pode ser descrita como:

    (a+b/10e6).(c+d/10e6) = a.c (parte inteira) + 10e-6.(a.d + b.c) + 10e-12.b.d (possivelmente descartável)

Dessa forma, a parte inteira é o produto das partes inteiras, somado com o overflow da soma das partes decimais.

Ex:
    2,123456*3,123456= 6,632521

    Em bits (5 multiplicações inteiras, 3 somas/subtrações em complemento de 2, 1 divisão por 10e6):

    Parte inteira
    2*3 = 00000000000000000010 * 00000000000000000011 = 00000000000000000110 (6)

    Parte decimal
    2*0,123456 + 3*0,123456 = (000000000000000000010*000011110001001000000 + 00000000000000000011*000011110001001000000)/011110100001001000000 = 0 01011010011011000000 + 0 00111100010010000000 (0,617280) 

    Até esse ponto existe um erro de 0,15241. Vamos introduzir a última parte para garantir mais precisão

    (0,123456*0,123456).10e-12 = 000011110001001000000*000011110001001000000 = 01110001100011101010001000000000000/011110100001001000000 = 0 00000011101110001001 (0,15241)

#### Divisão
A divisão pode ser descrita como:
                                 inteira            decimal
    (a+b/10e6)/(c+d/10e6) = 10e6*a/(10e6*c + d) + b/(10e6*c + d)

Ex:
    2,123456/3,123456 = 0,679842

    Em bits (2 divisão inteiras, 1 soma/subtração em complemento de 2):

    Parte inteira
    10e6*2/(10e6*3 + 123456) = 011110100001001000000*00000000000000000010/(011110100001001000000*00000000000000000011 + 00011110001001000000) = 0

    Parte decimal
    123456/(3*10e6 + 123456) = (000000000000000000010*1001100100100000000000)/011110100001001000000 = 0 00000000000000000001 (0,680272)

    Até esse ponto existe um erro de 0,000000. Vamos introduzir a última parte para garantir mais precisão

    123456/(3*10e6 + 123456) = (000011110001001000000/00000000000000000011*1001100100100000000000)/011110100001001000000 = 0 00000000000000000001 (0,000000)




    


## Pipeline de execução
## Construção de torres

