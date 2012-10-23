<?php
require_once 'inc.php';

$start =  microtime(true);

$xpath = '(//table//table//table//td)[last()]';

$url = 'http://myip.ru/';
$proxy_host = '174.122.73.8';
$proxy_port = 3128;
$proxy_user = 'ip2';
$proxy_pass = 'uyuxithaitaiwaihaquu';

$ch = curl_init();
curl_setopt($ch, CURLOPT_VERBOSE, TRUE);
//curl_setopt($ch, CURLOPT_AUTOREFERER, TRUE);
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_HEADER, FALSE);
//curl_setopt($ch, CURLOPT_COOKIESESSION, TRUE);
//curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, TRUE);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, FALSE);
curl_setopt($ch, CURLOPT_PROXY, $proxy_host);
curl_setopt($ch, CURLOPT_PROXYPORT, $proxy_port);
curl_setopt($ch, CURLOPT_PROXYUSERPWD, $proxy_user . ':' . $proxy_pass);
$html = curl_exec($ch);
$info = curl_getinfo($ch);

if($info['http_code'] == 200) {
    $dom = new DOMDocument();
    @$dom->loadHTML($html);
    $dom_xpath = new DOMXPath($dom);
    $dom_nodes = $dom_xpath->query($xpath);
    foreach ($dom_nodes as $node) {
        echo $node->nodeValue;
    }
} else {
    print_r($info);
}

$end =  microtime(true);
$amout = $end - $start;
//echo PHP_EOL . 'TIME TAKEN: ' . $amout;
