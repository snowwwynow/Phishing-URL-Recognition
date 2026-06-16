# В этом файле собранны все извлеченные признаки из URL, которое вводит пользователь
# длина URL
# количесвто тире в домене
# количесвто поддоменов
# наличие http или https
# глубина пути
# энтропия домена
 

def URL_PRIZNAKI(url):
    from urllib.parse import urlparse
    import math
    from collections import Counter

    try:
        url_chasti = urlparse(url)

        dlina = len(url) # длина URL
        coun_ture = url_chasti.netloc.count("-") # количесвто тире в домене

        # количесвто поддоменов
        def count_of_subdom (url_chasti):
            count_sbdmn = url_chasti.netloc
            split_subdmn = count_sbdmn.split(".")
            if len(split_subdmn) > 2:
                return len(split_subdmn) - 2
            else:
                return 0

        subdom = count_of_subdom(url_chasti)

        # наличие http или https
        def http_or_https (url_chasti):
            try:
                protocol = url_chasti.scheme
                return 1 if protocol == "http" else 0
            except AttributeError:
                return 0
    
        http_https = http_or_https(url_chasti)

        # глубина пути
        def glbn_pytu (url_chasti):
            try:
                path = url_chasti.path
                if not path or path == "/":
                    return 0
                segment_path = [i for i in path.split("/") if i]
                return len(segment_path)
            except AttributeError:
                return 0

        pyt = glbn_pytu(url_chasti)

        # энтропия домена

        def entropy (url_chasti):
            try:
                dmen = url_chasti.netloc
                if not dmen:
                    return 0.0
                dlin_dmen = len(dmen)
                chastota_simvlv_domena = Counter(dmen)
                entropy = 0.0
                for i in chastota_simvlv_domena.values():
                    veroatnost = i / dlin_dmen
                    entropy -= veroatnost * math.log2(veroatnost)
                return round(entropy, 3)
            except AttributeError:
                return 0.0
            
        entropy_dmn = entropy(url_chasti)

        return [dlina,coun_ture, subdom, http_https, pyt, entropy_dmn]
    
    except Exception as e:
        print("Ошибка при обработке URL:", e)
        return [0,0,0,0,0,0]
