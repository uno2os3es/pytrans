import dl_translate as dlt

mt = dlt.TranslationModel()  # Slow when you load it for the first time

text_hi = 'संयुक्त राष्ट्र के प्रमुख का कहना है कि सीरिया में कोई सैन्य समाधान नहीं है'
mt.translate(text_hi, source=dlt.lang.HINDI, target=dlt.lang.ENGLISH)
