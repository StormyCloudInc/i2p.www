---
title: "BOB – الجسر المفتوح الأساسي"
description: "واجهة برمجة التطبيقات المهملة لإدارة الوجهات (مهملة)"
slug: "bob"
lastUpdated: "2025-05"
layout: "single"
reviewStatus: "needs-review"
---

> **تحذير:** BOB (واجهة برمجة تطبيقات قديمة ضمن I2P) يدعم فقط نوع التوقيع القديم DSA-SHA1. توقّف Java I2P عن تضمين BOB في **1.7.0 (2022-02)**؛ ولا يزال موجوداً فقط في التثبيتات التي بدأت بـ 1.6.1 أو أقدم وفي بعض إصدارات i2pd. **يجب** على التطبيقات الجديدة استخدام [SAM v3](/docs/api/samv3/).

## واجهات ربط للغات البرمجة

- Go – [ccondom](https://bitbucket.org/kallevedin/ccondom)
- بايثون – [`i2py-bob`](http://git.repo.i2p/w/i2py-bob.git)
- Twisted – [`txi2p`](https://pypi.python.org/pypi/txi2p)
- C++ – [`bobcpp`](https://gitlab.com/rszibele/bobcpp)

## ملاحظات البروتوكول

- تشير `KEYS` إلى وجهة بصيغة base64 (مفاتيح عامة + خاصة).  
- `KEY` هو مفتاح عام بصيغة base64.  
- تأتي ردود `ERROR` بالشكل `ERROR <description>\n`.  
- يشير `OK` إلى اكتمال الأمر؛ وتأتي بيانات اختيارية بعده في السطر نفسه.  
- تقوم أسطر `DATA` ببث مخرجات إضافية قبل `OK` النهائي.

أمر `help` هو الاستثناء الوحيد: قد لا يُرجِع شيئًا للإشارة إلى «لا يوجد أمر بهذا الاسم».

## لافتة الاتصال

يستخدم BOB أسطر ASCII (ترميز المحارف) منتهية بمحرف نهاية سطر (LF أو CRLF). عند الاتصال، يُرسل:

```
BOB <version>
OK
```
الإصدار الحالي: `00.00.10`. كانت الإصدارات السابقة تستخدم خانات سداسية عشرية بأحرف كبيرة وترقيمًا غير قياسي.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">BOB Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.8</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Latest defined version</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.00 – 00.00.0F</td><td style="border:1px solid var(--color-border); padding:0.5rem;">—</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Development builds</td></tr>
  </tbody>
</table>
## الأوامر الأساسية

> للاطلاع على التفاصيل الكاملة للأوامر، اتصل عبر `telnet localhost 2827` ثم نفّذ `help`.

```
COMMAND     OPERAND                               RETURNS
help        [command]                             NOTHING | OK <info>
clear                                             ERROR | OK
getdest                                           ERROR | OK <KEY>
getkeys                                           ERROR | OK <KEYS>
getnick     <tunnelname>                          ERROR | OK
inhost      <hostname | IP>                       ERROR | OK
inport      <port>                                ERROR | OK
list                                              ERROR | DATA... + OK
lookup      <hostname>                            ERROR | OK <KEY>
nick        <friendlyname>                        ERROR | OK
outhost     <hostname | IP>                       ERROR | OK
outport     <port>                                ERROR | OK
quit                                              ERROR | OK
setkey      <base64 destination>                  ERROR | OK
start                                             ERROR | OK
status                                            ERROR | DATA... + OK
stop                                              ERROR | OK
```
## ملخص الإهمال

- لا يدعم BOB أنواع التواقيع الحديثة، أو LeaseSets المشفّرة، أو ميزات النقل.
- واجهة برمجة التطبيقات مجمّدة؛ لن تُضاف أوامر جديدة.
- يجب على التطبيقات التي لا تزال تعتمد على BOB الانتقال إلى SAM v3 في أقرب وقت ممكن.
