# Stage Money Backend
Django RestFramework project for Stage Money APP.


#### PythonAnyWhere Config:
- Clone repository (HTTPS)
- cat build.sh (check venv: if venv already exist -> "workon venv")
- ./build.sh
- Remplace DEBUG with EXTERNAL_HOSTNAME into .env 
- Create Web section (Django, Py3.10)
    - Configure Web section:
        - Source code (path)
        - Working directory (path)
        - WSGI configuration file
            ```bash
            import os
            import sys

            path = '/home/stagemoneyback/stage-money' #source-code
            if path not in sys.path:
                sys.path.append(path)

            os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

            from django.core.wsgi import get_wsgi_application
            application = get_wsgi_application()
        - Virtualenv (path to venv: working_directory + /.virtualenvs/venv)
        - Clear Static files (delete urls)
        - Security. Force HTTPS: Enabled

