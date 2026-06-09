<?php
function ulr_form_page($title, $message, $isError = false)
{
    header('Content-Type: text/html; charset=UTF-8');
    $safeTitle = htmlspecialchars($title, ENT_QUOTES, 'UTF-8');
    $safeMessage = htmlspecialchars($message, ENT_QUOTES, 'UTF-8');
    $accent = $isError ? '#b42318' : '#2d6a4f';
    echo '<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>' . $safeTitle . ' | Ubuntu Life Resources</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 520px; margin: 4rem auto; padding: 0 1rem; color: #1a1a1a; line-height: 1.5; }
    h1 { font-size: 1.5rem; color: ' . $accent . '; }
    a { color: #2d6a4f; }
  </style>
</head>
<body>
  <h1>' . $safeTitle . '</h1>
  <p>' . $safeMessage . '</p>
  <p><a href="javascript:history.back()">Go back</a> &nbsp;|&nbsp; <a href="../../index.html">Home</a></p>
</body>
</html>';
    exit;
}
