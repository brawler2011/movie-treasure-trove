#!/bin/sh
set -e

# Если в примонтированном томе /app/data базы еще нет, копируем сид-базу
if [ ! -f /app/data/bot_database.db ] && [ -f /app/seed_database.db ]; then
    echo "Инициализация постоянной базы данных из предварительно подготовленного сида..."
    cp /app/seed_database.db /app/data/bot_database.db
fi

# Запуск процесса с пониженным приоритетом CPU (nice 10), чтобы ОС и SSH не зависали
if command -v nice >/dev/null 2>&1; then
    exec nice -n 10 "$@"
else
    exec "$@"
fi

