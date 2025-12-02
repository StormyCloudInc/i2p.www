---
title: "Tunnels ECIES"
number: "152"
author: "chisana, zzz, orignal"
created: "2019-07-04"
lastupdated: "2025-03-05"
status: "Fermé"
thread: "http://zzz.i2p/topics/2737"
target: "0.9.48"
implementedin: "0.9.48"
toc: true
---

## Note

Déploiement du réseau et tests en cours. Sujet à des révisions mineures. Voir [SPEC](/docs/specs/implementation/) pour la spécification officielle.

## Aperçu général

Ce document propose des modifications au chiffrement des messages Tunnel Build en utilisant les primitives cryptographiques introduites par [ECIES-X25519](/docs/specs/ecies/). Il fait partie de la proposition globale [Proposition 156](/proposals/156-ecies-routers) pour convertir les routeurs des clés ElGamal vers les clés ECIES-X25519.

Pour les besoins de la transition du réseau d'ElGamal + AES256 vers ECIES + ChaCha20, des tunnels avec des routeurs ElGamal et ECIES mixtes sont nécessaires. Les spécifications pour la gestion des sauts de tunnel mixtes sont fournies. Aucune modification ne sera apportée au format, au traitement ou au chiffrement des sauts ElGamal.

Les créateurs de tunnels ElGamal devront créer des paires de clés X25519 éphémères par saut, et suivre cette spécification pour créer des tunnels contenant des sauts ECIES.

Cette proposition spécifie les modifications nécessaires pour la construction de tunnels ECIES-X25519. Pour un aperçu de toutes les modifications requises pour les routeurs ECIES, voir la proposition 156 [Proposition 156](/proposals/156-ecies-routers).

Cette proposition maintient la même taille pour les enregistrements de construction de tunnel, comme requis pour la compatibilité. Des enregistrements et messages de construction plus petits seront implémentés plus tard - voir [Proposition 157](/proposals/157-new-tbm).

### Cryptographic Primitives

Aucune nouvelle primitive cryptographique n'est introduite. Les primitives requises pour implémenter cette proposition sont :

- AES-256-CBC comme dans [Cryptography](/docs/specs/cryptography/)
- Fonctions STREAM ChaCha20/Poly1305 :
  ENCRYPT(k, n, plaintext, ad) et DECRYPT(k, n, ciphertext, ad) - comme dans [NTCP2](/docs/specs/ntcp2/) [ECIES-X25519](/docs/specs/ecies/) et [RFC-7539](https://tools.ietf.org/html/rfc7539)
- Fonctions X25519 DH - comme dans [NTCP2](/docs/specs/ntcp2/) et [ECIES-X25519](/docs/specs/ecies/)
- HKDF(salt, ikm, info, n) - comme dans [NTCP2](/docs/specs/ntcp2/) et [ECIES-X25519](/docs/specs/ecies/)

Autres fonctions Noise définies ailleurs :

- MixHash(d) - comme dans [NTCP2](/docs/specs/ntcp2/) et [ECIES-X25519](/docs/specs/ecies/)
- MixKey(d) - comme dans [NTCP2](/docs/specs/ntcp2/) et [ECIES-X25519](/docs/specs/ecies/)

### Goals

- Augmenter la vitesse des opérations cryptographiques
- Remplacer ElGamal + AES256/CBC par des primitives ECIES pour les BuildRequestRecords et BuildReplyRecords de tunnel.
- Aucun changement de taille des BuildRequestRecords et BuildReplyRecords chiffrés (528 octets) pour la compatibilité
- Aucun nouveau message I2NP
- Maintenir la taille des enregistrements de construction chiffrés pour la compatibilité
- Ajouter la confidentialité persistante pour les messages de construction de tunnel.
- Ajouter le chiffrement authentifié
- Détecter les sauts qui réorganisent les BuildRequestRecords
- Augmenter la résolution de l'horodatage afin que la taille du filtre de Bloom puisse être réduite
- Ajouter un champ pour l'expiration du tunnel afin que des durées de vie de tunnel variables soient possibles (tunnels entièrement ECIES uniquement)
- Ajouter un champ d'options extensible pour les fonctionnalités futures
- Réutiliser les primitives cryptographiques existantes
- Améliorer la sécurité des messages de construction de tunnel dans la mesure du possible tout en maintenant la compatibilité
- Prendre en charge les tunnels avec des pairs ElGamal/ECIES mixtes
- Améliorer les défenses contre les attaques de "marquage" sur les messages de construction
- Les sauts n'ont pas besoin de connaître le type de chiffrement du saut suivant avant de traiter le message de construction,
  car ils peuvent ne pas avoir le RI du saut suivant à ce moment-là
- Maximiser la compatibilité avec le réseau actuel
- Aucun changement au chiffrement AES des requêtes/réponses de construction de tunnel pour les routeurs ElGamal
- Aucun changement au chiffrement de "couche" AES du tunnel, pour cela voir [Proposition 153](/proposals/153-chacha20-layer-encryption)
- Continuer à prendre en charge à la fois les TBM/TBRM à 8 enregistrements et les VTBM/VTBRM de taille variable
- Ne pas exiger une mise à niveau "jour J" de l'ensemble du réseau

### Primitives cryptographiques

- Refonte complète des messages de construction de tunnel nécessitant un "flag day".
- Réduction des messages de construction de tunnel (nécessite des sauts all-ECIES et une nouvelle proposition)
- Utilisation des options de construction de tunnel telles que définies dans la [Proposition 143](/proposals/143-build-message-options), uniquement requise pour les petits messages
- Tunnels bidirectionnels - pour cela voir la [Proposition 119](/proposals/119-bidirectional-tunnels)
- Messages de construction de tunnel plus petits - pour cela voir la [Proposition 157](/proposals/157-new-tbm)

## Threat Model

### Objectifs

- Aucun saut n'est capable de déterminer l'origine du tunnel.

- Les hops intermédiaires ne doivent pas pouvoir déterminer la direction du tunnel
  ou leur position dans le tunnel.

- Aucun hop ne peut lire le contenu des autres enregistrements de requête ou de réponse, sauf
  le hash de routeur tronqué et la clé éphémère pour le hop suivant

- Aucun membre du tunnel de réponse pour la construction sortante ne peut lire les enregistrements de réponse.

- Aucun membre du tunnel sortant pour une construction entrante ne peut lire les enregistrements de requête, sauf que l'OBEP peut voir le hachage de routeur tronqué et la clé éphémère pour l'IBGW

### Objectifs non visés

Un objectif majeur de la conception de construction des tunnels est de rendre plus difficile pour les routers X et Y qui collaborent de savoir qu'ils se trouvent dans un même tunnel. Si le router X est au saut m et le router Y est au saut m+1, ils le sauront évidemment. Mais si le router X est au saut m et le router Y est au saut m+n pour n>1, cela devrait être beaucoup plus difficile.

Les attaques de marquage sont des situations où le router intermédiaire X modifie le message de construction de tunnel de telle manière que le router Y puisse détecter l'altération lorsque le message de construction l'atteint. L'objectif est que tout message altéré soit abandonné par un router entre X et Y avant qu'il n'atteigne le router Y. Pour les modifications qui ne sont pas abandonnées avant le router Y, le créateur du tunnel devrait détecter la corruption dans la réponse et rejeter le tunnel.

Attaques possibles :

- Modifier un enregistrement de construction
- Remplacer un enregistrement de construction
- Ajouter ou supprimer un enregistrement de construction
- Réorganiser les enregistrements de construction

TODO : La conception actuelle empêche-t-elle toutes ces attaques ?

## Design

### Noise Protocol Framework

Cette proposition fournit les exigences basées sur le Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Révision 34, 2018-07-11). Dans le jargon de Noise, Alice est l'initiateur, et Bob est le répondeur.

Cette proposition est basée sur le protocole Noise Noise_N_25519_ChaChaPoly_SHA256. Ce protocole Noise utilise les primitives suivantes :

- Modèle de poignée de main unidirectionnel : N
  Alice ne transmet pas sa clé statique à Bob (N)

- DH Function: X25519
  X25519 DH avec une longueur de clé de 32 octets comme spécifié dans [RFC-7748](https://tools.ietf.org/html/rfc7748).

- Fonction de chiffrement : ChaChaPoly
  AEAD_CHACHA20_POLY1305 tel que spécifié dans [RFC-7539](https://tools.ietf.org/html/rfc7539) section 2.8.
  Nonce de 12 octets, avec les 4 premiers octets définis à zéro.
  Identique à celui dans [NTCP2](/docs/specs/ntcp2/).

- Fonction de Hachage : SHA256
  Hachage standard de 32 octets, déjà largement utilisé dans I2P.

#### Additions to the Framework

Aucun.

### Objectifs de conception

Les handshakes utilisent les modèles de handshake [Noise](https://noiseprotocol.org/noise.html).

La correspondance de lettres suivante est utilisée :

- e = clé éphémère à usage unique
- s = clé statique
- p = charge utile du message

La demande de construction est identique au modèle Noise N. Ceci est également identique au premier message (Session Request) dans le modèle XK utilisé dans [NTCP2](/docs/specs/ntcp2/).

```text
<- s
  ...
  e es p ->
```
### Attaques par marquage

Les enregistrements de demande de construction sont créés par le créateur du tunnel et chiffrés asymétriquement pour chaque saut individuel. Ce chiffrement asymétrique des enregistrements de demande utilise actuellement ElGamal tel que défini dans [Cryptography](/docs/specs/cryptography/) et contient une somme de contrôle SHA-256. Cette conception n'offre pas de confidentialité persistante.

Le nouveau design utilisera le modèle Noise unidirectionnel "N" avec ECIES-X25519 ephemeral-static DH, avec un HKDF, et ChaCha20/Poly1305 AEAD pour la confidentialité persistante, l'intégrité et l'authentification. Alice est le demandeur de construction de tunnel. Chaque saut dans le tunnel est un Bob.

(Propriétés de Sécurité de la Charge Utile)

```text
N:                      Authentication   Confidentiality
    -> e, es                  0                2

    Authentication: None (0).
    This payload may have been sent by any party, including an active attacker.

    Confidentiality: 2.
    Encryption to a known recipient, forward secrecy for sender compromise
    only, vulnerable to replay.  This payload is encrypted based only on DHs
    involving the recipient's static key pair.  If the recipient's static
    private key is compromised, even at a later date, this payload can be
    decrypted.  This message can also be replayed, since there's no ephemeral
    contribution from the recipient.

    "e": Alice generates a new ephemeral key pair and stores it in the e
         variable, writes the ephemeral public key as cleartext into the
         message buffer, and hashes the public key along with the old h to
         derive a new h.

    "es": A DH is performed between the Alice's ephemeral key pair and the
          Bob's static key pair.  The result is hashed along with the old ck to
          derive a new ck and k, and n is set to zero.
```
### Reply encryption

Les enregistrements de réponse de construction sont créés par le créateur des sauts et chiffrés symétriquement au créateur. Ce chiffrement symétrique des enregistrements de réponse utilise actuellement AES avec une somme de contrôle SHA-256 ajoutée au début. et contient une somme de contrôle SHA-256. Cette conception n'offre pas de confidentialité persistante.

La nouvelle conception utilisera ChaCha20/Poly1305 AEAD pour l'intégrité et l'authentification.

### Framework de Protocole Noise

La clé publique éphémère dans la requête n'a pas besoin d'être obfusquée avec AES ou Elligator2. Le saut précédent est le seul qui peut la voir, et ce saut sait que le saut suivant est ECIES.

Les enregistrements de réponse n'ont pas besoin d'un chiffrement asymétrique complet avec un autre DH.

## Specification

### Build Request Records

Les BuildRequestRecords chiffrés font 528 octets pour ElGamal et ECIES, pour des raisons de compatibilité.

#### Request Record Unencrypted (ElGamal)

Pour référence, voici la spécification actuelle du tunnel BuildRequestRecord pour les routeurs ElGamal, tirée de [I2NP](/docs/specs/i2np/). Les données non chiffrées sont précédées d'un octet non nul et du hachage SHA-256 des données avant chiffrement, tel que défini dans [Cryptographie](/docs/specs/cryptography/).

Tous les champs sont en big-endian.

Taille non chiffrée : 222 octets

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes    4-35: local router identity hash
  bytes   36-39: next tunnel ID, nonzero
  bytes   40-71: next router identity hash
  bytes  72-103: AES-256 tunnel layer key
  bytes 104-135: AES-256 tunnel IV key
  bytes 136-167: AES-256 reply key
  bytes 168-183: AES-256 reply IV
  byte      184: flags
  bytes 185-188: request time (in hours since the epoch, rounded down)
  bytes 189-192: next message ID
  bytes 193-221: uninterpreted / random padding
```
#### Request Record Encrypted (ElGamal)

Pour référence, voici la spécification actuelle du BuildRequestRecord de tunnel pour les routeurs ElGamal, tirée de [I2NP](/docs/specs/i2np/).

Taille chiffrée : 528 octets

```text
bytes    0-15: Hop's truncated identity hash
  bytes  16-528: ElGamal encrypted BuildRequestRecord
```
#### Request Record Unencrypted (ECIES)

Voici la spécification proposée du BuildRequestRecord de tunnel pour les routeurs ECIES-X25519. Résumé des modifications :

- Supprimer le hachage de routeur 32-byte inutilisé
- Changer le temps de demande d'heures en minutes
- Ajouter un champ d'expiration pour le temps de tunnel variable futur
- Ajouter plus d'espace pour les drapeaux
- Ajouter un mapping pour les options de construction supplémentaires
- La clé de réponse AES-256 et l'IV ne sont pas utilisés pour l'enregistrement de réponse propre au saut
- L'enregistrement non chiffré est plus long car il y a moins de surcharge de chiffrement

L'enregistrement de requête ne contient aucune clé de réponse ChaCha. Ces clés sont dérivées d'une KDF. Voir ci-dessous.

Tous les champs sont en big-endian.

Taille non chiffrée : 464 bytes

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes     4-7: next tunnel ID, nonzero
  bytes    8-39: next router identity hash
  bytes   40-71: AES-256 tunnel layer key
  bytes  72-103: AES-256 tunnel IV key
  bytes 104-135: AES-256 reply key
  bytes 136-151: AES-256 reply IV
  byte      152: flags
  bytes 153-155: more flags, unused, set to 0 for compatibility
  bytes 156-159: request time (in minutes since the epoch, rounded down)
  bytes 160-163: request expiration (in seconds since creation)
  bytes 164-167: next message ID
  bytes   168-x: tunnel build options (Mapping)
  bytes     x-x: other data as implied by flags or options
  bytes   x-463: random padding
```
Le champ flags est identique à celui défini dans [Tunnel Creation](/docs/specs/implementation/) et contient ce qui suit ::

Ordre des bits : 76543210 (le bit 7 est MSB)  bit 7 : si défini, autoriser les messages de n'importe qui  bit 6 : si défini, autoriser les messages vers n'importe qui, et envoyer la réponse au

        specified next hop in a Tunnel Build Reply Message
bits 5-0 : Non définis, doivent être mis à 0 pour la compatibilité avec les options futures

Le bit 7 indique que le saut sera une passerelle entrante (IBGW). Le bit 6 indique que le saut sera un point de sortie sortant (OBEP). Si aucun des deux bits n'est défini, le saut sera un participant intermédiaire. Les deux ne peuvent pas être définis simultanément.

L'expiration de la demande est destinée à la durée variable future du tunnel. Pour le moment, la seule valeur prise en charge est 600 (10 minutes).

Les options de construction de tunnel sont une structure Mapping telle que définie dans [Structures communes](/docs/specs/common-structures/). Ceci est pour une utilisation future. Aucune option n'est actuellement définie. Si la structure Mapping est vide, cela correspond à deux octets 0x00 0x00. La taille maximale du Mapping (incluant le champ de longueur) est de 296 octets, et la valeur maximale du champ de longueur du Mapping est 294.

#### Request Record Encrypted (ECIES)

Tous les champs sont en big-endian sauf pour la clé publique éphémère qui est en little-endian.

Taille chiffrée : 528 octets

```text
bytes    0-15: Hop's truncated identity hash
  bytes   16-47: Sender's ephemeral X25519 public key
  bytes  48-511: ChaCha20 encrypted BuildRequestRecord
  bytes 512-527: Poly1305 MAC
```
### Modèles de handshake

Les BuildReplyRecords chiffrés font 528 octets pour ElGamal et ECIES, pour des raisons de compatibilité.

#### Reply Record Unencrypted (ElGamal)

Les réponses ElGamal sont chiffrées avec AES.

Tous les champs sont en big-endian.

Taille non chiffrée : 528 octets

```text
bytes   0-31: SHA-256 Hash of bytes 32-527
  bytes 32-526: random data
  byte     527: reply

  total length: 528
```
#### Reply Record Unencrypted (ECIES)

Ceci est la spécification proposée du BuildReplyRecord de tunnel pour les routeurs ECIES-X25519. Résumé des changements :

- Ajouter un mappage pour les options de réponse de construction
- L'enregistrement non chiffré est plus long car il y a moins de surcharge de chiffrement

Les réponses ECIES sont chiffrées avec ChaCha20/Poly1305.

Tous les champs sont en big-endian.

Taille non chiffrée : 512 octets

```text
bytes    0-x: Tunnel Build Reply Options (Mapping)
  bytes    x-x: other data as implied by options
  bytes  x-510: Random padding
  byte     511: Reply byte
```
Les options de réponse de construction de tunnel constituent une structure Mapping telle que définie dans [Structures Communes](/docs/specs/common-structures/). Ceci est prévu pour un usage futur. Aucune option n'est actuellement définie. Si la structure Mapping est vide, cela correspond à deux octets 0x00 0x00. La taille maximale du Mapping (y compris le champ de longueur) est de 511 octets, et la valeur maximale du champ de longueur du Mapping est de 509.

L'octet de réponse est l'une des valeurs suivantes telles que définies dans [Tunnel Creation](/docs/specs/implementation/) pour éviter l'empreinte digitale :

- 0x00 (accepter)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### Reply Record Encrypted (ECIES)

Taille chiffrée : 528 octets

```text
bytes   0-511: ChaCha20 encrypted BuildReplyRecord
  bytes 512-527: Poly1305 MAC
```
Après la transition complète vers les enregistrements ECIES, les règles de remplissage par plages sont les mêmes que pour les enregistrements de requête.

### Chiffrement des requêtes

Les tunnels mixtes sont autorisés, et nécessaires, pour la transition d'ElGamal vers ECIES. Pendant la période de transition, un nombre croissant de routers seront authentifiés avec des clés ECIES.

Le préprocessus de cryptographie symétrique s'exécutera de la même manière :

- "chiffrement" :

- chiffrement exécuté en mode déchiffrement
- enregistrements de requête déchiffrés de manière préventive lors du prétraitement (dissimulant les enregistrements de requête chiffrés)

- "decryption" :

- cipher exécuté en mode chiffrement
- enregistrements de requête chiffrés (révélant le prochain enregistrement de requête en texte clair) par les sauts de participants

- ChaCha20 n'a pas de "modes", donc il est simplement exécuté trois fois :

- une fois dans le prétraitement
- une fois par le saut
- une fois dans le traitement de la réponse finale

Lorsque des tunnels mixtes sont utilisés, les créateurs de tunnel devront baser le chiffrement symétrique du BuildRequestRecord sur le type de chiffrement du saut actuel et du saut précédent.

Chaque hop utilisera son propre type de chiffrement pour chiffrer les BuildReplyRecords, et les autres enregistrements dans le VariableTunnelBuildMessage (VTBM).

Sur le chemin de retour, le point de terminaison (expéditeur) devra annuler le [Multiple Encryption](https://en.wikipedia.org/wiki/Multiple_encryption), en utilisant la clé de réponse de chaque saut.

Comme exemple de clarification, regardons un tunnel sortant avec ECIES entouré par ElGamal :

- Expéditeur (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

Tous les BuildRequestRecords sont dans leur état chiffré (en utilisant ElGamal ou ECIES).

Le chiffrement AES256/CBC, lorsqu'il est utilisé, est toujours utilisé pour chaque enregistrement, sans chaînage entre plusieurs enregistrements.

De même, ChaCha20 sera utilisé pour chiffrer chaque enregistrement, et non en continu sur l'ensemble du VTBM.

Les enregistrements de requête sont prétraités par l'Expéditeur (OBGW) :

- L'enregistrement de H3 est "chiffré" en utilisant :

- Clé de réponse de H2 (ChaCha20)
- Clé de réponse de H1 (AES256/CBC)

- L'enregistrement de H2 est "chiffré" en utilisant :

- Clé de réponse de H1 (AES256/CBC)

- L'enregistrement de H1 sort sans chiffrement symétrique

Seul H2 vérifie le flag de chiffrement de réponse, et voit qu'il est suivi par AES256/CBC.

Après avoir été traités par chaque saut, les enregistrements sont dans un état « déchiffré » :

- L'enregistrement de H3 est "décrypté" en utilisant :

- Clé de réponse de H3 (AES256/CBC)

- L'enregistrement de H2 est "décrypté" en utilisant :

- Clé de réponse de H3 (AES256/CBC)
- Clé de réponse de H2 (ChaCha20-Poly1305)

- L'enregistrement de H1 est "décrypté" en utilisant :

- Clé de réponse de H3 (AES256/CBC)
- Clé de réponse de H2 (ChaCha20)
- Clé de réponse de H1 (AES256/CBC)

Le créateur de tunnel, également appelé Inbound Endpoint (IBEP), post-traite la réponse :

- L'enregistrement de H3 est "chiffré" en utilisant :

- Clé de réponse H3 (AES256/CBC)

- L'enregistrement H2 est "chiffré" en utilisant :

- Clé de réponse de H3 (AES256/CBC)
- Clé de réponse de H2 (ChaCha20-Poly1305)

- L'enregistrement de H1 est "chiffré" en utilisant :

- Clé de réponse de H3 (AES256/CBC)
- Clé de réponse de H2 (ChaCha20)
- Clé de réponse de H1 (AES256/CBC)

### Chiffrement des réponses

Ces clés sont explicitement incluses dans les ElGamal BuildRequestRecords. Pour les ECIES BuildRequestRecords, les clés de tunnel et les clés de réponse AES sont incluses, mais les clés de réponse ChaCha sont dérivées de l'échange DH. Voir la [Proposition 156](/proposals/156-ecies-routers) pour les détails des clés ECIES statiques du router.

Ci-dessous se trouve une description de la façon de dériver les clés précédemment transmises dans les enregistrements de requête.

#### KDF for Initial ck and h

Ceci est un [NOISE](https://noiseprotocol.org/noise.html) standard pour le motif "N" avec un nom de protocole standard.

```text
This is the "e" message pattern:

  // Define protocol_name.
  Set protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 bytes, US-ASCII encoded, no NULL termination).

  // Define Hash h = 32 bytes
  // Pad to 32 bytes. Do NOT hash it, because it is not more than 32 bytes.
  h = protocol_name || 0

  Define ck = 32 byte chaining key. Copy the h data to ck.
  Set chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // up until here, can all be precalculated by all routers.
```
#### KDF for Request Record

Les créateurs de tunnel ElGamal génèrent une paire de clés X25519 éphémère pour chaque saut ECIES dans le tunnel, et utilisent le schéma ci-dessus pour chiffrer leur BuildRequestRecord. Les créateurs de tunnel ElGamal utiliseront le schéma antérieur à cette spécification pour le chiffrement vers les sauts ElGamal.

Les créateurs de tunnels ECIES devront chiffrer vers la clé publique de chaque saut ElGamal en utilisant le schéma défini dans [Tunnel Creation](/docs/specs/implementation/). Les créateurs de tunnels ECIES utiliseront le schéma ci-dessus pour chiffrer vers les sauts ECIES.

Cela signifie que les sauts de tunnel ne verront que les enregistrements chiffrés de leur même type de chiffrement.

Pour les créateurs de tunnel ElGamal et ECIES, ils généreront des paires de clés X25519 éphémères uniques par-hop pour chiffrer vers les hops ECIES.

**IMPORTANT** : Les clés éphémères doivent être uniques par saut ECIES et par enregistrement de construction. L'échec à utiliser des clés uniques ouvre un vecteur d'attaque permettant aux sauts en collusion de confirmer qu'ils sont dans le même tunnel.

```text
// Each hop's X25519 static keypair (hesk, hepk) from the Router Identity
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || below means append
  h = SHA256(h || hepk);

  // up until here, can all be precalculated by each router
  // for all incoming build requests

  // Sender generates an X25519 ephemeral keypair per ECIES hop in the VTBM (sesk, sepk)
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  End of "e" message pattern.

  This is the "es" message pattern:

  // Noise es
  // Sender performs an X25519 DH with Hop's static public key.
  // Each Hop, finds the record w/ their truncated identity hash,
  // and extracts the Sender's ephemeral key preceding the encrypted record.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // Save for Reply Record KDF
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  plaintext = 464 byte build request record
  ad = h
  ciphertext = ENCRYPT(k, n, plaintext, ad)

  End of "es" message pattern.

  // MixHash(ciphertext)
  // Save for Reply Record KDF
  h = SHA256(h || ciphertext)
```
``replyKey``, ``layerKey`` et ``layerIV`` doivent toujours être inclus dans les enregistrements ElGamal, et peuvent être générés de manière aléatoire.

### Justification

Comme défini dans [Tunnel Creation](/docs/specs/implementation/). Il n'y a aucun changement au chiffrement pour les sauts ElGamal.

### Reply Record Encryption (ECIES)

L'enregistrement de réponse est chiffré avec ChaCha20/Poly1305.

```text
// AEAD parameters
  k = chainkey from build request
  n = 0
  plaintext = 512 byte build reply record
  ad = h from build request

  ciphertext = ENCRYPT(k, n, plaintext, ad)
```
### Enregistrements de Demande de Construction

Comme défini dans [Tunnel Creation](/docs/specs/implementation/). Il n'y a aucun changement au chiffrement pour les hops ElGamal.

### Security Analysis

ElGamal ne fournit pas de confidentialité persistante (forward secrecy) pour les messages Tunnel Build.

AES256/CBC est dans une position légèrement meilleure, n'étant vulnérable qu'à un affaiblissement théorique provenant d'une attaque `biclique` à texte clair connu.

La seule attaque pratique connue contre AES256/CBC est une attaque par oracle de bourrage, lorsque l'IV est connu de l'attaquant.

Un attaquant devrait casser le chiffrement ElGamal du saut suivant pour obtenir les informations de clé AES256/CBC (clé de réponse et IV).

ElGamal est considérablement plus gourmand en CPU qu'ECIES, ce qui peut entraîner un épuisement des ressources.

ECIES, utilisé avec de nouvelles clés éphémères par BuildRequestRecord ou VariableTunnelBuildMessage, fournit la confidentialité persistante.

ChaCha20Poly1305 fournit un chiffrement AEAD, permettant au destinataire de vérifier l'intégrité du message avant de tenter le déchiffrement.

## Modèle de menace

Cette conception maximise la réutilisation des primitives cryptographiques, protocoles et code existants. Cette conception minimise les risques.

## Implementation Notes

* Les routeurs plus anciens ne vérifient pas le type de chiffrement du saut et enverront des
  enregistrements chiffrés avec ElGamal. Certains routeurs récents sont défectueux et enverront
  divers types d'enregistrements mal formés. Les développeurs devraient détecter et rejeter
  ces enregistrements avant l'opération DH si possible, afin de réduire l'utilisation du CPU.

## Issues

## Conception

Voir [Proposition 156](/proposals/156-ecies-routers).
