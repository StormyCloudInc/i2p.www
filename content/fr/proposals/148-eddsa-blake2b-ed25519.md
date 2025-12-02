---
title: "RedDSA-BLAKE2b-Ed25519"
number: "148"
author: "zzz"
created: "2019-03-12"
lastupdated: "2019-04-11"
status: "Ouvrir"
thread: "http://zzz.i2p/topics/2689"
toc: true
---

## Aperçu

Cette proposition ajoute un nouveau type de signature utilisant BLAKE2b-512 avec des chaînes de personnalisation et des sels, pour remplacer SHA-512. Cela éliminera trois classes d'attaques possibles.

## Motivation

Lors des discussions et de la conception de NTCP2 (proposition 111) et LS2 (proposition 123), nous avons brièvement considéré diverses attaques qui étaient possibles, et comment les prévenir. Trois de ces attaques sont les Attaques d'Extension de Longueur, les Attaques Inter-Protocoles, et l'Identification de Messages Dupliqués.

Pour NTCP2 et LS2, nous avons décidé que ces attaques n'étaient pas directement pertinentes aux propositions en question, et que toute solution entrerait en conflit avec l'objectif de minimiser les nouvelles primitives. De plus, nous avons déterminé que la vitesse des fonctions de hachage dans ces protocoles n'était pas un facteur important dans nos décisions. Par conséquent, nous avons principalement reporté la solution à une proposition séparée. Bien que nous ayons ajouté quelques fonctionnalités de personnalisation à la spécification LS2, nous n'avons exigé aucune nouvelle fonction de hachage.

De nombreux projets, tels que [ZCash](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf), utilisent des fonctions de hachage et des algorithmes de signature basés sur des algorithmes plus récents qui ne sont pas vulnérables aux attaques suivantes.

### Length Extension Attacks

SHA-256 et SHA-512 sont vulnérables aux [Attaques par Extension de Longueur (LEA)](https://en.wikipedia.org/wiki/Length_extension_attack). C'est le cas quand les données réelles sont signées, pas le hash des données. Dans la plupart des protocoles I2P (streaming, datagrams, netdb, et autres), les données réelles sont signées. Une exception concerne les fichiers SU3, où le hash est signé. L'autre exception concerne les signed datagrams pour DSA (sig type 0) uniquement, où le hash est signé. Pour les autres types de signatures de datagrams, les données sont signées.

### Cross-Protocol Attacks

Les données signées dans les protocoles I2P peuvent être vulnérables aux attaques inter-protocoles (CPA) en raison de l'absence de séparation de domaine. Cela permet à un attaquant d'utiliser des données reçues dans un contexte (comme un datagramme signé) et de les présenter comme des données valides et signées dans un autre contexte (comme le streaming ou la base de données réseau). Bien qu'il soit improbable que les données signées d'un contexte soient analysées comme des données valides dans un autre contexte, il est difficile ou impossible d'analyser toutes les situations pour en être certain. De plus, dans certains contextes, il peut être possible pour un attaquant d'inciter une victime à signer des données spécialement conçues qui pourraient être des données valides dans un autre contexte. Encore une fois, il est difficile ou impossible d'analyser toutes les situations pour en être certain.

### Attaques par Extension de Longueur

Les protocoles I2P peuvent être vulnérables à l'identification de messages dupliqués (DMI). Cela peut permettre à un attaquant d'identifier que deux messages signés ont le même contenu, même si ces messages et leurs signatures sont chiffrés. Bien que cela soit peu probable en raison des méthodes de chiffrement utilisées dans I2P, il est difficile ou impossible d'analyser toutes les situations pour en être certain. En utilisant une fonction de hachage qui fournit une méthode pour ajouter un sel aléatoire, toutes les signatures seront différentes même lors de la signature des mêmes données. Bien que Red25519 tel que défini dans la proposition 123 ajoute un sel aléatoire à la fonction de hachage, cela ne résout pas le problème pour les lease sets non chiffrés.

### Attaques Cross-Protocol

Bien que cela ne soit pas une motivation principale pour cette proposition, SHA-512 est relativement lent, et des fonctions de hachage plus rapides sont disponibles.

## Goals

- Prévenir les attaques mentionnées ci-dessus
- Minimiser l'utilisation de nouvelles primitives cryptographiques
- Utiliser des primitives cryptographiques standard et éprouvées
- Utiliser des courbes standard
- Utiliser des primitives plus rapides si disponibles

## Design

Modifier le type de signature RedDSA_SHA512_Ed25519 existant pour utiliser BLAKE2b-512 au lieu de SHA-512. Ajouter des chaînes de personnalisation uniques pour chaque cas d'usage. Le nouveau type de signature peut être utilisé à la fois pour les leaseSets aveugles et non aveugles.

## Justification

- [BLAKE2b](https://blake2.net/blake2.pdf) n'est pas vulnérable au LEA.
- BLAKE2b fournit une méthode standard pour ajouter des chaînes de personnalisation pour la séparation de domaine
- BLAKE2b fournit une méthode standard pour ajouter un sel aléatoire afin de prévenir le DMI.
- BLAKE2b est plus rapide que SHA-256 et SHA-512 (et MD5) sur le matériel moderne,
  selon la [spécification BLAKE2](https://blake2.net/blake2.pdf).
- Ed25519 reste notre type de signature le plus rapide, beaucoup plus rapide qu'ECDSA, au moins en Java.
- [Ed25519](http://cr.yp.to/papers.html#ed25519) nécessite une fonction de hachage cryptographique de 512 bits.
  Elle ne spécifie pas SHA-512. BLAKE2b convient tout aussi bien pour la fonction de hachage.
- BLAKE2b est largement disponible dans les bibliothèques pour de nombreux langages de programmation, comme Noise.

## Specification

Utilisez BLAKE2b-512 non clé comme dans la [spécification BLAKE2](https://blake2.net/blake2.pdf) avec sel et personnalisation. Toutes les utilisations des signatures BLAKE2b utiliseront une chaîne de personnalisation de 16 caractères.

Lorsqu'utilisé dans la signature RedDSA_BLAKE2b_Ed25519, un salt aléatoire est autorisé, cependant il n'est pas nécessaire, car l'algorithme de signature ajoute 80 octets de données aléatoires (voir proposition 123). Si désiré, lors du hachage des données pour calculer r, définir un nouveau salt aléatoire BLAKE2b de 16 octets pour chaque signature. Lors du calcul de S, réinitialiser le salt à la valeur par défaut de tous-zéros.

Lors de l'utilisation dans la vérification RedDSA_BLAKE2b_Ed25519, n'utilisez pas un sel aléatoire, utilisez la valeur par défaut de tous-zéros.

Les fonctionnalités salt et personalisation ne sont pas spécifiées dans la [RFC 7693](https://tools.ietf.org/html/rfc7693) ; utilisez ces fonctionnalités comme spécifié dans la [spécification BLAKE2](https://blake2.net/blake2.pdf).

### Identification des Messages Dupliqués

Pour RedDSA_BLAKE2b_Ed25519, remplacer la fonction de hachage SHA-512 dans RedDSA_SHA512_Ed25519 (type de signature 11, tel que défini dans la proposition 123) par BLAKE2b-512. Aucun autre changement.

Nous n'avons pas besoin d'un remplacement pour EdDSA_SHA512_Ed25519ph (type de signature 8) pour les fichiers su3, car la version pré-hachée d'EdDSA n'est pas vulnérable à LEA. EdDSA_SHA512_Ed25519 (type de signature 7) n'est pas pris en charge pour les fichiers su3.

| Type | Type Code | Since | Usage |
|------|-----------|-------|-------|
| RedDSA_BLAKE2b_Ed25519 | 12 | TBD | For Router Identities, Destinations and encrypted leasesets only; never used for Router Identities |
### Vitesse

Ce qui suit s'applique au nouveau type de signature.

| Data Type | Length |
|-----------|--------|
| Hash | 64 |
| Private Key | 32 |
| Public Key | 32 |
| Signature | 64 |
### Personalizations

Pour fournir une séparation de domaine pour les diverses utilisations des signatures, nous utiliserons la fonctionnalité de personnalisation BLAKE2b.

Toutes les utilisations des signatures BLAKE2b utiliseront une chaîne de personnalisation de 16 caractères. Toute nouvelle utilisation doit être ajoutée au tableau ci-dessous, avec une personnalisation unique.

La négociation NTCP 1 et SSU utilisée ci-dessous concerne les données signées définies dans la négociation elle-même. Les RouterInfos signées dans les messages DatabaseStore utiliseront la personnalisation d'entrée NetDb, exactement comme si elles étaient stockées dans la NetDB.

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
## Objectifs

## Conception

- Alternative 1 : Proposition 146 ;
  Fournit une résistance LEA
- Alternative 2 : [Ed25519ctx dans RFC 8032](https://tools.ietf.org/html/rfc8032) ;
  Fournit une résistance LEA et une personnalisation.
  Standardisé, mais est-ce que quelqu'un l'utilise ?
  Voir [RFC 8032](https://tools.ietf.org/html/rfc8032) et [cette discussion](https://moderncrypto.org/mail-archive/curves/2017/000925.html).
- Le hachage « à clé » nous est-il utile ?

## Justification

La même chose qu'avec le déploiement des types de signature précédents.

Nous prévoyons de changer les nouveaux routeurs du type 7 au type 12 par défaut. Nous prévoyons de migrer à terme les routeurs existants du type 7 vers le type 12, en utilisant le processus de "rekeying" utilisé après l'introduction du type 7. Nous prévoyons de changer les nouvelles destinations du type 7 au type 12 par défaut. Nous prévoyons de changer les nouvelles destinations chiffrées du type 11 au type 13 par défaut.

Nous prendrons en charge l'aveuglement des types 7, 11 et 12 vers le type 12. Nous ne prendrons pas en charge l'aveuglement du type 12 vers le type 11.

Les nouveaux routeurs pourraient commencer à utiliser le nouveau type de signature par défaut après quelques mois. Les nouvelles destinations pourraient commencer à utiliser le nouveau type de signature par défaut après environ un an.

Pour la version minimale de router 0.9.TBD, les routers doivent s'assurer que :

- Ne pas stocker (ou diffuser) un RI ou LS avec le nouveau type de signature vers des routeurs de version inférieure à 0.9.TBD.
- Lors de la vérification d'un stockage netDb, ne pas récupérer un RI ou LS avec le nouveau type de signature depuis des routeurs de version inférieure à 0.9.TBD.
- Les routeurs avec un nouveau type de signature dans leur RI ne peuvent pas se connecter aux routeurs de version inférieure à 0.9.TBD,
  que ce soit avec NTCP, NTCP2, ou SSU.
- Les connexions streaming et les datagrammes signés ne fonctionneront pas vers des routeurs de version inférieure à 0.9.TBD,
  mais il n'y a aucun moyen de le savoir, donc le nouveau type de signature ne devrait pas être utilisé par défaut pendant une période
  de plusieurs mois ou années après la sortie de 0.9.TBD.
