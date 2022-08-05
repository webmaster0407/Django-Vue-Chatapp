import Accounts.util
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import encrypted_fields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=Accounts.util.user_directory_path)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('first', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_thread_first', to=settings.AUTH_USER_MODEL)),
                ('second', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_thread_second', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('first', 'second')},
            },
        ),
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_message', encrypted_fields.fields.EncryptedTextField(blank=True)),
                ('read', models.BooleanField(default=False)),
                ('last_message_from', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_message_user', to=settings.AUTH_USER_MODEL)),
                ('second', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inbox_second_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inbox_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Inbox',
                'verbose_name_plural': 'User Inbox',
                'unique_together': {('user', 'second')},
            },
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', encrypted_fields.fields.EncryptedTextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('attachment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Chat.Attachment')),
                ('inbox', models.ManyToManyField(blank=True, to='Chat.Inbox')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_receiver', to=settings.AUTH_USER_MODEL, verbose_name='receiver')),
                ('thread', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Chat.Thread')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_sender', to=settings.AUTH_USER_MODEL, verbose_name='sender')),
            ],
        ),
    ]
