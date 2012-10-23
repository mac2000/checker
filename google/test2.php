<?php
require_once 'inc.php';

$start =  microtime(true);

$xpath_query = file_get_contents('xpath.txt');
$ua = get_random_user_agent();
$cookie = get_cookie_file();

$keyword = 'residency personal statement writing services';
$country = 'countryUS';
$language = 'lang_en';
$top100 = 0;


$url = 'http://www.google.com/';
$html = get_html($url, $ua, $cookie);
if (!intval($html)) {

    $referrer = 'http://www.google.com/';
    $page = 1;

    $url = get_search_url($keyword, $country, $language, $top100);

    $html = get_html($url, $ua, $cookie, $referrer);
    echo 'FIRST PAGE SEARCH RESULTS' . PHP_EOL . '-----------------------------------------' . PHP_EOL;
    if (!intval($html)) {
        $dom = new DOMDocument();
        @$dom->loadHTML($html);
        $dom_xpath = new DOMXPath($dom);
        $dom_nodes = $dom_xpath->query($xpath_query);
        $counter = 1;
        foreach ($dom_nodes as $node) {
            $link = $node->getAttribute('href');
            $domain = parse_url($link, PHP_URL_HOST);
            $domain = str_replace('www.', '', $domain);

            echo ($counter++) . ' ' . $domain . PHP_EOL;
        }
    }
    /*
    $referrer = $url;
    $url = get_search_url('buy resume online in new york', $country, $language, $top100, 2);
    $html = get_html($url, $ua, $cookie, $referrer);
    echo PHP_EOL . 'SECOND PAGE SEARCH RESULTS' . PHP_EOL . '-----------------------------------------' . PHP_EOL;
    if (!intval($html)) {
        $dom = new DOMDocument();
        @$dom->loadHTML($html);
        $dom_xpath = new DOMXPath($dom);
        $dom_nodes = $dom_xpath->query($xpath_query);
        foreach ($dom_nodes as $node) {
            $link = $node->getAttribute('href');
            $domain = parse_url($link, PHP_URL_HOST);
            $domain = str_replace('www.', '', $domain);

            echo ($counter++) . ' ' . $domain . PHP_EOL;
        }
    }
    */

    for($i=2; $i<=10; $i++) {
        $referrer = $url;
        $url = get_search_url('buy resume online in new york', $country, $language, $top100, $i);
        $html = get_html($url, $ua, $cookie, $referrer);
        echo PHP_EOL . 'SECOND PAGE SEARCH RESULTS' . PHP_EOL . '-----------------------------------------' . PHP_EOL;
        if (!intval($html)) {
            $dom = new DOMDocument();
            @$dom->loadHTML($html);
            $dom_xpath = new DOMXPath($dom);
            $dom_nodes = $dom_xpath->query($xpath_query);
            foreach ($dom_nodes as $node) {
                $link = $node->getAttribute('href');
                $domain = parse_url($link, PHP_URL_HOST);
                $domain = str_replace('www.', '', $domain);

                echo ($counter++) . ' ' . $domain . PHP_EOL;
            }
        }
    }

}

$end =  microtime(true);
$amout = $end - $start;
echo PHP_EOL . 'TIME TAKEN: ' . $amout;
