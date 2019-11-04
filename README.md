# Лабораторные работы по дисциплине "Компьютерное моделирование" на факультете ПМИ, НГТУ
&nbsp;  

## 1. Знакомство с используемым программным инструментарием
### Условия задачи

Научиться использовать выбранное для научных расчетов ПО (такое как пакеты SciPy и SymPy языка Python) для решения различных вычислительных задач; научиться писать программы на соответствующем языке программирования.  

1) Решить уравнение 
![](https://latex.codecogs.com/svg.latex?2x%5E3-11x%5E2&plus;12x-9%3D0)
2) Создать на диске текстовый файл с каким-нибудь содержимым. Прочитать его и вывести на экран. Затем записать в этот же файл двойную копию прочитанного.
3) Написать процедуру, производящую сортировку списка методом пузырька. Сравнить правильность её работы со встроенной в язык функцией сортировки.
4) Найти производную выражения 
![](https://latex.codecogs.com/svg.latex?sin%28x%29cos%28x%5E2%29tan%28y%29&plus;ln%28x%29) 
по переменной *x*.
5) Решить интегралы 
![](https://latex.codecogs.com/svg.latex?%5Cint%20x%5E2%283&plus;4x%29%5E2dx) 
и 
![](https://latex.codecogs.com/svg.latex?%5Cint_%7B%5Cfrac%7B%5Cpi%7D%7B2%7D%7D%5E%7B%5Cpi%7D%20%5Cfrac%7Bsin%28x%29%7D%7Bcos%28x%5E2%29&plus;1%7Ddx).
6) Нарисовать график функции на отрезке *[0; 50]*.
7) Нарисовать гистограмму для указанных данных.  
&nbsp;  

## 2. Моделирование равномерно распределённых случайных величин
### Условия задачи

Научиться моделировать значения равномерно распределённой случайной величины и проводить статистический анализ сгенерированных данных. Построить генератор, дающий для заданного вида генератора достаточно качественную псевдослучайную последовательность.

Написать программу, выполняющую следующие действия:
1) Считывание из файла входных данных, необходимых для работы программы в автоматическом режиме;
2) Генерация последовательности псевдослучайных чисел длиной *N* с помощью заданного в варианте генератора (*N* не меньше *1000*) или с помощью стандартного генератора, встроенного в использованный при написании программы язык программирования в зависимости от заданного во входном файле параметра;
3) Выделение периода *T* в сгенерированной последовательности (*T* не меньше *100*; если *T < 100*, то выход из программы с сохранением в результирующих файлах соответствующей информации); далее под сгенерированной последовательностью будем понимать выделенный период длиной *T* и обрабатывать только его;
4) Для сгенерированной последовательности проверка выполнения теста №1 при 
![](https://latex.codecogs.com/svg.latex?%5Calpha%20%3D0.05)
для *n = 40* и *n = 100*;
5) Для сгенерированной последовательности проверка выполнения теста №2 при 
![](https://latex.codecogs.com/svg.latex?%5Calpha%20%3D0.05)
, *n = 40*, *n = 100* и заданном в варианте количестве интервалов *K*;
6) Для сгенерированной последовательности проверка выполнения теста №3 при заданных в варианте количестве подпоследовательностей r, количестве интервалов *K* и длинах подпоследовательностей *40 / r*,  *100 / r*; 
7) Проверка гипотезы о согласии распределения сгенерированной последовательности с равномерным распределением по критерию 
![](https://latex.codecogs.com/svg.latex?%5Cchi%5E2); 
для группирования выбирать интервалы равной длины, выбранное число интервалов должно быть обосновано, уровень значимости 
![](https://latex.codecogs.com/svg.latex?%5Calpha%20%3D0.05);
8) Проверка гипотезы о согласии распределения сгенерированной последовательности с равномерным распределением по непараметрическому критерию, заданному в варианте; уровень значимости 
![](https://latex.codecogs.com/svg.latex?%5Calpha%20%3D0.05);
9) В результате выполнения программы должно быть создано следующее:  
    * файл, содержащий всю сгенерированную последовательность (содержимое файла должно быть доступно при сдаче, но распечатывать его содержимое не обязательно);  
    *  файл, содержащий только период последовательности (содержимое файла должно быть доступно при сдаче, но распечатывать его содержимое не обязательно);  
    *  файл, содержащий заданные параметры, длину выделенного периода, описание результатов выполнения всех тестов и критериев (значения статистик, достигнутых уровней значимости, выводы об успешности теста и другая важная информация), а также общий вывод о том, является ли сгенерированная последовательность равномерной псевдослучайной последовательностью;  
    *  графики для теста №2 (гистограммы, столбцы которых отражают частоты попаданий в каждый интервал); график, построенный по группированным для критерия
![](https://latex.codecogs.com/svg.latex?%5Cchi%5E2)
данным; для теста №3 графики выводить не нужно.

Варьируя входные данные, с помощью написанной программы для заданного в варианте генератора подобрать его параметры так, чтобы получилась наиболее качественная псевдослучайная последовательность.  
С помощью написанной программы оценить качество псевдослучайной последовательности, создаваемой генератором, встроенным в использованный при написании программы язык программирования.  
### Исходные данные
| Генератор | Критерий  | Параметр теста №2 | Параметры теста №3 |
| :--------:| :---------:|:---------:|:---------:|
| ![](https://latex.codecogs.com/svg.latex?x_%7Bn&plus;1%7D%3D%28ax_%7Bn%7D%5E%7B2%7D&plus;bx_%7Bn%7D&plus;c%29%5Cmod%20m)   | Критерий Колмогорова | ![](https://latex.codecogs.com/svg.latex?K%3D20) | ![](https://latex.codecogs.com/svg.latex?r%3D3%20%5Cnewline%20K%3D8) |

&nbsp;  

## 3. Моделирование дискретно распределённых случайных величин
### Условия задачи

Научиться моделировать значения дискретно распределённой случайной величины и проводить статистический анализ сгенерированных данных.

Написать программу, выполняющую следующие действия:
1)	считывает из файла входные данные, необходимые для работы программы в автоматическом режиме;
2)	содержит функцию, генерирующую равномерно распределённые псевдослучайные числа с помощью генератора, встроенного в использованный при написании программы язык программирования;
3)	с помощью заданного в варианте алгоритма генерирует 2 последовательности дискретно распределённых псевдослучайных чисел, подчиняющихся заданному в варианте закону распределения: одна – длиной 40, другая – 100 чисел;
4)	определяет эффективность алгоритма, вычисляя количество операций, которое потребовалось для генерации последовательности;
5)	проверяет по критерию 
![](https://latex.codecogs.com/svg.latex?%5Cchi%5E2) 
гипотезу о согласии распределения 
(уровень значимости ![](https://latex.codecogs.com/svg.latex?%5Calpha%20%3D0.05)) 
каждой сгенерированной последовательности с заданным в варианте распределением; группирования как такого нет: вместо интервалов в 
![](https://latex.codecogs.com/svg.latex?%5Cchi%5E2) 
рассматриваются возможные реализации случайной величины 
![](https://latex.codecogs.com/svg.latex?%5Cxi_%7Bi%7D),
соответствующие им теоретические вероятности 
![](https://latex.codecogs.com/svg.latex?P%28%5Cxi_%7Bi%7D%29) 
и эмпирические частоты выпадения реализаций 
![](https://latex.codecogs.com/svg.latex?%5Cxi_%7Bi%7D), вычисляемые как 
![](https://latex.codecogs.com/svg.latex?%5Cfrac%7Bn_%7Bi%7D%7D%7Bn%7D)
(
![](https://latex.codecogs.com/svg.latex?n_%7Bi%7D) – сколько раз в выборке встретилось значение 
![](https://latex.codecogs.com/svg.latex?%5Cchi%5E2), 
![](https://latex.codecogs.com/svg.latex?n) 
– общий объем выборки), единственный интервал может представлять собой бесконечное подмножество реализаций 
![](https://latex.codecogs.com/svg.latex?%5Cxi_%7Bi%7D)
, больших определенного значения, для которых теоретическая вероятность, умноженная на объем выборки 
![](https://latex.codecogs.com/svg.latex?nP%28%5Cxi_%7Bi%7D%29%5Cleq%201).
6)	выполняет шаги 3–5 для нестандартного алгоритма, моделирующего распределение Пуассона;
7)	в результате выполнения создаёт следующее:  
    * файлы, содержащие каждую сгенерированную последовательность;  
    * файл, содержащий описание результатов проверки всех критериев (значения статистик, достигнутых уровней значимости, выводы об успешности теста и другая важная информация), результаты измерения эффективности алгоритмов;  
    * графики, построенные по группированным для критерия
    ![](https://latex.codecogs.com/svg.latex?%5Cchi%5E2) данным (гистограммы, столбцы которых отражают количество попаданий в каждый интервал);  
    * графики с «теоретическими» вероятностями 
    ![](https://latex.codecogs.com/svg.latex?P_%7Bi%7D) 
    моделируемого закона распределения (гистограммы, столбцы которых отражают теоретические вероятности появления элемента последовательности в соответствующие интервалы).  
    
Для всех заданных в варианте параметров распределений, а также для нестандартного алгоритма, моделирующего распределение Пуассона, получить последовательности псевдослучайных чисел, определить эффективность алгоритмов, оценить качество полученных последовательностей.
