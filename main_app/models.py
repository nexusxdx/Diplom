from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse


class Author(models.Model):
    first_name = models.CharField(_('Овог'), max_length=25, blank=True)
    last_name = models.CharField(_('Нэр'), max_length=25)
    image = models.ImageField(_('Зураг'), upload_to="profile_images",
                              default='profile_images/default_user.png',
                              blank=True)
    profession = models.CharField(_('Мэргэжил'), max_length=20, blank=True)
    graduated_school = models.CharField(_('Төгссөн сургууль'), max_length=40, blank=True)
    about = models.TextField(_('Тухай'), blank=True)
    rank = models.CharField(_('Албан тушаал'), max_length=20, blank=True)

    class Meta:
        verbose_name = 'Зохиолч'
        verbose_name_plural = 'Зохиолчид'
        ordering = ('first_name',)

    def get_author_status(self):
        if not self.first_name and not self.profession and not self.graduated_school and not self.rank:
            return False
        else:
            return True

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        if not self.first_name:
            return self.last_name
        else:
            return self.first_name[:1] + ". " + self.last_name

    def __str__(self):
        return self.first_name + " " + self.last_name


class Creation(models.Model):
    languages = (
        ('en', 'English'),
        ('mn', 'Монгол')
    )

    author = models.ForeignKey(Author, related_name="creations", on_delete=models.CASCADE, verbose_name='Зохиолч')
    title = models.CharField(_('Гарчиг'), max_length=150)
    co_authors = models.TextField(_('Хамтран зохиогчид'), )
    type = models.CharField(_('Бүтээлийн төрөл'), max_length=50)
    category = models.CharField(_('Бүтээлийн ангилал'), max_length=50)
    subclass = models.CharField(_('Дэд ангилал'), max_length=50)
    overview = models.TextField(_('Бүтээлийн товч'), )
    keyword = models.CharField(_('Түлхүүр үг'), max_length=100)
    created_date = models.DateField(_('Бүтээл бичигдсэн огноо'), )
    language = models.CharField(_('Хэл'), choices=languages, max_length=10)
    file = models.FileField(_('Файл'), upload_to="files", null=True, blank=True)
    price = models.IntegerField(default=0)
    num_of_page = models.PositiveSmallIntegerField(verbose_name="Хуудасны тоо")
    uploaded_date = models.DateField(auto_now=True, editable=False)
    count_overview = models.IntegerField(default=0, blank=True, editable=False)
    total_downloads = models.IntegerField(default=0, blank=True, editable=False)

    class Meta:
        verbose_name = 'Бүтээл'
        verbose_name_plural = 'Бүтээлүүд'
        ordering = ('-uploaded_date',)

    def get_absolute_url(self):
        return reverse('creation_detail', kwargs={'pk': self.pk})

    def is_paid(self):
        if self.price > 0:
            return True
        else:
            return False

    def __str__(self):
        return self.title


class ViewHit(models.Model):
    model = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='views')
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now=True, editable=False)


class CreationViewHit(models.Model):
    model = models.ForeignKey(Creation, on_delete=models.CASCADE, related_name='views')
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now=True, editable=False)
