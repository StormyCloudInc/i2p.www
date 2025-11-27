---
title: "RedDSA-BLAKE2b-Ed25519"
number: "148"
author: "zzz"
created: "2019-03-12"
lastupdated: "2019-04-11"
status: "Abrir"
thread: "http://zzz.i2p/topics/2689"
---

## Visão Geral

Esta proposta adiciona um novo tipo de assinatura usando BLAKE2b-512 com strings de personalização e salts, para substituir SHA-512. Isso eliminará três classes de possíveis ataques.

## Motivação

Durante as discussões e design do NTCP2 (proposta 111) e LS2 (proposta 123), consideramos brevemente vários ataques que eram possíveis e como preveni-los. Três desses ataques são Ataques de Extensão de Comprimento, Ataques Cross-Protocol e Identificação de Mensagem Duplicada.

Para tanto NTCP2 quanto LS2, decidimos que esses ataques não eram diretamente relevantes às propostas em questão, e quaisquer soluções conflitavam com o objetivo de minimizar novas primitivas. Além disso, determinamos que a velocidade das funções hash nesses protocolos não era um fator importante em nossas decisões. Portanto, adiamos em grande parte a solução para uma proposta separada. Embora tenhamos adicionado alguns recursos de personalização à especificação LS2, não exigimos nenhuma função hash nova.

Muitos projetos, como [ZCash](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf), estão usando funções hash e algoritmos de assinatura baseados em algoritmos mais novos que não são vulneráveis aos seguintes ataques.

### Length Extension Attacks

SHA-256 e SHA-512 são vulneráveis a [Ataques de Extensão de Comprimento (LEA)](https://en.wikipedia.org/wiki/Length_extension_attack). Este é o caso quando os dados reais são assinados, não o hash dos dados. Na maioria dos protocolos I2P (streaming, datagramas, netdb e outros), os dados reais são assinados. Uma exceção são os arquivos SU3, onde o hash é assinado. A outra exceção são datagramas assinados para DSA (tipo de assinatura 0) apenas, onde o hash é assinado. Para outros tipos de assinatura de datagramas assinados, os dados são assinados.

### Cross-Protocol Attacks

Dados assinados nos protocolos I2P podem ser vulneráveis a Ataques Cross-Protocol (CPA) devido à falta de separação de domínio. Isso permite que um atacante use dados recebidos em um contexto (como um datagrama assinado) e os apresente como dados válidos e assinados em outro contexto (como streaming ou network database). Embora seja improvável que os dados assinados de um contexto sejam analisados como dados válidos em outro contexto, é difícil ou impossível analisar todas as situações para ter certeza. Além disso, em alguns contextos, pode ser possível para um atacante induzir uma vítima a assinar dados especialmente elaborados que poderiam ser dados válidos em outro contexto. Novamente, é difícil ou impossível analisar todas as situações para ter certeza.

### Ataques de Extensão de Comprimento

Os protocolos I2P podem ser vulneráveis à Identificação de Mensagem Duplicada (DMI). Isso pode permitir que um atacante identifique que duas mensagens assinadas têm o mesmo conteúdo, mesmo que essas mensagens e suas assinaturas estejam criptografadas. Embora seja improvável devido aos métodos de criptografia usados no I2P, é difícil ou impossível analisar todas as situações para ter certeza. Ao usar uma função hash que fornece um método para adicionar um salt aleatório, todas as assinaturas serão diferentes mesmo ao assinar os mesmos dados. Embora o Red25519 conforme definido na proposta 123 adicione um salt aleatório à função hash, isso não resolve o problema para leaseSet não criptografados.

### Ataques Cross-Protocol

Embora não seja uma motivação principal para esta proposta, o SHA-512 é relativamente lento, e funções de hash mais rápidas estão disponíveis.

## Goals

- Prevenir os ataques mencionados acima
- Minimizar o uso de novas primitivas criptográficas
- Usar primitivas criptográficas comprovadas e padronizadas
- Usar curvas padronizadas
- Usar primitivas mais rápidas se disponíveis

## Design

Modifique o tipo de assinatura RedDSA_SHA512_Ed25519 existente para usar BLAKE2b-512 em vez de SHA-512. Adicione strings de personalização únicas para cada caso de uso. O novo tipo de assinatura pode ser usado tanto para leaseSets não cegos quanto cegos.

## Justification

- [BLAKE2b](https://blake2.net/blake2.pdf) não é vulnerável a LEA.
- BLAKE2b fornece uma maneira padrão de adicionar strings de personalização para separação de domínio
- BLAKE2b fornece uma maneira padrão de adicionar um salt aleatório para prevenir DMI.
- BLAKE2b é mais rápido que SHA-256 e SHA-512 (e MD5) em hardware moderno,
  de acordo com a [especificação BLAKE2](https://blake2.net/blake2.pdf).
- Ed25519 ainda é nosso tipo de assinatura mais rápido, muito mais rápido que ECDSA, pelo menos em Java.
- [Ed25519](http://cr.yp.to/papers.html#ed25519) requer uma função hash criptográfica de 512 bits.
  Não especifica SHA-512. BLAKE2b é igualmente adequado para a função hash.
- BLAKE2b está amplamente disponível em bibliotecas para muitas linguagens de programação, como Noise.

## Specification

Use BLAKE2b-512 sem chave como na [especificação BLAKE2](https://blake2.net/blake2.pdf) com salt e personalização. Todos os usos de assinaturas BLAKE2b usarão uma string de personalização de 16 caracteres.

Quando usado na assinatura RedDSA_BLAKE2b_Ed25519, um salt aleatório é permitido, porém não é necessário, pois o algoritmo de assinatura adiciona 80 bytes de dados aleatórios (veja proposta 123). Se desejado, ao fazer o hash dos dados para calcular r, defina um novo salt aleatório BLAKE2b de 16 bytes para cada assinatura. Ao calcular S, redefina o salt para o padrão de todos-zeros.

Quando usado na verificação RedDSA_BLAKE2b_Ed25519, não use um salt aleatório, use o padrão de todos-zeros.

As características de salt e personalização não estão especificadas na [RFC 7693](https://tools.ietf.org/html/rfc7693); use essas características conforme especificado na [especificação BLAKE2](https://blake2.net/blake2.pdf).

### Identificação de Mensagens Duplicadas

Para RedDSA_BLAKE2b_Ed25519, substitua a função hash SHA-512 em RedDSA_SHA512_Ed25519 (tipo de assinatura 11, conforme definido na proposta 123) por BLAKE2b-512. Nenhuma outra alteração.

Não precisamos de uma substituição para EdDSA_SHA512_Ed25519ph (tipo de assinatura 8) para arquivos su3, porque a versão pré-hash do EdDSA não é vulnerável ao LEA. EdDSA_SHA512_Ed25519 (tipo de assinatura 7) não é suportado para arquivos su3.

| Type | Type Code | Since | Usage |
|------|-----------|-------|-------|
| RedDSA_BLAKE2b_Ed25519 | 12 | TBD | For Router Identities, Destinations and encrypted leasesets only; never used for Router Identities |
### Velocidade

O seguinte aplica-se ao novo tipo de assinatura.

| Data Type | Length |
|-----------|--------|
| Hash | 64 |
| Private Key | 32 |
| Public Key | 32 |
| Signature | 64 |
### Personalizations

Para fornecer separação de domínio para os vários usos de assinaturas, usaremos o recurso de personalização do BLAKE2b.

Todos os usos de assinaturas BLAKE2b utilizarão uma string de personalização de 16 caracteres. Qualquer novo uso deve ser adicionado à tabela aqui, com uma personalização única.

Os handshakes NTCP 1 e SSU usados abaixo são para os dados assinados definidos no próprio handshake. RouterInfos assinados em Mensagens DatabaseStore usarão a personalização NetDb Entry, exatamente como se estivessem armazenados no NetDB.

| Usage | 16 Byte Personalization |
|-------|--------------------------|
| I2CP SessionConfig | "I2CP_SessionConf" |
| NetDB Entries (RI, LS, LS2) | "network_database" |
| NTCP 1 handshake | "NTCP_1_handshake" |
| Signed Datagrams | "sign_datagramI2P" |
| Streaming | "streaming_i2psig" |
| SSU handshake | "SSUHandshakeSign" |
| SU3 Files | n/a, not supported |
| Unit tests | "test1234test5678" |
## Objetivos

## Design

- Alternativa 1: Proposta 146;
  Fornece resistência a LEA
- Alternativa 2: [Ed25519ctx na RFC 8032](https://tools.ietf.org/html/rfc8032);
  Fornece resistência a LEA e personalização.
  Padronizado, mas alguém o usa?
  Veja [RFC 8032](https://tools.ietf.org/html/rfc8032) e [esta discussão](https://moderncrypto.org/mail-archive/curves/2017/000925.html).
- O hashing "com chave" é útil para nós?

## Justificação

O mesmo que com o lançamento para tipos de assinatura anteriores.

Planejamos alterar novos routers do tipo 7 para o tipo 12 como padrão. Planejamos eventualmente migrar routers existentes do tipo 7 para o tipo 12, usando o processo de "rekeying" utilizado após a introdução do tipo 7. Planejamos alterar novos destinos do tipo 7 para o tipo 12 como padrão. Planejamos alterar novos destinos criptografados do tipo 11 para o tipo 13 como padrão.

Ofereceremos suporte à ofuscação dos tipos 7, 11 e 12 para o tipo 12. Não ofereceremos suporte à ofuscação do tipo 12 para o tipo 11.

Novos routers poderiam começar a usar o novo tipo de assinatura por padrão após alguns meses. Novos destinos poderiam começar a usar o novo tipo de assinatura por padrão após talvez um ano.

Para a versão mínima do router 0.9.TBD, os routers devem garantir:

- Não armazenar (ou fazer flood) um RI ou LS com o novo tipo de assinatura para routers com versão inferior a 0.9.TBD.
- Ao verificar um armazenamento netDb, não buscar um RI ou LS com o novo tipo de assinatura de routers com versão inferior a 0.9.TBD.
- Routers com um novo tipo de assinatura em seu RI podem não conseguir conectar-se a routers com versão inferior a 0.9.TBD,
  seja com NTCP, NTCP2, ou SSU.
- Conexões streaming e datagramas assinados não funcionarão com routers com versão inferior a 0.9.TBD,
  mas não há como saber isso, então o novo tipo de assinatura não deve ser usado por padrão por alguns meses
  ou anos após o lançamento da versão 0.9.TBD.
