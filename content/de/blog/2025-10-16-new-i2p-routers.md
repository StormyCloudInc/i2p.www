---
title: "Neue I2P-Router(D)"
date: 2025-10-16
author: "idk"
categories: ["community"]
description: "Mehrere neue I2P-Router-Implementierungen sind im Entstehen begriffen, darunter emissary in Rust und go-i2p in Go, die neue Möglichkeiten für die Einbettung und Netzwerkvielfalt bieten."
---


Es ist eine aufregende Zeit für die I2P-Entwicklung, unsere Community wächst und es gibt nun mehrere neue, voll funktionsfähige I2P-Router-Prototypen, die in der Szene auftauchen! Wir freuen uns sehr über diese Entwicklung und darüber, diese Neuigkeiten mit Ihnen zu teilen.

## Wie hilft dies dem Netz?

Das Schreiben von I2P-Routern hilft uns zu beweisen, dass unsere Spezifikationsdokumente verwendet werden können, um neue I2P-Router zu erstellen, öffnet den Code für neue Analysetools und verbessert allgemein die Sicherheit und Interoperabilität des Netzwerks. Mehrere I2P-Router bedeuten, dass potentielle Bugs nicht einheitlich sind, ein Angriff auf einen Router funktioniert möglicherweise nicht auf einem anderen Router, wodurch das Problem der Monokultur vermieden wird. Die vielleicht aufregendste Aussicht auf lange Sicht ist jedoch das "Einbetten".

## Was ist "Einbetten"?

Im Kontext von I2P ist `Embedding` eine Möglichkeit, einen I2P-Router direkt in eine andere Anwendung einzubinden, ohne dass ein eigenständiger Router im Hintergrund laufen muss. Dies ist ein Weg, I2P einfacher zu machen, was das Netzwerk einfacher wachsen lässt, indem die Software zugänglicher gemacht wird. Sowohl Java als auch C++ leiden darunter, dass sie außerhalb ihrer eigenen Ökosysteme schwer zu benutzen sind, wobei C++ spröde handgeschriebene C-Bindungen erfordert und im Falle von Java die Kommunikation mit einer JVM-Anwendung von einer Nicht-JVM-Anwendung aus schwierig ist.

Obwohl diese Situation in vielerlei Hinsicht ganz normal ist, glaube ich, dass sie verbessert werden kann, um I2P zugänglicher zu machen. Andere Sprachen haben elegantere Lösungen für diese Probleme. Natürlich sollten wir immer die bestehenden Richtlinien für die Java- und C++-Router berücksichtigen und nutzen.

## Abgesandter" erscheint aus der Dunkelheit

Völlig unabhängig von unserem Team hat ein Entwickler namens `altonen` eine Rust-Implementierung von I2P namens `emissary` entwickelt. Obwohl es noch recht neu ist, und Rust uns nicht vertraut ist, ist dieses faszinierende Projekt sehr vielversprechend. Herzlichen Glückwunsch an altonen für die Entwicklung von `emissary`, wir sind sehr beeindruckt.

### Warum Rost?

Der Hauptgrund, Rust zu verwenden, ist im Grunde derselbe wie der Grund, Java oder Go zu verwenden. Rust ist eine kompilierte Programmiersprache mit Speicherverwaltung und einer großen, sehr enthusiastischen Gemeinschaft. Rust bietet auch fortschrittliche Funktionen für die Erstellung von Bindungen an die Programmiersprache C, die einfacher zu pflegen sind als in anderen Sprachen, während sie gleichzeitig die starken Speichersicherheitsfunktionen von Rust übernehmen.

### Möchten Sie sich an `emissary` beteiligen?

`emissary` wird auf Github von `altonen` entwickelt. Sie können das Repository finden unter: [altonen/emissary](https://github.com/altonen/emissary). Rust leidet auch unter einem Mangel an umfassenden SAMv3-Client-Bibliotheken, die mit populären Rust-Netzwerken kompatibel sind; das Schreiben einer SAMv3-Bibliothek ist ein guter Anfang.

## go-i2p" nähert sich der Fertigstellung

Seit etwa 3 Jahren arbeite ich an `go-i2p` und versuche, eine junge Bibliothek in einen vollwertigen I2P-Router in pure-Go, einer anderen speichersicheren Sprache, zu verwandeln. In den letzten 6 Monaten oder so wurde sie drastisch umstrukturiert, um die Leistung, Zuverlässigkeit und Wartbarkeit zu verbessern.

### Warum gehen?

Während Rust und Go viele der gleichen Vorteile haben, ist Go in vielerlei Hinsicht viel einfacher zu erlernen. Seit Jahren gibt es hervorragende Bibliotheken und Anwendungen für die Verwendung von I2P in der Programmiersprache Go, einschließlich der vollständigsten Implementierungen der SAMv3.3 Bibliotheken. Aber ohne einen I2P-Router, den wir automatisch verwalten können (wie z.B. einen eingebetteten Router), stellt es immer noch eine Barriere für die Benutzer dar. Das Ziel von go-i2p ist es, diese Lücke zu überbrücken und alle Ecken und Kanten für I2P-Anwendungsentwickler, die in Go arbeiten, zu beseitigen.

### Möchten Sie sich an "go-i2p" beteiligen?

`go-i2p` wird auf Github entwickelt, derzeit hauptsächlich von `eyedeekay`, und ist offen für Beiträge der Community unter [go-i2p] (https://github.com/go-i2p/). Innerhalb dieses Namensraumes existieren viele Projekte, wie z.B.:

#### Router-Bibliotheken

Wir haben diese Bibliotheken entwickelt, um unsere I2P-Router-Bibliotheken zu erstellen. Sie sind in mehrere Repositories aufgeteilt, um die Überprüfung zu erleichtern und sie für andere Leute nützlich zu machen, die experimentelle, benutzerdefinierte I2P-Router bauen wollen.

- [go-i2p the router itself, most active right now](https://github.com/go-i2p/go-i2p)
- [common our core library for I2P datastructures](https://github.com/go-i2p/common)
- [crypto our library for cryptographic operations](https://github.com/go-i2p/crypto)
- [go-noise a library for implementing noise-based connections](https://github.com/go-i2p/go-noise)
- [noise a low-level library for using the Noise framework](https://github.com/go-i2p/noise)
- [su3 a library for manipulating su3 files](https://github.com/go-i2p/su3)

#### Client-Bibliotheken

- [onramp a very convenient library for using(or combining) I2P and Tor](https://github.com/go-i2p/onramp)
- [go-sam-go an advanced, efficient, and very complete SAMv3 library](https://github.com/go-i2p/go-sam-go)

## Wenn Sie weder Go noch Rust mögen und daran denken, einen I2P-Router zu schreiben, was sollten Sie dann tun?

Nun, es gibt ein ruhendes Projekt, um einen [I2P-Router in C#] (https://github.com/PeterZander/i2p-cs) zu schreiben, wenn man I2P auf einer XBox laufen lassen möchte. Klingt eigentlich ganz nett. Wenn das auch nicht deine Vorliebe ist, könntest du es wie `altonen` machen und einen ganz neuen Router entwickeln.

### Entscheiden Sie, warum Sie ihn schreiben, für wen Sie ihn schreiben

Sie können einen I2P-Router aus jedem beliebigen Grund schreiben, es ist ein freies Netzwerk, aber es wird Ihnen helfen zu wissen, warum. Gibt es eine Gemeinschaft, die Sie unterstützen wollen, ein Tool, von dem Sie denken, dass es gut zu I2P passt, oder eine Strategie, die Sie ausprobieren wollen? Finden Sie heraus, was Ihr Ziel ist, um herauszufinden, wo Sie anfangen müssen und wie ein "fertiger" Zustand aussehen wird.

### Entscheiden Sie, in welcher Sprache Sie es machen wollen und warum

Hier sind einige Gründe, warum Sie eine Sprache wählen sollten:

- **C**: No need for binding-generation, supported everywhere, can be called from any language, lingua franca of modern computing
- **Typescript**: Massive community, lots of applications, services, and libraries, works with `node` and `deno`, seems like it's everywhere right now
- **D**: It's memory safe and not Rust or Go
- **Vala**: It emits C code for the target platform, combining some of the advantages of memory-safe languages with the flexibility of C
- **Python**: Everybody uses Python

Aber hier sind einige Gründe, warum Sie diese Sprachen nicht wählen sollten:

- **C**: Memory management can be challenging, leading to impactful bugs
- **Typescript**: TypeScript is transpiled to JavaScript, which is interpreted and may impact performance
- **D**: Relatively small community
- **Vala**: Not a lot of underlying infrastructure in Vala, you end up using C versions of most libraries
- **Python**: It's an interpreted language which may impact performance

Es gibt hunderte von Programmiersprachen und wir begrüßen es, wenn I2P-Bibliotheken und -Router in allen von ihnen gepflegt werden. Wählen Sie Ihre Kompromisse weise und beginnen Sie.

## Kontakt aufnehmen und mit dem Programmieren beginnen

Egal ob Sie in Rust, Go, Java, C++ oder einer anderen Sprache arbeiten wollen, kontaktieren Sie uns unter #i2p-dev auf Irc2P. Beginnen Sie dort, und wir werden Sie in die Router-spezifischen Kanäle aufnehmen. Wir sind auch auf ramble.i2p unter f/i2p, auf reddit unter r/i2p, und auf GitHub und git.idk.i2p vertreten. Wir freuen uns darauf, bald von Ihnen zu hören.
