import os
import multiprocessing

THREADS_PER_PAGE = multiprocessing.cpu_count() * 2

CSRF_ENABLED     = False

DATABASE_URL = os.environ['DATABASE_URL']
