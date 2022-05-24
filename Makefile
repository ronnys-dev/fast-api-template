include backend/.env
export
e=backend/.env


main.py:  # Запустить основное приложение
	python ./backend/main.py

beauty:  # запуск проверок перед коммитом
	pre-commit run --all-files
