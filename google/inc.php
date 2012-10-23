<?php
function get_random_user_agent()
{
    $useragents = explode(PHP_EOL, file_get_contents('useragent.txt'));
    shuffle($useragents);
    return array_shift($useragents);
}

function get_cookie_file()
{
    return tempnam(sys_get_temp_dir(), 'cookie');
}

/**
 * Get html of desired url
 *
 * @param $url - url to retrieve
 * @param null $ua - user agent to use
 * @param null $cookie - cookies magic
 * @param null $referrer - use specified referrer
 * @param null $proxy_host - host name or ip address of proxy
 * @param null $proxy_port - port to use
 * @param null $proxy_user - user name
 * @param null $proxy_pass - password
 * @return mixed
 */
function get_html($url, $ua = null, $cookie = null, $referrer = null, $proxy_host = null, $proxy_port = null, $proxy_user = null, $proxy_pass = null)
{
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_AUTOREFERER, TRUE);

    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_HEADER, FALSE);
    curl_setopt($ch, CURLOPT_COOKIESESSION, TRUE);

    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);

    curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, TRUE);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, FALSE);

    if ($ua) curl_setopt($ch, CURLOPT_USERAGENT, $ua);
    if ($cookie) {
        curl_setopt($ch, CURLOPT_COOKIEJAR, $cookie);
        curl_setopt($ch, CURLOPT_COOKIEFILE, $cookie);
    }
    if ($referrer) curl_setopt($ch, CURLOPT_REFERER, $referrer);

    if ($proxy_host) curl_setopt($ch, CURLOPT_PROXY, $proxy_host);
    if ($proxy_port) curl_setopt($ch, CURLOPT_PROXYPORT, $proxy_port);
    if ($proxy_user && $proxy_pass) curl_setopt($ch, CURLOPT_PROXYUSERPWD, $proxy_user . ':' . $proxy_pass);

    $html = curl_exec($ch);
    $http_status = curl_getinfo($ch, CURLINFO_HTTP_CODE);

    return $http_status == 200 ? $html : $http_status;
}

function get_search_url($keyword, $country = 'countryUS', $language = 'lang_en', $page = 1) {
    $url = 'http://www.google.com/search?q=' . urlencode($keyword) . '&hl=en&lr=' . $language . '&cr=' . $country;
    if($page > 1) $url = $url . '&start=' . (($page - 1) * 10);
    return $url;
}

function parse_google_page__get_links($html, $xpath_query) {
    $links = array();
    $dom = new DOMDocument();
    @$dom->loadHTML($html);
    $dom_xpath = new DOMXPath($dom);
    $dom_nodes = $dom_xpath->query($xpath_query);
    $counter = 1;
    foreach ($dom_nodes as $node) {
        $link = $node->getAttribute('href');
        $links[] = $link;
    }

    return $links;
}
