<?php
header('Content-Type: text/plain; charset=UTF-8');

$to = 'sanchia@ubuntuliferesources.co.za';

$firstName = isset($_POST['conFirstName']) ? trim(strip_tags($_POST['conFirstName'])) : '';
$surname = isset($_POST['conSurname']) ? trim(strip_tags($_POST['conSurname'])) : '';
$email = isset($_POST['conEmail']) ? trim($_POST['conEmail']) : '';
$phone = isset($_POST['conPhone']) ? trim(strip_tags($_POST['conPhone'])) : '';
$message = isset($_POST['conMessage']) ? trim(strip_tags($_POST['conMessage'])) : '';
$brochure = isset($_POST['brochureName']) ? trim(strip_tags($_POST['brochureName'])) : 'Brochure';

if ($firstName === '' || $surname === '' || $email === '' || $phone === '' || $message === '') {
    echo 'N';
    exit;
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo 'N';
    exit;
}

$subject = 'Brochure request: ' . $brochure;
$body = "A visitor has requested a brochure.\r\n\r\n";
$body .= "Brochure: {$brochure}\r\n";
$body .= "Name: {$firstName} {$surname}\r\n";
$body .= "Email: {$email}\r\n";
$body .= "Contact number: {$phone}\r\n\r\n";
$body .= "Message:\r\n{$message}\r\n";

$headers = "From: Ubuntu Life Resources <noreply@ubuntuliferesources.co.za>\r\n";
$headers .= "Reply-To: {$firstName} {$surname} <{$email}>\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

if (mail($to, $subject, $body, $headers)) {
    echo 'Y';
} else {
    echo 'N';
}
