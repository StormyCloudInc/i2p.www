---
title: "Sık Sorulan Sorular"
description: "Kapsamlı I2P SSS: router yardımı, yapılandırma, reseed'ler, gizlilik/güvenlik, performans ve sorun giderme"
slug: "faq"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: belgeler
---

## I2P Router Yardım

### What systems will I2P run on? {#systems}

I2P, Java programlama dili ile yazılmıştır. Windows, Linux, FreeBSD ve OSX üzerinde test edilmiştir. Android sürümü de mevcuttur.

Bellek kullanımı açısından, I2P varsayılan olarak 128 MB RAM kullanacak şekilde yapılandırılmıştır. Bu, tarayıcı ve IRC kullanımı için yeterlidir. Ancak, diğer etkinlikler daha fazla bellek tahsisi gerektirebilir. Örneğin, yüksek bant genişlikli bir router çalıştırmak, I2P torrent'lerine katılmak veya yoğun trafikli gizli hizmetler sunmak istiyorsanız, daha fazla bellek gereklidir.

İşlemci kullanımı açısından, I2P'nin Raspberry Pi serisi tek kartlı bilgisayarlar gibi mütevazı sistemlerde çalıştığı test edilmiştir. I2P kriptografik teknikleri yoğun şekilde kullandığından, daha güçlü bir işlemci hem I2P tarafından oluşturulan iş yükünü hem de sistemin geri kalanıyla ilgili görevleri (yani İşletim Sistemi, GUI, Web Tarama gibi Diğer süreçler) daha iyi şekilde yönetebilecektir.

Sun/Oracle Java veya OpenJDK kullanılması önerilir.

### I2P hangi sistemlerde çalışır? {#systems}

Evet, I2P Core kullanmak için Java gereklidir. Windows, Mac OSX ve Linux için kolay yükleyicilerimizin içinde Java'yı dahil ediyoruz. I2P Android uygulamasını çalıştırıyorsanız, çoğu durumda Dalvik veya ART gibi bir Java çalışma zamanına da ihtiyacınız olacaktır.

### I2P kullanmak için Java yüklemek gerekli mi? {#java}

Bir I2P Sitesi, I2P içinde barındırılması dışında normal bir web sitesidir. I2P siteleri, insanların yararına, kriptografik olmayan, insanlar tarafından okunabilir bir şekilde ".i2p" ile biten normal internet adresleri gibi görünen adreslere sahiptir. Bir I2P Sitesine gerçekten bağlanmak kriptografi gerektirir, bu da I2P Site adreslerinin aynı zamanda uzun "Base64" Destination'ları ve daha kısa "B32" adresleri olduğu anlamına gelir. Doğru şekilde gezinmek için ek yapılandırma yapmanız gerekebilir. I2P Sitelerinde gezinmek, I2P kurulumunuzda HTTP Proxy'yi etkinleştirmenizi ve ardından tarayıcınızı bunu kullanacak şekilde yapılandırmanızı gerektirecektir. Daha fazla bilgi için aşağıdaki "Tarayıcılar" bölümüne veya "Tarayıcı Yapılandırması" Kılavuzuna göz atın.

### "I2P Site" nedir ve tarayıcımı bunları kullanabilmek için nasıl yapılandırırım? {#I2P-Site}

Router konsolunuzdaki Eşler sayfasında iki sayı görebilirsiniz - Aktif x/y. İlk sayı, son birkaç dakika içinde kendisine mesaj gönderdiğiniz veya kendisinden mesaj aldığınız eş sayısıdır. İkinci sayı ise yakın zamanda görülen eş sayısıdır; bu sayı her zaman ilk sayıya eşit veya ondan büyük olacaktır.

### Router konsolundaki Aktif x/y numaraları ne anlama gelir? {#active}

Evet, bu normal olabilir, özellikle router yeni başlatıldığında. Yeni router'ların başlatılması ve ağın geri kalanına bağlanması için zamana ihtiyaç vardır. Ağ entegrasyonunu, çalışma süresini ve performansı iyileştirmeye yardımcı olmak için şu ayarları gözden geçirin:

- **Bant genişliği paylaşımı** - Bir router bant genişliği paylaşmak üzere yapılandırılmışsa, diğer router'lar için daha fazla trafik yönlendirecektir; bu da hem ağın geri kalanıyla entegrasyonuna yardımcı olur hem de yerel bağlantının performansını artırır. Bu ayar [http://localhost:7657/config](http://localhost:7657/config) sayfasından yapılandırılabilir.
- **Ağ arayüzü** - [http://localhost:7657/confignet](http://localhost:7657/confignet) sayfasında belirtilmiş bir arayüz olmadığından emin olun. Bilgisayarınız birden fazla harici IP adresine sahip çoklu ağ bağlantılı (multi-homed) değilse, bu performansı düşürebilir.
- **I2NP protocol** - Router'ın, ana bilgisayarın işletim sistemi ve boş ağ (Gelişmiş) ayarları için geçerli bir protokol üzerinden bağlantı bekleyecek şekilde yapılandırıldığından emin olun. Ağ yapılandırma sayfasındaki 'Hostname' alanına bir IP adresi girmeyin. Burada seçtiğiniz I2NP Protocol yalnızca henüz ulaşılabilir bir adresiniz yoksa kullanılacaktır. Örneğin, Amerika Birleşik Devletleri'ndeki çoğu Verizon 4G ve 5G kablosuz bağlantısı UDP'yi engeller ve bu protokol üzerinden erişilemez. Diğerleri UDP'yi kullanılabilir olsa bile zorla kullanır. Listelenen I2NP Protocols'dan makul bir ayar seçin.

### Yönlendiricimin çok az aktif eşi var, bu normal mi? {#peers}

Bu tür materyallerin hiçbiri varsayılan olarak yüklenmez. Ancak I2P bir peer-to-peer (eşler arası) ağ olduğundan, yasaklanmış içeriklerle kazara karşılaşmanız mümkündür. İşte I2P'nin sizi inançlarınızın ihlallerine gereksiz yere dahil olmaktan nasıl koruduğuna dair bir özet.

- **Dağıtım** - Trafik I2P ağının içinde kalır, siz bir [çıkış düğümü](#exit) değilsiniz (dokümantasyonumuzda outproxy olarak adlandırılır).
- **Depolama** - I2P ağı içeriğin dağıtılmış depolamasını yapmaz, bunun kullanıcı tarafından özel olarak kurulması ve yapılandırılması gerekir (örneğin Tahoe-LAFS ile). Bu, farklı bir anonim ağ olan [Freenet](http://freenetproject.org/)'in bir özelliğidir. Bir I2P router çalıştırarak kimse için içerik depolamıyorsunuz.
- **Erişim** - Router'ınız sizin özel talimatınız olmadan herhangi bir içerik talep etmeyecektir.

### Belirli içerik türlerine karşıyım. Bunları dağıtmaktan, depolamaktan veya erişmekten nasıl kaçınabilirim? {#badcontent}

Evet, şimdiye kadar en kolay ve en yaygın yol bootstrap veya "Reseed" sunucularını engellemektir. Tüm gizlenmiş trafiği tamamen engellemek de işe yarar (ancak bu, I2P olmayan başka birçok şeyi bozar ve çoğu kişi bu kadar ileri gitmeye istekli değildir). Reseed engellemesi durumunda, Github'da bir reseed paketi bulunur, bunu engellemek Github'ı da engelleyecektir. Bir proxy üzerinden reseed yapabilirsiniz (Tor kullanmak istemiyorsanız İnternet'te birçoğu bulunabilir) veya reseed paketlerini arkadaştan arkadaşa şeklinde çevrimdışı paylaşabilirsiniz.

### I2P'yi engellemek mümkün mü? {#blocking}

Bu hata, varsayılan olarak IPv6 kullanacak şekilde yapılandırılmış bazı sistemlerde ağ etkinleştirilmiş herhangi bir java yazılımında ortaya çıkabilir. Bunu çözmenin birkaç yolu vardır:

- Linux tabanlı sistemlerde, `echo 0 > /proc/sys/net/ipv6/bindv6only` komutunu çalıştırabilirsiniz
- `wrapper.config` dosyasında şu satırları arayın:
  ```
  #wrapper.java.additional.5=-Djava.net.preferIPv4Stack=true
  #wrapper.java.additional.6=-Djava.net.preferIPv6Addresses=false
  ```
  Eğer bu satırlar mevcutsa, "#" işaretlerini kaldırarak yorum satırı olmaktan çıkarın. Eğer bu satırlar mevcut değilse, "#" işaretleri olmadan ekleyin.

Başka bir seçenek ise `~/.i2p/clients.config` dosyasından `::1` ifadesini kaldırmak olacaktır

**UYARI**: `wrapper.config` dosyasında yapılan herhangi bir değişikliğin etkili olması için router'ı ve wrapper'ı tamamen durdurmanız gerekir. Router konsolunuzda *Yeniden Başlat*'a tıklamak bu dosyayı YENİDEN OKUMAZ! *Kapat*'a tıklamanız, 11 dakika beklemeniz ve ardından I2P'yi başlatmanız gerekir.

### Router Console yüklenirken `wrapper.log` dosyasında "`Protocol family unavailable`" hatası görüyorum {#protocolfamily}

Şimdiye kadar oluşturulmuş her I2P Site'ı düşünürseniz, evet, çoğu çevrimdışı. İnsanlar ve I2P Site'ları gelir ve gider. I2P'ye başlamak için iyi bir yol, şu anda aktif olan I2P Site'larının listesine göz atmaktır. [identiguy.i2p](http://identiguy.i2p) aktif I2P Site'larını takip eder.

### I2P içindeki I2P Sitelerinin çoğu çalışmıyor mu? {#down}

Kullandığımız Tanuki java service wrapper, JVM içinde çalışan yazılımla iletişim kurmak için bu portu açar — localhost'a bağlıdır. JVM başlatıldığında, wrapper'a bağlanabilmesi için bir anahtar verilir. JVM wrapper'a bağlantısını kurduktan sonra, wrapper ek bağlantıları reddeder.

Daha fazla bilgi [wrapper dokümantasyonunda](http://wrapper.tanukisoftware.com/doc/english/prop-port.html) bulunabilir.

### I2P neden 32000 portunu dinliyor? {#port32000}

Farklı tarayıcılar için proxy yapılandırması, ekran görüntüleriyle birlikte ayrı bir sayfadadır. FoxyProxy tarayıcı eklentisi veya Privoxy proxy sunucusu gibi harici araçlarla daha gelişmiş yapılandırmalar mümkündür, ancak kurulumunuzda sızıntılara neden olabilir.

### Tarayıcımı nasıl yapılandırırım? {#browserproxy}

I2P içindeki ana IRC sunucusuna, Irc2P'ye bir tunnel, I2P kurulduğunda oluşturulur ([I2PTunnel yapılandırma sayfasına](http://localhost:7657/i2ptunnel/index.jsp) bakın) ve I2P router başladığında otomatik olarak başlatılır. Bağlanmak için, IRC istemcinize `localhost 6668`'e bağlanmasını söyleyin. HexChat benzeri istemci kullanıcıları, `localhost/6668` sunucusuyla yeni bir ağ oluşturabilir (bir proxy sunucusu yapılandırdıysanız "Proxy sunucusunu atla" seçeneğini işaretlemeyi unutmayın). Weechat kullanıcıları yeni bir ağ eklemek için aşağıdaki komutu kullanabilir:

```
/server add irc2p localhost/6668
```
### I2P içinde IRC'ye nasıl bağlanırım? {#irc}

En kolay yöntem, router konsolundaki [i2ptunnel](http://127.0.0.1:7657/i2ptunnel/) bağlantısına tıklayıp yeni bir 'Sunucu Tüneli' oluşturmaktır. Tunnel hedefini Tomcat veya Jetty gibi mevcut bir web sunucusunun portuna ayarlayarak dinamik içerik sunabilirsiniz. Statik içerik de sunabilirsiniz. Bunun için tunnel hedefini şu şekilde ayarlayın: `0.0.0.0 port 7659` ve içeriği `~/.i2p/eepsite/docroot/` dizinine yerleştirin. (Linux dışı sistemlerde bu farklı bir yerde olabilir. Router konsolunu kontrol edin.) 'eepsite' yazılımı I2P kurulum paketinin bir parçası olarak gelir ve I2P başlatıldığında otomatik olarak başlayacak şekilde ayarlanmıştır. Oluşturulan varsayılan siteye http://127.0.0.1:7658 adresinden erişilebilir. Ancak 'eepsite'ınıza başkaları da eepsite anahtar dosyanız aracılığıyla erişebilir, bu dosya şurada bulunur: `~/.i2p/eepsite/i2p/eepsite.keys`. Daha fazla bilgi edinmek için şu konumdaki readme dosyasını okuyun: `~/.i2p/eepsite/README.txt`.

### Kendi I2P Sitemi nasıl kurarım? {#myI2P-Site}

Düşmanınıza ve tehdit modelinize bağlıdır. Yalnızca kurumsal "gizlilik" ihlalleri, tipik suçlular ve sansür konusunda endişeleniyorsanız, o zaman gerçekten tehlikeli değildir. Kolluk kuvvetleri, gerçekten isterse muhtemelen sizi yine de bulacaktır. Yalnızca normal bir (internet) ev kullanıcısı tarayıcısı çalışırken barındırma yapmak, o kısmı kimin barındırdığını bilmeyi gerçekten zorlaştıracaktır. Lütfen I2P sitenizi barındırmayı diğer herhangi bir hizmeti barındırmak gibi değerlendirin - kendiniz nasıl yapılandırıp yönettiğiniz kadar tehlikeli - veya güvenlidir.

Not: Bir i2p hizmetini (destination) i2p router'dan ayırmanın zaten bir yolu var. Eğer bunun [nasıl çalıştığını](/docs/overview/tech-intro#i2pservices) anlıyorsanız, o zaman genel olarak erişilebilir olacak web sitesi (veya hizmet) için ayrı bir makineyi sunucu olarak kurabilir ve bunu [çok] güvenli bir SSH tüneli üzerinden web sunucusuna yönlendirebilir veya güvenli, paylaşımlı bir dosya sistemi kullanabilirsiniz.

### Evde I2P üzerinde yalnızca HTML ve CSS içeren bir web sitesi barındırırsam, bu tehlikeli midir? {#hosting}

I2P Adres Defteri uygulaması, insan tarafından okunabilir isimleri hizmetlerle ilişkili uzun vadeli hedeflerle eşleştirir ve bu da onu bir ağ veritabanı veya DNS hizmetinden çok bir hosts dosyası veya kişi listesi gibi yapar. Ayrıca yerel önceliklidir - tanınmış bir küresel isim alanı yoktur, herhangi bir .i2p alan adının neyle eşleşeceğine siz karar verirsiniz. Ara yol, size insan tarafından okunabilir bir isim sağlayan ve "I2P router'ına $SITE_CRYPTO_KEY anahtarını $SITE_NAME.i2p adıyla çağırması için izin veriyor musunuz?" veya buna benzer bir ifade içeren bir sayfaya yönlendirerek çalışan "Jump Service" (Atlama Hizmeti) adı verilen bir şeydir. Adres defterinize eklendikten sonra, siteyi başkalarıyla paylaşmaya yardımcı olmak için kendi jump URL'lerinizi oluşturabilirsiniz.

### I2P ".i2p" web sitelerini nasıl bulur? {#addresses}

Ziyaret etmek istediğiniz sitenin en azından base32 veya base64 adresini bilmeden bir adres ekleyemezsiniz. İnsanlar tarafından okunabilen "hostname" (alan adı), base32 veya base64'e karşılık gelen kriptografik adresin yalnızca bir takma adıdır. Kriptografik adres olmadan bir I2P Sitesine erişmenin hiçbir yolu yoktur, bu tasarım gereğidir. Adresi henüz bilmeyen kişilere dağıtmak genellikle Jump hizmet sağlayıcısının sorumluluğundadır. Bilinmeyen bir I2P Sitesini ziyaret etmek, bir Jump hizmetinin kullanımını tetikleyecektir. stats.i2p en güvenilir Jump hizmetidir.

Eğer i2ptunnel üzerinden bir site barındırıyorsanız, henüz bir jump servisi ile kaydı olmayacaktır. Yerel olarak bir URL vermek için yapılandırma sayfasını ziyaret edin ve "Add to Local Address Book" yazan düğmeye tıklayın. Ardından addresshelper URL'sini aramak ve paylaşmak için http://127.0.0.1:7657/dns adresine gidin.

### Adres Defteri'ne nasıl adres eklerim? {#addressbook}

I2P tarafından kullanılan portlar 2 bölüme ayrılabilir:

1. Diğer I2P router'ları ile iletişim için kullanılan İnternet'e açık portlar
2. Yerel bağlantılar için yerel portlar

Bunlar aşağıda detaylı olarak açıklanmıştır.

#### 1. Internet-facing ports

Not: 0.7.8 sürümünden itibaren, yeni kurulumlar 8887 numaralı bağlantı noktasını kullanmaz; program ilk kez çalıştırıldığında 9000 ile 31000 arasında rastgele bir bağlantı noktası seçilir. Seçilen bağlantı noktası router [yapılandırma sayfasında](http://127.0.0.1:7657/confignet) gösterilir.

**GİDEN**

- [Yapılandırma sayfasında](http://127.0.0.1:7657/confignet) listelenen rastgele porttan rastgele uzak UDP portlarına UDP, yanıtlara izin verir
- Rastgele yüksek portlardan rastgele uzak TCP portlarına TCP
- 123 numaralı portta giden UDP, yanıtlara izin verir. Bu, I2P'nin dahili zaman senkronizasyonu için gereklidir (SNTP aracılığıyla - pool.ntp.org'daki rastgele bir SNTP sunucusunu veya belirttiğiniz başka bir sunucuyu sorgulama)

**GELEN**

- (İsteğe bağlı, önerilir) [Yapılandırma sayfasında](http://127.0.0.1:7657/confignet) belirtilen porta rastgele konumlardan UDP
- (İsteğe bağlı, önerilir) [Yapılandırma sayfasında](http://127.0.0.1:7657/confignet) belirtilen porta rastgele konumlardan TCP
- Gelen TCP bağlantıları [yapılandırma sayfasından](http://127.0.0.1:7657/confignet) devre dışı bırakılabilir

#### 2. Local I2P ports

Yerel I2P portları, aksi belirtilmedikçe varsayılan olarak yalnızca yerel bağlantıları dinler:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PORT</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PURPOSE</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">DESCRIPTION</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1900</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UPnP SSDP UDP multicast listener</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cannot be changed. Binds to all interfaces. May be disabled on <a href="http://127.0.0.1:7657/confignet">confignet</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2827</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB bridge</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A higher level socket API for clients. Disabled by default. May be enabled/disabled on <a href="http://127.0.0.1:7657/configclients">configclients</a>. May be changed in the bob.config file.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4444</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Configured on <a href="http://127.0.0.1:7657/configclients">configclients</a>, go to the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a> to start/stop it and on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/0">I2P HTTP Proxy</a> to configure it. Include in your browser's proxy configuration for HTTP</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4445</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTPS proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Configured on <a href="http://127.0.0.1:7657/configclients">configclients</a>, go to the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a> to start/stop it and on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/1">I2P HTTPS Proxy</a> to configure it. Include in your browser's proxy configuration for HTTPS</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6668</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">IRC proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A tunnel to the inside-the-I2P IRC network. Disabled by default. Configured on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/2">irc.postman.i2p (IRC proxy)</a> and may be enabled/disabled on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7654</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2CP (client protocol) port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For advanced client usage. Do not expose to an external network.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7656</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM bridge</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A socket API for clients. Disabled by default. May be enabled/disabled on <a href="http://127.0.0.1:7657/configclients">configclients</a> and configured on <a href="http://127.0.0.1:7657/sam">sam</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7657 (or 7658 via SSL)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router console</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">The router console provides valuable information about your router and the network, in addition to giving you access to configure your router and its associated applications.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7659</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">'eepsite' - an example webserver (Jetty)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Included in the <code>i2pinstall</code> and <code>i2pupdate</code> packages - may be disabled if another webserver is available. May be configured on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/3">eepsite</a> and disabled on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7660</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel UDP port for SSH</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Required for Grizzled's/novg's UDP support. Instances disabled by default. May be enabled/disabled and configured to use a different port on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">123</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTP Port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used by <a href="http://127.0.0.1:7657/confignet">NTP Time Sync</a>. May be disabled/changed.</td>
    </tr>
  </tbody>
</table>
### I2P hangi portları kullanır? {#ports}

Adres defteri [http://localhost:7657/dns](http://localhost:7657/dns) adresinde bulunmaktadır ve daha fazla bilgi burada bulunabilir.

**İyi adres defteri abonelik bağlantıları nelerdir?**

Aşağıdakileri deneyebilirsiniz:

- [http://stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
- [http://identiguy.i2p/hosts.txt](http://identiguy.i2p/hosts.txt)

### How can I access the web console from my other machines or password protect it? {#remote_webconsole}

Güvenlik amacıyla, router'ın yönetim konsolu varsayılan olarak yalnızca yerel arayüzde bağlantı dinler.

Konsola uzaktan erişim için iki yöntem bulunmaktadır:

1. SSH Tüneli
2. Konsolunuzu bir genel IP adresinde kullanıcı adı ve şifre ile erişilebilir hale getirme

Bunlar aşağıda detaylı olarak açıklanmıştır:

**Yöntem 1: SSH Tüneli**

Unix benzeri bir İşletim Sistemi çalıştırıyorsanız, bu I2P konsolunuza uzaktan erişim için en kolay yöntemdir. (Not: SSH sunucu yazılımı Windows çalıştıran sistemler için de mevcuttur, örneğin [https://github.com/PowerShell/Win32-OpenSSH](https://github.com/PowerShell/Win32-OpenSSH))

Sisteminize SSH erişimini yapılandırdıktan sonra, '-L' bayrağı uygun argümanlarla birlikte SSH'ye iletilir - örneğin:

```
ssh -L 7657:localhost:7657 (System_IP)
```
'(System_IP)' yerine sisteminizin IP adresi yazılır. Bu komut 7657 numaralı portu (ilk iki noktadan önceki sayı) uzak sistemin (ilk ve ikinci iki nokta arasındaki 'localhost' dizesi tarafından belirtildiği gibi) 7657 numaralı portuna (ikinci iki noktadan sonraki sayı) yönlendirir. Uzak I2P konsolunuz artık yerel sisteminizde 'http://localhost:7657' adresi üzerinden erişilebilir olacak ve SSH oturumunuz aktif olduğu sürece kullanılabilir durumda kalacaktır.

Uzak sistemde bir kabuk (shell) başlatmadan bir SSH oturumu başlatmak isterseniz, '-N' bayrağını ekleyebilirsiniz:

```
ssh -NL 7657:localhost:7657 (System_IP)
```
**Yöntem 2: Konsolunuzu genel IP adresinden kullanıcı adı ve şifre ile erişilebilir hale getirme**

1. `~/.i2p/clients.config` dosyasını açın ve şunu:
   ```
   clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
   ```
   bununla değiştirin:
   ```
   clientApp.0.args=7657 ::1,127.0.0.1,(System_IP) ./webapps/
   ```
   burada (System_IP) yerine sisteminizin genel IP adresini yazın

2. [http://localhost:7657/configui](http://localhost:7657/configui) adresine gidin ve isterseniz bir konsol kullanıcı adı ve şifresi ekleyin - I2P konsolunuzu kurcalamaya karşı korumak için bir kullanıcı adı ve şifre eklemeniz şiddetle önerilir, bu durum kimliğin açığa çıkmasına yol açabilir.

3. [http://localhost:7657/index](http://localhost:7657/index) adresine gidin ve JVM'i yeniden başlatıp istemci uygulamalarını yeniden yükleyen "Graceful restart" seçeneğine tıklayın

Bundan sonra başlatıldığında, artık konsolunuza uzaktan erişebilmelisiniz. Router konsolunu `http://(Sistem_IP):7657` adresinden yükleyin ve tarayıcınız kimlik doğrulama açılır penceresini destekliyorsa yukarıdaki 2. adımda belirttiğiniz kullanıcı adı ve parolayı girmeniz istenecektir.

NOT: Yukarıdaki yapılandırmada 0.0.0.0 belirtebilirsiniz. Bu bir ağ veya ağ maskesi değil, bir arayüz belirtir. 0.0.0.0 "tüm arayüzlere bağlan" anlamına gelir, böylece hem 127.0.0.1:7657 hem de herhangi bir LAN/WAN IP üzerinden erişilebilir olur. Bu seçeneği kullanırken dikkatli olun çünkü konsol, sisteminizde yapılandırılmış TÜM adreslerde erişilebilir olacaktır.

### How can I use applications from my other machines? {#remote_i2cp}

SSH Port Forwarding kullanımı için lütfen önceki cevaba bakın ve ayrıca konsolunuzdaki bu sayfaya göz atın: [http://localhost:7657/configi2cp](http://localhost:7657/configi2cp)

### Adres defterimde birçok host eksik. İyi abonelik linkleri nelerdir? {#subscriptions}

SOCKS proxy, 0.7.1 sürümünden beri çalışır durumdadır. SOCKS 4/4a/5 desteklenmektedir. I2P'nin bir SOCKS outproxy'si olmadığı için kullanımı yalnızca I2P içinde sınırlıdır.

Birçok uygulama, sizi İnternet üzerinde tanımlayabilecek hassas bilgileri sızdırır ve bu, I2P SOCKS proxy kullanırken farkında olunması gereken bir risktir. I2P yalnızca bağlantı verilerini filtreler, ancak çalıştırmayı düşündüğünüz program bu bilgiyi içerik olarak gönderirse, I2P anonimliğinizi koruyamaz. Örneğin, bazı e-posta uygulamaları üzerinde çalıştıkları makinenin IP adresini bir posta sunucusuna gönderir. I2P'ye özgü araçlar veya uygulamalar kullanmanızı öneririz (torrentler için [I2PSnark](http://localhost:7657/i2psnark/) gibi) veya [Firefox](https://www.mozilla.org/)'ta bulunan popüler eklentiler de dahil olmak üzere I2P ile kullanımının güvenli olduğu bilinen uygulamaları tercih edin.

### Web konsoluna diğer makinelerimden nasıl erişebilirim veya şifre ile nasıl koruyabilirim? {#remote_webconsole}

I2P ile İnternet arasında köprü görevi gören, Tor Çıkış Düğümleri gibi Outproxy adı verilen hizmetler bulunmaktadır. HTTP ve HTTPS için varsayılan outproxy işlevselliği `exit.stormycloud.i2p` tarafından sağlanır ve StormyCloud Inc. tarafından işletilir. Bu, HTTP Proxy içinde yapılandırılmıştır. Ek olarak, anonimliği korumaya yardımcı olmak için I2P, varsayılan olarak normal İnternet'e anonim bağlantılar kurmanıza izin vermez. Daha fazla bilgi için lütfen [Socks Outproxy](/docs/api/socks#outproxy) sayfasına bakın.

---

## Reseeds

### Diğer makinelerimdeki uygulamaları nasıl kullanabilirim? {#remote_i2cp}

İlk olarak Router Console'daki [http://127.0.0.1:7657/netdb](http://127.0.0.1:7657/netdb) sayfasını kontrol edin – ağ veritabanınız. I2P içinden listelenen tek bir router görmüyorsanız ancak konsol güvenlik duvarının arkasında olduğunuzu söylüyorsa, muhtemelen reseed sunucularına bağlanamıyorsunuzdur. Diğer I2P router'ları listeleniyorsa, [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config) adresinden maksimum bağlantı sayısını düşürmeyi deneyin, router'ınız çok sayıda bağlantıyı kaldıramıyor olabilir.

### I2P'yi SOCKS proxy olarak kullanmak mümkün mü? {#socks}

Normal koşullar altında, I2P sizi bootstrap bağlantılarımızı kullanarak otomatik olarak ağa bağlayacaktır. Kesintili internet, reseed sunucularından bootstrap yapılmasını başarısız kılarsa, bootstrap yapmanın kolay bir yolu Tor tarayıcısını kullanmaktır (Varsayılan olarak localhost'u açar), bu [http://127.0.0.1:7657/configreseed](http://127.0.0.1:7657/configreseed) ile çok iyi çalışır. Bir I2P router'ını manuel olarak reseed etmek de mümkündür.

Yeniden tohum almak için Tor tarayıcısı kullanırken aynı anda birden fazla URL seçebilir ve devam edebilirsiniz. Varsayılan değer olan 2 (birden fazla url'den) de çalışacaktır ancak yavaş olacaktır.

---

## Privacy-Safety

### Normal İnternet'teki IRC, BitTorrent veya diğer hizmetlere nasıl erişebilirim? {#proxy_other}

Hayır, router'ınız I2P ağı üzerinden şifrelenmiş uçtan uca trafiğin rastgele bir tunnel uç noktasına taşınmasına katılır, genellikle bir outproxy'ye değil, ancak router'ınız ile İnternet arasında transport katmanı üzerinden hiçbir trafik aktarılmaz. Son kullanıcı olarak, sistem ve ağ yönetiminde yetenekli değilseniz bir outproxy çalıştırmamalısınız.

### Is it easy to detect the use of I2P by analyzing network traffic? {#detection}

I2P trafiği genellikle UDP trafiğine benzer ve bundan fazlası değildir – ve bundan fazlası gibi görünmemesi bir hedeftir. Ayrıca TCP'yi de destekler. Biraz çaba ile, pasif trafik analizi trafiği "I2P" olarak sınıflandırabilir, ancak trafik gizlemenin sürekli geliştirilmesinin bunu daha da azaltacağını umuyoruz. obfs4 gibi oldukça basit bir protokol gizleme katmanı bile sansürcülerin I2P'yi engellemesini önleyecektir (I2P'nin dağıtması bir hedeftir).

### Router'ım birkaç dakikadır çalışıyor ve sıfır veya çok az bağlantısı var {#reseed}

Kişisel tehdit modelinize bağlıdır. Çoğu insan için I2P, hiçbir koruma kullanmamaktan çok daha güvenlidir. Bazı diğer ağlar (Tor, mixminion/mixmaster gibi), belirli düşmanlara karşı muhtemelen daha güvenlidir. Örneğin, I2P trafiği TLS/SSL kullanmaz, bu nedenle Tor'un sahip olduğu "en zayıf halka" sorunları yoktur. I2P, "Arap Baharı" sırasında Suriye'de birçok kişi tarafından kullanıldı ve son zamanlarda proje, Yakın ve Orta Doğu'daki daha küçük dil gruplarında I2P kurulumlarında daha büyük bir büyüme gördü. Burada belirtilmesi gereken en önemli şey, I2P'nin bir teknoloji olduğu ve İnternet'te gizliliğinizi/anonimliğinizi artırmak için bir nasıl yapılır/rehbere ihtiyacınız olduğudur. Ayrıca tarayıcınızı kontrol edin veya çok büyük (yani: tipik uzun kuyruklar / çok hassas çeşitli veri yapısı) bir veri setiyle parmak izi saldırılarını engellemek için parmak izi arama motorunu içe aktarın ve kendi TLS önbellek davranışı ve sağlayıcı iş yapısının teknik kurulumu gibi kendisinden kaynaklanan tüm riskleri azaltmak için VPN kullanmayın, çünkü bunlar kendi masaüstü sisteminizden daha kolay hacklenebilir. Harika parmak izi karşıtı korumaları olan izole bir Tor V-Browser kullanmak ve yalnızca gerekli sistem iletişimlerine izin veren genel bir appguard-ömür boyu-koruma ve "neredeyse kalıcı olası riski" kaldırmak için casus yazılım karşıtı devre dışı bırakma betikleri ve live-cd ile son savunma vm kullanımı ve azalan olasılıkla tüm riskleri düşürmek, halka açık ağda ve en üst düzey bireysel risk modelinde iyi bir seçenek olabilir ve i2p kullanımı için bu hedefle yapabileceğiniz en iyi şey olabilir.

### Manuel olarak nasıl reseed yaparım? {#manual_reseed}

Evet, router'ınız hakkında bilgi sahibi olan diğer I2P düğümleri için. Bunu I2P ağının geri kalanı ile bağlantı kurmak için kullanırız. Adresler fiziksel olarak "routerInfo'larda (anahtar,değer)nesnelerinde" bulunur; bunlar ya uzaktan alınır ya da eşlerden (peer) alınır. "routerInfo'lar", önyükleme (bootstrapping) için router'ın kendisi hakkında "eş tarafından yayınlanan" bazı bilgileri (bazıları opsiyonel fırsatçı olarak eklenmiş) barındırır. Bu nesnede istemcilerle ilgili herhangi bir veri bulunmaz. Kapağın altına daha yakından bakıldığında, herkesin "SHA-256 Hash'leri (düşük=Pozitif hash(-anahtar), yüksek=Negatif hash(+anahtar))" adı verilen en yeni kimlik oluşturma türüyle sayıldığını göreceksiniz. I2P ağı, yükleme ve indeksleme sırasında oluşturulan routerInfo'ların kendi veritabanı verilerine sahiptir, ancak bu durum anahtar/değer tablolarının ve ağ topolojisinin gerçekleştirilmesine ve yük durumuna / bant genişliği durumuna ve DB bileşenlerindeki depolama için yönlendirme olasılıklarına derinlemesine bağlıdır.

### Is using an outproxy safe? {#proxy_safe}

"Güvenli" tanımınızın ne olduğuna bağlıdır. Outproxy'ler çalıştıklarında harikadır, ancak ne yazık ki gönüllü olarak, ilgilerini kaybedebilecek veya bunları 7/24 sürdürmek için kaynaklara sahip olmayabilecek kişiler tarafından yönetilirler – lütfen hizmetlerin kullanılamadığı, kesintiye uğradığı veya güvenilir olmadığı dönemler yaşayabileceğinizi unutmayın ve bu hizmetle ilişkili değiliz ve üzerinde herhangi bir etkimiz yoktur.

Outproxy'lerin kendisi, uçtan uca şifrelenmiş HTTPS/SSL verileri hariç, trafiğinizin gelip gittiğini görebilir; tıpkı İSS'nizin bilgisayarınızdan gelen ve giden trafiğinizi görebildiği gibi. İSS'nize güveniyorsanız, outproxy ile durum daha kötü olmaz.

### Yönlendiricim normal İnternet'e bir "çıkış düğümü"(outproxy) mü? Olmasını istemiyorum. {#exit}

Çok uzun bir açıklama için [Tehdit Modeli](/docs/overview/threat-model) hakkındaki makalelerimizi okuyun. Genel olarak, anonim kalma yeterince dikkatli olmazsanız zor olmakla birlikte mümkündür.

---

## Internet Access/Performance

### Ağ trafiğini analiz ederek I2P kullanımını tespit etmek kolay mıdır? {#detection}

İnternet sitelerine proxy yapma (İnternet'e açık eepsite'lar) I2P kullanıcılarına engelleme yapmayan sağlayıcılar tarafından bir hizmet olarak sunulmaktadır. Bu hizmet I2P geliştirmesinin ana odak noktası değildir ve gönüllü olarak sağlanmaktadır. I2P üzerinde barındırılan eepsite'lar her zaman outproxy olmadan çalışmalıdır. Outproxy'ler bir kolaylıktır ancak tasarım gereği mükemmel değillerdir ve projenin büyük bir parçası da değillerdir. I2P'nin sunduğu diğer hizmetlerin sağlayabileceği yüksek kaliteli hizmeti sunamayabileceklerinin farkında olun.

### I2P kullanmak güvenli mi? {#safe}

Varsayılan HTTP proxy yalnızca HTTP ve HTTPS outproxy'yi destekler.

### Router konsolunda diğer tüm I2P düğümlerinin IP adreslerini görüyorum. Bu, benim IP adresimin de başkaları tarafından görülebildiği anlamına mı geliyor? {#netdb_ip}

Öncelikle, I2P ile ilgili her bileşenin en son sürümüne sahip olduğunuzdan emin olun – eski sürümlerde kodda gereksiz CPU tüketen bölümler bulunuyordu. Ayrıca, I2P performansındaki bazı iyileştirmeleri zaman içinde belgeleyen bir [performans Günlüğü](/about/performance) de mevcuttur.

### Outproxy kullanmak güvenli midir? {#proxy_safe}

I2P ağının genel kararlılığı devam eden bir araştırma alanıdır. Bu araştırmanın önemli bir bölümü, yapılandırma ayarlarındaki küçük değişikliklerin router'ın davranışını nasıl değiştirdiğine odaklanmıştır. I2P eşler arası bir ağ olduğundan, diğer eşlerin eylemleri router'ınızın performansı üzerinde etkili olacaktır.

### "Kimlik Açığa Çıkarma" saldırıları hakkında ne düşünüyorsunuz? {#deanon}

I2P, ekstra yönlendirme ve ek şifreleme katmanları ekleyen farklı koruma mekanizmalarına sahiptir. Ayrıca trafiği kendi hız ve kalitesine sahip diğer eşler (Tunnels) üzerinden yönlendirir; bazıları yavaş, bazıları hızlıdır. Bu durum, farklı yönlerde farklı hızlarda çok fazla ek yük ve trafik oluşturur. Tasarım gereği tüm bunlar, internetteki doğrudan bir bağlantıya kıyasla daha yavaş olmasına neden olur, ancak çok daha anonimdir ve çoğu şey için hâlâ yeterince hızlıdır.

Aşağıda, I2P kullanırken gecikme ve bant genişliği değerlendirmelerine bağlam sağlamaya yardımcı olmak için açıklamalı bir örnek sunulmaktadır.

Aşağıdaki diyagramı inceleyin. I2P üzerinden istek yapan bir istemci, I2P üzerinden isteği alan bir sunucu ve ardından yine I2P üzerinden yanıt veren sunucu arasındaki bağlantıyı göstermektedir. İsteğin üzerinde seyahat ettiği devre de gösterilmiştir.

Diyagramdan, 'P', 'Q' ve 'R' etiketli kutuların 'A' için bir outbound tunnel'ı temsil ettiğini ve 'X', 'Y' ve 'Z' etiketli kutuların 'B' için bir outbound tunnel'ı temsil ettiğini düşünün. Benzer şekilde, 'X', 'Y' ve 'Z' etiketli kutular 'B' için bir inbound tunnel'ı temsil ederken, 'P_1', 'Q_1' ve 'R_1' etiketli kutular 'A' için bir inbound tunnel'ı temsil eder. Kutular arasındaki oklar trafik yönünü gösterir. Okların üstündeki ve altındaki metinler, bir çift atlama arasındaki örnek bant genişliğini ve örnek gecikme sürelerini detaylandırır.

Hem istemci hem de sunucu baştan sona 3 atlamalı tüneller kullandığında, trafiğin aktarılmasında toplam 12 diğer I2P router'ı yer alır. 6 eş, istemciden sunucuya olan trafiği aktarır; bu trafik 'A'dan ('P', 'Q', 'R') 3 atlamalı giden bir tünele ve 'B'ye ('X', 'Y', 'Z') 3 atlamalı gelen bir tünele bölünür. Benzer şekilde, 6 eş sunucudan istemciye geri dönen trafiği aktarır.

İlk olarak, gecikmeyi ele alabiliriz - bir istemciden gelen bir isteğin I2P ağını geçmesi, sunucuya ulaşması ve istemciye geri dönmesi için geçen süre. Tüm gecikmeleri toplarsak şunu görürüz:

```
    40 + 100 + 20 + 60 + 80 + 10 + 30 ms        (client to server)
  + 60 + 40 + 80 + 60 + 100 + 20 + 40 ms        (server to client)
  -----------------------------------
  TOTAL:                          740 ms
```
Örneğimizdeki toplam gidiş-dönüş süresi 740 ms'ye ulaşıyor - bu kesinlikle normal internet sitelerine göz atarken görülen sürelerden çok daha yüksek.

İkinci olarak, mevcut bant genişliğini değerlendirebiliriz. Bu, istemci ile sunucu arasındaki atlamalar arasındaki en yavaş bağlantı ve sunucunun istemciye trafik iletimi sırasında belirlenir. İstemciden sunucuya giden trafik için, örneğimizde 'R' & 'X' atlamaları ile 'X' & 'Y' atlamaları arasındaki mevcut bant genişliğinin 32 KB/s olduğunu görüyoruz. Diğer atlamalar arasında daha yüksek mevcut bant genişliği olmasına rağmen, bu atlamalar darboğaz görevi görecek ve 'A'dan 'B'ye giden trafik için maksimum kullanılabilir bant genişliğini 32 KB/s ile sınırlayacaktır. Benzer şekilde, sunucudan istemciye giden yolu izlediğimizde maksimum 64 KB/s bant genişliği olduğunu görürüz - 'Z_1' & 'Y_1, 'Y_1' & 'X_1' ve 'Q_1' & 'P_1' atlamaları arasında.

Bant genişliği limitlerini artırmanızı öneririz. Bu, mevcut bant genişliği miktarını artırarak ağa yardımcı olur ve sonuç olarak I2P deneyiminizi iyileştirir. Bant genişliği ayarları [http://localhost:7657/config](http://localhost:7657/config) sayfasında bulunmaktadır. Lütfen İSS'nizin belirlediği internet bağlantınızın limitlerinin farkında olun ve ayarlarınızı buna göre düzenleyin.

Ayrıca yeterli miktarda paylaşımlı bant genişliği ayarlamanızı öneririz - bu, katılımcı tunnel'ların I2P router'ınız üzerinden yönlendirilmesine olanak tanır. Katılımcı trafiğe izin vermek, router'ınızı ağda iyi entegre tutar ve aktarım hızlarınızı iyileştirir.

I2P geliştirme aşamasında bir projedir. Birçok iyileştirme ve düzeltme uygulanmaktadır ve genel olarak, en son sürümü çalıştırmak performansınıza yardımcı olacaktır. Henüz yapmadıysanız, en son sürümü yükleyin.

### I think I found a bug, where can I report it? {#bug}

Karşılaştığınız hataları/sorunları, hem açık internet hem de I2P üzerinden erişilebilen hata izleyicimizde bildirebilirsiniz. Ayrıca I2P ve açık internet üzerinden erişilebilen bir tartışma forumumuz bulunmaktadır. IRC kanalımıza da katılabilirsiniz: IRC2P ağımız üzerinden veya Freenode'da.

- **Bugtracker'ımız:**
  - Genel internet: [https://i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)
  - I2P üzerinde: [http://git.idk.i2p/I2P_Developers/i2p.i2p/issues](http://git.idk.i2p/I2P_Developers/i2p.i2p/issues)
- **Forumlarımız:** [i2pforum.i2p](http://i2pforum.i2p/)
- **Logları yapıştırın:** İlginç logları [PrivateBin Wiki](https://github.com/PrivateBin/PrivateBin/wiki/PrivateBin-Directory) sayfasında listelenen genel internet servisleri veya bu [PrivateBin örneği](http://paste.crypthost.i2p) ya da bu [Javascript-siz paste servisi](http://pasta-nojs.i2p) gibi bir I2P paste servisine yapıştırabilir ve #i2p IRC kanalında takip edebilirsiniz
- **IRC:** #i2p-dev kanalına katılın ve geliştiricilerle IRC üzerinden görüşün

Lütfen router günlükleri sayfasından ilgili bilgileri ekleyin, sayfaya şu adresten erişilebilir: [http://127.0.0.1:7657/logs](http://127.0.0.1:7657/logs). 'I2P Version and Running Environment' bölümü altındaki tüm metni ve sayfada görüntülenen çeşitli günlüklerde gösterilen hata veya uyarıları paylaşmanızı rica ederiz.

---

### I2P üzerinden normal İnternet sitelerine erişemiyorum. {#outproxy}

Harika! Bizi IRC'de bulun:

- `irc.freenode.net` üzerinde `#i2p` kanalı
- `IRC2P` üzerinde `#i2p` kanalı

veya [foruma](http://i2pforum.i2p/) gönderin, biz de (umarız cevabıyla birlikte) buraya ekleyelim.
