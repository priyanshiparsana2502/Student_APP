# Generated by Django 3.1.2 on 2020-10-17 17:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.IntegerField(choices=[('0', 'Cancelled'), ('1', 'Confirmed'), ('2', 'On Hold')], default='1', max_length=1)),
                ('order_date', models.DateField(default=django.utils.timezone.now)),
                ('courses', models.ManyToManyField(to='myapp.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='myapp.student')),
            ],
        ),
    ]
