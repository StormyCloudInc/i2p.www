---
title: "RedDSA-BLAKE2b-Ed25519"
number: "148"
author: "zzz"
created: "2019-03-12"
lastupdated: "2019-04-11"
status: "Açık"
thread: "http://zzz.i2p/topics/2689"
toc: true
---

## Genel Bakış

Bu öneri, SHA-512'yi değiştirmek için kişiselleştirme dizgileri ve tuzlarla birlikte BLAKE2b-512 kullanan yeni bir imza türü ekler. Bu, olası üç saldırı sınıfını ortadan kaldıracaktır.

## Motivasyon

NTCP2 (öneri 111) ve LS2 (öneri 123) tartışmaları ve tasarımı sırasında, mümkün olan çeşitli saldırıları ve bunları nasıl önleyeceğimizi kısaca değerlendirdik. Bu saldırılardan üçü Uzunluk Genişletme Saldırıları, Çapraz Protokol Saldırıları ve Yinelenen Mesaj Tanımlamasıdır.

Hem NTCP2 hem de LS2 için, bu saldırıların eldeki önerilere doğrudan ilgili olmadığına ve herhangi bir çözümün yeni primitifleri minimize etme hedefiyle çeliştiğine karar verdik. Ayrıca, bu protokollerdeki hash fonksiyonlarının hızının kararlarımızda önemli bir faktör olmadığını belirledik. Bu nedenle, çözümü çoğunlukla ayrı bir öneriye erteledik. LS2 spesifikasyonuna bazı kişiselleştirme özellikleri eklemekle birlikte, herhangi bir yeni hash fonksiyonu gerektirmedik.

Birçok proje, [ZCash](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) gibi, aşağıdaki saldırılara karşı savunmasız olmayan yeni algoritmalara dayalı hash fonksiyonları ve imza algoritmaları kullanmaktadır.

### Length Extension Attacks

SHA-256 ve SHA-512, [Uzunluk Genişletme Saldırılarına (LEA)](https://en.wikipedia.org/wiki/Length_extension_attack) karşı savunmasızdır. Bu durum, verinin hash'i değil, gerçek verinin imzalandığı durumlarda geçerlidir. Çoğu I2P protokolünde (streaming, datagramlar, netDb ve diğerleri), gerçek veri imzalanır. Bir istisna, hash'in imzalandığı SU3 dosyalarıdır. Diğer istisna ise yalnızca DSA (sig türü 0) için imzalanmış datagrams'lardır; burada hash imzalanır. Diğer imzalanmış datagram sig türleri için ise veri imzalanır.

### Cross-Protocol Attacks

I2P protokollerindeki imzalı veriler, domain ayrımının olmaması nedeniyle Cross-Protocol Attacks (CPA) saldırılarına karşı savunmasız olabilir. Bu durum, bir saldırganın bir bağlamda (imzalı datagram gibi) alınan veriyi başka bir bağlamda (streaming veya network database gibi) geçerli, imzalı veri olarak sunmasına olanak tanır. Bir bağlamdan gelen imzalı verinin başka bir bağlamda geçerli veri olarak ayrıştırılması olasılığı düşük olsa da, tüm durumları analiz ederek kesin olarak bilmek zor veya imkansızdır. Ek olarak, bazı bağlamlarda bir saldırganın kurbanı başka bir bağlamda geçerli veri olabilecek özel olarak hazırlanmış veriyi imzalamaya yönlendirebilmesi mümkün olabilir. Yine, tüm durumları analiz ederek kesin olarak bilmek zor veya imkansızdır.

### Uzunluk Genişletme Saldırıları

I2P protokolleri Duplicate Message Identification (DMI) saldırısına karşı savunmasız olabilir. Bu, bir saldırganın iki imzalı mesajın aynı içeriğe sahip olduğunu, bu mesajlar ve imzaları şifrelenmiş olsa bile tespit etmesine olanak tanıyabilir. I2P'de kullanılan şifreleme yöntemleri nedeniyle olası olmasa da, emin olmak için tüm durumları analiz etmek zor veya imkansızdır. Rastgele salt ekleme yöntemi sağlayan bir hash fonksiyonu kullanarak, aynı veri imzalanırken bile tüm imzalar farklı olacaktır. 123 numaralı öneride tanımlandığı üzere Red25519 hash fonksiyonuna rastgele salt eklemesine rağmen, bu şifrelenmemiş lease set'ler için sorunu çözmez.

### Protokoller Arası Saldırılar

Bu öneri için birincil motivasyon olmasa da, SHA-512 nispeten yavaştır ve daha hızlı hash fonksiyonları mevcuttur.

## Goals

- Yukarıdaki saldırıları önlemek
- Yeni kripto ilkellerinin kullanımını minimize etmek
- Kanıtlanmış, standart kripto ilkelerini kullanmak
- Standart eğrileri kullanmak
- Mevcut ise daha hızlı ilkeleri kullanmak

## Design

Mevcut RedDSA_SHA512_Ed25519 imza türünü SHA-512 yerine BLAKE2b-512 kullanacak şekilde değiştirin. Her kullanım durumu için benzersiz kişiselleştirme dizeleri ekleyin. Yeni imza türü hem köreltilmemiş hem de köreltilmiş leaseSet'ler için kullanılabilir.

## Justification

- [BLAKE2b](https://blake2.net/blake2.pdf) LEA'ya karşı savunmasız değildir.
- BLAKE2b, alan ayrımı için kişiselleştirme dizileri eklemenin standart bir yolunu sağlar
- BLAKE2b, DMI'yi önlemek için rastgele tuz eklemenin standart bir yolunu sağlar
- BLAKE2b, [BLAKE2 spesifikasyonuna](https://blake2.net/blake2.pdf) göre modern donanımda SHA-256 ve SHA-512'den (ve MD5'ten) daha hızlıdır.
- Ed25519 hala en hızlı imza türümüz olup, en azından Java'da ECDSA'dan çok daha hızlıdır.
- [Ed25519](http://cr.yp.to/papers.html#ed25519) 512 bit kriptografik hash fonksiyonu gerektirir.
  SHA-512'yi belirtmez. BLAKE2b hash fonksiyonu için aynı derecede uygundur.
- BLAKE2b, Noise gibi birçok programlama dili için kütüphanelerde yaygın olarak mevcuttur.

## Specification

[BLAKE2 spesifikasyonunda](https://blake2.net/blake2.pdf) belirtildiği gibi tuz ve kişiselleştirme ile anahtarsız BLAKE2b-512 kullanın. BLAKE2b imzalarının tüm kullanımları 16 karakterlik bir kişiselleştirme dizesi kullanacaktır.

RedDSA_BLAKE2b_Ed25519 imzalamasında kullanıldığında, rastgele bir salt'a izin verilir, ancak bu gerekli değildir, çünkü imza algoritması 80 bayt rastgele veri ekler (önerge 123'e bakın). İstenirse, r'yi hesaplamak için veriyi hash'lerken, her imza için yeni bir BLAKE2b 16-bayt rastgele salt ayarlayın. S'yi hesaplarken, salt'ı varsayılan olan tamamı sıfır değerine sıfırlayın.

RedDSA_BLAKE2b_Ed25519 doğrulamasında kullanıldığında, rastgele bir salt kullanmayın, varsayılan olan tamamen sıfırları kullanın.

Salt ve kişiselleştirme özellikleri [RFC 7693](https://tools.ietf.org/html/rfc7693)'te belirtilmemiştir; bu özellikleri [BLAKE2 spesifikasyonu](https://blake2.net/blake2.pdf)'nda belirtildiği şekilde kullanın.

### Yinelenen Mesaj Tanımlama

RedDSA_BLAKE2b_Ed25519 için, RedDSA_SHA512_Ed25519'daki (teklif 123'te tanımlandığı gibi imza tipi 11) SHA-512 hash fonksiyonunu BLAKE2b-512 ile değiştirin. Başka değişiklik yok.

su3 dosyaları için EdDSA_SHA512_Ed25519ph (imza türü 8) yerine bir alternatife ihtiyacımız yok, çünkü EdDSA'nın önceden hash'lenmiş versiyonu LEA'ya karşı savunmasız değil. EdDSA_SHA512_Ed25519 (imza türü 7) su3 dosyaları için desteklenmiyor.

| Type | Type Code | Since | Usage |
|------|-----------|-------|-------|
| RedDSA_BLAKE2b_Ed25519 | 12 | TBD | For Router Identities, Destinations and encrypted leasesets only; never used for Router Identities |
### Hız

Aşağıdakiler yeni imza türü için geçerlidir.

| Data Type | Length |
|-----------|--------|
| Hash | 64 |
| Private Key | 32 |
| Public Key | 32 |
| Signature | 64 |
### Personalizations

İmzaların çeşitli kullanımları için domain ayrımı sağlamak amacıyla BLAKE2b kişiselleştirme özelliğini kullanacağız.

BLAKE2b imzalarının tüm kullanımları 16 karakterlik bir kişiselleştirme dizesi kullanacaktır. Yeni kullanımlar, benzersiz bir kişiselleştirme ile buradaki tabloya eklenmelidir.

Aşağıda kullanılan NTCP 1 ve SSU handshake'i, handshake'in kendisinde tanımlanan imzalı veriler içindir. DatabaseStore Mesajlarındaki imzalı RouterInfo'lar, tıpkı NetDB'de depolanmış gibi NetDb Entry kişiselleştirmesini kullanacaktır.

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
## Hedefler

## Tasarım

- Alternatif 1: Proposal 146;
  LEA direncini sağlar
- Alternatif 2: [RFC 8032'de Ed25519ctx](https://tools.ietf.org/html/rfc8032);
  LEA direncini ve kişiselleştirmeyi sağlar.
  Standartlaştırılmış, ancak bunu kullanan var mı?
  Bkz. [RFC 8032](https://tools.ietf.org/html/rfc8032) ve [bu tartışma](https://moderncrypto.org/mail-archive/curves/2017/000925.html).
- "Anahtarlı" hash işlemi bizim için yararlı mı?

## Gerekçe

Önceki imza türlerinin kullanıma sunulmasıyla aynı.

Yeni router'ları varsayılan olarak tip 7'den tip 12'ye değiştirmeyi planlıyoruz. Mevcut router'ları tip 7'den tip 12'ye geçirmek için tip 7 tanıtıldıktan sonra kullanılan "yeniden anahtarlama" sürecini kullanmayı planlıyoruz. Yeni hedefleri varsayılan olarak tip 7'den tip 12'ye değiştirmeyi planlıyoruz. Yeni şifrelenmiş hedefleri varsayılan olarak tip 11'den tip 13'e değiştirmeyi planlıyoruz.

Tip 7, 11 ve 12'den tip 12'ye blinding desteği sağlayacağız. Tip 12'den tip 11'e blinding desteği sağlamayacağız.

Yeni router'lar birkaç ay sonra varsayılan olarak yeni imza türünü kullanmaya başlayabilir. Yeni hedefler belki bir yıl sonra varsayılan olarak yeni imza türünü kullanmaya başlayabilir.

Minimum router sürümü 0.9.TBD için, router'lar şunları sağlamalıdır:

- Yeni sig türüne sahip bir RI veya LS'yi 0.9.TBD sürümünden düşük router'lara depolamayın (veya flood etmeyin).
- Bir netDb store doğrulaması yaparken, yeni sig türüne sahip bir RI veya LS'yi 0.9.TBD sürümünden düşük router'lardan almayın.
- RI'larında yeni sig türü bulunan router'lar, 0.9.TBD sürümünden düşük router'lara
  NTCP, NTCP2 veya SSU ile bağlanamayabilir.
- Streaming bağlantıları ve imzalı datagram'lar 0.9.TBD sürümünden düşük router'larda çalışmayacaktır,
  ancak bunu bilmenin bir yolu yoktur, bu nedenle yeni sig türü 0.9.TBD sürümü yayınlandıktan sonra
  aylarca veya yıllarca varsayılan olarak kullanılmamalıdır.
