# ML Alarm — Лабораторна робота №3

> **Студент:** [ПІБ]  
> **Група:** [Група]  
> **Лабораторна робота:** №3 — Розробка Web-додатка засобами Javascript/VueJS  
> **Завдання:** Адаптувати програмний код ЛР№2 до вимог фреймворку VueJS та забезпечити завантаження даних з Web-сервера.  
> **Звіт:** [Посилання на Google Drive]

---

## Опис додатку

**ML Alarm** — веб-додаток для управління будильниками з повноцінною авторизацією користувачів.

### Функціональність:
- Реєстрація та вхід (JWT-авторизація)
- Перегляд та редагування профілю
- Додавання, вмикання/вимкнення та видалення будильників
- Звуковий сигнал при спрацюванні будильника
- Збереження даних у SQLite через REST API

---

## Технологічний стек

| Рівень      | Технології                                    |
|-------------|-----------------------------------------------|
| **Frontend** | Vue 3, Vite, Pinia, Vue Router, Axios, Bootstrap 5 |
| **Backend**  | Python, Flask, Flask-CORS                     |
| **База даних** | SQLite (вбудована)                          |
| **Безпека**  | JWT (PyJWT), bcrypt                           |

---

## Структура проєкту

```
ml-alarm/
├── server/                  # Python Flask бекенд
│   ├── app.py               # Головний файл сервера (REST API)
│   ├── requirements.txt     # Залежності Python
│   └── ml_alarm.db          # SQLite база даних (генерується)
│
└── client/                  # Vue 3 + Vite фронтенд
    ├── index.html
    ├── vite.config.js
    ├── src/
    │   ├── main.js           # Точка входу
    │   ├── App.vue           # Кореневий компонент
    │   ├── api.js            # Axios клієнт
    │   ├── router/
    │   │   └── index.js      # Vue Router
    │   ├── stores/
    │   │   ├── auth.js       # Pinia: авторизація
    │   │   └── alarms.js     # Pinia: будильники
    │   ├── components/
    │   │   ├── AppNavbar.vue # Навігаційна панель
    │   │   ├── AppFooter.vue # Підвал
    │   │   ├── AlarmCard.vue # Картка будильника
    │   │   └── AlarmRing.vue # Оверлей спрацювання
    │   └── views/
    │       ├── HomeView.vue      # Головна / будильники
    │       ├── LoginView.vue     # Авторизація
    │       ├── RegisterView.vue  # Реєстрація
    │       ├── ProfileView.vue   # Профіль
    │       └── AboutView.vue     # Про додаток
```

---

## Схема Vue-компонентів

```
App.vue
├── AppNavbar.vue       ← auth store (isLoggedIn, logout)
├── RouterView
│   ├── HomeView.vue    ← alarms store (fetch/add/toggle/remove)
│   │   ├── AlarmCard.vue
│   │   └── AlarmRing.vue
│   ├── LoginView.vue   ← auth store (login)
│   ├── RegisterView.vue← auth store (register)
│   ├── ProfileView.vue ← auth store (user, updateProfile)
│   └── AboutView.vue
└── AppFooter.vue
```

---

## REST API

| Метод    | Ендпоінт              | Опис                         | Auth |
|----------|-----------------------|------------------------------|------|
| `POST`   | `/api/auth/register`  | Реєстрація нового користувача | —    |
| `POST`   | `/api/auth/login`     | Вхід, отримання JWT токену   | —    |
| `GET`    | `/api/auth/me`        | Дані поточного користувача   | ✅   |
| `PATCH`  | `/api/auth/me`        | Оновлення профілю            | ✅   |
| `GET`    | `/api/alarms`         | Список будильників           | ✅   |
| `POST`   | `/api/alarms`         | Створення будильника         | ✅   |
| `PATCH`  | `/api/alarms/:id`     | Оновлення будильника         | ✅   |
| `DELETE` | `/api/alarms/:id`     | Видалення будильника         | ✅   |

---

## Запуск проєкту

### 1. Бекенд (Flask сервер)

```bash
cd server
pip install -r requirements.txt
python app.py
# Сервер запускається на http://localhost:5000
```

### 2. Фронтенд (Vue + Vite)

```bash
cd client
npm install
npm run dev
# Додаток відкривається на http://localhost:5173
```

> Vite автоматично проксує `/api/*` запити на `http://localhost:5000`
