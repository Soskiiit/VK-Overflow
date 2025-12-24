### Как потестить
0. Если не имеем apache benchmark и nginx - устанавливаем. Устанавливаем gunicorn. 
1. Запускаем nginx 
    ```shell
    sudo nginx -c $PWD/nginx.conf 
    ```
2. Запускаем тесты
    ```shell
    ./test.sh
    ```

3. Рекомендуется убить nginx
    ```shell
    sudo nginx -c $PWD/nginx.conf -s stop
    ```
