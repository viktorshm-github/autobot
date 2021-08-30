from django.core.management.base import BaseCommand
from django.conf import settings

from typing import Tuple, Dict, Any

from tg_bot import models

from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CallbackContext, Filters, MessageHandler, CommandHandler, Updater, ConversationHandler, CallbackQueryHandler
from telegram.utils.request import Request

SELECTED_CAR, UNREGISTERED, NEW_CAR, CAR_INFO, STOPPING = map(chr, range(5))
ADD_CAR, LABEL_INFO = map(chr, range(5,7))
REFUELING, MAINTENANCE, INSURANCE, TIRES, PARKING, TOLL_ROAD, FINE, REG_NUM = map(chr, range(7,15))

# Shortcut for ConversationHandler.END
END = ConversationHandler.END

TEXTS = {
    REFUELING: f'Тааак, заправка... \nВведи через пробел:\nСумму, литры и пробег',
    MAINTENANCE: f'Молодец, ТО важно!\nВведи через пробел:\nСумму и пробег',
    INSURANCE: f'Без страховки страшновато...\nВведи через пробел:\nСумму и пробег',
    TIRES: f'О! Новые тапки!\nВведи через пробел:\nСумму и пробег',
    PARKING: f'Платим за стояночку\nВведи через пробел:\nСумму и пробег',
    TOLL_ROAD: f'Платная дорога\nВведи через пробел:\nСумму и пробег',
    FINE: f'Оплата штрафов\nВведи через пробел:\nСумму и пробег',
}

def registration_user(user_id: int, user_name: str) -> 'Profile':
    obj, created = models.Profile.objects.get_or_create(
    tg_id=user_id,
    tg_name=user_name,
)
    return obj

def get_car_list(user) -> list:
    return models.Automobile.objects.filter(owner=user)

def parse_data(q_label, q_data):
    car = q_data[REG_NUM]
    if q_label in q_data:
        data = q_data[q_label]
        db_car = models.Automobile.objects.get(reg_num=car)
        current_mileage = models.Refuilings.objects.filter(car=db_car).order_by('-car_mileage')

        if len(current_mileage)>0:
            t = int(current_mileage[0].car_mileage)
            s = int(data[::-1][0])
            if (s-t) <= 0:
                q_data.pop(q_label, None)
                return False


        if len(data) > 3:
            return False
        if len(data)==1:
            record = models.Refuilings.objects.create(car=db_car, cost_type=q_label, cost_summ=data[0])
        if len(data)==2:
            record = models.Refuilings.objects.create(car=db_car, cost_type=q_label, cost_summ=data[0], car_mileage=data[1])
        if len(data)==3:
            prs0, prs1 = str(data[0]), str(data[1])
            pr0, prs1 = prs0.replace(',','.'), prs1.replace(',','.')
            try:
                prs0, prs1 = float(prs0), float(prs1)
            except:
                return False
            record = models.Refuilings.objects.create(car=db_car, cost_type=q_label, cost_summ=prs0, car_mileage=data[2], liters=prs1)

        q_data.pop(q_label, None)
    return True

def start(update: Update, context: CallbackContext) -> str:
    user = update.effective_user
    profile = registration_user(user.id, user.name)
    car_list = get_car_list(profile)
    if len(car_list) == 0:
        text = f"Привет {user.name}!  У тебя еще нет машин. Добавь хотябы одну, что бы вести учёт расходов."
        buttons = [
            [
                InlineKeyboardButton(text='Добавить машину', callback_data=str(ADD_CAR)),
            ],
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        update.message.reply_text(text=text, reply_markup=keyboard)
        return NEW_CAR
    else:
        text = f"Привет {user.name}!  Выбери авто, для которой нужно учитывать расходы."
        butts = [InlineKeyboardButton(text=f'{car}', callback_data=f'{car.reg_num}') for car in car_list]
        buttons = [
            butts,
            [
                InlineKeyboardButton(text='Добавить машину', callback_data=str(ADD_CAR)),
            ],
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        update.message.reply_text(text=text, reply_markup=keyboard)
        return SELECTED_CAR

def add_expense(update: Update, context: CallbackContext) -> str:

    car_reg_num = update.callback_query.data
    user_data = context.user_data
    user_data[REG_NUM] = car_reg_num

    text = "Отлично! Что хочешь заполнить?"

    buttons = [
        [
            InlineKeyboardButton(text='Заправка', callback_data=str(REFUELING)),
            InlineKeyboardButton(text='ТО', callback_data=str(MAINTENANCE)),
        ],
        [
            InlineKeyboardButton(text='Штраф', callback_data=str(FINE)),
            InlineKeyboardButton(text='Парковка', callback_data=str(PARKING)),
        ],
        [
            InlineKeyboardButton(text='Платная дорога', callback_data=str(TOLL_ROAD)),
            InlineKeyboardButton(text='Страховка', callback_data=str(INSURANCE)),
        ],
        [
            InlineKeyboardButton(text='Шины', callback_data=str(TIRES)),
            InlineKeyboardButton(text='Закончить', callback_data=str(END)),
        ],
    ]

    keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return CAR_INFO

def collect_data(update: Update, context: CallbackContext) -> str:

    q = context.user_data[LABEL_INFO]
    inform = str(update.message.text).split()
    context.user_data[q] = inform

    if parse_data(q, context.user_data):
        text = f'Готово. Что-то еще?'
    else:
        text = f'Неа. Что-то пошло не так.\nПопробуй еще раз.'
    buttons = [
        [
            InlineKeyboardButton(text='Заправка', callback_data=str(REFUELING)),
            InlineKeyboardButton(text='ТО', callback_data=str(MAINTENANCE)),
        ],
        [
            InlineKeyboardButton(text='Штраф', callback_data=str(FINE)),
            InlineKeyboardButton(text='Парковка', callback_data=str(PARKING)),
        ],
        [
            InlineKeyboardButton(text='Платная дорога', callback_data=str(TOLL_ROAD)),
            InlineKeyboardButton(text='Страховка', callback_data=str(INSURANCE)),
        ],
        [
            InlineKeyboardButton(text='Шины', callback_data=str(TIRES)),
            InlineKeyboardButton(text='Закончить', callback_data=str(END)),
        ],
    ]

    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(text=text, reply_markup=keyboard)

    return CAR_INFO


def stop(update: Update, context: CallbackContext) -> int:
    """End Conversation by command."""
    update.message.reply_text('Okay, bye.')
    return END

def set_data(update: Update, context: CallbackContext) -> int:
    tq = update.callback_query.data
    text = TEXTS[tq]
    context.user_data[LABEL_INFO] = tq

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)
    return CAR_INFO

class Command(BaseCommand):
    help = 'Этот бот призван записывать все расходы на Автомобиль'

    def handle(self, *args, **options):
        bot = Bot(token=settings.TG_TOKEN, base_url=settings.TG_PROXY)
        updater = Updater(bot=bot, use_context=True)

        car_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(add_expense)],
            states={
                CAR_INFO: [
                    CallbackQueryHandler(set_data, pattern=f'^{REFUELING}$|^{MAINTENANCE}$|^{FINE}$|^{PARKING}$|^{TOLL_ROAD}$|^{INSURANCE}$|^{TIRES}$'),

                    MessageHandler(Filters.text & ~Filters.command, collect_data)
                ],
            },
            fallbacks=[CommandHandler('stop', stop)],
            map_to_parent={
                # Return to second level menu
                END: END
            },
        )

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                SELECTED_CAR: [car_handler],
                NEW_CAR: [],
                UNREGISTERED: [
                    ],

                STOPPING: [CommandHandler('start', start)],
            },
            fallbacks=[CommandHandler('stop', stop)],
        )

        updater.dispatcher.add_handler(conv_handler)

        updater.start_polling()
        updater.idle()
