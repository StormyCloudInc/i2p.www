---
title: "ECIES 터널"
number: "152"
author: "chisana, zzz, orignal"
created: "2019-07-04"
lastupdated: "2025-03-05"
status: "닫힘"
thread: "http://zzz.i2p/topics/2737"
target: "0.9.48"
implementedin: "0.9.48"
---

## 참고

네트워크 배포 및 테스트가 진행 중입니다. 소규모 수정이 있을 수 있습니다. 공식 사양은 [SPEC](/docs/specs/implementation/)을 참조하세요.

## 개요

이 문서는 [ECIES-X25519](/docs/specs/ecies/)에서 소개된 암호화 프리미티브를 사용하여 Tunnel Build 메시지 암호화를 변경하는 것을 제안합니다. 이는 router를 ElGamal에서 ECIES-X25519 키로 전환하기 위한 전체 제안 [Proposal 156](/proposals/156-ecies-routers)의 일부입니다.

네트워크를 ElGamal + AES256에서 ECIES + ChaCha20로 전환하기 위한 목적으로, ElGamal과 ECIES router가 혼합된 tunnel이 필요합니다. 혼합된 tunnel hop을 처리하기 위한 사양이 제공됩니다. ElGamal hop의 형식, 처리 또는 암호화에는 변경사항이 적용되지 않습니다.

ElGamal tunnel 생성자들은 홉별로 임시 X25519 키쌍을 생성해야 하며, ECIES 홉을 포함하는 tunnel을 생성할 때 이 사양을 따라야 합니다.

이 제안서는 ECIES-X25519 Tunnel Building에 필요한 변경사항을 명시합니다. ECIES router에 필요한 모든 변경사항의 개요는 제안서 156 [Proposal 156](/proposals/156-ecies-routers)을 참조하십시오.

이 제안은 호환성을 위해 필요한 대로 tunnel 구축 레코드의 동일한 크기를 유지합니다. 더 작은 구축 레코드와 메시지는 나중에 구현될 예정입니다 - [Proposal 157](/proposals/157-new-tbm)을 참조하십시오.

### Cryptographic Primitives

새로운 암호화 기본 요소는 도입되지 않습니다. 이 제안을 구현하는 데 필요한 기본 요소는 다음과 같습니다:

- [암호화](/docs/specs/cryptography/)에서와 같은 AES-256-CBC
- STREAM ChaCha20/Poly1305 함수들:
  ENCRYPT(k, n, plaintext, ad) 및 DECRYPT(k, n, ciphertext, ad) - [NTCP2](/docs/specs/ntcp2/) [ECIES-X25519](/docs/specs/ecies/) 및 [RFC-7539](https://tools.ietf.org/html/rfc7539)에서와 같음
- X25519 DH 함수들 - [NTCP2](/docs/specs/ntcp2/) 및 [ECIES-X25519](/docs/specs/ecies/)에서와 같음
- HKDF(salt, ikm, info, n) - [NTCP2](/docs/specs/ntcp2/) 및 [ECIES-X25519](/docs/specs/ecies/)에서와 같음

다른 곳에서 정의된 기타 Noise 함수들:

- MixHash(d) - [NTCP2](/docs/specs/ntcp2/)와 [ECIES-X25519](/docs/specs/ecies/)에서와 같이
- MixKey(d) - [NTCP2](/docs/specs/ntcp2/)와 [ECIES-X25519](/docs/specs/ecies/)에서와 같이

### Goals

- 암호화 작업 속도 향상
- tunnel BuildRequestRecords 및 BuildReplyRecords에 대해 ElGamal + AES256/CBC를 ECIES primitives로 교체
- 호환성을 위해 암호화된 BuildRequestRecords 및 BuildReplyRecords 크기(528바이트) 변경 없음
- 새로운 I2NP 메시지 없음
- 호환성을 위해 암호화된 빌드 레코드 크기 유지
- Tunnel Build Messages에 forward secrecy 추가
- 인증된 암호화 추가
- BuildRequestRecords 재정렬을 감지하는 홉 검출
- 블룸 필터 크기를 줄일 수 있도록 타임스탬프 해상도 증가
- 다양한 tunnel 수명이 가능하도록 tunnel 만료 필드 추가 (전체 ECIES tunnel만 해당)
- 향후 기능을 위한 확장 가능한 옵션 필드 추가
- 기존 암호화 primitives 재사용
- 호환성을 유지하면서 가능한 한 tunnel 빌드 메시지 보안 향상
- 혼합 ElGamal/ECIES 피어가 있는 tunnel 지원
- 빌드 메시지에 대한 "태깅" 공격 방어 개선
- 홉은 빌드 메시지를 처리하기 전에 다음 홉의 암호화 유형을 알 필요가 없음,
  해당 시점에 다음 홉의 RI를 가지고 있지 않을 수 있기 때문
- 현재 네트워크와의 호환성 최대화
- ElGamal router에 대한 tunnel 빌드 AES 요청/응답 암호화 변경 없음
- tunnel AES "layer" 암호화 변경 없음, 이에 대해서는 [Proposal 153](/proposals/153-chacha20-layer-encryption) 참조
- 8-레코드 TBM/TBRM 및 가변 크기 VTBM/VTBRM 모두 계속 지원
- 전체 네트워크에 "플래그 데이" 업그레이드 요구하지 않음

### 암호화 기본 요소

- "flag day"가 필요한 tunnel 구축 메시지의 완전한 재설계
- tunnel 구축 메시지 축소 (모든 ECIES 홉과 새로운 제안 필요)
- [Proposal 143](/proposals/143-build-message-options)에 정의된 tunnel 구축 옵션 사용, 작은 메시지에만 필요
- 양방향 tunnel - [Proposal 119](/proposals/119-bidirectional-tunnels) 참조
- 더 작은 tunnel 구축 메시지 - [Proposal 157](/proposals/157-new-tbm) 참조

## Threat Model

### 목표

- 어떤 홉도 tunnel의 발신자를 확인할 수 없습니다.

- 중간 홉들은 터널의 방향이나 터널 내에서의 자신의 위치를 결정할 수 없어야 합니다.

- 어떤 홉도 다음 홉을 위한 잘린 라우터 해시와 임시 키를 제외하고는 다른 요청이나 응답 레코드의 내용을 읽을 수 없습니다

- 아웃바운드 빌드에 대한 응답 tunnel의 어떤 구성원도 응답 레코드를 읽을 수 없습니다.

- 아웃바운드 tunnel의 구성원은 인바운드 빌드에 대한 어떤 요청 레코드도 읽을 수 없으며,
  OBEP가 IBGW에 대한 잘린 router 해시와 임시 키를 볼 수 있다는 점만 예외입니다

### 비목표

tunnel 구축 설계의 주요 목표는 공모하는 router X와 Y가 동일한 tunnel에 있다는 것을 알기 어렵게 만드는 것입니다. router X가 홉 m에 있고 router Y가 홉 m+1에 있다면, 이들은 당연히 알 수 있을 것입니다. 하지만 router X가 홉 m에 있고 router Y가 n>1인 홉 m+n에 있다면, 이를 알기가 훨씬 어려워야 합니다.

태깅 공격은 중간 홉 router X가 터널 구축 메시지를 변조하여 구축 메시지가 router Y에 도달했을 때 router Y가 그 변조를 감지할 수 있도록 하는 공격입니다. 목표는 변조된 메시지가 router Y에 도달하기 전에 X와 Y 사이의 router에 의해 폐기되도록 하는 것입니다. router Y 이전에 폐기되지 않은 수정 사항의 경우, 터널 생성자가 응답에서 손상을 감지하고 터널을 폐기해야 합니다.

가능한 공격:

- 빌드 기록 수정
- 빌드 기록 교체
- 빌드 기록 추가 또는 제거
- 빌드 기록 순서 변경

TODO: 현재 설계가 이러한 모든 공격을 방지하는가?

## Design

### Noise Protocol Framework

이 제안서는 Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (개정 34, 2018-07-11)를 기반으로 한 요구사항을 제공합니다. Noise 용어에서 Alice는 개시자(initiator)이고, Bob은 응답자(responder)입니다.

이 제안은 Noise protocol Noise_N_25519_ChaChaPoly_SHA256을 기반으로 합니다. 이 Noise protocol은 다음과 같은 기본 요소들을 사용합니다:

- One-Way Handshake Pattern: N
  Alice는 자신의 정적 키를 Bob에게 전송하지 않습니다 (N)

- DH Function: X25519
  [RFC-7748](https://tools.ietf.org/html/rfc7748)에 명시된 대로 32바이트 키 길이를 가진 X25519 DH.

- Cipher Function: ChaChaPoly
  [RFC-7539](https://tools.ietf.org/html/rfc7539) 섹션 2.8에 명시된 AEAD_CHACHA20_POLY1305.
  12바이트 nonce, 처음 4바이트는 0으로 설정.
  [NTCP2](/docs/specs/ntcp2/)와 동일함.

- Hash Function: SHA256
  I2P에서 이미 광범위하게 사용되고 있는 표준 32바이트 해시.

#### Additions to the Framework

없음.

### 설계 목표

핸드셰이크는 [Noise](https://noiseprotocol.org/noise.html) 핸드셰이크 패턴을 사용합니다.

다음 문자 매핑이 사용됩니다:

- e = 일회용 임시 키
- s = 정적 키
- p = 메시지 페이로드

빌드 요청은 Noise N 패턴과 동일합니다. 이는 또한 [NTCP2](/docs/specs/ntcp2/)에서 사용되는 XK 패턴의 첫 번째 (세션 요청) 메시지와도 동일합니다.

```text
<- s
  ...
  e es p ->
```
### 태깅 공격

Build request 레코드는 터널 생성자에 의해 생성되며 개별 홉에 비대칭 암호화됩니다. Request 레코드의 이 비대칭 암호화는 현재 [Cryptography](/docs/specs/cryptography/)에서 정의된 ElGamal이며 SHA-256 체크섬을 포함합니다. 이 설계는 forward-secret하지 않습니다.

새로운 설계는 순방향 보안성, 무결성, 인증을 위해 ECIES-X25519 ephemeral-static DH, HKDF, ChaCha20/Poly1305 AEAD와 함께 단방향 Noise 패턴 "N"을 사용할 것입니다. Alice는 tunnel 구축 요청자입니다. tunnel의 각 홉은 Bob입니다.

(페이로드 보안 속성)

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

Build reply 레코드는 hops creator에 의해 생성되고 creator에게 대칭 암호화됩니다. reply 레코드의 이 대칭 암호화는 현재 SHA-256 체크섬이 앞에 붙은 AES를 사용하며 SHA-256 체크섬을 포함합니다. 이 설계는 전방향 보안을 제공하지 않습니다.

새로운 설계는 무결성과 인증을 위해 ChaCha20/Poly1305 AEAD를 사용할 것입니다.

### Noise Protocol Framework

요청의 임시 공개 키는 AES나 Elligator2로 난독화할 필요가 없습니다. 이전 홉만이 이를 볼 수 있으며, 해당 홉은 다음 홉이 ECIES라는 것을 알고 있습니다.

응답 레코드는 다른 DH와의 완전한 비대칭 암호화가 필요하지 않습니다.

## Specification

### Build Request Records

암호화된 BuildRequestRecord는 호환성을 위해 ElGamal과 ECIES 모두에서 528바이트입니다.

#### Request Record Unencrypted (ElGamal)

참고용으로, 다음은 [I2NP](/docs/specs/i2np/)에서 가져온 ElGamal router용 tunnel BuildRequestRecord의 현재 사양입니다. 암호화되지 않은 데이터는 [Cryptography](/docs/specs/cryptography/)에서 정의된 대로 0이 아닌 바이트와 암호화 전 데이터의 SHA-256 해시로 앞에 붙여집니다.

모든 필드는 big-endian입니다.

암호화되지 않은 크기: 222 바이트

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

참고로, 다음은 [I2NP](/docs/specs/i2np/)에서 가져온 ElGamal router용 tunnel BuildRequestRecord의 현재 사양입니다.

암호화된 크기: 528바이트

```text
bytes    0-15: Hop's truncated identity hash
  bytes  16-528: ElGamal encrypted BuildRequestRecord
```
#### Request Record Unencrypted (ECIES)

이것은 ECIES-X25519 router들을 위한 tunnel BuildRequestRecord의 제안된 사양입니다. 변경사항 요약:

- 사용하지 않는 32바이트 router 해시 제거
- 요청 시간을 시간에서 분으로 변경
- 향후 가변 tunnel 시간을 위한 만료 필드 추가
- 플래그를 위한 더 많은 공간 추가
- 추가 빌드 옵션을 위한 매핑 추가
- AES-256 응답 키와 IV는 해당 홉의 자체 응답 레코드에는 사용되지 않음
- 암호화 오버헤드가 적기 때문에 암호화되지 않은 레코드가 더 김

요청 레코드에는 ChaCha 응답 키가 포함되지 않습니다. 이러한 키는 KDF에서 파생됩니다. 아래를 참조하십시오.

모든 필드는 big-endian입니다.

암호화되지 않은 크기: 464바이트

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
flags 필드는 [Tunnel Creation](/docs/specs/implementation/)에서 정의된 것과 동일하며 다음을 포함합니다::

비트 순서: 76543210 (비트 7이 MSB)  비트 7: 설정된 경우, 누구로부터든 메시지 허용  비트 6: 설정된 경우, 누구에게든 메시지 허용하고, 응답을 다음으로 전송:

        specified next hop in a Tunnel Build Reply Message
bits 5-0: 정의되지 않음, 향후 옵션과의 호환성을 위해 반드시 0으로 설정해야 함

비트 7은 해당 hop이 인바운드 gateway (IBGW)가 될 것임을 나타냅니다. 비트 6은 해당 hop이 아웃바운드 endpoint (OBEP)가 될 것임을 나타냅니다. 두 비트가 모두 설정되지 않은 경우, 해당 hop은 중간 참가자가 됩니다. 두 비트가 동시에 설정될 수는 없습니다.

요청 만료 시간은 향후 가변적인 터널 지속 시간을 위한 것입니다. 현재로서는 600(10분)만이 지원되는 값입니다.

tunnel 빌드 옵션은 [Common Structures](/docs/specs/common-structures/)에 정의된 Mapping 구조체입니다. 이는 향후 사용을 위한 것입니다. 현재 정의된 옵션은 없습니다. Mapping 구조체가 비어있다면, 이는 두 바이트 0x00 0x00입니다. Mapping의 최대 크기(길이 필드 포함)는 296바이트이며, Mapping 길이 필드의 최대값은 294입니다.

#### Request Record Encrypted (ECIES)

임시 공개 키가 little-endian인 것을 제외하고 모든 필드는 big-endian입니다.

암호화된 크기: 528바이트

```text
bytes    0-15: Hop's truncated identity hash
  bytes   16-47: Sender's ephemeral X25519 public key
  bytes  48-511: ChaCha20 encrypted BuildRequestRecord
  bytes 512-527: Poly1305 MAC
```
### 핸드셰이크 패턴

암호화된 BuildReplyRecord는 호환성을 위해 ElGamal과 ECIES 모두에서 528바이트입니다.

#### Reply Record Unencrypted (ElGamal)

ElGamal 응답은 AES로 암호화됩니다.

모든 필드는 big-endian입니다.

암호화되지 않은 크기: 528바이트

```text
bytes   0-31: SHA-256 Hash of bytes 32-527
  bytes 32-526: random data
  byte     527: reply

  total length: 528
```
#### Reply Record Unencrypted (ECIES)

이것은 ECIES-X25519 router들을 위한 터널 BuildReplyRecord의 제안된 사양입니다. 변경 사항 요약:

- 빌드 응답 옵션에 대한 매핑 추가
- 암호화되지 않은 레코드는 암호화 오버헤드가 적어 더 길다

ECIES 응답은 ChaCha20/Poly1305로 암호화됩니다.

모든 필드는 빅 엔디안입니다.

암호화되지 않은 크기: 512 바이트

```text
bytes    0-x: Tunnel Build Reply Options (Mapping)
  bytes    x-x: other data as implied by options
  bytes  x-510: Random padding
  byte     511: Reply byte
```
tunnel build reply options는 [공통 구조](/docs/specs/common-structures/)에 정의된 Mapping 구조입니다. 이것은 향후 사용을 위한 것입니다. 현재 정의된 옵션은 없습니다. Mapping 구조가 비어있으면, 이것은 0x00 0x00 두 바이트입니다. Mapping의 최대 크기(길이 필드 포함)는 511바이트이며, Mapping 길이 필드의 최대값은 509입니다.

응답 바이트는 핑거프린팅을 방지하기 위해 [Tunnel Creation](/docs/specs/implementation/)에서 정의된 다음 값 중 하나입니다:

- 0x00 (수락)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### Reply Record Encrypted (ECIES)

암호화된 크기: 528바이트

```text
bytes   0-511: ChaCha20 encrypted BuildReplyRecord
  bytes 512-527: Poly1305 MAC
```
ECIES 레코드로의 완전한 전환 후에는 범위 패딩 규칙이 요청 레코드와 동일합니다.

### 요청 암호화

혼합 tunnel은 허용되며, ElGamal에서 ECIES로의 전환을 위해 필요합니다. 전환 기간 동안, ECIES 키로 키가 설정된 router의 수가 증가할 것입니다.

대칭 암호화 전처리는 동일한 방식으로 실행됩니다:

- "encryption":

- cipher가 복호화 모드에서 실행됨
- 요청 레코드가 전처리에서 선제적으로 복호화됨 (암호화된 요청 레코드 은폐)

- "복호화":

- 암호화 모드로 실행되는 cipher
- 참가자 홉에 의해 암호화된(다음 평문 요청 레코드를 드러내는) 요청 레코드

- ChaCha20은 "모드"가 없으므로, 단순히 세 번 실행됩니다:

- 전처리에서 한 번
- 홉에서 한 번
- 최종 응답 처리에서 한 번

혼합 터널이 사용될 때, 터널 생성자는 현재 및 이전 홉의 암호화 유형을 기반으로 BuildRequestRecord의 대칭 암호화를 수행해야 합니다.

각 hop은 BuildReplyRecords와 VariableTunnelBuildMessage (VTBM)의 다른 레코드들을 암호화하기 위해 자체 암호화 유형을 사용합니다.

응답 경로에서 엔드포인트(발신자)는 각 홉의 응답 키를 사용하여 [Multiple Encryption](https://en.wikipedia.org/wiki/Multiple_encryption)을 해제해야 합니다.

명확한 예시로, ElGamal로 둘러싸인 ECIES를 사용하는 아웃바운드 tunnel을 살펴보겠습니다:

- 송신자 (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

모든 BuildRequestRecord는 암호화된 상태입니다 (ElGamal 또는 ECIES 사용).

AES256/CBC 암호가 사용될 때는 여전히 각 레코드에 대해 사용되며, 여러 레코드에 걸친 체이닝은 없습니다.

마찬가지로, ChaCha20은 전체 VTBM에 걸쳐 스트리밍하는 것이 아니라 각 레코드를 암호화하는 데 사용됩니다.

요청 레코드는 Sender (OBGW)에 의해 전처리됩니다:

- H3의 레코드는 다음을 사용하여 "암호화"됩니다:

- H2의 응답 키 (ChaCha20)
- H1의 응답 키 (AES256/CBC)

- H2의 레코드는 다음을 사용하여 "암호화"됩니다:

- H1의 응답 키 (AES256/CBC)

- H1의 레코드는 대칭 암호화 없이 전송됩니다

H2만이 응답 암호화 플래그를 확인하고, 그 뒤에 AES256/CBC가 따라오는 것을 확인합니다.

각 홉에서 처리된 후, 레코드들은 "복호화된" 상태가 됩니다:

- H3의 레코드는 다음을 사용하여 "복호화"됩니다:

- H3의 응답 키 (AES256/CBC)

- H2의 레코드는 다음을 사용하여 "복호화"됩니다:

- H3의 응답 키 (AES256/CBC)
- H2의 응답 키 (ChaCha20-Poly1305)

- H1의 레코드는 다음을 사용하여 "복호화"됩니다:

- H3의 응답 키 (AES256/CBC)
- H2의 응답 키 (ChaCha20)
- H1의 응답 키 (AES256/CBC)

tunnel 생성자, 즉 Inbound Endpoint (IBEP)는 응답을 후처리합니다:

- H3의 레코드는 다음을 사용하여 "암호화"됩니다:

- H3의 응답 키 (AES256/CBC)

- H2의 레코드는 다음을 사용하여 "암호화"됩니다:

- H3의 응답 키 (AES256/CBC)
- H2의 응답 키 (ChaCha20-Poly1305)

- H1의 레코드는 다음을 사용하여 "암호화"됩니다:

- H3의 응답 키 (AES256/CBC)
- H2의 응답 키 (ChaCha20)
- H1의 응답 키 (AES256/CBC)

### 응답 암호화

이러한 키들은 ElGamal BuildRequestRecord에 명시적으로 포함됩니다. ECIES BuildRequestRecord의 경우, 터널 키와 AES 응답 키는 포함되지만, ChaCha 응답 키는 DH 교환에서 파생됩니다. 라우터 정적 ECIES 키의 세부사항은 [Proposal 156](/proposals/156-ecies-routers)을 참조하세요.

아래는 요청 레코드에서 이전에 전송된 키를 도출하는 방법에 대한 설명입니다.

#### KDF for Initial ck and h

이것은 표준 프로토콜 이름을 가진 패턴 "N"에 대한 표준 [NOISE](https://noiseprotocol.org/noise.html)입니다.

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

ElGamal tunnel 생성자는 tunnel의 각 ECIES hop에 대해 임시 X25519 키쌍을 생성하고, 위의 방식을 사용하여 BuildRequestRecord를 암호화합니다. ElGamal tunnel 생성자는 ElGamal hop으로 암호화할 때 이 사양 이전의 방식을 사용합니다.

ECIES tunnel 생성자는 [Tunnel Creation](/docs/specs/implementation/)에 정의된 방식을 사용하여 각 ElGamal hop의 공개 키로 암호화해야 합니다. ECIES tunnel 생성자는 ECIES hop으로 암호화할 때 위의 방식을 사용할 것입니다.

이는 터널 홉들이 동일한 암호화 유형의 암호화된 레코드만을 볼 수 있음을 의미합니다.

ElGamal과 ECIES tunnel 생성자의 경우, ECIES hop으로 암호화하기 위해 hop별로 고유한 임시 X25519 키쌍을 생성합니다.

**중요**: Ephemeral key는 ECIES hop별로, 그리고 빌드 레코드별로 고유해야 합니다. 고유한 키를 사용하지 않으면 공모하는 hop들이 동일한 터널에 있다는 것을 확인할 수 있는 공격 벡터가 열립니다.

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
``replyKey``, ``layerKey`` 그리고 ``layerIV``는 여전히 ElGamal 레코드 내부에 포함되어야 하며, 무작위로 생성할 수 있습니다.

### 정당화

[Tunnel Creation](/docs/specs/implementation/)에서 정의된 바와 같습니다. ElGamal hop에 대한 암호화 변경사항은 없습니다.

### Reply Record Encryption (ECIES)

응답 레코드는 ChaCha20/Poly1305로 암호화됩니다.

```text
// AEAD parameters
  k = chainkey from build request
  n = 0
  plaintext = 512 byte build reply record
  ad = h from build request

  ciphertext = ENCRYPT(k, n, plaintext, ad)
```
### 빌드 요청 레코드

[Tunnel Creation](/docs/specs/implementation/)에서 정의된 대로입니다. ElGamal hop에 대한 암호화 변경사항은 없습니다.

### Security Analysis

ElGamal은 터널 빌드 메시지에 대해 순방향 비밀성을 제공하지 않습니다.

AES256/CBC는 알려진 평문 `biclique` 공격으로부터의 이론적 약화에만 취약하므로 약간 더 나은 상태에 있습니다.

AES256/CBC에 대해 알려진 유일한 실용적인 공격은 IV가 공격자에게 알려졌을 때의 패딩 오라클 공격입니다.

공격자는 AES256/CBC 키 정보(응답 키 및 IV)를 획득하기 위해 다음 홉의 ElGamal 암호화를 해독해야 합니다.

ElGamal은 ECIES보다 CPU 집약적이어서 잠재적인 리소스 고갈을 야기할 수 있습니다.

ECIES는 BuildRequestRecord 또는 VariableTunnelBuildMessage마다 새로운 임시 키와 함께 사용되어 전방향 보안성을 제공합니다.

ChaCha20Poly1305는 AEAD 암호화를 제공하여 수신자가 복호화를 시도하기 전에 메시지 무결성을 검증할 수 있도록 합니다.

## 위협 모델

이 설계는 기존 암호화 프리미티브, 프로토콜 및 코드의 재사용을 극대화합니다. 이 설계는 위험을 최소화합니다.

## Implementation Notes

* 오래된 라우터는 홉의 암호화 타입을 확인하지 않고 ElGamal로 암호화된
  레코드를 전송합니다. 일부 최신 라우터에는 버그가 있어 다양한 유형의 잘못된 형식의 레코드를 전송할 수 있습니다.
  구현자들은 가능하다면 DH 연산 이전에 이러한 레코드들을 감지하고 거부하여
  CPU 사용량을 줄여야 합니다.

## Issues

## 설계

[Proposal 156](/proposals/156-ecies-routers)을 참조하세요.
