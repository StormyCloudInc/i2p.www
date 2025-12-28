---
title: "Transporte SSU (Obsoleto)"
description: "Transporte UDP original usado antes do SSU2"
slug: "ssu"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
type: docs
reviewStatus: "needs-review"
---

> **Obsoleto:** SSU (UDP seguro semiconfiável) foi substituído por [SSU2](/docs/specs/ssu2/). O Java I2P removeu o SSU na versão 2.4.0 (API 0.9.61) e o i2pd o removeu na versão 2.44.0 (API 0.9.56). Este documento é mantido apenas para referência histórica.

## Destaques

- Transporte UDP fornecendo entrega ponto a ponto criptografada e autenticada de mensagens I2NP.
- Baseava-se em um aperto de mão Diffie–Hellman de 2048 bits (mesmo primo que o ElGamal).
- Cada datagrama transportava um HMAC-MD5 de 16 bytes (variante truncada não padrão) + um IV de 16 bytes, seguido por uma carga útil criptografada com AES-256-CBC.
- A prevenção de replay e o estado da sessão eram rastreados dentro da carga útil criptografada.

## Cabeçalho da mensagem

```
[16-byte MAC][16-byte IV][encrypted payload]
```
Cálculo de MAC utilizado: `HMAC-MD5(ciphertext || IV || (len ^ version ^ ((netid-2)<<8)))` com uma chave de MAC de 32 bytes. O comprimento da carga útil era um valor de 16 bits em big-endian, incluído no cálculo do MAC. A versão do protocolo assumia por padrão `0`; netId assumia por padrão `2` (rede principal).

## Chaves de Sessão e de MAC

Derivados do segredo DH compartilhado:

1. Converta o valor compartilhado para um array de bytes em big-endian (prefixe `0x00` se o bit mais significativo estiver definido).
2. Chave de sessão: primeiros 32 bytes (preencha com zeros se for mais curta).
3. Chave MAC: bytes 33–64; se insuficiente, use o hash SHA-256 do valor compartilhado.

## Estado

Routers não anunciam mais endereços SSU. Clientes devem migrar para os transportes SSU2 ou NTCP2. Implementações históricas podem ser encontradas em versões antigas:

- Código-fonte Java anterior à versão 2.4.0 em `router/transport/udp`
- Código-fonte do i2pd anterior à versão 2.44.0

Para o comportamento atual do transporte UDP, consulte a [especificação do SSU2](/docs/specs/ssu2/).
