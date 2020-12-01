# Generated by Django 2.2.10 on 2020-11-29 21:31

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_auto_20201129_2039'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='survey.Participant', verbose_name='участник')),
                ('scheme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='survey.Scheme', verbose_name='опрос')),
            ],
            options={
                'verbose_name': 'пройденный опрос',
                'verbose_name_plural': 'пройденные опросы',
                'ordering': ['-scheme'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='answer',
            name='participant',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='question',
        ),
        migrations.CreateModel(
            name='SurveyQuestion',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_question', to='survey.Question', verbose_name='вопрос')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_question', to='survey.Survey', verbose_name='пройденный опрос')),
            ],
            options={
                'verbose_name': 'связь вопросов с пройденными опросами',
                'verbose_name_plural': 'связи вопросов с пройденными опросами',
                'unique_together': {('survey', 'question')},
            },
        ),
        migrations.CreateModel(
            name='SurveyAnswer',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_answer', to='survey.Answer', verbose_name='ответ')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_answer', to='survey.Survey', verbose_name='опрос')),
            ],
            options={
                'verbose_name': 'связь ответов с пройденными опросами',
                'verbose_name_plural': 'связи ответов с пройденными опросами',
                'unique_together': {('survey', 'answer')},
            },
        ),
        migrations.CreateModel(
            name='SchemeQuestion',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scheme_question', to='survey.Question', verbose_name='вопрос')),
                ('scheme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scheme_question', to='survey.Scheme', verbose_name='опрос')),
            ],
            options={
                'verbose_name': 'связь вопросов с опросами',
                'verbose_name_plural': 'связи вопросов с опросами',
                'unique_together': {('scheme', 'question')},
            },
        ),
        migrations.CreateModel(
            name='AnswerQuestion',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_question', to='survey.Answer', verbose_name='ответ')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_question', to='survey.Question', verbose_name='вопрос')),
            ],
            options={
                'verbose_name': 'связь ответов с вопросами',
                'verbose_name_plural': 'связи ответов с вопросами',
                'unique_together': {('answer', 'question')},
            },
        ),
    ]