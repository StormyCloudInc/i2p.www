---
title: "RedDSA-BLAKE2b-Ed25519"
number: "148"
author: "zzz"
created: "2019-03-12"
lastupdated: "2019-04-11"
status: "打开"
thread: "http://zzz.i2p/topics/2689"
toc: true
---

## 概述

该提案添加了一种新的签名类型，使用带有个性化字符串和盐值的BLAKE2b-512来替代SHA-512。这将消除三类可能的攻击。

## 动机

在讨论和设计 NTCP2（提案 111）和 LS2（提案 123）期间，我们简要考虑了各种可能的攻击，以及如何防范它们。这些攻击中的三种是长度扩展攻击、跨协议攻击和重复消息识别。

对于NTCP2和LS2，我们认为这些攻击与当前的提案并不直接相关，任何解决方案都与最小化新原语的目标相冲突。此外，我们确定这些协议中哈希函数的速度并不是我们决策的重要因素。因此，我们主要将解决方案推迟到单独的提案中。虽然我们确实在LS2规范中添加了一些个性化功能，但我们没有要求任何新的哈希函数。

许多项目，例如 [ZCash](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)，正在使用基于较新算法的哈希函数和签名算法，这些算法不易受到以下攻击。

### Length Extension Attacks

SHA-256 和 SHA-512 容易受到[长度扩展攻击 (LEA)](https://en.wikipedia.org/wiki/Length_extension_attack)。当对实际数据进行签名而不是对数据的哈希进行签名时就会出现这种情况。在大多数 I2P 协议中（streaming、datagram、netDb 等），都是对实际数据进行签名。一个例外是 SU3 文件，其中对哈希进行签名。另一个例外是仅针对 DSA（签名类型 0）的签名数据报，其中对哈希进行签名。对于其他签名数据报签名类型，则对数据进行签名。

### Cross-Protocol Attacks

由于缺乏域分离，I2P协议中的签名数据可能容易受到跨协议攻击(CPA)的影响。这允许攻击者使用在一个上下文中接收到的数据（如签名数据报），并将其作为有效的签名数据在另一个上下文中（如流传输或网络数据库）呈现。虽然来自一个上下文的签名数据不太可能被解析为另一个上下文中的有效数据，但要分析所有情况以确保安全是困难或不可能的。此外，在某些情况下，攻击者可能诱导受害者签署特制的数据，这些数据在另一个上下文中可能是有效数据。同样，要分析所有情况以确保安全是困难或不可能的。

### 长度扩展攻击

I2P协议可能容易受到重复消息识别(DMI)攻击。这可能允许攻击者识别两个签名消息具有相同内容，即使这些消息及其签名都是加密的。虽然由于I2P中使用的加密方法，这种情况不太可能发生，但很难或不可能分析所有情况来确保安全。通过使用提供添加随机盐方法的哈希函数，即使在签署相同数据时，所有签名都会不同。虽然提案123中定义的Red25519为哈希函数添加了随机盐，但这并不能解决未加密leaseSet的问题。

### 跨协议攻击

虽然这不是本提案的主要动机，但 SHA-512 相对较慢，而且有更快的哈希函数可用。

## Goals

- 防止上述攻击
- 最小化使用新的加密原语
- 使用经过验证的标准加密原语
- 使用标准曲线
- 如果可用，使用更快的原语

## Design

修改现有的 RedDSA_SHA512_Ed25519 签名类型，使用 BLAKE2b-512 替代 SHA-512。为每个用例添加唯一的个性化字符串。新的签名类型可用于未盲化和盲化的 leaseSet。

## Justification

- [BLAKE2b](https://blake2.net/blake2.pdf) 不易受到 LEA 攻击。
- BLAKE2b 提供了添加个性化字符串进行域分离的标准方法
- BLAKE2b 提供了添加随机盐以防止 DMI 的标准方法。
- 根据 [BLAKE2 规范](https://blake2.net/blake2.pdf)，BLAKE2b 在现代硬件上比 SHA-256 和 SHA-512（以及 MD5）更快。
- Ed25519 仍然是我们最快的签名类型，比 ECDSA 快得多，至少在 Java 中如此。
- [Ed25519](http://cr.yp.to/papers.html#ed25519) 需要 512 位加密哈希函数。
  它没有指定 SHA-512。BLAKE2b 同样适合作为哈希函数。
- BLAKE2b 在许多编程语言的库中广泛可用，比如 Noise。

## Specification

使用未加密的 BLAKE2b-512，如 [BLAKE2 规范](https://blake2.net/blake2.pdf) 中所述，包含盐值和个性化参数。所有 BLAKE2b 签名的使用都将采用 16 字符的个性化字符串。

在RedDSA_BLAKE2b_Ed25519签名中使用时，允许使用随机盐值，但这并不是必需的，因为签名算法会添加80字节的随机数据（参见提案123）。如果需要，在对数据进行哈希计算r时，为每个签名设置一个新的BLAKE2b 16字节随机盐值。在计算S时，将盐值重置为默认的全零值。

当用于 RedDSA_BLAKE2b_Ed25519 验证时，不要使用随机盐值，使用全零的默认值。

盐值和个性化功能在 [RFC 7693](https://tools.ietf.org/html/rfc7693) 中未指定；请按照 [BLAKE2 规范](https://blake2.net/blake2.pdf) 中的规定使用这些功能。

### 重复消息识别

对于 RedDSA_BLAKE2b_Ed25519，将 RedDSA_SHA512_Ed25519（签名类型 11，如提案 123 中定义）中的 SHA-512 哈希函数替换为 BLAKE2b-512。无其他更改。

我们不需要为 su3 文件替换 EdDSA_SHA512_Ed25519ph（签名类型 8），因为 EdDSA 的预哈希版本不易受到 LEA 攻击。su3 文件不支持 EdDSA_SHA512_Ed25519（签名类型 7）。

| Type | Type Code | Since | Usage |
|------|-----------|-------|-------|
| RedDSA_BLAKE2b_Ed25519 | 12 | TBD | For Router Identities, Destinations and encrypted leasesets only; never used for Router Identities |
### 速度

以下适用于新的签名类型。

| Data Type | Length |
|-----------|--------|
| Hash | 64 |
| Private Key | 32 |
| Public Key | 32 |
| Signature | 64 |
### Personalizations

为了为签名的各种用途提供域分离，我们将使用 BLAKE2b 个性化功能。

所有 BLAKE2b 签名的使用都将采用 16 字符的个性化字符串。任何新的使用都必须添加到此表格中，并使用唯一的个性化字符串。

下面使用的 NTCP 1 和 SSU 握手是为握手本身中定义的签名数据。DatabaseStore 消息中的签名 RouterInfo 将使用 NetDb Entry 个性化，就像存储在 NetDB 中一样。

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
## 目标

## 设计

- 替代方案 1：提案 146；
  提供 LEA 抗性
- 替代方案 2：[RFC 8032 中的 Ed25519ctx](https://tools.ietf.org/html/rfc8032)；
  提供 LEA 抗性和个性化。
  已标准化，但有人使用吗？
  参见 [RFC 8032](https://tools.ietf.org/html/rfc8032) 和[此讨论](https://moderncrypto.org/mail-archive/curves/2017/000925.html)。
- "keyed" 哈希对我们有用吗？

## 理由说明

与之前签名类型的推出过程相同。

我们计划将新 router 的默认类型从 type 7 更改为 type 12。我们计划最终使用在引入 type 7 后使用的"重新密钥"过程，将现有 router 从 type 7 迁移到 type 12。我们计划将新目的地的默认类型从 type 7 更改为 type 12。我们计划将新加密目的地的默认类型从 type 11 更改为 type 13。

我们将支持从类型 7、11 和 12 到类型 12 的盲化。我们不会支持从类型 12 到类型 11 的盲化。

新的 router 可以在几个月后开始默认使用新的签名类型。新的目标地址可以在大约一年后开始默认使用新的签名类型。

对于最低 router 版本 0.9.TBD，router 必须确保：

- 不要向版本低于 0.9.TBD 的 router 存储（或泛洪）使用新签名类型的 RI 或 LS。
- 在验证 netDb 存储时，不要从版本低于 0.9.TBD 的 router 获取使用新签名类型的 RI 或 LS。
- 在其 RI 中使用新签名类型的 router 可能无法连接到版本低于 0.9.TBD 的 router，
  无论是通过 NTCP、NTCP2 还是 SSU。
- 流连接和签名数据报无法与版本低于 0.9.TBD 的 router 正常工作，
  但没有办法知道这一点，所以在 0.9.TBD 发布后的几个月或几年内，新签名类型不应该默认使用。
