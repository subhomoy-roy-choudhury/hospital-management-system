echo "[+] Loading Environment Variables form .env"
# For All Platform (MacOS, Windows, Linux)
while IFS= read -r line
do
    if [[ ! "$line" =~ ^\# && -n "$line" ]]; then
        export "$line"
    fi
done < ".env"

python main/manage.py runserver