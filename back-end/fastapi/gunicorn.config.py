"""gunicorn settings"""
import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
bind = "0.0.0.0:8000"
daemon = False

# ログ設定
accesslog = "-"
errorlog = "-"
loglevel = "warning"  # ログレベル ('debug', 'info', 'warning', 'error', 'critical')
