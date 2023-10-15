from django.db import models

from wagtail.models import Page
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField



class Events(Page):
    parent_page_types = []
    subpage_types = ["Event"]


class Event(Page):
    parent_page_types = ["Events"]
    subpage_types = ["Hall", "Game"]

    #title
    is_public = models.BooleanField(default=True, verbose_name="Видно всем")
    is_free = models.BooleanField(default=True, verbose_name="Присоедениться могут все", help_text="Если вход ограничен, обязательно отключите")
    photo = models.ImageField(verbose_name="Фото", blank=True, null=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    FAQs = models.TextField(verbose_name="FAQs", blank=True, null=True)
    website = models.URLField(verbose_name="Сайт организации", blank=True, null=True)
    organizers_contacts = models.TextField(verbose_name="Контакты оранизатора", blank=True, null=True)
    start_datetime = models.DateTimeField(verbose_name="Время начала", blank=True, null=True)
    end_datetime = models.DateTimeField(verbose_name="Время конца", blank=True, null=True)
    enter_GPS_lat = models.FloatField(verbose_name="GPS (широта) входа", blank=True, null=True)
    enter_GPS_lon = models.FloatField(verbose_name="GPS (долгота) входа", blank=True, null=True)
    enter_text = models.TextField(verbose_name="Как добараться?", blank=True, null=True)
    area_GPS = models.TextField(verbose_name="Облась мероприятия", blank=True, null=True, help_text="Пары значений (GPS широта и долгота) разеделенные переносом строки, обочающий зону мероприятия на карте")

    content_panels = Page.content_panels + [
        FieldPanel("is_public"),
        FieldPanel("is_free"),
        FieldPanel("photo"),
        FieldPanel("description"),
        FieldPanel("FAQs"),
        FieldPanel("website"),
        FieldPanel("organizers_contacts"),
        FieldPanel("start_datetime"),
        FieldPanel("end_datetime"),
        FieldPanel("enter_GPS_lat"),
        FieldPanel("enter_GPS_lon"),
        FieldPanel("enter_text"),
        FieldPanel("area_GPS"),
    ]


class Hall(Page):
    parent_page_types = ["Event"]
    subpage_types = ["Performance"]

    #title
    photo = models.ImageField(verbose_name="Фото", blank=True, null=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    enter_GPS_lat = models.FloatField(verbose_name="GPS (широта) входа", blank=True, null=True)
    enter_GPS_lon = models.FloatField(verbose_name="GPS (долгота) входа", blank=True, null=True)
    enter_text = models.TextField(verbose_name="Как добараться?", blank=True, null=True)
    area_GPS = models.TextField(verbose_name="Облась мероприятия", blank=True, null=True, help_text="Пары значений (GPS широта и долгота) разеделенные переносом строки, обочающий зону мероприятия на карте")

    content_panels = Page.content_panels + [
        FieldPanel("photo"),
        FieldPanel("description"),
        FieldPanel("enter_GPS_lat"),
        FieldPanel("enter_GPS_lon"),
        FieldPanel("enter_text"),
        FieldPanel("area_GPS"),
    ]


class Performance(Page):
    parent_page_types = ["Hall"]
    subpage_types = []

    #title
    photo = models.ImageField(verbose_name="Фото", blank=True, null=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    start_datetime = models.DateTimeField(verbose_name="Время начала", blank=True, null=True)
    end_datetime = models.DateTimeField(verbose_name="Время конца", blank=True, null=True)
    leads_text = models.TextField(verbose_name="Выступают", blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("photo"),
        FieldPanel("description"),
        FieldPanel("start_datetime"),
        FieldPanel("end_datetime"),
        FieldPanel("leads_text"),
    ]


class GamePoint(blocks.StructBlock):
    Performance_or_hall = blocks.PageChooserBlock(page_type=["Events.Hall", "Events.Performance"], help_text="Это выступление или зал будет связан с этим пунтом игры, учанитик получит информацию", required=False)
    text = blocks.TextBlock(help_text="Этот текст будет высвечиться вместе с сообщением о выступлении или зале, это может быть например загадка")   
    answers = blocks.TextBlock(help_text="Правильные варинты ответа по каждому на строку, регистр, пробельные и служебные символы  не учиываеються", required=False)


class Game(Page):
    parent_page_types = ["Event"]
    subpage_types = []

    #title
    photo = models.ImageField(verbose_name="Фото", blank=True, null=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    points = StreamField([('point', blocks.ListBlock(GamePoint()))], use_json_field=True, min_num=1, verbose_name="Точки игры", help_text="Игра считается пройдейнной, если учасник прошел через вссе")
    

    content_panels = Page.content_panels + [
        FieldPanel("photo"),
        FieldPanel("description"),
        FieldPanel("points"),
    ]


class TelegramUsers(models.Model):
    telegram_id = models.IntegerField(unique=True, primary_key=True)
    telegram_username = models.IntegerField(unique=True)
    #participated_in_events = models.ManyToManyField(Event)
    #participated_in_games = models.ManyToManyField(Game)


class GamePoint2TelegramUsers(models.Model):
    telegram_id = models.IntegerField()
    game_id = models.IntegerField()
    point_hash = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)


class Partisipatment(models.Model):
    telegram_id = models.IntegerField()
    page_id = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)
