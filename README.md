# Стеганографическая программа PVD(Pixel Value Difference) на Python

Этот проект является реализацией PVD, которая позволяет скрыть текстовое сообщение в изображении. Для этого используется изменение значений пикселей изображения таким образом, чтобы эти изменения были незаметны для человеческого глаза.

## Установка

1. Убедитесь, что у вас установлен Python версии 3.x.
2. Установите необходимые библиотеки, запустив команду:

    ```
    pip install pillow numpy
    ```

## Использование

Поместите изображение, в которое хотите скрыть сообщение, в корневой каталог проекта. Для примера в файле использован файл `Lenna.png`.
После выполнения программы появится новое изображение `out.png`, в котором будет скрыто ваше сообщение.

## Извлечение сообщения

Поместите изображение, в котором хотите раскрыть сообщение, в корневой каталог проекта. Для примера в файле использован файл `out.png`.
 
## Важно

- Эта программа работает только с текстом на латинице.

## Теоритические сведения

В методе разности значений пикселей (Pixel Value Difference, PVD) [4] изображение разбивается на непересекающиеся пары пикселей (P_i,P_(i+1) ) и для каждой пары считается разность их значений d_k=P_i-P_(i+1), k=(i+1)/2. 

Абсолютное значение разности пары пикселей |d_k | попадает в один из шести отрезков вида [l_k,u_k ]. Эти отрезки заданы заранее и обычно определяются следующим образом: [0, 7], [8, 15], [16, 31], [32, 63], [64, 127], [128, 255].

Количество битов сообщения, которое может быть встроено в пару пикселей (P_i,P_(i+1) ), определяется по формуле 
n_k=log_2⁡〖(u_k-l_k+1)〗.	

Далее фрагмент сообщения длиной n_k битов представляется в виде целого числа m_k и вычисляется новое значение разности d_k* для данной пары пикселей по формуле

d_k*= l_k+m_k, если d_k≥0 или -(l_k+m_k ), если d_k<0
        
Встраивание фрагмента сообщения m_k в пару пикселей осуществляется по формуле:

(P_i',P_(i+1)' ) = (P_i+⌈((d_k*-d_k ))/2⌉ ,P_(i+1)-⌊((d_k*-d_k ))/2⌋), если d_k  -нечетное 

или (P_i+⌊((d_k*-d_k ))/2⌋ ,P_(i+1)-⌈((d_k*-d_k ))/2⌉), если d_k  -четное.  

Извлечение сообщения выполняется по формуле	
m_k=|P_i'-P_(i+1)'|-l_k.

