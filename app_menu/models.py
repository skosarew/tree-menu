from django.db import models


class Category(models.Model):
    title = models.CharField(verbose_name='Title', max_length=255)
    parent = models.ForeignKey(verbose_name='Parent category',
                               to='self', blank=True, null=True,
                               related_name='children',
                               on_delete=models.CASCADE)
    position = models.IntegerField(verbose_name='Position', blank=True,
                                   null=True)
    level = models.IntegerField(blank=True, null=True)
    named_url = models.CharField(max_length=50, default=None, null=True,
                                 unique=True)

    left = models.IntegerField(blank=True, null=True)
    right = models.IntegerField(blank=True, null=True)
    published = models.BooleanField(verbose_name='Published', default=True)

    class Meta:
        ordering = ('left',)

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        self.set_mptt()

    def set_mptt(self, left=1, parent=None, level=1):
        for i in type(self).objects.filter(parent=parent).order_by('position'):
            obj, children_count = i, 0

            for child in obj.children.all():
                children_count += 1
                children_count += self.get_child(child, 0)

            data = {
                'level': level,
                'left': left,
                'right': left + (children_count * 2) + 1
            }
            type(self).objects.filter(id=i.id).update(**data)
            left = data['right'] + 1
            self.set_mptt(left=data['left'] + 1, parent=i.id,
                          level=data['level'] + 1)

    def __str__(self):
        return self.title

    def get_child(self, obj, children_count):
        for child in obj.children.all():
            obj = child
            children_count = self.get_child(obj, children_count) + 1
        return children_count

    def get_elder_ids(self):
        if self.parent:
            return self.parent.get_elder_ids() + [self.parent.id]
        else:
            return []
