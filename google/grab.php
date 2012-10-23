<?php
require_once 'inc.php';

$start = microtime(true);

$xpath_query = file_get_contents('xpath.txt');
$ua = get_random_user_agent();
$cookie = get_cookie_file();

$keyword = 'residency personal statement writing services';
$country = 'countryUS';
$language = 'lang_en';

$max_pages = 10;
$minutes_to_sleep_on_captcha = 15;

$url = 'http://www.google.com/';
$html = get_html($url, $ua, $cookie);

if (!intval($html)) {
    $htmls = array();
    $errors_count = 0;
    sleep(5);

    for($page = 1; $page <= $max_pages; $page++) {
        $referrer = $url;
        $url = get_search_url($keyword, $country, $language, $page);

        $html = get_html($url, $ua, $cookie, $referrer);
        if (!intval($html)) {
            $htmls[] = $html;
        } else {
            echo $html . ' - ' . $url . PHP_EOL;
            $errors_count++;
        }
        sleep(5);
    }

    echo count($htmls) . ' domains fetched from ' . (10 - $errors_count) . ' pages' . PHP_EOL;
    echo $errors_count . ' errors' . PHP_EOL;

    if($errors_count == $max_pages) {
        echo 'Probably captcha' . PHP_EOL;
        sleep($minutes_to_sleep_on_captcha * 60);
        //TODO: notify about captcha
    }


} else {
    echo 'Can not open google.com ' . $html . PHP_EOL;
    if($html == 503) {
        echo 'Probably captcha' . PHP_EOL;
        sleep($minutes_to_sleep_on_captcha * 60);
        //TODO: notify about captcha
    }
}

$end = microtime(true);

echo PHP_EOL . PHP_EOL . "TIME TAKEN: " . round($end - $start) . " SECONDS";