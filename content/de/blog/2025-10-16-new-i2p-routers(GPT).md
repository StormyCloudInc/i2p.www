---
title: "Neue I2P Router(G)"
date: 2025-10-16
author: "idk"
categories: ["community"]
description: "Mehrere neue I2P router-Implementierungen entstehen, darunter emissary in Rust und go-i2p in Go, die neue Möglichkeiten für das Einbetten und die Netzwerkvielfalt eröffnen."
---

Es ist eine aufregende Zeit für die I2P-Entwicklung, unsere Community wächst, und es treten nun mehrere neue, voll funktionsfähige I2P router-Prototypen in Erscheinung! Wir freuen uns sehr über diese Entwicklung und darauf, die Neuigkeiten mit Ihnen zu teilen.

## Wie hilft das dem Netzwerk?

Die Implementierung von I2P routers hilft uns nachzuweisen, dass unsere Spezifikationsdokumente zur Erstellung neuer I2P routers verwendet werden können, macht den Code für neue Analysewerkzeuge zugänglich und verbessert allgemein die Sicherheit und Interoperabilität des Netzwerks. Mehrere I2P routers bedeuten, dass potenzielle Fehler nicht einheitlich sind; ein Angriff auf einen router funktioniert möglicherweise auf einem anderen router nicht, wodurch ein Monokultur-Problem vermieden wird. Die vielleicht spannendste Perspektive auf lange Sicht ist jedoch `embedding`.

## Was ist `embedding`?
Im Kontext von I2P ist `embedding` eine Möglichkeit, einen I2P router direkt in eine andere App einzubinden, ohne einen eigenständigen router zu benötigen, der im Hintergrund läuft. Auf diese Weise können wir I2P leichter nutzbar machen, was das Wachstum des Netzwerks erleichtert, indem die Software zugänglicher wird. Sowohl Java als auch C++ leiden darunter, außerhalb ihrer jeweiligen Ökosysteme schwer nutzbar zu sein; C++ erfordert fragile, handgeschriebene C-Bindings, und im Fall von Java entsteht die Mühsal, aus einer Nicht-JVM-Anwendung mit einer JVM-Anwendung zu kommunizieren.

Obwohl diese Situation in vielerlei Hinsicht ganz normal ist, glaube ich, dass sie verbessert werden kann, um I2P zugänglicher zu machen. Andere Sprachen haben für diese Probleme elegantere Lösungen. Natürlich sollten wir stets die bestehenden Richtlinien für die Java- und C++ routers berücksichtigen und verwenden.

## `emissary` erscheint aus der Dunkelheit

Völlig unabhängig von unserem Team hat ein Entwickler namens `altonen` eine Rust-Implementierung von I2P mit dem Namen `emissary` entwickelt. Obwohl es noch recht neu ist und uns Rust noch nicht vertraut ist, hat dieses spannende Projekt großes Potenzial. Glückwunsch an altonen zur Erstellung von `emissary`, wir sind sehr beeindruckt.

### Why Rust?

Der Hauptgrund, Rust zu verwenden, ist im Wesentlichen derselbe wie der Grund, Java oder Go zu verwenden. Rust ist eine kompilierte Programmiersprache mit Speicherverwaltung und einer riesigen, äußerst engagierten Community. Außerdem bietet Rust fortgeschrittene Funktionen zur Erstellung von Bindings (Sprachbindungen) für die Programmiersprache C, die möglicherweise leichter zu warten sind als in anderen Sprachen, wobei sie zugleich Rusts starke Speichersicherheit erben.

### Do you want to get involved with `emissary`?

`emissary` wird auf GitHub von `altonen` entwickelt. Sie finden das Repository unter: [altonen/emissary](https://github.com/altonen/emissary). Rust leidet zudem unter einem Mangel an umfassenden SAMv3-Client-Bibliotheken, die mit beliebten Rust-Netzwerkbibliotheken kompatibel sind; eine SAMv3-Bibliothek zu schreiben, ist ein hervorragender Einstieg.

## `go-i2p` is getting closer to completion

Seit etwa 3 Jahren arbeite ich an `go-i2p` und versuche, eine noch junge Bibliothek in einen vollwertigen I2P router in reinem Go, einer speichersicheren Sprache, zu verwandeln. In den vergangenen etwa 6 Monaten wurde es grundlegend umstrukturiert, um Leistung, Zuverlässigkeit und Wartbarkeit zu verbessern.

### Why Go?

Obwohl Rust und Go viele derselben Vorteile haben, ist Go in vielerlei Hinsicht wesentlich einfacher zu erlernen. Seit Jahren gibt es hervorragende Bibliotheken und Anwendungen zur Nutzung von I2P in der Programmiersprache Go, einschließlich der vollständigsten Implementierungen von SAMv3.3. Ohne einen I2P router, den wir automatisch verwalten können (wie etwa einen embedded router (eingebetteter Router)), stellt dies für Benutzer jedoch weiterhin eine Hürde dar. Ziel von go-i2p ist es, diese Lücke zu schließen und alle Stolpersteine für I2P‑Anwendungsentwickler, die in Go arbeiten, zu beseitigen.

### Warum Rust?

`go-i2p` wird auf Github entwickelt, derzeit hauptsächlich von `eyedeekay`, und ist für Beiträge aus der Community unter [go-i2p](https://github.com/go-i2p/) offen. Innerhalb dieses Namensraums existieren viele Projekte, wie zum Beispiel:

#### Router Libraries

Wir haben diese Bibliotheken entwickelt, um unsere Bibliotheken für I2P router zu erstellen. Sie sind auf mehrere spezialisierte Repositories verteilt, um Code-Reviews zu erleichtern und sie für andere nützlich zu machen, die experimentelle, maßgeschneiderte I2P routers bauen möchten.

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

Translation:
Nun, es gibt ein inaktives Projekt, um einen [I2P router in C#](https://github.com/PeterZander/i2p-cs) zu schreiben, falls du I2P auf einer XBox laufen lassen willst. Klingt eigentlich ziemlich cool. Wenn dir das auch nicht zusagt, könntest du es so machen wie `altonen` und gleich einen komplett neuen entwickeln.

### Möchten Sie sich an `emissary` beteiligen?

Sie können aus jedem beliebigen Grund einen I2P router entwickeln – es ist ein freies Netzwerk –, aber es hilft, wenn Sie wissen, warum. Gibt es eine Community, die Sie stärken möchten, ein Tool, das Ihrer Meinung nach gut zu I2P passt, oder eine Strategie, die Sie ausprobieren möchten? Definieren Sie Ihr Ziel, um daraus abzuleiten, wo Sie beginnen müssen und wie ein "fertiger" Zustand aussehen wird.

### Decide what language you want to do it in and why

Hier sind einige Gründe, warum Sie sich für eine Sprache entscheiden könnten:

Übersetzung:

- **C**: No need for binding-generation, supported everywhere, can be called from any language, lingua franca of modern computing
- **Typescript**: Massive community, lots of applications, services, and libraries, works with `node` and `deno`, seems like it's everywhere right now
- **D**: It's memory safe and not Rust or Go
- **Vala**: It emits C code for the target platform, combining some of the advantages of memory-safe languages with the flexibility of C
- **Python**: Everybody uses Python

Aber hier sind einige Gründe, warum Sie diese Sprachen möglicherweise nicht wählen:

Übersetzung:

- **C**: Memory management can be challenging, leading to impactful bugs
- **Typescript**: TypeScript is transpiled to JavaScript, which is interpreted and may impact performance
- **D**: Relatively small community
- **Vala**: Not a lot of underlying infrastructure in Vala, you end up using C versions of most libraries
- **Python**: It's an interpreted language which may impact performance

Es gibt Hunderte von Programmiersprachen, und wir begrüßen aktiv gepflegte I2P-Bibliotheken und routers in allen Sprachen. Treffen Sie Ihre Kompromisse mit Bedacht und legen Sie los.

## `go-i2p` rückt der Fertigstellung näher

Ob du in Rust, Go, Java, C++ oder einer anderen Sprache arbeiten möchtest, melde dich bei uns im #i2p-dev auf Irc2P. Starte dort, und wir führen dich in router-spezifische Kanäle ein. Wir sind außerdem auf ramble.i2p unter f/i2p, auf reddit unter r/i2p sowie auf GitHub und git.idk.i2p vertreten. Wir freuen uns darauf, bald von dir zu hören.
