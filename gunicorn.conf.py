bind = '0.0.0.0:8080' 

workers = 3

worker_class = "gevent" 

worker_connections = 200 #Simultaneous maximum connection number

pidfile = 'gunicorn.pid' #pid file

proc_name = 'guni_web' # Process name

timeout = 30 # thread timeout