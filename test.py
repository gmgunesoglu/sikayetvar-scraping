import re

# Verilen string
texts = [
    "7 sa 6 dk 21 sn",
    "6 dk 21 sn",
    "7 sa 6 dk",
    "7 sa 21 sn"
]

# Regex deseni
pattern = r'(?:(\d+)\s*sa)?\s*(?:(\d+)\s*dk)?\s*(?:(\d+)\s*sn)?'

for text in texts:
    # Eşleşmeyi bulma
    match = re.match(pattern, text)

    if match:
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        
        print("Saat:", hours)
        print("Dakika:", minutes)
        print("Saniye:", seconds)
        print("---")
    else:
        print("Eşleşme bulunamadı.")
