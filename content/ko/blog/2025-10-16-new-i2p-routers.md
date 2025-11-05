---
title: "새로운 I2P Routers"
date: 2025-10-16
author: "idk"
categories: ["community"]
description: "Rust로 작성된 emissary와 Go로 작성된 go-i2p를 포함하여, 여러 새로운 I2P router 구현이 등장하고 있으며, 내장 및 네트워크 다양성에 새로운 가능성을 제공하고 있습니다."
---

지금은 I2P 개발에 매우 흥미진진한 시기입니다. 우리 커뮤니티는 성장하고 있으며, 이제 완전한 기능을 갖춘 새로운 I2P router 프로토타입이 여러 개 등장하고 있습니다! 우리는 이러한 발전과 이 소식을 여러분과 공유하게 되어 매우 기쁩니다.

## 이것이 네트워크에 어떻게 도움이 되나요?

I2P routers를 구현하는 것은 우리의 명세 문서가 새로운 I2P routers를 만드는 데 사용될 수 있음을 입증하는 데 도움이 되고, 코드를 새로운 분석 도구에 개방하며, 전반적으로 네트워크의 보안성과 상호운용성을 향상시킵니다. 여러 I2P routers가 존재한다는 것은 잠재적인 버그가 획일적이지 않음을 의미하며, 한 router에 대한 공격이 다른 router에서는 통하지 않을 수 있어 monoculture(단일 생태계) 문제를 피할 수 있다는 뜻입니다. 그러나 장기적으로 가장 흥미로운 가능성은 아마도 `embedding`입니다.

## `embedding`이란 무엇인가요?

I2P의 맥락에서 `embedding`(내장 방식)은 백그라운드에서 독립 실행형 router를 실행할 필요 없이, 다른 앱에 I2P router를 직접 포함하는 방식입니다. 이는 I2P를 더 쉽게 사용할 수 있게 하는 방법으로, 소프트웨어의 접근성을 높여 네트워크가 더 쉽게 성장하도록 돕습니다. Java와 C++ 모두 자체 생태계 밖에서는 사용하기 어렵다는 문제가 있으며, C++은 취약한 수작업 C 바인딩을 요구하고, Java의 경우 비-JVM 애플리케이션에서 JVM 애플리케이션과 통신해야 하는 번거로움이 있습니다.

많은 면에서 이 상황은 꽤 정상적이지만, I2P의 접근성을 높이기 위해 개선할 수 있다고 생각합니다. 다른 언어들은 이러한 문제에 대해 더 세련된 해결책을 가지고 있습니다. 물론, Java 및 C++ routers에 대한 기존 가이드라인을 항상 고려하고 활용해야 합니다.

## `emissary`가 어둠 속에서 나타난다

우리 팀과는 완전히 독립적으로, `altonen`이라는 개발자가 `emissary`라는 이름의 Rust 기반 I2P 구현을 개발했습니다. 아직 상당히 새로운 프로젝트이고 우리에게는 Rust가 익숙하지 않지만, 이 흥미로운 프로젝트는 큰 잠재력을 지니고 있습니다. `emissary`를 만든 altonen에게 축하를 전하며, 우리는 상당히 깊은 인상을 받았습니다.

### Why Rust?

Rust를 사용하는 주된 이유는 기본적으로 Java나 Go를 사용하는 이유와 같다. Rust는 메모리 관리 기능과 거대하고 매우 열정적인 커뮤니티를 갖춘 컴파일형 프로그래밍 언어다. 또한 Rust는 C 프로그래밍 언어용 바인딩을 생성하기 위한 고급 기능을 제공하며, 이를 통해 다른 언어보다 유지보수가 더 쉬우면서도 Rust의 강력한 메모리 안전성 기능을 그대로 계승할 수 있다.

### Do you want to get involved with `emissary`?

`emissary`는 `altonen`이 GitHub에서 개발하고 있습니다. 저장소는 다음에서 찾을 수 있습니다: [altonen/emissary](https://github.com/altonen/emissary). 또한 Rust에는 인기 있는 Rust 네트워킹 도구와 호환되는 포괄적인 SAMv3(SAM 프로토콜 v3) 클라이언트 라이브러리가 부족하므로, SAMv3 라이브러리를 작성하는 것부터 시작하는 것이 훌륭한 출발점입니다.

## `go-i2p` is getting closer to completion

약 3년 동안 `go-i2p`를 개발해 오면서, 초기 단계의 라이브러리를 순수 Go(또 하나의 메모리 안전한 언어)로 구현된 완전한 기능을 갖춘 I2P router로 발전시키기 위해 노력해 왔습니다. 지난 6개월가량 동안에는 성능, 신뢰성, 유지보수성을 향상시키기 위해 대대적인 재구성이 이루어졌습니다.

### Why Go?

Rust와 Go는 많은 공통된 장점을 가지고 있지만, 여러 면에서 Go가 배우기에 훨씬 더 단순합니다. 수년간 Go 프로그래밍 언어에서 I2P를 사용하기 위한 훌륭한 라이브러리와 애플리케이션이 존재해 왔으며, SAMv3.3 라이브러리에 대한 가장 완전한 구현도 포함되어 있습니다. 그러나 자동으로 관리할 수 있는 I2P router(예: embedded router)가 없다면 사용자들에게는 여전히 장벽이 됩니다. go-i2p의 목적은 그 격차를 메우고, Go에서 작업하는 I2P 애플리케이션 개발자들을 위해 모든 불편함과 까다로운 부분을 제거하는 것입니다.

### 왜 Rust인가?

`go-i2p`는 현재 주로 `eyedeekay`가 Github에서 개발하고 있으며, 커뮤니티의 기여를 [go-i2p](https://github.com/go-i2p/)에서 받고 있습니다. 이 네임스페이스에는 다음과 같은 많은 프로젝트가 있습니다:

#### Router Libraries

우리는 I2P router 라이브러리를 제작하기 위해 이러한 라이브러리를 만들었습니다. 검토를 용이하게 하고 실험적이고 맞춤형 I2P router를 만들고자 하는 다른 사람들에게도 유용하도록, 여러 개의 목적별 저장소로 분산해 두었습니다.

- [go-i2p the router itself, most active right now](https://github.com/go-i2p/go-i2p)
- [common our core library for I2P datastructures](https://github.com/go-i2p/common)
- [crypto our library for cryptographic operations](https://github.com/go-i2p/crypto)
- [go-noise a library for implementing noise-based connections](https://github.com/go-i2p/go-noise)
- [noise a low-level library for using the Noise framework](https://github.com/go-i2p/noise)
- [su3 a library for manipulating su3 files](https://github.com/go-i2p/su3)

#### Client libraries

- [onramp a very convenient library for using(or combining) I2P and Tor](https://github.com/go-i2p/onramp)
- [go-sam-go an advanced, efficient, and very complete SAMv3 library](https://github.com/go-i2p/go-sam-go)

## If you don't like Go or Rust and are thinking of writing an I2P Router, what should you do?

음, XBox에서 I2P를 실행하고 싶다면 [C#로 된 I2P router](https://github.com/PeterZander/i2p-cs)를 작성하려는 휴면 상태의 프로젝트가 하나 있습니다. 사실 꽤 멋져 보입니다. 그것도 마음에 들지 않으면, `altonen`이 했던 것처럼 완전히 새로운 I2P router를 개발할 수도 있습니다.

### `emissary`에 참여하시겠습니까?

I2P는 자유로운 네트워크이므로 어떤 이유에서든 I2P router를 구현할 수 있습니다. 그러나 왜 그렇게 하는지 스스로 분명히 아는 것이 도움이 됩니다. 힘을 실어주고 싶은 커뮤니티, I2P에 잘 맞는다고 생각하는 도구, 또는 시도해 보고 싶은 전략이 있나요? 무엇이 목표인지 정해야 어디서 시작해야 하는지, 그리고 "완료" 상태가 어떤 모습일지를 알 수 있습니다.

### Decide what language you want to do it in and why

언어를 선택할 때 고려할 수 있는 이유는 다음과 같습니다:

- **C**: No need for binding-generation, supported everywhere, can be called from any language, lingua franca of modern computing
- **Typescript**: Massive community, lots of applications, services, and libraries, works with `node` and `deno`, seems like it's everywhere right now
- **D**: It's memory safe and not Rust or Go
- **Vala**: It emits C code for the target platform, combining some of the advantages of memory-safe languages with the flexibility of C
- **Python**: Everybody uses Python

하지만 다음은 그 언어들을 선택하지 않을 수도 있는 몇 가지 이유입니다:

- **C**: Memory management can be challenging, leading to impactful bugs
- **Typescript**: TypeScript is transpiled to JavaScript, which is interpreted and may impact performance
- **D**: Relatively small community
- **Vala**: Not a lot of underlying infrastructure in Vala, you end up using C versions of most libraries
- **Python**: It's an interpreted language which may impact performance

프로그래밍 언어는 수백 가지가 있으며, 우리는 모든 언어로 구현되어 유지보수되는 I2P 라이브러리와 routers를 환영합니다. 트레이드오프를 현명하게 선택하고 시작하세요.

## `go-i2p`는 완성에 점차 가까워지고 있습니다

Rust, Go, Java, C++ 또는 다른 언어로 작업하고 싶다면 Irc2P의 #i2p-dev에서 저희에게 연락해 주세요. 그곳에서 시작하시면 router 전용 채널로 초대해 드리겠습니다. 저희는 ramble.i2p의 f/i2p, reddit의 r/i2p, 그리고 GitHub 및 git.idk.i2p에서도 활동하고 있습니다. 곧 연락을 기다리겠습니다.
