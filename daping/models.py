# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class OriginalEvents(models.Model):
    index = models.IntegerField(db_column='ID')  # Field name made lowercase.
    newst = models.DateTimeField(db_column='NewsT')  # Field name made lowercase.
    province = models.CharField(db_column='Province', max_length=10)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=10, blank=True, null=True)  # Field name made lowercase.
    district = models.CharField(db_column='District', max_length=10, blank=True, null=True)  # Field name made lowercase.
    casualty = models.IntegerField(db_column='Casualty', blank=True, null=True)  # Field name made lowercase.
    reason = models.CharField(db_column='Reason', max_length=20, blank=True, null=True)  # Field name made lowercase.
    link = models.CharField(db_column='Link', max_length=150, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'original_events'

class RankingList(models.Model):
    district = models.CharField(db_column='district', max_length=10, blank=True, primary_key =True)  # Field name made lowercase.
    DistrictCounts = models.IntegerField(db_column='DistrictCounts', blank=True, null=False)  # Field name made lowercase.
    class Meta:
         managed = False
         db_table = 'ranking_list'
      
class Monthcountall(models.Model):
    month = models.CharField(db_column='month', max_length=10, blank=True, primary_key =True)  # Field name made lowercase.
    AllCounts = models.IntegerField(db_column='AllCounts', blank=True, null=False)  # Field name made lowercase.
    class Meta:
         managed = False
         db_table = 'month_countall'


class Monthcountly(models.Model):
    month = models.CharField(db_column='month', max_length=10, blank=True, primary_key =True)  # Field name made lowercase.
    LyCounts = models.IntegerField(db_column='LyCounts', blank=True, null=False)  # Field name made lowercase.
    class Meta:
         managed = False
         db_table = 'month_countly'         

class RegionCount(models.Model):
    province = models.CharField(db_column='Province', max_length=10,blank=True, primary_key =True)  # Field name made lowercase.
    regioncounts = models.IntegerField(db_column='RegionCounts', blank=True, null=True)   # Field name made lowercase.

    class Meta:
         managed = False
         db_table = 'region_count'

class EventsReason(models.Model):
    reason = models.CharField(db_column='Reason', max_length=50, blank=True, null=False, primary_key =True)  # Field name made lowercase.
    reasoncounts = models.IntegerField(db_column='ReasonCounts', blank=True, null=True)  # Field name made lowercase.

    class Meta:
         managed = False
         db_table = 'events_reason'

class MonthCountavgm(models.Model):
	month = models.IntegerField(db_column='month', blank=True, primary_key =True)
	AvgmCounts = models.FloatField(db_column='AvgmCounts', max_length=3, blank=True, null=True)
	class Meta:
		managed = False
		db_table = 'month_countavgm'

class MonthCountavgy(models.Model):
	AvgyCounts = models.FloatField(db_column='AvgyCounts', max_length=3, blank=True, primary_key=True)
	class Meta:
		managed = False
		db_table = 'month_countavgy'