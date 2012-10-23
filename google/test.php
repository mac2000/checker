<?php
/*
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, 'https://www.google.com.ua/search?num=100&hl=ru&as_q=hello+world&as_epq=&as_oq=&as_eq=&as_nlo=&as_nhi=&lr=&cr=&as_qdr=all&as_sitesearch=&as_occt=any&safe=images&as_filetype=&as_rights=&count=100#num=100&hl=ru&lr=&as_qdr=all&q=hello+world&oq=hello+world&gs_l=serp.3..0l10.3039.4306.0.4380.11.10.0.1.1.0.180.1175.3j6.9.0...0.0...1c.1._4WTQtGT5Wc&pbx=1&fp=1&biw=1183&bih=737&bav=on.2,or.r_gc.r_pw.r_cp.&cad=b&sei=j9RiUNajO8jIswal6oEI');
curl_setopt($ch, CURLOPT_HEADER, false);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 30);
curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729)');
$data = curl_exec($ch);
curl_close($ch);
echo $data;
*/

$ch = curl_init("https://www.google.com.ua/search?q=buy+resume+online+in+new+york&sugexp=chrome,mod=13&sourceid=chrome&ie=UTF-8");
//$ch = curl_init("http://my-ip-address.com/");

curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.1) Gecko/20061204 Firefox/2.0.0.1");
curl_setopt($ch, CURLOPT_REFERER, "https://www.google.com.ua");
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, TRUE);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
curl_setopt($ch, CURLOPT_PROXY, "174.122.73.120");
curl_setopt($ch, CURLOPT_PROXYPORT, 3128);
curl_setopt ($ch, CURLOPT_PROXYUSERPWD, "ip3:ohzahnohdohnuyoseeph");
$x = curl_exec($ch);
print "page:" . $x . curl_error($ch) ;
curl_close($ch);