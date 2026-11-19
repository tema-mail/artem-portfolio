#!/bin/zsh
cd ${0:A:h}
./run.sh nsk2 "16:9, горизонтальная" "$(cat p-nsk2.txt)"
./run.sh nsk2-story "9:16, вертикальная" "$(cat p-nsk2-story.txt)"
