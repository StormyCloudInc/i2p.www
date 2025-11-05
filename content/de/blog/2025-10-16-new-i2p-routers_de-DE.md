---
title: "New I2P Routers(t)"
date: 2025-10-16
author: "idk"
categories: ["community"]
description: "Multiple new I2P router implementations are emerging, including emissary in Rust and go-i2p in Go, bringing new possibilities for embedding and network diversity."
---

Es ist eine aufregende Zeit für die I2P-Entwicklung, unsere Community wächst und es gibt jetzt mehrere neue, voll funktionsfähige I2P-Router-Prototypen, die in der Szene auftauchen! Wir freuen uns sehr über diese Entwicklung und darüber, die Neuigkeiten mit Ihnen zu teilen.

## Wie hilft das dem Netzwerk?

Das Schreiben von I2P-Routern hilft uns zu beweisen, dass unsere Spezifikationsdokumente zur Herstellung neuer I2P-Router verwendet werden können, öffnet den Code für neue Analysetools und verbessert allgemein die Sicherheit und Interoperabilität des Netzwerks. Mehrere I2P-Router bedeuten, dass potenzielle Fehler nicht einheitlich sind. Ein Angriff auf einen Router funktioniert möglicherweise nicht auf einem anderen Router, wodurch ein Monokulturproblem vermieden wird. Die vielleicht aufregendste Perspektive auf lange Sicht ist jedoch die `Einbettung`.

## Was ist `Einbettung`?

Im Rahmen von I2P ist die `Einbettung` eine Möglichkeit, einen I2P-Router direkt in eine andere App einzubinden, ohne dass ein freistehender Router im Hintergrund läuft. Auf diese Weise können wir die Nutzung von I2P vereinfachen, was das Wachstum des Netzwerks erleichtert, indem wir die Software zugänglicher machen. Sowohl Java als auch C++ sind außerhalb ihrer eigenen Ökosysteme schwierig zu verwenden, wobei C++ spröde handschriftliche C-Bindungen erfordert und im Fall von Java der Schmerz der Kommunikation mit einer JVM-Anwendung aus einer Nicht-JVM-Anwendung.

Obwohl diese Situation in vielerlei Hinsicht ganz normal ist, glaube ich, dass sie verbessert werden kann, um I2P zugänglicher zu machen. Andere Sprachen haben elegantere Lösungen für diese Probleme. Natürlich sollten wir immer die bestehenden Richtlinien für die Java- und C++ -Router berücksichtigen und anwenden.

## `abgesandter` erscheint aus der Dunkelheit

Völlig unabhängig von unserem Team hat ein Entwickler `namens` altonen eine Rust-Implementierung von I2P namens `emissary` entwickelt. Es ist zwar noch recht neu und Rust ist uns unbekannt, aber dieses faszinierende Projekt ist vielversprechend. Herzlichen Glückwunsch an altonen zur Erstellung des `Abgesandten`, wir sind ziemlich beeindruckt.

### Warum Rost?

Der Hauptgrund für die Verwendung von Rust ist im Grunde derselbe wie der Grund für die Verwendung von Java oder Go. Rust ist eine kompilierte Programmiersprache mit Speicherverwaltung und einer riesigen, sehr enthusiastischen Community. Rust bietet auch erweiterte Funktionen zum Erstellen von Bindungen an die Programmiersprache C, die möglicherweise einfacher zu pflegen sind als in anderen Sprachen, während sie gleichzeitig die starken Speichersicherheitsfunktionen von Rust übernehmen.

### Möchtest du dich auf den `Abgesandten` einlassen?

`emissary` wird auf Github von altonen `entwickelt`. Sie finden das Repository unter: [altonen/emissary](https://github.com/altonen/emissary). Rust leidet auch unter einem Mangel an umfassenden SAMv3-Client-Bibliotheken, die mit den beliebten Rust-Netzwerkprodukten kompatibel sind. Das Schreiben einer SAMv3-Bibliothek ist ein großartiger Ausgangspunkt.

## `go-i2p` nähert sich der Fertigstellung

Seit etwa 3 Jahren arbeite ich an go-i2p und `versuche`, eine junge Bibliothek in einen vollwertigen I2P-Router in pure-Go, einer weiteren speichersicheren Sprache, zu verwandeln. In den letzten 6 Monaten wurde es drastisch umstrukturiert, um Leistung, Zuverlässigkeit und Wartbarkeit zu verbessern.

### Warum gehen?

Während Rust und Go viele der gleichen Vorteile haben, ist Go in vielerlei Hinsicht viel einfacher zu erlernen. Seit Jahren gibt es hervorragende Bibliotheken und Anwendungen für die Verwendung von I2P in der Programmiersprache Go, einschließlich der vollständigsten Implementierungen der SAMv3.3-Bibliotheken. Aber ohne einen I2P-Router, den wir automatisch verwalten können (z. B. einen eingebetteten Router), stellt es immer noch eine Barriere für die Benutzer dar. Der Punkt von go-i2p ist es, diese Lücke zu schließen und alle Ecken und Kanten für I2P-Anwendungsentwickler zu entfernen, die in Go arbeiten.

### Möchtest du dich auf go-i2p `einlassen`?

`go-i2p` wird auf Github entwickelt, zu diesem `Zeitpunkt` primär von eyedeekay und offen für Beiträge der Community bei [go-i2p](https://github.com/go-i2p/). Innerhalb dieses Namespace existieren viele Projekte, wie zum Beispiel:

#### Router-Bibliotheken

Wir haben diese Bibliotheken erstellt, um unsere I2P-Router-Bibliotheken zu produzieren. Sie sind auf mehrere, fokussierte Repositories verteilt, um die Überprüfung zu erleichtern und sie für andere Personen nützlich zu machen, die experimentelle, benutzerdefinierte I2P-Router erstellen möchten.

- [go-i2p der Router selbst, derzeit am aktivsten](https://github.com/go-i2p/go-i2p)
- [gemeinsame Kernbibliothek für I2P-Datenstrukturen](https://github.com/go-i2p/common)
- [krypto unsere Bibliothek für kryptographische Operationen](https://github.com/go-i2p/crypto)
- [go-noise eine Bibliothek zur Implementierung von geräuschbasierten Verbindungen](https://github.com/go-i2p/go-noise)
- [eine Low-Level-Bibliothek für die Verwendung des Noise-Frameworks](https://github.com/go-i2p/noise)
- [su3 eine Bibliothek zum Manipulieren von su3-Dateien](https://github.com/go-i2p/su3)

#### Kundenbibliotheken

- [onramp eine sehr praktische Bibliothek für die Verwendung(oder Kombination) von I2P und Tor](https://github.com/go-i2p/onramp)
- [go-sam-go eine fortschrittliche, effiziente und sehr vollständige SAMv3-Bibliothek](https://github.com/go-i2p/go-sam-go)

## Wenn Sie Go oder Rust nicht mögen und daran denken, einen I2P-Router zu schreiben, was sollten Sie tun?

Nun, es gibt ein ruhendes Projekt, um [einen I2P-Router in C#](https://github.com/PeterZander/i2p-cs) zu schreiben, wenn Sie I2P auf einer XBox ausführen möchten. Klingt eigentlich ziemlich ordentlich. Wenn das auch nicht deine Präferenz ist, könntest du es `wie` altonen machen und eine ganz neue entwickeln.

### Entscheide, warum du es schreibst, für wen du es schreibst

Sie können einen I2P-Router aus irgendeinem Grund schreiben, es ist ein kostenloses Netzwerk, aber es wird Ihnen helfen zu wissen, warum. Gibt es eine Community, die Sie stärken möchten, ein Tool, das Ihrer Meinung nach gut zu I2P passt, oder eine Strategie, die Sie ausprobieren möchten? Finden Sie heraus, was Ihr Ziel ist, um herauszufinden, wo Sie anfangen müssen, und wie ein "fertiger" Zustand aussehen wird.

### Entscheiden Sie, in welcher Sprache Sie es tun möchten und warum

Hier sind einige Gründe, warum Sie eine Sprache wählen könnten:

- **C**: No need for binding-generation, supported everywhere, can be called from any language, lingua franca of modern computing
- **Typescript**: Massive Community, viele Anwendungen, Dienste und Bibliotheken, arbeitet mit `Node` und `Deno`, scheint im Moment überall zu sein
- **D**: Es ist speichersicher und nicht Rust or Go
- **Vala**: Es gibt C-Code für die Zielplattform aus und kombiniert einige der Vorteile von speichersicheren Sprachen mit der Flexibilität von C
- **Python**: Jeder verwendet Python

Aber hier sind einige Gründe, warum Sie diese Sprachen möglicherweise nicht wählen:

- **C**: Speicherverwaltung kann eine Herausforderung sein, die zu wirkungsvollen Fehlern führt
- **Typescript**: TypeScript wird in JavaScript transpiliert, was interpretiert wird und die Leistung beeinträchtigen kann
- **D**: Relativ kleine Gemeinschaft
- **Vala**: Nicht viel zugrunde liegende Infrastruktur in Vala, Sie verwenden am Ende C-Versionen der meisten Bibliotheken
- **Python**: Es ist eine interpretierte Sprache, die sich auf die Leistung auswirken kann

Es gibt Hunderte von Programmiersprachen und wir begrüßen gewartete I2P-Bibliotheken und Router in allen. Wählen Sie Ihre Kompromisse mit Bedacht und beginnen Sie.

## Kontaktieren Sie uns und beginnen Sie mit der Programmierung

Egal, ob Sie in Rust, Go, Java, C++ oder einer anderen Sprache arbeiten möchten, kontaktieren Sie uns unter #i2p-dev auf Irc2P. Beginnen Sie dort, und wir werden Sie zu routerspezifischen Kanälen einbinden. Wir sind auch auf ramble.i2p bei f/i2p, auf reddit bei r/i2p und auf GitHub und git.idk.i2p präsent. Wir freuen uns, bald von Ihnen zu hören.
