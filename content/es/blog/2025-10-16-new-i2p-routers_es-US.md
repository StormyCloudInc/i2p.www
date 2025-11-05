---
title: "New I2P Routers(T)"
date: 2025-10-16
author: "idk"
categories: ["community"]
description: "Multiple new I2P router implementations are emerging, including emissary in Rust and go-i2p in Go, bringing new possibilities for embedding and network diversity."
---

¡Es un momento emocionante para el desarrollo de I2P, nuestra comunidad está creciendo y ahora hay múltiples prototipos de enrutadores I2P nuevos y completamente funcionales que emergen en escena! Estamos muy entusiasmados con este desarrollo y con compartir las noticias contigo.

## ¿Cómo ayuda esto a la red?

Escribir enrutadores I2P nos ayuda a demostrar que nuestros documentos de especificación se pueden utilizar para producir nuevos enrutadores I2P, abre el código a nuevas herramientas de análisis y, en general, mejora la seguridad y la interoperabilidad de la red. Múltiples enrutadores I2P significan que los errores potenciales no son uniformes, un ataque a un enrutador puede no funcionar en un enrutador diferente, evitando un problema de monocultivo. Sin embargo, quizás la perspectiva más emocionante a largo plazo sea la `incorporación`.

## ¿Qué es `la incrustación`?

En el contexto de I2P, la `incrustación` es una forma de incluir un enrutador I2P en otra aplicación directamente, sin necesidad de un enrutador independiente que se ejecute en segundo plano. Esta es una forma en que podemos hacer que I2P sea más fácil de usar, lo que hace que la red sea más fácil de hacer crecer al hacer que el software sea más accesible. Tanto Java como C++ sufren de ser difíciles de usar fuera de sus propios ecosistemas, ya que C++ requiere enlaces C escritos a mano quebradizos y, en el caso de Java, el dolor de comunicarse con una aplicación JVM desde una aplicación no JVM.

Si bien en muchos sentidos esta situación es bastante normal, creo que se puede mejorar para que I2P sea más accesible. Otros idiomas tienen soluciones más elegantes a estos problemas. Por supuesto, siempre debemos considerar y usar las pautas existentes para los enrutadores Java y C++.

## `emisario` aparece de la oscuridad

Completamente independiente de nuestro equipo, un desarrollador llamado `altonen` ha desarrollado una implementación Rust de I2P llamada `Emisary`. Si bien es bastante nuevo todavía, y Rust no nos es familiar, este intrigante proyecto es muy prometedor. Felicitaciones a altonen por crear `un emisario`, estamos bastante impresionados.

### ¿Por qué se oxida?

La razón principal para usar Rust es básicamente la misma que la razón para usar Java o Go. Rust es un lenguaje de programación compilado con gestión de memoria y una comunidad enorme y muy entusiasta. Rust también ofrece funciones avanzadas para producir enlaces al lenguaje de programación C que pueden ser más fáciles de mantener que en otros lenguajes sin dejar de heredar las sólidas características de seguridad de la memoria de Rust.

### ¿Quieres involucrarte con Emisary``?

`emisario` está desarrollado en Github por `altonen`. Puede encontrar el repositorio en: [altonen/emissary](https://github.com/altonen/emissary). Rust también sufre la falta de bibliotecas cliente SAMv3 integrales que sean compatibles con las populares redes de Rust, por lo que escribir una biblioteca SAMv3 es un buen punto de partida.

## `go-i2p` está cada vez más cerca de completarse

Durante aproximadamente 3 años he estado trabajando en go-i2p, `tratando` de convertir una biblioteca incipiente en un enrutador I2P completo en pure-Go, otro lenguaje seguro para la memoria. En los últimos 6 meses más o menos, se ha reestructurado drásticamente para mejorar el rendimiento, la fiabilidad y la capacidad de mantenimiento.

### ¿Por qué ir?

Si bien Rust y Go tienen muchas de las mismas ventajas, en muchos sentidos Go es mucho más fácil de aprender. Durante años, ha habido excelentes bibliotecas y aplicaciones para usar I2P en el lenguaje de programación Go, incluidas las implementaciones más completas de las bibliotecas SAMv3.3. Pero sin un enrutador I2P que podamos administrar automáticamente(como un enrutador integrado), sigue siendo una barrera para los usuarios. El punto de go-i2p es cerrar esa brecha y eliminar todas las asperezas para los desarrolladores de aplicaciones I2P que están trabajando en Go.

### ¿Quieres involucrarte con `go-i2p`?

`go-i2p` está desarrollado en Github, principalmente por `eyedeekay` en este momento y abierto a las contribuciones de la comunidad en [go-i2p](https://github.com/go-i2p/). Dentro de este espacio de nombres existen muchos proyectos, tales como:

#### Bibliotecas de enrutadores

Construimos estas bibliotecas para producir nuestras bibliotecas de enrutadores I2P. Se distribuyen en múltiples repositorios enfocados para facilitar la revisión y hacerlos útiles para otras personas que desean construir enrutadores I2P experimentales y personalizados.

- [go-i2p el enrutador en sí, más activo en este momento](https://github.com/go-i2p/go-i2p)
- [común nuestra biblioteca principal para estructuras de datos I2P](https://github.com/go-i2p/common)
- [cripto nuestra biblioteca para operaciones criptográficas](https://github.com/go-i2p/crypto)
- [go-noise una biblioteca para implementar conexiones basadas en ruido](https://github.com/go-i2p/go-noise)
- [noise una biblioteca de bajo nivel para usar el marco Noise](https://github.com/go-i2p/noise)
- [su3 una biblioteca para manipular archivos su3](https://github.com/go-i2p/su3)

#### Bibliotecas de clientes

- [onramp una biblioteca muy conveniente para usar(o combinar) I2P y Tor](https://github.com/go-i2p/onramp)
- [go-sam-go una biblioteca SAMv3 avanzada, eficiente y muy completa](https://github.com/go-i2p/go-sam-go)

## Si no te gusta Go o Rust y estás pensando en escribir un router I2P, ¿qué debes hacer?

Bueno, hay un proyecto inactivo para escribir un [enrutador I2P en C#](https://github.com/PeterZander/i2p-cs) si desea ejecutar I2P en un XBox. Suena bastante bien en realidad. Si esa tampoco es tu preferencia, podrías hacer como `hizo` Altonen y desarrollar una completamente nueva.

### Decide por qué lo estás escribiendo, para quién lo estás escribiendo

Puedes escribir un enrutador I2P por cualquier motivo, es una red gratuita, pero te ayudará a saber por qué. ¿Hay una comunidad a la que quieras empoderar, una herramienta que creas que es una buena opción para I2P o una estrategia que quieras probar? Averigüe cuál es su objetivo para averiguar dónde necesita comenzar y cómo se verá un estado "terminado".

### Decide en qué idioma quieres hacerlo y por qué

Estas son algunas de las razones por las que podrías elegir un idioma:

- **C**: No hay necesidad de generación vinculante, soportada en todas partes, se puede llamar desde cualquier idioma, lingua franca de la informática moderna
- **Typescript**: Comunidad masiva, muchas aplicaciones, servicios y bibliotecas, trabaja con `node` y `deno`, parece que está en todas partes en este momento
- **D**: Es seguro para la memoria y no Rust or Go
- **Vala**: Emite código C para la plataforma de destino, combinando algunas de las ventajas de los lenguajes seguros para la memoria con la flexibilidad de C
- **Python**: Todo el mundo usa Python

Pero aquí hay algunas razones por las que es posible que no elijas esos idiomas:

- **C**: La gestión de la memoria puede ser un desafío, lo que lleva a errores impactantes
- **Typescript**: TypeScript se transpila a JavaScript, que se interpreta y puede afectar el rendimiento
- **D**: Comunidad relativamente pequeña
- **Vala**: No hay mucha infraestructura subyacente en Vala, terminas usando versiones C de la mayoría de las bibliotecas
- **Python**: Es un lenguaje interpretado que puede afectar el rendimiento

Hay cientos de lenguajes de programación y damos la bienvenida a las bibliotecas y enrutadores I2P mantenidos en todos ellos. Elija sus compensaciones sabiamente y comience.

## Ponte en contacto y comienza a codificar

Tanto si quieres trabajar en Rust, Go, Java, C++ o algún otro lenguaje, ponte en contacto con nosotros en #i2p-dev en Irc2P. Comienza allí y te incorporaremos a los canales específicos del enrutador. También estamos presentes en ramble.i2p en f/i2p, en reddit en r/i2p, y en GitHub y git.idk.i2p. Quedamos a la espera de tu respuesta.
