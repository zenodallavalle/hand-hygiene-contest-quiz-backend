# Generated by Django 4.2.2 on 2023-06-27 13:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_alter_startevent_job"),
    ]

    operations = [
        migrations.AddField(
            model_name="answerevent",
            name="job",
            field=models.IntegerField(
                choices=[
                    (1, "Medico"),
                    (2, "Professionista sanitario (inferiere, fisioterapista, ecc.)"),
                    (3, "Operatore socio-sanitario"),
                    (4, "Studente di medicina/odontoiatria"),
                    (5, "Studente di professioni sanitarie"),
                    (6, "Nessuna delle precedenti"),
                ],
                default=1,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="resultevent",
            name="job",
            field=models.IntegerField(
                choices=[
                    (1, "Medico"),
                    (2, "Professionista sanitario (inferiere, fisioterapista, ecc.)"),
                    (3, "Operatore socio-sanitario"),
                    (4, "Studente di medicina/odontoiatria"),
                    (5, "Studente di professioni sanitarie"),
                    (6, "Nessuna delle precedenti"),
                ],
                default=1,
            ),
            preserve_default=False,
        ),
    ]
