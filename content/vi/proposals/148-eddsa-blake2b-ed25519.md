---
title: "RedDSA-BLAKE2b-Ed25519"
number: "148"
author: "zzz"
created: "2019-03-12"
lastupdated: "2019-04-11"
status: "Mở"
thread: "http://zzz.i2p/topics/2689"
toc: true
---

## Tổng quan

Đề xuất này thêm một loại chữ ký mới sử dụng BLAKE2b-512 với chuỗi cá nhân hóa và salt, để thay thế SHA-512. Điều này sẽ loại bỏ ba loại tấn công có thể xảy ra.

## Động lực

Trong quá trình thảo luận và thiết kế NTCP2 (đề xuất 111) và LS2 (đề xuất 123), chúng tôi đã xem xét ngắn gọn các cuộc tấn công khác nhau có thể xảy ra và cách ngăn chặn chúng. Ba cuộc tấn công trong số này là Tấn công Mở rộng Độ dài, Tấn công Liên giao thức và Nhận dạng Thông điệp Trùng lặp.

Đối với cả NTCP2 và LS2, chúng tôi quyết định rằng các cuộc tấn công này không liên quan trực tiếp đến các đề xuất hiện tại, và bất kỳ giải pháp nào cũng xung đột với mục tiêu giảm thiểu các nguyên thủy mới. Ngoài ra, chúng tôi xác định rằng tốc độ của các hàm hash trong các giao thức này không phải là yếu tố quan trọng trong các quyết định của chúng tôi. Do đó, chúng tôi phần lớn hoãn lại việc giải quyết cho một đề xuất riêng biệt. Mặc dù chúng tôi đã thêm một số tính năng cá nhân hóa vào đặc tả LS2, chúng tôi không yêu cầu bất kỳ hàm hash mới nào.

Nhiều dự án, chẳng hạn như [ZCash](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf), đang sử dụng các hàm băm và thuật toán chữ ký dựa trên các thuật toán mới hơn không dễ bị tổn thương trước các cuộc tấn công sau đây.

### Length Extension Attacks

SHA-256 và SHA-512 dễ bị tấn công bằng [Tấn công mở rộng độ dài (LEA)](https://en.wikipedia.org/wiki/Length_extension_attack). Điều này xảy ra khi dữ liệu thực tế được ký, chứ không phải hash của dữ liệu. Trong hầu hết các giao thức I2P (streaming, datagrams, netdb và các giao thức khác), dữ liệu thực tế được ký. Một ngoại lệ là các tệp SU3, nơi hash được ký. Ngoại lệ khác là signed datagrams cho DSA (sig type 0), nơi hash được ký. Đối với các signed datagram sig types khác, dữ liệu được ký.

### Cross-Protocol Attacks

Dữ liệu đã ký trong các giao thức I2P có thể dễ bị tấn công Cross-Protocol (CPA) do thiếu sự phân tách miền. Điều này cho phép kẻ tấn công sử dụng dữ liệu nhận được trong một ngữ cảnh (chẳng hạn như một datagram đã ký) và trình bày nó như dữ liệu hợp lệ, đã ký trong một ngữ cảnh khác (chẳng hạn như streaming hoặc network database). Mặc dù không có khả năng dữ liệu đã ký từ một ngữ cảnh sẽ được phân tích cú pháp như dữ liệu hợp lệ trong một ngữ cảnh khác, nhưng rất khó hoặc không thể phân tích tất cả các tình huống để biết chắc chắn. Ngoài ra, trong một số ngữ cảnh, kẻ tấn công có thể có khả năng khiến nạn nhân ký dữ liệu được chế tạo đặc biệt có thể là dữ liệu hợp lệ trong một ngữ cảnh khác. Một lần nữa, rất khó hoặc không thể phân tích tất cả các tình huống để biết chắc chắn.

### Tấn Công Mở Rộng Độ Dài

Các giao thức I2P có thể dễ bị tổn thương bởi Duplicate Message Identification (DMI). Điều này có thể cho phép kẻ tấn công xác định rằng hai thông điệp đã ký có cùng nội dung, ngay cả khi các thông điệp này và chữ ký của chúng đã được mã hóa. Mặc dù điều này khó xảy ra do các phương pháp mã hóa được sử dụng trong I2P, nhưng rất khó hoặc không thể phân tích tất cả các tình huống để biết chắc chắn. Bằng cách sử dụng một hàm hash cung cấp phương pháp thêm salt ngẫu nhiên, tất cả các chữ ký sẽ khác nhau ngay cả khi ký cùng một dữ liệu. Mặc dù Red25519 như được định nghĩa trong đề xuất 123 thêm salt ngẫu nhiên vào hàm hash, điều này không giải quyết vấn đề đối với các leaseSet không được mã hóa.

### Tấn Công Liên Giao Thức

Mặc dù không phải là động lực chính cho đề xuất này, SHA-512 tương đối chậm, và có các hàm hash nhanh hơn có sẵn.

## Goals

- Ngăn chặn các cuộc tấn công trên
- Giảm thiểu việc sử dụng các primitive mật mã mới
- Sử dụng các primitive mật mã tiêu chuẩn, đã được chứng minh
- Sử dụng các đường cong tiêu chuẩn
- Sử dụng các primitive nhanh hơn nếu có sẵn

## Design

Sửa đổi loại chữ ký RedDSA_SHA512_Ed25519 hiện có để sử dụng BLAKE2b-512 thay vì SHA-512. Thêm các chuỗi cá nhân hóa duy nhất cho từng trường hợp sử dụng. Loại chữ ký mới có thể được sử dụng cho cả leaseSet không bị che và có che.

## Justification

- [BLAKE2b](https://blake2.net/blake2.pdf) không dễ bị tổn thương trước LEA.
- BLAKE2b cung cấp cách thức chuẩn để thêm chuỗi cá nhân hóa nhằm phân tách miền
- BLAKE2b cung cấp cách thức chuẩn để thêm salt ngẫu nhiên nhằm ngăn chặn DMI.
- BLAKE2b nhanh hơn SHA-256 và SHA-512 (và MD5) trên phần cứng hiện đại,
  theo [đặc tả BLAKE2](https://blake2.net/blake2.pdf).
- Ed25519 vẫn là loại chữ ký nhanh nhất của chúng ta, nhanh hơn nhiều so với ECDSA, ít nhất là trong Java.
- [Ed25519](http://cr.yp.to/papers.html#ed25519) yêu cầu hàm hash mật mã 512 bit.
  Nó không chỉ định SHA-512. BLAKE2b cũng phù hợp cho hàm hash này.
- BLAKE2b được hỗ trợ rộng rãi trong các thư viện cho nhiều ngôn ngữ lập trình, chẳng hạn như Noise.

## Specification

Sử dụng BLAKE2b-512 không khóa như trong [đặc tả BLAKE2](https://blake2.net/blake2.pdf) với salt và personalization. Tất cả việc sử dụng chữ ký BLAKE2b sẽ dùng chuỗi personalization 16 ký tự.

Khi được sử dụng trong ký RedDSA_BLAKE2b_Ed25519, một salt ngẫu nhiên được cho phép, tuy nhiên nó không cần thiết, vì thuật toán chữ ký thêm 80 byte dữ liệu ngẫu nhiên (xem đề xuất 123). Nếu muốn, khi băm dữ liệu để tính r, hãy đặt một salt ngẫu nhiên BLAKE2b 16-byte mới cho mỗi chữ ký. Khi tính S, hãy đặt lại salt về mặc định là tất cả số không.

Khi được sử dụng trong xác minh RedDSA_BLAKE2b_Ed25519, không sử dụng salt ngẫu nhiên, hãy sử dụng giá trị mặc định là tất cả số không.

Các tính năng salt và personalization không được chỉ định trong [RFC 7693](https://tools.ietf.org/html/rfc7693); sử dụng các tính năng đó như được chỉ định trong [đặc tả BLAKE2](https://blake2.net/blake2.pdf).

### Xác định Thông điệp Trùng lặp

Đối với RedDSA_BLAKE2b_Ed25519, thay thế hàm hash SHA-512 trong RedDSA_SHA512_Ed25519 (loại chữ ký 11, như được định nghĩa trong đề xuất 123) bằng BLAKE2b-512. Không có thay đổi nào khác.

Chúng tôi không cần một sự thay thế cho EdDSA_SHA512_Ed25519ph (loại chữ ký 8) cho các tệp su3, bởi vì phiên bản prehashed của EdDSA không dễ bị tấn công LEA. EdDSA_SHA512_Ed25519 (loại chữ ký 7) không được hỗ trợ cho các tệp su3.

| Type | Type Code | Since | Usage |
|------|-----------|-------|-------|
| RedDSA_BLAKE2b_Ed25519 | 12 | TBD | For Router Identities, Destinations and encrypted leasesets only; never used for Router Identities |
### Tốc độ

Điều sau đây áp dụng cho loại chữ ký mới.

| Data Type | Length |
|-----------|--------|
| Hash | 64 |
| Private Key | 32 |
| Public Key | 32 |
| Signature | 64 |
### Personalizations

Để cung cấp tách biệt miền cho các cách sử dụng khác nhau của chữ ký, chúng ta sẽ sử dụng tính năng cá nhân hóa BLAKE2b.

Tất cả các cách sử dụng chữ ký BLAKE2b sẽ sử dụng chuỗi cá nhân hóa 16 ký tự. Bất kỳ cách sử dụng mới nào cũng phải được thêm vào bảng ở đây, với một chuỗi cá nhân hóa duy nhất.

Handshake NTCP 1 và SSU sử dụng bên dưới là cho dữ liệu đã ký được định nghĩa trong chính handshake đó. RouterInfos đã ký trong DatabaseStore Messages sẽ sử dụng cá nhân hóa NetDb Entry, giống như khi được lưu trữ trong NetDB.

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
## Mục tiêu

## Thiết kế

- Phương án 1: Đề xuất 146;
  Cung cấp khả năng chống LEA
- Phương án 2: [Ed25519ctx trong RFC 8032](https://tools.ietf.org/html/rfc8032);
  Cung cấp khả năng chống LEA và personalization.
  Đã được chuẩn hóa, nhưng có ai sử dụng nó không?
  Xem [RFC 8032](https://tools.ietf.org/html/rfc8032) và [cuộc thảo luận này](https://moderncrypto.org/mail-archive/curves/2017/000925.html).
- Hashing "có khóa" có hữu ích cho chúng ta không?

## Lý do chính đáng

Tương tự như với việc triển khai các loại chữ ký trước đó.

Chúng tôi dự định thay đổi các router mới từ type 7 thành type 12 làm mặc định. Chúng tôi dự định cuối cùng sẽ di chuyển các router hiện có từ type 7 sang type 12, sử dụng quy trình "rekeying" được sử dụng sau khi type 7 được giới thiệu. Chúng tôi dự định thay đổi các destination mới từ type 7 thành type 12 làm mặc định. Chúng tôi dự định thay đổi các destination được mã hóa mới từ type 11 thành type 13 làm mặc định.

Chúng tôi sẽ hỗ trợ blinding từ các loại 7, 11 và 12 sang loại 12. Chúng tôi sẽ không hỗ trợ blinding loại 12 sang loại 11.

Các router mới có thể bắt đầu sử dụng loại chữ ký mới theo mặc định sau vài tháng. Các destination mới có thể bắt đầu sử dụng loại chữ ký mới theo mặc định sau khoảng một năm.

Đối với phiên bản router tối thiểu 0.9.TBD, các router phải đảm bảo:

- Không lưu trữ (hoặc flood) một RI hoặc LS với loại chữ ký mới đến các router có phiên bản thấp hơn 0.9.TBD.
- Khi xác minh một netdb store, không tìm nạp RI hoặ LS với loại chữ ký mới từ các router có phiên bản thấp hơn 0.9.TBD.
- Các router có loại chữ ký mới trong RI của chúng có thể không kết nối được với các router có phiên bản thấp hơn 0.9.TBD,
  dù là với NTCP, NTCP2, hoặc SSU.
- Các kết nối streaming và signed datagrams sẽ không hoạt động với các router có phiên bản thấp hơn 0.9.TBD,
  nhưng không có cách nào để biết điều đó, vì vậy loại chữ ký mới không nên được sử dụng mặc định trong một khoảng thời gian
  vài tháng hoặc vài năm sau khi 0.9.TBD được phát hành.
