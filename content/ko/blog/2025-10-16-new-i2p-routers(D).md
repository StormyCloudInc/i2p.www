---
title: "새로운 I2P 라우터(D)"
date: 2025-10-16
author: "idk"
categories: ["community"]
description: "임베딩과 네트워크 다양성을 위한 새로운 가능성을 제공하는 Rust의 emissary와 Go의 go-i2p를 비롯한 여러 새로운 I2P 라우터 구현이 등장하고 있습니다."
---


지금은 I2P 개발의 흥미로운 시기이며, 저희 커뮤니티가 성장하고 있고 이제 완전히 작동하는 새로운 I2P 라우터 프로토타입이 여러 개 등장하고 있습니다! 저희는 이러한 발전과 소식을 여러분과 공유하게 되어 매우 기쁩니다.

## 이것이 네트워크에 어떤 도움이 되나요?

I2P 라우터를 작성하면 사양 문서가 새로운 I2P 라우터를 만드는 데 사용될 수 있음을 증명하고 새로운 분석 도구에 코드를 개방하며 일반적으로 네트워크의 보안과 상호 운용성을 개선하는 데 도움이 됩니다. I2P 라우터가 여러 대라는 것은 잠재적인 버그가 균일하지 않다는 것을 의미하며, 한 라우터에 대한 공격이 다른 라우터에서는 작동하지 않을 수 있으므로 단일 라우터 문제를 피할 수 있습니다. 그러나 장기적으로 가장 흥미로운 전망은 아마도 '임베딩'일 것입니다.

## '임베딩'이란 무엇인가요?

I2P의 맥락에서 '임베딩'은 독립형 라우터를 백그라운드에서 실행할 필요 없이 다른 앱에 직접 I2P 라우터를 포함시키는 방법입니다. 이는 I2P를 더 쉽게 사용할 수 있는 방법으로, 소프트웨어의 접근성을 높여 네트워크를 더 쉽게 확장할 수 있습니다. Java와 C++는 모두 자체 에코시스템 외부에서 사용하기 어렵다는 단점이 있으며, C++는 깨지기 쉬운 수기 C 바인딩이 필요하고 Java의 경우 JVM이 아닌 애플리케이션에서 JVM 애플리케이션과 통신해야 하는 어려움이 있습니다.

여러 면에서 이러한 상황은 지극히 정상적인 것이지만, I2P의 접근성을 높이기 위해 개선될 수 있다고 생각합니다. 다른 언어에는 이러한 문제에 대한 더 우아한 해결책이 있습니다. 물론 Java 및 C++ 라우터에 대한 기존 가이드라인을 항상 고려하고 사용해야 합니다.

## 어둠 속에서 '사절단'이 나타납니다.

저희 팀과는 완전히 독립적으로 'altonen'이라는 개발자가 'emissary'라는 I2P의 Rust 구현을 개발했습니다. 아직 새롭고 Rust는 우리에게 생소하지만, 이 흥미로운 프로젝트는 큰 가능성을 가지고 있습니다. 알토넨이 `emissary`를 개발한 것을 축하드립니다.

### 왜 러스트일까요?

Rust를 사용하는 주된 이유는 기본적으로 Java나 Go를 사용하는 이유와 동일합니다. Rust는 메모리 관리 기능이 있는 컴파일된 프로그래밍 언어이며 매우 열정적인 대규모 커뮤니티가 있습니다. 또한 Rust는 다른 언어에 비해 유지 관리가 쉬우면서도 Rust의 강력한 메모리 안전 기능을 그대로 계승하는 C 프로그래밍 언어에 대한 바인딩을 생성하기 위한 고급 기능을 제공합니다.

### '메신저'에 참여하고 싶으신가요?

'emissary'는 `altonen`이 Github에서 개발했습니다. 저장소는 다음에서 찾을 수 있습니다: [altonen/emissary](https://github.com/altonen/emissary). Rust는 또한 널리 사용되는 Rust 네트워킹과 호환되는 포괄적인 SAMv3 클라이언트 라이브러리가 부족하기 때문에 SAMv3 라이브러리를 작성하는 것이 좋은 출발점이 될 수 있습니다.

## 'GO-I2P'의 완성이 가까워지고 있습니다.

저는 약 3년 동안 'go-i2p'를 개발하면서 신생 라이브러리를 또 다른 메모리 안전 언어인 pure-Go로 본격적인 I2P 라우터로 바꾸려고 노력해 왔습니다. 지난 6개월 정도 동안 성능, 안정성 및 유지보수성을 개선하기 위해 대폭적으로 재구성했습니다.

### 왜 가야 하나요?

Rust와 Go는 동일한 장점을 많이 가지고 있지만, 여러 가지 면에서 Go가 훨씬 더 배우기 쉽습니다. 수년 동안 Go 프로그래밍 언어에서 I2P를 사용하기 위한 훌륭한 라이브러리와 애플리케이션이 존재해 왔으며, 가장 완벽한 구현의 SAMv3.3 라이브러리도 포함되어 있습니다. 그러나 임베디드 라우터와 같이 자동으로 관리할 수 있는 I2P 라우터가 없으면 여전히 사용자에게 장벽이 됩니다. go-i2p의 요점은 그 간극을 메우고, Go에서 작업하는 I2P 애플리케이션 개발자들을 위해 모든 거친 부분을 제거하는 것입니다.

### 'GO-I2P'에 참여하고 싶으신가요?

'go-i2p'는 현재 주로 'eyedeekay'에 의해 Github에서 개발되고 있으며 [go-i2p](https://github.com/go-i2p/)에서 커뮤니티의 기여에 열려 있습니다. 이 네임스페이스에는 다음과 같은 많은 프로젝트가 존재합니다:

#### 라우터 라이브러리

저희는 I2P 라우터 라이브러리를 제작하기 위해 이러한 라이브러리를 구축했습니다. 이 라이브러리는 여러 개의 집중된 리포지토리에 분산되어 있어 검토가 용이하고 실험적인 맞춤형 I2P 라우터를 구축하려는 다른 사람들에게 유용하게 사용될 수 있습니다.

- [go-i2p the router itself, most active right now](https://github.com/go-i2p/go-i2p)
- [common our core library for I2P datastructures](https://github.com/go-i2p/common)
- [crypto our library for cryptographic operations](https://github.com/go-i2p/crypto)
- [go-noise a library for implementing noise-based connections](https://github.com/go-i2p/go-noise)
- [noise a low-level library for using the Noise framework](https://github.com/go-i2p/noise)
- [su3 a library for manipulating su3 files](https://github.com/go-i2p/su3)

#### 클라이언트 라이브러리

- [onramp a very convenient library for using(or combining) I2P and Tor](https://github.com/go-i2p/onramp)
- [go-sam-go an advanced, efficient, and very complete SAMv3 library](https://github.com/go-i2p/go-sam-go)

## Go나 Rust가 마음에 들지 않고 I2P 라우터를 사용하려는 경우 어떻게 해야 할까요?

X박스에서 I2P를 실행하고 싶다면 [C#으로 I2P 라우터]를 작성하는 휴면 프로젝트(https://github.com/PeterZander/i2p-cs)가 있습니다. 사실 꽤 깔끔하게 들리네요. 그것도 선호하지 않는다면 'altonen'이 한 것처럼 완전히 새로운 것을 개발할 수도 있습니다.

### 작성 이유와 작성 대상을 결정하세요.

무료 네트워크인 I2P 라우터는 어떤 이유로든 만들 수 있지만, 그 이유를 알아두면 도움이 될 것입니다. 힘을 실어주고 싶은 커뮤니티가 있거나, I2P에 적합하다고 생각되는 도구가 있거나, 시도해보고 싶은 전략이 있나요? 목표가 무엇인지 파악하여 어디서부터 시작해야 하는지, '완성된' 상태는 어떤 모습일지 생각해 보세요.

### 원하는 언어와 그 이유를 결정하세요.

언어를 선택할 수 있는 몇 가지 이유는 다음과 같습니다:

- **C**: No need for binding-generation, supported everywhere, can be called from any language, lingua franca of modern computing
- **Typescript**: Massive community, lots of applications, services, and libraries, works with `node` and `deno`, seems like it's everywhere right now
- **D**: It's memory safe and not Rust or Go
- **Vala**: It emits C code for the target platform, combining some of the advantages of memory-safe languages with the flexibility of C
- **Python**: Everybody uses Python

하지만 이러한 언어를 선택하지 않을 수 있는 몇 가지 이유가 있습니다:

- **C**: Memory management can be challenging, leading to impactful bugs
- **Typescript**: TypeScript is transpiled to JavaScript, which is interpreted and may impact performance
- **D**: Relatively small community
- **Vala**: Not a lot of underlying infrastructure in Vala, you end up using C versions of most libraries
- **Python**: It's an interpreted language which may impact performance

수백 개의 프로그래밍 언어가 있으며 모든 프로그래밍 언어에서 유지 관리되는 I2P 라이브러리와 라우터를 환영합니다. 장단점을 현명하게 선택하고 시작하세요.

## 연락하여 코딩 시작하기

Rust, Go, Java, C++ 또는 다른 언어로 작업하고 싶으시다면 Irc2P의 #i2p-dev로 연락해 주세요. 거기서 시작하시면 라우터별 채널에 온보딩해드리겠습니다. f/i2p의 ramble.i2p, reddit의 r/i2p, GitHub 및 git.idk.i2p에서도 만나보실 수 있습니다. 곧 여러분의 의견을 기다리겠습니다.
