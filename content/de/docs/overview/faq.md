---
title: "Häufig gestellte Fragen"
description: "Umfassende I2P FAQ: Router-Hilfe, Konfiguration, Reseeds, Datenschutz/Sicherheit, Leistung und Fehlerbehebung"
slug: "faq"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: Dokumentation
---

## I2P Router Hilfe

### What systems will I2P run on? {#systems}

I2P ist in der Programmiersprache Java geschrieben. Es wurde auf Windows, Linux, FreeBSD und OSX getestet. Eine Android-Portierung ist ebenfalls verfügbar.

Was die Speichernutzung betrifft, ist I2P standardmäßig so konfiguriert, dass 128 MB RAM verwendet werden. Dies ist ausreichend für das Surfen und die Nutzung von IRC. Andere Aktivitäten können jedoch eine größere Speicherzuweisung erfordern. Wenn man beispielsweise einen Hochgeschwindigkeits-Router betreiben, an I2P-Torrents teilnehmen oder hochfrequentierte versteckte Dienste bereitstellen möchte, ist eine höhere Speichermenge erforderlich.

Was die CPU-Auslastung betrifft, wurde I2P erfolgreich auf bescheidenen Systemen wie der Raspberry Pi-Reihe von Einplatinencomputern getestet. Da I2P intensiv kryptografische Verfahren nutzt, ist eine leistungsstärkere CPU besser geeignet, um die von I2P erzeugte Last sowie Aufgaben des restlichen Systems (d.h. Betriebssystem, GUI, andere Prozesse wie z.B. Webbrowsing) zu bewältigen.

Die Verwendung von Sun/Oracle Java oder OpenJDK wird empfohlen.

### Auf welchen Systemen läuft I2P? {#systems}

Ja, Java wird für die Verwendung von I2P Core benötigt. Wir binden Java in unsere einfachen Installationsprogramme für Windows, Mac OSX und Linux ein. Wenn Sie die I2P-Android-App verwenden, benötigen Sie in den meisten Fällen auch eine Java-Laufzeitumgebung wie Dalvik oder ART.

### Ist die Installation von Java erforderlich, um I2P zu nutzen? {#java}

Eine I2P-Site ist eine normale Website, außer dass sie innerhalb von I2P gehostet wird. I2P-Sites haben Adressen, die wie normale Internetadressen aussehen und auf „.i2p" enden – auf eine für Menschen lesbare, nicht-kryptographische Weise, zum Vorteil der Nutzer. Die tatsächliche Verbindung zu einer I2P-Site erfordert Kryptographie, was bedeutet, dass I2P-Site-Adressen auch die langen „Base64"-Destinations und die kürzeren „B32"-Adressen sind. Möglicherweise müssen Sie zusätzliche Konfigurationen vornehmen, um korrekt zu browsen. Das Browsen von I2P-Sites erfordert die Aktivierung des HTTP-Proxys in Ihrer I2P-Installation und anschließend die Konfiguration Ihres Browsers, diesen zu verwenden. Für weitere Informationen schauen Sie in den Abschnitt „Browser" weiter unten oder in die Anleitung zur „Browser-Konfiguration".

### Was ist eine "I2P Site" und wie konfiguriere ich meinen Browser, um sie nutzen zu können? {#I2P-Site}

Auf der Peers-Seite in Ihrer Router-Konsole sehen Sie möglicherweise zwei Zahlen - Aktiv x/y. Die erste Zahl ist die Anzahl der Peers, an die Sie in den letzten Minuten eine Nachricht gesendet oder von denen Sie eine empfangen haben. Die zweite Zahl ist die Anzahl der kürzlich gesehenen Peers, diese ist immer größer oder gleich der ersten Zahl.

### Was bedeuten die Aktiv x/y Zahlen in der Router-Konsole? {#active}

Ja, das kann normal sein, besonders wenn der Router gerade erst gestartet wurde. Neue Router benötigen Zeit zum Hochfahren und zur Verbindung mit dem Rest des Netzwerks. Um die Netzwerkintegration, Verfügbarkeit und Leistung zu verbessern, überprüfen Sie diese Einstellungen:

- **Bandbreite teilen** - Wenn ein Router so konfiguriert ist, dass er Bandbreite teilt, leitet er mehr Verkehr für andere Router weiter, was dabei hilft, ihn in den Rest des Netzwerks zu integrieren und gleichzeitig die Leistung der eigenen lokalen Verbindung verbessert. Dies kann auf der Seite [http://localhost:7657/config](http://localhost:7657/config) konfiguriert werden.
- **Netzwerkschnittstelle** - Stellen Sie sicher, dass auf der Seite [http://localhost:7657/confignet](http://localhost:7657/confignet) keine Schnittstelle angegeben ist. Dies kann die Leistung verringern, es sei denn, Ihr Computer ist Multi-Homed mit mehreren externen IP-Adressen.
- **I2NP-Protokoll** - Stellen Sie sicher, dass der Router so konfiguriert ist, dass er Verbindungen über ein gültiges Protokoll für das Betriebssystem des Hosts und leere Netzwerk(Erweitert)-Einstellungen erwartet. Geben Sie keine IP-Adresse in das Feld 'Hostname' auf der Netzwerkkonfigurationsseite ein. Das hier ausgewählte I2NP-Protokoll wird nur verwendet, wenn Sie noch keine erreichbare Adresse haben. Die meisten Verizon 4G- und 5G-Drahtlosverbindungen in den Vereinigten Staaten blockieren beispielsweise UDP und können darüber nicht erreicht werden. Andere würden UDP zwangsweise verwenden, selbst wenn es ihnen zur Verfügung steht. Wählen Sie eine sinnvolle Einstellung aus den aufgelisteten I2NP-Protokollen.

### Mein Router hat sehr wenige aktive Peers, ist das in Ordnung? {#peers}

Nichts davon ist standardmäßig installiert. Da I2P jedoch ein Peer-to-Peer-Netzwerk ist, besteht die Möglichkeit, dass Sie versehentlich auf verbotene Inhalte stoßen. Hier ist eine Zusammenfassung, wie I2P verhindert, dass Sie unnötig in Verstöße gegen Ihre Überzeugungen verwickelt werden.

- **Verteilung** - Der Datenverkehr ist intern im I2P-Netzwerk, du bist kein [Exit-Knoten](#exit) (in unserer Dokumentation als Outproxy bezeichnet).
- **Speicherung** - Das I2P-Netzwerk führt keine verteilte Speicherung von Inhalten durch, dies muss vom Benutzer explizit installiert und konfiguriert werden (z.B. mit Tahoe-LAFS). Das ist eine Funktion eines anderen anonymen Netzwerks, [Freenet](http://freenetproject.org/). Durch den Betrieb eines I2P-Routers speicherst du keine Inhalte für andere.
- **Zugriff** - Dein Router wird ohne deine ausdrückliche Anweisung keine Inhalte anfordern.

### Ich bin gegen bestimmte Arten von Inhalten. Wie kann ich verhindern, dass ich sie verteile, speichere oder darauf zugreife? {#badcontent}

Ja, die bei weitem einfachste und häufigste Methode ist das Blockieren von Bootstrap- oder "Reseed"-Servern. Das vollständige Blockieren allen verschleierten Datenverkehrs würde ebenfalls funktionieren (obwohl dies viele, viele andere Dinge außer I2P blockieren würde und die meisten nicht bereit sind, so weit zu gehen). Im Fall der Reseed-Blockierung gibt es ein Reseed-Bundle auf Github; dessen Blockierung würde auch Github blockieren. Sie können Reseed über einen Proxy durchführen (viele sind im Internet zu finden, wenn Sie nicht Tor verwenden möchten) oder Reseed-Bundles auf Friend-to-Friend-Basis offline teilen.

### Ist es möglich, I2P zu blockieren? {#blocking}

Dieser Fehler tritt häufig bei jeder netzwerkfähigen Java-Software auf Systemen auf, die standardmäßig für die Verwendung von IPv6 konfiguriert sind. Es gibt mehrere Möglichkeiten, dies zu lösen:

- Auf Linux-basierten Systemen können Sie `echo 0 > /proc/sys/net/ipv6/bindv6only` ausführen
- Suchen Sie nach den folgenden Zeilen in `wrapper.config`:
  ```
  #wrapper.java.additional.5=-Djava.net.preferIPv4Stack=true
  #wrapper.java.additional.6=-Djava.net.preferIPv6Addresses=false
  ```
  Wenn die Zeilen vorhanden sind, entfernen Sie die Kommentarzeichen, indem Sie die "#" entfernen. Wenn die Zeilen nicht vorhanden sind, fügen Sie sie ohne die "#" hinzu.

Eine andere Möglichkeit wäre, die `::1` aus `~/.i2p/clients.config` zu entfernen

**WARNUNG**: Damit Änderungen an `wrapper.config` wirksam werden, müssen Sie den Router und den Wrapper vollständig stoppen. Ein Klick auf *Neustart* in Ihrer Router-Konsole wird diese Datei NICHT erneut einlesen! Sie müssen auf *Herunterfahren* klicken, 11 Minuten warten und dann I2P starten.

### In `wrapper.log` sehe ich einen Fehler mit dem Hinweis "`Protocol family unavailable`" beim Laden der Router Console {#protocolfamily}

Wenn man jede I2P-Site betrachtet, die jemals erstellt wurde, ja, die meisten sind offline. Menschen und I2P-Sites kommen und gehen. Ein guter Weg, um mit I2P zu beginnen, ist eine Liste von I2P-Sites zu prüfen, die derzeit online sind. [identiguy.i2p](http://identiguy.i2p) verfolgt aktive I2P-Sites.

### Die meisten I2P-Sites innerhalb von I2P sind nicht erreichbar? {#down}

Der Tanuki Java Service Wrapper, den wir verwenden, öffnet diesen Port – gebunden an localhost – um mit der im JVM laufenden Software zu kommunizieren. Wenn die JVM gestartet wird, erhält sie einen Schlüssel, damit sie sich mit dem Wrapper verbinden kann. Nachdem die JVM ihre Verbindung zum Wrapper hergestellt hat, lehnt der Wrapper alle weiteren Verbindungen ab.

Weitere Informationen finden Sie in der [Wrapper-Dokumentation](http://wrapper.tanukisoftware.com/doc/english/prop-port.html).

### Warum lauscht I2P auf Port 32000? {#port32000}

Die Proxy-Konfiguration für verschiedene Browser befindet sich auf einer separaten Seite mit Screenshots. Fortgeschrittenere Konfigurationen mit externen Tools, wie dem Browser-Plugin FoxyProxy oder dem Proxy-Server Privoxy, sind möglich, könnten aber Sicherheitslücken in Ihrer Konfiguration verursachen.

### Wie konfiguriere ich meinen Browser? {#browserproxy}

Ein Tunnel zum Haupt-IRC-Server innerhalb von I2P, Irc2P, wird bei der Installation von I2P erstellt (siehe die [I2PTunnel-Konfigurationsseite](http://localhost:7657/i2ptunnel/index.jsp)) und startet automatisch, wenn der I2P-Router startet. Um sich zu verbinden, konfigurieren Sie Ihren IRC-Client so, dass er sich mit `localhost 6668` verbindet. Benutzer von HexChat-ähnlichen Clients können ein neues Netzwerk mit dem Server `localhost/6668` erstellen (denken Sie daran, "Proxy-Server umgehen" anzukreuzen, wenn Sie einen Proxy-Server konfiguriert haben). Weechat-Benutzer können den folgenden Befehl verwenden, um ein neues Netzwerk hinzuzufügen:

```
/server add irc2p localhost/6668
```
### Wie verbinde ich mich mit IRC innerhalb von I2P? {#irc}

Die einfachste Methode ist, auf den [i2ptunnel](http://127.0.0.1:7657/i2ptunnel/)-Link in der Router-Konsole zu klicken und einen neuen 'Server Tunnel' zu erstellen. Sie können dynamische Inhalte bereitstellen, indem Sie das Tunnel-Ziel auf den Port eines bestehenden Webservers setzen, wie z.B. Tomcat oder Jetty. Sie können auch statische Inhalte bereitstellen. Setzen Sie dafür das Tunnel-Ziel auf: `0.0.0.0 port 7659` und platzieren Sie den Inhalt im Verzeichnis `~/.i2p/eepsite/docroot/`. (Auf Nicht-Linux-Systemen kann sich dies an einem anderen Ort befinden. Prüfen Sie die Router-Konsole.) Die 'eepsite'-Software ist Teil des I2P-Installationspakets und wird automatisch gestartet, wenn I2P gestartet wird. Die Standardseite, die dadurch erstellt wird, ist unter http://127.0.0.1:7658 erreichbar. Ihre 'eepsite' ist jedoch auch für andere über Ihre eepsite-Schlüsseldatei zugänglich, die sich hier befindet: `~/.i2p/eepsite/i2p/eepsite.keys`. Um mehr zu erfahren, lesen Sie die Readme-Datei unter: `~/.i2p/eepsite/README.txt`.

### Wie richte ich meine eigene I2P-Site ein? {#myI2P-Site}

Es hängt von Ihrem Gegner und Ihrem Bedrohungsmodell ab. Wenn Sie sich nur Sorgen um Verletzungen der "Privatsphäre" durch Unternehmen, typische Kriminelle und Zensur machen, dann ist es nicht wirklich gefährlich. Strafverfolgungsbehörden werden Sie wahrscheinlich trotzdem finden, wenn sie es wirklich wollen. Nur das Hosten, wenn Sie einen normalen (Internet-)Browser für Heimanwender laufen haben, macht es wirklich schwierig herauszufinden, wer diesen Teil hostet. Bitte betrachten Sie das Hosten Ihrer I2P-Site genauso wie das Hosten jedes anderen Dienstes - es ist so gefährlich - oder sicher - wie Sie es selbst konfigurieren und verwalten.

Hinweis: Es gibt bereits eine Möglichkeit, das Hosting eines I2P-Service (destination) vom I2P-Router zu trennen. Wenn Sie [verstehen, wie](/docs/overview/tech-intro#i2pservices) es funktioniert, können Sie einfach einen separaten Rechner als Server für die Website (oder den Service) einrichten, der öffentlich zugänglich sein wird, und diesen über einen [sehr] sicheren SSH-Tunnel an den Webserver weiterleiten oder ein gesichertes, gemeinsam genutztes Dateisystem verwenden.

### Wenn ich eine Website auf I2P zu Hause hoste, die nur HTML und CSS enthält, ist das gefährlich? {#hosting}

Die I2P Adressbuch-Anwendung ordnet menschenlesbare Namen langfristigen Destinations zu, die mit Diensten verknüpft sind, wodurch sie eher einer Hosts-Datei oder einer Kontaktliste ähnelt als einer Netzwerkdatenbank oder einem DNS-Dienst. Sie ist zudem lokal-zuerst ausgerichtet – es gibt keinen anerkannten globalen Namensraum, Sie entscheiden letztendlich selbst, worauf eine bestimmte .i2p-Domain verweist. Der Mittelweg ist ein sogenannter "Jump Service", der einen menschenlesbaren Namen bereitstellt, indem er Sie zu einer Seite weiterleitet, auf der Sie gefragt werden: "Erlauben Sie dem I2P-router, $SITE_CRYPTO_KEY den Namen $SITE_NAME.i2p zu geben" oder etwas in der Art. Sobald sich der Eintrag in Ihrem Adressbuch befindet, können Sie eigene Jump-URLs erstellen, um die Seite mit anderen zu teilen.

### Wie findet I2P „.i2p"-Websites? {#addresses}

Sie können keine Adresse hinzufügen, ohne mindestens die Base32- oder Base64-Adresse der Website zu kennen, die Sie besuchen möchten. Der "Hostname", der für Menschen lesbar ist, ist nur ein Alias für die kryptografische Adresse, die der Base32- oder Base64-Adresse entspricht. Ohne die kryptografische Adresse gibt es keine Möglichkeit, auf eine I2P-Website zuzugreifen – dies ist beabsichtigt. Die Verteilung der Adresse an Personen, die sie noch nicht kennen, liegt normalerweise in der Verantwortung des Jump-Service-Anbieters. Der Besuch einer unbekannten I2P-Website löst die Nutzung eines Jump-Services aus. stats.i2p ist der zuverlässigste Jump-Service.

Wenn Sie eine Website über i2ptunnel hosten, hat diese noch keine Registrierung bei einem Jump-Service. Um ihr lokal eine URL zu geben, besuchen Sie die Konfigurationsseite und klicken Sie auf die Schaltfläche "Add to Local Address Book". Gehen Sie dann zu http://127.0.0.1:7657/dns, um die Addresshelper-URL nachzuschlagen und zu teilen.

### Wie füge ich Adressen zum Adressbuch hinzu? {#addressbook}

Die von I2P verwendeten Ports können in 2 Bereiche unterteilt werden:

1. Internetfähige Ports, die für die Kommunikation mit anderen I2P-Routern verwendet werden
2. Lokale Ports für lokale Verbindungen

Diese werden im Folgenden detailliert beschrieben.

#### 1. Internet-facing ports

Hinweis: Seit Version 0.7.8 verwenden neue Installationen nicht mehr Port 8887; beim ersten Programmstart wird ein zufälliger Port zwischen 9000 und 31000 ausgewählt. Der ausgewählte Port wird auf der Router-[Konfigurationsseite](http://127.0.0.1:7657/confignet) angezeigt.

**AUSGEHEND**

- UDP vom zufälligen Port, der auf der [Konfigurationsseite](http://127.0.0.1:7657/confignet) aufgeführt ist, zu beliebigen entfernten UDP-Ports, mit Erlaubnis für Antworten
- TCP von zufälligen hohen Ports zu beliebigen entfernten TCP-Ports
- Ausgehende UDP-Verbindungen auf Port 123, mit Erlaubnis für Antworten. Dies ist für die interne Zeitsynchronisation von I2P erforderlich (über SNTP - Abfrage eines zufälligen SNTP-Hosts in pool.ntp.org oder eines anderen von Ihnen angegebenen Servers)

**EINGEHEND**

- (Optional, empfohlen) UDP zum Port, der auf der [Konfigurationsseite](http://127.0.0.1:7657/confignet) angegeben ist, von beliebigen Standorten
- (Optional, empfohlen) TCP zum Port, der auf der [Konfigurationsseite](http://127.0.0.1:7657/confignet) angegeben ist, von beliebigen Standorten
- Eingehendes TCP kann auf der [Konfigurationsseite](http://127.0.0.1:7657/confignet) deaktiviert werden

#### 2. Local I2P ports

Lokale I2P-Ports hören standardmäßig nur auf lokale Verbindungen, außer wo anders angegeben:

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
### Welche Ports verwendet I2P? {#ports}

Das Adressbuch befindet sich unter [http://localhost:7657/dns](http://localhost:7657/dns), wo weitere Informationen zu finden sind.

**Was sind gute Abonnement-Links für Adressbücher?**

Sie können Folgendes versuchen:

- [http://stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
- [http://identiguy.i2p/hosts.txt](http://identiguy.i2p/hosts.txt)

### How can I access the web console from my other machines or password protect it? {#remote_webconsole}

Aus Sicherheitsgründen akzeptiert die Admin-Konsole des Routers standardmäßig nur Verbindungen über die lokale Schnittstelle.

Es gibt zwei Methoden, um remote auf die Konsole zuzugreifen:

1. SSH Tunnel
2. Konfigurieren Sie Ihre Konsole so, dass sie über eine öffentliche IP-Adresse mit Benutzername und Passwort verfügbar ist

Diese werden im Folgenden detailliert beschrieben:

**Methode 1: SSH-Tunnel**

Wenn Sie ein Unix-ähnliches Betriebssystem verwenden, ist dies die einfachste Methode, um remote auf Ihre I2P-Konsole zuzugreifen. (Hinweis: SSH-Server-Software ist auch für Windows-Systeme verfügbar, zum Beispiel [https://github.com/PowerShell/Win32-OpenSSH](https://github.com/PowerShell/Win32-OpenSSH))

Sobald Sie den SSH-Zugriff auf Ihr System konfiguriert haben, wird das Flag '-L' mit entsprechenden Argumenten an SSH übergeben - zum Beispiel:

```
ssh -L 7657:localhost:7657 (System_IP)
```
wobei '(System_IP)' durch die IP-Adresse Ihres Systems ersetzt wird. Dieser Befehl leitet Port 7657 (die Zahl vor dem ersten Doppelpunkt) an den Port 7657 des entfernten Systems (angegeben durch die Zeichenkette 'localhost' zwischen dem ersten und zweiten Doppelpunkt) weiter (die Zahl nach dem zweiten Doppelpunkt). Ihre entfernte I2P-Konsole ist nun auf Ihrem lokalen System unter 'http://localhost:7657' verfügbar und bleibt so lange erreichbar, wie Ihre SSH-Sitzung aktiv ist.

Wenn Sie eine SSH-Sitzung starten möchten, ohne eine Shell auf dem entfernten System zu initiieren, können Sie das Flag '-N' hinzufügen:

```
ssh -NL 7657:localhost:7657 (System_IP)
```
**Methode 2: Konfiguration Ihrer Konsole für den Zugriff über eine öffentliche IP-Adresse mit Benutzername und Passwort**

1. Öffnen Sie `~/.i2p/clients.config` und ersetzen Sie:
   ```
   clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
   ```
   durch:
   ```
   clientApp.0.args=7657 ::1,127.0.0.1,(System_IP) ./webapps/
   ```
   wobei Sie (System_IP) durch die öffentliche IP-Adresse Ihres Systems ersetzen

2. Gehen Sie zu [http://localhost:7657/configui](http://localhost:7657/configui) und fügen Sie bei Bedarf einen Benutzernamen und ein Passwort für die Konsole hinzu - Das Hinzufügen eines Benutzernamens und Passworts wird dringend empfohlen, um Ihre I2P-Konsole vor Manipulation zu schützen, die zu einer De-Anonymisierung führen könnte.

3. Gehen Sie zu [http://localhost:7657/index](http://localhost:7657/index) und klicken Sie auf "Graceful restart", wodurch die JVM neu gestartet und die Client-Anwendungen neu geladen werden

Nachdem dies gestartet wurde, sollten Sie nun in der Lage sein, Ihre Konsole aus der Ferne zu erreichen. Laden Sie die Router-Konsole unter `http://(System_IP):7657` und Sie werden nach dem Benutzernamen und Passwort gefragt, die Sie in Schritt 2 oben angegeben haben, sofern Ihr Browser das Authentifizierungs-Popup unterstützt.

HINWEIS: Sie können 0.0.0.0 in der obigen Konfiguration angeben. Dies spezifiziert eine Schnittstelle, nicht ein Netzwerk oder eine Netzmaske. 0.0.0.0 bedeutet "an alle Schnittstellen binden", sodass es sowohl unter 127.0.0.1:7657 als auch unter jeder LAN/WAN-IP erreichbar ist. Seien Sie vorsichtig bei der Verwendung dieser Option, da die Konsole auf ALLEN auf Ihrem System konfigurierten Adressen verfügbar sein wird.

### How can I use applications from my other machines? {#remote_i2cp}

Bitte siehe die vorherige Antwort für Anweisungen zur Verwendung von SSH Port Forwarding und siehe auch diese Seite in deiner Konsole: [http://localhost:7657/configi2cp](http://localhost:7657/configi2cp)

### In meinem Adressbuch fehlen viele Hosts. Welche guten Abonnement-Links gibt es? {#subscriptions}

Der SOCKS-Proxy ist seit Version 0.7.1 funktionsfähig. SOCKS 4/4a/5 werden unterstützt. I2P hat keinen SOCKS-Outproxy, daher ist die Nutzung auf I2P beschränkt.

Viele Anwendungen geben sensible Informationen preis, die Sie im Internet identifizieren könnten, und dies ist ein Risiko, dessen Sie sich bewusst sein sollten, wenn Sie den I2P-SOCKS-Proxy verwenden. I2P filtert nur Verbindungsdaten, aber wenn das Programm, das Sie verwenden möchten, diese Informationen als Inhalt sendet, kann I2P Ihre Anonymität nicht schützen. Beispielsweise senden einige E-Mail-Anwendungen die IP-Adresse des Rechners, auf dem sie laufen, an einen Mailserver. Wir empfehlen I2P-spezifische Tools oder Anwendungen (wie [I2PSnark](http://localhost:7657/i2psnark/) für Torrents) oder Anwendungen, die bekanntermaßen sicher mit I2P verwendet werden können, einschließlich beliebter Plugins für [Firefox](https://www.mozilla.org/).

### Wie kann ich von anderen Rechnern auf die Web-Konsole zugreifen oder sie mit einem Passwort schützen? {#remote_webconsole}

Es gibt Dienste namens Outproxies, die zwischen I2P und dem Internet vermitteln, ähnlich wie Tor Exit Nodes. Die Standard-Outproxy-Funktionalität für HTTP und HTTPS wird von `exit.stormycloud.i2p` bereitgestellt und von StormyCloud Inc. betrieben. Sie wird im HTTP-Proxy konfiguriert. Um die Anonymität zu schützen, erlaubt I2P standardmäßig keine anonymen Verbindungen zum regulären Internet. Weitere Informationen finden Sie auf der [Socks Outproxy](/docs/api/socks#outproxy)-Seite.

---

## Reseeds

### Wie kann ich Anwendungen von meinen anderen Rechnern verwenden? {#remote_i2cp}

Überprüfen Sie zunächst die [http://127.0.0.1:7657/netdb](http://127.0.0.1:7657/netdb) Seite in der Router-Konsole – Ihre Netzwerkdatenbank. Wenn Sie keinen einzigen Router innerhalb von I2P aufgelistet sehen, die Konsole aber anzeigt, dass Sie durch eine Firewall geschützt sein sollten, dann können Sie wahrscheinlich keine Verbindung zu den Reseed-Servern herstellen. Wenn Sie andere I2P-Router aufgelistet sehen, versuchen Sie, die maximale Anzahl an Verbindungen unter [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config) zu verringern – möglicherweise kann Ihr Router nicht viele Verbindungen gleichzeitig verarbeiten.

### Ist es möglich, I2P als SOCKS-Proxy zu verwenden? {#socks}

Unter normalen Umständen verbindet I2P Sie automatisch mit dem Netzwerk über unsere Bootstrap-Links. Wenn eine gestörte Internetverbindung das Bootstrapping von Reseed-Servern fehlschlagen lässt, ist eine einfache Möglichkeit zum Bootstrapping die Verwendung des Tor-Browsers (standardmäßig öffnet er localhost), der sehr gut mit [http://127.0.0.1:7657/configreseed](http://127.0.0.1:7657/configreseed) funktioniert. Es ist auch möglich, einen I2P-Router manuell zu reseeden.

Wenn Sie den Tor-Browser zum Reseeden verwenden, können Sie mehrere URLs gleichzeitig auswählen und fortfahren. Obwohl der Standardwert von 2 (aus den mehreren URLs) ebenfalls funktioniert, wird es langsam sein.

---

## Privacy-Safety

### Wie greife ich auf IRC, BitTorrent oder andere Dienste im regulären Internet zu? {#proxy_other}

Nein, Ihr Router beteiligt sich am Transport von Ende-zu-Ende verschlüsseltem Datenverkehr über das I2P-Netzwerk zu einem zufälligen Tunnel-Endpunkt, normalerweise kein Outproxy, aber es wird kein Datenverkehr zwischen Ihrem Router und dem Internet über die Transportschicht weitergeleitet. Als Endbenutzer sollten Sie keinen Outproxy betreiben, wenn Sie nicht in System- und Netzwerkadministration erfahren sind.

### Is it easy to detect the use of I2P by analyzing network traffic? {#detection}

I2P-Verkehr sieht normalerweise wie UDP-Verkehr aus, und nicht viel mehr – und es so aussehen zu lassen wie nicht viel mehr ist ein Ziel. Es unterstützt auch TCP. Mit einigem Aufwand kann eine passive Verkehrsanalyse den Verkehr möglicherweise als "I2P" klassifizieren, aber wir hoffen, dass die kontinuierliche Entwicklung der Verkehrsverschleierung dies weiter reduzieren wird. Selbst eine relativ einfache Protokollverschleierungsschicht wie obfs4 wird Zensoren daran hindern, I2P zu blockieren (es ist ein Ziel, das I2P implementiert).

### Mein Router läuft seit mehreren Minuten und hat null oder sehr wenige Verbindungen {#reseed}

Es hängt von Ihrem persönlichen Bedrohungsmodell ab. Für die meisten Menschen ist I2P wesentlich sicherer als gar keinen Schutz zu verwenden. Einige andere Netzwerke (wie Tor, mixminion/mixmaster) sind wahrscheinlich sicherer gegen bestimmte Angreifer. Zum Beispiel verwendet I2P-Verkehr kein TLS/SSL, sodass es nicht die "schwächstes Glied"-Probleme hat, die Tor aufweist. I2P wurde von vielen Menschen in Syrien während des "Arabischen Frühlings" genutzt, und kürzlich hat das Projekt ein größeres Wachstum bei kleineren sprachlichen Installationen von I2P im Nahen und Mittleren Osten verzeichnet. Das Wichtigste hierbei ist zu beachten, dass I2P eine Technologie ist und Sie eine Anleitung/einen Leitfaden benötigen, um Ihre Privatsphäre/Anonymität im Internet zu verbessern. Überprüfen Sie auch Ihren Browser oder importieren Sie die Fingerprint-Suchmaschine, um Fingerprint-Angriffe mit einem sehr großen (bedeutet: typische Long Tails / sehr präzise diverse Datenstruktur) Datensatz über viele Umgebungsmerkmale zu blockieren, und verwenden Sie kein VPN, um alle Risiken zu reduzieren, die von ihm selbst ausgehen, wie das eigene TLS-Cache-Verhalten und die technische Konstruktion des Provider-Geschäfts, das einfacher gehackt werden kann als ein eigenes Desktop-System. Die Verwendung eines isolierten Tor-V-Browsers mit seinen großartigen Anti-Fingerprint-Schutzmaßnahmen und einem umfassenden Appguard-Livetime-Schutz, der nur die notwendigen Systemkommunikationen erlaubt, sowie eine letzte VM-Nutzung mit Anti-Spionage-Deaktivierungsskripten und Live-CD, um jedes "nahezu dauerhaft mögliche Risiko" zu beseitigen und alle Risiken durch abnehmende Wahrscheinlichkeit zu reduzieren, könnte eine gute Option in öffentlichen Netzwerken und bei hohem individuellem Risikomodell sein und möglicherweise das Beste, was Sie mit diesem Ziel für die I2P-Nutzung tun können.

### Wie führe ich ein manuelles Reseeding durch? {#manual_reseed}

Ja, für andere I2P-Knoten, die Ihren Router kennen. Wir verwenden dies, um uns mit dem Rest des I2P-Netzwerks zu verbinden. Die Adressen befinden sich physisch in "routerInfos (Schlüssel-Wert-Objekten)", die entweder remote abgerufen oder von Peers empfangen werden. Die "routerInfos" enthalten einige Informationen (einige optional opportunistisch hinzugefügt), "vom Peer veröffentlicht", über den Router selbst zum Bootstrapping. In diesem Objekt befinden sich keine Daten über Clients. Ein genauerer Blick unter die Haube zeigt, dass jeder mit der neuesten Art der ID-Erstellung gezählt wird, die "SHA-256 Hashes (niedrig=Positiver Hash(-Schlüssel), hoch=Negativer Hash(+Schlüssel))" genannt wird. Das I2P-Netzwerk verfügt über eine eigene Datenbank mit routerInfos, die während des Uploads und der Indizierung erstellt werden, aber dies hängt tief von der Realisierung der Schlüssel-/Werttabellen und der Netzwerktopologie sowie dem Auslastungszustand / Bandbreitenzustand und den Routing-Wahrscheinlichkeiten für Speicherungen in DB-Komponenten ab.

### Is using an outproxy safe? {#proxy_safe}

Es kommt darauf an, was Sie unter „sicher" verstehen. Outproxies sind großartig, wenn sie funktionieren, aber leider werden sie freiwillig von Personen betrieben, die das Interesse verlieren oder nicht die Ressourcen haben könnten, um sie rund um die Uhr zu betreiben – bitte beachten Sie, dass es Zeiträume geben kann, in denen Dienste nicht verfügbar, unterbrochen oder unzuverlässig sind, und wir sind nicht mit diesem Dienst verbunden und haben keinen Einfluss darauf.

Die Outproxys selbst können Ihren Datenverkehr sehen, mit Ausnahme von Ende-zu-Ende-verschlüsselten HTTPS/SSL-Daten, genauso wie Ihr Internetanbieter Ihren Datenverkehr von Ihrem Computer sehen kann. Wenn Sie Ihrem Internetanbieter vertrauen, wäre es mit dem Outproxy nicht schlechter.

### Ist mein Router ein "Exit-Node" (Outproxy) zum regulären Internet? Ich möchte nicht, dass er das ist. {#exit}

Für eine sehr ausführliche Erklärung lesen Sie mehr in unseren Artikeln über [Bedrohungsmodell](/docs/overview/threat-model). Im Allgemeinen ist eine De-Anonymisierung nicht trivial, aber möglich, wenn Sie nicht vorsichtig genug sind.

---

## Internet Access/Performance

### Ist es einfach, die Nutzung von I2P durch die Analyse von Netzwerkverkehr zu erkennen? {#detection}

Das Proxying zu Internet-Seiten (eepsites, die auf das Internet zugreifen) wird I2P-Nutzern als Dienst von Non-Block-Anbietern zur Verfügung gestellt. Dieser Dienst steht nicht im Hauptfokus der I2P-Entwicklung und wird auf freiwilliger Basis bereitgestellt. Eepsites, die auf I2P gehostet werden, sollten immer ohne Outproxy funktionieren. Outproxies sind eine praktische Ergänzung, aber sie sind konzeptbedingt weder perfekt noch ein wesentlicher Bestandteil des Projekts. Beachten Sie, dass sie möglicherweise nicht die hochwertige Dienstqualität bieten können, die andere Dienste von I2P bereitstellen.

### Ist die Nutzung von I2P sicher? {#safe}

Der Standard-HTTP-Proxy unterstützt nur HTTP- und HTTPS-Outproxying.

### Ich sehe IP-Adressen aller anderen I2P-Knoten in der Router-Konsole. Bedeutet das, dass meine IP-Adresse für andere sichtbar ist? {#netdb_ip}

Stellen Sie zunächst sicher, dass Sie die neueste Version aller I2P-bezogenen Komponenten haben – ältere Versionen enthielten unnötige CPU-intensive Abschnitte im Code. Es gibt auch ein [Performance-Log](/about/performance), das einige der Verbesserungen der I2P-Performance im Laufe der Zeit dokumentiert.

### Ist die Verwendung eines Outproxys sicher? {#proxy_safe}

Die allgemeine Stabilität des I2P-Netzwerks ist ein fortlaufendes Forschungsgebiet. Ein besonderer Schwerpunkt dieser Forschung liegt darauf, wie kleine Änderungen an Konfigurationseinstellungen das Verhalten des Routers verändern. Da I2P ein Peer-to-Peer-Netzwerk ist, werden die Aktionen anderer Peers einen Einfluss auf die Leistung Ihres Routers haben.

### Was ist mit „De-Anonymisierungs"-Angriffen? {#deanon}

I2P verfügt über verschiedene Schutzmaßnahmen, die zusätzliches Routing und weitere Verschlüsselungsebenen hinzufügen. Es leitet auch den Datenverkehr über andere Peers (Tunnels) um, die ihre eigene Geschwindigkeit und Qualität haben – manche sind langsam, manche schnell. Dies führt zu erheblichem Overhead und Datenverkehr mit unterschiedlichem Tempo in verschiedene Richtungen. Durch dieses Design sind all diese Dinge im Vergleich zu einer direkten Verbindung im Internet langsamer, aber deutlich anonymer und dennoch für die meisten Anwendungsfälle schnell genug.

Unten wird ein Beispiel mit Erklärung präsentiert, um etwas Kontext zu den Latenz- und Bandbreitenüberlegungen bei der Nutzung von I2P zu bieten.

Betrachten Sie das folgende Diagramm. Es zeigt eine Verbindung zwischen einem Client, der eine Anfrage über I2P stellt, einem Server, der die Anfrage über I2P empfängt und dann ebenfalls über I2P antwortet. Der Pfad, den die Anfrage durchläuft, ist ebenfalls dargestellt.

Betrachten Sie im Diagramm die mit 'P', 'Q' und 'R' beschrifteten Boxen als einen ausgehenden Tunnel für 'A' und die mit 'X', 'Y' und 'Z' beschrifteten Boxen als einen ausgehenden Tunnel für 'B'. Entsprechend stellen die mit 'X', 'Y' und 'Z' beschrifteten Boxen einen eingehenden Tunnel für 'B' dar, während die mit 'P_1', 'Q_1' und 'R_1' beschrifteten Boxen einen eingehenden Tunnel für 'A' darstellen. Die Pfeile zwischen den Boxen zeigen die Richtung des Datenverkehrs. Der Text über und unter den Pfeilen enthält Beispielwerte für die Bandbreite zwischen einem Hop-Paar sowie Beispiel-Latenzen.

Wenn sowohl Client als auch Server durchgehend 3-Hop-Tunnel verwenden, sind insgesamt 12 weitere I2P-Router an der Weiterleitung des Datenverkehrs beteiligt. 6 Peers leiten den Datenverkehr vom Client zum Server weiter, der in einen 3-Hop-Outbound-Tunnel von 'A' ('P', 'Q', 'R') und einen 3-Hop-Inbound-Tunnel zu 'B' ('X', 'Y', 'Z') aufgeteilt ist. Ebenso leiten 6 Peers den Datenverkehr vom Server zurück zum Client weiter.

Zunächst können wir die Latenz betrachten - die Zeit, die eine Anfrage von einem Client benötigt, um das I2P-Netzwerk zu durchqueren, den Server zu erreichen und zurück zum Client zu gelangen. Addiert man alle Latenzen, sehen wir, dass:

```
    40 + 100 + 20 + 60 + 80 + 10 + 30 ms        (client to server)
  + 60 + 40 + 80 + 60 + 100 + 20 + 40 ms        (server to client)
  -----------------------------------
  TOTAL:                          740 ms
```
Die gesamte Roundtrip-Zeit in unserem Beispiel beträgt 740 ms – deutlich höher als das, was man normalerweise beim Surfen auf regulären Internet-Websites sehen würde.

Zweitens können wir die verfügbare Bandbreite betrachten. Diese wird durch die langsamste Verbindung zwischen den Hops vom Client zum Server sowie bei der Übertragung von Datenverkehr vom Server zum Client bestimmt. Für Datenverkehr vom Client zum Server sehen wir in unserem Beispiel, dass die verfügbare Bandbreite zwischen den Hops 'R' & 'X' sowie den Hops 'X' & 'Y' 32 KB/s beträgt. Trotz höherer verfügbarer Bandbreite zwischen den anderen Hops werden diese Hops als Engpass fungieren und die maximal verfügbare Bandbreite für Datenverkehr von 'A' nach 'B' auf 32 KB/s begrenzen. Ebenso zeigt die Verfolgung des Pfades vom Server zum Client, dass es eine maximale Bandbreite von 64 KB/s gibt - zwischen den Hops 'Z_1' & 'Y_1', 'Y_1' & 'X_1' und 'Q_1' & 'P_1'.

Wir empfehlen, Ihre Bandbreitenlimits zu erhöhen. Dies hilft dem Netzwerk, indem die Menge der verfügbaren Bandbreite erhöht wird, was wiederum Ihre I2P-Erfahrung verbessert. Die Bandbreiteneinstellungen finden Sie auf der Seite [http://localhost:7657/config](http://localhost:7657/config). Bitte beachten Sie die Limits Ihrer Internetverbindung, die von Ihrem Internetanbieter festgelegt werden, und passen Sie Ihre Einstellungen entsprechend an.

Wir empfehlen außerdem, eine ausreichende Menge an geteilter Bandbreite festzulegen - dies ermöglicht es, dass participating tunnels über Ihren I2P router geleitet werden. Das Zulassen von participating traffic hält Ihren router gut ins Netzwerk integriert und verbessert Ihre Übertragungsgeschwindigkeiten.

I2P ist ein laufendes Projekt. Viele Verbesserungen und Fehlerbehebungen werden implementiert, und im Allgemeinen wird die Verwendung der neuesten Version Ihre Leistung verbessern. Falls noch nicht geschehen, installieren Sie die neueste Version.

### I think I found a bug, where can I report it? {#bug}

Sie können alle Fehler/Probleme, auf die Sie stoßen, in unserem Bugtracker melden, der sowohl über das normale Internet als auch über I2P verfügbar ist. Wir haben ein Diskussionsforum, das ebenfalls über I2P und das normale Internet verfügbar ist. Sie können auch unserem IRC-Kanal beitreten: entweder über unser IRC-Netzwerk, IRC2P, oder auf Freenode.

- **Unser Bugtracker:**
  - Non-private internet: [https://i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)
  - Auf I2P: [http://git.idk.i2p/I2P_Developers/i2p.i2p/issues](http://git.idk.i2p/I2P_Developers/i2p.i2p/issues)
- **Unsere Foren:** [i2pforum.i2p](http://i2pforum.i2p/)
- **Logs einfügen:** Sie können interessante Logs in einen Paste-Dienst einfügen, wie z.B. die auf dem [PrivateBin Wiki](https://github.com/PrivateBin/PrivateBin/wiki/PrivateBin-Directory) gelisteten Non-private-Internet-Dienste, oder einen I2P-Paste-Dienst wie diese [PrivateBin-Instanz](http://paste.crypthost.i2p) oder diesen [Javascript-freien Paste-Dienst](http://pasta-nojs.i2p) und anschließend im IRC in #i2p nachfragen
- **IRC:** Treten Sie #i2p-dev bei, um mit den Entwicklern im IRC zu diskutieren

Bitte fügen Sie relevante Informationen von der Router-Protokollseite hinzu, die verfügbar ist unter: [http://127.0.0.1:7657/logs](http://127.0.0.1:7657/logs). Wir bitten Sie, den gesamten Text aus dem Abschnitt 'I2P Version and Running Environment' sowie alle Fehler oder Warnungen, die in den verschiedenen auf der Seite angezeigten Protokollen erscheinen, mit uns zu teilen.

---

### Ich kann nicht auf normale Internet-Seiten über I2P zugreifen. {#outproxy}

Großartig! Finde uns auf IRC:

- auf `irc.freenode.net` Kanal `#i2p`
- auf `IRC2P` Kanal `#i2p`

oder poste im [Forum](http://i2pforum.i2p/) und wir werden es hier veröffentlichen (hoffentlich mit der Antwort).
