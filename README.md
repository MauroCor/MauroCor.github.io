# Stage Money Backend
Django RestFramework project for Stage Money APP.


#### PythonAnyWhere Config:
- Clone repository
- .build.sh (if venv already exist -> "workon venv")
- Create Web section (Django, Py3.10)
- Remplace DEBUG by EXTERNAL_HOSTNAME into .env 
- Configure Web section:
    - Source code (path)
    - Working directory (path)
    - WSGI configuration file
        ```bash
        import os
        import sys

        path = '/home/stagemoneyback/stage-money'
        if path not in sys.path:
            sys.path.append(path)

        os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
    - VirtualEnv (path to venv)
