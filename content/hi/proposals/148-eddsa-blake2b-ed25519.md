---
title: "RedDSA-BLAKE2b-Ed25519"
number: "148"
author: "zzz"
created: "2019-03-12"
lastupdated: "2019-04-11"
status: "खुला"
thread: "http://zzz.i2p/topics/2689"
---

## अवलोकन

यह प्रस्ताव BLAKE2b-512 का उपयोग करके personalization strings और salts के साथ एक नया signature type जोड़ता है, जो SHA-512 को बदल देगा। इससे संभावित हमलों की तीन श्रेणियां समाप्त हो जाएंगी।

## प्रेरणा

NTCP2 (प्रस्ताव 111) और LS2 (प्रस्ताव 123) की चर्चा और डिज़ाइन के दौरान, हमने संक्षेप में विभिन्न हमलों पर विचार किया जो संभव थे, और उन्हें कैसे रोकना है। इन तीन हमलों में Length Extension Attacks, Cross-Protocol Attacks, और Duplicate Message Identification हैं।

NTCP2 और LS2 दोनों के लिए, हमने निर्णय लिया कि ये हमले प्रस्तावित प्रस्तावों के लिए प्रत्यक्ष रूप से प्रासंगिक नहीं थे, और कोई भी समाधान नए primitives को न्यूनतम रखने के लक्ष्य के साथ संघर्ष में था। इसके अलावा, हमने निर्धारित किया कि इन प्रोटोकॉल में hash functions की गति हमारे निर्णयों में एक महत्वपूर्ण कारक नहीं थी। इसलिए, हमने अधिकतर समाधान को एक अलग प्रस्ताव के लिए स्थगित कर दिया। जबकि हमने LS2 specification में कुछ personalization सुविधाएं जोड़ीं, हमें किसी भी नए hash functions की आवश्यकता नहीं थी।

कई परियोजनाएं, जैसे [ZCash](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf), नवीन algorithms पर आधारित hash functions और signature algorithms का उपयोग कर रही हैं जो निम्नलिखित हमलों के लिए संवेदनशील नहीं हैं।

### Length Extension Attacks

SHA-256 और SHA-512 [Length Extension Attacks (LEA)](https://en.wikipedia.org/wiki/Length_extension_attack) के लिए संवेदनशील हैं। यह तब होता है जब वास्तविक डेटा पर हस्ताक्षर किए जाते हैं, डेटा के hash पर नहीं। अधिकांश I2P protocols (streaming, datagrams, netDb, और अन्य) में, वास्तविक डेटा पर हस्ताक्षर किए जाते हैं। एक अपवाद SU3 files हैं, जहाँ hash पर हस्ताक्षर किए जाते हैं। दूसरा अपवाद केवल DSA (sig type 0) के लिए signed datagrams हैं, जहाँ hash पर हस्ताक्षर किए जाते हैं। अन्य signed datagram sig types के लिए, डेटा पर हस्ताक्षर किए जाते हैं।

### Cross-Protocol Attacks

I2P प्रोटोकॉल में signed data domain separation की कमी के कारण Cross-Protocol Attacks (CPA) के लिए संवेदनशील हो सकता है। यह एक आक्रमणकारी को एक संदर्भ में प्राप्त डेटा (जैसे कि एक signed datagram) का उपयोग करने और इसे दूसरे संदर्भ में (जैसे कि streaming या network database) वैध, signed डेटा के रूप में प्रस्तुत करने की अनुमति देता है। हालांकि यह असंभावित है कि एक संदर्भ से signed डेटा को दूसरे संदर्भ में वैध डेटा के रूप में parsed किया जाए, सभी स्थितियों का विश्लेषण करना कठिन या असंभव है कि निश्चित रूप से पता चल सके। इसके अतिरिक्त, कुछ संदर्भों में, एक आक्रमणकारी के लिए पीड़ित को विशेष रूप से तैयार किए गए डेटा पर हस्ताक्षर करने के लिए प्रेरित करना संभव हो सकता है जो दूसरे संदर्भ में वैध डेटा हो सकता है। फिर से, सभी स्थितियों का विश्लेषण करना कठिन या असंभव है कि निश्चित रूप से पता चल सके।

### Length Extension हमले

I2P protocols Duplicate Message Identification (DMI) के लिए संवेदनशील हो सकते हैं। यह किसी आक्रमणकारी को पहचानने की अनुमति दे सकता है कि दो signed messages में समान content है, भले ही ये messages और उनके signatures encrypted हों। जबकि I2P में उपयोग की जाने वाली encryption methods के कारण यह संभावना कम है, सभी स्थितियों का विश्लेषण करना कठिन या असंभव है ताकि निश्चित रूप से पता चल सके। एक hash function का उपयोग करके जो random salt जोड़ने की विधि प्रदान करता है, सभी signatures अलग होंगे भले ही समान data को sign किया जा रहा हो। जबकि proposal 123 में परिभाषित Red25519 hash function में random salt जोड़ता है, यह unencrypted lease sets के लिए समस्या का समाधान नहीं करता है।

### क्रॉस-प्रोटोकॉल अटैक

जबकि यह इस प्रस्ताव की मुख्य प्रेरणा नहीं है, SHA-512 अपेक्षाकृत धीमा है, और तेज़ hash functions उपलब्ध हैं।

## Goals

- उपरोक्त हमलों को रोकना
- नए crypto primitives का उपयोग कम से कम करना
- सिद्ध, मानक crypto primitives का उपयोग करना
- मानक curves का उपयोग करना
- यदि उपलब्ध हो तो तेज़ primitives का उपयोग करना

## Design

मौजूदा RedDSA_SHA512_Ed25519 signature प्रकार को SHA-512 के बजाय BLAKE2b-512 का उपयोग करने के लिए संशोधित करें। प्रत्येक उपयोग मामले के लिए अनूठी personalization strings जोड़ें। नया signature प्रकार unblinded और blinded दोनों leasesets के लिए उपयोग किया जा सकता है।

## Justification

- [BLAKE2b](https://blake2.net/blake2.pdf) LEA के लिए vulnerable नहीं है।
- BLAKE2b domain separation के लिए personalization strings जोड़ने का एक मानक तरीका प्रदान करता है
- BLAKE2b DMI को रोकने के लिए random salt जोड़ने का एक मानक तरीका प्रदान करता है।
- BLAKE2b आधुनिक hardware पर SHA-256 और SHA-512 (और MD5) से तेज़ है,
  [BLAKE2 specification](https://blake2.net/blake2.pdf) के अनुसार।
- Ed25519 अभी भी हमारा सबसे तेज़ signature type है, कम से कम Java में ECDSA से बहुत तेज़।
- [Ed25519](http://cr.yp.to/papers.html#ed25519) को 512 bit cryptographic hash function की आवश्यकता होती है।
  यह SHA-512 specify नहीं करता। BLAKE2b hash function के लिए उतना ही suitable है।
- BLAKE2b कई programming languages की libraries में व्यापक रूप से उपलब्ध है, जैसे Noise।

## Specification

[BLAKE2 specification](https://blake2.net/blake2.pdf) में दिए गए अनुसार salt और personalization के साथ unkeyed BLAKE2b-512 का उपयोग करें। BLAKE2b signatures के सभी उपयोग 16-character personalization string का उपयोग करेंगे।

जब RedDSA_BLAKE2b_Ed25519 signing में उपयोग किया जाता है, तो एक random salt की अनुमति है, हालांकि यह आवश्यक नहीं है, क्योंकि signature algorithm 80 bytes का random data जोड़ता है (proposal 123 देखें)। यदि वांछित हो, तो r की गणना के लिए data को hash करते समय, प्रत्येक signature के लिए एक नया BLAKE2b 16-byte random salt सेट करें। S की गणना करते समय, salt को सभी-zeros के default पर reset करें।

जब RedDSA_BLAKE2b_Ed25519 verification में उपयोग किया जाए, तो random salt का उपयोग न करें, सभी-शून्य के default का उपयोग करें।

salt और personalization सुविधाएं [RFC 7693](https://tools.ietf.org/html/rfc7693) में निर्दिष्ट नहीं हैं; उन सुविधाओं का उपयोग [BLAKE2 specification](https://blake2.net/blake2.pdf) में निर्दिष्ट अनुसार करें।

### डुप्लिकेट संदेश पहचान

RedDSA_BLAKE2b_Ed25519 के लिए, RedDSA_SHA512_Ed25519 (signature type 11, जैसा कि proposal 123 में परिभाषित है) में SHA-512 hash function को BLAKE2b-512 से बदलें। कोई अन्य परिवर्तन नहीं।

हमें su3 फाइलों के लिए EdDSA_SHA512_Ed25519ph (signature type 8) के प्रतिस्थापन की आवश्यकता नहीं है, क्योंकि EdDSA का prehashed संस्करण LEA के लिए संवेदनशील नहीं है। EdDSA_SHA512_Ed25519 (signature type 7) su3 फाइलों के लिए समर्थित नहीं है।

| Type | Type Code | Since | Usage |
|------|-----------|-------|-------|
| RedDSA_BLAKE2b_Ed25519 | 12 | TBD | For Router Identities, Destinations and encrypted leasesets only; never used for Router Identities |
### गति

निम्नलिखित नए signature type पर लागू होता है।

| Data Type | Length |
|-----------|--------|
| Hash | 64 |
| Private Key | 32 |
| Public Key | 32 |
| Signature | 64 |
### Personalizations

signatures के विभिन्न उपयोगों के लिए domain separation प्रदान करने हेतु, हम BLAKE2b personalization feature का उपयोग करेंगे।

BLAKE2b signatures के सभी उपयोग 16-वर्ण का personalization string उपयोग करेंगे। किसी भी नए उपयोग को यहाँ तालिका में unique personalization के साथ जोड़ा जाना चाहिए।

NTCP 1 और SSU handshake जो नीचे उपयोग किए गए हैं, वे handshake में ही परिभाषित signed data के लिए हैं। DatabaseStore Messages में Signed RouterInfos NetDb Entry personalization का उपयोग करेंगे, बिल्कुल वैसे ही जैसे कि NetDB में stored हों।

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
## लक्ष्य

## डिज़ाइन

- वैकल्पिक 1: प्रस्ताव 146;
  LEA प्रतिरोध प्रदान करता है
- वैकल्पिक 2: [RFC 8032 में Ed25519ctx](https://tools.ietf.org/html/rfc8032);
  LEA प्रतिरोध और व्यक्तिकरण प्रदान करता है।
  मानकीकृत है, लेकिन क्या कोई इसका उपयोग करता है?
  देखें [RFC 8032](https://tools.ietf.org/html/rfc8032) और [यह चर्चा](https://moderncrypto.org/mail-archive/curves/2017/000925.html)।
- क्या "keyed" hashing हमारे लिए उपयोगी है?

## औचित्य

पिछले signature प्रकारों के rollout के समान।

हमारी योजना है कि नए routers को type 7 से type 12 में default के रूप में बदला जाए। हमारी योजना है कि अंततः मौजूदा routers को type 7 से type 12 में migrate किया जाए, उस "rekeying" प्रक्रिया का उपयोग करके जो type 7 के आने के बाद इस्तेमाल की गई थी। हमारी योजना है कि नए destinations को type 7 से type 12 में default के रूप में बदला जाए। हमारी योजना है कि नए encrypted destinations को type 11 से type 13 में default के रूप में बदला जाए।

हम टाइप 7, 11, और 12 से टाइप 12 तक blinding का समर्थन करेंगे। हम टाइप 12 से टाइप 11 तक blinding का समर्थन नहीं करेंगे।

नए router कुछ महीनों बाद डिफ़ॉल्ट रूप से नए sig type का उपयोग करना शुरू कर सकते हैं। नए destinations शायद एक साल बाद डिफ़ॉल्ट रूप से नए sig type का उपयोग करना शुरू कर सकते हैं।

न्यूनतम router संस्करण 0.9.TBD के लिए, routers को यह सुनिश्चित करना चाहिए:

- नई sig type के साथ RI या LS को version 0.9.TBD से कम वाले routers में store (या flood) न करें।
- netdb store को verify करते समय, version 0.9.TBD से कम वाले routers से नई sig type के साथ RI या LS को fetch न करें।
- अपने RI में नई sig type वाले routers version 0.9.TBD से कम वाले routers से connect नहीं हो सकते,
  चाहे NTCP, NTCP2, या SSU के साथ हो।
- Streaming connections और signed datagrams version 0.9.TBD से कम वाले routers के साथ काम नहीं करेंगे,
  लेकिन यह जानने का कोई तरीका नहीं है, इसलिए 0.9.TBD release होने के बाद कुछ महीनों या सालों तक
  नई sig type को default रूप से उपयोग नहीं करना चाहिए।
