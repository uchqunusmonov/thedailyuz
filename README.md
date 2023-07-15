# thedailyuz

<h5>
  # redisni ishga tushurish uchun:
  
  $ docker run -it --rm --name redis -p 6379:6379 redis

  # celery ni ishga tushirish:

  $ celery -A config worker -l info

  # celery beat ni ishga tushirish:

  $ celery -A config beat -l info
</h5>
