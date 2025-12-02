---
title: "RedDSA-BLAKE2b-Ed25519"
number: "148"
author: "zzz"
created: "2019-03-12"
lastupdated: "2019-04-11"
status: "Otevřít"
thread: "http://zzz.i2p/topics/2689"
toc: true
---

## Přehled

Tento návrh přidává nový typ podpisu používající BLAKE2b-512 s personalizačními řetězci a soli, aby nahradil SHA-512. Toto eliminuje tři třídy možných útoků.

## Motivace

Během diskusí a návrhu NTCP2 (návrh 111) a LS2 (návrh 123) jsme krátce zvažovali různé možné útoky a způsoby, jak jim zabránit. Tři z těchto útoků jsou útoky rozšíření délky (Length Extension Attacks), útoky mezi protokoly (Cross-Protocol Attacks) a identifikace duplicitních zpráv (Duplicate Message Identification).

Pro NTCP2 i LS2 jsme se rozhodli, že tyto útoky nebyly přímo relevantní pro dané návrhy a jakákoli řešení by byla v rozporu s cílem minimalizovat nové primitiva. Také jsme zjistili, že rychlost hashovacích funkcí v těchto protokolech nebyla důležitým faktorem v našich rozhodnutích. Proto jsme řešení většinou odložili na samostatný návrh. Ačkoli jsme do specifikace LS2 přidali některé personalizační funkce, nevyžadovali jsme žádné nové hashovací funkce.

Mnoho projektů, jako je [ZCash](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf), používá hashovací funkce a algoritmy pro podepisování založené na novějších algoritmech, které nejsou zranitelné vůči následujícím útokům.

### Length Extension Attacks

SHA-256 a SHA-512 jsou zranitelné vůči [útokům rozšíření délky (LEA)](https://en.wikipedia.org/wiki/Length_extension_attack). Jedná se o případ, kdy jsou podepsána skutečná data, nikoli hash dat. Ve většině I2P protokolů (streaming, datagramy, netDb a další) jsou podepsána skutečná data. Jednou výjimkou jsou soubory SU3, kde je podepsán hash. Další výjimkou jsou podepsané datagramy pro DSA (typ podpisu 0), kde je podepsán hash. U ostatních typů podpisů podepsaných datagramů jsou podepsána data.

### Cross-Protocol Attacks

Podepsaná data v I2P protokolech mohou být zranitelná vůči Cross-Protocol Attacks (CPA) kvůli nedostatku oddělení domén. To umožňuje útočníkovi použít data přijatá v jednom kontextu (například podepsaný datagram) a předložit je jako platná, podepsaná data v jiném kontextu (například streaming nebo síťová databáze). I když je nepravděpodobné, že by podepsaná data z jednoho kontextu byla analyzována jako platná data v jiném kontextu, je obtížné nebo nemožné analyzovat všechny situace, abychom si byli jisti. Navíc v některých kontextech může být možné, aby útočník přiměl oběť podepsat speciálně vytvořená data, která by mohla být platnými daty v jiném kontextu. Opět je obtížné nebo nemožné analyzovat všechny situace, abychom si byli jisti.

### Útoky rozšířením délky

Protokoly I2P mohou být zranitelné vůči Duplicate Message Identification (DMI). To může umožnit útočníkovi identifikovat, že dvě podepsané zprávy mají stejný obsah, i když jsou tyto zprávy a jejich podpisy šifrované. Ačkoli je to kvůli šifrovacím metodám používaným v I2P nepravděpodobné, je obtížné nebo nemožné analyzovat všechny situace, abychom to věděli jistě. Použitím hash funkce, která poskytuje metodu pro přidání náhodné soli, budou všechny podpisy odlišné i při podepisování stejných dat. Zatímco Red25519 jak je definováno v návrhu 123 přidává náhodnou sůl do hash funkce, toto neřeší problém pro nešifrované leaseSet.

### Útoky mezi protokoly

Ačkoli to není hlavní motivací pro tento návrh, SHA-512 je relativně pomalé a jsou k dispozici rychlejší hashovací funkce.

## Goals

- Zabránit výše uvedeným útokům
- Minimalizovat použití nových kryptografických primitiv
- Používat ověřené, standardní kryptografické primitiva
- Používat standardní křivky
- Používat rychlejší primitiva, pokud jsou dostupná

## Design

Upravte existující typ podpisu RedDSA_SHA512_Ed25519 tak, aby používal BLAKE2b-512 namísto SHA-512. Přidejte jedinečné personalizační řetězce pro každý případ použití. Nový typ podpisu může být použit jak pro neoslepené, tak pro oslepené leaseSety.

## Justification

- [BLAKE2b](https://blake2.net/blake2.pdf) není zranitelný vůči LEA.
- BLAKE2b poskytuje standardní způsob přidání personalizačních řetězců pro doménovou separaci
- BLAKE2b poskytuje standardní způsob přidání náhodné soli pro prevenci DMI.
- BLAKE2b je rychlejší než SHA-256 a SHA-512 (i MD5) na moderním hardwaru,
  podle [specifikace BLAKE2](https://blake2.net/blake2.pdf).
- Ed25519 je stále náš nejrychlejší typ podpisu, mnohem rychlejší než ECDSA, alespoň v Javě.
- [Ed25519](http://cr.yp.to/papers.html#ed25519) vyžaduje 512bitovou kryptografickou hashovací funkci.
  Nespecifikuje SHA-512. BLAKE2b je stejně vhodný pro hashovací funkci.
- BLAKE2b je široce dostupný v knihovnách pro mnoho programovacích jazyků, jako je Noise.

## Specification

Používejte unkeyed BLAKE2b-512 podle [specifikace BLAKE2](https://blake2.net/blake2.pdf) se salt a personalizací. Všechna použití BLAKE2b podpisů budou používat 16-znakový personalizační řetězec.

Při použití v RedDSA_BLAKE2b_Ed25519 podepisování je náhodná sůl povolena, není však nutná, protože algoritmus podpisu přidává 80 bajtů náhodných dat (viz návrh 123). Pokud je to žádoucí, při hashování dat pro výpočet r nastavte novou BLAKE2b 16-bajtovou náhodnou sůl pro každý podpis. Při výpočtu S resetujte sůl na výchozí hodnotu všech nul.

Při použití v RedDSA_BLAKE2b_Ed25519 verifikaci nepoužívejte náhodnou sůl, použijte výchozí hodnotu samých nul.

Funkce salt a personalizace nejsou specifikovány v [RFC 7693](https://tools.ietf.org/html/rfc7693); použijte tyto funkce podle specifikace v [BLAKE2 specification](https://blake2.net/blake2.pdf).

### Identifikace duplicitních zpráv

Pro RedDSA_BLAKE2b_Ed25519 nahraďte hashovací funkci SHA-512 v RedDSA_SHA512_Ed25519 (typ podpisu 11, jak je definováno v návrhu 123) funkcí BLAKE2b-512. Žádné další změny.

Nepotřebujeme náhradu za EdDSA_SHA512_Ed25519ph (typ podpisu 8) pro su3 soubory, protože předhashovaná verze EdDSA není zranitelná vůči LEA. EdDSA_SHA512_Ed25519 (typ podpisu 7) není podporován pro su3 soubory.

| Type | Type Code | Since | Usage |
|------|-----------|-------|-------|
| RedDSA_BLAKE2b_Ed25519 | 12 | TBD | For Router Identities, Destinations and encrypted leasesets only; never used for Router Identities |
### Rychlost

Následující se vztahuje na nový typ podpisu.

| Data Type | Length |
|-----------|--------|
| Hash | 64 |
| Private Key | 32 |
| Public Key | 32 |
| Signature | 64 |
### Personalizations

Pro zajištění separace domén pro různá použití podpisů budeme používat funkci personalizace BLAKE2b.

Všechna použití BLAKE2b podpisů budou používat 16znakový personalizační řetězec. Jakákoli nová použití musí být přidána do tabulky zde s jedinečnou personalizací.

NTCP 1 a SSU handshake použité níže jsou pro podepsaná data definovaná v samotném handshake. Podepsané RouterInfo v DatabaseStore zprávách budou používat personalizaci NetDb Entry, stejně jako kdyby byly uloženy v NetDB.

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
## Cíle

## Návrh

- Alternativa 1: Proposal 146;
  Poskytuje odolnost proti LEA
- Alternativa 2: [Ed25519ctx v RFC 8032](https://tools.ietf.org/html/rfc8032);
  Poskytuje odolnost proti LEA a personalizaci.
  Standardizováno, ale používá to někdo?
  Viz [RFC 8032](https://tools.ietf.org/html/rfc8032) a [tuto diskusi](https://moderncrypto.org/mail-archive/curves/2017/000925.html).
- Je pro nás užitečné "keyed" hashování?

## Odůvodnění

Stejně jako při zavádění předchozích typů podpisů.

Plánujeme změnit nové routery z typu 7 na typ 12 jako výchozí. Plánujeme postupně migrovat existující routery z typu 7 na typ 12 pomocí procesu "rekeying", který se používá po zavedení typu 7. Plánujeme změnit nové destinace z typu 7 na typ 12 jako výchozí. Plánujeme změnit nové šifrované destinace z typu 11 na typ 13 jako výchozí.

Budeme podporovat blinding z typů 7, 11 a 12 na typ 12. Nebudeme podporovat blinding z typu 12 na typ 11.

Nové routery by mohly začít používat nový typ podpisu jako výchozí po několika měsících. Nové destinace by mohly začít používat nový typ podpisu jako výchozí možná po roce.

Pro minimální verzi routeru 0.9.TBD musí routery zajistit:

- Neukládejte (ani nezaplavujte) RI nebo LS s novým typem podpisu do routerů starších než verze 0.9.TBD.
- Při ověřování netdb store nevytahujte RI nebo LS s novým typem podpisu z routerů starších než verze 0.9.TBD.
- Routery s novým typem podpisu ve svém RI se nemusí být schopny připojit k routerům starším než verze 0.9.TBD,
  ať už přes NTCP, NTCP2, nebo SSU.
- Streaming spojení a podepsané datagramy nebudou fungovat s routery staršími než verze 0.9.TBD,
  ale neexistuje způsob, jak to zjistit, takže nový typ podpisu by neměl být používán jako výchozí po dobu
  několika měsíců či let po vydání verze 0.9.TBD.
