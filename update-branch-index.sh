#!/bin/bash

# Script: update-branch-index.sh
# Location: /var/web_server/update-branch-index.sh
# Purpose: Scans the HOST directory /var/web_server/htdocs and generates TWO index files:
#          1. admin/index.html (for /admin/ URL)
#          2. branches/index.html (for /branches/ URL)

echo "Updating admin and branches index pages..."

# --- Configuration ---
HOST_WEB_ROOT="/var/web_server/htdocs" # HOST path where branches are deployed

ADMIN_INDEX_FILE="${HOST_WEB_ROOT}/admin/index.html"
BRANCHES_INDEX_FILE="${HOST_WEB_ROOT}/branches/index.html"

# List of directory/file names at HOST_WEB_ROOT level to exclude from branch lists
EXCLUDE_ITEMS=("main_book_root" "admin" "draft" "branches" "default.conf" "he" "static" "figures" "book" "frontend" "backend") # Add other non-branch items if needed

# --- Scan for branch directories on HOST ---
echo "Scanning for branches in $HOST_WEB_ROOT..."
branch_names=() # Array to store found branch names
while IFS= read -r -d $'\0'; do
    item_path="$REPLY"
    if [ -d "$item_path" ]; then # Check if it's a directory
        branch_name=$(basename "$item_path")
        should_exclude=0
        # Check against exclusion list
        for exclude in "${EXCLUDE_ITEMS[@]}"; do
            if [[ "$branch_name" == "$exclude" ]]; then
                should_exclude=1
                break
            fi
        done
        # Add to list if not excluded
        if [ $should_exclude -eq 0 ]; then
            echo "  Found branch directory: $branch_name"
            branch_names+=("$branch_name")
        fi
    fi
done < <(find "$HOST_WEB_ROOT" -maxdepth 1 -mindepth 1 -print0) # Find items in HOST_WEB_ROOT

# Sort branch names alphabetically
IFS=$'\n' sorted_branch_names=($(sort <<<"${branch_names[*]}"))
unset IFS


# --- Generate admin/index.html ---
echo "Generating $ADMIN_INDEX_FILE..."
ADMIN_TMP_FILE=$(mktemp)

# HTML Header and common styles
cat << 'HTML_HEAD' > "$ADMIN_TMP_FILE"
<!DOCTYPE html>
<html>
<head>
  <title>HE Staff Book - Admin View</title> <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background-color: #f5f5f5; }
    .container { max-width: 800px; margin: 0 auto; padding: 20px; background-color: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    h1, h2 { color: #00A6D6; } /* TU Delft Blue */
    h1 { border-bottom: 2px solid #00A6D6; padding-bottom: 10px; }
    ul { list-style-type: none; padding: 0; }
    li { margin-bottom: 10px; padding: 10px; background-color: #f8f8f8; border-radius: 4px; word-wrap: break-word; }
    a { color: #00A6D6; text-decoration: none; font-weight: bold; }
    a:hover { text-decoration: underline; }
    .special-link { margin-bottom: 20px; padding: 15px; background-color: #e6f7ff; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>HE Staff Book - Admin View</h1>
HTML_HEAD

# Fixed links for admin page
cat << 'ADMIN_LINKS' >> "$ADMIN_TMP_FILE"
    <div class="special-link">
      <a href="/">Main Branch Book</a> - The primary production version
    </div>
    <div class="special-link">
      <a href="/draft/">Draft Branch Book</a> - The current development version
    </div>
    <div class="special-link">
       <a href="/branches/">View Branches Page (/branches/)</a>
    </div>

    <h2>All Other Deployed Branch Versions:</h2>
    <ul>
ADMIN_LINKS

# Add dynamic branch list to admin page
found_branches_count=${#sorted_branch_names[@]}
if [ $found_branches_count -gt 0 ]; then
    for branch_name in "${sorted_branch_names[@]}"; do
        # Escape potential special characters in branch name for HTML safety
        escaped_branch_name=$(echo "$branch_name" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g; s/"/\&quot;/g; s/'"'"'/\&#39;/g')
        # Link uses the dynamic branch location structure: /<branch_name>/
        echo "      <li><a href=\"/${escaped_branch_name}/\">${escaped_branch_name}</a></li>" >> "$ADMIN_TMP_FILE"
    done
else
    echo "      <li>No other branches found.</li>" >> "$ADMIN_TMP_FILE"
fi

# HTML Footer for admin page
cat << 'HTML_FOOT' >> "$ADMIN_TMP_FILE"
    </ul>
  </div>
</body>
</html>
HTML_FOOT

# Move temp file to actual admin index file
mkdir -p "${HOST_WEB_ROOT}/admin" # Ensure admin dir exists
mv "$ADMIN_TMP_FILE" "$ADMIN_INDEX_FILE"
if [ $? -ne 0 ]; then
  echo "::error::Failed to move temporary file to $ADMIN_INDEX_FILE"
  rm -f "$ADMIN_TMP_FILE" # Clean up
else
   chmod 644 "$ADMIN_INDEX_FILE"
   echo "Admin index updated at $ADMIN_INDEX_FILE"
fi


# --- Generate branches/index.html ---
echo "Generating $BRANCHES_INDEX_FILE..."
BRANCHES_TMP_FILE=$(mktemp)

# HTML Header (reuse style, change title)
cat << 'HTML_HEAD' > "$BRANCHES_TMP_FILE"
<!DOCTYPE html>
<html>
<head>
  <title>HE Staff Book - Deployed Versions</title> <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background-color: #f5f5f5; }
    .container { max-width: 800px; margin: 0 auto; padding: 20px; background-color: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    h1, h2 { color: #00A6D6; } /* TU Delft Blue */
    h1 { border-bottom: 2px solid #00A6D6; padding-bottom: 10px; }
    ul { list-style-type: none; padding: 0; }
    li { margin-bottom: 10px; padding: 10px; background-color: #f8f8f8; border-radius: 4px; word-wrap: break-word; }
    a { color: #00A6D6; text-decoration: none; font-weight: bold; }
    a:hover { text-decoration: underline; }
    .special-link { margin-bottom: 20px; padding: 15px; background-color: #e6f7ff; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>HE Staff Book - Deployed Versions</h1>
HTML_HEAD

# Fixed links for branches page (like user's original script)
cat << 'BRANCHES_LINKS' >> "$BRANCHES_TMP_FILE"
    <div class="special-link">
      <a href="/">Main Branch Book</a> (Root)
    </div>
    <div class="special-link">
      <a href="/admin/">Admin Page</a>
    </div>
    <div class="special-link">
      <a href="/draft/">Draft Branch Book</a>
    </div>

    <h2>Other Deployed Branches:</h2>
    <ul>
BRANCHES_LINKS

# Add dynamic branch list to branches page (using the same list)
if [ $found_branches_count -gt 0 ]; then
    for branch_name in "${sorted_branch_names[@]}"; do
        escaped_branch_name=$(echo "$branch_name" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g; s/"/\&quot;/g; s/'"'"'/\&#39;/g')
        echo "      <li><a href=\"/${escaped_branch_name}/\">${escaped_branch_name}</a></li>" >> "$BRANCHES_TMP_FILE"
    done
else
    echo "      <li>No other branch versions found deployed.</li>" >> "$BRANCHES_TMP_FILE"
fi

# HTML Footer for branches page
cat << 'HTML_FOOT' >> "$BRANCHES_TMP_FILE"
    </ul>
  </div>
</body>
</html>
HTML_FOOT

# Move temp file to actual branches index file
mkdir -p "${HOST_WEB_ROOT}/branches" # Ensure branches dir exists
mv "$BRANCHES_TMP_FILE" "$BRANCHES_INDEX_FILE"
if [ $? -ne 0 ]; then
  echo "::error::Failed to move temporary file to $BRANCHES_INDEX_FILE"
  rm -f "$BRANCHES_TMP_FILE" # Clean up
else
   chmod 644 "$BRANCHES_INDEX_FILE"
   echo "Branches index updated at $BRANCHES_INDEX_FILE"
fi


echo "Index update script finished."
exit 0