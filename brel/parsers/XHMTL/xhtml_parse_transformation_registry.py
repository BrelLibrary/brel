from optparse import Option
from typing import Optional
from convertdate import indian_civil
import datetime
import re
from lxml.etree import _Element

from brel.data.errors.error_repository import ErrorRepository
from brel.errors.error_code import ErrorCode


number_format_to_regex = {
    "ixt:num-comma-decimal-apos": r"^([\.\'`´’′  0-9]*)(,[  0-9]+)?$",
    "ixt:num-dot-decimal-apos": r"^([,\'`´’′  0-9]*)(\.[  0-9]+)?$",
    "ixt:num-unit-decimal-apos": r"^([0-9０-９\.,，\'`´’′＇]+)[^0-9０-９\.,，\'`´’′＇][^0-9０-９]*([0-9０-９]{1,2})[^0-9０-９]*$",
    "ixt:num-comma-decimal": r"^([\.  0-9]*)(,[  0-9]+)?$",
    "ixt:num-dot-decimal": r"^([,  0-9]*)(\.[  0-9]+)?$",
    "ixt:num-unit-decimal": r"^([0-9０-９\.,，]+)[^0-9０-９\.,，][^0-9０-９]*([0-9０-９]{1,2})[^0-9０-９]*$",
}

date_format_to_regex = {
    "ixt:date-day-monthname-cy": r"^([0-9]{1,2})[^0-9]*[^0-9a-zA-Z]+(ion|chwe|maw|ebr|mai|meh|gor|aws|med|hyd|tach|rhag|ION|CHWE|MAW|EBR|MAI|MEH|GOR|AWS|MED|HYD|TACH|RHAG|Ion|Chwe|Maw|Ebr|Mai|Meh|Gor|Aws|Med|Hyd|Tach|Rhag)[^0-9]{0,7}$",
    "ixt:date-monthname-year-cy": r"^(ion|chwe|maw|faw|ebr|mai|fai|meh|feh|gor|ngor|aws|med|fed|hyd|tach|dach|nhach|thach|rhag|rag|ION|CHWE|MAW|FAW|EBR|MAI|FAI|MEH|FEH|GOR|NGOR|AWS|MED|FED|HYD|TACH|DACH|NHACH|THACH|RHAG|RAG|Ion|Chwe|Maw|Faw|Ebr|Mai|Fai|Meh|Feh|Gor|Ngor|Aws|Med|Fedi|Hyd|Tach|Dach|Nhach|Thach|Rhag|Rag)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-day-monthname-year-cy": r"^([0-9]{1,2})[^0-9]*[^0-9a-zA-Z]+(ion|chwe|maw|ebr|mai|meh|gor|aws|med|hyd|tach|rhag|ION|CHWE|MAW|EBR|MAI|MEH|GOR|AWS|MED|HYD|TACH|RHAG|Ion|Chwe|Maw|Ebr|Mai|Meh|Gor|Aws|Med|Hyd|Tach|Rhag)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-day-month": r"^([0-9]{1,2})[^0-9]+([0-9]{1,2})$",
    "ixt:date-month-day": r"^([0-9]{1,2})[^0-9]+([0-9]{1,2})$",
    "ixt:date-day-month-year": r"^([0-9०-९]{1,2})[^0-9०-९]+([0-9०-९]{1,2})[^0-9०-९]+([0-9०-९]{1,2}|[0-9०-९]{4})$",  # indian numerals
    "ixt:date-month-day-year": r"^([0-9]{1,2})[^0-9]+([0-9]{1,2})[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-year-month-day": r"^([0-9０-９]{1,2}|[0-9０-９]{4})[^0-9０-９]+([0-9０-９]{1,2})[^0-9０-９]+([0-9０-９]{1,2})[^0-9０-９]*$",  # japanese numerals
    "ixt:date-year-month": r"^([0-9０-９]{1,2}|[0-9０-９]{4})[^0-9０-９]+([0-9０-９]{1,2})[^0-9０-９]*$",  # japanese numerals
    "ixt:date-month-year": r"^([0-9०-९]{1,2})[^0-9०-९]+([0-9०-९]{1,2}|[0-9०-९]{4})$",  # indian numerals
    "ixt:date-day-monthname-bg": r"^([0-9]{1,2})[^0-9]+(ян|фев|мар|апр|май|маи|юни|юли|авг|сеп|окт|ное|дек|ЯН|ФЕВ|МАР|АПР|МАЙ|МАИ|ЮНИ|ЮЛИ|АВГ|СЕП|ОКТ|НОЕ|ДЕК|Ян|Фев|Мар|Апр|Май|Маи|Юни|Юли|Авг|Сеп|Окт|Ное|Дек)[^0-9]{0,6}$",
    "ixt:date-day-monthname-year-bg": r"^([0-9]{1,2})[^0-9]+(ян|фев|мар|апр|май|маи|юни|юли|авг|сеп|окт|ное|дек|ЯН|ФЕВ|МАР|АПР|МАЙ|МАИ|ЮНИ|ЮЛИ|АВГ|СЕП|ОКТ|НОЕ|ДЕК|Ян|Фев|Мар|Апр|Май|Маи|Юни|Юли|Авг|Сеп|Окт|Ное|Дек)[^0-9]+([0-9]{1,2}|[0-9]{4})[^0-9]*$",
    "ixt:date-monthname-year-bg": r"^(ян|фев|мар|апр|май|маи|юни|юли|авг|сеп|окт|ное|дек|ЯН|ФЕВ|МАР|АПР|МАЙ|МАИ|ЮНИ|ЮЛИ|АВГ|СЕП|ОКТ|НОЕ|ДЕК|Ян|Фев|Мар|Апр|Май|Маи|Юни|Юли|Авг|Сеп|Окт|Ное|Дек)[^0-9]+([0-9]{1,2}|[0-9]{4})[^0-9]*$",
    "ixt:date-day-monthname-cs": r"^([0-9]{1,2})[^0-9]+(ledna|února|unora|března|brezna|dubna|května|kvetna|června|cervna|července|cervence|srpna|září|zari|října|rijna|listopadu|prosince|led|úno|uno|bře|bre|dub|kvě|kve|čvn|cvn|čvc|cvc|srp|zář|zar|říj|rij|lis|pro|LEDNA|ÚNORA|UNORA|BŘEZNA|BREZNA|DUBNA|KVĚTNA|KVETNA|ČERVNA|CERVNA|ČERVENCE|CERVENCE|SRPNA|ZÁŘÍ|ZARI|ŘÍJNA|RIJNA|LISTOPADU|PROSINCE|LED|ÚNO|UNO|BŘE|BRE|DUB|KVĚ|KVE|ČVN|CVN|ČVC|CVC|SRP|ZÁŘ|ZAR|ŘÍJ|RIJ|LIS|PRO|Ledna|Února|Unora|Března|Brezna|Dubna|Května|Kvetna|Června|Cervna|Července|Cervence|Srpna|Září|Zari|Října|Rijna|Listopadu|Prosince|Led|Úno|Uno|Bře|Bre|Dub|Kvě|Kve|Čvn|Cvn|Čvc|Cvc|Srp|Zář|Zar|Říj|Rij|Lis|Pro)\.?$",
    "ixt:date-day-monthname-year-cs": r"^([0-9]{1,2})[^0-9]+(ledna|února|unora|března|brezna|dubna|května|kvetna|června|cervna|července|cervence|srpna|září|zari|října|rijna|listopadu|prosince|led|úno|uno|bře|bre|dub|kvě|kve|čvn|cvn|čvc|cvc|srp|zář|zar|říj|rij|lis|pro|LEDNA|ÚNORA|UNORA|BŘEZNA|BREZNA|DUBNA|KVĚTNA|KVETNA|ČERVNA|CERVNA|ČERVENCE|CERVENCE|SRPNA|ZÁŘÍ|ZARI|ŘÍJNA|RIJNA|LISTOPADU|PROSINCE|LED|ÚNO|UNO|BŘE|BRE|DUB|KVĚ|KVE|ČVN|CVN|ČVC|CVC|SRP|ZÁŘ|ZAR|ŘÍJ|RIJ|LIS|PRO|Ledna|Února|Unora|Března|Brezna|Dubna|Května|Kvetna|Června|Cervna|Července|Cervence|Srpna|Září|Zari|Října|Rijna|Listopadu|Prosince|Led|Úno|Uno|Bře|Bre|Dub|Kvě|Kve|Čvn|Cvn|Čvc|Cvc|Srp|Zář|Zar|Říj|Rij|Lis|Pro)[^0-9a-zA-Z]+[^0-9]*([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-monthname-year-cs": r"^(leden|ledna|lednu|únor|unor|února|unora|únoru|unoru|březen|brezen|března|brezna|březnu|breznu|duben|dubna|dubnu|květen|kveten|května|kvetna|květnu|kvetnu|červen|cerven|června|cervna|červnu|cervnu|červenec|cervenec|července|cervence|červenci|cervenci|srpen|srpna|srpnu|září|zari|říjen|rijen|října|rijna|říjnu|rijnu|listopad|listopadu|prosinec|prosince|prosinci|led|úno|uno|bře|bre|dub|kvě|kve|čvn|cvn|čvc|cvc|srp|zář|zar|říj|rij|lis|pro|LEDEN|LEDNA|LEDNU|ÚNOR|UNOR|ÚNORA|UNORA|ÚNORU|UNORU|BŘEZEN|BREZEN|BŘEZNA|BREZNA|BŘEZNU|BREZNU|DUBEN|DUBNA|DUBNU|KVĚTEN|KVETEN|KVĚTNA|KVETNA|KVĚTNU|KVETNU|ČERVEN|CERVEN|ČERVNA|CERVNA|ČERVNU|CERVNU|ČERVENEC|CERVENEC|ČERVENCE|CERVENCE|ČERVENCI|CERVENCI|SRPEN|SRPNA|SRPNU|ZÁŘÍ|ZARI|ŘÍJEN|RIJEN|ŘÍJNA|RIJNA|ŘÍJNU|RIJNU|LISTOPAD|LISTOPADU|PROSINEC|PROSINCE|PROSINCI|LED|ÚNO|UNO|BŘE|BRE|DUB|KVĚ|KVE|ČVN|CVN|ČVC|CVC|SRP|ZÁŘ|ZAR|ŘÍJ|RIJ|LIS|PRO|Leden|Ledna|Lednu|Únor|Unor|Února|Unora|Únoru|Unoru|Březen|Brezen|Března|Brezna|Březnu|Breznu|Duben|Dubna|Dubnu|Květen|Kveten|Května|Kvetna|Květnu|Kvetnu|Červen|Cerven|Června|Cervna|Červnu|Cervnu|Červenec|Cervenec|Července|Cervence|Červenci|Cervenci|Srpen|Srpna|Srpnu|Září|Zari|Říjen|Rijen|Října|Rijna|Říjnu|Rijnu|Listopad|Listopadu|Prosinec|Prosince|Prosinci|Led|Úno|Uno|Bře|Bre|Dub|Kvě|Kve|Čvn|Cvn|Čvc|Cvc|Srp|Zář|Zar|Říj|Rij|Lis|Pro)[^0-9a-zA-Z]+[^0-9]*([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-day-monthname-da": r"^([0-9]{1,2})[^0-9]+(jan|feb|mar|apr|maj|jun|jul|aug|sep|okt|nov|dec|JAN|FEB|MAR|APR|MAJ|JUN|JUL|AUG|SEP|OKT|NOV|DEC|Jan|Feb|Mar|Apr|Maj|Jun|Jul|Aug|Sep|Okt|Nov|Dec)[^0-9]{0,6}$",
    "ixt:date-day-monthname-year-da": r"^([0-9]{1,2})[^0-9]+(jan|feb|mar|apr|maj|jun|jul|aug|sep|okt|nov|dec|JAN|FEB|MAR|APR|MAJ|JUN|JUL|AUG|SEP|OKT|NOV|DEC|Jan|Feb|Mar|Apr|Maj|Jun|Jul|Aug|Sep|Okt|Nov|Dec)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-monthname-year-da": r"^(jan|feb|mar|apr|maj|jun|jul|aug|sep|okt|nov|dec|JAN|FEB|MAR|APR|MAJ|JUN|JUL|AUG|SEP|OKT|NOV|DEC|Jan|Feb|Mar|Apr|Maj|Jun|Jul|Aug|Sep|Okt|Nov|Dec)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-day-monthname-de": r"^([0-9]{1,2})[^0-9]+(jan|feb|mar|apr|maj|jun|jul|aug|sep|okt|nov|dec|JAN|FEB|MAR|APR|MAJ|JUN|JUL|AUG|SEP|OKT|NOV|DEC|Jan|Feb|Mar|Apr|Maj|Jun|Jul|Aug|Sep|Okt|Nov|Dec)[^0-9]{0,6}$",
    "ixt:date-day-monthname-year-de": r"^([0-9]{1,2})[^0-9]+(jan|feb|mar|apr|maj|jun|jul|aug|sep|okt|nov|dec|JAN|FEB|MAR|APR|MAJ|JUN|JUL|AUG|SEP|OKT|NOV|DEC|Jan|Feb|Mar|Apr|Maj|Jun|Jul|Aug|Sep|Okt|Nov|Dec)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-monthname-year-de": r"^(jan|feb|mar|apr|maj|jun|jul|aug|sep|okt|nov|dec|JAN|FEB|MAR|APR|MAJ|JUN|JUL|AUG|SEP|OKT|NOV|DEC|Jan|Feb|Mar|Apr|Maj|Jun|Jul|Aug|Sep|Okt|Nov|Dec)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-day-monthname-el": r"^([0-9]{1,2})[^0-9]+(ιαν|ίαν|φεβ|μάρ|μαρ|απρ|άπρ|αρίλ|άρίλ|αριλ|άριλ|μαΐ|μαι|μάι|μαϊ|μάϊ|ιούν|ίούν|ίουν|ιουν|ιούλ|ίούλ|ίουλ|ίουλ|ιουλ|αύγ|αυγ|σεπ|οκτ|όκτ|νοέ|νοε|δεκ|ΙΑΝ|ΊΑΝ|IΑΝ|ΦΕΒ|ΜΆΡ|ΜΑΡ|ΑΠΡ|ΆΠΡ|AΠΡ|AΡΙΛ|ΆΡΙΛ|ΑΡΙΛ|ΜΑΪ́|ΜΑΙ|ΜΆΙ|ΜΑΪ|ΜΆΪ|ΙΟΎΝ|ΊΟΎΝ|ΊΟΥΝ|IΟΥΝ|ΙΟΥΝ|IΟΥΝ|ΙΟΎΛ|ΊΟΎΛ|ΊΟΥΛ|IΟΎΛ|ΙΟΥΛ|IΟΥΛ|ΑΎΓ|ΑΥΓ|ΣΕΠ|ΟΚΤ|ΌΚΤ|OΚΤ|ΝΟΈ|ΝΟΕ|ΔΕΚ|Ιαν|Ίαν|Iαν|Φεβ|Μάρ|Μαρ|Απρ|Άπρ|Aπρ|Αρίλ|Άρίλ|Aρίλ|Aριλ|Άριλ|Αριλ|Μαΐ|Μαι|Μάι|Μαϊ|Μάϊ|Ιούν|Ίούν|Ίουν|Iούν|Ιουν|Iουν|Ιούλ|Ίούλ|Ίουλ|Iούλ|Ιουλ|Iουλ|Αύγ|Αυγ|Σεπ|Οκτ|Όκτ|Oκτ|Νοέ|Νοε|Δεκ)[^0-9]{0,8}$",
    "ixt:date-day-monthname-year-el": r"^([0-9]{1,2})[^0-9]+(ιαν|ίαν|φεβ|μάρ|μαρ|απρ|άπρ|αρίλ|άρίλ|αριλ|άριλ|μαΐ|μαι|μάι|μαϊ|μάϊ|ιούν|ίούν|ίουν|ιουν|ιούλ|ίούλ|ίουλ|ίουλ|ιουλ|αύγ|αυγ|σεπ|οκτ|όκτ|νοέ|νοε|δεκ|ΙΑΝ|ΊΑΝ|IΑΝ|ΦΕΒ|ΜΆΡ|ΜΑΡ|ΑΠΡ|ΆΠΡ|AΠΡ|AΡΙΛ|ΆΡΙΛ|ΑΡΙΛ|ΜΑΪ́|ΜΑΙ|ΜΆΙ|ΜΑΪ|ΜΆΪ|ΙΟΎΝ|ΊΟΎΝ|ΊΟΥΝ|IΟΎΝ|ΙΟΥΝ|IΟΥΝ|ΙΟΎΛ|ΊΟΎΛ|ΊΟΥΛ|IΟΎΛ|ΙΟΥΛ|IΟΥΛ|ΑΎΓ|ΑΥΓ|ΣΕΠ|ΟΚΤ|ΌΚΤ|OΚΤ|ΝΟΈ|ΝΟΕ|ΔΕΚ|Ιαν|Ίαν|Iαν|Φεβ|Μάρ|Μαρ|Απρ|Άπρ|Aπρ|Αρίλ|Άρίλ|Aρίλ|Aριλ|Άριλ|Αριλ|Μαΐ|Μαι|Μάι|Μαϊ|Μάϊ|Ιούν|Ίούν|Ίουν|Iούν|Ιουν|Iουν|Ιούλ|Ίούλ|Ίουλ|Iούλ|Ιουλ|Iουλ|Αύγ|Αυγ|Σεπ|Οκτ|Όκτ|Oκτ|Νοέ|Νοε|Δεκ)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-monthname-year-el": r"^(ιαν|ίαν|φεβ|μάρ|μαρ|απρ|άπρ|αρίλ|άρίλ|αριλ|άριλ|μαΐ|μαι|μάι|μαϊ|μάϊ|ιούν|ίούν|ίουν|ιουν|ιούλ|ίούλ|ίουλ|ίουλ|ιουλ|αύγ|αυγ|σεπ|οκτ|όκτ|νοέ|νοε|δεκ|ΙΑΝ|ΊΑΝ|IΑΝ|ΦΕΒ|ΜΆΡ|ΜΑΡ|ΑΠΡ|ΆΠΡ|AΠΡ|AΡΙΛ|ΆΡΙΛ|ΑΡΙΛ|ΜΑΪ́|ΜΑΙ|ΜΆΙ|ΜΑΪ|ΜΆΪ|ΙΟΎΝ|ΊΟΎΝ|ΊΟΥΝ|IΟΎΝ|ΙΟΥΝ|IΟΥΝ|ΙΟΎΛ|ΊΟΎΛ|ΊΟΥΛ|IΟΎΛ|ΙΟΥΛ|IΟΥΛ|ΑΎΓ|ΑΥΓ|ΣΕΠ|ΟΚΤ|ΌΚΤ|OΚΤ|ΝΟΈ|ΝΟΕ|ΔΕΚ|Ιαν|Ίαν|Iαν|Φεβ|Μάρ|Μαρ|Απρ|Άπρ|Aπρ|Αρίλ|Άρίλ|Aρίλ|Aριλ|Άριλ|Αριλ|Μαΐ|Μαι|Μάι|Μαϊ|Μάϊ|Ιούν|Ίούν|Ίουν|Iούν|Ιουν|Iουν|Ιούλ|Ίούλ|Ίουλ|Iούλ|Ιουλ|Iουλ|Αύγ|Αυγ|Σεπ|Οκτ|Όκτ|Oκτ|Νοέ|Νοε|Δεκ)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-day-monthname-en": r"^([0-9]{1,2})[^0-9]+(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)$",
    "ixt:date-day-monthname-year-en": r"^([0-9]{1,2})[^0-9]+(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-monthname-day-en": r"^(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)[^0-9]+([0-9]{1,2})[a-zA-Z]{0,2}$",
    "ixt:date-monthname-day-year-en": r"^(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)[^0-9]+([0-9]{1,2})[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-monthname-year-en": r"^(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-year-monthname-en": r"^([0-9]{1,2}|[0-9]{4})[^0-9]+(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)$",
    "ixt:date-day-monthname-es": r"^([0-9]{1,2})[^0-9]+(ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic|ENE|FEB|MAR|ABR|MAY|JUN|JUL|AGO|SEP|OCT|NOV|DIC|Ene|Feb|Mar|Abr|May|Jun|Jul|Ago|Sep|Oct|Nov|Dic)[^0-9]{0,7}$",
    "ixt:date-day-monthname-year-es": r"^([0-9]{1,2})[^0-9]+(ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic|ENE|FEB|MAR|ABR|MAY|JUN|JUL|AGO|SEP|OCT|NOV|DIC|Ene|Feb|Mar|Abr|May|Jun|Jul|Ago|Sep|Oct|Nov|Dic)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-monthname-year-es": r"^(ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic|ENE|FEB|MAR|ABR|MAY|JUN|JUL|AGO|SEP|OCT|NOV|DIC|Ene|Feb|Mar|Abr|May|Jun|Jul|Ago|Sep|Oct|Nov|Dic)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-day-monthname-et": r"^([0-9]{1,2})[^0-9]+(jaan|veebr|märts|marts|apr|mai|juuni|juuli|aug|sept|okt|nov|dets|JAAN|VEEBR|MÄRTS|MARTS|APR|MAI|JUUNI|JUULI|AUG|SEPT|OKT|NOV|DETS|Jaan|Veebr|Märts|Marts|Apr|Mai|Juuni|Juuli|Aug|Sept|Okt|Nov|Dets)[^0-9]{0,5}$",
    "ixt:date-day-monthname-year-et": r"^([0-9]{1,2})[^0-9]+(jaan|veebr|märts|marts|apr|mai|juuni|juuli|aug|sept|okt|nov|dets|JAAN|VEEBR|MÄRTS|MARTS|APR|MAI|JUUNI|JUULI|AUG|SEPT|OKT|NOV|DETS|Jaan|Veebr|Märts|Marts|Apr|Mai|Juuni|Juuli|Aug|Sept|Okt|Nov|Dets)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-monthname-year-et": r"^(jaan|veebr|märts|marts|apr|mai|juuni|juuli|aug|sept|okt|nov|dets|JAAN|VEEBR|MÄRTS|MARTS|APR|MAI|JUUNI|JUULI|AUG|SEPT|OKT|NOV|DETS|Jaan|Veebr|Märts|Marts|Apr|Mai|Juuni|Juuli|Aug|Sept|Okt|Nov|Dets)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-day-monthname-fi": r"^([0-9]{1,2})[^0-9]*[^0-9a-zA-Z]+(tam|hel|maa|huh|tou|kes|hei|elo|syy|lok|mar|jou|TAM|HEL|MAA|HUH|TOU|KES|HEI|ELO|SYY|LOK|MAR|JOU|Tam|Hel|Maa|Huh|Tou|Kes|Hei|Elo|Syy|Lok|Mar|Jou)[^0-9]{0,8}$",
    "ixt:date-day-monthname-year-fi": r"^([0-9]{1,2})[^0-9]*[^0-9a-zA-Z]+(tam|hel|maa|huh|tou|kes|hei|elo|syy|lok|mar|jou|TAM|HEL|MAA|HUH|TOU|KES|HEI|ELO|SYY|LOK|MAR|JOU|Tam|Hel|Maa|Huh|Tou|Kes|Hei|Elo|Syy|Lok|Mar|Jou)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-monthname-year-fi": r"^(tam|hel|maa|huh|tou|kes|hei|elo|syy|lok|mar|jou|TAM|HEL|MAA|HUH|TOU|KES|HEI|ELO|SYY|LOK|MAR|JOU|Tam|Hel|Maa|Huh|Tou|Kes|Hei|Elo|Syy|Lok|Mar|Jou)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-day-monthname-fr": r"^([0-9]{1,2})[^0-9]+(janv|févr|fevr|mars|avr|mai|juin|juil|août|aout|sept|oct|nov|déc|dec|JANV|FÉVR|FEVR|MARS|AVR|MAI|JUIN|JUIL|AOÛT|AOUT|SEPT|OCT|NOV|DÉC|DEC|Janv|Févr|Fevr|Mars|Avr|Mai|Juin|Juil|Août|Aout|Sept|Oct|Nov|Déc|Dec)[^0-9]{0,5}$",
    "ixt:date-day-monthname-year-fr": r"^([0-9]{1,2})[^0-9]+(janv|févr|fevr|mars|avr|mai|juin|juil|août|aout|sept|oct|nov|déc|dec|JANV|FÉVR|FEVR|MARS|AVR|MAI|JUIN|JUIL|AOÛT|AOUT|SEPT|OCT|NOV|DÉC|DEC|Janv|Févr|Fevr|Mars|Avr|Mai|Juin|Juil|Août|Aout|Sept|Oct|Nov|Déc|Dec)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-monthname-year-fr": r"^(janv|févr|fevr|mars|avr|mai|juin|juil|août|aout|sept|oct|nov|déc|dec|JANV|FÉVR|FEVR|MARS|AVR|MAI|JUIN|JUIL|AOÛT|AOUT|SEPT|OCT|NOV|DÉC|DEC|Janv|Févr|Fevr|Mars|Avr|Mai|Juin|Juil|Août|Aout|Sept|Oct|Nov|Déc|Dec)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-day-monthname-hr": r"^([0-9]{1,2})[^0-9]+(sij|velj|ožu|ozu|tra|svi|lip|srp|kol|ruj|lis|stu|pro|SIJ|VELJ|OŽU|OZU|TRA|SVI|LIP|SRP|KOL|RUJ|LIS|STU|PRO|Sij|Velj|Ožu|Ozu|Tra|Svi|Lip|Srp|Kol|Ruj|Lis|Stu|Pro)[^0-9]{0,6}$",
    "ixt:date-day-monthname-year-hr": r"^([0-9]{1,2})[^0-9]+(sij|velj|ožu|ozu|tra|svi|lip|srp|kol|ruj|lis|stu|pro|SIJ|VELJ|OŽU|OZU|TRA|SVI|LIP|SRP|KOL|RUJ|LIS|STU|PRO|Sij|Velj|Ožu|Ozu|Tra|Svi|Lip|Srp|Kol|Ruj|Lis|Stu|Pro)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-monthname-year-hr": r"^(sij|velj|ožu|ozu|tra|svi|lip|srp|kol|ruj|lis|stu|pro|SIJ|VELJ|OŽU|OZU|TRA|SVI|LIP|SRP|KOL|RUJ|LIS|STU|PRO|Sij|Velj|Ožu|Ozu|Tra|Svi|Lip|Srp|Kol|Ruj|Lis|Stu|Pro)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-day-monthroman": r"^([0-9]{1,2})[^0-9]*[^XVIxvi]((I?(X|V|I)I{0,3})|(i?(x|v|i)i{0,3}))$",
    "ixt:date-day-monthroman-year": r"^([0-9]{1,2})[^0-9]*[^XVIxvi]((I?(X|V|I)I{0,3})|(i?(x|v|i)i{0,3}))[^XVIxvi][^0-9]*([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-monthroman-year": r"^((I?(X|V|I)I{0,3})|(i?(x|v|i)i{0,3}))[^XVIxvi][^0-9]*([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-day-monthname-it": r"^([0-9]{1,2})[^0-9]+(gen|feb|mar|apr|mag|giu|lug|ago|set|ott|nov|dic|GEN|FEB|MAR|APR|MAG|GIU|LUG|AGO|SET|OTT|NOV|DIC|Gen|Feb|Mar|Apr|Mag|Giu|Lug|Ago|Set|Ott|Nov|Dic)[^0-9]{0,6}$",
    "ixt:date-day-monthname-year-it": r"^([0-9]{1,2})[^0-9]+(gen|feb|mar|apr|mag|giu|lug|ago|set|ott|nov|dic|GEN|FEB|MAR|APR|MAG|GIU|LUG|AGO|SET|OTT|NOV|DIC|Gen|Feb|Mar|Apr|Mag|Giu|Lug|Ago|Set|Ott|Nov|Dic)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-monthname-year-it": r"^(gen|feb|mar|apr|mag|giu|lug|ago|set|ott|nov|dic|GEN|FEB|MAR|APR|MAG|GIU|LUG|AGO|SET|OTT|NOV|DIC|Gen|Feb|Mar|Apr|Mag|Giu|Lug|Ago|Set|Ott|Nov|Dic)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-day-monthname-nl": r"^([0-9]{1,2})[^0-9]+(jan|feb|maa|mrt|apr|mei|jun|jul|aug|sep|okt|nov|dec|JAN|FEB|MAA|MRT|APR|MEI|JUN|JUL|AUG|SEP|OKT|NOV|DEC|Jan|Feb|Maa|Mrt|Apr|Mei|Jun|Jul|Aug|Sep|Okt|Nov|Dec)[^0-9]{0,6}$",
    "ixt:date-day-monthname-year-nl": r"^([0-9]{1,2})[^0-9]+(jan|feb|maa|mrt|apr|mei|jun|jul|aug|sep|okt|nov|dec|JAN|FEB|MAA|MRT|APR|MEI|JUN|JUL|AUG|SEP|OKT|NOV|DEC|Jan|Feb|Maa|Mrt|Apr|Mei|Jun|Jul|Aug|Sep|Okt|Nov|Dec)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-monthname-year-nl": r"^(jan|feb|maa|mrt|apr|mei|jun|jul|aug|sep|okt|nov|dec|JAN|FEB|MAA|MRT|APR|MEI|JUN|JUL|AUG|SEP|OKT|NOV|DEC|Jan|Feb|Maa|Mrt|Apr|Mei|Jun|Jul|Aug|Sep|Okt|Nov|Dec)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-monthname-day-hu": r"^(jan|feb|márc|marc|ápr|apr|máj|maj|jún|jun|júl|jul|aug|szept|okt|nov|dec|JAN|FEB|MÁRC|MARC|ÁPR|APR|MÁJ|MAJ|JÚN|JUN|JÚL|JUL|AUG|SZEPT|OKT|NOV|DEC|Jan|Feb|Márc|Marc|Ápr|Apr|Máj|Maj|Jún|Jun|Júl|Jul|Aug|Szept|Okt|Nov|Dec)[^0-9]{0,7}[^0-9]+([0-9]{1,2})$",
    "ixt:date-year-monthname-day-hu": r"^([0-9]{1,2}|[0-9]{4})[^0-9]+(jan|feb|márc|marc|ápr|apr|máj|maj|jún|jun|júl|jul|aug|szept|okt|nov|dec|JAN|FEB|MÁRC|MARC|ÁPR|APR|MÁJ|MAJ|JÚN|JUN|JÚL|JUL|AUG|SZEPT|OKT|NOV|DEC|Jan|Feb|Márc|Marc|Ápr|Apr|Máj|Maj|Jún|Jun|Júl|Jul|Aug|Szept|Okt|Nov|Dec)[^0-9]+([0-9]{1,2})$",
    "ixt:date-year-monthname-hu": r"^([0-9]{1,2}|[0-9]{4})[^0-9]+(jan|feb|márc|marc|ápr|apr|máj|maj|jún|jun|júl|jul|aug|szept|okt|nov|dec|JAN|FEB|MÁRC|MARC|ÁPR|APR|MÁJ|MAJ|JÚN|JUN|JÚL|JUL|AUG|SZEPT|OKT|NOV|DEC|Jan|Feb|Márc|Marc|Ápr|Apr|Máj|Maj|Jún|Jun|Júl|Jul|Aug|Szept|Okt|Nov|Dec)[^0-9]{0,7}$",
    "ixt:date-monthname-day-lt": r"^(sau|vas|kov|bal|geg|bir|lie|rugp|rgp|rugs|rgs|spa|spl|lap|gru|grd|SAU|VAS|KOV|BAL|GEG|BIR|LIE|RUGP|RGP|RUGS|RGS|SPA|SPL|LAP|GRU|GRD|Sau|Vas|Kov|Bal|Geg|Bir|Lie|Rugp|Rgp|Rugs|Rgs|Spa|Spl|Lap|Gru|Grd)[^0-9]{0,6}[^0-9]+([0-9]{1,2})[^0-9]*$",
    "ixt:date-year-monthname-day-lt": r"^([0-9]{1,2}|[0-9]{4})[^0-9]*[^0-9a-zA-Z]+(sau|vas|kov|bal|geg|bir|lie|rugp|rgp|rugs|rgs|spa|spl|lap|gru|grd|SAU|VAS|KOV|BAL|GEG|BIR|LIE|RUGP|RGP|RUGS|RGS|SPA|SPL|LAP|GRU|GRD|Sau|Vas|Kov|Bal|Geg|Bir|Lie|Rugp|Rgp|Rugs|Rgs|Spa|Spl|Lap|Gru|Grd)[^0-9]+([0-9]{1,2})[^0-9]*$",
    "ixt:date-year-monthname-lt": r"^([0-9]{1,2}|[0-9]{4})[^0-9]*[^0-9a-zA-Z]+(sau|vas|kov|bal|geg|bir|lie|rugp|rgp|rugs|rgs|spa|spl|lap|gru|grd|SAU|VAS|KOV|BAL|GEG|BIR|LIE|RUGP|RGP|RUGS|RGS|SPA|SPL|LAP|GRU|GRD|Sau|Vas|Kov|Bal|Geg|Bir|Lie|Rugp|Rgp|Rugs|Rgs|Spa|Spl|Lap|Gru|Grd)[^0-9]*$",
    "ixt:date-day-monthname-lv": r"^([0-9]{1,2})[^0-9]+(janv|febr|marts|apr|maijs|jūn|jun|jūl|jul|aug|sept|okt|nov|dec|JANV|FEBR|MARTS|APR|MAIJS|JŪN|JUN|JŪL|JUL|AUG|SEPT|OKT|NOV|DEC|Janv|Febr|Marts|Apr|Maijs|Jūn|Jun|Jūl|Jul|Aug|Sept|Okt|Nov|Dec)[^0-9]{0,6}$",
    "ixt:date-year-day-monthname-lv": r"^([0-9]{1,2}|[0-9]{4})[^0-9]+([0-9]{1,2})[^0-9]+(janv|febr|marts|apr|maijs|jūn|jun|jūl|jul|aug|sept|okt|nov|dec|JANV|FEBR|MARTS|APR|MAIJS|JŪN|JUN|JŪL|JUL|AUG|SEPT|OKT|NOV|DEC|Janv|Febr|Marts|Apr|Maijs|Jūn|Jun|Jūl|Jul|Aug|Sept|Okt|Nov|Dec)[^0-9]*$",
    "ixt:date-year-monthname-lv": r"^([0-9]{1,2}|[0-9]{4})[^0-9]+(janv|febr|marts|apr|maijs|jūn|jun|jūl|jul|aug|sept|okt|nov|dec|JANV|FEBR|MARTS|APR|MAIJS|JŪN|JUN|JŪL|JUL|AUG|SEPT|OKT|NOV|DEC|Janv|Febr|Marts|Apr|Maijs|Jūn|Jun|Jūl|Jul|Aug|Sept|Okt|Nov|Dec)[^0-9]{0,7}$",
    "ixt:date-day-monthname-no": r"^([0-9]{1,2})[^0-9]+(jan|feb|mar|apr|mai|jun|jul|aug|sep|okt|nov|des|JAN|FEB|MAR|APR|MAI|JUN|JUL|AUG|SEP|OKT|NOV|DES|Jan|Feb|Mar|Apr|Mai|Jun|Jul|Aug|Sep|Okt|Nov|Des)[^0-9]{0,6}$",
    "ixt:date-day-monthname-year-no": r"^([0-9]{1,2})[^0-9]+(jan|feb|mar|apr|mai|jun|jul|aug|sep|okt|nov|des|JAN|FEB|MAR|APR|MAI|JUN|JUL|AUG|SEP|OKT|NOV|DES|Jan|Feb|Mar|Apr|Mai|Jun|Jul|Aug|Sep|Okt|Nov|Des)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-monthname-year-no": r"^(jan|feb|mar|apr|mai|jun|jul|aug|sep|okt|nov|des|JAN|FEB|MAR|APR|MAI|JUN|JUL|AUG|SEP|OKT|NOV|DES|Jan|Feb|Mar|Apr|Mai|Jun|Jul|Aug|Sep|Okt|Nov|Des)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-day-monthname-pl": r"^([0-9]{1,2})[^0-9]*[^0-9a-zA-Z]+(sty|lut|mar|kwi|maj|cze|lip|sie|wrz|paź|paz|lis|gru|STY|LUT|MAR|KWI|MAJ|CZE|LIP|SIE|WRZ|PAŹ|PAZ|LIS|GRU|Sty|Lut|Mar|Kwi|Maj|Cze|Lip|Sie|Wrz|Paź|Paz|Lis|Gru)[^0-9]{0,9}$",
    "ixt:date-day-monthname-year-pl": r"^([0-9]{1,2})[^0-9]*[^0-9a-zA-Z]+(sty|lut|mar|kwi|maj|cze|lip|sie|wrz|paź|paz|lis|gru|STY|LUT|MAR|KWI|MAJ|CZE|LIP|SIE|WRZ|PAŹ|PAZ|LIS|GRU|Sty|Lut|Mar|Kwi|Maj|Cze|Lip|Sie|Wrz|Paź|Paz|Lis|Gru)[^0-9]+([0-9]{1,2}|[0-9]{4})[^0-9]*$",
    "ixt:date-monthname-year-pl": r"^(sty|lut|mar|kwi|maj|cze|lip|sie|wrz|paź|paz|lis|gru|STY|LUT|MAR|KWI|MAJ|CZE|LIP|SIE|WRZ|PAŹ|PAZ|LIS|GRU|Sty|Lut|Mar|Kwi|Maj|Cze|Lip|Sie|Wrz|Paź|Paz|Lis|Gru)[^0-9]+([0-9]{1,2}|[0-9]{4})[^0-9]*$",
    "ixt:date-day-monthname-pt": r"^([0-9]{1,2})[^0-9]+(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez|JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ|Jan|Fev|Mar|Abr|Mai|Jun|Jul|Ago|Set|Out|Nov|Dez)[^0-9]{0,6}$",
    "ixt:date-day-monthname-year-pt": r"^([0-9]{1,2})[^0-9]+(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez|JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ|Jan|Fev|Mar|Abr|Mai|Jun|Jul|Ago|Set|Out|Nov|Dez)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-monthname-year-pt": r"^(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez|JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ|Jan|Fev|Mar|Abr|Mai|Jun|Jul|Ago|Set|Out|Nov|Dez)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-day-monthname-ro": r"^([0-9]{1,2})[^0-9]+(ian|feb|mar|apr|mai|iun|iul|aug|sep|oct|noi|nov|dec|IAN|FEB|MAR|APR|MAI|IUN|IUL|AUG|SEP|OCT|NOI|NOV|DEC|Ian|Feb|Mar|Apr|Mai|Iun|Iul|Aug|Sep|Oct|Noi|Nov|Dec)[^0-9]{0,7}$",
    "ixt:date-day-monthname-year-ro": r"^([0-9]{1,2})[^0-9]+(ian|feb|mar|apr|mai|iun|iul|aug|sep|oct|noi|nov|dec|IAN|FEB|MAR|APR|MAI|IUN|IUL|AUG|SEP|OCT|NOI|NOV|DEC|Ian|Feb|Mar|Apr|Mai|Iun|Iul|Aug|Sep|Oct|Noi|Nov|Dec)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-monthname-year-ro": r"^(ian|feb|mar|apr|mai|iun|iul|aug|sep|oct|noi|nov|dec|IAN|FEB|MAR|APR|MAI|IUN|IUL|AUG|SEP|OCT|NOI|NOV|DEC|Ian|Feb|Mar|Apr|Mai|Iun|Iul|Aug|Sep|Oct|Noi|Nov|Dec)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-day-monthname-sk": r"^([0-9]{1,2})[^0-9]+(jan|feb|mar|apr|máj|maj|jún|jun|júl|jul|aug|sep|okt|nov|dec|JAN|FEB|MAR|APR|MÁJ|MAJ|JÚN|JUN|JÚL|JUL|AUG|SEP|OKT|NOV|DEC|Jan|Feb|Mar|Apr|Máj|Maj|Jún|Jun|Júl|Jul|Aug|Sep|Okt|Nov|Dec)[^0-9]{0,6}$",
    "ixt:date-day-monthname-year-sk": r"^([0-9]{1,2})[^0-9]+(jan|feb|mar|apr|máj|maj|jún|jun|júl|jul|aug|sep|okt|nov|dec|JAN|FEB|MAR|APR|MÁJ|MAJ|JÚN|JUN|JÚL|JUL|AUG|SEP|OKT|NOV|DEC|Jan|Feb|Mar|Apr|Máj|Maj|Jún|Jun|Júl|Jul|Aug|Sep|Okt|Nov|Dec)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-monthname-year-sk": r"^(jan|feb|mar|apr|máj|maj|jún|jun|júl|jul|aug|sep|okt|nov|dec|JAN|FEB|MAR|APR|MÁJ|MAJ|JÚN|JUN|JÚL|JUL|AUG|SEP|OKT|NOV|DEC|Jan|Feb|Mar|Apr|Máj|Maj|Jún|Jun|Júl|Jul|Aug|Sep|Okt|Nov|Dec)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-day-monthname-sl": r"^[0-9]{1,2}[^0-9]+(jan|feb|mar|apr|maj|jun|jul|avg|sep|okt|nov|dec|JAN|FEB|MAR|APR|MAJ|JUN|JUL|AVG|SEP|OKT|NOV|DEC|Jan|Feb|Mar|Apr|Maj|Jun|Jul|Avg|Sep|Okt|Nov|Dec)[^0-9]{0,6}$",
    "ixt:date-day-monthname-year-sl": r"^[0-9]{1,2}[^0-9]+(jan|feb|mar|apr|maj|jun|jul|avg|sep|okt|nov|dec|JAN|FEB|MAR|APR|MAJ|JUN|JUL|AVG|SEP|OKT|NOV|DEC|Jan|Feb|Mar|Apr|Maj|Jun|Jul|Avg|Sep|Okt|Nov|Dec)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-monthname-year-sl": r"^(jan|feb|mar|apr|maj|jun|jul|avg|sep|okt|nov|dec|JAN|FEB|MAR|APR|MAJ|JUN|JUL|AVG|SEP|OKT|NOV|DEC|Jan|Feb|Mar|Apr|Maj|Jun|Jul|Avg|Sep|Okt|Nov|Dec)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-day-monthname-sv": r"^([0-9]{1,2})[^0-9]+(jan|feb|mar|apr|maj|jun|jul|aug|sep|okt|nov|dec|JAN|FEB|MAR|APR|MAJ|JUN|JUL|AUG|SEP|OKT|NOV|DEC|Jan|Feb|Mar|Apr|Maj|Jun|Jul|Aug|Sep|Okt|Nov|Dec)[^0-9]{0,6}$",
    "ixt:date-day-monthname-year-sv": r"^([0-9]{1,2})[^0-9]+(jan|feb|mar|apr|maj|jun|jul|aug|sep|okt|nov|dec|JAN|FEB|MAR|APR|MAJ|JUN|JUL|AUG|SEP|OKT|NOV|DEC|Jan|Feb|Mar|Apr|Maj|Jun|Jul|Aug|Sep|Okt|Nov|Dec)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-monthname-year-sv": r"^(jan|feb|mar|apr|maj|jun|jul|aug|sep|okt|nov|dec|JAN|FEB|MAR|APR|MAJ|JUN|JUL|AUG|SEP|OKT|NOV|DEC|Jan|Feb|Mar|Apr|Maj|Jun|Jul|Aug|Sep|Okt|Nov|Dec)[^0-9]+([0-9]{1,2}|[0-9]{4})$",
    "ixt:date-jpn-era-year-month": r"^(明治|明|大正|大|昭和|昭|平成|平|令和|令)[\s ]*([0-9０-９]{1,2}|元)[\s ]*年[\s ]*([0-9０-９]{1,2})[\s ]*月$",
    "ixt:date-jpn-era-year-month-day": r"^(明治|明|大正|大|昭和|昭|平成|平|令和|令)[\s ]*([0-9０-９]{1,2}|元)[\s ]*年[\s ]*([0-9０-９]{1,2})[\s ]*月[\s ]*([0-9０-９]{1,2})[\s ]*日$",
    "ixt:date-day-monthname-year-hi": r"^([0-9]{1,2}|[०-९]{1,2})[^0-9०-९]+(जनवरी|फरवरी|मार्च|अप्रैल|मई|जून|जुलाई|अगस्त|सितंबर|अक्टूबर|नवंबर|दिसंबर)[^0-9०-९]+([0-9]{2}|[0-9]{4}|[०-९]{2}|[०-९]{4})$",
    "ixt:date-monthname-year-hi": r"^(जनवरी|फरवरी|मार्च|अप्रैल|मई|जून|जुलाई|अगस्त|सितंबर|अक्टूबर|नवंबर|दिसंबर)[^0-9०-९]+([0-9]{2}|[0-9]{4}|[०-९]{2}|[०-९]{4})$",
    "ixt:date-ind-day-monthname-year-hi": r"^([0-9]{1,2}|[०-९]{1,2})[^0-9०-९]+(C\S*ait|चैत्र|Vai|वैशाख|बैसाख|Jy|ज्येष्ठ|dha|ḍha|आषाढ|आषाढ़|vana|Śrāvaṇa|श्रावण|सावन|Bh\S+dra|Proṣṭhapada|भाद्रपद|भादो|in|आश्विन|K\S+rti|कार्तिक|M\S+rga|Agra|मार्गशीर्ष|अगहन|Pau|पौष|M\S+gh|माघ|Ph\S+lg|फाल्गुन)[^0-9०-९]+([0-9]{2}|[0-9]{4}|[०-९]{2}|[०-९]{4})$",
}

# Default order is assumed to be ['day', 'month', 'year'] for full dates, ['day', 'month'] for recurring dates and ['month', 'year'] for Month-Year dates
irregular_date_order_dict = {
    "ixt:date-month-day": ["month", "day"],
    "ixt:date-month-day-year": ["month", "day", "year"],
    "ixt:date-year-month-day": ["year", "month", "day"],
    "ixt:date-year-month": ["year", "month"],
    "ixt:date-monthname-day-en": ["month", "day"],
    "ixt:date-monthname-day-year-en": ["month", "day", "year"],
    "ixt:date-year-monthname-en": ["year", "month"],
    "ixt:date-monthname-day-en": ["month", "day"],
    "ixt:date-monthname-day-year-en": ["month", "day", "year"],
    "ixt:date-year-monthname-en": ["year", "month"],
    "ixt:date-monthname-year-it": ["month", "year"],
    "ixt:date-monthname-day-hu": ["month", "day"],
    "ixt:date-year-monthname-day-hu": ["year", "month", "day"],
    "ixt:date-year-monthname-hu": ["year", "month"],
    "ixt:date-monthname-day-lt": ["month", "day"],
    "ixt:date-year-monthname-day-lt": ["year", "month", "day"],
    "ixt:date-year-monthname-lt": ["year", "month"],
    "ixt:date-year-day-monthname-lv": ["year", "day", "month"],
    "ixt:date-year-monthname-lv": ["year", "month"],
    "ixt:date-day-monthname-year-hi": ["day", "month", "year"],
    "ixt:date-monthname-year-hi": ["month", "year"],
    "ixt:date-jpn-era-year-month": ["era", "year", "month"],
    "ixt:date-jpn-era-year-month-day": ["era", "year", "month", "day"],
}

country_to_month_names = {
    None: [
        ["01", "1"],
        ["02", "2"],
        ["03", "3"],
        ["04", "4"],
        ["05", "5"],
        ["06", "6"],
        ["07", "7"],
        ["08", "8"],
        ["09", "9"],
        ["10"],
        ["11"],
        ["12"],
    ],
    "roman": [
        ["i"],
        ["ii"],
        ["iii"],
        ["iv"],
        ["v"],
        ["vi"],
        ["vii"],
        ["viii"],
        ["ix"],
        ["x"],
        ["xi"],
        ["xii"],
    ],
    "bg": [
        ["ян"],
        ["фев"],
        ["мар"],
        ["апр"],
        ["май", "маи"],
        ["юни"],
        ["юли"],
        ["авг"],
        ["сеп"],
        ["окт"],
        ["ное"],
        ["дек"],
    ],
    "cs": [
        ["leden", "ledna", "lednu", "led"],
        ["únor", "unor", "února", "unora", "únoru", "unoru", "úno", "uno"],
        ["březen", "brezen", "března", "brezna", "březnu", "breznu", "bře", "bre"],
        ["duben", "dubna", "dubnu", "dub"],
        ["květen", "kveten", "května", "kvetna", "květnu", "kvetnu", "kvě", "kve"],
        ["červen", "cerven", "června", "cervna", "červnu", "cervnu", "čvn", "cvn"],
        [
            "červenec",
            "cervenec",
            "července",
            "cervence",
            "červenci",
            "cervenci",
            "čvc",
            "cvc",
        ],
        ["srpen", "srpna", "srpnu", "srp"],
        ["září", "zari", "zář", "zar"],
        ["říjen", "rijen", "října", "rijna", "říjnu", "rijnu", "říj", "rij"],
        ["listopad", "listopadu", "lis"],
        ["prosinec", "prosince", "prosinci", "pro"],
    ],
    "cy": [
        ["ion"],
        ["chwe"],
        ["maw"],
        ["ebr"],
        ["mai"],
        ["meh"],
        ["gor"],
        ["aws"],
        ["med"],
        ["hyd"],
        ["tach"],
        ["rhag"],
    ],
    "da": [
        ["jan"],
        ["feb"],
        ["mar"],
        ["apr"],
        ["maj"],
        ["jun"],
        ["jul"],
        ["aug"],
        ["sep"],
        ["okt"],
        ["nov"],
        ["dec"],
    ],
    "de": [
        ["jan", "jän", "jaen"],
        ["feb"],
        ["mär", "maer", "mar"],
        ["apr"],
        ["mai"],
        ["jun"],
        ["jul"],
        ["aug"],
        ["sep"],
        ["okt"],
        ["nov"],
        ["dez"],
    ],
    "el": [
        ["ιαν", "ίαν"],
        ["φεβ"],
        ["μάρ", "μαρ"],
        ["απρ", "άπρ", "αρίλ", "άρίλ", "αριλ", "άριλ"],
        ["μαΐ", "μαι", "μάι", "μαϊ", "μάϊ"],
        ["ιούν", "ίούν", "ίουν", "ιουν"],
        ["ιούλ", "ίούλ", "ίουλ", "ίουλ", "ιουλ"],
        ["αύγ", "αυγ"],
        ["σεπ"],
        ["οκτ", "όκτ"],
        ["νοέ", "νοε"],
        ["δεκ"],
    ],
    "en": [
        ["january", "jan"],
        ["february", "feb"],
        ["march", "mar"],
        ["april", "apr"],
        ["may"],
        ["june", "jun"],
        ["july", "jul"],
        ["august", "aug"],
        ["september", "sep"],
        ["october", "oct"],
        ["november", "nov"],
        ["december", "dec"],
    ],
    "es": [
        ["ene"],
        ["feb"],
        ["mar"],
        ["abr"],
        ["may"],
        ["jun"],
        ["jul"],
        ["ago"],
        ["sep"],
        ["oct"],
        ["nov"],
        ["dic"],
    ],
    "et": [
        ["jaan"],
        ["veebr"],
        ["märts", "marts"],
        ["apr"],
        ["mai"],
        ["juuni"],
        ["juuli"],
        ["aug"],
        ["sept"],
        ["okt"],
        ["nov"],
        ["dets"],
    ],
    "fi": [
        ["tam"],
        ["hel"],
        ["maa"],
        ["huh"],
        ["tou"],
        ["kes"],
        ["hei"],
        ["elo"],
        ["syy"],
        ["lok"],
        ["mar"],
        ["jou"],
    ],
    "fr": [
        ["janv"],
        ["févr", "fevr"],
        ["mars"],
        ["avr"],
        ["mai"],
        ["juin"],
        ["juil"],
        ["août", "aout"],
        ["sept"],
        ["oct"],
        ["nov"],
        ["déc", "dec"],
    ],
    "hi": [
        ["जनवरी", "cait", "chait", "चैत्र"],
        ["फरवरी", "vai", "वैशाख", "बैसाख"],
        ["मार्च", "jy", "ज्येष्ठ"],
        ["अप्रैल", "dha", "ḍha", "आषाढ", "आषाढ़"],
        ["मई", "vana", "śrāvaṇa", "श्रावण", "सावन"],
        ["जून", "bhadra", "proṣṭhapada", "भाद्रपद", "भादो"],
        ["जुलाई", "in", "आश्विन"],
        ["अगस्त", "karti", "kartik", "कार्तिक"],
        ["सितंबर", "mrga", "marga", "agra", "मार्गशीर्ष", "अगहन"],
        ["अक्टूबर", "pau", "पौष"],
        ["नवंबर", "mgh", "magha", "माघ"],
        ["दिसंबर", "phlg", "phalg", "फाल्गुन"],
    ],
    "hr": [
        ["sij"],
        ["velj"],
        ["ožu", "ozu"],
        ["tra"],
        ["svi"],
        ["lip"],
        ["srp"],
        ["kol"],
        ["ruj"],
        ["lis"],
        ["stu"],
        ["pro"],
    ],
    "it": [
        ["gen"],
        ["feb"],
        ["mar"],
        ["apr"],
        ["mag"],
        ["giu"],
        ["lug"],
        ["ago"],
        ["set"],
        ["ott"],
        ["nov"],
        ["dic"],
    ],
    "nl": [
        ["jan"],
        ["feb"],
        ["maa"],
        ["mrt"],
        ["apr"],
        ["mei"],
        ["jun"],
        ["jul"],
        ["aug"],
        ["sep"],
        ["okt"],
        ["nov"],
        ["dec"],
    ],
    "hu": [
        ["jan"],
        ["feb"],
        ["márc", "marc"],
        ["ápr", "apr"],
        ["máj", "maj"],
        ["jún", "jun"],
        ["júl", "jul"],
        ["aug"],
        ["szept"],
        ["okt"],
        ["nov"],
        ["dec"],
    ],
    "lt": [
        ["sau"],
        ["vas"],
        ["kov"],
        ["bal"],
        ["geg"],
        ["bir"],
        ["lie"],
        ["rugp", "rgp", "rugs", "rgs"],
        ["spa", "spl"],
        ["lap"],
        ["gru", "grd"],
    ],
    "lv": [
        ["janv"],
        ["febr"],
        ["marts"],
        ["apr"],
        ["maijs"],
        ["jūn", "jun"],
        ["jūl", "jul"],
        ["aug"],
        ["sept"],
        ["okt"],
        ["nov"],
        ["dec"],
    ],
    "no": [
        ["jan"],
        ["feb"],
        ["mar"],
        ["apr"],
        ["mai"],
        ["jun"],
        ["jul"],
        ["aug"],
        ["sep"],
        ["okt"],
        ["nov"],
        ["des"],
    ],
    "pl": [
        ["sty"],
        ["lut"],
        ["mar"],
        ["kwi"],
        ["maj"],
        ["cze"],
        ["lip"],
        ["sie"],
        ["wrz"],
        ["paź", "paz"],
        ["lis"],
        ["gru"],
    ],
    "pt": [
        ["jan"],
        ["fev"],
        ["mar"],
        ["abr"],
        ["mai"],
        ["jun"],
        ["jul"],
        ["ago"],
        ["set"],
        ["out"],
        ["nov"],
        ["dez"],
    ],
    "ro": [
        ["ian"],
        ["feb"],
        ["mar"],
        ["apr"],
        ["mai"],
        ["iun"],
        ["iul"],
        ["aug"],
        ["sep"],
        ["oct"],
        ["noi", "nov"],
        ["dec"],
    ],
    "sk": [
        ["jan"],
        ["feb"],
        ["mar"],
        ["apr"],
        ["máj", "maj"],
        ["jún", "jun"],
        ["júl", "jul"],
        ["aug"],
        ["sep"],
        ["okt"],
        ["nov"],
        ["dec"],
    ],
    "sl": [
        ["jan"],
        ["feb"],
        ["mar"],
        ["apr"],
        ["maj"],
        ["jun"],
        ["jul"],
        ["avg"],
        ["sep"],
        ["okt"],
        ["nov"],
        ["dec"],
    ],
    "sv": [
        ["jan"],
        ["feb"],
        ["mar"],
        ["apr"],
        ["maj"],
        ["jun"],
        ["jul"],
        ["aug"],
        ["sep"],
        ["okt"],
        ["nov"],
        ["dec"],
    ],
}

japanese_era_to_gregorian_period = {
    # era: (starting_date, ending_date)
    "明治": (datetime.date(1868, 10, 23), datetime.date(1912, 7, 29)),
    "明": (datetime.date(1868, 10, 23), datetime.date(1912, 7, 29)),
    "大正": (datetime.date(1912, 7, 30), datetime.date(1926, 12, 24)),
    "大": (datetime.date(1912, 7, 30), datetime.date(1926, 12, 24)),
    "昭和": (datetime.date(1926, 12, 25), datetime.date(1989, 1, 7)),
    "昭": (datetime.date(1926, 12, 25), datetime.date(1989, 1, 7)),
    "平成": (datetime.date(1989, 1, 8), datetime.date(2019, 4, 30)),
    "平": (datetime.date(1989, 1, 8), datetime.date(2019, 4, 30)),
    "令和": (datetime.date(2019, 5, 1), datetime.date(9999, 12, 31)),
    "令": (datetime.date(2019, 5, 1), datetime.date(9999, 12, 31)),
}

legacy_to_current_formats = {
    # Transformation registries 2 and 3
    "ixt:booleanfalse": "ixt:fixed-false",
    "ixt:booleantrue": "ixt:fixed-true",
    "ixt:calindaymonthyear": "ixt:date-ind-day-month-year-hi",
    "ixt:datedaymonth": "ixt:date-day-month",
    "ixt:datedaymonthdk": "ixt:date-day-monthname-da",
    "ixt:datedaymonthen": "ixt:date-day-monthname-en",
    "ixt:datedaymonthyear": "ixt:date-day-month-year",
    "ixt:datedaymonthyeardk": "ixt:date-day-monthname-year-da",
    "ixt:datedaymonthyearen": "ixt:date-day-monthname-year-en",
    "ixt:dateerayearmonthdayjp": "ixt:date-jpn-era-year-month-day",
    "ixt:dateerayearmonthjp": "ixt:date-jpn-era-year-month",
    "ixt:datemonthday": "ixt:date-month-day",
    "ixt:datemonthdayen": "ixt:date-monthname-day-en",
    "ixt:datemonthdayyear": "ixt:date-month-day-year",
    "ixt:datemonthdayyearen": "ixt:date-monthname-day-year-en",
    "ixt:datemonthyear": "ixt:date-month-year",
    "ixt:datemonthyeardk": "ixt:date-monthname-year-da",
    "ixt:datemonthyearen": "ixt:date-monthname-year-en",
    "ixt:datemonthyearin": "ixt:date-monthname-year-hi",
    "ixt:dateyearmonthday": "ixt:date-year-month-day",
    "ixt:dateyearmonthdaycjk": "ixt:date-year-month-day",
    "ixt:dateyearmonthcjk": "ixt:date-year-month",
    "ixt:dateyearmonthen": "ixt:date-year-monthname-en",
    "ixt:nocontent": "ixt:fixed-empty",
    "ixt:numcommadecimal": "ixt:num-comma-decimal",
    "ixt:numdotdecimal": "ixt:num-dot-decimal",
    "ixt:numdotdecimalin": "ixt:num-dot-decimal",
    "ixt:numunitdecimal": "ixt:num-unit-decimal",
    "ixt:numunitdecimalin": "ixt:num-unit-decimal",
    "ixt:zerodash": "ixt:fixed-zero",
    # Transformation registry 1.0
    "ixt:numcomma": "ixt:num-comma-decimal",
    "ixt:numcommadot": "ixt:num-dot-decimal",
    "ixt:numdash": "ixt:fixed-zero",
    "ixt:numdotcomma": "ixt:num-comma-decimal",
    "ixt:numspacecomma": "ixt:num-comma-decimal",
    "ixt:numspacedot": "ixt:num-dot-decimal",
    "ixt:datedoteu": "ixt:date-day-month-year",
    "ixt:datedotus": "ixt:date-month-day-year",
    "ixt:datelonguk": "ixt:date-day-monthname-year-en",
    "ixt:datelongus": "ixt:date-monthname-day-year-en",
    "ixt:dateshortuk": "ixt:date-day-monthname-year-en",
    "ixt:dateshortus": "ixt:date-monthname-day-year-en",
    "ixt:dateslasheu": "ixt:date-day-month-year",
    "ixt:dateslashus": "ixt:date-month-day-year",
    "ixt:datelongdaymonthuk": "ixt:date-day-monthname-en",
    "ixt:datelongmonthdayus": "ixt:date-monthname-day-en",
    "ixt:dateshortdaymonthuk": "ixt:date-day-monthname-en",
    "ixt:dateshortmonthdayus": "ixt:date-day-monthname-en",
    "ixt:dateslashdaymontheu": "ixt:date-day-month",
    "ixt:dateslashmonthdayus": "ixt:date-month-day",
    "ixt:datelongyearmonth": "ixt:date-year-monthname-en",
    "ixt:dateshortyearmonth": "ixt:date-year-monthname-en",
    "ixt:datelongmonthyear": "ixt:date-monthname-year-en",
    "ixt:dateshortmonthyear": "ixt:date-monthname-year-en",
}


def match_regex_date_fact_value(
    fact_value: str,
    fact_format: str,
    element: _Element,
    error_repository: ErrorRepository,
) -> Optional[re.Match]:
    regex_pattern = date_format_to_regex.get(fact_format)
    if not regex_pattern:
        error_repository.insert(
            ErrorCode.UNSUPPORTED_DATE_FORMAT, element, format=fact_format
        )

        return None

    match = re.search(regex_pattern, fact_value)
    if not match:
        error_repository.insert(
            ErrorCode.DATE_DOES_NOT_MATCH_EXPECTED_FORMAT,
            element,
            date=fact_value,
            format=fact_format,
        )

        return None

    return match


def parse_date_match(
    match: re.Match, fact_format: str, is_recurring: bool, is_full_date: bool
) -> dict[str, str]:
    date_order = irregular_date_order_dict.get(fact_format)

    # Default date order (day) month (year)
    if not date_order:
        day_component = ["day"] if is_recurring or is_full_date else []
        month_component = ["month"]
        year_component = ["year"] if not is_recurring else []
        date_order = day_component + month_component + year_component

    date_parts = {}

    for i, date_part in enumerate(date_order):
        date_parts[date_part] = match.group(i + 1)

    return date_parts


def convert_japanese_imperial_date_to_gregorian(
    date_parts: dict[str, str], fact_format: str
) -> dict[str, str]:
    era_starting_year = japanese_era_to_gregorian_period[date_parts["era"]][0].year
    year_offset = 1 if date_parts["year"] == "元" else int(date_parts["year"])
    gregorian_year = era_starting_year + year_offset - 1

    date_parts["year"] = str(gregorian_year)

    return date_parts


def convert_national_indian_date_to_gregorian(
    date_parts: dict[str, str]
) -> dict[str, str]:
    if len("year") == 2:
        date_parts["year"] = "19" + date_parts["year"]

    gregorian_date = indian_civil.to_gregorian(
        int(date_parts["year"]), int(date_parts["month"]), int(date_parts["day"])
    )

    gregorian_year, gregorian_month, gregorian_day = gregorian_date

    # We assume two-digit years fall within 2000 and 2099, as in the specifications
    if len("year") == 2 and gregorian_year < 2000:
        gregorian_year += 100

    date_parts["year"] = str(gregorian_year)
    date_parts["month"] = "{:02n}".format(gregorian_month)
    date_parts["day"] = "{:02n}".format(gregorian_day)

    return date_parts


def normalize_date_parts(
    date_parts: dict[str, str], fact_format: str
) -> dict[str, str]:
    date_parts = {k: normalize_digits_in_string(v) for k, v in date_parts.items()}

    # special handling of japanese imperial calendar
    if "jpn" in fact_format:
        date_parts = convert_japanese_imperial_date_to_gregorian(
            date_parts, fact_format
        )

    normalized_date_parts = {}

    if "day" in date_parts:
        normalized_date_parts["day"] = "{:02n}".format(int(date_parts["day"]))
    if "month" in date_parts:
        country = fact_format[-2:] if fact_format[-3] == "-" else None

        if not country and "monthroman" in fact_format:
            country = "roman"

        month_names = country_to_month_names[country]

        date_parts["month"] = date_parts["month"].lower()
        for i, month_i_names in enumerate(month_names):
            if date_parts["month"] in month_i_names:
                normalized_date_parts["month"] = "{:02n}".format(i + 1)
                break
    if "year" in date_parts:
        # special handling of indian national calendar
        if fact_format == "ixt:date-ind-day-monthname-year-hi":
            normalized_date_parts = convert_national_indian_date_to_gregorian(
                normalized_date_parts
            )
        elif len(date_parts["year"]) == 2:
            normalized_date_parts["year"] = "20" + date_parts["year"]
        elif len(date_parts["year"]) == 1:
            normalized_date_parts["year"] = "200" + date_parts["year"]
        else:
            normalized_date_parts["year"] = date_parts["year"]

    return normalized_date_parts


def check_japanese_imperial_date_valid(date_parts: dict[str, str]) -> bool:
    era_start_date = japanese_era_to_gregorian_period[date_parts["era"]][0]
    era_end_date = japanese_era_to_gregorian_period[date_parts["era"]][1]

    if "day" in date_parts:
        iso8601_formatted_string = (
            f'{date_parts["year"]}-{date_parts["month"]}-{date_parts["day"]}'
        )
        given_date = datetime.date.fromisoformat(iso8601_formatted_string)

        if given_date < era_start_date or given_date > era_end_date:
            return False
    else:
        iso8601_formatted_string = (
            f'{date_parts["year"]}-{date_parts["month"]}-{era_start_date.day}'
        )
        given_date = datetime.date.fromisoformat(iso8601_formatted_string)

        if given_date < era_start_date:
            return False

        iso8601_formatted_string = (
            f'{date_parts["year"]}-{date_parts["month"]}-{era_end_date.day}'
        )
        given_date = datetime.date.fromisoformat(iso8601_formatted_string)

        if given_date > era_end_date:
            return False

    return True


def validate_date_fact_value(
    date_parts: dict[str, str],
    fact_value: str,
    element: _Element,
    error_repository: ErrorRepository,
    is_recurring=False,
    is_full_date=False,
) -> None:
    if is_recurring:
        if "year" in date_parts:
            error_repository.insert(
                ErrorCode.YEAR_PRESENT_IN_RECURRING_DATE, element, date=fact_value
            )
        if "month" not in date_parts or "day" not in date_parts:
            error_repository.insert(
                ErrorCode.MONTH_OR_DAY_NOT_PRESENT_IN_RECURRING_DATE,
                element,
                date=fact_value,
            )
    elif "year" not in date_parts or "month" not in date_parts:
        error_repository.insert(
            ErrorCode.YEAR_OR_MONTH_NOT_PRESENT_IN_NON_RECURRING_DATE,
            element,
            date=fact_value,
        )

    if is_full_date and "day" not in date_parts:
        error_repository.insert(
            ErrorCode.DAY_NOT_PRESENT_IN_FULL_DATE, element, date=fact_value
        )

    iso8601_formatted_string = f"{date_parts['year'] if not is_recurring else '2020'}-{date_parts['month']}-{date_parts['day'] if is_full_date else '01'}"

    try:
        datetime.date.fromisoformat(iso8601_formatted_string)
    except Exception:
        error_repository.insert(
            ErrorCode.INVALID_GREGORIAN_DATE, element, date=fact_value
        )

    if "era" in date_parts:
        if not check_japanese_imperial_date_valid(date_parts):
            error_repository.insert(
                ErrorCode.INVALID_JAPANESE_IMPERIAL_DATE, element, date=fact_value
            )


def parse_date_fact_value(
    fact_value: str,
    fact_format: str,
    element: _Element,
    error_repository: ErrorRepository,
) -> str:
    fact_value = fact_value.strip()
    is_full_date = "day" in fact_format and "year" in fact_format
    is_recurring = "day" in fact_format and "year" not in fact_format

    match = match_regex_date_fact_value(
        fact_value, fact_format, element, error_repository
    )

    # No match found
    if not match:
        return fact_value

    date_parts = parse_date_match(
        match, fact_format, is_recurring=is_recurring, is_full_date=is_full_date
    )
    date_parts = normalize_date_parts(date_parts, fact_format)

    validate_date_fact_value(
        date_parts,
        is_recurring=is_recurring,
        is_full_date=is_full_date,
        fact_value=fact_value,
        element=element,
        error_repository=error_repository,
    )

    if is_full_date:
        return f"{date_parts['year']}-{date_parts['month']}-{date_parts['day']}"
    elif is_recurring:
        return f"--{date_parts['month']}-{date_parts['day']}"
    else:
        return f"{date_parts['year']}-{date_parts['month']}"


def parse_literal_fact_value(
    fact_value: str,
    fact_format: str,
    element: _Element,
    error_repository: ErrorRepository,
) -> str:
    if fact_format == "ixt:fixed-empty":
        fact_value = ""
    elif fact_format == "ixt:fixed-false":
        fact_value = "false"
    elif fact_format == "ixt:fixed-true":
        fact_value = "true"
    elif fact_format == "ixt:fixed-zero":
        fact_value = "0"
    else:
        error_repository.insert(
            ErrorCode.UNSUPPORTED_LITERAL_FACT_FORMAT, element, format=fact_format
        )

        return fact_value

    return fact_value


def normalize_digits_in_string(string: str) -> str:
    digits_map = {
        # Japanese digits
        "０": "0",
        "１": "1",
        "２": "2",
        "３": "3",
        "４": "4",
        "５": "5",
        "６": "6",
        "７": "7",
        "８": "8",
        "９": "9",
        # Hindu digits
        "०": "0",
        "१": "1",
        "२": "2",
        "३": "3",
        "४": "4",
        "५": "5",
        "६": "6",
        "७": "7",
        "८": "8",
        "९": "9",
    }

    return "".join(digits_map.get(c, c) for c in string)


def match_regex_numerical_fact_value(
    fact_value: str,
    fact_format: str,
    element: _Element,
    error_repository: ErrorRepository,
) -> Optional[re.Match]:
    number_format_regex = number_format_to_regex.get(fact_format)

    if not number_format_regex:
        error_repository.insert(
            ErrorCode.UNSUPPORTED_NON_FRACTION_FACT_FORMAT, element, format=fact_format
        )

        return None

    match = re.match(number_format_regex, fact_value)
    if not match:
        error_repository.insert(
            ErrorCode.NUMBER_DOES_NOT_MATCH_EXPECTED_FORMAT,
            element,
            number=fact_value,
            format=fact_format,
        )

        return None

    return match


def apply_scale(whole_part: str, decimal_part: str, scale: int) -> tuple[str, str]:
    if scale < 0:
        if -scale > len(whole_part):
            whole_part = "0" * (-scale - len(whole_part)) + whole_part

        decimal_part = whole_part[scale:] + decimal_part
        whole_part = whole_part[:scale]
    else:
        if scale > len(decimal_part):
            decimal_part = decimal_part + "0" * (scale - len(decimal_part))

        whole_part = whole_part + decimal_part[:scale]
        decimal_part = decimal_part[scale:]

    return whole_part, decimal_part


def process_number_part(number_part: str) -> str:
    separators = " .,，'`´’′＇"

    if not number_part:
        number_part = "0"
    for sep in separators:
        number_part = number_part.replace(sep, "")

    return number_part


def process_numerical_fact_value(
    match: re.Match,
    fact_scale: str,
    element: _Element,
    error_repository: ErrorRepository,
) -> str:
    # Parse whole and decimal parts
    whole_part = process_number_part(match.group(1))
    decimal_part = process_number_part(match.group(2))

    # Parse the scale
    scale = 0
    try:
        scale = int(fact_scale)
    except Exception:
        error_repository.insert(
            ErrorCode.INVALID_SCALE_ATTRIBUTE_VALUE, element, scale=fact_scale
        )

    whole_part, decimal_part = apply_scale(whole_part, decimal_part, scale)
    fact_value = whole_part + "." + decimal_part

    return fact_value


def normalize_numerical_fact_value(fact_value: str) -> str:
    fact_value = normalize_digits_in_string(fact_value)

    fact_value = fact_value.rstrip("0")

    # Remove decimal point if there is no remaining fractional part
    if fact_value.endswith("."):
        fact_value = fact_value[:-1]

    fact_value = fact_value.lstrip("0")

    # Add leading zero if necessary
    if fact_value.startswith("."):
        fact_value = "0" + fact_value

    return fact_value


def parse_numerical_fact_value(
    fact_value: str,
    fact_format: str,
    fact_scale: str,
    element: _Element,
    error_repository: ErrorRepository,
) -> str:
    """
    Parses and converts a numerical fact value from a string based on the specified format and scale.

    This function handles various numerical fact formats defined by XBRL, such as dot or comma as decimal
    separators, and potentially removes additional formatting characters like spaces or apostrophes. The
    function then scales the numerical value by a factor of 10 raised to the power of the given scale.

    :param fact_value: The numerical fact value as a string.
    :param fact_format: The format of the numerical fact, indicating how the value is formatted.
    :param fact_scale: The scale to apply to the numerical value, represented as a power of 10.
    :return: The parsed and scaled numerical value as a string.
    :raises ValueError: If the format is not supported.
    """
    if fact_format == "ixt:fixed-zero":
        return "0"

    fact_format = legacy_to_current_formats.get(fact_format, fact_format)

    fact_value = fact_value.strip()
    match = match_regex_numerical_fact_value(
        fact_value, fact_format, element, error_repository
    )

    if not match:
        return fact_value

    fact_value = process_numerical_fact_value(
        match, fact_scale, element, error_repository
    )
    fact_value = normalize_numerical_fact_value(fact_value)

    return fact_value


def parse_non_numerical_fact_value(
    fact_value: str,
    fact_format: Optional[str],
    element: _Element,
    error_repository: ErrorRepository,
) -> str:
    if not fact_format:
        return fact_value

    fact_format = legacy_to_current_formats.get(fact_format, fact_format)

    if fact_format.startswith("ixt:num") or fact_format == "ixt:fixed-zero":
        error_repository.insert(
            ErrorCode.UNSUPPORTED_NON_NUMERIC_FACT_FORMAT,
            element,
            format=fact_format,
        )

        return fact_value

    if fact_format.startswith("ixt:date"):
        # Special handling of legacy format
        if fact_format == "ixt:datedaymonthyearin":
            fact_value_option_1 = parse_date_fact_value(
                fact_value, "ixt:date-day-month-year", element, error_repository
            )

            fact_value_option_2 = parse_date_fact_value(
                fact_value, "ixt:date-day-monthname-year-hi", element, error_repository
            )

            fact_value = fact_value_option_1 or fact_value_option_2
        else:
            fact_value = parse_date_fact_value(
                fact_value, fact_format, element, error_repository
            )
    else:
        fact_value = parse_literal_fact_value(
            fact_value, fact_format, element, error_repository
        )

    return fact_value
