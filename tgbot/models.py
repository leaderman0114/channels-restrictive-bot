from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True


class Group(BaseModel):
    chat_id = models.BigIntegerField()
    username = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)


class Channel(models.Model):
    ALLOWED = 'allowed'
    BANNED = 'banned'
    MODES = (
        (ALLOWED, ALLOWED),
        (BANNED, BANNED)
    )
    mode = models.CharField(max_length=20, default=ALLOWED)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    chat_id = models.BigIntegerField()
    username = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)

    @classmethod
    def ban(self, channel_id, channel_username=None, channel_title=None):
        banned = True
        try:
            channel = self.objects.get(
                chat_id=channel_id,
                )
            channel: self
            channel.mode = self.BANNED
            channel.username=channel_username,
            channel.title=channel_title
            channel.save()

        except self.DoesNotExist:
            self.objects.create(
                chat_id=channel_id,
                username=channel_username,
                title=channel_title,
                mode=self.BANNED
            )
        except Exception:
            banned = False

        finally:
            return {
                'status': banned,
                'message': 'The channel is banned!'
            }
    @classmethod
    def allow(self, channel_id):
        allowed = True
        try:
            channel = self.objects.get(
                channel_id=channel_id
                )
            channel: self
            channel.mode = self.ALLOWED
            channel.save()

        except self.DoesNotExist:
            self.objects.create(
                channel_id=channel_id,
                mode=self.ALLOWED
            )
        except Exception:
            allowed = False

        finally:
            return {
                'status': allowed,
                'message': 'The channel is allowed!'
            }
