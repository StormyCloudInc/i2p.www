---
title: "Nuevos routers I2P(d)"
date: 2025-10-16
author: "idk"
categories: ["community"]
description: "Están surgiendo múltiples implementaciones nuevas de enrutadores I2P, como emissary en Rust y go-i2p en Go, que aportan nuevas posibilidades de incrustación y diversidad de redes."
---


Es un momento emocionante para el desarrollo de I2P, nuestra comunidad está creciendo y ahora hay varios prototipos de routers I2P nuevos y completamente funcionales que están apareciendo en escena. Estamos muy ilusionados con este desarrollo y con compartir las noticias contigo.

## ¿Cómo ayuda esto a la red?

Escribir enrutadores I2P nos ayuda a demostrar que nuestros documentos de especificación pueden utilizarse para producir nuevos enrutadores I2P, abre el código a nuevas herramientas de análisis y, en general, mejora la seguridad y la interoperabilidad de la red. Múltiples enrutadores I2P significa que los errores potenciales no son uniformes, un ataque en un enrutador puede no funcionar en un enrutador diferente, evitando un problema de monocultivo. Pero quizá la perspectiva más interesante a largo plazo sea la "incrustación".

## ¿Qué es la "incrustación"?

En el contexto de I2P, `embedding` es una forma de incluir un router I2P en otra aplicación directamente, sin necesidad de un router independiente ejecutándose en segundo plano. Esta es una forma de facilitar el uso de I2P, lo que facilita el crecimiento de la red al hacer el software más accesible. Tanto Java como C++ adolecen de ser difíciles de usar fuera de sus propios ecosistemas, con C++ requiriendo frágiles enlaces C escritos a mano y, en el caso de Java, el dolor de comunicarse con una aplicación JVM desde una aplicación no JVM.

Aunque en muchos aspectos esta situación es bastante normal, creo que puede mejorarse para que I2P sea más accesible. Otros lenguajes tienen soluciones más elegantes a estos problemas. Por supuesto, siempre debemos tener en cuenta y utilizar las directrices existentes para los routers Java y C++.

## `emisario` aparece de la oscuridad

Completamente independiente de nuestro equipo, un desarrollador llamado `altonen` ha desarrollado una implementación en Rust de I2P llamada `emissary`. Aunque todavía es bastante nuevo, y Rust no nos resulta familiar, este intrigante proyecto es muy prometedor. Enhorabuena a altonen por crear `emissary`, estamos bastante impresionados.

### ¿Por qué el óxido?

La razón principal para usar Rust es básicamente la misma que para usar Java o Go. Rust es un lenguaje de programación compilado con gestión de memoria y una comunidad enorme y muy entusiasta. Rust también ofrece características avanzadas para producir bindings al lenguaje de programación C que pueden ser más fáciles de mantener que en otros lenguajes sin dejar de heredar las fuertes características de seguridad de memoria de Rust.

### ¿Quieres participar en `emissary`?

`emissary` está desarrollado en Github por `altonen`. Puedes encontrar el repositorio en: [altonen/emissary](https://github.com/altonen/emissary). Rust también adolece de una falta de bibliotecas cliente SAMv3 completas que sean compatibles con el material de red popular de Rust, escribir una biblioteca SAMv3 es un gran lugar para empezar.

## `go-i2p` está cada vez más cerca de completarse

Durante unos 3 años he estado trabajando en `go-i2p`, tratando de convertir una librería incipiente en un router I2P completo en pure-Go, otro lenguaje seguro en memoria. En los últimos 6 meses más o menos, se ha reestructurado drásticamente para mejorar el rendimiento, la fiabilidad y la facilidad de mantenimiento.

### ¿Por qué ir?

Aunque Rust y Go tienen muchas de las mismas ventajas, en muchos aspectos Go es mucho más sencillo de aprender. Desde hace años, existen excelentes bibliotecas y aplicaciones para utilizar I2P en el lenguaje de programación Go, incluidas las implementaciones más completas de las bibliotecas SAMv3.3. Pero sin un enrutador I2P que podamos gestionar automáticamente (como un enrutador integrado), sigue suponiendo una barrera para los usuarios. El objetivo de go-i2p es salvar esa distancia y eliminar todas las asperezas para los desarrolladores de aplicaciones I2P que trabajan en Go.

### ¿Quiere participar en `go-i2p`?

go-i2p` está desarrollado en Github, principalmente por `eyedeekay` en este momento y abierto a contribuciones de la comunidad en [go-i2p](https://github.com/go-i2p/). Dentro de este espacio de nombres existen muchos proyectos, tales como:

#### Bibliotecas de routers

Construimos estas librerías para producir nuestras librerías de routers I2P. Están repartidas en varios repositorios específicos para facilitar su revisión y hacerlas útiles a otras personas que quieran crear enrutadores I2P experimentales y personalizados.

- [go-i2p the router itself, most active right now](https://github.com/go-i2p/go-i2p)
- [common our core library for I2P datastructures](https://github.com/go-i2p/common)
- [crypto our library for cryptographic operations](https://github.com/go-i2p/crypto)
- [go-noise a library for implementing noise-based connections](https://github.com/go-i2p/go-noise)
- [noise a low-level library for using the Noise framework](https://github.com/go-i2p/noise)
- [su3 a library for manipulating su3 files](https://github.com/go-i2p/su3)

#### Bibliotecas de clientes

- [onramp a very convenient library for using(or combining) I2P and Tor](https://github.com/go-i2p/onramp)
- [go-sam-go an advanced, efficient, and very complete SAMv3 library](https://github.com/go-i2p/go-sam-go)

## Si no te gusta Go o Rust y estás pensando en escribir un router I2P, ¿qué deberías hacer?

Bueno hay un proyecto inactivo para escribir un [router I2P en C#](https://github.com/PeterZander/i2p-cs) si quieres ejecutar I2P en una XBox. Suena bastante bien en realidad. Si tampoco es tu preferencia, podrías hacer como hizo `altonen` y desarrollar uno completamente nuevo.

### Decide por qué lo escribes, para quién lo escribes

Puedes escribir un router I2P por cualquier motivo, es una red libre, pero te ayudará saber por qué. ¿Hay una comunidad a la que quieres potenciar, una herramienta que crees que encaja bien con I2P, o una estrategia que quieres probar? Averigua cuál es tu objetivo para saber por dónde tienes que empezar y qué aspecto tendrá un estado "acabado".

### Decide en qué lengua quieres hacerlo y por qué

He aquí algunas razones para elegir un idioma:

- **C**: No need for binding-generation, supported everywhere, can be called from any language, lingua franca of modern computing
- **Typescript**: Massive community, lots of applications, services, and libraries, works with `node` and `deno`, seems like it's everywhere right now
- **D**: It's memory safe and not Rust or Go
- **Vala**: It emits C code for the target platform, combining some of the advantages of memory-safe languages with the flexibility of C
- **Python**: Everybody uses Python

Pero he aquí algunas razones por las que podría no elegir esos idiomas:

- **C**: Memory management can be challenging, leading to impactful bugs
- **Typescript**: TypeScript is transpiled to JavaScript, which is interpreted and may impact performance
- **D**: Relatively small community
- **Vala**: Not a lot of underlying infrastructure in Vala, you end up using C versions of most libraries
- **Python**: It's an interpreted language which may impact performance

Hay cientos de lenguajes de programación y nos complace mantener bibliotecas y routers I2P en todos ellos. Elige bien tus opciones y empieza.

## Ponte en contacto y empieza a programar

Si quieres trabajar en Rust, Go, Java, C++ o algún otro lenguaje, ponte en contacto con nosotros en #i2p-dev en Irc2P. Empieza por ahí y te incorporaremos a los canales específicos del router. También estamos presentes en ramble.i2p en f/i2p, en reddit en r/i2p, y en GitHub y git.idk.i2p. Esperamos tener pronto noticias suyas.
