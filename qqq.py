import inspect
import autogen_agentchat.teams as teams

for name, obj in teams.__dict__.items():
    if inspect.isclass(obj):
        print(name)