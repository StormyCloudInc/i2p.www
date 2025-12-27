---
title: "常见问题"
description: "I2P 综合常见问题解答：router 帮助、配置、重新播种、隐私/安全、性能和故障排除"
slug: "faq"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: 文档
---

## I2P Router 帮助

### What systems will I2P run on? {#systems}

I2P 是用 Java 编程语言编写的。它已在 Windows、Linux、FreeBSD 和 OSX 上进行了测试。同时还提供了 Android 版本。

在内存使用方面，I2P 默认配置使用 128 MB 的内存。这对于浏览网页和使用 IRC 来说已经足够。然而，其他活动可能需要分配更多内存。例如，如果想要运行高带宽 router、参与 I2P 种子下载或提供高流量的隐藏服务，则需要更多的内存。

在CPU使用方面,I2P已经过测试,可以在诸如树莓派系列单板计算机这样的低配置系统上运行。由于I2P大量使用加密技术,更强大的CPU将更适合处理I2P产生的工作负载以及系统其他部分相关的任务(即操作系统、图形界面、其他进程,如网页浏览)。

推荐使用 Sun/Oracle Java 或 OpenJDK。

### I2P 可以在哪些系统上运行？{#systems}

是的，使用 I2P Core 需要 Java。我们在 Windows、Mac OSX 和 Linux 的简易安装程序中已包含 Java。如果你运行 I2P Android 应用程序，在大多数情况下还需要安装 Java 运行时，如 Dalvik 或 ART。

### 使用 I2P 需要安装 Java 吗？ {#java}

I2P 站点是一个普通网站，只不过它托管在 I2P 内部。I2P 站点的地址看起来像普通的互联网地址，以".i2p"结尾，采用人类可读的非加密方式，方便人们使用。实际连接到 I2P 站点需要加密技术，这意味着 I2P 站点地址也可以是长格式的"Base64"目的地址和较短的"B32"地址。您可能需要进行额外配置才能正确浏览。浏览 I2P 站点需要在您的 I2P 安装中激活 HTTP 代理，然后配置您的浏览器使用该代理。更多信息请浏览下面的"浏览器"部分或"浏览器配置"指南。

### 什么是"I2P Site"，我该如何配置浏览器以使用它们？ {#I2P-Site}

在路由器控制台的 Peers 页面中,您可能会看到两个数字 - Active x/y。第一个数字是您在最近几分钟内发送或接收消息的对等节点数量。第二个数字是最近看到的对等节点数量,这个数字总是大于或等于第一个数字。

### 路由器控制台中的 Active x/y 数字是什么意思？{#active}

是的，这可能是正常的，特别是当 router 刚刚启动时。新的 router 需要时间来启动并连接到网络的其他部分。为了帮助改善网络集成、运行时间和性能，请检查以下设置：

- **共享带宽** - 如果 router 配置为共享带宽,它将为其他 router 路由更多流量,这有助于将其与网络的其余部分集成,并改善本地连接的性能。这可以在 [http://localhost:7657/config](http://localhost:7657/config) 页面上配置。
- **网络接口** - 确保在 [http://localhost:7657/confignet](http://localhost:7657/confignet) 页面上没有指定接口。这可能会降低性能,除非您的计算机是多宿主的,具有多个外部 IP 地址。
- **I2NP 协议** - 确保 router 配置为在主机操作系统和空网络(高级)设置的有效协议上接受连接。不要在网络配置页面的"主机名"字段中输入 IP 地址。只有在您还没有可达地址时,才会使用您在此处选择的 I2NP 协议。例如,美国的大多数 Verizon 4G 和 5G 无线连接会阻止 UDP,因此无法通过 UDP 到达。其他人即使可以使用 UDP 也会强制使用 UDP。从列出的 I2NP 协议中选择一个合理的设置。

### 我的 router 只有很少的活跃对等节点，这样正常吗？ {#peers}

默认情况下不会安装任何此类内容。然而，由于 I2P 是一个点对点网络，您可能会意外遇到违禁内容。以下是 I2P 如何防止您不必要地卷入违反您信念的行为的概述。

- **分发** - 流量仅在 I2P 网络内部传输,您不是[出口节点](#exit)(在我们的文档中称为 outproxy)。
- **存储** - I2P 网络不进行内容的分布式存储,这需要用户专门安装和配置(例如使用 Tahoe-LAFS)。这是另一个匿名网络 [Freenet](http://freenetproject.org/) 的特性。运行 I2P router 不会为任何人存储内容。
- **访问** - 您的 router 不会在没有您明确指令的情况下请求任何内容。

### 我反对某些类型的内容。如何避免分发、存储或访问它们？ {#badcontent}

是的，目前最简单和最常见的方法是屏蔽引导服务器，即"Reseed"服务器。完全屏蔽所有混淆流量也能达到目的（尽管这会破坏许多其他非 I2P 的服务，大多数人不愿意走到这一步）。在 reseed 屏蔽的情况下，Github 上有一个 reseed 包，屏蔽它也会同时屏蔽 Github。你可以通过代理进行 reseed（如果不想使用 Tor，可以在互联网上找到许多代理），或者以朋友间离线分享的方式共享 reseed 包。

### 是否可能封锁 I2P？ {#blocking}

通常，这个错误会在某些默认配置为使用 IPv6 的系统上运行任何启用网络的 Java 软件时出现。有几种方法可以解决此问题：

- 在基于 Linux 的系统上,你可以执行 `echo 0 > /proc/sys/net/ipv6/bindv6only`
- 在 `wrapper.config` 中查找以下行:
  ```
  #wrapper.java.additional.5=-Djava.net.preferIPv4Stack=true
  #wrapper.java.additional.6=-Djava.net.preferIPv6Addresses=false
  ```
  如果这些行存在,通过删除"#"来取消注释。如果这些行不存在,则添加它们但不带"#"。

另一个选项是从 `~/.i2p/clients.config` 中删除 `::1`

**警告**：要使对 `wrapper.config` 的任何更改生效，您必须完全停止 router 和 wrapper。在路由器控制台上点击 *重启* 不会重新读取此文件！您必须点击 *关闭*，等待11分钟，然后启动 I2P。

### 在 `wrapper.log` 中，加载路由器控制台时我看到一个错误提示 "`Protocol family unavailable`" {#protocolfamily}

如果你考虑所有曾经创建过的 I2P 站点，是的，大多数都已经关闭了。人们和 I2P 站点来来去去。开始使用 I2P 的一个好方法是查看当前在线的 I2P 站点列表。[identiguy.i2p](http://identiguy.i2p) 会跟踪活跃的 I2P 站点。

### I2P 内的大多数 I2P 站点都无法访问？ {#down}

我们使用的 Tanuki Java 服务包装器会打开这个端口——绑定到 localhost——以便与 JVM 内运行的软件进行通信。当 JVM 启动时,它会获得一个密钥,以便连接到包装器。在 JVM 与包装器建立连接后,包装器会拒绝任何其他连接。

更多信息可以在 [wrapper 文档](http://wrapper.tanukisoftware.com/doc/english/prop-port.html) 中找到。

### 为什么 I2P 在 32000 端口上监听？ {#port32000}

不同浏览器的代理配置在单独的页面上，并附有截图。使用外部工具进行更高级的配置是可能的，例如浏览器插件 FoxyProxy 或代理服务器 Privoxy，但可能会在你的设置中引入泄漏风险。

### 如何配置我的浏览器？{#browserproxy}

当安装 I2P 时，会创建一个通往 I2P 内主要 IRC 服务器 Irc2P 的 tunnel（参见 [I2PTunnel 配置页面](http://localhost:7657/i2ptunnel/index.jsp)），并且会在 I2P router 启动时自动启动。要连接到它，请让您的 IRC 客户端连接到 `localhost 6668`。类似 HexChat 的客户端用户可以创建一个新的网络，服务器设置为 `localhost/6668`（如果您配置了代理服务器，记得勾选"绕过代理服务器"）。Weechat 用户可以使用以下命令添加新网络：

```
/server add irc2p localhost/6668
```
### 如何在 I2P 中连接到 IRC？{#irc}

最简单的方法是点击 router console 中的 [i2ptunnel](http://127.0.0.1:7657/i2ptunnel/) 链接并创建一个新的"服务器隧道"。您可以通过将 tunnel 目标设置为现有 Web 服务器的端口(如 Tomcat 或 Jetty)来提供动态内容。您也可以提供静态内容。为此,将 tunnel 目标设置为:`0.0.0.0 port 7659` 并将内容放置在 `~/.i2p/eepsite/docroot/` 目录中。(在非 Linux 系统上,该目录可能位于不同位置。请查看 router console。)eepsite 软件作为 I2P 安装包的一部分提供,并设置为在 I2P 启动时自动启动。创建的默认站点可以通过 http://127.0.0.1:7658 访问。然而,您的 eepsite 也可以通过您的 eepsite 密钥文件被其他人访问,该文件位于:`~/.i2p/eepsite/i2p/eepsite.keys`。要了解更多信息,请阅读位于 `~/.i2p/eepsite/README.txt` 的自述文件。

### 如何搭建我自己的 I2P 站点？ {#myI2P-Site}

这取决于你的对手和威胁模型。如果你只是担心企业的"隐私"侵犯、典型的犯罪活动和审查制度,那么这并不算真正危险。如果执法部门真的想找到你,他们可能还是会找到的。只有在你运行普通(互联网)家庭用户浏览器时才托管,这会让人很难知道是谁在托管那部分内容。请将托管你的I2P站点视为托管任何其他服务——它的危险程度或安全程度取决于你自己如何配置和管理。

注意：已经有一种方法可以将托管 i2p 服务（destination）与 i2p router 分离。如果您[理解其工作原理](/docs/overview/tech-intro#i2pservices)，那么您只需将一台单独的机器设置为网站（或服务）的服务器，该服务器将可公开访问，并通过一个[非常]安全的 SSH 隧道将其转发到网络服务器，或者使用一个安全的共享文件系统。

### 如果我在家里通过 I2P 托管一个仅包含 HTML 和 CSS 的网站，这危险吗？ {#hosting}

I2P 地址簿应用程序将人类可读的名称映射到长期目标地址(destinations),这些地址与服务相关联,使其更像是一个 hosts 文件或联系人列表,而不是网络数据库或 DNS 服务。它也是本地优先的——没有公认的全局命名空间,你可以决定任何给定的 .i2p 域名最终映射到什么地址。折中方案是一种称为"Jump Service"(跳转服务)的东西,它通过将你重定向到一个页面来提供人类可读的名称,在该页面上你会被询问"你是否授权 I2P router 将 $SITE_CRYPTO_KEY 称为 $SITE_NAME.i2p"之类的内容。一旦它被添加到你的地址簿中,你就可以生成自己的跳转 URL 来帮助与他人分享该站点。

### I2P 如何找到 ".i2p" 网站？ {#addresses}

如果不知道您想要访问的站点的 base32 或 base64 地址，就无法添加地址。人类可读的"主机名"只是加密地址的别名，该加密地址对应于 base32 或 base64。没有加密地址，就无法访问 I2P 站点，这是设计使然。向尚不知道该地址的人分发地址通常是 Jump 服务提供商的责任。访问未知的 I2P 站点将触发使用 Jump 服务。stats.i2p 是最可靠的 Jump 服务。

如果您通过 i2ptunnel 托管一个站点,那么它还没有在跳转服务中注册。要在本地为其设置一个 URL,请访问配置页面并点击"添加到本地地址簿"按钮。然后访问 http://127.0.0.1:7657/dns 查找 addresshelper URL 并分享它。

### 如何向地址簿添加地址？ {#addressbook}

I2P 使用的端口可以分为两个部分:

1. 面向互联网的端口,用于与其他 I2P router 通信
2. 本地端口,用于本地连接

下面将详细介绍这些内容。

#### 1. Internet-facing ports

注意：从 0.7.8 版本开始，新安装不再使用端口 8887；程序首次运行时会在 9000 到 31000 之间随机选择一个端口。所选端口会显示在 router [配置页面](http://127.0.0.1:7657/confignet)上。

**出站**

- 从[配置页面](http://127.0.0.1:7657/confignet)上列出的随机端口发出的 UDP 流量到任意远程 UDP 端口,允许回复
- 从随机高端口发出的 TCP 流量到任意远程 TCP 端口
- 端口 123 上的出站 UDP 流量,允许回复。这对于 I2P 的内部时间同步是必需的(通过 SNTP - 查询 pool.ntp.org 中的随机 SNTP 主机或您指定的其他服务器)

**入站**

- (可选,推荐) 从任意位置到 [配置页面](http://127.0.0.1:7657/confignet) 上标注端口的 UDP 连接
- (可选,推荐) 从任意位置到 [配置页面](http://127.0.0.1:7657/confignet) 上标注端口的 TCP 连接
- 入站 TCP 可以在 [配置页面](http://127.0.0.1:7657/confignet) 上禁用

#### 2. Local I2P ports

默认情况下，本地 I2P 端口仅监听本地连接，除非另有说明：

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
### I2P 使用哪些端口？ {#ports}

地址簿位于 [http://localhost:7657/dns](http://localhost:7657/dns)，在那里可以找到更多信息。

**有哪些好的地址簿订阅链接？**

您可以尝试以下方法：

- [http://stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
- [http://identiguy.i2p/hosts.txt](http://identiguy.i2p/hosts.txt)

### How can I access the web console from my other machines or password protect it? {#remote_webconsole}

出于安全考虑,router 的管理控制台默认只监听本地接口的连接。

有两种方法可以远程访问控制台：

1. SSH 隧道
2. 配置您的控制台使其在公共 IP 地址上可用并设置用户名和密码

详细说明如下：

**方法 1：SSH 隧道**

如果您运行的是类Unix操作系统,这是远程访问I2P控制台最简单的方法。(注意:运行Windows系统也可以使用SSH服务器软件,例如 [https://github.com/PowerShell/Win32-OpenSSH](https://github.com/PowerShell/Win32-OpenSSH))

配置好系统的 SSH 访问后，使用 '-L' 标志并传递适当的参数给 SSH - 例如：

```
ssh -L 7657:localhost:7657 (System_IP)
```
其中 '(System_IP)' 替换为您系统的 IP 地址。此命令将端口 7657(第一个冒号前的数字)转发到远程系统(由第一个和第二个冒号之间的字符串 'localhost' 指定)的端口 7657(第二个冒号后的数字)。您的远程 I2P 控制台现在将在本地系统上以 'http://localhost:7657' 的形式可用,并且只要您的 SSH 会话处于活动状态就会保持可用。

如果您想启动一个 SSH 会话而不在远程系统上启动 shell，可以添加 '-N' 标志：

```
ssh -NL 7657:localhost:7657 (System_IP)
```
**方法2：配置你的控制台在公共IP地址上可用，并设置用户名和密码**

1. 打开 `~/.i2p/clients.config` 并替换：
   ```
   clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
   ```
   为：
   ```
   clientApp.0.args=7657 ::1,127.0.0.1,(System_IP) ./webapps/
   ```
   其中将 (System_IP) 替换为你系统的公网 IP 地址

2. 访问 [http://localhost:7657/configui](http://localhost:7657/configui),如需要可以添加控制台用户名和密码 - 强烈建议添加用户名和密码来保护您的 I2P 控制台免受篡改,这可能导致去匿名化。

3. 访问 [http://localhost:7657/index](http://localhost:7657/index) 并点击 "Graceful restart"，这将重启 JVM 并重新加载客户端应用程序

启动后,您现在应该能够远程访问控制台了。在浏览器中访问 `http://(System_IP):7657` 加载 router console,如果您的浏览器支持身份验证弹窗,系统将提示您输入在上述第2步中指定的用户名和密码。

注意:您可以在上述配置中指定 0.0.0.0。这指定的是一个接口,而不是网络或子网掩码。0.0.0.0 表示"绑定到所有接口",因此它可以在 127.0.0.1:7657 以及任何局域网/广域网 IP 上访问。使用此选项时请小心,因为控制台将在系统上配置的所有地址上可用。

### How can I use applications from my other machines? {#remote_i2cp}

请参阅上一个答案中关于使用 SSH 端口转发的说明，也可以查看控制台中的此页面：[http://localhost:7657/configi2cp](http://localhost:7657/configi2cp)

### 我的地址簿中缺少很多主机。有哪些好的订阅链接？{#subscriptions}

SOCKS 代理自 0.7.1 版本起开始可用。支持 SOCKS 4/4a/5 协议。I2P 没有 SOCKS outproxy，因此仅限于在 I2P 内部使用。

许多应用程序会泄露可能在互联网上识别您身份的敏感信息，这是使用 I2P SOCKS 代理时应该注意的风险。I2P 仅过滤连接数据，但如果您打算运行的程序将这些信息作为内容发送，I2P 就无法保护您的匿名性。例如，一些邮件应用程序会将其运行的机器的 IP 地址发送到邮件服务器。我们推荐使用 I2P 专用工具或应用程序（例如用于种子下载的 [I2PSnark](http://localhost:7657/i2psnark/)），或者已知可以安全与 I2P 配合使用的应用程序，包括 [Firefox](https://www.mozilla.org/) 上的流行插件。

### 如何从其他机器访问 Web 控制台或为其设置密码保护？ {#remote_webconsole}

有一些称为 Outproxy 的服务在 I2P 和互联网之间架起桥梁,类似于 Tor 出口节点。HTTP 和 HTTPS 的默认 outproxy 功能由 `exit.stormycloud.i2p` 提供,由 StormyCloud Inc. 运营。它在 HTTP 代理中配置。此外,为了帮助保护匿名性,I2P 默认不允许您与常规互联网建立匿名连接。请参阅 [Socks Outproxy](/docs/api/socks#outproxy) 页面了解更多信息。

---

## Reseeds

### 如何在其他机器上使用应用程序？ {#remote_i2cp}

首先检查 Router Console（路由器控制台）中的 [http://127.0.0.1:7657/netdb](http://127.0.0.1:7657/netdb) 页面 – 您的网络数据库。如果您在 I2P 内看不到列出的任何 router，但控制台显示您应该被防火墙阻挡，那么您可能无法连接到 reseed 服务器。如果您确实看到列出了其他 I2P router，那么请尝试在 [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config) 中降低最大连接数，也许您的 router 无法处理过多连接。

### 是否可以将 I2P 用作 SOCKS 代理？{#socks}

在正常情况下，I2P 会使用我们的引导链接自动将您连接到网络。如果互联网中断导致从重新种子服务器引导失败，一个简单的引导方法是使用 Tor 浏览器(默认情况下它打开 localhost)，它与 [http://127.0.0.1:7657/configreseed](http://127.0.0.1:7657/configreseed) 配合得非常好。也可以手动为 I2P router 重新播种。

当使用 Tor 浏览器进行 reseed 时,您可以一次选择多个 URL 并继续操作。虽然默认值为 2(从多个 URL 中选择)也可以工作,但速度会比较慢。

---

## Privacy-Safety

### 如何访问常规互联网上的 IRC、BitTorrent 或其他服务？{#proxy_other}

不会，你的 router 参与在 i2p 网络中传输端到端加密流量到一个随机的 tunnel 端点，通常不是 outproxy，并且没有流量会通过传输层在你的 router 和互联网之间传递。作为最终用户，如果你不熟练系统和网络管理，就不应该运行 outproxy。

### Is it easy to detect the use of I2P by analyzing network traffic? {#detection}

I2P 流量通常看起来像 UDP 流量,仅此而已——让它看起来不那么显眼正是我们的目标。它也支持 TCP。通过一些努力,被动流量分析可能能够将流量归类为"I2P",但我们希望通过持续开发流量混淆技术来进一步降低这种可能性。即使是像 obfs4 这样相对简单的协议混淆层也能防止审查者封锁 I2P(这是 I2P 部署的一个目标)。

### 我的 router 已经运行了几分钟，但连接数为零或非常少 {#reseed}

这取决于你的个人威胁模型。对于大多数人来说，I2P 比不使用任何保护要安全得多。某些其他网络（如 Tor、mixminion/mixmaster）在面对某些对手时可能更安全。例如，I2P 流量不使用 TLS/SSL，因此不存在 Tor 所面临的"最薄弱环节"问题。在"阿拉伯之春"期间，叙利亚有很多人使用 I2P，最近该项目在中东和近东地区的较小语言安装版本中出现了更大的增长。这里最重要的是要注意 I2P 是一种技术，你需要操作指南来增强你在互联网上的隐私/匿名性。同时检查你的浏览器或导入指纹搜索引擎，使用非常大的（意味着：典型的长尾/非常精确的多样化数据结构）关于大量环境信息的数据集来阻止指纹攻击，并且不要使用 VPN 以减少其自身带来的所有风险，如自身的 TLS 缓存行为以及提供商业务的技术架构，这些可能比自己的桌面系统更容易被攻击。可以考虑使用具有出色反指纹保护的隔离 Tor V-Browser，配合只允许必要系统通信的全面应用程序保护，最后使用带有反间谍禁用脚本和 Live CD 的虚拟机来消除任何"几乎永久的可能风险"，通过降低概率来减少所有风险，这在公共网络和高度个人化风险模型中可能是一个好选择，也可能是为 I2P 使用实现此目标的最佳方案。

### 如何手动重新播种？{#manual_reseed}

是的,对于知道你的 router 的其他 I2P 节点来说是这样的。我们使用这些信息与 I2P 网络的其余部分建立连接。这些地址实际位于"routerInfo(键值对)对象"中,可以是远程获取的,也可以是从对等节点接收的。routerInfo 包含一些信息(有些是可选的机会性添加的),"由对等节点发布",关于 router 本身的引导信息。此对象中不包含客户端的数据。深入了解底层机制会发现,每个节点都使用最新的 ID 创建类型进行计数,称为"SHA-256 哈希(低位=正哈希(-键),高位=负哈希(+键))"。I2P 网络拥有自己的 routerInfo 数据库,在上传和索引期间创建,但这深度依赖于键值表的实现、网络拓扑、负载状态/带宽状态以及数据库组件中存储的路由概率。

### Is using an outproxy safe? {#proxy_safe}

这取决于你对"安全"的定义。Outproxy在工作时很好用,但不幸的是它们是由志愿者运行的,这些人可能会失去兴趣或可能没有资源全天候维护它们——请注意,你可能会遇到服务不可用、中断或不可靠的时间段,我们与此服务无关,也无法对其施加影响。

outproxy 本身可以看到你的流量进出，除了端到端加密的 HTTPS/SSL 数据，就像你的 ISP 可以看到你的流量从你的计算机进出一样。如果你信任你的 ISP，那么使用 outproxy 也不会更糟。

### 我的 router 是通往常规互联网的"出口节点"(outproxy)吗?我不希望它成为出口节点。 {#exit}

如需详细了解，请阅读我们关于[威胁模型](/docs/overview/threat-model)的文章。一般来说，去匿名化并非易事，但如果您不够谨慎，仍有可能发生。

---

## Internet Access/Performance

### 通过分析网络流量来检测 I2P 的使用是否容易？{#detection}

代理访问互联网站点（即连接到互联网的 eepsite）是由非屏蔽提供商作为服务提供给 I2P 用户的。这项服务并非 I2P 开发的主要重点，而是在自愿的基础上提供的。托管在 I2P 上的 eepsite 应始终能够在没有出口代理的情况下正常工作。出口代理是一种便利功能，但按设计它们并不完美，也不是项目的主要组成部分。请注意，它们可能无法提供 I2P 其他服务所能提供的高质量服务。

### 使用 I2P 安全吗？ {#safe}

默认的 HTTP 代理仅支持 HTTP 和 HTTPS 出站代理。

### 我在路由器控制台中看到了所有其他 I2P 节点的 IP 地址。这是否意味着我的 IP 地址也会被其他人看到？{#netdb_ip}

首先，确保你已经安装了所有 I2P 相关组件的最新版本——旧版本的代码中存在不必要的 CPU 消耗部分。还有一个[性能日志](/about/performance)记录了 I2P 性能随时间改进的一些情况。

### 使用出口代理安全吗？{#proxy_safe}

I2P 网络的整体稳定性是一个持续研究的领域。其中相当一部分研究集中在配置设置的微小变化如何改变 router 的行为。由于 I2P 是一个点对点网络,其他对等节点的行为会对你的 router 性能产生影响。

### 关于"去匿名化"攻击呢？ {#deanon}

I2P 具有不同的保护机制，可以增加额外的路由和加密层。它还会通过其他节点（Tunnels）转发流量，这些节点各自的速度和质量不同，有的慢，有的快。这导致了大量的开销，并且不同方向上的流量速度各异。按照设计，所有这些因素会使其相比互联网上的直接连接更慢，但匿名性更强，而且对于大多数用途来说仍然足够快。

下面是一个示例，并附带解释，以帮助理解在使用 I2P 时延迟和带宽方面的考虑因素。

考虑下面的图表。它描述了一个客户端通过 I2P 发起请求、服务器通过 I2P 接收请求然后同样通过 I2P 响应的连接过程。图中还展示了请求传输所经过的电路。

从图表中可以看出,标记为 'P'、'Q' 和 'R' 的方框代表 'A' 的出站 tunnel,标记为 'X'、'Y' 和 'Z' 的方框代表 'B' 的出站 tunnel。同样,标记为 'X'、'Y' 和 'Z' 的方框代表 'B' 的入站 tunnel,而标记为 'P_1'、'Q_1' 和 'R_1' 的方框代表 'A' 的入站 tunnel。方框之间的箭头表示流量的方向。箭头上方和下方的文字详细说明了一对跳点之间的示例带宽以及示例延迟。

当客户端和服务器端都使用3跳tunnel时,总共涉及12个其他I2P router来中继流量。6个节点将流量从客户端中继到服务器,这些流量被分成从'A'出发的3跳出站tunnel('P'、'Q'、'R')和到达'B'的3跳入站tunnel('X'、'Y'、'Z')。同样地,另外6个节点将流量从服务器中继回客户端。

首先，我们可以考虑延迟——客户端的请求穿越 I2P 网络、到达服务器并返回客户端所需的时间。将所有延迟相加，我们可以看到：

```
    40 + 100 + 20 + 60 + 80 + 10 + 30 ms        (client to server)
  + 60 + 40 + 80 + 60 + 100 + 20 + 40 ms        (server to client)
  -----------------------------------
  TOTAL:                          740 ms
```
在我们的示例中,总往返时间加起来为 740 毫秒——这无疑比浏览常规互联网网站时通常看到的时间要高得多。

其次，我们可以考虑可用带宽。这取决于客户端和服务器之间各跳点的最慢链路，以及服务器向客户端传输流量时的情况。对于从客户端到服务器的流量，我们在示例中看到跳点 'R' 和 'X' 之间以及跳点 'X' 和 'Y' 之间的可用带宽为 32 KB/s。尽管其他跳点之间有更高的可用带宽，但这些跳点将成为瓶颈，并将从 'A' 到 'B' 的流量的最大可用带宽限制在 32 KB/s。同样，追踪从服务器到客户端的路径显示最大带宽为 64 KB/s - 在跳点 'Z_1' 和 'Y_1' 之间、'Y_1' 和 'X_1' 之间以及 'Q_1' 和 'P_1' 之间。

我们建议增加您的带宽限制。这有助于网络增加可用带宽量,从而改善您的 I2P 使用体验。带宽设置位于 [http://localhost:7657/config](http://localhost:7657/config) 页面。请注意您的互联网服务提供商(ISP)所规定的连接限制,并相应调整您的设置。

我们还建议设置足够的共享带宽 - 这允许参与隧道(participating tunnels)通过您的 I2P router 进行路由。允许参与流量可以使您的 router 更好地融入网络,并提高您的传输速度。

I2P 是一个持续开发中的项目。许多改进和修复正在实施，通常来说，运行最新版本将有助于提升性能。如果您还没有安装，请安装最新版本。

### I think I found a bug, where can I report it? {#bug}

您可以在我们的问题追踪系统上报告遇到的任何漏洞/问题,该系统可通过公开互联网和I2P访问。我们也有一个讨论论坛,同样可在I2P和公开互联网上访问。您还可以加入我们的IRC频道:通过我们的IRC网络IRC2P,或者在Freenode上。

- **我们的 Bugtracker（问题追踪系统）：**
  - 非私有互联网：[https://i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)
  - 在 I2P 上：[http://git.idk.i2p/I2P_Developers/i2p.i2p/issues](http://git.idk.i2p/I2P_Developers/i2p.i2p/issues)
- **我们的论坛：**[i2pforum.i2p](http://i2pforum.i2p/)
- **粘贴日志：**您可以将任何有趣的日志粘贴到粘贴服务，例如 [PrivateBin Wiki](https://github.com/PrivateBin/PrivateBin/wiki/PrivateBin-Directory) 上列出的非私有互联网服务，或 I2P 粘贴服务，例如这个 [PrivateBin 实例](http://paste.crypthost.i2p)或这个[无 Javascript 粘贴服务](http://pasta-nojs.i2p)，然后在 IRC 的 #i2p 频道跟进
- **IRC：**加入 #i2p-dev 在 IRC 上与开发者讨论

请包含来自 router 日志页面的相关信息,该页面位于:[http://127.0.0.1:7657/logs](http://127.0.0.1:7657/logs)。我们请求您分享"I2P Version and Running Environment"部分下的所有文本,以及页面上显示的各种日志中的任何错误或警告信息。

---

### 我无法通过 I2P 访问常规的互联网网站。 {#outproxy}

太好了！在 IRC 上找到我们：

- 在 `irc.freenode.net` 频道 `#i2p`
- 在 `IRC2P` 频道 `#i2p`

或发布到[论坛](http://i2pforum.i2p/)，我们会将其发布在这里（希望能附上答案）。
