import os
import aspose.words as aw
from natsort import natsorted

FROM_EXT = os.getenv('FROM_EXT')
TO_EXT = os.getenv('TO_EXT')

print(f'ENV: FROM [.{FROM_EXT}] TO [.{TO_EXT}]')

from_files = natsorted([
  f for f in os.listdir(f'/workspace/{FROM_EXT}') if f.endswith(f'.{FROM_EXT}')
])

for from_file in from_files:
  to_file = from_file.replace('.' + FROM_EXT, '.' + TO_EXT)

  print(f'⌛️ {from_file}')

  if os.path.exists(f'/workspace/{TO_EXT}/{to_file}'):
    print(f'👉 {to_file} already exists')
    continue

  doc = aw.Document(f'/workspace/{FROM_EXT}/{from_file}')
  doc.save(f'/workspace/{TO_EXT}/{to_file}')

  print(f'✅ {to_file}')
