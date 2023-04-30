import re

url_list = [
    "https://solicitud.vexi.mx/?codRef=10960&utmID=Destacame&utm_source=email&utm_format=email&utm_medium=emm_new&utm_campaign=mailing",
    "https://kueski.com/prestamos-sin-buro?utm_source=dseodw&utm_medium=p_mlg&utm_campaign=pybxot&utm_term=ppg&utm_content=nh",
    "https://www.americanexpress.com/es-mx/credit-cards/apply/personal/gold-grcc?sourcecode=A0000FEKHJ&cpid=100476432&intlink=GoldEliteDestacameMarzo22EMM",
    "https://informes.kubofinanciero.com/prestamos?utm_source=destacame&utm_medium=mail&utm_campaign=destacamemailing",
    "https://registro.curadeuda.com/destacame/?&qb_fuente=109&qb_campaign=162",
    "https://app.destacame.cl/debts/pad",
    "https://www.vivus.com.mx/?ref_id=63581115ce0e7d00014478b4&affiliate_name=Destacame+mailing",
    "https://app.destacame.cl/debts/pad",
    "https://app.destacame.cl/debts/pad",
    "https://app.destacame.cl/debts/pad",
    "https://app.destacame.cl/debts/pad",
    "https://app.destacame.cl/debts/pad",
    "https://castor.app/?source=destacamemailing",
    "https://openmarket.bbva.mx/tarjetadecredito/",
    "https://creditea.mx/?utm_source=DestacameEmailingPremium&utm_medium=affiliate&utm_campaign=cpl__21&utm_content=mx_es___broad",
    "https://creditea.mx/?utm_source=DestacameEmailingBasico&utm_medium=affiliate&utm_campaign=cpl__21&utm_content=mx_es___broad",
    "https://app.destacame.cl/debts/pad",
    "https://app.destacame.cl/debts/pad",
    "https://app.destacame.cl/debts/pad",
    "https://app.destacame.cl/debts/pad",
    "https://app.destacame.cl/debts/pad",
    "https://app.destacame.cl/debts/pad/",
    "https://informes.kubofinanciero.com/prestamos?utm_source=destacame&utm_medium=mail&utm_campaign=destacamemailing",
    "https://bs.serving-sys.com/Serving/adServer.bs?cn=trd&pli=1077502978&gdpr=${GDPR}&gdpr_consent=${GDPR_CONSENT_68}&adid=1085947442&ord=[timestamp]",
    "https://www.vivus.com.mx/?ref_id=63581115ce0e7d00014478b4&affiliate_name=Destacame+mailing",
    "https://www.americanexpress.com/es-mx/credit-cards/apply/personal/gold-grcc?sourcecode=A0000FEKHJ&cpid=100476432&intlink=GoldEliteDestacameMarzo22EMM",
    "https://registro.curadeuda.com/destacame/?&qb_fuente=109&qb_campaign=162",
    "https://kueski.com/prestamos-sin-buro?utm_source=dseodw&utm_medium=p_mlg&utm_campaign=pybxot&utm_term=ppg&utm_content=nh",
    "https://solicitud.vexi.mx/?codRef=10960&utmID=Destacame&utm_source=email&utm_format=email&utm_medium=emm_new&utm_campaign=mailing",
    "https://creditea.mx/?utm_source=DestacameEmail&utm_medium=affiliate&utm_campaign=cpa__21&utm_content=mx_es___broad",
    "https://bs.serving-sys.com/Serving/adServer.bs?cn=trd&pli=1078831564&gdpr=${GDPR}&gdpr_consent=${GDPR_CONSENT_68}&us_privacy=${US_PRIVACY}&adid=1089403745&ord=[timestamp]",
    "https://solicitud.vexi.mx/?codRef=10960&utmID=Destacame&utm_source=email&utm_format=email&utm_medium=emm_new&utm_campaign=mailing",
]

url_regex = r"(?i)\b((?:[a-z][\w-]+:(?:\/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}\/)(?:[^\s()<>]+|\((?:[^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\((?:[^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’$]))"

for url in url_list:
    if re.match(url_regex, url):
        print(f"Valid URL: {url}")
    else:
        print(f"Invalid URL: {url}")
