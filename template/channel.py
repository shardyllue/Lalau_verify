from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


mute_message = """
<b>Вирт в канале только по подписке.</b>
"""

goto = "Перейти в бота"


mute_add = """
<b>Слово(вa) <i>{word}</i> обозначено(ны) как запрещеное(ный)!</b> 
"""

mute_remove = """
<b>Слово(вa) <i>{word}</i> было(и) удалено(ы) из списка запрещенных слов!</b> 
"""

mute_list = """
<b>Список запрещенных слов:</b>

<i>{words}</i>

<b>Команды:</b>

<b>/mute add слово1 слово2</b>
<i>Добивть слова в список</i>

<b>/mute remove слово1 слово2</b>
<i>Удалить слова из списка</i>

<b>/mute</b>
<i>Список всех слов</i> 
"""


channel_text = """
<b>Хочешь найти</b> спонсора или содержанку? 
<b>Используй все проекты lalau!</b>

<b>1.</b> Черный список спонсоров.
<b>2.</b> Мужской клуб lalau.
<b>3.</b> Виртуальное общение.
<b>4.</b> Premium🏆 канал lalau.
Всё это в: @Lalau_verify_bot

🏙️Чаты по городам: @lalau_city
📜Доска объявлений: @lalau_ru
♥️Бот знакомств: @Lalau_love_bot

⛔️<b>Запрещены в канале:</b>
Прайсы, услуги проституции, наркотики, реклама, 
спам, несовершеннолетние, продажа фото и записанных видео.

<b>Удачного тебе поиска!</b>🥳
"""

channel_kb = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="Проекты lalau😁", 
        url="t.me/Lalau_verify_bot"
    )
)