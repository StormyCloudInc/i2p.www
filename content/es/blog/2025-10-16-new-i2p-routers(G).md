---
title: "Nuevos Routers de I2P"
date: 2025-10-16
author: "idk"
categories: ["community"]
description: "Están surgiendo múltiples implementaciones nuevas del router I2P, incluyendo emissary en Rust y go-i2p en Go, aportando nuevas posibilidades para la integración y la diversidad de la red."
---

Es un momento emocionante para el desarrollo de I2P; nuestra comunidad está creciendo y ahora están apareciendo en escena varios nuevos prototipos de I2P router completamente funcionales. Estamos muy entusiasmados con este desarrollo y con poder compartir la noticia contigo.

## ¿Cómo ayuda esto a la red?

Escribir routers de I2P nos ayuda a demostrar que nuestros documentos de especificación pueden utilizarse para producir nuevos routers de I2P, abre el código a nuevas herramientas de análisis y, en general, mejora la seguridad y la interoperabilidad de la red. La existencia de múltiples routers de I2P significa que los posibles errores no son uniformes; un ataque contra un router puede no funcionar contra otro router, evitando un problema de monocultivo. Sin embargo, quizá la perspectiva más emocionante a largo plazo sea `embedding` (integración embebida).

## ¿Qué es `embedding`?

En el contexto de I2P, `embedding` es una forma de incluir un router de I2P directamente dentro de otra aplicación, sin requerir un router independiente ejecutándose en segundo plano. De este modo podemos hacer que I2P sea más fácil de usar, lo cual facilita el crecimiento de la red al hacer que el software sea más accesible. Tanto Java como C++ adolecen de ser difíciles de usar fuera de sus propios ecosistemas; en C++ se requieren enlaces (bindings) en C frágiles y escritos a mano y, en el caso de Java, está el dolor de comunicarse con una aplicación de la JVM desde una aplicación que no se ejecuta en la JVM.

Aunque en muchos aspectos esta situación es bastante normal, creo que puede mejorarse para que I2P sea más accesible. Otros lenguajes tienen soluciones más elegantes para estos problemas. Por supuesto, siempre debemos considerar y utilizar las directrices existentes para los routers de Java y C++.

## `emissary` aparece desde la oscuridad

Totalmente independiente de nuestro equipo, un desarrollador llamado `altonen` ha desarrollado una implementación de I2P en Rust llamada `emissary`. Aunque todavía es bastante nuevo y Rust no nos resulta familiar, este intrigante proyecto tiene un gran potencial. Felicitaciones a altonen por crear `emissary`, estamos muy impresionados.

### Why Rust?

La razón principal para usar Rust es, básicamente, la misma que para usar Java o Go. Rust es un lenguaje de programación compilado con gestión de memoria y una comunidad enorme y sumamente entusiasta. Rust también ofrece funcionalidades avanzadas para producir bindings (enlaces de interoperabilidad) al lenguaje de programación C, que pueden ser más fáciles de mantener que en otros lenguajes, sin dejar de heredar las sólidas características de seguridad de memoria de Rust.

### Do you want to get involved with `emissary`?

`emissary` es desarrollado en GitHub por `altonen`. Puede encontrar el repositorio en: [altonen/emissary](https://github.com/altonen/emissary). Rust también carece de bibliotecas cliente de SAMv3 integrales que sean compatibles con las herramientas de redes populares de Rust; escribir una biblioteca de SAMv3 es un excelente punto de partida.

## `go-i2p` is getting closer to completion

Desde hace unos 3 años he estado trabajando en `go-i2p`, intentando convertir una biblioteca incipiente en un router I2P totalmente funcional en Go puro, otro lenguaje con seguridad de memoria. En los últimos 6 meses aproximadamente, se ha reestructurado drásticamente para mejorar el rendimiento, la fiabilidad y la mantenibilidad.

### Why Go?

Aunque Rust y Go comparten muchas de las mismas ventajas, en muchos sentidos Go es mucho más sencillo de aprender. Durante años han existido excelentes bibliotecas y aplicaciones para usar I2P en el lenguaje de programación Go, incluidas las implementaciones más completas de las bibliotecas SAMv3.3. Pero sin un I2P router que podamos gestionar automáticamente (como un router embebido), sigue presentando una barrera para los usuarios. El objetivo de go-i2p es salvar esa brecha y eliminar todas las asperezas para los desarrolladores de aplicaciones I2P que trabajan en Go.

### ¿Por qué Rust?

`go-i2p` se desarrolla en Github, principalmente por `eyedeekay` en este momento y está abierto a contribuciones de la comunidad en [go-i2p](https://github.com/go-i2p/). Dentro de este espacio de nombres existen muchos proyectos, tales como:

#### Router Libraries

Construimos estas bibliotecas para crear nuestras bibliotecas del router de I2P. Están distribuidas en múltiples repositorios especializados para facilitar la revisión y hacerlas útiles para otras personas que quieran construir routers de I2P experimentales y personalizados.

- [go-i2p the router itself, most active right now](https://github.com/go-i2p/go-i2p)
- [common our core library for I2P datastructures](https://github.com/go-i2p/common)
- [crypto our library for cryptographic operations](https://github.com/go-i2p/crypto)
- [go-noise a library for implementing noise-based connections](https://github.com/go-i2p/go-noise)
- [noise a low-level library for using the Noise framework](https://github.com/go-i2p/noise)
- [su3 a library for manipulating su3 files](https://github.com/go-i2p/su3)

#### Client libraries

- [onramp a very convenient library for using(or combining) I2P and Tor](https://github.com/go-i2p/onramp)
- [go-sam-go an advanced, efficient, and very complete SAMv3 library](https://github.com/go-i2p/go-sam-go)

## If you don't like Go or Rust and are thinking of writing an I2P Router, what should you do?

Bueno, hay un proyecto inactivo para escribir un [I2P router en C#](https://github.com/PeterZander/i2p-cs) si quieres ejecutar I2P en una XBox. De hecho suena bastante bien. Si eso tampoco te convence, puedes hacer como `altonen` y desarrollar uno completamente nuevo.

### ¿Quieres participar en `emissary`?

Puedes desarrollar un I2P router por cualquier motivo, es una red libre, pero te ayudará saber por qué. ¿Hay alguna comunidad a la que quieras empoderar, una herramienta que consideres adecuada para I2P, o una estrategia que quieras probar? Define cuál es tu objetivo para determinar por dónde necesitas empezar y cómo se verá un estado "terminado".

### Decide what language you want to do it in and why

Estas son algunas razones por las que podrías elegir un idioma:

- **C**: No need for binding-generation, supported everywhere, can be called from any language, lingua franca of modern computing
- **Typescript**: Massive community, lots of applications, services, and libraries, works with `node` and `deno`, seems like it's everywhere right now
- **D**: It's memory safe and not Rust or Go
- **Vala**: It emits C code for the target platform, combining some of the advantages of memory-safe languages with the flexibility of C
- **Python**: Everybody uses Python

Pero aquí hay algunas razones por las que podrías no elegir esos idiomas:

- **C**: Memory management can be challenging, leading to impactful bugs
- **Typescript**: TypeScript is transpiled to JavaScript, which is interpreted and may impact performance
- **D**: Relatively small community
- **Vala**: Not a lot of underlying infrastructure in Vala, you end up using C versions of most libraries
- **Python**: It's an interpreted language which may impact performance

Hay cientos de lenguajes de programación y damos la bienvenida a bibliotecas de I2P mantenidas y routers en todos ellos. Elige sabiamente tus compromisos y empieza.

## `go-i2p` está cada vez más cerca de completarse

Ya sea que quieras trabajar en Rust, Go, Java, C++ u otro lenguaje, ponte en contacto con nosotros en #i2p-dev en Irc2P. Comienza allí, y te guiaremos hacia canales específicos del router. También estamos presentes en ramble.i2p en f/i2p, en reddit en r/i2p, y en GitHub y git.idk.i2p. Esperamos saber de ti pronto.
