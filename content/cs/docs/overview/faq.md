---
title: "Často kladené otázky"
description: "Komplexní I2P FAQ: nápověda k routeru, konfigurace, reseedy, soukromí/bezpečnost, výkon a řešení problémů"
slug: "faq"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: dokumentace
---

## Nápověda I2P routeru

### What systems will I2P run on? {#systems}

I2P je napsán v programovacím jazyce Java. Byl testován na Windows, Linux, FreeBSD a OSX. K dispozici je také verze pro Android.

Pokud jde o využití paměti, I2P je ve výchozím nastavení nakonfigurováno tak, aby používalo 128 MB RAM. To postačuje pro prohlížení webu a používání IRC. Další aktivity však mohou vyžadovat větší alokaci paměti. Například pokud chcete provozovat vysokopásmový router, účastnit se I2P torrentů nebo poskytovat vysoce navštěvované skryté služby, je zapotřebí vyšší množství paměti.

Z hlediska využití CPU byl I2P testován na skromných systémech, jako je řada jednodeskových počítačů Raspberry Pi. Protože I2P intenzivně využívá kryptografické techniky, výkonnější procesor bude lépe zvládat zátěž generovanou I2P i úkoly související se zbytkem systému (tj. operační systém, grafické rozhraní, další procesy jako např. prohlížení webu).

Doporučuje se použití Sun/Oracle Java nebo OpenJDK.

### Na jakých systémech poběží I2P? {#systems}

Ano, Java je vyžadována pro použití I2P Core. Java je součástí našich instalačních balíčků pro Windows, Mac OSX a Linux. Pokud používáte aplikaci I2P pro Android, budete ve většině případů také potřebovat běhové prostředí Java, jako je Dalvik nebo ART.

### Je pro používání I2P nutná instalace Javy? {#java}

I2P stránka je běžná webová stránka s tím rozdílem, že je hostována uvnitř I2P. I2P stránky mají adresy, které vypadají jako běžné internetové adresy, končící na ".i2p" v lidsky čitelné, nekryptografické podobě, pro pohodlí uživatelů. Samotné připojení k I2P stránce však vyžaduje kryptografii, což znamená, že adresy I2P stránek jsou také dlouhé "Base64" Destinations a kratší "B32" adresy. Pro správné prohlížení může být nutná dodatečná konfigurace. Prohlížení I2P stránek vyžaduje aktivaci HTTP Proxy ve vaší instalaci I2P a následnou konfiguraci prohlížeče k jejímu použití. Pro více informací si prohlédněte sekci "Prohlížeče" níže nebo průvodce "Konfigurace prohlížeče".

### Co je "I2P Site" a jak nakonfiguruji prohlížeč, abych je mohl používat? {#I2P-Site}

Na stránce Peers (Uzly) v konzoli vašeho routeru můžete vidět dvě čísla - Active x/y. První číslo udává počet uzlů, kterým jste poslali nebo od kterých jste obdrželi zprávu v posledních několika minutách. Druhé číslo udává počet uzlů viděných nedávno, toto číslo bude vždy větší nebo rovno prvnímu číslu.

### Co znamenají čísla Aktivní x/y v konzoli routeru? {#active}

Ano, to může být normální, zejména když byl router právě spuštěn. Nové routery potřebují čas na spuštění a připojení ke zbytku sítě. Pro zlepšení integrace do sítě, doby provozu a výkonu zkontrolujte tato nastavení:

- **Sdílení šířky pásma** - Pokud je router nakonfigurován pro sdílení šířky pásma, bude směrovat více provozu pro ostatní routery, což pomáhá integrovat jej se zbytkem sítě a zároveň zlepšuje výkon vlastního lokálního připojení. To lze nakonfigurovat na stránce [http://localhost:7657/config](http://localhost:7657/config).
- **Síťové rozhraní** - Ujistěte se, že na stránce [http://localhost:7657/confignet](http://localhost:7657/confignet) není uvedeno žádné konkrétní rozhraní. To může snížit výkon, pokud váš počítač není multi-homed s více externími IP adresami.
- **I2NP protokol** - Ujistěte se, že router je nakonfigurován tak, aby očekával připojení na platném protokolu pro operační systém hostitele a prázdné nastavení sítě (Pokročilé). Nezadávejte IP adresu do pole 'Hostname' na stránce konfigurace sítě. I2NP protokol, který zde vyberete, bude použit pouze v případě, že ještě nemáte dosažitelnou adresu. Například většina bezdrátových připojení Verizon 4G a 5G ve Spojených státech blokuje UDP a nelze přes něj navázat spojení. Jiné by používaly UDP na sílu, i když je jim k dispozici. Vyberte rozumné nastavení ze seznamu I2NP protokolů.

### Můj router má jen velmi málo aktivních peerů, je to v pořádku? {#peers}

Žádný takový obsah není nainstalován ve výchozím nastavení. Protože je však I2P peer-to-peer síť, je možné, že se můžete náhodně setkat se zakázaným obsahem. Zde je shrnutí toho, jak vás I2P chrání před nežádoucím zapojením do porušování vašich zásad.

- **Distribuce** - Provoz je interní v rámci sítě I2P, nejste [výstupním uzlem](#exit) (v naší dokumentaci označovaný jako outproxy).
- **Úložiště** - Síť I2P neprovádí distribuované ukládání obsahu, to musí být specificky nainstalováno a nakonfigurováno uživatelem (například pomocí Tahoe-LAFS). To je funkce jiné anonymní sítě, [Freenet](http://freenetproject.org/). Provozováním I2P routeru neukládáte obsah pro nikoho jiného.
- **Přístup** - Váš router nebude požadovat žádný obsah bez vašeho výslovného pokynu k tomu.

### Jsem proti určitým typům obsahu. Jak mohu zabránit jejich distribuci, ukládání nebo přístupu k nim? {#badcontent}

Ano, zdaleka nejjednodušší a nejběžnější způsob je blokování bootstrap serverů, neboli "Reseed" serverů. Úplné blokování veškerého obfuskovaného provozu by také fungovalo (ačkoliv by to narušilo mnoho dalších věcí, které nejsou I2P, a většina není ochotna zajít tak daleko). V případě blokování reseedu existuje reseed balíček na Githubu, jeho blokování zablokuje také Github. Můžete provést reseed přes proxy (mnoho jich lze najít na internetu, pokud nechcete používat Tor) nebo sdílet reseed balíčky mezi přáteli offline.

### Je možné zablokovat I2P? {#blocking}

Často se tato chyba vyskytuje u jakéhokoli síťového java softwaru na některých systémech, které jsou ve výchozím nastavení nakonfigurovány pro použití IPv6. Existuje několik způsobů, jak tento problém vyřešit:

- Na systémech založených na Linuxu můžete použít `echo 0 > /proc/sys/net/ipv6/bindv6only`
- Vyhledejte následující řádky v souboru `wrapper.config`:
  ```
  #wrapper.java.additional.5=-Djava.net.preferIPv4Stack=true
  #wrapper.java.additional.6=-Djava.net.preferIPv6Addresses=false
  ```
  Pokud tam tyto řádky jsou, odkomentujte je odstraněním znaků "#". Pokud tam řádky nejsou, přidejte je bez znaků "#".

Další možností by bylo odstranit `::1` ze souboru `~/.i2p/clients.config`

**VAROVÁNÍ**: Aby se jakékoliv změny v `wrapper.config` projevily, musíte zcela zastavit router a wrapper. Kliknutí na *Restart* v konzole routeru tento soubor NEPŘEČTE znovu! Musíte kliknout na *Vypnout*, počkat 11 minut a poté spustit I2P.

### V `wrapper.log` vidím chybu, která uvádí "`Protocol family unavailable`" při načítání Router Console {#protocolfamily}

Pokud vezmete v úvahu každou I2P Site, která kdy byla vytvořena, ano, většina z nich je nedostupná. Lidé a I2P Sites přichází a odchází. Dobrý způsob, jak začít v I2P, je podívat se na seznam I2P Sites, které jsou aktuálně dostupné. [identiguy.i2p](http://identiguy.i2p) sleduje aktivní I2P Sites.

### Většina I2P Sites v rámci I2P je nedostupná? {#down}

Tanuki java service wrapper, který používáme, otevírá tento port — vázaný na localhost — za účelem komunikace se softwarem běžícím uvnitř JVM. Když je JVM spuštěn, je mu předán klíč, aby se mohl připojit k wrapperu. Po navázání spojení JVM s wrapperem wrapper odmítá jakákoli další připojení.

Více informací naleznete v [dokumentaci wrapperu](http://wrapper.tanukisoftware.com/doc/english/prop-port.html).

### Proč I2P naslouchá na portu 32000? {#port32000}

Konfigurace proxy pro různé prohlížeče je na samostatné stránce s ukázkami obrazovky. Jsou možné pokročilejší konfigurace s externími nástroji, jako je zásuvný modul prohlížeče FoxyProxy nebo proxy server Privoxy, ale mohly by do vašeho nastavení vnést úniky informací.

### Jak nakonfiguruji svůj prohlížeč? {#browserproxy}

Tunel k hlavnímu IRC serveru v rámci I2P, Irc2P, se vytvoří při instalaci I2P (viz [konfigurační stránka I2PTunnel](http://localhost:7657/i2ptunnel/index.jsp)) a automaticky se spustí při startu I2P routeru. Pro připojení nastavte svého IRC klienta, aby se připojil k `localhost 6668`. Uživatelé klientů typu HexChat mohou vytvořit novou síť se serverem `localhost/6668` (nezapomeňte zaškrtnout "Obejít proxy server", pokud máte nakonfigurovaný proxy server). Uživatelé Weechatu mohou použít následující příkaz pro přidání nové sítě:

```
/server add irc2p localhost/6668
```
### Jak se připojím k IRC v rámci I2P? {#irc}

Nejjednodušší metodou je kliknout na odkaz [i2ptunnel](http://127.0.0.1:7657/i2ptunnel/) v konzoli routeru a vytvořit nový 'Server Tunnel'. Můžete poskytovat dynamický obsah nastavením cílové adresy tunelu na port existującího webového serveru, jako je Tomcat nebo Jetty. Můžete také poskytovat statický obsah. Pro tento účel nastavte cílovou adresu tunelu na: `0.0.0.0 port 7659` a umístěte obsah do adresáře `~/.i2p/eepsite/docroot/`. (V systémech jiných než Linux může být umístění jiné. Zkontrolujte konzoli routeru.) Software 'eepsite' je součástí instalačního balíčku I2P a je nastaven tak, aby se automaticky spouštěl při startu I2P. Výchozí stránka, která se tím vytvoří, je přístupná na adrese http://127.0.0.1:7658. Váš 'eepsite' je však také přístupný ostatním prostřednictvím souboru s klíčem eepsite, který se nachází v: `~/.i2p/eepsite/i2p/eepsite.keys`. Chcete-li se dozvědět více, přečtěte si soubor readme na adrese: `~/.i2p/eepsite/README.txt`.

### Jak nastavím svůj vlastní I2P web? {#myI2P-Site}

Záleží na vašem protivníkovi a vašem modelu hrozeb. Pokud se obáváte pouze firemních narušení "soukromí", běžných zločinců a cenzury, pak to není opravdu nebezpečné. Orgány činné v trestním řízení vás pravděpodobně stejně najdou, pokud budou opravdu chtít. Hostování pouze v době, kdy máte spuštěný běžný (internetový) domácí uživatelský prohlížeč, skutečně ztíží zjištění, kdo tu část hostuje. Zvažte prosím hostování vaší I2P stránky stejně jako hostování jakékoli jiné služby - je to stejně nebezpečné - nebo bezpečné - jako si to sami nakonfigurujete a spravujete.

Poznámka: Již existuje způsob, jak oddělit hostování i2p služby (destination) od i2p routeru. Pokud [rozumíte tomu, jak](/docs/overview/tech-intro#i2pservices) to funguje, můžete jednoduše nastavit samostatný počítač jako server pro webovou stránku (nebo službu), která bude veřejně přístupná, a přesměrovat to na webový server přes [velmi] zabezpečený SSH tunel nebo použít zabezpečený, sdílený souborový systém.

### Pokud provozuji webovou stránku na I2P doma, obsahující pouze HTML a CSS, je to nebezpečné? {#hosting}

Aplikace I2P Address Book mapuje lidsky čitelné názvy na dlouhodobé destinace spojené se službami, což ji činí spíše souborem hostitelů nebo seznamem kontaktů než síťovou databází nebo DNS službou. Je také primárně lokální – neexistuje uznávaný globální jmenný prostor, vy rozhodujete, na co se nakonec jakákoli daná .i2p doména mapuje. Střední cestou je něco, čemu se říká "Jump Service" (přesměrovací služba), která poskytuje lidsky čitelný název tím, že vás přesměruje na stránku, kde budete dotázáni "Udělujete routeru I2P oprávnění nazývat $SITE_CRYPTO_KEY názvem $SITE_NAME.i2p" nebo něco v tomto smyslu. Jakmile je záznam ve vašem address booku, můžete generovat vlastní jump URL pro pomoc s sdílením stránky s ostatními.

### Jak I2P nachází webové stránky ".i2p"? {#addresses}

Nemůžete přidat adresu, aniž byste znali alespoň base32 nebo base64 stránky, kterou chcete navštívit. "Hostname" (doménové jméno), který je čitelný pro člověka, je pouze alias pro kryptografickou adresu, která odpovídá base32 nebo base64. Bez kryptografické adresy neexistuje žádný způsob, jak přistupovat k I2P Site (I2P stránce), to je záměrné. Distribuce adresy lidem, kteří ji ještě neznají, je obvykle zodpovědností poskytovatele Jump služby. Návštěva I2P Site, která není známá, spustí použití Jump služby. stats.i2p je nejspolehlivější Jump služba.

Pokud hostujete stránku přes i2ptunnel, ještě nebude zaregistrována u jump service. Chcete-li jí přiřadit URL lokálně, navštivte konfigurační stránku a klikněte na tlačítko "Add to Local Address Book." Poté přejděte na http://127.0.0.1:7657/dns, kde najdete addresshelper URL a můžete ji sdílet.

### Jak přidám adresy do Adresáře? {#addressbook}

Porty používané I2P lze rozdělit do 2 sekcí:

1. Porty směřující k internetu, které jsou používány pro komunikaci s ostatními I2P routery
2. Lokální porty, pro lokální připojení

Ty jsou podrobně popsány níže.

#### 1. Internet-facing ports

Poznámka: Od verze 0.7.8 nové instalace nepoužívají port 8887; při prvním spuštění programu je vybrán náhodný port mezi 9000 a 31000. Vybraný port je zobrazen na [konfigurační stránce](http://127.0.0.1:7657/confignet) routeru.

**ODCHOZÍ**

- UDP z náhodného portu uvedeného na [konfigurační stránce](http://127.0.0.1:7657/confignet) na libovolné vzdálené UDP porty, umožňující odpovědi
- TCP z náhodných vysokých portů na libovolné vzdálené TCP porty
- Odchozí UDP na portu 123, umožňující odpovědi. To je nezbytné pro interní synchronizaci času I2P (prostřednictvím SNTP - dotazování náhodného SNTP hostitele v pool.ntp.org nebo jiného serveru, který zadáte)

**PŘÍCHOZÍ**

- (Volitelné, doporučené) UDP na port uvedený na [konfigurační stránce](http://127.0.0.1:7657/confignet) z libovolných umístění
- (Volitelné, doporučené) TCP na port uvedený na [konfigurační stránce](http://127.0.0.1:7657/confignet) z libovolných umístění
- Příchozí TCP lze zakázat na [konfigurační stránce](http://127.0.0.1:7657/confignet)

#### 2. Local I2P ports

Lokální I2P porty ve výchozím nastavení naslouchají pouze lokálním připojením, pokud není uvedeno jinak:

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
### Jaké porty používá I2P? {#ports}

Adresář je umístěn na [http://localhost:7657/dns](http://localhost:7657/dns), kde lze nalézt další informace.

**Jaké jsou dobré odkazy na předplatné adresáře?**

Můžete zkusit následující:

- [http://stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
- [http://identiguy.i2p/hosts.txt](http://identiguy.i2p/hosts.txt)

### How can I access the web console from my other machines or password protect it? {#remote_webconsole}

Z bezpečnostních důvodů administrátorská konzole routeru ve výchozím nastavení naslouchá připojením pouze na lokálním rozhraní.

Existují dvě metody pro vzdálený přístup ke konzoli:

1. SSH Tunnel
2. Konfigurace vaší konzole tak, aby byla dostupná na veřejné IP adrese s uživatelským jménem a heslem

Ty jsou podrobně popsány níže:

**Metoda 1: SSH tunel**

Pokud používáte unixový operační systém, jedná se o nejjednodušší metodu pro vzdálený přístup k vaší I2P konzoli. (Poznámka: SSH server je k dispozici i pro systémy se systémem Windows, například [https://github.com/PowerShell/Win32-OpenSSH](https://github.com/PowerShell/Win32-OpenSSH))

Jakmile máte nakonfigurován SSH přístup k vašemu systému, je příznaku SSH předán příznak '-L' s odpovídajícími argumenty - například:

```
ssh -L 7657:localhost:7657 (System_IP)
```
kde '(System_IP)' je nahrazeno IP adresou vašeho systému. Tento příkaz přesměruje port 7657 (číslo před první dvojtečkou) na port 7657 vzdáleného systému (jak je specifikováno řetězcem 'localhost' mezi první a druhou dvojtečkou) (číslo za druhou dvojtečkou). Vaše vzdálená I2P konzole bude nyní dostupná na vašem lokálním systému jako 'http://localhost:7657' a bude k dispozici po celou dobu trvání vaší SSH relace.

Pokud chcete spustit SSH relaci bez zahájení shellu na vzdáleném systému, můžete přidat příznak '-N':

```
ssh -NL 7657:localhost:7657 (System_IP)
```
**Metoda 2: Konfigurace vaší konzole tak, aby byla dostupná na veřejné IP adrese s uživatelským jménem a heslem**

1. Otevřete `~/.i2p/clients.config` a nahraďte:
   ```
   clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
   ```
   tímto:
   ```
   clientApp.0.args=7657 ::1,127.0.0.1,(System_IP) ./webapps/
   ```
   kde (System_IP) nahradíte veřejnou IP adresou vašeho systému

2. Přejděte na [http://localhost:7657/configui](http://localhost:7657/configui) a podle potřeby přidejte uživatelské jméno a heslo ke konzoli - Přidání uživatelského jména a hesla je vysoce doporučeno k zabezpečení vaší I2P konzole před neoprávněným zásahem, který by mohl vést k deanonymizaci.

3. Přejděte na [http://localhost:7657/index](http://localhost:7657/index) a klikněte na "Graceful restart", což restartuje JVM a znovu načte klientské aplikace

Poté, co se spustí, byste měli být schopni vzdáleně přistupovat ke své konzoli. Načtěte router konzoli na adrese `http://(IP_systému):7657` a budete vyzváni k zadání uživatelského jména a hesla, které jste zadali v kroku 2 výše, pokud váš prohlížeč podporuje autentizační popup.

POZNÁMKA: V uvedené konfiguraci můžete specifikovat 0.0.0.0. Toto určuje rozhraní, nikoli síť nebo síťovou masku. 0.0.0.0 znamená "navázat na všechna rozhraní", takže bude dostupné na 127.0.0.1:7657 i na jakékoli LAN/WAN IP adrese. Při použití této možnosti buďte opatrní, protože konzole bude dostupná na VŠECH adresách nakonfigurovaných ve vašem systému.

### How can I use applications from my other machines? {#remote_i2cp}

Přečtěte si prosím předchozí odpověď s pokyny k použití SSH Port Forwarding a také navštivte tuto stránku ve vaší konzoli: [http://localhost:7657/configi2cp](http://localhost:7657/configi2cp)

### V adresáři mi chybí spousta hostitelů. Jaké jsou dobré odkazy na odběry? {#subscriptions}

SOCKS proxy je funkční od verze 0.7.1. Podporovány jsou SOCKS 4/4a/5. I2P nemá SOCKS outproxy, taktakže je omezeno pouze na použití v rámci I2P.

Mnoho aplikací odhaluje citlivé informace, které vás mohou identifikovat na internetu, a to je riziko, kterého byste si měli být vědomi při používání I2P SOCKS proxy. I2P filtruje pouze data o připojení, ale pokud program, který chcete spustit, tyto informace odesílá jako obsah, I2P nemá žádnou možnost ochránit vaši anonymitu. Například některé e-mailové aplikace odešlou IP adresu počítače, na kterém běží, na poštovní server. Doporučujeme používat nástroje nebo aplikace specifické pro I2P (například [I2PSnark](http://localhost:7657/i2psnark/) pro torrenty), nebo aplikace, u kterých je známo, že jsou bezpečné pro použití s I2P, včetně oblíbených doplňků pro [Firefox](https://www.mozilla.org/).

### Jak mohu přistupovat k webové konzoli z jiných počítačů nebo ji chránit heslem? {#remote_webconsole}

Existují služby zvané Outproxy, které fungují jako most mezi I2P a internetem, podobně jako Tor Exit Nodes. Výchozí funkcionalita outproxy pro HTTP a HTTPS je poskytována službou `exit.stormycloud.i2p` a provozuje ji společnost StormyCloud Inc. Je nakonfigurována v HTTP Proxy. Navíc, aby byla lépe chráněna anonymita, I2P ve výchozím nastavení neumožňuje vytvářet anonymní připojení k běžnému internetu. Více informací naleznete na stránce [Socks Outproxy](/docs/api/socks#outproxy).

---

## Reseeds

### Jak mohu používat aplikace z mých dalších počítačů? {#remote_i2cp}

Nejprve zkontrolujte stránku [http://127.0.0.1:7657/netdb](http://127.0.0.1:7657/netdb) v Router Console – vaši síťovou databázi. Pokud nevidíte jediný router uvedený z I2P, ale konzole říká, že byste měli být za firewallem, pak se pravděpodobně nemůžete připojit k reseed serverům. Pokud vidíte jiné I2P routery uvedené, zkuste snížit počet maximálních připojení [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config), možná váš router nemůže zvládnout mnoho připojení.

### Je možné použít I2P jako SOCKS proxy? {#socks}

Za normálních okolností vás I2P připojí k síti automaticky pomocí našich bootstrapových odkazů. Pokud přerušené připojení k internetu způsobí selhání bootstrapování ze reseed serverů, jednoduchým způsobem bootstrapování je použití prohlížeče Tor (ve výchozím nastavení otevírá localhost), který funguje velmi dobře s [http://127.0.0.1:7657/configreseed](http://127.0.0.1:7657/configreseed). Je také možné provést reseed I2P routeru manuálně.

Při použití prohlížeče Tor k reseedu můžete vybrat více URL najednou a pokračovat. Ačkoli výchozí hodnota, která je 2 (z více url adres), bude také fungovat, ale bude to pomalé.

---

## Privacy-Safety

### Jak získám přístup k IRC, BitTorrentu nebo jiným službám na běžném internetu? {#proxy_other}

Ne, váš router se podílí na přenosu end-to-end šifrovaného provozu přes síť i2p ke koncovému bodu náhodného tunelu, obvykle ne k outproxy, ale žádný provoz není předáván mezi vaším routerem a internetem přes transportní vrstvu. Jako koncový uživatel byste neměli provozovat outproxy, pokud nejste zběhlí v administraci systémů a sítí.

### Is it easy to detect the use of I2P by analyzing network traffic? {#detection}

Provoz I2P obvykle vypadá jako UDP provoz a ne o moc víc – a cílem je, aby toho moc víc nepřipomínal. Podporuje také TCP. S určitým úsilím může pasivní analýza provozu klasifikovat provoz jako "I2P", ale doufáme, že pokračující vývoj maskování provozu to dále omezí. Dokonce i poměrně jednoduchá vrstva maskování protokolu jako obfs4 zabrání cenzorům v blokování I2P (je to cíl, který I2P sleduje).

### Můj router běží již několik minut a má nula nebo velmi málo spojení {#reseed}

Záleží na vašem osobním modelu hrozeb. Pro většinu lidí je I2P mnohem bezpečnější než nepoužívání žádné ochrany. Některé jiné sítě (jako Tor, mixminion/mixmaster) jsou pravděpodobně bezpečnější proti určitým protivníkům. Například provoz I2P nepoužívá TLS/SSL, taktakže nemá problémy s "nejslabším článkem", které má Tor. I2P používalo mnoho lidí v Sýrii během "Arabského jara" a v poslední době projekt zaznamenal větší růst v menších jazykových instalacích I2P na Blízkém a Středním východě. Nejdůležitější věcí, kterou je třeba zde poznamenat, je, že I2P je technologie a potřebujete návod, jak zlepšit své soukromí/anonymitu na internetu. Také zkontrolujte svůj prohlížeč nebo importujte vyhledávač otisků prstů, abyste zablokovali útoky pomocí otisků prstů s velmi velkou (což znamená: typické dlouhé chvosty / velmi přesná rozmanitá datová struktura) databází o mnoha věcech týkajících se prostředí a nepoužívejte VPN, abyste snížili všechna rizika, která z ní plynou, jako je chování vlastní TLS cache a technická konstrukce poskytovatele, která může být hacknuta snadněji než vlastní desktopový systém. Možná použití izolovaného Tor V-Browseru s jeho skvělými ochranami proti otiskům prstů a celkovou ochranou appguard-livetime-protection, která povoluje pouze nezbytnou systémovou komunikaci, a nakonec použití vm s anti-spy disable skripty a live-cd pro odstranění jakéhokoli "téměř trvalého možného rizika" a snížení všech rizik klesající pravděpodobností jsou dobrou možností ve veřejné síti a při špičkovém individuálním modelu rizik a mohou být tím nejlepším, co můžete udělat s tímto cílem pro použití i2p.

### Jak mohu provést ruční reseed? {#manual_reseed}

Ano, pro ostatní I2P uzly, které znají váš router. Používáme to k připojení ke zbytku I2P sítě. Adresy jsou fyzicky umístěny v objektech "routerInfos (klíč,hodnota)", buď vzdáleně načtených, nebo přijatých od partnera. "routerInfos" obsahuje některé informace (některé volitelně oportunisticky přidané), "publikované partnerem", o samotném routeru pro bootstrapping (初始启动). V tomto objektu nejsou žádná data o klientech. Bližší pohled pod kapotu vám řekne, že každý je počítán s nejnovějším typem vytváření identifikátorů nazývaným "SHA-256 Hashes (nízký=Pozitivní hash(-klíč), vysoký=Negativní hash(+klíč))". I2P síť má vlastní databázi dat routerInfos vytvořených během nahrávání a indexování, ale to hluboce závisí na realizaci tabulek klíč/hodnota a topologii sítě a stavu zatížení / stavu šířky pásma a pravděpodobnostech směrování pro uložení v databázových komponentách.

### Is using an outproxy safe? {#proxy_safe}

Záleží na tom, co máte na mysli pod pojmem "bezpečný". Outproxy jsou skvělé, když fungují, ale bohužel jsou dobrovolně provozovány lidmi, kteří mohou ztratit zájem nebo nemusí mít zdroje k jejich nepřetržitému provozu – uvědomte si prosím, že můžete zažít období, během kterých budou služby nedostupné, přerušované nebo nespolehlivé, a my nejsme spojeni s touto službou a nemáme na ni žádný vliv.

Samotné outproxy servery mohou vidět váš příchozí a odchozí provoz, s výjimkou end-to-end šifrovaných HTTPS/SSL dat, stejně jako váš poskytovatel internetu může vidět provoz přicházející a odcházející z vašeho počítače. Pokud věříte svému poskytovateli internetu, nebude to s outproxy o nic horší.

### Je můj router "výstupním uzlem" (outproxy) do běžného internetu? Nechci, aby to tak bylo. {#exit}

Pro velmi dlouhé vysvětlení si přečtěte více v našich článcích o [Modelu hrozeb](/docs/overview/threat-model). Obecně platí, že deanonymizace není triviální, ale je možná, pokud nejste dostatečně opatrní.

---

## Internet Access/Performance

### Je snadné detekovat používání I2P analýzou síťového provozu? {#detection}

Proxying na internetové stránky (eepsites, které vedou na internet) je poskytováno jako služba uživatelům I2P od poskytovatelů bez blokování. Tato služba není hlavním zaměřením vývoje I2P a je poskytována dobrovolně. Eepsites hostované na I2P by měly vždy fungovat bez outproxy. Outproxy jsou pohodlné, ale podle návrhu nejsou dokonalé ani velkou částí projektu. Uvědomte si, že nemusí být schopny poskytovat vysoce kvalitní služby, které mohou poskytovat jiné služby I2P.

### Je používání I2P bezpečné? {#safe}

Výchozí HTTP proxy podporuje pouze HTTP a HTTPS outproxying.

### V konzoli routeru vidím IP adresy všech ostatních I2P uzlů. Znamená to, že moje IP adresa je viditelná pro ostatní? {#netdb_ip}

Nejprve se ujistěte, že máte nejnovější verzi všech součástí souvisejících s I2P – starší verze obsahovaly zbytečné části kódu náročné na CPU. Existuje také [výkonnostní Log](/about/performance), který dokumentuje některá zlepšení výkonu I2P v průběhu času.

### Je používání outproxy bezpečné? {#proxy_safe}

Obecná stabilita sítě I2P je průběžnou oblastí výzkumu. Značná část tohoto výzkumu se zaměřuje na to, jak drobné změny v nastavení ovlivňují chování routeru. Protože I2P je peer-to-peer síť, akce ostatních účastníků budou mít vliv na výkon vašeho routeru.

### A co "de-anonymizační" útoky? {#deanon}

I2P má různé ochranné mechanismy, které přidávají další směrování a dodatečné vrstvy šifrování. Také odráží provoz přes další uzly (tunnels), které mají svou vlastní rychlost a kvalitu, některé jsou pomalé, jiné rychlé. To vše vede k vysoké režii a provozu v různém tempu a různými směry. Z principu tyto věci způsobí, že je I2P pomalejší ve srovnání s přímým připojením na internetu, ale mnohem anonymnější a stále dostatečně rychlé pro většinu účelů.

Níže je uveden příklad s vysvětlením, který pomůže poskytnout kontext pro úvahy o latenci a šířce pásma při používání I2P.

Zvažte níže uvedený diagram. Znázorňuje spojení mezi klientem provádějícím požadavek přes I2P, serverem přijímajícím požadavek přes I2P a následně odpovídajícím zpět také přes I2P. Zobrazen je také okruh, kterým požadavek cestuje.

Z diagramu vyplývá, že políčka označená 'P', 'Q' a 'R' představují odchozí tunnel pro 'A' a políčka označená 'X', 'Y' a 'Z' představují odchozí tunnel pro 'B'. Podobně políčka označená 'X', 'Y' a 'Z' představují příchozí tunnel pro 'B', zatímco políčka označená 'P_1', 'Q_1' a 'R_1' představují příchozí tunnel pro 'A'. Šipky mezi políčky ukazují směr provozu. Text nad a pod šipkami uvádí ukázkovou šířku pásma mezi párem skoků, stejně jako ukázkové latence.

Když klient i server používají 3-hopové tunnely, celkem 12 dalších I2P routerů se podílí na přenosu dat. 6 uzlů přenáší data z klienta na server, což je rozděleno do 3-hopového odchozího tunnelu z 'A' ('P', 'Q', 'R') a 3-hopového příchozího tunnelu do 'B' ('X', 'Y', 'Z'). Podobně 6 uzlů přenáší data ze serveru zpět ke klientovi.

Nejprve můžeme zvážit latenci - čas, který trvá, než požadavek od klienta projde sítí I2P, dorazí k serveru a vrátí se zpět ke klientovi. Sečtením všech latencí vidíme, že:

```
    40 + 100 + 20 + 60 + 80 + 10 + 30 ms        (client to server)
  + 60 + 40 + 80 + 60 + 100 + 20 + 40 ms        (server to client)
  -----------------------------------
  TOTAL:                          740 ms
```
Celková doba odezvy v našem příkladu činí 740 ms - rozhodně mnohem více, než by člověk obvykle viděl při procházení běžných internetových webových stránek.

Zadruhé můžeme zvážit dostupnou šířku pásma. Ta je určena nejpomalejším spojením mezi skoky od klienta k serveru a také při přenosu dat ze serveru ke klientovi. U provozu směřujícího od klienta k serveru vidíme, že dostupná šířka pásma v našem příkladu mezi skoky 'R' & 'X' a také skoky 'X' & 'Y' je 32 KB/s. Navzdory vyšší dostupné šířce pásma mezi ostatními skoky budou tyto skoky fungovat jako úzké hrdlo a omezí maximální dostupnou šířku pásma pro provoz z 'A' do 'B' na 32 KB/s. Podobně trasování cesty ze serveru ke klientovi ukazuje, že maximální šířka pásma je 64 KB/s - mezi skoky 'Z_1' & 'Y_1, 'Y_1' & 'X_1' a 'Q_1' & 'P_1'.

Doporučujeme zvýšit vaše limity šířky pásma. To pomůže síti zvýšením množství dostupné šířky pásma, což následně zlepší vaše zkušenosti s I2P. Nastavení šířky pásma najdete na stránce [http://localhost:7657/config](http://localhost:7657/config). Mějte prosím na paměti limity vašeho internetového připojení stanovené vaším poskytovatelem internetu a odpovídajícím způsobem upravte svá nastavení.

Doporučujeme také nastavit dostatečné množství sdílené šířky pásma - to umožňuje směrování participujících tunnelů přes váš I2P router. Povolení participujícího provozu udržuje váš router dobře integrovaný v síti a zlepšuje rychlost přenosu dat.

I2P je projekt, na kterém se neustále pracuje. Implementuje se mnoho vylepšení a oprav a obecně platí, že používání nejnovější verze pomůže vašemu výkonu. Pokud jste tak ještě neučinili, nainstalujte si nejnovější verzi.

### I think I found a bug, where can I report it? {#bug}

Jakékoliv chyby či problémy, se kterými se setkáte, můžete nahlásit v našem systému pro sledování chyb, který je dostupný jak přes běžný internet, tak přes I2P. Máme diskuzní fórum, které je také dostupné na I2P i na běžném internetu. Můžete se také připojit k našemu IRC kanálu: buď prostřednictvím naší IRC sítě IRC2P, nebo na Freenode.

- **Náš Bugtracker:**
  - Veřejný internet: [https://i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)
  - Na I2P: [http://git.idk.i2p/I2P_Developers/i2p.i2p/issues](http://git.idk.i2p/I2P_Developers/i2p.i2p/issues)
- **Naše fóra:** [i2pforum.i2p](http://i2pforum.i2p/)
- **Vkládání logů:** Můžete vložit jakékoliv zajímavé logy do služby pro vkládání textu, jako jsou služby na veřejném internetu uvedené na [PrivateBin Wiki](https://github.com/PrivateBin/PrivateBin/wiki/PrivateBin-Directory), nebo služby I2P jako tato [instance PrivateBin](http://paste.crypthost.i2p) nebo tato [služba pro vkládání textu bez Javascriptu](http://pasta-nojs.i2p) a poté pokračujte na IRC v #i2p
- **IRC:** Připojte se k #i2p-dev a diskutujte s vývojáři na IRC

Prosím, přiložte relevantní informace ze stránky logů routeru, která je dostupná na: [http://127.0.0.1:7657/logs](http://127.0.0.1:7657/logs). Žádáme vás, abyste sdíleli veškerý text z části 'I2P Version and Running Environment' (Verze I2P a běhové prostředí) stejně jako jakékoli chyby nebo varování zobrazené v různých logech na této stránce.

---

### Nemohu přistupovat k běžným internetovým stránkám přes I2P. {#outproxy}

Skvělé! Najdete nás na IRC:

- na `irc.freenode.net` kanál `#i2p`
- na `IRC2P` kanál `#i2p`

nebo napište na [fórum](http://i2pforum.i2p/) a my to zveřejníme zde (doufejme i s odpovědí).
