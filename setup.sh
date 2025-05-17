#!/usr/bin/env bash

set -euo pipefail

VENV_DIR=".venv"
REQUIREMENTS_FILES=$(find . -type f -name "requirements.txt")
SECRETS_DIR="secrets"
HOME_DIR=$(pwd)
ZIP_DIRECTORY_NAME="2135_mini_finance"
ZIP_NAME="${ZIP_DIRECTORY_NAME}.zip"
TEMPLATE_LINK="https://www.tooplate.com/zip-templates/${ZIP_NAME}"
PYTHON_APP_DIR="$HOME_DIR/app"

# shellcheck disable=SC2181
if [[ $? -ne 0 ]] && [[ $1 != "source" ]]; then
    echo ".venv will not be activated."
    echo "Usage: source ./script.sh"
fi

if ! command -v python3 &> /dev/null; then
    echo "Installing python3"
    sudo apt-get install python3
fi

if [[ ! -d "${VENV_DIR}" ]];then
    echo "Creating virtual environment in $VENV_DIR"
    python3 -m venv "$VENV_DIR"
fi

if [[ $? -eq 1 ]];then
    # shellcheck disable=SC1091
    source $VENV_DIR/bin/activate
fi

echo "Upgrading pip..."
pip install --upgrade pip

for REQUIREMENTS_FILE in $REQUIREMENTS_FILES;do
    if [[ -f "${REQUIREMENTS_FILE}" ]];then
        echo "Installing python requirements."
        pip install -r "${REQUIREMENTS_FILE}"
    else
        echo "No ${REQUIREMENTS_FILE} file"
    fi
done

if [[ ! -d "secrets" ]];then
    mkdir "${SECRETS_DIR}"
    cat <<EOF > "${SECRETS_DIR}/secrets.json"
{
  "username": "",
  "password": ""
}
EOF
else
    rm -rf "app/${SECRETS_DIR}"
    rm -rf "mongodb/${SECRETS_DIR}"
    cp -r "${SECRETS_DIR}" "app/${SECRETS_DIR}"
    cp -r "${SECRETS_DIR}" "mongodb/${SECRETS_DIR}"
fi

sudo apt-get install -y yq jq

if [[ ! -d "tmp" ]]; then
    mkdir tmp
else
    if [[ -f "${HOME_DIR}/tmp/${ZIP_NAME}" ]];then
        rm "${HOME_DIR}/tmp/${ZIP_NAME}"
    fi
fi

cd tmp && wget "${TEMPLATE_LINK}"
cd "${ZIP_DIRECTORY_NAME}"
cp -r "js/" "${PYTHON_APP_DIR}/" 
cp -r "css/" "${PYTHON_APP_DIR}/" 
cp -r "fonts/" "${PYTHON_APP_DIR}/" 
cp -r "images/" "${PYTHON_APP_DIR}/" 
rm -rf "${ZIP_DIRECTORY_NAME}"
cd "${HOME_DIR}"
