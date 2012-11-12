#!/usr/bin/env python
#-*- conding: utf-8 -*-

def google(keyword, page = 1, language = 'lang_en', country = 'countryUS', proxy = None, ua = None, cookie = None, verbose = True):
    from fetch import fetch

    url = "http://www.google.com/search?q=%s&hl=en&lr=%s&cr=%s" % (keyword, language, country)
    if page > 1:
        url = "%s&start=%d" % (url, 10 * (page - 1))

    return fetch(url, proxy, ua, cookie, verbose)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description = 'Fetch google search results')
    parser.add_argument('keyword', help = 'Keyword to search')

    parser.add_argument('-q', '--quiet', dest = 'verbose', action = 'store_false', help = 'Toggle output verbose')
    parser.add_argument('-a', '--useragent', dest = 'ua', action = 'store', help = 'User agent to use')
    parser.add_argument('-c', '--cookie', dest = 'cookie', action = 'store', help = 'Cookies file path to use')
    parser.add_argument('-p', '--proxy', dest = 'proxy', action = 'store', help = 'Proxy to use')

    parser.add_argument('--page', default = 1, type = int, dest = 'page', action = 'store', help = 'Page to search')

    parser.add_argument('--language', action='store', dest='language', choices=[
            'lang_af', 'lang_ar', 'lang_hy', 'lang_be',
            'lang_bg', 'lang_ca', 'lang_zh-CN', 'lang_zh-TW',
            'lang_hr', 'lang_cs', 'lang_da', 'lang_nl',
            'lang_en', 'lang_eo', 'lang_et', 'lang_tl',
            'lang_fi', 'lang_fr', 'lang_de', 'lang_el',
            'lang_iw', 'lang_hi', 'lang_hu', 'lang_is',
            'lang_id', 'lang_it', 'lang_ja', 'lang_ko',
            'lang_lv', 'lang_lt', 'lang_no', 'lang_fa',
            'lang_pl', 'lang_pt', 'lang_ro', 'lang_ru',
            'lang_sr', 'lang_sk', 'lang_sl', 'lang_es',
            'lang_sw', 'lang_sv', 'lang_th', 'lang_tr',
            'lang_uk', 'lang_vi'
        ], default='lang_en', help='Language to search in')
    parser.add_argument('--country', action='store', 
            choices=[
                'countryAF', 'countryAL', 'countryDZ', 'countryAS',
                'countryAD', 'countryAO', 'countryAI', 'countryAQ',
                'countryAG', 'countryAR', 'countryAM', 'countryAW',
                'countryAU', 'countryAT', 'countryAZ', 'countryBS',
                'countryBH', 'countryBD', 'countryBB', 'countryBY',
                'countryBE', 'countryBZ', 'countryBJ', 'countryBM',
                'countryBT', 'countryBO', 'countryBA', 'countryBW',
                'countryBV', 'countryBR', 'countryIO', 'countryVG',
                'countryBN', 'countryBG', 'countryBF', 'countryBI',
                'countryKH', 'countryCM', 'countryCA', 'countryCV',
                'countryKY', 'countryCF', 'countryTD', 'countryCL',
                'countryCN', 'countryCX', 'countryCC', 'countryCO',
                'countryKM', 'countryCD', 'countryCG', 'countryCK',
                'countryCR', 'countryCI', 'countryHR', 'countryCU',
                'countryCY', 'countryCZ', 'countryDK', 'countryDJ',
                'countryDM', 'countryDO', 'countryEC', 'countryEG',
                'countrySV', 'countryGQ', 'countryER', 'countryEE',
                'countryET', 'countryFK', 'countryFO', 'countryFJ',
                'countryFI', 'countryFR', 'countryGF', 'countryPF',
                'countryTF', 'countryGA', 'countryGM', 'countryGE',
                'countryDE', 'countryGH', 'countryGI', 'countryGR',
                'countryGL', 'countryGD', 'countryGP', 'countryGU',
                'countryGT', 'countryGN', 'countryGW', 'countryGY',
                'countryHT', 'countryHM', 'countryHN', 'countryHK',
                'countryHU', 'countryIS', 'countryIN', 'countryID',
                'countryIR', 'countryIQ', 'countryIE', 'countryIL',
                'countryIT', 'countryJM', 'countryJP', 'countryJO',
                'countryKZ', 'countryKE', 'countryKI', 'countryKW',
                'countryKG', 'countryLA', 'countryLV', 'countryLB',
                'countryLS', 'countryLR', 'countryLY', 'countryLI',
                'countryLT', 'countryLU', 'countryMO', 'countryMK',
                'countryMG', 'countryMW', 'countryMY', 'countryMV',
                'countryML', 'countryMT', 'countryMH', 'countryMQ',
                'countryMR', 'countryMU', 'countryYT', 'countryMX',
                'countryFM', 'countryMD', 'countryMC', 'countryMN',
                'countryMS', 'countryMA', 'countryMZ', 'countryMM',
                'countryNA', 'countryNR', 'countryNP', 'countryNL',
                'countryNC', 'countryNZ', 'countryNI', 'countryNE',
                'countryNG', 'countryNU', 'countryNF', 'countryKP',
                'countryMP', 'countryNO', 'countryOM', 'countryPK',
                'countryPW', 'countryPS', 'countryPA', 'countryPG',
                'countryPY', 'countryPE', 'countryPH', 'countryPN',
                'countryPL', 'countryPT', 'countryPR', 'countryQA',
                'countryRE', 'countryRO', 'countryRU', 'countryRW',
                'countrySH', 'countryKN', 'countryLC', 'countryPM',
                'countryVC', 'countryWS', 'countrySM', 'countryST',
                'countrySA', 'countrySN', 'countryRS', 'countrySC',
                'countrySL', 'countrySG', 'countrySK', 'countrySI',
                'countrySB', 'countrySO', 'countryZA', 'countryGS',
                'countryKR', 'countryES', 'countryLK', 'countrySD',
                'countrySR', 'countrySJ', 'countrySZ', 'countrySE',
                'countryCH', 'countrySY', 'countryTW', 'countryTJ',
                'countryTZ', 'countryTH', 'countryTG', 'countryTK',
                'countryTO', 'countryTT', 'countryTN', 'countryTR',
                'countryTM', 'countryTC', 'countryTV', 'countryUM',
                'countryVI', 'countryUG', 'countryUA', 'countryAE',
                'countryGB', 'countryUS', 'countryUY', 'countryUZ',
                'countryVU', 'countryVA', 'countryVE', 'countryVN',
                'countryWF', 'countryEH', 'countryYE', 'countryZM',
                'countryZW'
                ], dest='country', default='countryUS', help='Country to search in')

    args = parser.parse_args()
    if not args.keyword:
        parser.error('Keyword not given')

    response = google(args.keyword, args.page, args.language, args.country, args.proxy, args.ua, args.cookie, args.verbose)

    if response['status'] is 200:
        print response['response']
    else:
        print response
