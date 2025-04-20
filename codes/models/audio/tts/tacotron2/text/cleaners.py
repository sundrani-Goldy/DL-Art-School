""" from https://github.com/keithito/tacotron """

'''
Cleaners are transformations that run over the input text at both training and eval time.

Cleaners can be selected by passing a comma-delimited list of cleaner names as the "cleaners"
hyperparameter. Some cleaners are English-specific. You'll typically want to use:
  1. "english_cleaners" for English text (now handles Marathi text as well)
  2. "transliteration_cleaners" for non-English text that can be transliterated to ASCII using
     the Unidecode library (https://pypi.python.org/pypi/Unidecode)
  3. "basic_cleaners" if you do not want to transliterate (in this case, you should also update
     the symbols in symbols.py to match your data).
'''

import re
from unidecode import unidecode
from .numbers import normalize_numbers


# Regular expression matching whitespace:
_whitespace_re = re.compile(r'\s+')

# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations = [(re.compile('\\b%s\\.' % x[0], re.IGNORECASE), x[1]) for x in [
  ('mrs', 'misess'),
  ('mr', 'mister'),
  ('dr', 'doctor'),
  ('st', 'saint'),
  ('co', 'company'),
  ('jr', 'junior'),
  ('maj', 'major'),
  ('gen', 'general'),
  ('drs', 'doctors'),
  ('rev', 'reverend'),
  ('lt', 'lieutenant'),
  ('hon', 'honorable'),
  ('sgt', 'sergeant'),
  ('capt', 'captain'),
  ('esq', 'esquire'),
  ('ltd', 'limited'),
  ('col', 'colonel'),
  ('ft', 'fort'),
]]

# List of (regular expression, replacement) pairs for Marathi abbreviations:
_marathi_abbreviations = [(re.compile('\\b%s\\.' % x[0], re.IGNORECASE), x[1]) for x in [
  ('डॉ', 'doctor'),
  ('श्री', 'shri'),
  ('कु', 'kumari'),
  ('सौ', 'saumati'),
  ('प्रा', 'professor'),
]]


def expand_abbreviations(text):
  for regex, replacement in _abbreviations:
    text = re.sub(regex, replacement, text)
  return text


def expand_marathi_abbreviations(text):
  for regex, replacement in _marathi_abbreviations:
    text = re.sub(regex, replacement, text)
  return text


def expand_numbers(text):
  return normalize_numbers(text)


def lowercase(text):
  return text.lower()


def collapse_whitespace(text):
  return re.sub(_whitespace_re, ' ', text)


def convert_to_ascii(text):
  return unidecode(text)


def basic_cleaners(text):
  '''Basic pipeline that lowercases and collapses whitespace without transliteration.'''
  text = lowercase(text)
  text = collapse_whitespace(text)
  return text


def transliteration_cleaners(text):
  '''Pipeline for non-English text that transliterates to ASCII.'''
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = collapse_whitespace(text)
  return text


def english_cleaners(text):
  '''Pipeline for English and Marathi text, including number and abbreviation expansion.'''
  # Check if text contains Devanagari characters (for Marathi)
  has_devanagari = any('\u0900' <= c <= '\u097F' for c in text)
  
  if has_devanagari:
    # Handle Marathi text
    try:
      from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
      normalizer = IndicNormalizerFactory().get_normalizer('mr')
      text = normalizer.normalize(text)
    except ImportError:
      # If library not available, continue without normalization
      pass
    
    # Expand Marathi abbreviations before converting to ASCII
    text = expand_marathi_abbreviations(text)
  else:
    # Handle English abbreviations for English text
    text = expand_abbreviations(text)
  
  # Common processing for both languages
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = expand_numbers(text)
  text = collapse_whitespace(text)
  text = text.replace('"', '')
  return text