---
title: "RedDSA-BLAKE2b-Ed25519"
number: "148"
author: "zzz"
created: "2019-03-12"
lastupdated: "2019-04-11"
status: "열기"
thread: "http://zzz.i2p/topics/2689"
---

## 개요

이 제안은 개인화 문자열과 솔트를 사용하는 BLAKE2b-512를 이용한 새로운 서명 타입을 추가하여 SHA-512를 대체합니다. 이를 통해 세 가지 유형의 가능한 공격을 제거할 것입니다.

## 동기

NTCP2 (제안 111)와 LS2 (제안 123)의 논의 및 설계 과정에서, 우리는 가능한 다양한 공격들과 이를 방지하는 방법에 대해 간략히 고려했습니다. 이러한 공격 중 세 가지는 길이 확장 공격(Length Extension Attacks), 교차 프로토콜 공격(Cross-Protocol Attacks), 그리고 중복 메시지 식별(Duplicate Message Identification)입니다.

NTCP2와 LS2 모두에 대해, 우리는 이러한 공격들이 당면한 제안들과 직접적으로 관련이 없으며, 어떤 해결책도 새로운 기본 요소를 최소화한다는 목표와 상충된다고 판단했습니다. 또한, 우리는 이러한 프로토콜에서 해시 함수의 속도가 우리 결정에 중요한 요소가 아니라고 판단했습니다. 따라서 우리는 대부분 해결책을 별도의 제안으로 미루었습니다. LS2 사양에 일부 개인화 기능을 추가하기는 했지만, 새로운 해시 함수는 요구하지 않았습니다.

많은 프로젝트들, 예를 들어 [ZCash](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)와 같은 프로젝트들은 다음과 같은 공격에 취약하지 않은 최신 알고리즘 기반의 해시 함수와 서명 알고리즘을 사용하고 있습니다.

### Length Extension Attacks

SHA-256과 SHA-512은 [길이 확장 공격(Length Extension Attacks, LEA)](https://en.wikipedia.org/wiki/Length_extension_attack)에 취약합니다. 이는 데이터의 해시가 아닌 실제 데이터가 서명될 때 발생하는 경우입니다. 대부분의 I2P 프로토콜(스트리밍, 데이터그램, netDb 및 기타)에서는 실제 데이터가 서명됩니다. 한 가지 예외는 해시가 서명되는 SU3 파일입니다. 다른 예외는 해시가 서명되는 DSA(sig type 0)에 대해서만 해당하는 서명된 데이터그램입니다. 다른 서명된 데이터그램 sig type의 경우 데이터가 서명됩니다.

### Cross-Protocol Attacks

I2P 프로토콜에서 서명된 데이터는 도메인 분리의 부족으로 인해 Cross-Protocol Attack(CPA)에 취약할 수 있습니다. 이는 공격자가 한 컨텍스트(서명된 데이터그램 등)에서 수신한 데이터를 다른 컨텍스트(스트리밍이나 network database 등)에서 유효한 서명된 데이터로 제시할 수 있게 합니다. 한 컨텍스트의 서명된 데이터가 다른 컨텍스트에서 유효한 데이터로 파싱될 가능성은 낮지만, 모든 상황을 분석하여 확실히 알기는 어렵거나 불가능합니다. 또한 일부 컨텍스트에서는 공격자가 피해자로 하여금 다른 컨텍스트에서 유효한 데이터가 될 수 있는 특별히 제작된 데이터에 서명하도록 유도할 수 있습니다. 마찬가지로 모든 상황을 분석하여 확실히 알기는 어렵거나 불가능합니다.

### 길이 확장 공격

I2P 프로토콜은 중복 메시지 식별(DMI)에 취약할 수 있습니다. 이로 인해 공격자가 메시지와 서명이 암호화되어 있더라도 서명된 두 메시지가 동일한 내용을 가지고 있음을 식별할 수 있습니다. I2P에서 사용되는 암호화 방법으로 인해 가능성은 낮지만, 모든 상황을 분석하여 확실히 알기는 어렵거나 불가능합니다. 무작위 salt를 추가하는 방법을 제공하는 해시 함수를 사용함으로써, 동일한 데이터를 서명할 때도 모든 서명이 달라집니다. 제안서 123에서 정의된 Red25519는 해시 함수에 무작위 salt를 추가하지만, 이는 암호화되지 않은 leaseSet에 대한 문제를 해결하지 못합니다.

### 교차 프로토콜 공격

이 제안의 주요 동기는 아니지만, SHA-512는 상대적으로 느리며 더 빠른 해시 함수들이 사용 가능합니다.

## Goals

- 위 공격들을 방지
- 새로운 암호화 primitives 사용 최소화
- 검증되고 표준적인 암호화 primitives 사용
- 표준 곡선 사용
- 가능한 경우 더 빠른 primitives 사용

## Design

기존 RedDSA_SHA512_Ed25519 서명 유형을 SHA-512 대신 BLAKE2b-512를 사용하도록 수정합니다. 각 사용 사례에 대해 고유한 개인화 문자열을 추가합니다. 새로운 서명 유형은 블라인드되지 않은 leaseSet과 블라인드된 leaseSet 모두에 사용될 수 있습니다.

## Justification

- [BLAKE2b](https://blake2.net/blake2.pdf)는 LEA에 취약하지 않습니다.
- BLAKE2b는 도메인 분리를 위한 개인화 문자열을 추가하는 표준 방법을 제공합니다
- BLAKE2b는 DMI를 방지하기 위해 랜덤 솔트를 추가하는 표준 방법을 제공합니다.
- BLAKE2b는 [BLAKE2 명세서](https://blake2.net/blake2.pdf)에 따르면 최신 하드웨어에서 SHA-256과 SHA-512 (그리고 MD5)보다 빠릅니다.
- Ed25519는 여전히 우리가 사용하는 가장 빠른 서명 유형으로, 적어도 Java에서는 ECDSA보다 훨씬 빠릅니다.
- [Ed25519](http://cr.yp.to/papers.html#ed25519)는 512비트 암호화 해시 함수가 필요합니다.
  SHA-512를 명시하지는 않습니다. BLAKE2b도 해시 함수로 똑같이 적합합니다.
- BLAKE2b는 Noise와 같은 많은 프로그래밍 언어의 라이브러리에서 널리 사용 가능합니다.

## Specification

[BLAKE2 사양](https://blake2.net/blake2.pdf)에서와 같이 salt와 personalization을 사용하는 키가 없는 BLAKE2b-512를 사용합니다. BLAKE2b 서명의 모든 사용은 16자 personalization 문자열을 사용합니다.

RedDSA_BLAKE2b_Ed25519 서명에서 사용될 때, 랜덤 솔트가 허용되지만 필수는 아닙니다. 서명 알고리즘이 80바이트의 랜덤 데이터를 추가하기 때문입니다 (제안서 123 참조). 원한다면, r을 계산하기 위해 데이터를 해싱할 때 각 서명마다 새로운 BLAKE2b 16바이트 랜덤 솔트를 설정하세요. S를 계산할 때는 솔트를 모두 0인 기본값으로 재설정하세요.

RedDSA_BLAKE2b_Ed25519 검증에 사용될 때는 무작위 솔트를 사용하지 말고, 모든 값이 0인 기본값을 사용하십시오.

salt와 personalization 기능은 [RFC 7693](https://tools.ietf.org/html/rfc7693)에 명시되어 있지 않습니다. 이러한 기능은 [BLAKE2 specification](https://blake2.net/blake2.pdf)에 명시된 대로 사용하십시오.

### 중복 메시지 식별

RedDSA_BLAKE2b_Ed25519의 경우, RedDSA_SHA512_Ed25519(제안 123에 정의된 서명 타입 11)의 SHA-512 해시 함수를 BLAKE2b-512로 교체합니다. 다른 변경 사항은 없습니다.

su3 파일의 경우 EdDSA_SHA512_Ed25519ph (서명 타입 8)에 대한 대체가 필요하지 않습니다. EdDSA의 사전 해시 버전은 LEA에 취약하지 않기 때문입니다. EdDSA_SHA512_Ed25519 (서명 타입 7)은 su3 파일에서 지원되지 않습니다.

| Type | Type Code | Since | Usage |
|------|-----------|-------|-------|
| RedDSA_BLAKE2b_Ed25519 | 12 | TBD | For Router Identities, Destinations and encrypted leasesets only; never used for Router Identities |
### 속도

다음은 새로운 서명 유형에 적용됩니다.

| Data Type | Length |
|-----------|--------|
| Hash | 64 |
| Private Key | 32 |
| Public Key | 32 |
| Signature | 64 |
### Personalizations

서명의 다양한 용도에 대한 도메인 분리를 제공하기 위해 BLAKE2b 개인화 기능을 사용할 것입니다.

BLAKE2b 서명의 모든 사용은 16자리 개인화 문자열을 사용합니다. 새로운 사용 사례는 고유한 개인화와 함께 여기 표에 추가되어야 합니다.

아래 사용되는 NTCP 1 및 SSU handshake는 handshake 자체에서 정의된 서명된 데이터를 위한 것입니다. DatabaseStore 메시지의 서명된 RouterInfo들은 NetDB에 저장된 것처럼 NetDb Entry 개인화를 사용할 것입니다.

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
## 목표

## 설계

- 대안 1: Proposal 146;
  LEA 저항성 제공
- 대안 2: [RFC 8032의 Ed25519ctx](https://tools.ietf.org/html/rfc8032);
  LEA 저항성과 개인화 기능 제공.
  표준화되었지만, 실제로 사용하는 곳이 있나?
  [RFC 8032](https://tools.ietf.org/html/rfc8032)와 [이 토론](https://moderncrypto.org/mail-archive/curves/2017/000925.html) 참조.
- "키가 있는" 해싱이 우리에게 유용한가?

## 정당화

이전 서명 유형들의 롤아웃과 동일합니다.

새로운 router를 기본값으로 type 7에서 type 12로 변경할 계획입니다. type 7이 도입된 후 사용된 "rekeying" 프로세스를 사용하여 기존 router를 type 7에서 type 12로 최종 마이그레이션할 계획입니다. 새로운 destination을 기본값으로 type 7에서 type 12로 변경할 계획입니다. 새로운 암호화된 destination을 기본값으로 type 11에서 type 13으로 변경할 계획입니다.

우리는 타입 7, 11, 12에서 타입 12로의 블라인딩을 지원할 것입니다. 타입 12에서 타입 11로의 블라인딩은 지원하지 않을 것입니다.

몇 달 후부터는 새로운 router들이 기본적으로 새로운 서명 타입을 사용하기 시작할 수 있습니다. 새로운 destination들은 아마도 1년 후부터 기본적으로 새로운 서명 타입을 사용하기 시작할 수 있습니다.

최소 router 버전 0.9.TBD의 경우, router들은 다음을 보장해야 합니다:

- 버전 0.9.TBD 미만의 router에는 새로운 sig type을 가진 RI 또는 LS를 저장(또는 flood)하지 마십시오.
- netdb store를 검증할 때, 버전 0.9.TBD 미만의 router에서 새로운 sig type을 가진 RI 또는 LS를 가져오지 마십시오.
- RI에 새로운 sig type을 가진 router는 NTCP, NTCP2, 또는 SSU를 통해 버전 0.9.TBD 미만의 router에 연결하지 않을 수 있습니다.
- 스트리밍 연결과 서명된 datagram은 버전 0.9.TBD 미만의 router에서 작동하지 않지만,
  이를 알 방법이 없으므로 새로운 sig type은 0.9.TBD가 릴리스된 후 몇 개월 또는 몇 년 동안
  기본적으로 사용되어서는 안 됩니다.
