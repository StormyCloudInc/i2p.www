---
title: "Poll Widget Test"
date: 2025-10-23
description: "Test page for poll widget integration"
API_Translate: true
---

This is a test page for the poll widget.

<!-- Poll Widget -->
<div id="poll-widget"
     data-poll-id="2"
     data-api-url="http://feedback.stormycloud.org:5000"
     data-show-results="false">
</div>

<!-- Load widget script (add once per page) -->
<script src="http://feedback.stormycloud.org:5000/widgets/voting.js"></script>
<link rel="stylesheet" href="http://feedback.stormycloud.org:5000/widgets/styles.css">

<!-- Feature Request Widget -->
<!-- Feature Request Widget -->
<div id="features-widget"
     data-api-url="https://feedback.stormycloud.org"
     data-mode="list"
     data-max-items="10">
</div>

<!-- Load widget scripts (add once per page) -->
<script src="https://feedback.stormycloud.org/widgets/features.js"></script>
<link rel="stylesheet" href="https://feedback.stormycloud.org/widgets/styles.css">
  <!-- Add this to any page -->
  <div id="mailing-list-widget"
       data-api-url="https://feedback.stormycloud.org">
  </div>

  <script src="https://feedback.stormycloud.org/widgets/mailing-list.js"></script>
  <link rel="stylesheet" href="https://feedback.stormycloud.org/widgets/styles.css">