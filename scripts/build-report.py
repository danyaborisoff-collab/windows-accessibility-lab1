"""Build an evidence-based PDF; requires reportlab and Pillow."""
from pathlib import Path
import os
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image
R=Path(__file__).resolve().parents[1]
regular=next((p for p in [Path(os.getenv('REPORT_FONT','/usr/share/fonts/msttcore/arial.ttf')),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')] if p.exists()),None)
bold=next((p for p in [Path('/usr/share/fonts/msttcore/arialbd.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')] if p.exists()),regular)
pdfmetrics.registerFont(TTFont('Body',str(regular)));pdfmetrics.registerFont(TTFont('Bold',str(bold)))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily('Body',normal='Body',bold='Bold')
W,H=595.276,841.89;M=42;AW=W-2*M
for image in (R/'evidence').glob('*.webp'):
    Image.open(image).convert('RGB').save(image.with_suffix('.jpg'), quality=87, optimize=True)
out=R/'REPORT.pdf';c=canvas.Canvas(str(out),pagesize=(W,H));c.setTitle('ЛР 1 — экранный доступ в Windows');c.setAuthor('Дмитрий Ярославов; Борисов Даниил; Чуров Александр; Иван Кожухин')
styles={
'body':ParagraphStyle('body',fontName='Body',fontSize=11,leading=15,textColor=colors.HexColor('#2c2c2b'),spaceAfter=8),
'small':ParagraphStyle('small',fontName='Body',fontSize=9,leading=12,textColor=colors.HexColor('#67645f')),
'cell':ParagraphStyle('cell',fontName='Body',fontSize=9,leading=12,textColor=colors.HexColor('#2c2c2b')),
'h1':ParagraphStyle('h1',fontName='Bold',fontSize=21,leading=25,textColor=colors.HexColor('#2c2c2b')),
'h2':ParagraphStyle('h2',fontName='Bold',fontSize=14,leading=18,textColor=colors.HexColor('#2568a8')),
'code':ParagraphStyle('code',fontName='Body',fontSize=10,leading=14,textColor=colors.HexColor('#2c2c2b'))}
y=0;page=0

def p(text,style='body',gap=8):
 global y
 obj=Paragraph(text,styles[style]);_,h=obj.wrap(AW,1000)
 if y-h<46:raise RuntimeError(f'Overflow page {page}: {text[:70]} y={y} h={h}')
 obj.drawOn(c,M,y-h);y-=h+gap

def title(n,heading):
 global y,page
 if page:c.showPage()
 page=n;y=H-40
 c.setStrokeColor(colors.HexColor('#e6e5e3'));c.line(M,32,W-M,32)
 c.setFont('Body',9);c.setFillColor(colors.HexColor('#67645f'));c.drawString(M,20,'ЛР № 1 · отчёт по предоставленным материалам');c.drawRightString(W-M,20,str(n))
 p(heading,'h1',14)

def img(name,maxh,caption):
 global y
 file=R/'evidence'/name
 im=Image.open(file);iw,ih=im.size;scale=min(AW/iw,maxh/ih);w,h=iw*scale,ih*scale
 if y-h<46:raise RuntimeError(f'Image overflow {page} {name}')
 c.drawImage(str(file.with_suffix('.jpg')),M+(AW-w)/2,y-h,w,h);y-=h+6;p(caption,'small',12)

def table(headers,rows,widths):
 global y
 data=[[Paragraph(str(t),styles['cell']) for t in row] for row in [headers]+rows]
 t=Table(data,colWidths=[AW*x/sum(widths) for x in widths],hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e5f2fc')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.5,colors.HexColor('#d5d3d0')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
 _,h=t.wrap(AW,1000)
 if y-h<46:raise RuntimeError(f'Table overflow {page}: y={y} h={h}')
 t.drawOn(c,M,y-h);y-=h+12

def diagram():
 global y
 top=y;boxes=[(0,100,'Пользователь','слух, осязание'),(139,100,'Скринридер','NVDA / Narrator'),(278,100,'UI Automation','свойства, события'),(417,100,'Приложение','провайдер / дерево'),(139,0,'Синтез речи','звук'),(278,0,'Брайль','строка / дисплей')]
 bottom=top-180
 for x,dy,h,sub in boxes:
  xx=M+x;yy=bottom+dy;ww=94
  c.setFillColor(colors.HexColor('#f9f8f7'));c.setStrokeColor(colors.HexColor('#c6c4c0'));c.roundRect(xx,yy,ww,56,7,fill=1,stroke=1)
  c.setFillColor(colors.HexColor('#2c2c2b'));c.setFont('Bold',9);c.drawCentredString(xx+ww/2,yy+34,h);c.setFont('Body',8);c.drawCentredString(xx+ww/2,yy+17,sub)
 def arrow(x1,y1,x2,y2):
  c.setStrokeColor(colors.HexColor('#2568a8'));c.setFillColor(colors.HexColor('#2568a8'));c.setLineWidth(1.5);c.line(M+x1,bottom+y1,M+x2,bottom+y2)
  import math
  a=math.atan2(y2-y1,x2-x1);q=c.beginPath();q.moveTo(M+x2,bottom+y2);q.lineTo(M+x2-6*math.cos(a-.4),bottom+y2-6*math.sin(a-.4));q.lineTo(M+x2-6*math.cos(a+.4),bottom+y2-6*math.sin(a+.4));q.close();c.drawPath(q,fill=1,stroke=0)
 for a,b in [(94,139),(233,278),(372,417)]:arrow(a,140,b,140)
 for a,b in [(233,278),(372,417)]:arrow(b,116,a,116)
 arrow(186,100,186,56)
 c.line(M+216,bottom+100,M+216,bottom+80);c.line(M+216,bottom+80,M+325,bottom+80);arrow(325,80,325,56)
 c.line(M+139,bottom+28,M+65,bottom+28);arrow(65,28,65,100)
 c.line(M+325,bottom,M+325,bottom-20);c.line(M+325,bottom-20,M+32,bottom-20);arrow(32,-20,32,100)
 c.setFont('Body',8);c.setFillColor(colors.HexColor('#2568a8'));c.drawString(M+97,bottom+164,'Клавиатура →');c.drawString(M+280,bottom+164,'Действия →');c.drawString(M+282,bottom+184,'← данные и события')
 y=bottom-35

# 1
title(1,'Лабораторная работа № 1<br/>Экранный доступ в Windows')
p('От навигации к UI Automation · 27 октября 2026 года','h2')
p('Отчёт составлен по скриншотам команды и исходникам тестовой формы. Ранее вымышленные результаты исключены. Свойства и события, которых нет в материалах, не объявлены измеренными.')
table(['Участник','Раздел оформления'],[
['Дмитрий Ярославов','Разделы «Среда» и «Навигация»'],['Борисов Даниил','Раздел о брайлевском выводе'],['Чуров Александр','Описание объектов'],['Иван Кожухин','Схема и проверки']],[1,2.3])
p('В таблице указаны ответственные за оформление разделов. Учебная группа и дисциплина не сообщены.','small')
table(['Параметр','Подтверждённое значение'],[['ОС','Windows 11 Pro · 26H2 · сборка 26300.9711'],['Скринридер','NVDA 2026.3 (2026.3.0.58174)'],['Браузер','Microsoft Edge']],[1,2.3])
img('environment.webp',182,'Рис. 1. «О системе» и «О NVDA». Значения прочитаны с предоставленного снимка.')
#2
title(2,'Часть 1. Выбранные ресурсы')
p('В материалах представлены Bing, France Football и Transfermarkt. На снимках есть исходные английские и переведённые русские подписи; их формулировки могут различаться между состояниями страницы.')
img('web-search.webp',280,'Рис. 2. В поле Bing введено «france football», раскрыт список подсказок. Клавиши и речь NVDA снимком не зафиксированы.')
img('transfers.webp',255,'Рис. 3. Transfermarkt: открыт раздел «ТРАНСФЕРЫ И СЛУХИ». В адресной строке /navigation/transfersundgeruechte.')
p('Снимки подтверждают открытые страницы и видимое содержимое, но сами по себе не подтверждают навигацию с выключенным экраном.','small')
#3
title(3,'Поиск игрока и аудиопроизношение')
img('player-search.webp',220,'Рис. 4. В поиске введено «Lamin Yamal», в выдаче одна строка «Lamine Yamal». Вокруг текста результата заметна рамка.')
img('player-audio.webp',270,'Рис. 5. Профиль игрока: аудиоплеер показывает 0:03 / 0:03. На кнопке воспроизведения видна рамка.')
p('Подтверждённые наблюдения','h2')
p('В выдаче видны игрок, клуб FC Barcelona и позиция RW. В профиле присутствуют аудиоплеер, регулятор громкости и меню. Рамка около управляющего элемента согласуется с состоянием фокуса, но не заменяет свойства инспектора или запись события FocusChanged.')
p('Отметка времени плеера не доказывает, что звук был слышен. Дословные реплики NVDA, способ активации и персональный исполнитель на снимках отсутствуют.','small')
#4
title(4,'Протокол действий и объекты')
p('Ниже представлены этапы работы и состояния, зафиксированные на изображениях. Точная последовательность нажатий не записана.','body')
table(['№','Этап','Результат на снимке'],[['1','Поиск в Bing','Введено «france football», есть подсказки'],['2','Открытие раздела','Страница Transfermarkt «ТРАНСФЕРЫ И СЛУХИ»'],['3','Поиск игрока','Одна строка «Lamine Yamal» в выдаче'],['4','Просмотр аудио','В профиле плеер 0:03 / 0:03'],['5','Просмотр брайля','Открыто окно NVDA с точками и текстовой строкой']],[.25,1,2])
p('Клавиши, точные реплики, исполнитель каждой строки и отсутствие визуального контроля в предоставленных материалах не зафиксированы.','small')
table(['Объект','Визуальные данные','Роль / имя / состояние UIA'],[['Поле Bing','Текст запроса и подсказки','Не сняты'],['Поле Transfermarkt','Текст «Lamin Yamal»','Не сняты'],['Результат поиска','Текст «Lamine Yamal», рамка','Не сняты'],['Аудиоплеер','Воспроизведение, время, громкость','Не сняты'],['Баннер cookies','Две кнопки на France Football','Не сняты']],[1,1.35,1.1])
img('braille-detail.webp',99,'Рис. 6. Увеличенный фрагмент просмотрщика брайля. Строка: https://www.lequipe.fr/France-Football.')
p('Дословная речь для того же объекта не предоставлена, поэтому сравнение речи и брайля не завершено. Условные сокращения edt/chk из образца не перенесены: на снимке их нет.','small')
#5
title(5,'Брайлевский вывод и архитектура')
img('braille.webp',270,'Рис. 7. Просмотрщик брайля NVDA поверх France Football. Адресная строка браузера показывает francefootball.fr.')
p('В просмотрщике видны брайлевские точки и текст https://www.lequipe.fr/France-Football. Адрес отличается и от адресной строки браузера, и от ссылки статьи в строке состояния; точный источник текущего объекта по снимку не установлен.')
p('Компоненты экранного доступа','h2')
diagram()
p('Устройство ввода передаёт действия пользователя; скринридер обрабатывает собственные команды и преобразует семантику интерфейса в речь и брайль. UIA предоставляет дерево, свойства, события и поддерживаемые действия. NVDA может использовать также другие интерфейсы доступности; конкретный канал по этим снимкам не определяется.','small')
#6
title(6,'Часть 2. Инспекция и события')
p('Объект для изменения кода — собственная HTML-форма из before/after. Скриншоты публичных сайтов части 1 не являются инспекцией этой формы. Снимков Live Inspect, Inspect, Events или AccEvent среди материалов нет.')
table(['Элемент формы','Свойства Windows UIA'],[['searchBtn — кнопка поиска','ControlType, Name, состояния, Patterns и родитель не сняты'],['searchInput — поле поиска','Name, Value, состояния, Patterns и родитель не сняты'],['name — поле имени','Name, Value, состояния, Patterns и родитель не сняты'],['volume — ползунок','Name, RangeValue, состояния и родитель не сняты'],['agree — флажок','Name, ToggleState, Patterns и родитель не сняты']],[1.1,2])
table(['Тип события','Статус в предоставленных данных'],[['FocusChanged','Журнала нет; видимая рамка не равна записи события'],['PropertyChanged / Value','Журнала нет; текст в поле не доказывает тип уведомления'],['WindowOpened','Журнала нет; открытый просмотрщик не доказывает регистрацию']],[1,2])
p('Барьеры в исходном коде локальной формы','h2')
p('<b>1. Кнопка поиска:</b> декоративный SVG скрыт через aria-hidden, текста и aria-label в before нет → не задано понятное доступное имя → назначение может быть неясно → проверить кнопку с NVDA и инспектором.')
p('<b>2. Поле поиска:</b> нет связанного label и aria-label → назначение не задано программной подписью → пользователь может не понять ввод → проверить searchInput в Windows.')
p('Эти дефекты заложены в собственной форме. На основании внешнего вида нельзя объявлять такие же дефекты на Bing, Transfermarkt или France Football.','small')
#7
title(7,'Исправление и выполненные проверки')
p('Код исправления присутствует в проекте. Кнопке добавлено имя, сама иконка осталась прежней. Внутреннее содержимое SVG ниже сокращено многоточием.')
table(['До','После'],[['&lt;button id="searchBtn"&gt;<br/>&nbsp; &lt;svg aria-hidden="true"&gt;…&lt;/svg&gt;<br/>&lt;/button&gt;','&lt;button id="searchBtn"<br/>&nbsp; aria-label="Поиск"&gt;<br/>&nbsp; &lt;svg aria-hidden="true"&gt;…&lt;/svg&gt;<br/>&lt;/button&gt;']],[1,1])
p('Фактические автоматические тесты проекта','h2')
p('В docs/BROWSER-CHECKS.json сохранены реальные проверки Linux Chromium / Playwright. Прошли ввод, ползунок, флажок, локальный поиск, HTML-диалог, возврат фокуса, popup и отсутствие горизонтального переполнения при 390 px. Это не Windows UIA и не NVDA.')
table(['Параметр','Before','After'],[['Браузерный снимок кнопки','- button','- button "Поиск"'],['Активация поиска','Работает','Работает'],['Речь NVDA','Не записана','Не записана'],['Windows UIA Name','Не снято','Не снято']],[1.1,1,1])
table(['Тест','Ожидание','Фактический статус'],[['Позитивный: кнопка','Имя «Поиск»; понятная речь; поиск','Браузерное имя и действие проверены. Windows/NVDA не подтверждены'],['Негативный: поле','Отсутствие подписи сохраняется','В коде label/aria-label нет. Windows-проверка не предоставлена']],[1,1,1.6])
p('Синтетические статусы «пройдено» и реплики из прежнего прототипа удалены из текущего отчёта.','small')
#8
title(8,'Итоговый вывод')
p('Предоставленные материалы показывают работу с несколькими веб-интерфейсами в Windows и открытый просмотрщик брайля NVDA. Версии среды установлены по снимку: Windows 11 Pro 26H2, сборка 26300.9711, и NVDA 2026.3. В просмотрщике отображается адрес https://www.lequipe.fr/France-Football, представленный брайлевскими точками и текстом. Из этого видно, что программа формирует отдельное представление информации об интерфейсе, но без записи речи нельзя провести полное сравнение двух каналов. Скринридеру доступны семантические имена, роли, значения и состояния элементов, которые не определяются только внешним видом. В исходном коде локальной формы добавление aria-label задаёт имя кнопки, не меняя иконку. Автоматическая проверка в Linux Chromium подтвердила изменение браузерного имени, однако она не заменяет UIA/NVDA-тест в Windows. Для завершения лабораторной по всем требованиям остаются нужны реальные протоколы клавиш и речи, свойства пяти элементов, журнал трёх типов событий и Windows-сравнение до и после.')
p('Какие данные ещё нужны','h2')
table(['Требование','Состояние'],[['Версии Windows и NVDA','Подтверждены скриншотом'],['Пять действий со скринридером','Есть пять видимых этапов; клавиши и речь не предоставлены'],['Брайлевский вывод','Есть снимок; речь для того же объекта отсутствует'],['Пять элементов UIA / три типа событий','Снимки инспектора и журнал отсутствуют'],['Исправление одного барьера','Есть в собственном коде; Windows-сравнение не предоставлено']],[1.2,2])
p('Источники и оформление','h2')
p('Шесть снимков команды в текущем чате; исходники before/after; docs/BROWSER-CHECKS.json. Образец PDF использован для структуры, но не как источник результатов. Все присланные снимки включены; их содержание не дорисовывалось.','small')
c.save();print(out)
