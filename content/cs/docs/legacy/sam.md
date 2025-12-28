---
title: "SAM v1"
description: "Starší protokol Simple Anonymous Messaging (jednoduché anonymní zasílání zpráv) (zastaralý)"
slug: "sam"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **Zastaralé:** SAM v1 je zachován pouze pro historické účely. Nové aplikace by měly používat [SAM v3](/docs/api/samv3/) nebo [BOB](/docs/legacy/bob/). Původní bridge (překlenovací služba) podporuje pouze destinace DSA-SHA1 a omezenou sadu možností.

## Knihovny

Strom zdrojových kódů Java I2P stále obsahuje zastaralé jazykové vazby pro C, C#, Perl a Python. Už nejsou udržovány a jsou distribuovány hlavně kvůli archivní kompatibilitě.

## Vyjednávání verze

Klienti se připojují přes TCP (výchozí `127.0.0.1:7656`) a vyměňují si:

```
Client → HELLO VERSION MIN=1 MAX=1
Bridge → HELLO REPLY RESULT=OK VERSION=1.0
```
Od verze Java I2P 0.9.14 je parametr `MIN` volitelný a jak `MIN`, tak `MAX` přijímají jednociferné zápisy (`"3"` apod.) pro aktualizované bridges (mosty).

## Vytvoření relace

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]*
```
- `DESTINATION=name` načte nebo vytvoří záznam v `sam.keys`; `TRANSIENT` vždy vytvoří dočasnou destination (cílovou identitu).
- `STYLE` vybírá virtuální streamy (podobné TCP), podepsané datagramy nebo surové datagramy.
- `DIRECTION` platí pouze pro streamové relace; výchozí hodnota je `BOTH`.
- Další páry klíč/hodnota se předávají jako volby I2CP (například `tunnels.quantityInbound=3`).

Most odpoví:

```
SESSION STATUS RESULT=OK DESTINATION=name
```
Chyby vracejí `DUPLICATED_DEST`, `I2P_ERROR` nebo `INVALID_KEY` spolu s volitelnou zprávou.

## Formáty zpráv

Zprávy SAM jsou jednořádkové ASCII a obsahují dvojice klíč/hodnota oddělené mezerami. Klíče jsou v UTF‑8; hodnoty mohou být uzavřeny do uvozovek, pokud obsahují mezery. Není definováno žádné escaping (nahrazování speciálních znaků únikovými sekvencemi).

Typy komunikace:

- **Streamy** – zprostředkované přes I2P streaming library (knihovna pro streamování v I2P)
- **Datagramy s možností odpovědi** – podepsaná data (Datagram1)
- **Surové datagramy** – nepodepsaná data (Datagram RAW)

## Možnosti přidané ve verzi 0.9.14

- `DEST GENERATE` přijímá `SIGNATURE_TYPE=...` (umožňuje Ed25519 apod.)
- `HELLO VERSION` považuje `MIN` za volitelný a přijímá jednociferné řetězce verzí

## Kdy použít SAM v1

Pouze pro zajištění interoperability se starším softwarem, který nelze aktualizovat. Pro veškerý nový vývoj používejte:

- [SAM v3](/docs/api/samv3/) pro plnohodnotný přístup ke streamům/datagramům
- [BOB](/docs/legacy/bob/) pro správu destinací (stále omezený, ale podporuje modernější funkce)

## Reference

- [SAM v2](/docs/legacy/samv2/)
- [SAM v3](/docs/api/samv3/)
- [Specifikace datagramů](/docs/api/datagrams/)
- [Streamovací protokol](/spec/api/streaming/)

SAM v1 položil základy vývoje aplikací nezávislých na routeru, ale ekosystém se posunul dál. Považujte tento dokument spíše za pomůcku pro zajištění kompatibility než za výchozí bod.
