from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Pad(models.Model):
    """The room where collaborative editing and chat happens

    """

    owner = models.ForeignKey(User, related_name="pads_owned" ) #User who created Pad
    participants = models.ManyToManyField(User, related_name="pads_memberships")

    guid = models.CharField(max_length=32, unique=True) #md5 hash of `title.lower()`

    title = models.CharField( max_length=255 )
    slug = models.CharField( max_length=255 )
    created_time = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ( ( 'slug', 'owner'), ('title', 'owner') )
        ordering = ('-last_modified', )

    def __unicode__(self):
        return '({user}) -- {title}'.format(
            user=self.owner,
            title=self.title,
        )

    @models.permalink
    def get_absolute_url(self):
        return ( 'pads_detail', (), { 'owner_id': self.owner.id, 'pad_slug': self.slug,  } )

    def save(self):
        self.slug = slugify( self.title )

        # catch non-unique slugs in the form before it comes to this
        # this is like the 'you made a dupe on yourself, now you get a
        # nonsense slug' nonanswer.
        if Pad.objects.filter( owner=self.owner, slug=self.slug ):
            from random import shuffle
            l = list(self.slug)
            shuffle(l)
            self.slug = ''.join(l)
        super(Pad, self).save()

    def delete(self):
        """Delete all associated Revisions

        """

        TextAreaRevision.objects.filter(
                pad_guid=self.pad.guid
        ).delete()

        super(Pad, self).delete()


class TextArea(models.Model):
    """Pad objects can have multiple TextArea objects keyed to them

    """

    pad = models.ForeignKey(Pad)
    content = models.TextField( blank=True,)
    editor = models.ForeignKey(User) #User who edited Pad
    edit_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-edit_time',)

    def __unicode__(self):
        return '{pad} - {content}'.format(
            pad=self.pad,
            content=self.content[:20],
        )

    '''
    def save(self, *args, **kwargs):
        """Save a Revisioned copy after the real save.
        """
        super(TextArea, self).save(*args, **kwargs)
        new_revision = TextAreaRevision()
        new_revision.pad_guid=self.pad.guid
        new_revision.content=self.content
        new_revision.editor=self.editor
        new_revision.edit_time=self.edit_time
        new_revision.save()
    '''

class TextAreaRevision(models.Model):
    """Snapshot of the current TextArea state
    """
    pad_guid = models.CharField(max_length=32)
    content = models.TextField( blank=True )
    editor = models.ForeignKey(User) #User who edited Pad
    edit_time = models.DateTimeField( auto_now_add=True )

    class Meta:
        ordering = ("-edit_time",)

    def __unicode__(self):
        return '{editor} - {time} - {content}'.format(
            editor=self.editor,
            time=self.edit_time,
            content=self.content[:50],
        )

