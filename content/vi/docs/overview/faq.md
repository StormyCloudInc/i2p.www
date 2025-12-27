---
title: "Các Câu Hỏi Thường Gặp"
description: "Câu hỏi thường gặp toàn diện về I2P: trợ giúp router, cấu hình, reseed, quyền riêng tư/an toàn, hiệu suất và khắc phục sự cố"
slug: "faq"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: tài liệu
---

## Trợ giúp I2P Router

### What systems will I2P run on? {#systems}

I2P được viết bằng ngôn ngữ lập trình Java. Nó đã được kiểm tra trên Windows, Linux, FreeBSD và OSX. Phiên bản Android cũng có sẵn.

Về mức sử dụng bộ nhớ, I2P được cấu hình sử dụng 128 MB RAM theo mặc định. Điều này đủ cho việc duyệt web và sử dụng IRC. Tuy nhiên, các hoạt động khác có thể yêu cầu phân bổ bộ nhớ lớn hơn. Ví dụ, nếu muốn chạy một router băng thông cao, tham gia vào I2P torrent hoặc phục vụ các dịch vụ ẩn có lưu lượng truy cập cao, thì cần một lượng bộ nhớ lớn hơn.

Về mức sử dụng CPU, I2P đã được thử nghiệm chạy trên các hệ thống khiêm tốn như dòng máy tính đơn board Raspberry Pi. Do I2P sử dụng nhiều các kỹ thuật mật mã, CPU mạnh hơn sẽ phù hợp hơn để xử lý khối lượng công việc do I2P tạo ra cũng như các tác vụ liên quan đến phần còn lại của hệ thống (ví dụ: Hệ điều hành, GUI, Các tiến trình khác như Duyệt Web).

Khuyến nghị sử dụng Sun/Oracle Java hoặc OpenJDK.

### I2P sẽ chạy trên những hệ thống nào? {#systems}

Có, Java là cần thiết để sử dụng I2P Core. Chúng tôi đã tích hợp Java vào trong các bộ cài đặt dễ dàng cho Windows, Mac OSX và Linux. Nếu bạn đang chạy ứng dụng I2P Android, trong hầu hết các trường hợp bạn cũng sẽ cần một môi trường chạy Java như Dalvik hoặc ART được cài đặt.

### Có cần cài đặt Java để sử dụng I2P không? {#java}

Một I2P Site là một trang web bình thường ngoại trừ việc nó được lưu trữ bên trong I2P. Các I2P site có địa chỉ trông giống như địa chỉ internet thông thường, kết thúc bằng ".i2p" theo cách dễ đọc cho con người, không mã hóa, vì lợi ích của mọi người. Thực tế việc kết nối đến một I2P Site yêu cầu mật mã học, có nghĩa là địa chỉ I2P Site cũng là các Destination "Base64" dài và các địa chỉ "B32" ngắn hơn. Bạn có thể cần thực hiện cấu hình bổ sung để duyệt web đúng cách. Duyệt các I2P Site sẽ yêu cầu kích hoạt HTTP Proxy trong cài đặt I2P của bạn và sau đó cấu hình trình duyệt của bạn để sử dụng nó. Để biết thêm thông tin, hãy xem phần "Browsers" bên dưới hoặc hướng dẫn "Browser Configuration".

### "I2P Site" là gì và làm thế nào để cấu hình trình duyệt của tôi để có thể sử dụng chúng? {#I2P-Site}

Trong trang Peers (Các nút mạng) trên bảng điều khiển router của bạn, bạn có thể thấy hai con số - Active x/y. Con số thứ nhất là số lượng peers mà bạn đã gửi hoặc nhận tin nhắn trong vài phút gần đây. Con số thứ hai là số lượng peers được thấy gần đây, con số này sẽ luôn lớn hơn hoặc bằng con số thứ nhất.

### Các số Active x/y trong bảng điều khiển router có nghĩa là gì? {#active}

Có, điều này có thể bình thường, đặc biệt khi router mới được khởi động. Các router mới sẽ cần thời gian để khởi động và kết nối với phần còn lại của mạng. Để giúp cải thiện sự tích hợp mạng, thời gian hoạt động và hiệu suất, hãy xem xét các cài đặt sau:

- **Chia sẻ băng thông** - Nếu một router được cấu hình để chia sẻ băng thông, nó sẽ định tuyến nhiều lưu lượng hơn cho các router khác, điều này giúp tích hợp nó với phần còn lại của mạng, cũng như cải thiện hiệu suất kết nối cục bộ của bạn. Điều này có thể được cấu hình trên trang [http://localhost:7657/config](http://localhost:7657/config).
- **Giao diện mạng** - Đảm bảo rằng không có giao diện nào được chỉ định trên trang [http://localhost:7657/confignet](http://localhost:7657/confignet). Điều này có thể làm giảm hiệu suất trừ khi máy tính của bạn có nhiều địa chỉ IP bên ngoài (multi-homed).
- **Giao thức I2NP** - Đảm bảo rằng router được cấu hình để mong đợi các kết nối trên một giao thức hợp lệ cho hệ điều hành của máy chủ và các cài đặt mạng(Nâng cao) trống. Không nhập địa chỉ IP vào trường 'Hostname' trong trang cấu hình Mạng. Giao thức I2NP bạn chọn ở đây sẽ chỉ được sử dụng nếu bạn chưa có địa chỉ có thể truy cập được. Ví dụ, hầu hết các kết nối không dây 4G và 5G của Verizon tại Hoa Kỳ chặn UDP và không thể truy cập qua nó. Những người khác sẽ buộc phải sử dụng UDP ngay cả khi nó có sẵn cho họ. Hãy chọn cài đặt hợp lý từ danh sách các Giao thức I2NP được liệt kê.

### Router của tôi có rất ít peer hoạt động, như vậy có sao không? {#peers}

Không có nội dung nào như vậy được cài đặt mặc định. Tuy nhiên, vì I2P là mạng ngang hàng (peer-to-peer), có khả năng bạn có thể vô tình gặp phải nội dung bị cấm. Dưới đây là tóm tắt về cách I2P ngăn chặn bạn khỏi bị liên quan không cần thiết đến các vi phạm niềm tin của bạn.

- **Phân phối** - Lưu lượng truy cập là nội bộ trong mạng I2P, bạn không phải là [exit node](#exit) (được gọi là outproxy trong tài liệu của chúng tôi).
- **Lưu trữ** - Mạng I2P không thực hiện lưu trữ phân tán nội dung, điều này phải được người dùng cài đặt và cấu hình cụ thể (ví dụ với Tahoe-LAFS). Đó là tính năng của một mạng ẩn danh khác, [Freenet](http://freenetproject.org/). Bằng cách chạy router I2P, bạn không lưu trữ nội dung cho bất kỳ ai.
- **Truy cập** - Router của bạn sẽ không yêu cầu bất kỳ nội dung nào nếu không có chỉ thị cụ thể từ bạn.

### Tôi phản đối một số loại nội dung nhất định. Làm thế nào để tôi tránh phân phối, lưu trữ hoặc truy cập chúng? {#badcontent}

Có, cách dễ nhất và phổ biến nhất là chặn các máy chủ bootstrap, hay "Reseed". Chặn hoàn toàn tất cả lưu lượng được làm rối cũng có hiệu quả (mặc dù điều này sẽ phá vỡ rất nhiều thứ khác không phải I2P và hầu hết không muốn đi xa đến vậy). Trong trường hợp chặn reseed, có một gói reseed trên Github, việc chặn nó cũng sẽ chặn Github. Bạn có thể reseed qua proxy (có thể tìm thấy nhiều trên Internet nếu bạn không muốn dùng Tor) hoặc chia sẻ các gói reseed trực tiếp với bạn bè theo cách ngoại tuyến.

### Có thể chặn I2P không? {#blocking}

Thường thì lỗi này sẽ xảy ra với bất kỳ phần mềm Java có kích hoạt mạng nào trên một số hệ thống được cấu hình để sử dụng IPv6 theo mặc định. Có một vài cách để giải quyết vấn đề này:

- Trên các hệ thống dựa trên Linux, bạn có thể `echo 0 > /proc/sys/net/ipv6/bindv6only`
- Tìm các dòng sau trong `wrapper.config`:
  ```
  #wrapper.java.additional.5=-Djava.net.preferIPv4Stack=true
  #wrapper.java.additional.6=-Djava.net.preferIPv6Addresses=false
  ```
  Nếu các dòng này có mặt, hãy bỏ comment bằng cách xóa dấu "#". Nếu các dòng không có, hãy thêm chúng vào mà không có dấu "#".

Một tùy chọn khác là xóa `::1` khỏi `~/.i2p/clients.config`

**CẢNH BÁO**: Để bất kỳ thay đổi nào đối với `wrapper.config` có hiệu lực, bạn phải dừng hoàn toàn router và wrapper. Việc nhấp vào *Khởi động lại* trên bảng điều khiển router của bạn sẽ KHÔNG đọc lại tệp này! Bạn phải nhấp vào *Tắt máy*, đợi 11 phút, sau đó khởi động I2P.

### Trong `wrapper.log` tôi thấy lỗi hiển thị "`Protocol family unavailable`" khi tải Router Console {#protocolfamily}

Nếu bạn xem xét tất cả các I2P Site từng được tạo ra, đúng vậy, hầu hết chúng đã ngừng hoạt động. Con người và I2P Site đến rồi đi. Một cách tốt để bắt đầu với I2P là xem danh sách các I2P Site hiện đang hoạt động. [identiguy.i2p](http://identiguy.i2p) theo dõi các I2P Site đang hoạt động.

### Hầu hết các I2P Sites trong I2P đều không hoạt động? {#down}

Tanuki java service wrapper mà chúng tôi sử dụng mở cổng này — gắn với localhost — để giao tiếp với phần mềm đang chạy bên trong JVM. Khi JVM được khởi chạy, nó được cung cấp một key để có thể kết nối với wrapper. Sau khi JVM thiết lập kết nối với wrapper, wrapper sẽ từ chối mọi kết nối bổ sung.

Thông tin chi tiết có thể tìm thấy trong [tài liệu wrapper](http://wrapper.tanukisoftware.com/doc/english/prop-port.html).

### Tại sao I2P lại lắng nghe trên cổng 32000? {#port32000}

Cấu hình proxy cho các trình duyệt khác nhau nằm trên một trang riêng có kèm ảnh chụp màn hình. Các cấu hình nâng cao hơn với các công cụ bên ngoài, chẳng hạn như plug-in trình duyệt FoxyProxy hoặc máy chủ proxy Privoxy, là có thể nhưng có thể gây ra rò rỉ thông tin trong thiết lập của bạn.

### Làm thế nào để cấu hình trình duyệt của tôi? {#browserproxy}

Một tunnel tới máy chủ IRC chính trong I2P, Irc2P, được tạo khi cài đặt I2P (xem [trang cấu hình I2PTunnel](http://localhost:7657/i2ptunnel/index.jsp)), và tự động khởi động khi I2P router khởi động. Để kết nối tới nó, hãy cấu hình IRC client của bạn kết nối tới `localhost 6668`. Người dùng client giống HexChat có thể tạo một mạng mới với máy chủ `localhost/6668` (nhớ đánh dấu "Bypass proxy server" nếu bạn đã cấu hình proxy server). Người dùng Weechat có thể sử dụng lệnh sau để thêm một mạng mới:

```
/server add irc2p localhost/6668
```
### Làm thế nào để kết nối IRC trong I2P? {#irc}

Phương pháp dễ nhất là nhấp vào liên kết [i2ptunnel](http://127.0.0.1:7657/i2ptunnel/) trong bảng điều khiển router và tạo một 'Server Tunnel' mới. Bạn có thể phục vụ nội dung động bằng cách đặt đích đến của tunnel tới cổng của một máy chủ web hiện có, chẳng hạn như Tomcat hoặc Jetty. Bạn cũng có thể phục vụ nội dung tĩnh. Để làm điều này, đặt đích đến của tunnel thành: `0.0.0.0 port 7659` và đặt nội dung vào thư mục `~/.i2p/eepsite/docroot/`. (Trên các hệ thống không phải Linux, vị trí này có thể khác. Hãy kiểm tra bảng điều khiển router.) Phần mềm 'eepsite' đi kèm trong gói cài đặt I2P và được thiết lập để tự động khởi động khi I2P được khởi động. Trang web mặc định được tạo ra có thể truy cập tại http://127.0.0.1:7658. Tuy nhiên, 'eepsite' của bạn cũng có thể được người khác truy cập thông qua tệp khóa eepsite của bạn, nằm tại: `~/.i2p/eepsite/i2p/eepsite.keys`. Để tìm hiểu thêm, hãy đọc tệp readme tại: `~/.i2p/eepsite/README.txt`.

### Làm thế nào để tôi thiết lập I2P Site của riêng mình? {#myI2P-Site}

Điều này phụ thuộc vào đối thủ của bạn và mô hình đe dọa của bạn. Nếu bạn chỉ lo lắng về các vi phạm "quyền riêng tư" của doanh nghiệp, tội phạm thông thường và kiểm duyệt, thì nó không thực sự nguy hiểm. Cơ quan thực thi pháp luật có thể sẽ tìm thấy bạn nếu họ thực sự muốn. Chỉ host khi bạn có trình duyệt người dùng gia đình bình thường (internet) đang chạy sẽ khiến việc biết ai đang host phần đó trở nên thực sự khó khăn. Vui lòng cân nhắc việc host trang I2P của bạn giống như host bất kỳ dịch vụ nào khác - nó nguy hiểm - hoặc an toàn - tùy thuộc vào cách bạn cấu hình và quản lý nó.

Lưu ý: Đã có cách để tách biệt việc lưu trữ một dịch vụ i2p (destination) khỏi i2p router. Nếu bạn [hiểu cách thức](/docs/overview/tech-intro#i2pservices) hoạt động của nó, thì bạn chỉ cần thiết lập một máy riêng biệt làm máy chủ cho trang web (hoặc dịch vụ) sẽ được truy cập công khai và chuyển tiếp đến máy chủ web qua một SSH tunnel [rất] an toàn hoặc sử dụng một hệ thống tệp được chia sẻ, bảo mật.

### Nếu tôi host một trang web trên I2P tại nhà, chỉ chứa HTML và CSS, liệu có nguy hiểm không? {#hosting}

Ứng dụng Sổ địa chỉ I2P ánh xạ các tên dễ đọc với người dùng đến các đích đến dài hạn, được liên kết với các dịch vụ, khiến nó giống một tệp hosts hoặc danh sách liên hệ hơn là một cơ sở dữ liệu mạng hay dịch vụ DNS. Nó cũng ưu tiên cục bộ - không có không gian tên toàn cầu được công nhận, bạn tự quyết định bất kỳ tên miền .i2p nào sẽ ánh xạ đến đâu. Giải pháp trung gian là thứ gọi là "Jump Service" (Dịch vụ nhảy) cung cấp một tên dễ đọc bằng cách chuyển hướng bạn đến một trang nơi bạn sẽ được hỏi "Bạn có cho phép I2P router gọi $SITE_CRYPTO_KEY bằng tên $SITE_NAME.i2p không" hoặc tương tự như vậy. Khi nó đã có trong sổ địa chỉ của bạn, bạn có thể tạo các jump URL của riêng mình để giúp chia sẻ trang web với người khác.

### I2P tìm các trang web ".i2p" như thế nào? {#addresses}

Bạn không thể thêm một địa chỉ mà không biết ít nhất là base32 hoặc base64 của trang web bạn muốn truy cập. "Hostname" mà con người có thể đọc được chỉ là một bí danh cho địa chỉ mật mã, tương ứng với base32 hoặc base64. Không có địa chỉ mật mã, sẽ không có cách nào để truy cập một I2P Site, điều này được thiết kế như vậy. Việc phân phối địa chỉ cho những người chưa biết đến nó thường là trách nhiệm của nhà cung cấp dịch vụ Jump. Truy cập một I2P Site chưa được biết đến sẽ kích hoạt việc sử dụng dịch vụ Jump. stats.i2p là dịch vụ Jump đáng tin cậy nhất.

Nếu bạn đang lưu trữ một trang web qua i2ptunnel, thì nó chưa có đăng ký với dịch vụ jump. Để cấp cho nó một URL cục bộ, hãy truy cập trang cấu hình và nhấp vào nút có nội dung "Add to Local Address Book." Sau đó truy cập http://127.0.0.1:7657/dns để tra cứu URL addresshelper và chia sẻ nó.

### Làm thế nào để thêm địa chỉ vào Sổ địa chỉ? {#addressbook}

Các cổng được sử dụng bởi I2P có thể được chia thành 2 phần:

1. Các cổng hướng Internet, được sử dụng để giao tiếp với các router I2P khác
2. Các cổng cục bộ, dùng cho các kết nối cục bộ

Những điều này được mô tả chi tiết dưới đây.

#### 1. Internet-facing ports

Lưu ý: Kể từ phiên bản 0.7.8, các cài đặt mới không sử dụng cổng 8887; một cổng ngẫu nhiên trong khoảng từ 9000 đến 31000 được chọn khi chương trình chạy lần đầu tiên. Cổng được chọn sẽ hiển thị trên [trang cấu hình](http://127.0.0.1:7657/confignet) của router.

**ĐI RA**

- UDP từ cổng ngẫu nhiên được liệt kê trên [trang cấu hình](http://127.0.0.1:7657/confignet) đến các cổng UDP từ xa tùy ý, cho phép nhận phản hồi
- TCP từ các cổng cao ngẫu nhiên đến các cổng TCP từ xa tùy ý
- UDP đисходящие trên cổng 123, cho phép nhận phản hồi. Điều này cần thiết cho đồng bộ thời gian nội bộ của I2P (thông qua SNTP - truy vấn máy chủ SNTP ngẫu nhiên trong pool.ntp.org hoặc máy chủ khác mà bạn chỉ định)

**ĐẾN**

- (Tùy chọn, khuyến nghị) UDP đến cổng được ghi chú trên [trang cấu hình](http://127.0.0.1:7657/confignet) từ các vị trí bất kỳ
- (Tùy chọn, khuyến nghị) TCP đến cổng được ghi chú trên [trang cấu hình](http://127.0.0.1:7657/confignet) từ các vị trí bất kỳ
- TCP đến có thể bị vô hiệu hóa trên [trang cấu hình](http://127.0.0.1:7657/confignet)

#### 2. Local I2P ports

Các cổng I2P cục bộ mặc định chỉ lắng nghe các kết nối cục bộ, trừ khi có ghi chú khác:

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
### I2P sử dụng những cổng nào? {#ports}

Sổ địa chỉ nằm ở [http://localhost:7657/dns](http://localhost:7657/dns) nơi có thể tìm thấy thêm thông tin.

**Một số liên kết đăng ký sổ địa chỉ tốt là gì?**

Bạn có thể thử những cách sau:

- [http://stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
- [http://identiguy.i2p/hosts.txt](http://identiguy.i2p/hosts.txt)

### How can I access the web console from my other machines or password protect it? {#remote_webconsole}

Vì mục đích bảo mật, bảng điều khiển quản trị của router theo mặc định chỉ lắng nghe các kết nối trên giao diện cục bộ.

Có hai phương pháp để truy cập console từ xa:

1. SSH Tunnel
2. Cấu hình console của bạn để có thể truy cập trên địa chỉ IP công khai với tên người dùng & mật khẩu

Các chi tiết được mô tả dưới đây:

**Phương pháp 1: SSH Tunnel**

Nếu bạn đang chạy hệ điều hành giống Unix, đây là phương pháp dễ nhất để truy cập từ xa vào console I2P của bạn. (Lưu ý: Phần mềm SSH server cũng có sẵn cho các hệ thống chạy Windows, ví dụ [https://github.com/PowerShell/Win32-OpenSSH](https://github.com/PowerShell/Win32-OpenSSH))

Sau khi bạn đã cấu hình quyền truy cập SSH vào hệ thống của mình, cờ '-L' được truyền cho SSH với các đối số thích hợp - ví dụ:

```
ssh -L 7657:localhost:7657 (System_IP)
```
trong đó '(System_IP)' được thay thế bằng địa chỉ IP của Hệ thống của bạn. Lệnh này chuyển tiếp cổng 7657 (số trước dấu hai chấm đầu tiên) đến cổng 7657 của hệ thống từ xa (được chỉ định bởi chuỗi 'localhost' giữa dấu hai chấm thứ nhất và thứ hai) (số sau dấu hai chấm thứ hai). Console I2P từ xa của bạn giờ đây sẽ có sẵn trên hệ thống cục bộ của bạn tại 'http://localhost:7657' và sẽ có sẵn miễn là phiên SSH của bạn còn hoạt động.

Nếu bạn muốn khởi động một phiên SSH mà không khởi chạy shell trên hệ thống từ xa, bạn có thể thêm cờ '-N':

```
ssh -NL 7657:localhost:7657 (System_IP)
```
**Phương pháp 2: Cấu hình console của bạn để có thể truy cập trên địa chỉ IP công khai với tên người dùng & mật khẩu**

1. Mở `~/.i2p/clients.config` và thay thế:
   ```
   clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
   ```
   bằng:
   ```
   clientApp.0.args=7657 ::1,127.0.0.1,(System_IP) ./webapps/
   ```
   trong đó bạn thay thế (System_IP) bằng địa chỉ IP công khai của hệ thống

2. Truy cập [http://localhost:7657/configui](http://localhost:7657/configui) và thêm tên người dùng cùng mật khẩu cho console nếu muốn - Việc thêm tên người dùng & mật khẩu được khuyến khích mạnh mẽ để bảo vệ I2P console của bạn khỏi bị can thiệp, điều này có thể dẫn đến mất ẩn danh.

3. Truy cập [http://localhost:7657/index](http://localhost:7657/index) và nhấn "Graceful restart", điều này sẽ khởi động lại JVM và tải lại các ứng dụng client

Sau khi khởi động xong, bạn sẽ có thể truy cập console từ xa. Mở router console tại `http://(System_IP):7657` và bạn sẽ được yêu cầu nhập tên người dùng và mật khẩu mà bạn đã chỉ định ở bước 2 ở trên nếu trình duyệt của bạn hỗ trợ popup xác thực.

LƯU Ý: Bạn có thể chỉ định 0.0.0.0 trong cấu hình trên. Điều này chỉ định một giao diện, không phải một mạng hoặc netmask. 0.0.0.0 có nghĩa là "gắn kết với tất cả các giao diện", do đó nó có thể được truy cập trên 127.0.0.1:7657 cũng như bất kỳ địa chỉ IP LAN/WAN nào. Hãy cẩn thận khi sử dụng tùy chọn này vì giao diện điều khiển sẽ có sẵn trên TẤT CẢ các địa chỉ được cấu hình trên hệ thống của bạn.

### How can I use applications from my other machines? {#remote_i2cp}

Vui lòng xem câu trả lời trước đó để biết hướng dẫn sử dụng SSH Port Forwarding, và cũng xem trang này trong console của bạn: [http://localhost:7657/configi2cp](http://localhost:7657/configi2cp)

### Tôi thiếu rất nhiều host trong sổ địa chỉ của mình. Một số liên kết đăng ký tốt là gì? {#subscriptions}

SOCKS proxy đã hoạt động từ phiên bản 0.7.1. Hỗ trợ SOCKS 4/4a/5. I2P không có SOCKS outproxy nên nó chỉ giới hạn sử dụng trong mạng I2P.

Nhiều ứng dụng làm rò rỉ thông tin nhạy cảm có thể định danh bạn trên Internet và đây là rủi ro mà người dùng cần nhận thức khi sử dụng SOCKS proxy của I2P. I2P chỉ lọc dữ liệu kết nối, nhưng nếu chương trình bạn định chạy gửi thông tin này dưới dạng nội dung, I2P không có cách nào bảo vệ tính ẩn danh của bạn. Ví dụ, một số ứng dụng email sẽ gửi địa chỉ IP của máy tính đang chạy chúng đến máy chủ thư. Chúng tôi khuyến nghị sử dụng các công cụ hoặc ứng dụng chuyên dụng cho I2P (như [I2PSnark](http://localhost:7657/i2psnark/) cho torrents), hoặc các ứng dụng được biết là an toàn khi sử dụng với I2P bao gồm các plugin phổ biến trên [Firefox](https://www.mozilla.org/).

### Làm thế nào để tôi có thể truy cập web console từ các máy khác hoặc bảo vệ nó bằng mật khẩu? {#remote_webconsole}

Có các dịch vụ được gọi là Outproxies hoạt động như cầu nối giữa I2P và Internet, tương tự như Tor Exit Nodes. Chức năng outproxy mặc định cho HTTP và HTTPS được cung cấp bởi `exit.stormycloud.i2p` và được vận hành bởi StormyCloud Inc. Nó được cấu hình trong HTTP Proxy. Ngoài ra, để giúp bảo vệ tính ẩn danh, I2P không cho phép bạn thực hiện các kết nối ẩn danh tới Internet thông thường theo mặc định. Vui lòng xem trang [Socks Outproxy](/docs/api/socks#outproxy) để biết thêm thông tin.

---

## Reseeds

### Làm thế nào để sử dụng các ứng dụng từ các máy khác? {#remote_i2cp}

Trước tiên hãy kiểm tra trang [http://127.0.0.1:7657/netdb](http://127.0.0.1:7657/netdb) trong Router Console – cơ sở dữ liệu mạng của bạn. Nếu bạn không thấy bất kỳ router nào được liệt kê từ bên trong I2P nhưng console hiển thị rằng bạn có thể đang bị tường lửa chặn, thì có thể bạn không thể kết nối đến các máy chủ reseed. Nếu bạn có thấy các router I2P khác được liệt kê thì hãy thử giảm số lượng kết nối tối đa tại [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config), có thể router của bạn không thể xử lý nhiều kết nối.

### Có thể sử dụng I2P như một SOCKS proxy không? {#socks}

Trong điều kiện bình thường, I2P sẽ tự động kết nối bạn với mạng lưới bằng cách sử dụng các liên kết bootstrap của chúng tôi. Nếu kết nối internet bị gián đoạn khiến việc bootstrap từ các reseed server thất bại, một cách dễ dàng để bootstrap là sử dụng trình duyệt Tor (Mặc định nó mở localhost), hoạt động rất tốt với [http://127.0.0.1:7657/configreseed](http://127.0.0.1:7657/configreseed). Cũng có thể thực hiện reseed một I2P router theo cách thủ công.

Khi sử dụng trình duyệt Tor để reseed, bạn có thể chọn nhiều URL cùng lúc và tiếp tục. Mặc dù giá trị mặc định là 2 (trong số nhiều url) cũng sẽ hoạt động nhưng nó sẽ chậm.

---

## Privacy-Safety

### Làm thế nào để tôi truy cập IRC, BitTorrent, hoặc các dịch vụ khác trên Internet thông thường? {#proxy_other}

Không, router của bạn chỉ tham gia vận chuyển lưu lượng được mã hóa đầu cuối (e2e) qua mạng i2p đến một điểm cuối tunnel ngẫu nhiên, thường không phải là outproxy, và không có lưu lượng nào được truyền giữa router của bạn và Internet qua tầng vận chuyển. Với vai trò người dùng cuối, bạn không nên chạy outproxy nếu bạn không có kỹ năng về quản trị hệ thống và mạng.

### Is it easy to detect the use of I2P by analyzing network traffic? {#detection}

Lưu lượng I2P thường trông giống như lưu lượng UDP, và không hơn thế nhiều – và mục tiêu là làm cho nó trông không khác biệt hơn thế. Nó cũng hỗ trợ TCP. Với một số nỗ lực, phân tích lưu lượng thụ động có thể phân loại lưu lượng này là "I2P", nhưng chúng tôi hy vọng rằng sự phát triển liên tục của kỹ thuật làm rối lưu lượng sẽ giảm thiểu điều này hơn nữa. Ngay cả một lớp làm rối giao thức khá đơn giản như obfs4 cũng sẽ ngăn chặn việc kiểm duyệt chặn I2P (đây là một mục tiêu mà I2P triển khai).

### Router của tôi đã chạy được vài phút nhưng không có hoặc có rất ít kết nối {#reseed}

Điều này phụ thuộc vào mô hình đe dọa cá nhân của bạn. Đối với hầu hết mọi người, I2P an toàn hơn nhiều so với việc không sử dụng bất kỳ biện pháp bảo vệ nào. Một số mạng khác (như Tor, mixminion/mixmaster), có thể an toàn hơn trước những đối thủ nhất định. Ví dụ, lưu lượng I2P không sử dụng TLS/SSL, vì vậy nó không gặp vấn đề về "mắt xích yếu nhất" như Tor. I2P đã được nhiều người ở Syria sử dụng trong thời kỳ "Mùa xuân Ả Rập", và gần đây dự án đã chứng kiến sự tăng trưởng lớn hơn trong các cài đặt I2P theo ngôn ngữ nhỏ hơn ở Cận Đông và Trung Đông. Điều quan trọng nhất cần lưu ý ở đây là I2P là một công nghệ và bạn cần hướng dẫn/cách thức để tăng cường quyền riêng tư/ẩn danh của mình trên Internet. Ngoài ra hãy kiểm tra trình duyệt của bạn hoặc nhập công cụ tìm kiếm dấu vân tay để chặn các cuộc tấn công dấu vân tay với một bộ dữ liệu rất lớn (nghĩa là: đuôi dài điển hình / cấu trúc dữ liệu đa dạng rất chính xác) về nhiều thứ trong môi trường và đừng sử dụng VPN để giảm mọi rủi ro đến từ chính nó như hành vi bộ nhớ đệm TLS riêng và cấu trúc kỹ thuật của nhà cung cấp dịch vụ có thể bị hack dễ dàng hơn một hệ thống máy tính để bàn riêng. Có thể sử dụng Tor V-Browser cô lập với khả năng chống dấu vân tay tuyệt vời và bảo vệ suốt đời appguard tổng thể chỉ cho phép các giao tiếp hệ thống cần thiết và sử dụng vm cuối cùng với các script vô hiệu hóa chống gián điệp và live-cd để loại bỏ mọi "rủi ro có thể gần như vĩnh viễn" và giảm tất cả rủi ro bằng xác suất giảm dần là một lựa chọn tốt trong mạng công cộng và mô hình rủi ro cá nhân cao và có thể là điều tốt nhất bạn có thể làm với mục tiêu này khi sử dụng i2p.

### Làm thế nào để reseed thủ công? {#manual_reseed}

Có, đối với các nút I2P khác biết về router của bạn. Chúng tôi sử dụng điều này để kết nối với phần còn lại của mạng I2P. Các địa chỉ được lưu trữ vật lý trong "routerInfos (các đối tượng key,value)", được lấy từ xa hoặc nhận từ peer. "routerInfos" chứa một số thông tin (một số thông tin cơ hội tùy chọn được thêm vào), "được công bố bởi peer", về chính router đó để khởi động. Không có dữ liệu nào trong đối tượng này về các client. Xem xét kỹ hơn bên trong sẽ cho bạn biết rằng mọi người đều được đếm bằng loại tạo id mới nhất có tên là "SHA-256 Hashes (low=Positive hash(-key), high=Negative hash(+key))". Mạng I2P có cơ sở dữ liệu riêng của các routerInfos được tạo trong quá trình tải lên và lập chỉ mục, nhưng điều này phụ thuộc sâu vào việc thực hiện các bảng key/value và cấu trúc mạng và trạng thái tải / trạng thái băng thông cùng xác suất định tuyến cho việc lưu trữ trong các thành phần DB.

### Is using an outproxy safe? {#proxy_safe}

Điều này phụ thuộc vào định nghĩa "an toàn" của bạn là gì. Outproxy rất tuyệt khi chúng hoạt động, nhưng tiếc là chúng được vận hành tự nguyện bởi những người có thể mất hứng thú hoặc có thể không có đủ nguồn lực để duy trì chúng 24/7 – xin lưu ý rằng bạn có thể trải qua những khoảng thời gian mà các dịch vụ không khả dụng, bị gián đoạn hoặc không ổn định, và chúng tôi không liên kết với dịch vụ này cũng như không có ảnh hưởng gì đến nó.

Bản thân các outproxy có thể thấy lưu lượng truy cập của bạn đi và đến, ngoại trừ dữ liệu HTTPS/SSL được mã hóa đầu cuối, giống như ISP của bạn có thể thấy lưu lượng truy cập đi và đến từ máy tính của bạn. Nếu bạn cảm thấy thoải mái với ISP của mình, thì sử dụng outproxy cũng không tệ hơn.

### Router của tôi có phải là "exit node"(outproxy) ra Internet thông thường không? Tôi không muốn như vậy. {#exit}

Để biết thêm chi tiết, hãy đọc thêm tại bài viết của chúng tôi về [Mô hình Đe dọa](/docs/overview/threat-model). Nhìn chung, việc bỏ ẩn danh không đơn giản, nhưng có thể xảy ra nếu bạn không đủ thận trọng.

---

## Internet Access/Performance

### Có dễ dàng phát hiện việc sử dụng I2P bằng cách phân tích lưu lượng mạng không? {#detection}

Dịch vụ proxy để truy cập các trang web Internet (eepsite kết nối ra Internet) được cung cấp cho người dùng I2P bởi các nhà cung cấp không chặn. Dịch vụ này không phải là trọng tâm chính của phát triển I2P, và được cung cấp trên cơ sở tự nguyện. Các eepsite được lưu trữ trên I2P sẽ luôn hoạt động mà không cần outproxy. Outproxy là một tiện ích nhưng theo thiết kế chúng không hoàn hảo cũng như không phải là một phần quan trọng của dự án. Hãy lưu ý rằng chúng có thể không cung cấp được dịch vụ chất lượng cao như các dịch vụ khác của I2P có thể cung cấp.

### Sử dụng I2P có an toàn không? {#safe}

HTTP proxy mặc định chỉ hỗ trợ outproxy cho HTTP và HTTPS.

### Tôi thấy địa chỉ IP của tất cả các node I2P khác trong bảng điều khiển router. Điều đó có nghĩa là địa chỉ IP của tôi có thể bị người khác nhìn thấy không? {#netdb_ip}

Đầu tiên, hãy đảm bảo bạn có phiên bản mới nhất của mọi thành phần liên quan đến I2P – các phiên bản cũ có những đoạn mã không cần thiết làm tiêu tốn CPU. Ngoài ra còn có một [Nhật ký hiệu năng](/about/performance) ghi lại một số cải tiến về hiệu năng của I2P theo thời gian.

### Việc sử dụng outproxy có an toàn không? {#proxy_safe}

Tính ổn định chung của mạng I2P là một lĩnh vực nghiên cứu đang được tiến hành. Một phần đáng kể của nghiên cứu đó tập trung vào việc những thay đổi nhỏ trong cài đặt cấu hình ảnh hưởng như thế nào đến hành vi của router. Vì I2P là một mạng ngang hàng (peer-to-peer), các hành động của các peer khác sẽ có ảnh hưởng đến hiệu suất router của bạn.

### Các cuộc tấn công "De-Anonymizing" (Phá bỏ ẩn danh) thì sao? {#deanon}

I2P có các biện pháp bảo vệ khác nhau bổ sung thêm định tuyến và các lớp mã hóa. Nó cũng chuyển hướng lưu lượng qua các peer khác (Tunnels) có tốc độ và chất lượng riêng, một số chậm, một số nhanh. Điều này dẫn đến nhiều chi phí overhead và lưu lượng truy cập với tốc độ khác nhau theo các hướng khác nhau. Theo thiết kế, tất cả những điều này sẽ làm cho nó chậm hơn so với kết nối trực tiếp trên internet, nhưng ẩn danh hơn nhiều và vẫn đủ nhanh cho hầu hết các mục đích.

Dưới đây là một ví dụ được trình bày kèm theo giải thích để giúp cung cấp ngữ cảnh về các yếu tố độ trễ và băng thông khi sử dụng I2P.

Xem xét sơ đồ dưới đây. Nó mô tả một kết nối giữa một client thực hiện yêu cầu qua I2P, một server nhận yêu cầu qua I2P và sau đó phản hồi lại cũng qua I2P. Đường truyền mà yêu cầu đi qua cũng được mô tả trong sơ đồ.

Từ sơ đồ, hãy xem các ô được đánh dấu 'P', 'Q' và 'R' đại diện cho một tunnel outbound của 'A' và các ô được đánh dấu 'X', 'Y' và 'Z' đại diện cho một tunnel outbound của 'B'. Tương tự, các ô được đánh dấu 'X', 'Y' và 'Z' đại diện cho một tunnel inbound của 'B' trong khi các ô được đánh dấu 'P_1', 'Q_1' và 'R_1' đại diện cho một tunnel inbound của 'A'. Các mũi tên giữa các ô hiển thị hướng lưu lượng. Văn bản phía trên và dưới các mũi tên mô tả một số ví dụ về băng thông giữa một cặp hop cũng như độ trễ ví dụ.

Khi cả client và server đều sử dụng tunnel 3-hop, tổng cộng có 12 router I2P khác tham gia vào việc chuyển tiếp lưu lượng. 6 peer chuyển tiếp lưu lượng từ client đến server được chia thành một outbound tunnel 3-hop từ 'A' ('P', 'Q', 'R') và một inbound tunnel 3-hop đến 'B' ('X', 'Y', 'Z'). Tương tự, 6 peer chuyển tiếp lưu lượng từ server trở lại client.

Đầu tiên, chúng ta có thể xem xét độ trễ - thời gian cần thiết để một yêu cầu từ client đi qua mạng I2P, đến server và quay trở lại client. Cộng tất cả các độ trễ lại, chúng ta thấy rằng:

```
    40 + 100 + 20 + 60 + 80 + 10 + 30 ms        (client to server)
  + 60 + 40 + 80 + 60 + 100 + 20 + 40 ms        (server to client)
  -----------------------------------
  TOTAL:                          740 ms
```
Tổng thời gian khứ hồi trong ví dụ của chúng ta lên tới 740 ms - chắc chắn cao hơn nhiều so với những gì người dùng thường thấy khi duyệt các trang web internet thông thường.

Thứ hai, chúng ta có thể xem xét băng thông khả dụng. Điều này được xác định thông qua liên kết chậm nhất giữa các hop từ client đến server cũng như khi lưu lượng đang được truyền từ server đến client. Đối với lưu lượng đi từ client đến server, chúng ta thấy rằng băng thông khả dụng trong ví dụ của chúng ta giữa các hop 'R' & 'X' cũng như các hop 'X' & 'Y' là 32 KB/s. Mặc dù băng thông khả dụng cao hơn giữa các hop khác, những hop này sẽ đóng vai trò là điểm nghẽn cổ chai và sẽ giới hạn băng thông khả dụng tối đa cho lưu lượng từ 'A' đến 'B' ở mức 32 KB/s. Tương tự, theo dõi đường đi từ server đến client cho thấy băng thông tối đa là 64 KB/s - giữa các hop 'Z_1' & 'Y_1, 'Y_1' & 'X_1' và 'Q_1' & 'P_1'.

Chúng tôi khuyến nghị bạn tăng giới hạn băng thông của mình. Điều này giúp mạng lưới bằng cách tăng lượng băng thông khả dụng, từ đó sẽ cải thiện trải nghiệm I2P của bạn. Cài đặt băng thông nằm ở trang [http://localhost:7657/config](http://localhost:7657/config). Vui lòng lưu ý đến giới hạn kết nối internet của bạn do nhà cung cấp dịch vụ Internet (ISP) quy định, và điều chỉnh cài đặt cho phù hợp.

Chúng tôi cũng khuyến nghị thiết lập băng thông chia sẻ đủ lớn - điều này cho phép các tunnel tham gia được định tuyến qua router I2P của bạn. Cho phép lưu lượng tham gia giúp router của bạn được tích hợp tốt vào mạng lưới và cải thiện tốc độ truyền tải của bạn.

I2P là một dự án đang trong quá trình phát triển. Rất nhiều cải tiến và sửa lỗi đang được triển khai, và nói chung, chạy phiên bản mới nhất sẽ giúp cải thiện hiệu suất của bạn. Nếu chưa làm, hãy cài đặt phiên bản mới nhất.

### I think I found a bug, where can I report it? {#bug}

Bạn có thể báo cáo bất kỳ lỗi/vấn đề nào gặp phải trên hệ thống theo dõi lỗi của chúng tôi, có sẵn trên cả internet công cộng và I2P. Chúng tôi có diễn đàn thảo luận, cũng có sẵn trên I2P và internet công cộng. Bạn cũng có thể tham gia kênh IRC của chúng tôi: thông qua mạng IRC của chúng tôi, IRC2P, hoặc trên Freenode.

- **Bugtracker của chúng tôi:**
  - Internet không riêng tư: [https://i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)
  - Trên I2P: [http://git.idk.i2p/I2P_Developers/i2p.i2p/issues](http://git.idk.i2p/I2P_Developers/i2p.i2p/issues)
- **Diễn đàn của chúng tôi:** [i2pforum.i2p](http://i2pforum.i2p/)
- **Dán nhật ký:** Bạn có thể dán bất kỳ nhật ký thú vị nào vào dịch vụ paste như các dịch vụ internet không riêng tư được liệt kê trên [PrivateBin Wiki](https://github.com/PrivateBin/PrivateBin/wiki/PrivateBin-Directory), hoặc dịch vụ paste I2P như [phiên bản PrivateBin này](http://paste.crypthost.i2p) hoặc [dịch vụ paste không cần Javascript này](http://pasta-nojs.i2p) và theo dõi trên IRC trong #i2p
- **IRC:** Tham gia #i2p-dev để thảo luận với các nhà phát triển trên IRC

Vui lòng bao gồm thông tin liên quan từ trang nhật ký router có sẵn tại: [http://127.0.0.1:7657/logs](http://127.0.0.1:7657/logs). Chúng tôi yêu cầu bạn chia sẻ toàn bộ văn bản trong phần 'I2P Version and Running Environment' cũng như bất kỳ lỗi hoặc cảnh báo nào được hiển thị trong các nhật ký khác nhau trên trang.

---

### Tôi không thể truy cập các trang web Internet thông thường qua I2P. {#outproxy}

Tuyệt vời! Tìm chúng tôi trên IRC:

- trên `irc.freenode.net` kênh `#i2p`
- trên `IRC2P` kênh `#i2p`

hoặc đăng lên [diễn đàn](http://i2pforum.i2p/) và chúng tôi sẽ đăng nó ở đây (cùng với câu trả lời, hy vọng vậy).
