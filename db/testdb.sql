

INSERT INTO public.change_type (type_id, change_name) VALUES (1, 'Создание задачи');
INSERT INTO public.change_type (type_id, change_name) VALUES (2, 'Изменение статуса');
INSERT INTO public.change_type (type_id, change_name) VALUES (3, 'Изменение описания');
INSERT INTO public.change_type (type_id, change_name) VALUES (4, 'Изменение дедлайна');
INSERT INTO public.change_type (type_id, change_name) VALUES (5, 'Изменение исполнителя');
INSERT INTO public.change_type (type_id, change_name) VALUES (6, 'Изменение приоритета');
INSERT INTO public.change_type (type_id, change_name) VALUES (7, 'Изменение названия');



INSERT INTO public.users (user_id, surname, name, last_name, login, password, birthday, email_adress) VALUES (11, 'Григорьев', 'Дмитрий', 'Леонидович', 'dimas', 'scrypt:32768:8:1$61EBLhCSxlNE7P10$c6afd767faee355a0eee58c106cc6c429a136b4700eede82ff82cdbaeee6bb294d39e5da8345e10c0bed71f570bcca33de2aa51335b3b71300413ac2a3ae64d5', '2005-01-05', 'dimas.grigorev.055.7@gmail.com');
INSERT INTO public.users (user_id, surname, name, last_name, login, password, birthday, email_adress) VALUES (12, 'Григорьев', 'Денис', 'Leonidovich', 'den123', 'scrypt:32768:8:1$rM7bqHfYKmqRPW6D$6d3f325362a79159d22a4001a1103e1236f27e3b53e6249fe743891fd3dc4a06d9fc52523558838729778dadf76ef882b24705cb1c9020559a42699dab653992', '2005-01-05', 'denis.grigorev056@gmail.com');
INSERT INTO public.users (user_id, surname, name, last_name, login, password, birthday, email_adress) VALUES (13, 'Григорьев', 'Дмитрий', 'Леонидович', 'dimas2', 'scrypt:32768:8:1$pEUMS3xnfbfdDPbR$39a534cd498430555ec0589e38050cce9a41c44233a5bf4d338031850736de5b9d0788ddef08102dc4db33f2bb0c37254f55759280bd1fa88ef519a4dc2630b8', '2005-01-05', 'dimas.grigorev.055.7@gmail.com');



INSERT INTO public.project (project_id, creator_project_id, name, date_of_creation, description) VALUES (20, 11, 'тест проект после добавления записи в парт проджек', '2025-12-21', 'тест');
INSERT INTO public.project (project_id, creator_project_id, name, date_of_creation, description) VALUES (22, 12, 'Проектирование архитектуры приложения', '2025-12-21', 'lallalalal123');
INSERT INTO public.project (project_id, creator_project_id, name, date_of_creation, description) VALUES (23, 12, '<p>lala</p>', '2025-12-21', 'asdasd');
INSERT INTO public.project (project_id, creator_project_id, name, date_of_creation, description) VALUES (24, 11, 'тест1 фикс багов', '2025-12-21', '3455235342');
INSERT INTO public.project (project_id, creator_project_id, name, date_of_creation, description) VALUES (25, 11, 'тест проект2 фикс багов', '2025-12-21', 'фикс');
INSERT INTO public.project (project_id, creator_project_id, name, date_of_creation, description) VALUES (26, 11, 'фикс роута с добавлением юзеров в проект', '2025-12-21', 'добавление юзеров в проект (создание совместного проекта с отдельными задачами для каждого пользователя)');
INSERT INTO public.project (project_id, creator_project_id, name, date_of_creation, description) VALUES (27, 13, 'Ещё один проект (тоже совместный для dimas)', '2025-12-22', 'Здесь я от dimas2 создал проект, создам пару задач себе, добавлю dimas и пару задач назначу ему');



INSERT INTO public.status (status_id, name) VALUES (1, 'Новая');
INSERT INTO public.status (status_id, name) VALUES (2, 'В работе');
INSERT INTO public.status (status_id, name) VALUES (3, 'На проверке');
INSERT INTO public.status (status_id, name) VALUES (4, 'Завершена');
INSERT INTO public.status (status_id, name) VALUES (5, 'Отложена');



INSERT INTO public.task (task_id, name, deadline, creator_id, executor_id, priority, status, description, status_id, project_id) VALUES (29, 'задача dimas для dimas ', '2025-12-30 23:04:00', 11, 11, 1, 'Новая', 'Задача от dimas - владелец самому себе dimas (владелец) = исполнитель ', 1, 26);
INSERT INTO public.task (task_id, name, deadline, creator_id, executor_id, priority, status, description, status_id, project_id) VALUES (23, '234', '2222-04-23 23:23:00', 12, 12, 2, 'Новая', '234234324324324324324324324324324', 1, 22);
INSERT INTO public.task (task_id, name, deadline, creator_id, executor_id, priority, status, description, status_id, project_id) VALUES (32, 'Таск1 себе (димас2)', '2026-12-31 12:20:00', 13, 13, 1, 'Новая', 'таск1 димас2', 1, 27);
INSERT INTO public.task (task_id, name, deadline, creator_id, executor_id, priority, status, description, status_id, project_id) VALUES (33, 'Таск2 себе (димас2)', '2026-12-12 12:42:00', 13, 13, 1, 'Новая', 'таск2 себе димасу2', 1, 27);
INSERT INTO public.task (task_id, name, deadline, creator_id, executor_id, priority, status, description, status_id, project_id) VALUES (34, 'Таск1 юзеру dimas', '2026-12-12 14:45:00', 13, 11, 1, 'Новая', 'Таск1 dimas`у', 1, 27);
INSERT INTO public.task (task_id, name, deadline, creator_id, executor_id, priority, status, description, status_id, project_id) VALUES (35, 'Таск2 юзеру dimas', '2026-03-12 12:04:00', 13, 11, 2, 'Новая', 'Проверь эти задачи у себя в совместном проекте', 1, 27);
INSERT INTO public.task (task_id, name, deadline, creator_id, executor_id, priority, status, description, status_id, project_id) VALUES (22, 'вжэдлфыв', '2223-03-12 12:03:00', 12, 12, 1, 'В работе', 'ы.двлоьаыдвлаьывю.а23-98469234234sqwwfdf''sdf''sdflkhsdkljf230u4230320[p9', 1, 22);
INSERT INTO public.task (task_id, name, deadline, creator_id, executor_id, priority, status, description, status_id, project_id) VALUES (18, 'ТЕСТ6 ЗАДАЧА СЕБЕ', '2025-12-31 23:59:00', 11, 11, 2, 'Новая', 'ТЕСТ6', 1, 20);
INSERT INTO public.task (task_id, name, deadline, creator_id, executor_id, priority, status, description, status_id, project_id) VALUES (24, '123', '9999-11-11 09:55:00', 12, 12, 2, 'Новая', '1231231', 1, 23);
INSERT INTO public.task (task_id, name, deadline, creator_id, executor_id, priority, status, description, status_id, project_id) VALUES (16, 'тест2 назначаю задачу другому от владельца', '2025-12-24 19:00:00', 11, NULL, 1, 'Новая', '2', 1, 20);
INSERT INTO public.task (task_id, name, deadline, creator_id, executor_id, priority, status, description, status_id, project_id) VALUES (17, 'ТЕСТ3 НАЗНАЧАЮ ДРУГОГО ИСПОЛНИТЕЛЯ', '2025-12-24 20:00:00', 11, NULL, 1, 'Новая', '3', 1, 20);
INSERT INTO public.task (task_id, name, deadline, creator_id, executor_id, priority, status, description, status_id, project_id) VALUES (25, '2342135', '9999-03-12 12:53:00', 11, 11, 1, 'Новая', '235215', 1, 24);
INSERT INTO public.task (task_id, name, deadline, creator_id, executor_id, priority, status, description, status_id, project_id) VALUES (26, '1252353', '2026-05-12 03:59:00', 11, 11, 1, 'Новая', '24125125', 1, 24);
INSERT INTO public.task (task_id, name, deadline, creator_id, executor_id, priority, status, description, status_id, project_id) VALUES (27, '234124', '5551-03-12 23:15:00', 11, 11, 1, 'Новая', '241242', 1, 24);
INSERT INTO public.task (task_id, name, deadline, creator_id, executor_id, priority, status, description, status_id, project_id) VALUES (28, 'задача для добавленного юзера dimas2 от dimas', '2025-12-30 14:40:00', 11, 13, 2, 'Новая', 'Задача с изменённым исполнителем (dimas - владелец создал задачу и назначил исполнителем юзера dimas2 - участник проекта). Он добавлен сразу после создания проекта. Но разумеется, dimas2 был зарегистрирован в системе на момент его добавления в проект.', 1, 26);

INSERT INTO public.change (change_id, change_author, user_author_id, type, task_id, data_change, change_type_id) VALUES (32, 'den123', 12, 'Изменение описания', 22, '2025-12-21 22:06:57.33422', 3);
INSERT INTO public.change (change_id, change_author, user_author_id, type, task_id, data_change, change_type_id) VALUES (33, 'den123', 12, 'Изменение описания', 22, '2025-12-21 22:07:11.716299', 3);
INSERT INTO public.change (change_id, change_author, user_author_id, type, task_id, data_change, change_type_id) VALUES (34, 'den123', 12, 'Изменение статуса', 22, '2025-12-21 22:07:19.388708', 2);
INSERT INTO public.change (change_id, change_author, user_author_id, type, task_id, data_change, change_type_id) VALUES (35, 'den123', 12, 'Изменение приоритета', 22, '2025-12-21 22:07:28.357133', 6);
INSERT INTO public.change (change_id, change_author, user_author_id, type, task_id, data_change, change_type_id) VALUES (36, 'den123', 12, 'Изменение описания', 22, '2025-12-21 22:07:41.265795', 3);
INSERT INTO public.change (change_id, change_author, user_author_id, type, task_id, data_change, change_type_id) VALUES (37, 'dimas', 11, 'Изменение приоритета', 18, '2025-12-21 22:11:55.806794', 6);


INSERT INTO public.role (role_id, role_name) VALUES (1, 'владелец');
INSERT INTO public.role (role_id, role_name) VALUES (2, 'участник');


INSERT INTO public.part_in_project (participation_id, user_id, role_name, date_add_to_project, project_id, role_id) VALUES (13, 11, 'владелец', '2025-12-21 00:37:03.72648', 20, 1);
INSERT INTO public.part_in_project (participation_id, user_id, role_name, date_add_to_project, project_id, role_id) VALUES (16, 12, 'владелец', '2025-12-21 21:45:39.359375', 22, 1);
INSERT INTO public.part_in_project (participation_id, user_id, role_name, date_add_to_project, project_id, role_id) VALUES (25, 12, 'владелец', '2025-12-21 21:56:06.373576', 23, 1);
INSERT INTO public.part_in_project (participation_id, user_id, role_name, date_add_to_project, project_id, role_id) VALUES (27, 11, 'владелец', '2025-12-21 22:21:51.374633', 24, 1);
INSERT INTO public.part_in_project (participation_id, user_id, role_name, date_add_to_project, project_id, role_id) VALUES (28, 11, 'владелец', '2025-12-21 22:22:51.816525', 25, 1);
INSERT INTO public.part_in_project (participation_id, user_id, role_name, date_add_to_project, project_id, role_id) VALUES (30, 11, 'владелец', '2025-12-21 23:37:41.745687', 26, 1);
INSERT INTO public.part_in_project (participation_id, user_id, role_name, date_add_to_project, project_id, role_id) VALUES (31, 13, 'участник', '2025-12-21 23:38:01.156383', 26, 2);
INSERT INTO public.part_in_project (participation_id, user_id, role_name, date_add_to_project, project_id, role_id) VALUES (33, 13, 'владелец', '2025-12-22 03:48:39.129114', 27, 1);
INSERT INTO public.part_in_project (participation_id, user_id, role_name, date_add_to_project, project_id, role_id) VALUES (34, 11, 'участник', '2025-12-22 03:51:00.880992', 27, 2);

