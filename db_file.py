import psycopg2


conn = psycopg2.connect(host="localhost", port=5432, database="bot", user="postgres", password="123")
cur = conn.cursor()
print("Database opened successfully")

'''
class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = psycopg2.connect(database)
        self.cursor = self.connection.cursor()
        print("Database opened successfully")

    def get_subscriptions(self, status=True):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM subscriptions WHERE status = %s ", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            self.cursor.execute(f'SELECT * FROM subscriptions WHERE user_id = {user_id}')
            query_results = self.cursor.fetchall()
            print(bool(len(query_results)))
            print(user_id)
            return bool(len(query_results))


    def add_subscriber(self, user_id, status=True):
        """Добавляем нового подписчика"""
        with self.connection:
            print(status)
            return self.cursor.execute(f"INSERT INTO subscriptions (user_id, status) VALUES(%s, %s)", (user_id, status))

    def update_subscription(self, user_id, status):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute(f"UPDATE subscriptions SET status = {status} WHERE user_id = {user_id}")

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
'''
