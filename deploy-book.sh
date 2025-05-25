#!/bin/bash
set -e

# Deploys book content using host paths and basic chmod 755 permissions.

echo "Starting enhanced book deployment script"

# --- Input Arguments ---
BRANCH=${1}
CONTENT_SOURCE_DIR=${2}

# --- Validation ---
if [ -z "$BRANCH" ]; then echo "::error::Missing Branch name"; exit 1; fi
if [ -z "$CONTENT_SOURCE_DIR" ]; then echo "::error::Missing Content source directory"; exit 1; fi
if [ ! -d "$CONTENT_SOURCE_DIR" ]; then echo "::error::Content source directory '$CONTENT_SOURCE_DIR' not found"; exit 1; fi
if [ ! -f "$CONTENT_SOURCE_DIR/index.html" ]; then echo "::warning::index.html not found in '$CONTENT_SOURCE_DIR'."; fi

echo "Branch: $BRANCH"
echo "Content Source Directory: $CONTENT_SOURCE_DIR"

# --- Configuration ---
NGINX_WEB_ROOT="/var/web_server/htdocs" # HOST path
ADMIN_SOURCE_DIR="frontend"

# --- Determine Deployment Path ---
SANITIZED_BRANCH_NAME=$(echo "$BRANCH" | sed 's/[^a-zA-Z0-9]/-/g')
echo "Sanitized Branch Name: $SANITIZED_BRANCH_NAME"
DEPLOY_PATH_BOOK=""
DEPLOY_PATH_ADMIN=""
if [ "$BRANCH" == "main" ]; then
  DEPLOY_PATH_BOOK="$NGINX_WEB_ROOT/main_book_root"
  DEPLOY_PATH_ADMIN="$NGINX_WEB_ROOT/admin"
elif [ "$BRANCH" == "draft" ]; then
  DEPLOY_PATH_BOOK="$NGINX_WEB_ROOT/draft"
else
  DEPLOY_PATH_BOOK="$NGINX_WEB_ROOT/$SANITIZED_BRANCH_NAME"
fi

# --- Deploy Book Content ---
echo "Target book deployment path (Host): $DEPLOY_PATH_BOOK"
mkdir -p "$DEPLOY_PATH_BOOK"
if [ $? -ne 0 ]; then echo "::error::Failed to create directory $DEPLOY_PATH_BOOK"; exit 1; fi

echo "Cleaning $DEPLOY_PATH_BOOK..."
find "$DEPLOY_PATH_BOOK" -mindepth 1 -delete || echo "Warning: Cleaning $DEPLOY_PATH_BOOK might have encountered issues."
# Remove any empty directories that may remain (including old some_content)
find "$DEPLOY_PATH_BOOK" -type d -empty -delete || echo "Warning: Removing empty directories in $DEPLOY_PATH_BOOK might have encountered issues."

echo "Copying content from $CONTENT_SOURCE_DIR to $DEPLOY_PATH_BOOK..."
rsync -a --delete "$CONTENT_SOURCE_DIR/" "$DEPLOY_PATH_BOOK/"
if [ $? -ne 0 ]; then echo "::error::Failed to copy book content using rsync."; exit 1; fi

echo "Setting standard permissions (755) for $DEPLOY_PATH_BOOK..."
# Use sudo as the parent directory might require it to change permissions recursively
sudo chmod -R 755 "$DEPLOY_PATH_BOOK"
if [ $? -ne 0 ]; then echo "::error::Failed to set 755 permissions for $DEPLOY_PATH_BOOK."; exit 1; fi


# --- Deploy Admin Page (Only for Main Branch) ---
if [ "$BRANCH" == "main" ]; then
  echo "--- Deploying Admin Page ---"
  if [ -d "$ADMIN_SOURCE_DIR" ]; then
    echo "Admin source directory found: $ADMIN_SOURCE_DIR"
    echo "Target admin deployment path (Host): $DEPLOY_PATH_ADMIN"
    mkdir -p "$DEPLOY_PATH_ADMIN"
    if [ $? -ne 0 ]; then echo "::error::Failed to create directory $DEPLOY_PATH_ADMIN"; exit 1; fi

    echo "Cleaning $DEPLOY_PATH_ADMIN..."
    find "$DEPLOY_PATH_ADMIN" -mindepth 1 -delete || echo "Warning: Cleaning $DEPLOY_PATH_ADMIN might have encountered issues."

    echo "Copying admin content from $ADMIN_SOURCE_DIR to $DEPLOY_PATH_ADMIN..."
    rsync -a --delete "$ADMIN_SOURCE_DIR/" "$DEPLOY_PATH_ADMIN/"
    if [ $? -ne 0 ]; then echo "::error::Failed to copy admin content using rsync."; exit 1; fi

    echo "Setting standard permissions (755) for $DEPLOY_PATH_ADMIN..."
    sudo chmod -R 755 "$DEPLOY_PATH_ADMIN"
    if [ $? -ne 0 ]; then echo "::error::Failed to set 755 permissions for $DEPLOY_PATH_ADMIN."; exit 1; fi
  else
    echo "::warning::Admin source directory '$ADMIN_SOURCE_DIR' not found."
  fi

# --- Optional: Update Branch Index ---
UPDATE_SCRIPT="/var/web_server/update-branch-index.sh"
if [ -f "$UPDATE_SCRIPT" ]; then
  echo "Calling update-branch-index.sh script..."
  "$UPDATE_SCRIPT"
  if [ $? -ne 0 ]; then
      echo "::warning::Failed to update branch index using $UPDATE_SCRIPT."
  else
      echo "Branch index script finished."
  fi
else
    echo "Update branch index script ($UPDATE_SCRIPT) not found, skipping."
fi

echo "--- Deployment Summary ---"
echo "Branch: $BRANCH"
echo "Book content deployed to (Host Path): $DEPLOY_PATH_BOOK"
if [ "$BRANCH" == "main" ]; then
  if [ -n "$DEPLOY_PATH_ADMIN" ]; then
      if [ -d "$ADMIN_SOURCE_DIR" ]; then
          echo "Admin content deployed to (Host Path): $DEPLOY_PATH_ADMIN"
      else
          echo "Admin content deployment skipped (source directory '$ADMIN_SOURCE_DIR' not found)."
      fi
  fi
fi
echo "Deployment script finished successfully."
exit 0