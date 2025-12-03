---
title: "Introducer Expiration"
number: "133"
author: "zzz"
created: "2017-02-05"
lastupdated: "2017-08-09"
status: "Closed"
thread: "http://zzz.i2p/topics/2230"
target: "0.9.30"
implementedin: "0.9.30"
toc: true
---

## Overview

This proposal is about improving the success rate for introductions.


## Motivation

Introducers expire after a certain time, but that info isn't published in the
Router Info. Routers must currently use heuristics to estimate when an
introducer is no longer valid.


## Design

In an SSU Router Address containing introducers, the publisher may optionally
include expiration times for each introducer.


## Specification

```
iexp{X}={nnnnnnnnnn}

X :: The introducer number (0-2)

nnnnnnnnnn :: The time in seconds (not ms) since the epoch.
```

### Notes

* Each expiration must be greater than the publish date of the Router Info,
  and less than 6 hours after the publish date of the Router Info.

* Publishing routers and introducers should attempt to keep the introducer valid
  until expiration, however there is no way for them to guarantee this.

* Routers should not use a published introducer after its expiration.

* The introducer expirations are in the Router Address mapping.
  They are not the (currently unused) 8-byte expiration field in the Router Address.

**Example:** `iexp0=1486309470`


## Migration

No issues. Implementation is optional.
Backwards compatibility is assured, as older routers will ignore unknown parameters.


## References

* [RouterAddress](/docs/specs/common-structures/#routeraddress)
* [RouterInfo](/docs/specs/common-structures/#routerinfo)
* [TRAC-TICKET](http://trac.i2p2.i2p/ticket/1352)
