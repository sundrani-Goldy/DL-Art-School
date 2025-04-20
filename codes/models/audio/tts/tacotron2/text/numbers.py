""" from https://github.com/keithito/tacotron """

import inflect
import re


_inflect = inflect.engine()
_comma_number_re = re.compile(r'([0-9][0-9\,]+[0-9])')
_decimal_number_re = re.compile(r'([0-9]+\.[0-9]+)')
_pounds_re = re.compile(r'£([0-9\,]*[0-9]+)')
_dollars_re = re.compile(r'\$([0-9\.\,]*[0-9]+)')
_ordinal_re = re.compile(r'[0-9]+(st|nd|rd|th)')
_number_re = re.compile(r'[0-9]+')

# Marathi number mappings
_marathi_number_mapping = {
    '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
    '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
}
_marathi_number_re = re.compile(r'[०-९]+')
_marathi_decimal_re = re.compile(r'([०-९]+\.[०-९]+)')
_marathi_rupee_re = re.compile(r'₹([०-९\,]*[०-९]+)')


def _remove_commas(m):
  return m.group(1).replace(',', '')


def _expand_decimal_point(m):
  return m.group(1).replace('.', ' point ')


def _expand_dollars(m):
  match = m.group(1)
  parts = match.split('.')
  if len(parts) > 2:
    return match + ' dollars'  # Unexpected format
  dollars = int(parts[0]) if parts[0] else 0
  cents = int(parts[1]) if len(parts) > 1 and parts[1] else 0
  if dollars and cents:
    dollar_unit = 'dollar' if dollars == 1 else 'dollars'
    cent_unit = 'cent' if cents == 1 else 'cents'
    return '%s %s, %s %s' % (dollars, dollar_unit, cents, cent_unit)
  elif dollars:
    dollar_unit = 'dollar' if dollars == 1 else 'dollars'
    return '%s %s' % (dollars, dollar_unit)
  elif cents:
    cent_unit = 'cent' if cents == 1 else 'cents'
    return '%s %s' % (cents, cent_unit)
  else:
    return 'zero dollars'


def _expand_rupees(m):
  match = m.group(1)
  # Convert Marathi digits to English if needed
  for mar_digit, eng_digit in _marathi_number_mapping.items():
    match = match.replace(mar_digit, eng_digit)
    
  match = match.replace(',', '')
  
  if '.' in match:
    parts = match.split('.')
    if len(parts) > 2:
      return match + ' rupees'  # Unexpected format
    rupees = int(parts[0]) if parts[0] else 0
    paise = int(parts[1]) if len(parts) > 1 and parts[1] else 0
    
    if rupees and paise:
      rupee_unit = 'rupee' if rupees == 1 else 'rupees'
      paisa_unit = 'paisa' if paise == 1 else 'paise'
      return '%s %s, %s %s' % (rupees, rupee_unit, paise, paisa_unit)
    elif rupees:
      rupee_unit = 'rupee' if rupees == 1 else 'rupees'
      return '%s %s' % (rupees, rupee_unit)
    elif paise:
      paisa_unit = 'paisa' if paise == 1 else 'paise'
      return '%s %s' % (paise, paisa_unit)
    else:
      return 'zero rupees'
  else:
    rupees = int(match)
    rupee_unit = 'rupee' if rupees == 1 else 'rupees'
    return '%s %s' % (rupees, rupee_unit)


def _expand_ordinal(m):
  return _inflect.number_to_words(m.group(0))


def _expand_number(m):
  num = int(m.group(0))
  if num > 1000 and num < 3000:
    if num == 2000:
      return 'two thousand'
    elif num > 2000 and num < 2010:
      return 'two thousand ' + _inflect.number_to_words(num % 100)
    elif num % 100 == 0:
      return _inflect.number_to_words(num // 100) + ' hundred'
    else:
      return _inflect.number_to_words(num, andword='', zero='oh', group=2).replace(', ', ' ')
  else:
    return _inflect.number_to_words(num, andword='')


def _convert_marathi_to_english_digits(text):
  """Convert Marathi digits to English digits."""
  for mar_digit, eng_digit in _marathi_number_mapping.items():
    text = text.replace(mar_digit, eng_digit)
  return text


def normalize_numbers(text):
  """Normalize numbers in text (supports both English and Marathi)."""
  # Check for Marathi digits
  has_marathi_digits = any(char in _marathi_number_mapping for char in text)
  
  if has_marathi_digits:
    # Handle Marathi rupee symbols
    text = re.sub(_marathi_rupee_re, _expand_rupees, text)
    
    # Convert all Marathi digits to English
    text = _convert_marathi_to_english_digits(text)
  
  # Now process with the standard English normalization
  text = re.sub(_comma_number_re, _remove_commas, text)
  text = re.sub(_pounds_re, r'\1 pounds', text)
  text = re.sub(_dollars_re, _expand_dollars, text)
  text = re.sub(_decimal_number_re, _expand_decimal_point, text)
  text = re.sub(_ordinal_re, _expand_ordinal, text)
  text = re.sub(_number_re, _expand_number, text)
  
  return text