# JobRecognizer

**JobRecognizer** - удобный веб-сервис, предоставляющий быструю и качественную обработку вакансий. <br>

Протестировать наше решение вы можете по ссылке: http://92.53.119.76:8000/ (на данный момент сайт не работает)

В гитхаб репозиторий не удалось загрузить файл с параметрами модели ('models/SPACY/vocab/vectors'). Нужно удалить все содержимое папки models/SPACY, подгрузить архим из google drive по ссылке : https://drive.google.com/drive/u/0/folders/19iQsjZ_SR5HW6UfJKssOW5PeIz0XDPsI и разархивировать его в папку models/SPACY
## Введение
Одной из самых основных проблем при просмотре вакансий является нечитаемость резюме: огромный текст, большое кол-во смайликов, очень много лишней информации, которую очень сложно структурировать. Из-за всего этого соискателю приходится тратить время на выискивание в описании нужных ему разделов, будь то: требования к соискателю, условия работы, обязанности и примечания, которые не должны попадать в первые три раздела, но будут полезны при поиске работы. 




<p align="center" width="100%">
    <img width="50%" src="https://github.com/sasniy/JobRecognizer/assets/54496303/b97a4862-de94-4cfe-b3fe-58f834a5f5d4">
    
</p>
                                      
<p align="center">
  Описание вакансии (пример взят с сайта avito.ru)
</p>
<br>
<p align="center" width="100%">
    <img width="50%" src="https://github.com/sasniy/JobRecognizer/assets/54496303/5bbe696d-7752-4b14-b9d0-de3ecec4b02b">
    
</p>


Наш сервис будет полезен всякому, кто желает сэкономить свое время, удобный и понятный интерфейс стремится помочь соискателям при поиске работы.

## Использование

Наш сервис в первую очередь ориенторован на формат excel - excel. Вы загружаете на сервер excel файл в котором должна быть столбец с описанием вакансии ('responsibilities' или 'description'), после чего можно скачать измененный датасет с новыми полями (Требования, условия, обязанности и примечания). Скачивание и предобработка данных займет какое-то время (на train датасет потребовалось около минуты).

Вы также можете попробовать формат text - table. В поле ввода текста можно ввести любой текст или нажать на кнопку "Пример", который возьмет шаблон данных. После чего в поле вывода текста появятся все найденные разделы.
<p align="center" width="120%">
    <img width="50%" src="https://github.com/sasniy/JobRecognizer/assets/54496303/dbf48522-0bc4-4ce0-9024-0be073670c0c">
</p>
<p align="center">
  Пример работы сайта
</p>

## Обучение, метрики, валидация, разметка

В качестве baseline модели была использована предобученная модель для распознования именнованных сущностей с библиотеки spacy. Полная предобработка данных, обучение и валидацию модели можно посмотреть в папке notebooks (файл model.ipynb). Сама модель находится в папке models.

В ходе исследования нашей задачи была отмечена плохая разметка данных(некоторые разделы выделялись неправильно или не до конца, половина полей вообще отсутствовала, либо перекрывалась другой, из-зз чего были проблемы с обучением). В связи с этим было решено самостоятельно вручную переразметить датасет(Оригинальный и переразмеченный датасеты находятся в папке data)

Валидация и проверка нашего решения осуществлялась с помощью нескольких метрик, таких как косинусное расстояние, macro f1 и расстояние Жаккара,полное исследование доступно в ноутбуке scores.ipynb (папка notebooks)

После обучения наша модель была протестирована на валидирующей выборке и на train датасете (новый файл находится в data/model_train.xlsx)

