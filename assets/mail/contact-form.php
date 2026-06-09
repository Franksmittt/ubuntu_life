<?php
require_once __DIR__ . '/form-page.php';

$to = 'sanchia@ubuntuliferesources.co.za';

$name = isset($_POST['conName']) ? trim(strip_tags($_POST['conName'])) : '';
$email = isset($_POST['conEmail']) ? trim($_POST['conEmail']) : '';
$phone = isset($_POST['conPhone']) ? trim(strip_tags($_POST['conPhone'])) : '';
$subjectLine = isset($_POST['conSubject']) ? trim(strip_tags($_POST['conSubject'])) : 'General enquiry';
$message = isset($_POST['conMessage']) ? trim(strip_tags($_POST['conMessage'])) : '';

if ($name === '' || $email === '' || $phone === '' || $message === '') {
    ulr_form_page('Missing information', 'Please fill in all required fields and try again.', true);
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    ulr_form_page('Invalid email', 'Please enter a valid email address and try again.', true);
}

$subject = 'Website enquiry: ' . $subjectLine;
$body = "A new message was submitted via the contact form.\r\n\r\n";
$body .= "Name: {$name}\r\n";
$body .= "Email: {$email}\r\n";
$body .= "Phone: {$phone}\r\n";
$body .= "Topic: {$subjectLine}\r\n\r\n";
$body .= "Message:\r\n{$message}\r\n";

$headers = "From: Ubuntu Life Resources <noreply@ubuntuliferesources.co.za>\r\n";
$headers .= "Reply-To: {$name} <{$email}>\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

if (mail($to, $subject, $body, $headers)) {
    ulr_form_page('Message sent', 'Thank you for contacting us. We will get back to you shortly.');
}

ulr_form_page('Something went wrong', 'Your message could not be sent. Please try again or email us directly.', true);
