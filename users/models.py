from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = ProcessedImageField(blank=True, null=True,
                                default='기본프로필.png', upload_to='profile_pics',
                                processors=[Thumbnail(300, 300)],
                                format='JPEG',
                                options={'quality': 60}, )

    phone_number = models.CharField(blank=True, max_length=20, null=True)
    region = models.CharField(blank=True, max_length=50, null=True)
    nickname = models.CharField(blank=True, null=True, max_length=30)
    # interests = models.ManyToManyField('Interest', max_length=20, blank=True, null=True, related_name='users')

    group = models.ManyToManyField('Group', through='GroupMember', related_name="groups", blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class Interest(models.Model):
    # STATUS_CHOICES = (
    #     ('음식', '음식'),
    #     ('스포츠', '스포츠'),
    #     ('코딩', '코딩'),
    #     ('여행', '여행'),
    #     ('컴퓨터', '컴퓨터'),
    #     ('게임', '게임'),
    #     ('영화', '영화'),
    #     ('언어', '언어'),
    #     ('예술', '예술'),
    #     ('음악', '음악'),
    #     ('경훈', '경훈'),
    # )
    name = models.CharField(max_length=10, blank=True, null=True)


class Group(models.Model):
    group_name = models.CharField(max_length=100)
    group_img = ProcessedImageField(blank=True, null=True,
                                    processors=[Thumbnail(300, 300)],
                                    format='JPEG',
                                    options={'quality': 60}, )
    group_info = models.TextField()
    group_head = models.ForeignKey(User, on_delete=models.CASCADE)
    group_users = models.ManyToManyField(Profile, through='GroupMember', related_name="people")

    GROUP_APPLY_STATUS_CHOICES = (
        ('n', '가입 신청 비허용'),
        ('y', '가입 신청 허용'),
    )
    group_apply_status = models.CharField(
        max_length=1,
        choices=GROUP_APPLY_STATUS_CHOICES,
        default='y',
    )

    GROUP_OPEN_STATUS_CHOICES = (
        ('n', '비공개'),
        ('s', '검색만가능'),
        ('o', '공개'),
    )
    group_open_status = models.CharField(
        max_length=1,
        choices=GROUP_OPEN_STATUS_CHOICES,
        default='o',
    )

    def __str__(self):
        return self.group_name

    # master_id = models.ForeignKey(Profile, related_name="slave_group", on_delete=models.CASCADE)


class GroupMember(models.Model):
    person = models.ForeignKey(Profile, related_name='membership', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='membership', on_delete=models.CASCADE)

    STATUS_CHOICES = (
        ('g', '가입요청'),
        ('u', '가입승인요청'),
        ('a', 'ACCEPTED'),
        ('r', 'REFUSE')
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    GROUP_ROLE = (
        ('h', '관리자'),
        ('m', '그룹 멤버')
    )
    group_role = models.CharField(
        max_length=1,
        choices=GROUP_ROLE,
        default='m',
    )

    @property
    def is_manager(self):
        if self.group_role == 'h':
            return True
        else:
            return False

    @property
    def is_member(self):
        if self.status == 'a':
            return True
        else:
            return False

    def __str__(self):
        return f'{self.id} {self.person} {self.group} {self.status} {self.group_role}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
