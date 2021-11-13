# Who Wants to Be a Millionaire!

# quick start

```
git clone this repo
cd millionaire

virtualenv -p python3 venv
source venv/bin/activate

cp main_app/.env.example main_app/.evn
vim main_app/.env

pip install -r requirements/dev.txt
python manage.py npminstall
python manage.py migrate
```
