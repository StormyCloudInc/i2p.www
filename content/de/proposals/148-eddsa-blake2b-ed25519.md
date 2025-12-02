---
title: "RedDSA-BLAKE2b-Ed25519"
number: "148"
author: "zzz"
created: "2019-03-12"
lastupdated: "2019-04-11"
status: "Öffnen"
thread: "http://zzz.i2p/topics/2689"
toc: true
---

## Übersicht

Dieser Vorschlag fügt einen neuen Signaturtyp hinzu, der BLAKE2b-512 mit Personalisierungsstrings und Salts verwendet, um SHA-512 zu ersetzen. Dies wird drei Klassen möglicher Angriffe eliminieren.

## Motivation

Während der Diskussionen und des Designs von NTCP2 (Vorschlag 111) und LS2 (Vorschlag 123) haben wir verschiedene mögliche Angriffe kurz betrachtet und wie man sie verhindern kann. Drei dieser Angriffe sind Length Extension Attacks, Cross-Protocol Attacks und Duplicate Message Identification.

Sowohl für NTCP2 als auch für LS2 entschieden wir, dass diese Angriffe nicht direkt relevant für die vorliegenden Vorschläge waren, und jegliche Lösungen standen im Konflikt mit dem Ziel, neue Primitive zu minimieren. Außerdem stellten wir fest, dass die Geschwindigkeit der Hash-Funktionen in diesen Protokollen kein wichtiger Faktor für unsere Entscheidungen war. Daher vertagten wir die Lösung größtenteils auf einen separaten Vorschlag. Obwohl wir der LS2-Spezifikation einige Personalisierungsfunktionen hinzufügten, erforderten wir keine neuen Hash-Funktionen.

Viele Projekte, wie [ZCash](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf), verwenden Hash-Funktionen und Signaturalgorithmen, die auf neueren Algorithmen basieren, welche nicht anfällig für die folgenden Angriffe sind.

### Length Extension Attacks

SHA-256 und SHA-512 sind anfällig für [Length Extension Attacks (LEA)](https://en.wikipedia.org/wiki/Length_extension_attack). Dies ist der Fall, wenn tatsächliche Daten signiert werden, nicht der Hash der Daten. In den meisten I2P-Protokollen (Streaming, Datagrams, netDb und andere) werden die tatsächlichen Daten signiert. Eine Ausnahme sind SU3-Dateien, bei denen der Hash signiert wird. Die andere Ausnahme sind signierte Datagrams für DSA (Sig-Typ 0) nur, bei denen der Hash signiert wird. Für andere signierte Datagram-Sig-Typen werden die Daten signiert.

### Cross-Protocol Attacks

Signierte Daten in I2P-Protokollen können aufgrund fehlender Domain-Separation anfällig für Cross-Protocol Attacks (CPA) sein. Dies ermöglicht es einem Angreifer, Daten, die in einem Kontext empfangen wurden (wie ein signiertes Datagramm), zu verwenden und sie als gültige, signierte Daten in einem anderen Kontext (wie Streaming oder Netzwerkdatenbank) zu präsentieren. Obwohl es unwahrscheinlich ist, dass die signierten Daten aus einem Kontext als gültige Daten in einem anderen Kontext geparst würden, ist es schwierig oder unmöglich, alle Situationen zu analysieren, um sicher zu wissen. Zusätzlich könnte es in manchen Kontexten für einen Angreifer möglich sein, ein Opfer dazu zu bringen, speziell präparierte Daten zu signieren, die gültige Daten in einem anderen Kontext sein könnten. Auch hier ist es schwierig oder unmöglich, alle Situationen zu analysieren, um sicher zu wissen.

### Length Extension Attacks

I2P-Protokolle können anfällig für Duplicate Message Identification (DMI) sein. Dies könnte es einem Angreifer ermöglichen zu identifizieren, dass zwei signierte Nachrichten den gleichen Inhalt haben, auch wenn diese Nachrichten und ihre Signaturen verschlüsselt sind. Obwohl dies aufgrund der in I2P verwendeten Verschlüsselungsmethoden unwahrscheinlich ist, ist es schwierig oder unmöglich, alle Situationen zu analysieren, um sicher zu wissen. Durch die Verwendung einer Hash-Funktion, die eine Methode zum Hinzufügen eines zufälligen Salts bereitstellt, werden alle Signaturen unterschiedlich sein, auch wenn dieselben Daten signiert werden. Während Red25519 wie in Vorschlag 123 definiert einen zufälligen Salt zur Hash-Funktion hinzufügt, löst dies das Problem für unverschlüsselte leaseSets nicht.

### Cross-Protokoll-Angriffe

Obwohl dies nicht die primäre Motivation für diesen Vorschlag ist, ist SHA-512 relativ langsam, und schnellere Hash-Funktionen sind verfügbar.

## Goals

- Verhindere oben genannte Angriffe
- Minimiere die Verwendung neuer kryptographischer Primitive
- Verwende bewährte, standardisierte kryptographische Primitive
- Verwende Standardkurven
- Verwende schnellere Primitive, falls verfügbar

## Design

Modifizieren Sie den bestehenden RedDSA_SHA512_Ed25519 Signaturtyp, um BLAKE2b-512 anstelle von SHA-512 zu verwenden. Fügen Sie eindeutige Personalisierungszeichenfolgen für jeden Anwendungsfall hinzu. Der neue Signaturtyp kann sowohl für unblinded als auch blinded leasesets verwendet werden.

## Justification

- [BLAKE2b](https://blake2.net/blake2.pdf) ist nicht anfällig für LEA.
- BLAKE2b bietet eine Standardmethode zum Hinzufügen von Personalisierungsstrings für Domain-Separation
- BLAKE2b bietet eine Standardmethode zum Hinzufügen eines zufälligen Salts zur Verhinderung von DMI.
- BLAKE2b ist schneller als SHA-256 und SHA-512 (und MD5) auf moderner Hardware,
  laut der [BLAKE2-Spezifikation](https://blake2.net/blake2.pdf).
- Ed25519 ist immer noch unser schnellster Signaturtyp, viel schneller als ECDSA, zumindest in Java.
- [Ed25519](http://cr.yp.to/papers.html#ed25519) erfordert eine 512-Bit-kryptographische Hash-Funktion.
  Es spezifiziert nicht SHA-512. BLAKE2b ist genauso geeignet für die Hash-Funktion.
- BLAKE2b ist weit verbreitet in Bibliotheken für viele Programmiersprachen verfügbar, wie zum Beispiel Noise.

## Specification

Verwenden Sie unkeyed BLAKE2b-512 wie in der [BLAKE2-Spezifikation](https://blake2.net/blake2.pdf) mit Salt und Personalisierung. Alle Verwendungen von BLAKE2b-Signaturen werden eine 16-Zeichen-Personalisierungszeichenkette verwenden.

Bei der Verwendung beim RedDSA_BLAKE2b_Ed25519-Signieren ist ein zufälliges Salt erlaubt, jedoch nicht notwendig, da der Signaturalgorithmus 80 Bytes an Zufallsdaten hinzufügt (siehe Vorschlag 123). Falls gewünscht, setzen Sie beim Hashen der Daten zur Berechnung von r ein neues BLAKE2b 16-Byte-Zufalls-Salt für jede Signatur. Bei der Berechnung von S setzen Sie das Salt auf den Standard von Null-Bytes zurück.

Bei der Verwendung in RedDSA_BLAKE2b_Ed25519-Verifikation kein zufälliges Salt verwenden, sondern die Standardeinstellung aus lauter Nullen verwenden.

Die Salt- und Personalization-Features sind nicht in [RFC 7693](https://tools.ietf.org/html/rfc7693) spezifiziert; verwenden Sie diese Features wie in der [BLAKE2-Spezifikation](https://blake2.net/blake2.pdf) angegeben.

### Erkennung doppelter Nachrichten

Für RedDSA_BLAKE2b_Ed25519 ersetze die SHA-512 Hash-Funktion in RedDSA_SHA512_Ed25519 (Signaturtyp 11, wie in Proposal 123 definiert) durch BLAKE2b-512. Keine anderen Änderungen.

Wir benötigen keinen Ersatz für EdDSA_SHA512_Ed25519ph (Signaturtyp 8) für su3-Dateien, da die vorab-gehashte Version von EdDSA nicht anfällig für LEA ist. EdDSA_SHA512_Ed25519 (Signaturtyp 7) wird für su3-Dateien nicht unterstützt.

| Type | Type Code | Since | Usage |
|------|-----------|-------|-------|
| RedDSA_BLAKE2b_Ed25519 | 12 | TBD | For Router Identities, Destinations and encrypted leasesets only; never used for Router Identities |
### Geschwindigkeit

Das Folgende gilt für den neuen Signaturtyp.

| Data Type | Length |
|-----------|--------|
| Hash | 64 |
| Private Key | 32 |
| Public Key | 32 |
| Signature | 64 |
### Personalizations

Um eine Domänen-Trennung für die verschiedenen Verwendungen von Signaturen zu gewährleisten, werden wir die BLAKE2b-Personalisierungsfunktion verwenden.

Alle Verwendungen von BLAKE2b-Signaturen verwenden eine 16-Zeichen-Personalisierungszeichenfolge. Alle neuen Verwendungen müssen in die Tabelle hier aufgenommen werden, mit einer eindeutigen Personalisierung.

Der NTCP 1 und SSU Handshake verwendet unten stehende für die signierten Daten, die im Handshake selbst definiert sind. Signierte RouterInfos in DatabaseStore Messages verwenden die NetDb Entry Personalisierung, genau wie wenn sie in der NetDB gespeichert wären.

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
## Ziele

## Design

- Alternative 1: Proposal 146;
  Bietet LEA-Resistenz
- Alternative 2: [Ed25519ctx in RFC 8032](https://tools.ietf.org/html/rfc8032);
  Bietet LEA-Resistenz und Personalisierung.
  Standardisiert, aber nutzt es überhaupt jemand?
  Siehe [RFC 8032](https://tools.ietf.org/html/rfc8032) und [diese Diskussion](https://moderncrypto.org/mail-archive/curves/2017/000925.html).
- Ist "keyed" Hashing für uns nützlich?

## Begründung

Das gleiche wie bei der Einführung vorheriger Signaturtypen.

Wir planen, neue Router vom Typ 7 standardmäßig auf Typ 12 zu ändern. Wir planen, bestehende Router schließlich von Typ 7 auf Typ 12 zu migrieren, unter Verwendung des "Rekeying"-Prozesses, der nach der Einführung von Typ 7 verwendet wurde. Wir planen, neue Destinations vom Typ 7 standardmäßig auf Typ 12 zu ändern. Wir planen, neue verschlüsselte Destinations vom Typ 11 standardmäßig auf Typ 13 zu ändern.

Wir werden Blinding von den Typen 7, 11 und 12 zu Typ 12 unterstützen. Wir werden kein Blinding von Typ 12 zu Typ 11 unterstützen.

Neue Router könnten nach einigen Monaten standardmäßig den neuen Signaturtyp verwenden. Neue Ziele könnten nach etwa einem Jahr standardmäßig den neuen Signaturtyp verwenden.

Für die minimale Router-Version 0.9.TBD müssen Router sicherstellen:

- Speichere (oder überflute) keine RI oder LS mit dem neuen sig type an router mit einer Version kleiner als 0.9.TBD.
- Beim Verifizieren eines netDb store, hole keine RI oder LS mit dem neuen sig type von routern mit einer Version kleiner als 0.9.TBD.
- Router mit einem neuen sig type in ihrer RI können sich möglicherweise nicht mit routern mit einer Version kleiner als 0.9.TBD verbinden,
  weder mit NTCP, NTCP2, noch mit SSU.
- Streaming-Verbindungen und signierte Datagramme funktionieren nicht zu routern mit einer Version kleiner als 0.9.TBD,
  aber es gibt keine Möglichkeit das zu wissen, daher sollte der neue sig type für einen Zeitraum
  von Monaten oder Jahren nach der Veröffentlichung von 0.9.TBD nicht standardmäßig verwendet werden.
