from django.db import models

class Publication(models.Model):
    """Модель записи в блоге"""
    heading = models.CharField(max_length=150, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    preview = models.ImageField(null=True, upload_to='images/', verbose_name='Превью')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_publicated = models.BooleanField(default=True, verbose_name='Признак публикации')
    views_counter = models.IntegerField(default=0, verbose_name='Счетчик просмотров')

    def __str__(self):
        return f'{self.heading} (опубликовано {self.created_at})'

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'публикации'
        ordering = ['created_at', ]
        db_table = 'publications'
        