# Basic usage
translate_and_update()
# Custom configuration
translate_and_update(
    source_file='my_words.txt',
    output_file='my_dic.json',
    batch_size=3000,  # Smaller batches
    num_processes=8,  # More parallel processes
    delay=0.5,  # Faster batch starts
)
translate_and_update(
source_file='words.txt',
output_file='dic.json',
batch_size=50, # دستههای کوچکتر
num_processes=1, # بدون موازیسازی
delay=3.0 # تأخیر بیشتر
)
import random
def translate_with_retry(word, max_retries=3):
"""ترجمه با تلاش مجدد"""
translator = GoogleTranslator(source='fa', target='en')
    for attempt in range(max_retries):
        try:
            translation = translator.translate(word)
            return translation
        except Exception as e:
            if "429" in str(e) or "Too Many Requests" in str(e):
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"خطای 429 - انتظار {wait_time:.1f} ثانیه...")
                time.sleep(wait_time)
            else:
                return "[ERROR]"
    return "[ERROR]"
from deep_translator import DeeplTranslator
def translate_batch(words, source='fa', target='en', api_key=None):
"""استفاده از DeepL به جای Google"""
translator = DeeplTranslator(
source=source,
target=target,
api_key=api_key, # نیاز به API key دارد
use_free_api=True
) # ... بقیه کد
def translate_batch(words, source='fa', target='en'):
"""ترجمه کلمات به صورت تکبهتک"""
translator = GoogleTranslator(source=source, target=target)
result = {}
    for word in words:
        try:
            time.sleep(0.5)  # تأخیر بین هر ترجمه
            translation = translator.translate(word)
            result[word] = translation
        except Exception as e:
            print(f"خطا در ترجمه '{word}': {e}")
            result[word] = "[ERROR]"
            time.sleep(2)  # تأخیر بیشتر بعد از خطا
    return result
translate_and_update(
source_file='words.txt',
output_file='dic.json',
batch_size=100, # کاهش اندازه دسته از 5000 به 100
num_processes=1, # کاهش فرآیندهای موازی
delay=2.0 # افزایش تأخیر به 2 ثانیه
)
