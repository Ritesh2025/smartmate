# Generated by Django 4.1.1 on 2023-05-17 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartmate__1', '0002_facultydetail_did_fk_studentdetail_cid_fk_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='cid_fk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='smartmate__1.coursedetail'),
        ),
        migrations.AddField(
            model_name='studentdetail',
            name='access_stu',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='coursedetail',
            name='cid',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='departmentdetail',
            name='did',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='facultydetail',
            name='fid',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='note',
            name='note_id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='studentdetail',
            name='sid',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='subject',
            name='sub_id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]