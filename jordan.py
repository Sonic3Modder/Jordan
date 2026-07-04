import typing as t
import hikari

class PrefixCommand:
    def __init__(self, name: str, callback: t.Callable[..., t.Awaitable[None]]):
        self.name = name.lower()
        self.callback = callback

class PrefixHandler:
    def __init__(self, bot: hikari.GatewayBot, prefix: str):
        self.bot = bot
        self.prefix = prefix
        self.commands: t.Dict[str, PrefixCommand] = {}

        # Hooks the listener automatically
        self.bot.listen(hikari.MessageCreateEvent)(self._process_commands)

    def command(self, name: str):
        def decorator(func: t.Callable[..., t.Awaitable[None]]):
            cmd = PrefixCommand(name, func)
            self.commands[cmd.name] = cmd
            return func
        return decorator

    async def _process_commands(self, event: hikari.MessageCreateEvent) -> None:
        if event.is_bot or not event.content:
            return

        if not event.content.startswith(self.prefix):
            return

        raw_payload = event.content[len(self.prefix):].strip().split()
        if not raw_payload:
            return

        command_name = raw_payload[0].lower()
        args = raw_payload[1:]

        if command_name in self.commands:
            try:
                await self.commands[command_name].callback(event, args)
            except Exception as error:
                print(f"❌ Error in command '{command_name}': {error}")
                await event.message.respond("⚠️ Something went wrong while running that command.")
