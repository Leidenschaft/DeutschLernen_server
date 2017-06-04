# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-03 18:08
from __future__ import unicode_literals

from django.db import migrations, models
from lxml import etree
my_choice=(
    ('T', 'Text'),
    ('I', 'Intentionen'),
    ('L', 'Leseverstehen'),
    ('E','Einführung'),
    ('U','Übungen'),
    ('H','Hörverstehen'),
    ('O','Others'),
    )
my_choice_dic={'Text':'T',
               'Intentionen':'I',
               'Leseverstehen':'L',
               'Einführung':'E',
               'Übungen':'U',
               'Hörverstehen':'H',
               }
def add_einheit_anteil(apps,schema_editor):
    Word=apps.get_model("DeutschLernen","Word")
    i=1
    while(i<465):
        f=open('E:/DeutschLernen/Deutsch-Lernen/Deutsch-Lernen/Wort/%d.xml'%i,'rb')
        st=f.read()
        root=etree.fromstring(st)
        u=Word.objects.get(xml_file_name='N'+str(i)+'.xml')
        u.enheit=int(root[1].text)
        if(my_choice_dic.get(root[2].text)):
            u.anteil=my_choice_dic[root[2].text]
        else:
           u.anteil='O';
        u.save()
        i=i+1


class Migration(migrations.Migration):

    dependencies = [
        ('DeutschLernen', '0005_merge_20170403_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='anteil',
            field=models.CharField(blank=True,null=True,choices=my_choice, default='T', max_length=1),
        ),
        migrations.AddField(
            model_name='word',
            name='einheit',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.RunPython(add_einheit_anteil),
    ]
