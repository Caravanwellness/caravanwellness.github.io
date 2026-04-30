#!/usr/bin/env python3
"""
Renames thumbnail images in articles.json to topic-based generic names.
Updates both the JSON references and the actual image files.
"""

import json
import os
import re

ARTICLES_JSON = "for onspire/accounts/39061852/articles.json"
ASSETS_DIR = "for onspire/assets"

# Priority keyword list - first match wins (case-insensitive, whole-word)
KEYWORDS = [
    "alcohol", "diabetes", "heart", "sleep", "anxiety", "stress", "trauma",
    "meditation", "cancer", "dementia", "alzheimer", "mental", "nutrition",
    "diet", "exercise", "fitness", "glp-1", "glp1", "weight", "endometriosis",
    "pregnancy", "fertility", "ovulation", "eye", "vision", "gut", "digestion",
    "caregiving", "caregiver", "social", "relationship", "friendship", "work",
    "career", "allergy", "spine", "breathing", "breathwork", "mindfulness",
    "gratitude", "journaling", "volunteering", "parenting", "menopause",
    "cholesterol", "stroke", "thyroid", "immunity", "inflammation", "vitamin",
    "supplement", "hydration", "posture", "stretching", "yoga", "pilates",
    "walking", "grief", "loneliness", "suicide", "ptsd", "addiction",
    "smoking", "tobacco",
]

STOP_WORDS = {
    "how", "the", "a", "an", "is", "are", "can", "for", "to", "of", "in",
    "with", "your", "our", "what", "why", "when", "and", "or", "at", "from",
    "by", "on", "as", "its", "their", "that", "this", "these", "those",
    "understanding", "exploring", "discover", "build", "creating", "choosing",
    "finding", "using", "managing", "navigating", "building", "making",
    "getting", "having", "taking", "living", "being", "becoming", "embracing",
    "tips", "guide", "basics", "facts", "signs", "ways", "types", "benefits",
    "effects", "behind", "through", "between", "after", "before", "during",
    "about", "across", "beyond", "within", "without", "into", "up", "down",
    "vs", "vs.", "amp", "&",
}


def extract_keyword(title: str) -> str:
    """Extract a topic keyword from an article title."""
    title_lower = title.lower()

    # Try priority keywords first (whole-word match)
    for kw in KEYWORDS:
        pattern = r'\b' + re.escape(kw) + r'\b'
        if re.search(pattern, title_lower):
            # Sanitize for filename (glp-1 -> glp1)
            return re.sub(r'[^a-z0-9]', '', kw)

    # Fallback: first significant word
    words = re.split(r'[\s\-_/,.:;!?()&]+', title_lower)
    for word in words:
        word = re.sub(r'[^a-z0-9]', '', word)
        if word and word not in STOP_WORDS and len(word) > 2:
            return word

    return "article"


def main():
    # Load articles.json
    with open(ARTICLES_JSON, encoding="utf-8") as f:
        data = json.load(f)

    articles = data["data"]
    print(f"Loaded {len(articles)} articles")

    # Build map: thumbnail_path -> English title (fallback to any title)
    thumb_to_title = {}
    for article in articles:
        thumb = article.get("thumbnail", "")
        if not thumb:
            continue
        # Prefer English titles
        if thumb not in thumb_to_title or article.get("language") == "en":
            thumb_to_title[thumb] = article["name"]

    unique_thumbs = sorted(thumb_to_title.keys())
    print(f"Found {len(unique_thumbs)} unique thumbnails")

    # Get existing files in assets dir
    existing_files = set(os.listdir(ASSETS_DIR))

    # Extract keyword for each thumbnail
    thumb_keyword = {}
    for thumb in unique_thumbs:
        title = thumb_to_title[thumb]
        kw = extract_keyword(title)
        thumb_keyword[thumb] = kw

    # Group thumbnails by keyword (sorted for deterministic numbering)
    from collections import defaultdict
    keyword_groups = defaultdict(list)
    for thumb in unique_thumbs:
        keyword_groups[thumb_keyword[thumb]].append(thumb)

    for kw in keyword_groups:
        keyword_groups[kw].sort()

    # Assign new names, avoiding conflicts with existing unreferenced files
    rename_map = {}  # old_basename -> new_basename
    used_names = set()  # new names already assigned this run

    for kw, thumbs in sorted(keyword_groups.items()):
        counter = 1
        for thumb in thumbs:
            old_basename = os.path.basename(thumb)
            # Find a free name
            while True:
                new_basename = f"{kw}-{counter}.png"
                # Skip if it exists in assets AND isn't a file we're about to rename away
                conflict = new_basename in existing_files and new_basename != old_basename
                duplicate = new_basename in used_names
                if not conflict and not duplicate:
                    break
                counter += 1
            rename_map[old_basename] = new_basename
            used_names.add(new_basename)
            counter += 1

    # Print planned renames
    print("\n=== PLANNED RENAMES ===")
    unchanged = 0
    for old, new in sorted(rename_map.items()):
        if old == new:
            unchanged += 1
        else:
            print(f"  {old!r:70s} -> {new!r}")
    print(f"  ({unchanged} files already had the target name)")

    # --- Execute renames ---
    missing_files = []
    renamed = 0

    for old_basename, new_basename in rename_map.items():
        if old_basename == new_basename:
            continue
        old_path = os.path.join(ASSETS_DIR, old_basename)
        new_path = os.path.join(ASSETS_DIR, new_basename)
        if not os.path.exists(old_path):
            missing_files.append(old_basename)
            continue
        os.rename(old_path, new_path)
        renamed += 1

    print(f"\nRenamed {renamed} files")
    if missing_files:
        print(f"\nWARNING: {len(missing_files)} files not found in assets/:")
        for f in missing_files:
            print(f"  MISSING: {f}")

    # --- Update articles.json ---
    updated = 0
    for article in articles:
        thumb = article.get("thumbnail", "")
        if not thumb:
            continue
        old_basename = os.path.basename(thumb)
        if old_basename in rename_map:
            new_basename = rename_map[old_basename]
            new_thumb = "assets/" + new_basename
            if new_thumb != thumb:
                article["thumbnail"] = new_thumb
                updated += 1

    with open(ARTICLES_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Updated {updated} thumbnail references in articles.json")

    # Report unreferenced files
    referenced_new = set(rename_map.values())
    all_after = (existing_files - set(rename_map.keys())) | set(rename_map.values())
    unreferenced_after = sorted(f for f in all_after if f.endswith(".png") and f not in referenced_new)
    if unreferenced_after:
        print(f"\n{len(unreferenced_after)} PNG files in assets/ not referenced by this account's articles.json:")
        for f in unreferenced_after:
            print(f"  {f}")

    print("\nDone.")


if __name__ == "__main__":
    main()
