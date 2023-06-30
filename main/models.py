from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from main.post_save_checks import check_captcha_token, trace_ip
from threading import Thread

# Create your models here.


class JobChoices(models.IntegerChoices):
    MEDICO = 1, "Medico/odontoiatra"
    PROF_SAN = 2, "Professionista sanitario (infermiere, fisioterapista, ecc.)"
    OSS = 3, "Operatore socio-sanitario"
    MED_STU = 4, "Studente di medicina/odontoiatria"
    PROF_SAN_STU = 5, "Studente di professioni sanitarie"
    OTHER_HEALTH = 6, "Altra tipologia di operatore sanitario"
    OTHER_NOT_HEALTH = 7, "Non operatore sanitario"


class DeviceChoices(models.IntegerChoices):
    MOBILE = 1, "Mobile"
    TABLET = 2, "Tablet"
    DESKTOP = 3, "Desktop"
    OTHER = 4, "Altro"


class StartEvent(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    device_uid = models.CharField(max_length=100)
    device_type = models.IntegerField(choices=DeviceChoices.choices, null=True)
    ip = models.CharField(max_length=100)
    user_agent = models.CharField(max_length=1000)
    referrer = models.CharField(max_length=1000, null=True)

    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    country_code = models.CharField(max_length=100, null=True)
    country_name = models.CharField(max_length=100, null=True)
    province = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=100, null=True)

    isp = models.CharField(max_length=1000, null=True)

    recaptcha_token = models.CharField(max_length=2000)
    recaptcha_score = models.FloatField(null=True)

    quiz_uid = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)

    job = models.IntegerField(choices=JobChoices.choices)

    def __str__(self):
        return f"[{self.datetime}] [{self.quiz_uid}] [{self.device_uid}] [{self.ip}] {self.nickname}"

    def __repr__(self) -> str:
        return f"<StartEvent {self.datetime} {self.quiz_uid} {self.device_uid} {self.ip}: {self.nickname}>"


class AnswerEvent(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    device_uid = models.CharField(max_length=100)
    device_type = models.IntegerField(choices=DeviceChoices.choices, null=True)
    ip = models.CharField(max_length=100)
    user_agent = models.CharField(max_length=1000)

    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    recaptcha_token = models.CharField(max_length=2000)
    recaptcha_score = models.FloatField(null=True)

    nickname = models.CharField(max_length=100)
    job = models.IntegerField(choices=JobChoices.choices)

    quiz_uid = models.CharField(max_length=100)

    question_id = models.IntegerField()
    answer_id = models.IntegerField()
    question_text = models.TextField()
    answer_text = models.TextField()

    def __str__(self):
        return f"[{self.datetime}] [{self.quiz_uid}] [{self.device_uid}] [{self.ip}] [{self.nickname}] answer_id {self.answer_id} to question_id {self.question_id}"

    def __repr__(self) -> str:
        return f"<AnswerEvent {self.datetime} {self.quiz_uid} {self.device_uid} {self.ip} {self.nickname}: answer_id {self.answer_id} to question_id {self.question_id}>"


class ResultEvent(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    device_uid = models.CharField(max_length=100)
    device_type = models.IntegerField(choices=DeviceChoices.choices, null=True)
    ip = models.CharField(max_length=100)
    user_agent = models.CharField(max_length=1000)

    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    recaptcha_token = models.CharField(max_length=2000)
    recaptcha_score = models.FloatField(null=True)

    nickname = models.CharField(max_length=100)
    job = models.IntegerField(choices=JobChoices.choices)

    quiz_uid = models.CharField(max_length=100)

    marks = models.IntegerField()

    def __str__(self):
        return f"[{self.datetime}] [{self.quiz_uid}] [{self.device_uid}] [{self.ip}] [{self.nickname}] {self.marks}"

    def __repr__(self) -> str:
        return f"<ResultEvent {self.datetime} {self.quiz_uid} {self.device_uid} {self.ip} {self.nickname}: {self.marks}>"


@receiver(post_save, sender=StartEvent)
@receiver(post_save, sender=AnswerEvent)
@receiver(post_save, sender=ResultEvent)
def retrace_captcha(sender, instance, created, **kwargs):
    if created:
        if not instance.recaptcha_score:
            # Check score
            t = Thread(target=check_captcha_token, args=(instance,))
            t.start()
        if not instance.latitude and not instance.longitude:
            # Trace IP
            t = Thread(target=trace_ip, args=(instance,))
            t.start()
