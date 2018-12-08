nohup spark-submit --packages mysql:mysql-connector-java:5.1.39

spark-submit --packages mysql:mysql-connector-java:5.1.39 --master=local[*] tasks.py

Apython3.6 -m celery -A tasks worker --loglevel=info --hostname=worker1@%h