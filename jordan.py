import inspect
import typing as t

import hikari


class PrefixCommand:
    def __init__(
        self,
        name: str,
        callback: t.Callable[..., t.Awaitable[None]]
    ):
        self.name = name.lower()
        self.callback = callback


PrefixType = str | t.Callable[
    [hikari.MessageCreateEvent],
    t.Awaitable[str] | str
]


class PrefixHandler:
    def __init__(
        self,
        bot: hikari.GatewayBot,
        prefix: PrefixType
    ):
        self.bot = bot
        self.prefix = prefix
        self.commands: dict[str, PrefixCommand] = {}

        self.bot.listen(hikari.MessageCreateEvent)(
            self._process_commands
        )

    def command(self, name: str):
        def decorator(
            func: t.Callable[..., t.Awaitable[None]]
        ):
            command = PrefixCommand(name, func)
            self.commands[command.name] = command
            return func

        return decorator

    async def get_prefix(
        self,
        event: hikari.MessageCreateEvent
    ) -> str:
        if callable(self.prefix):
            value = self.prefix(event)

            if inspect.isawaitable(value):
                value = await value

            return value

        return self.prefix

    async def _process_commands(
        self,
        event: hikari.MessageCreateEvent
    ) -> None:
        if event.is_bot or not event.content:
            return

        prefix = await self.get_prefix(event)
        used_prefix = None

        if event.content.startswith(prefix):
            used_prefix = prefix
        else:
            me = self.bot.get_me()

            if me:
                for mention in (
                    f"<@{me.id}>",
                    f"<@!{me.id}>"
                ):
                    if event.content.startswith(mention):
                        used_prefix = mention
                        break

        if used_prefix is None:
            return

        payload = event.content[len(used_prefix):].strip()

        if not payload:
            return

        parts = payload.split()

        command_name = parts[0].lower()
        args = parts[1:]

        command = self.commands.get(command_name)

        if command is None:
            return

        try:
            await command.callback(event, args)
        except Exception as error:
            print(f"❌ Error in '{command_name}': {error}")
            await event.message.respond(
                "⚠️ Something went wrong while running that command."
            )