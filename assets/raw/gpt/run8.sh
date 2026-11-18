#!/bin/zsh
# 8 вариантов сторис через Codex imagegen, строго по одному. Запуск из папки gpt.
export PATH=$HOME/.local/node/bin:$HOME/.local/bin:$PATH
base=$(cat base.txt)
while IFS='|' read -r name comp; do
  [[ -f "$name.png" ]] && continue
  codex exec -m gpt-5.6-sol -c model_reasoning_effort=low -s workspace-write --skip-git-repo-check -C "$PWD" \
    -i trio.jpg -i guy-glasses.jpg -i guy-leather.jpg -i bg.jpg -o "$name.log" "Сгенерируй одно изображение встроенным imagegen, пропорции 9:16 (вертикаль для Stories). Приложены 4 картинки-референса в порядке: image 1 = trio.jpg, image 2 = guy-glasses.jpg, image 3 = guy-leather.jpg, image 4 = bg.jpg – передай их генератору как референсы.
Скопируй текст между маркерами в imagegen дословно, символ в символ. Не перефразируй, не сокращай, не дополняй.

=== НАЧАЛО ПРОМТА ===
$base
$comp
=== КОНЕЦ ПРОМТА ===

Сохрани результат как $PWD/$name.png. API-ключи и scripts/image_gen.py не используй." < /dev/null > "$name.out" 2>&1
  echo "$name $(ls -la $name.png 2>&1 | awk '{print $5}')"
done < ${1:-variants.txt}
