from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:category-detail', args=[self.slug])


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="images/%Y/%m/%d/")
    title = models.CharField(max_length=500)
    slug = models.CharField(max_length=500)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.created} || {self.title}"

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse('news:post-detail', args=[self.created.year, self.created.month, self.created.day, self.slug])


class Add(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    url = models.URLField()
    click_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.url

    class Meta:
        ordering = ['is_active']


REGIONS = [
    ('40.8154,72.2837', 'Andijon'),
    ('39.7681,64.4556', 'Buxoro'),
    ('40.3734,71.7978', 'Farg\'ona'),
    ('40.1250,67.8808', 'Jizzax'),
    ('41.0058,71.6436', 'Namangan'),
    ('40.1039,65.3688', 'Navoiy'),
    ('42.4619,59.6166', 'Nukus'),
    ('38.8612,65.7847', 'Qarshi'),
    ('39.6508,66.9654', 'Samarqand'),
    ('40.8373,68.6618', 'Sirdaryo'),
    ('37.2611,67.3086', 'Termiz'),
    ('41.2995,69.2401', 'Toshkent'),
    ('41.2213,69.8597', 'Toshkent vil'),
    ('41.3565,60.8567', 'Xorazm'),
]


class Weather(models.Model):
    location = models.CharField(choices=REGIONS, max_length=30)
    temp = models.FloatField()
    text = models.CharField(max_length=20)
    icon = models.URLField()

    def __str__(self):
        return self.location


SOCIAL_NETWORKS = [
    ('telegram', 'Telegram'),
    ('instagram', 'Instagram'),
    ('facebook', 'Facebook'),
    ('youtube', 'YouTube'),
    ('twitter', 'Twitter'),
]


class SocialAccounts(models.Model):
    name = models.CharField(choices=SOCIAL_NETWORKS, max_length=20, help_text='Social network name')
    url = models.URLField(help_text='Your account URL')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Social Account'
        verbose_name_plural = 'Social Accounts'


class FooterData(models.Model):
    phone_number = PhoneNumberField(help_text='Your phone number')
    email = models.EmailField(help_text='Your e-mail address')

    def __str__(self):
        return f"{self.email, self.phone_number}"
