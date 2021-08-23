from aiogram import types


async def set_commands(dp):
    commands = [
        types.BotCommand(command="/notes", description="добавь новые заметки"),
        types.BotCommand(command="/new_tasks", description="новые задачи"),
        types.BotCommand(command="/new_context", description="новые контексты"),
        types.BotCommand(command="/plan_for_tomorrow", description="запланировать завтрашний день"),
        types.BotCommand(command="/all_tasks", description="посмотреть все актуальные задачи"),
        types.BotCommand(command="/get_today_plan", description="план на сегодня"),
        types.BotCommand(command="/day_report", description="дневной отчёт"),
        types.BotCommand(command="/special_dates", description="примерные даты"),
    ]
    await dp.bot.set_my_commands(commands)
