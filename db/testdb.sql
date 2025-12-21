
INSERT INTO public.change_type VALUES (1, 'Создание задачи');
INSERT INTO public.change_type VALUES (2, 'Изменение статуса');
INSERT INTO public.change_type VALUES (3, 'Изменение описания');
INSERT INTO public.change_type VALUES (4, 'Изменение дедлайна');
INSERT INTO public.change_type VALUES (5, 'Изменение исполнителя');
INSERT INTO public.change_type VALUES (6, 'Изменение приоритета');
INSERT INTO public.change_type VALUES (7, 'Изменение названия');

INSERT INTO public.role VALUES (1, 'владелец');
INSERT INTO public.role VALUES (2, 'участник');


INSERT INTO public.users VALUES (1, 'Иванов', 'Иван', 'Иванович', 'ivanov_ii', 'password123', '1990-05-15', 'ivanov@mail.ru');
INSERT INTO public.users VALUES (2, 'Петров', 'Петр', 'Петрович', 'petrov_pp', 'qwerty456', '1985-12-20', 'petrov@yandex.ru');
INSERT INTO public.users VALUES (4, 'Козлов', 'Алексей', 'Дмитриевич', 'kozlov_ad', 'alex1234', '1988-03-10', 'kozlov@mail.ru');
INSERT INTO public.users VALUES (5, 'Николаева', 'Елена', 'Владимировна', 'nikolaeva_ev', 'lena567', '1995-11-25', 'nikolaeva@yandex.ru');
INSERT INTO public.users VALUES (6, 'Федоров', 'Дмитрий', 'Александрович', 'fedorov_da', 'dima890', '1991-07-18', 'fedorov@gmail.com');
INSERT INTO public.users VALUES (7, 'Дмитрий', 'Григорьев', 'Леонидович', 'deemassg', '123456', '2005-01-05', 'dimas.grigorev.055.7@gmail.com');
INSERT INTO public.users VALUES (8, 'Денис', 'Григорьев', 'Леонидович', 'den', '1234567', '2005-01-05', 'denis.grigorev.055.7@gmail.com');
INSERT INTO public.users VALUES (9, 'Megafon', 'Android', 'Andreevich', 'MegaAndroid', '123456', '1000-01-01', 'megafon.android.055.7@gmail.com');
INSERT INTO public.users VALUES (10, 'sdfsalf', 'sdgasg', 'sadgasg', 'abc', '123456', '1111-11-11', 'abc@gmail.com');
INSERT INTO public.users VALUES (3, 'Сидорова', 'Мария', 'Сергеевна', 'sidorova_ms', 'maria789', '1992-08-03', 'sidorova@gmail.com');


INSERT INTO public.project VALUES (2, 3, 'Веб-сайт компании', '2024-02-01', 'Разработка корпоративного веб-сайта с системой управления контентом');
INSERT INTO public.project VALUES (3, 2, 'Автоматизация отчетности', '2024-01-20', 'Система автоматической генерации отчетов для отдела аналитики');
INSERT INTO public.project VALUES (4, 4, 'Интеграция с API', '2024-02-10', 'Интеграция с внешними API сервисами для синхронизации данных');
INSERT INTO public.project VALUES (5, 3, 'Первый пробный проект', '2025-12-15', 'Создать задачи внутри первого проекта. Для этого сначала нужно закончить роут с созданием задач)');
INSERT INTO public.project VALUES (8, 1, 'Четвертый пробный проект', '2025-12-15', '');
INSERT INTO public.project VALUES (9, 1, 'Пятый пробный проект', '2025-12-15', '');
INSERT INTO public.project VALUES (11, 1, 'Android', '2025-12-15', '');
INSERT INTO public.project VALUES (12, 1, 'Проект Димаса и MC Крутой', '2025-12-15', '');
INSERT INTO public.project VALUES (13, 1, 'Посмотрим', '2025-12-15', '');
INSERT INTO public.project VALUES (14, 1, 'сколько', '2025-12-15', '');
INSERT INTO public.project VALUES (15, 1, 'проектов можно создать если записать очень ', '2025-12-15', '');
INSERT INTO public.project VALUES (1, 1, 'Разработка мобильного приложения.', '2024-01-15', 'Создание кроссплатформенного мобильного приложения для управления задачами');
INSERT INTO public.project VALUES (6, 1, 'Второй (изменённый) пробный проект', '2025-12-15', 'Создал  ещё один пробный проект, их будет много - для теста. Описание кстати необязательное) ТЕПЕРЬ МЕНЯЮ ОПИСАНИЕ И НАЗВАНИЕ ПРОЕКТА => всё работает!!!');
INSERT INTO public.project VALUES (16, 1, '12345678', '2025-12-17', '12345678');


INSERT INTO public.status VALUES (1, 'Новая');
INSERT INTO public.status VALUES (2, 'В работе');
INSERT INTO public.status VALUES (3, 'На проверке');
INSERT INTO public.status VALUES (4, 'Завершена');
INSERT INTO public.status VALUES (5, 'Отложена');


INSERT INTO task VALUES (3, 'Разработка авторизации', '2024-03-15', 1, 4, 3, 'Новая', 'Реализовать систему регистрации и авторизации пользователей', 1, 1);
INSERT INTO task VALUES (4, 'Главная страница', '2024-03-10', 2, 5, 1, 'На проверке', 'Сверстать главную страницу сайта согласно макету', 3, 2);
INSERT INTO task VALUES (5, 'Бэкенд для форм', '2024-03-20', 3, 2, 2, 'В работе', 'Разработать бэкенд для обработки форм обратной связи', 2, 2);
INSERT INTO task VALUES (6, 'Генерация отчетов', '2024-02-25', 4, 6, 1, 'Завершена', 'Настроить автоматическую генерацию еженедельных отчетов', 4, 3);
INSERT INTO task VALUES (7, 'Аутентификация API', '2024-03-05', 1, 4, 2, 'В работе', 'Реализовать систему аутентификации для внешнего API', 2, 4);
INSERT INTO task VALUES (8, 'Синхронизация данных', '2024-03-25', 4, 5, 3, 'Новая', 'Настроить синхронизацию данных между системами', 1, 4);
INSERT INTO task VALUES (1, 'Проектирование архитектуры приложения', '2025-12-15', 1, 8, 1, 'Новая', 'SDAT ZAVTRA!!!!!!!! Разработать архитектуру мобильного приложения и выбрать технологии для разработки. Примечание - мягкий дедлайн пятница след недели, жесткий - зачетная неделя Jestkiy jmon', 2, 1);
INSERT INTO task VALUES (2, 'Дизайн интерфейса', '2026-02-28', 3, 3, 2, 'В работе', 'Создать дизайн-макеты основных экранов приложения', 2, 1);
INSERT INTO task VALUES (9, 'Первая пробная задача', '2025-12-17', 3, 3, 3, 'Новая', 'Первая пробная задача , щас всё протестим', 1, 2);
INSERT INTO task VALUES (10, 'Первая пробная задача', '2025-12-17', 3, 3, 3, 'Новая', 'Первая пробная задача , щас всё протестим', 1, 2);
INSERT INTO task VALUES (13, 'hahhahah', '2222-12-12', 3, 2, 1, 'Новая', 'eqrwet', 1, 1);
INSERT INTO task VALUES (11, 'ТЕСТ1 НАЗНАЧАЮ ДРУГОГО ИСПОЛНИТЕЛЯ', '8888-08-08', 3, 2, 2, 'Новая', 'ТЕСТ ТЕСТ ТЕСТ добавил поля с айди статуса и айди проекта в апдейт. Создаю задачу, назначая другого исполнителя. Всё создалось. Теперь я могу редактировать её', 1, 1);


INSERT INTO public.change VALUES (1, 'ivanov_ii', 1, 'Создание задачи', 1, '2024-02-01 09:00:00', 1);
INSERT INTO public.change VALUES (2, 'sidorova_ms', 3, 'Создание задачи', 2, '2024-02-01 10:30:00', 1);
INSERT INTO public.change VALUES (3, 'ivanov_ii', 1, 'Создание задачи', 3, '2024-02-02 11:15:00', 1);
INSERT INTO public.change VALUES (4, 'petrov_pp', 2, 'Изменение статуса', 1, '2024-02-03 14:20:00', 2);
INSERT INTO public.change VALUES (5, 'petrov_pp', 2, 'Создание задачи', 4, '2024-02-05 16:45:00', 1);
INSERT INTO public.change VALUES (6, 'sidorova_ms', 3, 'Создание задачи', 5, '2024-02-06 09:30:00', 1);
INSERT INTO public.change VALUES (7, 'kozlov_ad', 4, 'Создание задачи', 6, '2024-02-07 11:00:00', 1);
INSERT INTO public.change VALUES (8, 'petrov_pp', 2, 'Изменение статуса', 4, '2024-02-08 13:15:00', 2);
INSERT INTO public.change VALUES (9, 'kozlov_ad', 4, 'Изменение статуса', 6, '2024-02-10 15:40:00', 2);
INSERT INTO public.change VALUES (10, 'ivanov_ii', 1, 'Создание задачи', 7, '2024-02-12 10:20:00', 1);
INSERT INTO public.change VALUES (11, 'kozlov_ad', 4, 'Создание задачи', 8, '2024-02-13 12:30:00', 1);
INSERT INTO public.change VALUES (12, 'nikolaeva_ev', 5, 'Изменение описания', 2, '2024-02-14 14:50:00', 3);
INSERT INTO public.change VALUES (13, 'fedorov_da', 6, 'Изменение дедлайна', 6, '2024-02-15 16:10:00', 4);


INSERT INTO public.part_in_project (participation_id, user_id, role_name, date_add_to_project, project_id, role_id) VALUES
(1, 1, 'owner', '2024-01-15 09:00:00', 1, 1),    
(2, 2, 'member', '2024-01-15 10:00:00', 1, 2),   
(3, 3, 'member', '2024-01-15 11:00:00', 1, 2),   
(4, 4, 'member', '2024-01-20 12:00:00', 1, 2),
(5, 2, 'owner', '2024-02-01 09:00:00', 2, 1),
(6, 3, 'member', '2024-02-01 10:00:00', 2, 2),
(7, 5, 'member', '2024-02-05 11:00:00', 2, 2),
(8, 4, 'owner', '2024-01-20 09:00:00', 3, 1), 
(9, 6, 'member', '2024-01-25 10:00:00', 3, 2),
(10, 1, 'owner', '2024-02-10 09:00:00', 4, 1),
(11, 4, 'member', '2024-02-10 10:00:00', 4, 2),
(12, 5, 'member', '2024-02-12 11:00:00', 4, 2);


