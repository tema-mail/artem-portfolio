#!/bin/zsh
# Ждём сброса лимита imagegen (Plus) и добиваем v4, v6 с шестым парнем. Пробуем раз в 30 мин, до 12 попыток.
cd "${0:A:h}"
sleep 15600
for i in {1..12}; do
  ./add6.sh v4 v6
  if [[ -f v4-6.png && -f v6-6.png ]]; then
    S=~/Downloads/teyes-storis/shestero; mkdir -p $S
    python3 -c "
from PIL import Image
for v,n in (('v4','4-idut-6'),('v6','6-solnce-6')):
    Image.open(f'{v}-6.png').convert('RGB').resize((1080,1920),Image.LANCZOS).save(f'$S/{n}.jpg',quality=92)"
    echo "готово на попытке $i"; exit 0
  fi
  sleep 1800
done
echo "не вышло за 12 попыток"; exit 1
