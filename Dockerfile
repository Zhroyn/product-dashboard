FROM selenium/standalone-chrome:latest
WORKDIR /app
COPY ./backend .
RUN sudo mv /usr/lib/python3.12/EXTERNALLY-MANAGED /usr/lib/python3.12/EXTERNALLY-MANAGED.backup
RUN sudo pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]