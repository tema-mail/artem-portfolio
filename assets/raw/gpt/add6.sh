#!/bin/zsh
# Добавить шестого парня (guy3-src.jpg) в готовые варианты. Строго по одному. Промт – p-add6.txt.
export PATH=$HOME/.local/node/bin:$HOME/.local/bin:$PATH
prompt=$(cat p-add6.txt)
for v in "$@"; do
  out="$v-6.png"; [[ -f "$out" ]] && continue
  python3 -c "from PIL import Image; Image.open('$v.png').convert('RGB').save('$v-ref.jpg', quality=92)"
  codex exec -m gpt-5.6-sol -c model_reasoning_effort=low -s workspace-write --skip-git-repo-check -C "$PWD" \
    -i "$v-ref.jpg" -i guy3-src.jpg -o "$v-6.log" "Отредактируй изображение встроенным imagegen, пропорции 9:16. Приложены 2 картинки: image 1 = $v-ref.jpg (исходник), image 2 = guy3-src.jpg (лицо нового человека) – передай обе генератору как референсы.
Скопируй текст между маркерами в imagegen дословно, символ в символ.

=== НАЧАЛО ПРОМТА ===
$prompt
=== КОНЕЦ ПРОМТА ===

Сохрани результат как $PWD/$out. API-ключи и scripts/image_gen.py не используй." < /dev/null > "$v-6.out" 2>&1
  echo "$v $(ls -la $out 2>&1 | awk '{print $5}')"
done
