#!/usr/bin/env python3
"""
既存のprofiles.jsonに shopname フィールドを追加する移行スクリプト
何度実行しても安全（既にshopnameがある場合はスキップ）
"""

import json
import os
from urllib.parse import urlparse


def extract_shopname_from_url(url):
    """
    Booth URLからショップ名を抽出

    Args:
        url: アバター作者URL

    Returns:
        str: ショップ名（抽出できない場合は空文字）
    """
    if not url or "booth.pm" not in url:
        return ""

    try:
        parsed = urlparse(url)
        hostname = parsed.netloc

        # サブドメインを抽出
        # 例: mio3works.booth.pm → mio3works
        parts = hostname.split('.')
        if len(parts) >= 3 and parts[-2] == 'booth':
            return parts[0]
    except Exception:
        pass

    return ""


def add_shopname_field(json_path):
    """
    profiles.jsonに shopname フィールドを追加

    Args:
        json_path: profiles.jsonのパス
    """
    print("=" * 80)
    print("shopname フィールド追加スクリプト")
    print("=" * 80)

    # JSONファイルを読み込み
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    profiles = data.get("profiles", [])
    updated_count = 0
    skipped_count = 0

    print(f"\n総プロファイル数: {len(profiles)}")
    print("\n処理中...")
    print("-" * 80)

    for profile in profiles:
        profile_id = profile.get("id", "unknown")
        avatar_name = profile.get("avatarName", "")

        # 既に shopname が存在する場合はスキップ
        if "shopname" in profile:
            skipped_count += 1
            shopname_value = profile.get("shopname", "")
            print(f"[{profile_id}] {avatar_name}: shopname already exists ('{shopname_value}'), skipped")
            continue

        # avatarAuthorUrl から shopname を抽出
        avatar_author_url = profile.get("avatarAuthorUrl", "")
        shopname = extract_shopname_from_url(avatar_author_url)

        # shopname フィールドを追加
        profile["shopname"] = shopname
        updated_count += 1

        if shopname:
            print(f"[{profile_id}] {avatar_name}: added shopname = '{shopname}'")
        else:
            print(f"[{profile_id}] {avatar_name}: added shopname = '' (empty)")

    print("-" * 80)
    print(f"\n更新されたプロファイル数: {updated_count}")
    print(f"スキップされたプロファイル数: {skipped_count}")

    # 更新がある場合のみ書き戻し
    if updated_count > 0:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n✅ {json_path} を更新しました")
        return True
    else:
        print("\n✅ 更新は必要ありませんでした")
        return False


def main():
    # profiles.jsonのパス
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    json_path = os.path.join(repo_root, "data", "profiles.json")

    if not os.path.exists(json_path):
        print(f"エラー: {json_path} が見つかりません")
        return 1

    updated = add_shopname_field(json_path)
    print("=" * 80)

    # 更新があった場合は終了コード0、なければ0（どちらも成功扱い）
    return 0


if __name__ == "__main__":
    exit(main())
