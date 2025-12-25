from deep_translator import GoogleTranslator
import time
import os
import json
from multiprocessing import Pool, Manager, Lock
from functools import partial


def translate_batch(words, source='fa', target='en'):
    """
    Translate a batch of words in a single request.

    Args:
        words: List of words to translate
        source: Source language code
        target: Target language code

    Returns:
        Dictionary of {original: translation}
    """
    try:
        translator = GoogleTranslator(source=source, target=target)
        # Join words with newline for batch translation
        text_to_translate = '\n'.join(words)
        translated_text = translator.translate(text_to_translate)

        # Split translations back
        translations = translated_text.split('\n')

        # Create dictionary
        result = {}
        for original, translated in zip(words, translations):
            result[original] = translated.strip()

        return result
    except Exception as e:
        print(f'ERROR in batch translation: {e}')
        # Return error markers for failed batch
        return {word: '[ERROR]' for word in words}


def translate_batch_worker(batch_info, lock, shared_dict, output_file):
    """
    Worker function for multiprocessing.

    Args:
        batch_info: Tuple of (batch_number, words_list)
        lock: Multiprocessing lock for file writing
        shared_dict: Shared dictionary for progress tracking
        output_file: Path to output JSON file
    """
    batch_num, words = batch_info

    print(f'[Batch {batch_num}] Starting translation of {len(words)} words...')

    try:
        # Translate the batch
        translations = translate_batch(words)

        # Update shared dictionary and save
        with lock:
            # Load existing data
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as f:
                    all_translations = json.load(f)
            else:
                all_translations = {}

            # Update with new translations
            all_translations.update(translations)

            # Save to file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_translations, f, ensure_ascii=False, indent=2)

            shared_dict['completed'] = shared_dict.get('completed',
                                                       0) + len(words)
            print(
                f'[Batch {batch_num}] ✓ Completed! Total progress: {shared_dict["completed"]} words'
            )

        return translations

    except Exception as e:
        print(f'[Batch {batch_num}] ERROR: {e}')
        return {}


def translate_and_update(
    source_file='words.txt',
    output_file='dic.json',
    batch_size=5000,
    num_processes=4,
    delay=1.0,
):
    """
    Translate words using multiprocessing with batch translation.

    Args:
        source_file: Source file with Persian words
        output_file: Output JSON file for translations
        batch_size: Number of words to translate per request
        num_processes: Number of parallel processes
        delay: Delay between batches (seconds)
    """

    # Load existing translations
    translations = {}
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            translations = json.load(f)
        print(f'Loaded {len(translations)} existing translations')

    # Load all words
    with open(source_file, 'r', encoding='utf-8') as f:
        all_words = [line.strip() for line in f if line.strip()]

    # Find untranslated words
    untranslated = [w for w in all_words if w not in translations]
    print(f'Total words: {len(all_words)}')
    print(f'Already translated: {len(translations)}')
    print(f'Remaining: {len(untranslated)}')

    if not untranslated:
        print('All words already translated!')
        return

    # Split into batches
    batches = []
    for i in range(0, len(untranslated), batch_size):
        batch = untranslated[i:i + batch_size]
        batches.append((i // batch_size + 1, batch))

    print(f'\nCreated {len(batches)} batches of up to {batch_size} words each')
    print(f'Using {num_processes} parallel processes\n')

    # Create manager for shared state
    manager = Manager()
    lock = manager.Lock()
    shared_dict = manager.dict()
    shared_dict['completed'] = len(translations)

    # Create partial function with fixed arguments
    worker_func = partial(
        translate_batch_worker,
        lock=lock,
        shared_dict=shared_dict,
        output_file=output_file,
    )

    # Process batches with multiprocessing
    with Pool(processes=num_processes) as pool:
        results = []
        for batch_info in batches:
            result = pool.apply_async(worker_func, (batch_info,))
            results.append(result)
            time.sleep(delay)  # Small delay between starting batches

        # Wait for all to complete
        for result in results:
            result.get()

    print(f'\n✓ Complete! All translations saved to {output_file}')

    # Print final statistics
    with open(output_file, 'r', encoding='utf-8') as f:
        final_translations = json.load(f)
    print(f'Total translations in file: {len(final_translations)}')


def view_sample(output_file='dic.json', num_samples=10):
    """View sample translations from the output file."""
    if not os.path.exists(output_file):
        print(f'File {output_file} not found!')
        return

    with open(output_file, 'r', encoding='utf-8') as f:
        translations = json.load(f)

    print(f'\nSample translations ({num_samples} of {len(translations)}):')
    print('-' * 50)
    for i, (persian,
            english) in enumerate(list(translations.items())[:num_samples], 1):
        print(f'{i}. {persian} = {english}')


# Run the script
if __name__ == '__main__':
    translate_and_update(
        source_file='words.txt',
        output_file='dic.json',
        batch_size=5000,  # Translate 5000 words per request
        num_processes=4,  # Use 4 parallel processes
        delay=1.0,  # 1 second delay between starting batches
    )

    # View sample results
    view_sample('dic.json', num_samples=20)
