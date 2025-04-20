""" from https://github.com/keithito/tacotron """
'''
Defines all symbols needed for Marathi (Devanagari + Romanization) and English text.
Supports:
1. Native Devanagari script
2. ISO 15919 / IAST transliteration
3. Harvard-Kyoto transliteration
4. Punctuation (English + Marathi)
5. Special tokens (padding, EOS)
'''

from models.audio.tts.tacotron2.text import cmudict

# === SPECIAL TOKENS ===
_pad = '_'       # Padding token (for alignment)
_eos = '~'       # End-of-sentence token
_space = ' '     # Space separator

# === PUNCTUATION ===
_english_punc = '!\'"(),.:;?- '  
_marathi_punc = '।॥'            # Devanagari danda (।) and double danda (॥)
_punctuation = _english_punc + _marathi_punc

# === BASE LATIN LETTERS (English) ===
_base_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

# === MARATHI TRANSLITERATION SYMBOLS (Romanized) ===
# Vowels & Diacritics
_marathi_vowels = 'āīūṛṝḷḹēō'    # Long vowels (आ, ई, ऊ, ऋ, ॠ, ऌ, ॡ, ए, ओ)
_marathi_consonants = 'ṅñṭḍṇśṣ'  # Special consonants (ङ, ञ, ट, ड, ण, श, ष)
_marathi_other = 'ṃḥ'            # Anusvara (ं) and Visarga (ः)

# === DEVANAGARI UNICODE RANGE (Native Marathi) ===
# Vowels (अ-औ), consonants (क-ह), numerals (०-९), and modifiers (e.g., ् for halant)
_devanagari_vowels = 'अआइईउऊऋॠऌॡएऐओऔ'
_devanagari_consonants = 'कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह'
_devanagari_numerals = '०१२३४५६७८९'
_devanagari_modifiers = '़ािीुूृॄॢॣेैोौंः्'  # Matras, anusvara, visarga, halant

# Combine all Devanagari
_devanagari = (
    _devanagari_vowels +
    _devanagari_consonants +
    _devanagari_numerals +
    _devanagari_modifiers
)

# === ALL LETTERS (Latin + Devanagari) ===
_letters = (
    _base_letters +
    _marathi_vowels +
    _marathi_consonants +
    _marathi_other +
    _devanagari
)

# === ARPABET (English phonemes) ===
_arpabet = ['@' + s for s in cmudict.valid_symbols]

# === FINAL SYMBOLS LIST ===
symbols = (
    [_pad, _eos] +                # Special tokens
    list(_punctuation) +          # Punctuation
    list(_letters) +              # All letters (Latin + Devanagari)
    _arpabet                      # ARPAbet symbols (English)
)