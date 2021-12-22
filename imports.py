import asyncio
import datetime as dt
import json
import os
import random
import re
import typing as t
from os import error

import aiohttp
import discord
import discord_slash
import pymongo
import wavelink
from discord import channel, client, colour
from discord.ext import commands
from discord.ext.commands import context
from discord.ext.commands.core import command, has_permissions
from discord.flags import alias_flag_value
from discord.webhook import AsyncWebhookAdapter
from discord_slash import SlashCommand, cog_ext
from pymongo import MongoClient as mc
from pymongo import collection, database

from lists import *