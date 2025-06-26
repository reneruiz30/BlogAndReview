@echo off
cd /d F:\BlogAndReview-main\BlogAndReview\blogproject
call venv\Scripts\activate
pip install channels-redis redis
set DJANGO_SETTINGS_MODULE=blogproject.settings
set PYTHONPATH=F:\BlogAndReview-main\BlogAndReview\blogproject
python -m daphne blogproject.asgi:application -p 8002 