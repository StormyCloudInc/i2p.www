---
title: "RedDSA-BLAKE2b-Ed25519"
number: "148"
author: "zzz"
created: "2019-03-12"
lastupdated: "2019-04-11"
status: "Abrir"
thread: "http://zzz.i2p/topics/2689"
---

## Descripción general

Esta propuesta añade un nuevo tipo de firma usando BLAKE2b-512 con cadenas de personalización y sales, para reemplazar SHA-512. Esto eliminará tres clases de posibles ataques.

## Motivación

Durante las discusiones y el diseño de NTCP2 (propuesta 111) y LS2 (propuesta 123), consideramos brevemente varios ataques que eran posibles y cómo prevenirlos. Tres de estos ataques son los Ataques de Extensión de Longitud, los Ataques Cross-Protocol y la Identificación de Mensajes Duplicados.

Para ambos NTCP2 y LS2, decidimos que estos ataques no eran directamente relevantes a las propuestas en cuestión, y cualquier solución entraba en conflicto con el objetivo de minimizar nuevas primitivas. Además, determinamos que la velocidad de las funciones hash en estos protocolos no era un factor importante en nuestras decisiones. Por lo tanto, en su mayoría diferimos la solución a una propuesta separada. Aunque sí agregamos algunas características de personalización a la especificación LS2, no requerimos ninguna función hash nueva.

Muchos proyectos, como [ZCash](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf), están utilizando funciones hash y algoritmos de firma basados en algoritmos más nuevos que no son vulnerables a los siguientes ataques.

### Length Extension Attacks

SHA-256 y SHA-512 son vulnerables a [Ataques de Extensión de Longitud (LEA)](https://en.wikipedia.org/wiki/Length_extension_attack). Este es el caso cuando se firman los datos reales, no el hash de los datos. En la mayoría de protocolos I2P (streaming, datagramas, netDb, y otros), se firman los datos reales. Una excepción son los archivos SU3, donde se firma el hash. La otra excepción son los datagramas firmados para DSA (tipo de firma 0) únicamente, donde se firma el hash. Para otros tipos de firma de datagramas firmados, se firman los datos.

### Cross-Protocol Attacks

Los datos firmados en los protocolos I2P pueden ser vulnerables a Ataques Cross-Protocol (CPA) debido a la falta de separación de dominio. Esto permite a un atacante usar datos recibidos en un contexto (como un datagrama firmado) y presentarlos como datos válidos y firmados en otro contexto (como streaming o base de datos de red). Aunque es poco probable que los datos firmados de un contexto se analicen como datos válidos en otro contexto, es difícil o imposible analizar todas las situaciones para saberlo con certeza. Además, en algunos contextos, puede ser posible que un atacante induzca a una víctima a firmar datos especialmente diseñados que podrían ser datos válidos en otro contexto. Nuevamente, es difícil o imposible analizar todas las situaciones para saberlo con certeza.

### Ataques de Extensión de Longitud

Los protocolos I2P pueden ser vulnerables a la Identificación de Mensajes Duplicados (DMI). Esto podría permitir a un atacante identificar que dos mensajes firmados tienen el mismo contenido, incluso si estos mensajes y sus firmas están cifrados. Aunque es poco probable debido a los métodos de cifrado utilizados en I2P, es difícil o imposible analizar todas las situaciones para saberlo con certeza. Al usar una función hash que proporciona un método para añadir una sal aleatoria, todas las firmas serán diferentes incluso al firmar los mismos datos. Aunque Red25519 tal como se define en la propuesta 123 añade una sal aleatoria a la función hash, esto no resuelve el problema para los lease sets no cifrados.

### Ataques Cross-Protocol

Aunque no es una motivación principal para esta propuesta, SHA-512 es relativamente lento, y hay funciones hash más rápidas disponibles.

## Goals

- Prevenir los ataques mencionados anteriormente
- Minimizar el uso de nuevas primitivas criptográficas
- Usar primitivas criptográficas probadas y estándar
- Usar curvas estándar
- Usar primitivas más rápidas si están disponibles

## Design

Modificar el tipo de firma RedDSA_SHA512_Ed25519 existente para usar BLAKE2b-512 en lugar de SHA-512. Agregar cadenas de personalización únicas para cada caso de uso. El nuevo tipo de firma puede usarse tanto para leasesets no ciegos como ciegos.

## Justification

- [BLAKE2b](https://blake2.net/blake2.pdf) no es vulnerable a LEA.
- BLAKE2b proporciona una forma estándar de agregar cadenas de personalización para la separación de dominios
- BLAKE2b proporciona una forma estándar de agregar una sal aleatoria para prevenir DMI.
- BLAKE2b es más rápido que SHA-256 y SHA-512 (y MD5) en hardware moderno,
  según la [especificación BLAKE2](https://blake2.net/blake2.pdf).
- Ed25519 sigue siendo nuestro tipo de firma más rápido, mucho más rápido que ECDSA, al menos en Java.
- [Ed25519](http://cr.yp.to/papers.html#ed25519) requiere una función hash criptográfica de 512 bits.
  No especifica SHA-512. BLAKE2b es igualmente adecuado para la función hash.
- BLAKE2b está ampliamente disponible en bibliotecas para muchos lenguajes de programación, como Noise.

## Specification

Usar BLAKE2b-512 sin clave como en la [especificación BLAKE2](https://blake2.net/blake2.pdf) con salt y personalización. Todos los usos de firmas BLAKE2b utilizarán una cadena de personalización de 16 caracteres.

Cuando se utiliza en la firma RedDSA_BLAKE2b_Ed25519, se permite una salt aleatoria, sin embargo no es necesaria, ya que el algoritmo de firma añade 80 bytes de datos aleatorios (ver propuesta 123). Si se desea, al hacer hash de los datos para calcular r, establecer una nueva salt aleatoria BLAKE2b de 16 bytes para cada firma. Al calcular S, restablecer la salt al valor predeterminado de todos ceros.

Cuando se use en la verificación RedDSA_BLAKE2b_Ed25519, no usar un salt aleatorio, usar el valor por defecto de todos-ceros.

Las características de salt y personalización no están especificadas en [RFC 7693](https://tools.ietf.org/html/rfc7693); utiliza esas características tal como se especifica en la [especificación BLAKE2](https://blake2.net/blake2.pdf).

### Identificación de Mensajes Duplicados

Para RedDSA_BLAKE2b_Ed25519, reemplazar la función hash SHA-512 en RedDSA_SHA512_Ed25519 (tipo de firma 11, como se define en la propuesta 123) con BLAKE2b-512. Sin otros cambios.

No necesitamos un reemplazo para EdDSA_SHA512_Ed25519ph (tipo de firma 8) para archivos su3, porque la versión prehashed de EdDSA no es vulnerable a LEA. EdDSA_SHA512_Ed25519 (tipo de firma 7) no está soportado para archivos su3.

| Type | Type Code | Since | Usage |
|------|-----------|-------|-------|
| RedDSA_BLAKE2b_Ed25519 | 12 | TBD | For Router Identities, Destinations and encrypted leasesets only; never used for Router Identities |
### Velocidad

Lo siguiente se aplica al nuevo tipo de firma.

| Data Type | Length |
|-----------|--------|
| Hash | 64 |
| Private Key | 32 |
| Public Key | 32 |
| Signature | 64 |
### Personalizations

Para proporcionar separación de dominios para los diversos usos de firmas, utilizaremos la característica de personalización de BLAKE2b.

Todos los usos de firmas BLAKE2b utilizarán una cadena de personalización de 16 caracteres. Cualquier nuevo uso debe añadirse a la tabla aquí, con una personalización única.

El handshake de NTCP 1 y SSU que se usa a continuación es para los datos firmados definidos en el propio handshake. Los RouterInfos firmados en los Mensajes DatabaseStore usarán la personalización NetDb Entry, tal como si estuvieran almacenados en la NetDB.

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

## Diseño

- Alternativa 1: Propuesta 146;
  Proporciona resistencia LEA
- Alternativa 2: [Ed25519ctx en RFC 8032](https://tools.ietf.org/html/rfc8032);
  Proporciona resistencia LEA y personalización.
  Estandarizado, ¿pero alguien lo usa?
  Ver [RFC 8032](https://tools.ietf.org/html/rfc8032) y [esta discusión](https://moderncrypto.org/mail-archive/curves/2017/000925.html).
- ¿Es útil para nosotros el hashing "con clave"?

## Justificación

Lo mismo que con el despliegue para tipos de firma anteriores.

Planeamos cambiar los nuevos routers del tipo 7 al tipo 12 como predeterminado. Planeamos eventualmente migrar los routers existentes del tipo 7 al tipo 12, utilizando el proceso de "rekeying" usado después de que se introdujo el tipo 7. Planeamos cambiar los nuevos destinos del tipo 7 al tipo 12 como predeterminado. Planeamos cambiar los nuevos destinos encriptados del tipo 11 al tipo 13 como predeterminado.

Admitiremos blinding desde los tipos 7, 11 y 12 al tipo 12. No admitiremos blinding del tipo 12 al tipo 11.

Los nuevos routers podrían comenzar a usar el nuevo tipo de firma por defecto después de unos pocos meses. Los nuevos destinos podrían comenzar a usar el nuevo tipo de firma por defecto después de quizás un año.

Para la versión mínima del router 0.9.TBD, los routers deben asegurar:

- No almacenar (o inundar) un RI o LS con el nuevo tipo de sig a routers con versión menor a 0.9.TBD.
- Al verificar un almacén de netdb, no obtener un RI o LS con el nuevo tipo de sig de routers con versión menor a 0.9.TBD.
- Los routers con un nuevo tipo de sig en su RI pueden no conectarse a routers con versión menor a 0.9.TBD,
  ya sea con NTCP, NTCP2, o SSU.
- Las conexiones de streaming y datagramas firmados no funcionarán con routers con versión menor a 0.9.TBD,
  pero no hay manera de saberlo, por lo que el nuevo tipo de sig no debería usarse por defecto durante
  algunos meses o años después de que se lance 0.9.TBD.
