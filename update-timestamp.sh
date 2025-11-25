#!/bin/bash
# 最終更新日時を自動更新するスクリプト（JST）

TIMESTAMP=$(TZ=Asia/Tokyo date '+%Y-%m-%d %H:%M:%S JST')

# profiles.jsonの最終更新日時を更新
sed -i "s/\"lastUpdated\": \".*\"/\"lastUpdated\": \"$TIMESTAMP\"/" data/profiles.json

echo "✅ 最終更新日時を更新しました: $TIMESTAMP"
