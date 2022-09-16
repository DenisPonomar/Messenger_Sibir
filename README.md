# Мессенджер Сибирь
Мессенджер Сибирь - это бесплатный мессенджер на python с открытым исходным кодом, позволяющий пользователь обмениваться сообщениями. Сервер различает пользователей по индивидуальному токену, генерируемый при старте приложения, который посылается получателю в виде хэш-токена, созданного с помощью SHA-256.

# Что нового
* Версия 2.0
  * Добавлены комментарии в коде
  * Исправлены баги с отображением времени сообщения
  * Теперь при запуске приложение просит ввести токен
  * Добавлена полоса прокрутки в окне сообщений
  * Теперь сообщения, которые не показываются, не рендерятся, что увеличило производительность
  * Если отображается окно избранного, не показывааются кнопки изменения контакта и удаления
  * Доработано окно настроек
    * Добавлен горизонтальный слайдер, отвечающий за цвет блока сообщения
    * Добавлена кнопка сброса настроек
* Версия 3.0
  * Исправлены баги с отображением блока сообщения, содержащий перенсённый текст
  * Добавлена возможность выделять блоки сообщений
  * Добавлена возможность копировать и изменять (если оно отправлено не позже 86400 секунд назад) сообщение, а также удалять одно или несколько сообщений
  * Ограничено длина имени контакта 24 символами
* Версия 4.0
  * Добавлен код сервера (папка server)
  * Клиентский код был перенесён в папку client
  * Добавлена возможность приёма и отправки сообщений
  * Исправлен баг, при котором не отображались очень большие сообщения при скроллинге
  * В настройках пункт "Скопировать токен" заменён на "Скопировать id"
  * Неотправленные сообщения в случае недоступности сервера будут отправлены в случае его доступности даже после перезапуска клиента
  * (!) Редактирование и удаление сообщений поддерживается только локально, также пока можно редактировать входящие сообщения. Будет исправлено в следующей версии.
  
# Зависимости
Для работы в системе должны быть установлены следующие библиотеки:
* pygame
* clipboard
* pygame_gui
* requests (добавлена в версии 4.0)
# Назначение файлов
* messenger_sibir_v_[номер версии].py - исполняемый файл
* colour.txt - содержит кортеж в виде RGBA, определяющий цвет фона
* colour_soob.txt - содержит кортеж в виде RGB, определяющий цвет блока сообщения (добавлен в версии 2.0)
* photo.txt - содержит путь до фонового изображениия, если файл пуст или путь неверный, цвет фона задаётся из файла colour.txt
* private.txt - содержит строковое значение "Мои контакты" или "Все пользователи", которое определяет, кто может писать пользователю (функциональность добавлена в версии 4.0)
* token.txt - содержит 64-битный токен пользователя в кодировке base16 (функциональность не разработана)
* vvod.json - содержит стили для элементов pygame_gui
# Назначение папок
Название папки - это id контакта пользователя, за исключением "15421" - это избранное.
Важно! Не добавляйте никакие папки, так как каждую папку программа считатет папкой контакта.
Состав папки:
* face.jpg - фото пользователя
* message.txt - переписка с пользователя, которая представлена в виде двумерного массивва, типа [['0K3RgtC+INCY0LfQsdGA0LDQvdC90L7QtSE=', '0', 1, 1]]:
  * '0K3RgtC+INCY0LfQsdGA0LDQvdC90L7QtSE=' - отдельное сообщение, закодированное в base64;
  * '0' - сообщение отправил пользователь (если '1', то контакт);
  * 1 - время в секундах в виде числа с плавающей точкой, прошедшее с 1 января 1970 года (00:00:00 (UTC))
  * 1 - сообщение доставлено до сервера, если 0, то не доставлено.
* name.txt - содержит имя пользователя

Язык запросов:
* Для проверки новых сообщений: http://+ip+/+a+&+token, где
  * & - знак умножения (*)
  * ip - ip-адрес и порт сервера
  * token - токен пользователя
* Входящих сообщений: hash_token_otpravitel+&+time_soob+&+text_soob, где
  * & - знак умножения (*)
  * hash_token_otpravitel - id (хэш-токен) пользователя
  * time_soob - серверное время приёма сообщения на сервере
  * text_soob - сообщение, закодированное в base64
* Для отправки сообщений: http://+ip+/+b+&+token+&+soob_pol_buffer+&+soob_bufer, где
  * & - знак умножения (*)
  * ip - ip-адрес и порт сервера
  * token - токен пользователя
  * soob_pol_buffer - id (хэш-токен) получателя
  * soob_bufer - сообщение, закодированное в base64
* Для ответа на сообщение: server_time, где
  * server_time - серверное время приёма сообщения на сервере

Кнопка с символом "+" оставлена для дальнейшей разработки и не является функциональной

![изображение](https://user-images.githubusercontent.com/104255472/189518821-cb8c0725-4e26-4073-9ca0-7bef6e1084e0.png)
![изображение](https://user-images.githubusercontent.com/104255472/189518810-350f0712-f691-4277-ba9e-eebe5f47fa46.png)
![изображение](https://user-images.githubusercontent.com/104255472/189518842-a95d6d6c-3260-477e-a76c-6b6ec84eaf7b.png)
![изображение](https://user-images.githubusercontent.com/104255472/189518874-9a266095-f9f0-416d-ad36-3263845673c4.png)
![изображение](https://user-images.githubusercontent.com/104255472/189518903-8f0831eb-fbd9-481e-ba47-ff5fd5f2ce06.png)
![изображение](https://user-images.githubusercontent.com/104255472/189518944-fe620bf6-1ed8-4dca-870e-a9bfa1a18333.png)
