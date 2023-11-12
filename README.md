# hw3_ui

In this task I was supposed to link my HTML to some API using both Get and Post methods. The page should also render together with execuded script. 

Here is the task: 

**Критерии выполненного задания:**
* Есть функция, получающая данные с сервера (`GET`)
* Есть функция, отправляющие данные на сервер (`POST`/`PUT`/`PATCH`)
* Есть функция, динамически формирующая вёрстку с данными, которые были получены с сервера

So I have decided to make my own small API with Yandex Cloud. 

In the `main.py` you can see the code of the API. It saves data to YDB and gets it from there. 
The start page is the `register.html`. The user supposed to provide required data and click 'Create Account'. He would be redirected to another page, where will be greeted accordingly. 
The method `POST` is used on the page `register.html`, the method `GET` is used on page `profile.html`, and the page formatting is formed together with the data gathered from the server. 

## The link to demonstration: [VIDEO](https://drive.google.com/file/d/1NHJ15HxxvV9qDyS9-o0NjGLuWONbh-7e/view?usp=sharing)
