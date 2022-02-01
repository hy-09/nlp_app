FROM mysql:5.7.28
RUN touch /var/log/mysql/mysqld.log
RUN apt update \
    && apt install -y --no-install-recommends \
    vim \
    && apt -y clean \
    && rm -rf /var/lib/apt/lists/*